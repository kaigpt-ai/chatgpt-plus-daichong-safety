"""Tests for scripts/check.py: the real repository passes, and each rule catches a
deliberately broken copy. Offline; standard library only.

Banned words are taken from the script's own encoded list, so this file does not
spell them out either.
"""

from __future__ import annotations

import importlib.util
import io
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check.py"


def load_check(root: Path):
    """Import scripts/check.py so that ROOT points at `root`."""
    spec = importlib.util.spec_from_file_location(f"check_{id(root)}", root / "scripts" / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(root: Path, *args: str):
    mod = load_check(root)
    out = io.StringIO()
    with redirect_stdout(out):
        code = mod.main(list(args))
    return code, out.getvalue()


class RealRepository(unittest.TestCase):
    def test_passes(self):
        code, out = run(ROOT)
        self.assertEqual(code, 0, out)

    def test_strict_only_flags_the_owner_placeholder(self):
        code, out = run(ROOT, "--strict")
        errors = [line for line in out.splitlines() if line.startswith("error")]
        self.assertTrue(all("OWNER" in line for line in errors), out)


class BrokenCopies(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        self.terms = load_check(self.root).TERMS

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def append(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.write_text(path.read_text(encoding="utf-8") + "\n" + text + "\n", encoding="utf-8")

    def assertCaught(self, needle: str):
        code, out = run(self.root)
        self.assertEqual(code, 1, out)
        self.assertIn(needle, out)

    def test_banned_word(self):
        word = self.terms["banned"][0][0].split("|")[0]
        self.append("docs/scam-patterns.md", f"这是{word}说明。")
        self.assertCaught("banned wording")

    def test_other_site_name(self):
        self.append("docs/scam-patterns.md", "see " + self.terms["cross_site"][0][0])
        self.assertCaught("banned wording")

    def test_extra_self_link(self):
        self.append("docs/scam-patterns.md", "[KAI](https://kaigpt.ai/?utm_source=github)")
        self.assertCaught("link(s) to kaigpt.ai, expected 0")

    def test_self_link_without_utm(self):
        path = self.root / "docs" / "order-status-glossary.md"
        text = path.read_text(encoding="utf-8")
        start = text.index("https://kaigpt.ai/blog/understand-order-status")
        end = text.index(")", start)
        path.write_text(text[:start] + "https://kaigpt.ai/blog/understand-order-status" + text[end:], encoding="utf-8")
        self.assertCaught("without utm_source=github")

    def test_redemption_domain_without_warning(self):
        domain = ".".join(["kai" + "gpt", "pro"])  # built at run time so this file does not trip the rules itself
        (self.root / "docs" / "extra.md").write_text(f"最后核实：2026-09-29\n\n在 {domain} 提交。\n", encoding="utf-8")
        self.assertCaught("without the warning")

    def test_broken_anchor(self):
        self.append("README.md", "[x](docs/what-is-session.md#no-such-heading)")
        self.assertCaught("missing anchor #no-such-heading")

    def test_checklist_anchor_must_exist(self):
        path = self.root / "docs" / "pre-purchase-checklist.md"
        text = path.read_text(encoding="utf-8").replace("## 4. 订单记录：有订单号和状态时间线", "## 4. 订单")
        path.write_text(text, encoding="utf-8")
        self.assertCaught("checklist.json: order-record")

    def test_missing_last_verified(self):
        path = self.root / "docs" / "scam-patterns.md"
        path.write_text(path.read_text(encoding="utf-8").replace("最后核实", "更新"), encoding="utf-8")
        self.assertCaught("missing 「最后核实")

    def test_max_age(self):
        code, out = run(self.root, "--max-age-days", "-1")
        self.assertEqual(code, 1)
        self.assertIn("re-check the sources", out)


if __name__ == "__main__":
    unittest.main()
