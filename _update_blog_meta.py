#!/usr/bin/env python3
"""Patches <title>, meta description, and og:title/og:description in static blog pages
by reading ground-truth values from data/blog.json."""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "data", "blog.json")) as f:
    articles = json.load(f)

by_slug = {a["slug"]: a for a in articles}


def patch_file(html_path: str, article: dict) -> bool:
    with open(html_path, encoding="utf-8") as f:
        content = f.read()

    meta_title = article.get("metaTitle", "")
    meta_desc = article.get("metaDescription", "")
    if not meta_title or not meta_desc:
        print(f"  SKIP {html_path}: missing metaTitle or metaDescription in JSON")
        return False

    original = content

    # <title>…</title>
    content = re.sub(r"<title>[^<]*</title>", f"<title>{meta_title}</title>", content, count=1)

    # <meta name="description" content="…">
    content = re.sub(
        r'(<meta\s+name=["\']description["\']\s+content=["\'])[^"\']*(["\'])',
        lambda m: m.group(1) + meta_desc + m.group(2),
        content,
        count=1,
    )

    # <meta property="og:title" content="…">
    content = re.sub(
        r'(<meta\s+property=["\']og:title["\']\s+content=["\'])[^"\']*(["\'])',
        lambda m: m.group(1) + meta_title + m.group(2),
        content,
        count=1,
    )

    # <meta property="og:description" content="…">
    content = re.sub(
        r'(<meta\s+property=["\']og:description["\']\s+content=["\'])[^"\']*(["\'])',
        lambda m: m.group(1) + meta_desc + m.group(2),
        content,
        count=1,
    )

    if content == original:
        return False

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


updated = 0
for slug, article in by_slug.items():
    html_path = os.path.join(BASE, "blog", slug, "index.html")
    if not os.path.exists(html_path):
        print(f"  NOT FOUND: blog/{slug}/index.html")
        continue
    if patch_file(html_path, article):
        print(f"  updated: blog/{slug}/index.html")
        updated += 1

print(f"\nDone — {updated} blog pages updated.")
