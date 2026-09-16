#!/usr/bin/env python3
"""站点自检：结构、内链、SEO 元素、外链 rel 属性。

用法：python3 scripts/check.py
不访问网络，只检查仓库内的文件。失败时退出码非零。
"""
import glob
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
OWN_SITES = ("kaigpt.ai", "gptzzz.ai")
VOID = {"meta", "link", "br", "img", "hr", "input", "source", "area", "col", "embed", "param", "track", "wbr"}


class Nesting(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            self.errors.append(f"标签错位 </{tag}>，当前栈顶是 <{self.stack[-1]}>")


def check(path: pathlib.Path) -> list[str]:
    s = path.read_text(encoding="utf-8")
    problems = []

    if not re.search(r"<title>.+?</title>", s, re.S):
        problems.append("缺少 <title>")
    if not re.search(r'name="description"\s+content=".+?"', s):
        problems.append("缺少 meta description")
    if not re.search(r'rel="canonical"', s):
        problems.append("缺少 canonical")
    if 'lang="zh-CN"' not in s:
        problems.append("缺少 lang=zh-CN")

    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    if len(h1) != 1:
        problems.append(f"H1 数量应为 1，实际 {len(h1)}")

    nest = Nesting()
    nest.feed(s)
    problems += nest.errors
    if nest.stack:
        problems.append(f"标签未闭合：{nest.stack}")

    # 内链
    for href in re.findall(r'href="([^"#:]+\.(?:html|md|css|png|svg|xml|txt))"', s):
        if not (ROOT / href).exists():
            problems.append(f"死链：{href}")

    # 自家站的外链必须是 dofollow
    for tag in re.findall(r"<a\s[^>]*>", s):
        m = re.search(r'href="(https?://[^"]+)"', tag)
        if not m or not any(d in m.group(1) for d in OWN_SITES):
            continue
        rel = re.search(r'rel="([^"]*)"', tag)
        if rel and "nofollow" in rel.group(1):
            problems.append(f"自家链接被标成 nofollow：{m.group(1)}")

    return problems


def main() -> int:
    pages = sorted(ROOT.glob("*.html"))
    if not pages:
        print("没有找到任何 HTML 页面")
        return 1

    failed = 0
    for page in pages:
        problems = check(page)
        print(f"{'OK  ' if not problems else 'FAIL'}  {page.name}")
        for p in problems:
            print(f"        ! {p}")
        failed += bool(problems)

    # sitemap 与实际页面是否一致
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    listed = {u.rsplit("/", 1)[-1] or "index.html" for u in re.findall(r"<loc>(.*?)</loc>", sitemap)}
    actual = {p.name for p in pages}
    missing = actual - listed
    stale = listed - actual
    if missing or stale:
        failed += 1
        print("FAIL  sitemap.xml")
        for m in sorted(missing):
            print(f"        ! 页面存在但未列入 sitemap：{m}")
        for m in sorted(stale):
            print(f"        ! sitemap 里有但文件不存在：{m}")
    else:
        print(f"OK    sitemap.xml（{len(listed)} 个 URL）")

    # IndexNow 密钥文件
    keys = list(ROOT.glob("????????????????????????????????.txt"))
    if not keys:
        failed += 1
        print("FAIL  缺少 IndexNow 密钥文件")
    else:
        key = keys[0]
        if key.read_text().strip() != key.stem:
            failed += 1
            print(f"FAIL  IndexNow 密钥内容与文件名不一致：{key.name}")
        else:
            print(f"OK    IndexNow 密钥（{key.name}）")

    print()
    print("全部通过" if not failed else f"{failed} 项未通过")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
