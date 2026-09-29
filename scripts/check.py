#!/usr/bin/env python3
"""Offline consistency checks for this repository. Standard library only.

    python3 scripts/check.py                    # every push (CI)
    python3 scripts/check.py --strict           # also fail on publish placeholders
    python3 scripts/check.py --max-age-days 45  # monthly: "last verified" dates must be recent
    python3 scripts/check.py --online           # manual: external links answer (network)

Checks:
  1. wording: banned phrases and the other site's name, zero tolerance, in every
     text file. The word list is stored base64-encoded below so that this file
     does not contain the words it forbids.
  2. self links: only README.md (2) and docs/order-status-glossary.md (1) may
     link to kaigpt.ai, and every such link carries utm_source=github.
  3. session rule: any file that mentions kaigpt.pro also says not to send
     passwords, codes or the session to anyone, customer service included.
  4. relative links and #anchors resolve (GitHub heading slugs).
  5. checklist.json: ids unique, 7 checks and 9 scam signals, every doc anchor exists.
  6. every page states "最后核实：YYYY-MM-DD" with a valid date.
  7. publish placeholders (kaigpt-ai) are replaced (--strict only).
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
TEXT_SUFFIXES = {".md", ".json", ".txt", ".cff", ".yml", ".yaml", ".py", ".html"}

_TERMS_B64 = (
    "eyJiYW5uZWQiOiBbWyLlrpjmlrl85a6Y572RIiwgIuWGmeOAjE9wZW5BSSDluK7liqnkuK3lv4Pj"
    "gI3jgIxPcGVuQUkg5L2/55So5p2h5qy+44CN6L+Z57G75YW35L2T5ZCN56ewIl0sIFsi5o6I5p2D"
    "fOato+inhHzmnoHpgJ9856eS5YiwfOS/neivgeWIsOi0pnzlronlhajnqLPlrpp86Zu26aOO6Zmp"
    "fOawuOS4jeWwgeWPt3zml6DpnIDku7vkvZXlh63or4EiLCAi6LWE6LSo57G75oiW57ud5a+55YyW"
    "55So6K+tIl0sIFsiMTAwXFxzKiUiLCAi57ud5a+55YyW55So6K+tIl0sIFsi5pyA5L2O5Lu3fOac"
    "gOS+v+WunHzlhajnvZHmnIB85YWo572R56ys5LiAIiwgIuavlOS7t+exu+e7neWvueWMlueUqOiv"
    "rSJdLCBbIue/u+WimXzmoq/lrZB85YWN57+7fOWbveWGheebtOi/nnznu5Xov4d8XFxidnBuXFxi"
    "IiwgIuacrOS7k+W6k+S4jeaPkOS+m+S7u+S9leinhOmBv+WcsOWMuumZkOWItueahOaWueazlSJd"
    "LCBbIui0puWPt+i0reS5sCIsICLkuI3mtonlj4rotKblj7fkubDljZbvvIzlhpnjgIzmiJDlk4Hl"
    "j7fjgI3lubbor7TmmI7po47pmakiXSwgWyLkurLmtYt85a6e5rWLfOmZkOaXtuS8mOaDoHzlvq7k"
    "v6HmlK/ku5h8XFxidXNkdFxcYiIsICLmlofmoYjljIXnpoHnlKjooajov7AiXSwgWyJwcm9cXHMq"
    "MjB8MjBcXHMq5YCNfFxcYjIwXFxzKlt4w5ddIiwgIuS4jeeCueWQjeOAgeS4jeaOqOiNkOW3suaa"
    "guWBnOaWsOiuoumYheeahOaho+S9jSJdLCBbIlxcYm9mZmljaWFsXFxifFxcYmF1dGhvcmlbc3pd"
    "ZWRcXGJ8XFxiZ3VhcmFudGVlIiwgIuiLseaWh+WQjOagt+S4jeWGmSJdXSwgImNyb3NzX3NpdGUi"
    "OiBbWyJncHR6enoiLCAi5Lik5Liq56uZ54K55LqS5LiN5o+Q5Y+KIl0sIFsiKD88IWdpdGh1Ylxc"
    "LmNvbS8pa2FpXFxzKmdwdCg/IVxcLig/OmFpfHBybylcXGIpIiwgIuWTgeeJjOWPquWGmeOAjEtB"
    "SSDCtyDlvIBncHRBSeOAjeaIluOAjEtBSe+8iGthaWdwdC5hae+8ieOAjSJdXX0="
)
TERMS = json.loads(base64.b64decode(_TERMS_B64).decode("utf-8"))
RULES = [(re.compile(p, re.I), why) for p, why in TERMS["banned"] + TERMS["cross_site"]]

SELF_LINK = re.compile(r"https?://(?:www\.)?kaigpt\.(?:ai|pro)\b[^\s)\"'<>\]]*")
SELF_LINK_BUDGET = {"README.md": 2, "docs/order-status-glossary.md": 1}
SESSION_SAFETY = ("不要通过私聊、邮件或工单", "包括客服")
PLACEHOLDER = "{{" + "OWNER" + "}}"
DATE_RE = re.compile(r"最后核实：\**\s*(\d{4}-\d{2}-\d{2})")
MD_LINK = re.compile(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def text_files():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        if path.suffix in TEXT_SUFFIXES or path.name in {"LICENSE", "llms.txt"}:
            yield path


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def slug(heading: str) -> str:
    """GitHub-style anchor for a Markdown heading."""
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    heading = heading.replace("`", "").strip().lower()
    out = []
    for ch in heading:
        cat = unicodedata.category(ch)
        if ch == " ":
            out.append("-")
        elif ch in "-_" or cat[0] in "LN" or cat == "Mn":
            out.append(ch)
    return "".join(out)


def anchors(path: Path) -> set:
    found, seen, in_code = set(), {}, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        m = None if in_code else re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            s = slug(m.group(2))
            n = seen.get(s, 0)
            seen[s] = n + 1
            found.add(s if n == 0 else f"{s}-{n}")
    return found


class Report:
    def __init__(self) -> None:
        self.errors: list = []
        self.notes: list = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def note(self, msg: str) -> None:
        self.notes.append(msg)


LEGAL_TEXT = {"LICENSE-CC-BY-4.0.txt"}  # verbatim licence text is not ours to reword


def check_wording(rep: Report) -> None:
    for path in text_files():
        if path == SELF or path.name in LEGAL_TEXT:
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for rx, why in RULES:
                m = rx.search(line)
                if m:
                    rep.error(f"{rel(path)}:{n}: banned wording {m.group(0)!r} ({why})")


def check_self_links(rep: Report) -> None:
    """Count clickable kaigpt links (Markdown link targets); plain-text domains are fine."""
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        clickable = [u for u in MD_LINK.findall(path.read_text(encoding="utf-8")) if SELF_LINK.match(u)]
        budget = SELF_LINK_BUDGET.get(rel(path), 0)
        if len(clickable) != budget:
            rep.error(f"{rel(path)}: {len(clickable)} link(s) to kaigpt.ai, expected {budget}")
        for u in clickable:
            if "utm_source=github" not in u:
                rep.error(f"{rel(path)}: kaigpt link without utm_source=github: {u}")
            if "kaigpt.pro" in u:
                rep.error(f"{rel(path)}: kaigpt.pro is written as plain text, never linked")


def check_session_rule(rep: Report) -> None:
    for path in text_files():
        if path == SELF:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "kaigpt.pro" in text and not all(s in text for s in SESSION_SAFETY):
            rep.error(f"{rel(path)}: mentions kaigpt.pro without the warning "
                      f"「不要通过私聊、邮件或工单……发给任何人（包括客服）」")


def check_links(rep: Report) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        in_code = False
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for target in MD_LINK.findall(line):
                if re.match(r"^(https?:|mailto:)", target):
                    continue
                file_part, _, frag = target.partition("#")
                dest = (path.parent / file_part).resolve() if file_part else path
                if file_part and not dest.exists():
                    rep.error(f"{rel(path)}:{n}: broken link {target}")
                    continue
                if frag and dest.suffix == ".md" and frag not in anchors(dest):
                    rep.error(f"{rel(path)}:{n}: missing anchor #{frag} in {rel(dest)}")


def check_checklist(rep: Report) -> None:
    data = json.loads((ROOT / "checklist.json").read_text(encoding="utf-8"))
    checks, signals = data.get("checks", []), data.get("scam_signals", [])
    if len(checks) != 7:
        rep.error(f"checklist.json: expected 7 checks, found {len(checks)}")
    if len(signals) != 9:
        rep.error(f"checklist.json: expected 9 scam signals, found {len(signals)}")
    ids = [item["id"] for item in checks + signals]
    if len(ids) != len(set(ids)):
        rep.error("checklist.json: duplicate id")
    for group in (checks, signals):
        if [item["order"] for item in group] != list(range(1, len(group) + 1)):
            rep.error("checklist.json: order must be 1..n without gaps")
    for item in checks + signals:
        file_part, _, frag = item["doc"].partition("#")
        dest = ROOT / file_part
        if not dest.exists():
            rep.error(f"checklist.json: {item['id']}: {file_part} does not exist")
        elif frag not in anchors(dest):
            rep.error(f"checklist.json: {item['id']}: anchor #{frag} not found in {file_part}")


def check_dates(rep: Report, max_age: int | None) -> None:
    today = dt.date.today()
    pages = [ROOT / "README.md"] + sorted((ROOT / "docs").glob("*.md"))
    for path in pages:
        m = DATE_RE.search(path.read_text(encoding="utf-8"))
        if not m:
            rep.error(f"{rel(path)}: missing 「最后核实：YYYY-MM-DD」")
            continue
        try:
            day = dt.date.fromisoformat(m.group(1))
        except ValueError:
            rep.error(f"{rel(path)}: invalid date {m.group(1)}")
            continue
        if day > today:
            rep.error(f"{rel(path)}: last-verified date {day} is in the future")
        if max_age is not None and (today - day).days > max_age:
            rep.error(f"{rel(path)}: last verified {day}, more than {max_age} days ago; re-check the sources")


def check_placeholders(rep: Report, strict: bool) -> None:
    for path in text_files():
        if path == SELF:
            continue
        if PLACEHOLDER in path.read_text(encoding="utf-8", errors="ignore"):
            msg = f"{rel(path)}: replace {PLACEHOLDER} with the GitHub account name before publishing"
            (rep.error if strict else rep.note)(msg)


def check_online(rep: Report) -> None:
    urls = set()
    for path in ROOT.rglob("*.md"):
        urls.update(u for u in MD_LINK.findall(path.read_text(encoding="utf-8")) if u.startswith("http"))
    for url in sorted(urls):
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Mozilla/5.0 link-check"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                status = resp.status
        except urllib.error.HTTPError as e:
            status = e.code
        except Exception as e:  # noqa: BLE001
            rep.error(f"{url}: {type(e).__name__}")
            continue
        if status == 403 and ("openai.com" in url):
            rep.note(f"{url}: 403 to scripts (open it in a browser)")
        elif status >= 400:
            rep.error(f"{url}: HTTP {status}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true", help="fail on publish placeholders")
    ap.add_argument("--max-age-days", type=int, help="fail when a page was last verified longer ago")
    ap.add_argument("--online", action="store_true", help="also request every external link")
    args = ap.parse_args(argv)

    rep = Report()
    check_wording(rep)
    check_self_links(rep)
    check_session_rule(rep)
    check_links(rep)
    check_checklist(rep)
    check_dates(rep, args.max_age_days)
    check_placeholders(rep, args.strict)
    if args.online:
        check_online(rep)

    for msg in rep.notes:
        print(f"note   {msg}")
    for msg in rep.errors:
        print(f"error  {msg}")
    print(f"{'FAILED' if rep.errors else 'OK'}: {len(rep.errors)} error(s), {len(rep.notes)} note(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
