#!/usr/bin/env python3
"""
Fix trailing slashes across all HTML files and sitemap.xml.

Rules:
- Remove trailing slashes from all trekko.com.br URLs in HTML (canonical,
  og:url, hreflang, schema.org JSON-LD, internal links).
- Preserve the root URL https://trekko.com.br/ unchanged.
- Preserve href="/" unchanged.
- Fix sitemap.xml: remove trailing slashes from all <loc> except homepage.
"""

import os
import re
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Regex helpers
# ---------------------------------------------------------------------------

# Absolute trekko.com.br URL with a trailing slash, followed by a quote or
# angle bracket (e.g. in HTML attributes and JSON-LD strings).
# Matches: https://trekko.com.br/some/path/
# Does NOT match: https://trekko.com.br/  (root — must have a path segment)
_ABS_URL_RE = re.compile(
    r'(https://trekko\.com\.br)'
    r'(/[^/\s"\'<>]+(?:/[^/\s"\'<>]+)*)/'
    r'(?=["\'<>\s])'
)

# Internal href/src with trailing slash: href="/some/path/"
# Matches: href="/blog/post/" → href="/blog/post"
# Does NOT match: href="/"
_INTERNAL_HREF_RE = re.compile(
    r'((?:href|src)=")'
    r'(/[^/\s"]+(?:/[^/\s"]+)*)/'
    r'(")'
)


def fix_absolute_urls(text: str) -> str:
    """Remove trailing slash from absolute trekko.com.br URLs."""
    return _ABS_URL_RE.sub(r'\1\2', text)


def fix_internal_hrefs(text: str) -> str:
    """Remove trailing slash from internal href/src links."""
    return _INTERNAL_HREF_RE.sub(r'\1\2\3', text)


def fix_html_file(path: str) -> tuple[bool, int]:
    """
    Fix a single HTML file. Returns (changed: bool, fixes_count: int).
    """
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    result = fix_absolute_urls(original)
    result = fix_internal_hrefs(result)

    if result == original:
        return False, 0

    # Count approximate number of fixes
    fixes = sum(
        1 for a, b in zip(original.split('\n'), result.split('\n')) if a != b
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(result)

    return True, fixes


def fix_sitemap(path: str) -> bool:
    """
    Fix sitemap.xml: remove trailing slashes from all <loc> tags
    except the homepage (https://trekko.com.br/).
    """
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    # Match <loc>https://trekko.com.br/path/</loc>
    # Do NOT match <loc>https://trekko.com.br/</loc> (homepage)
    result = re.sub(
        r'(<loc>https://trekko\.com\.br)(/[^<]*?)/(</loc>)',
        r'\1\2\3',
        original,
    )

    if result == original:
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(result)

    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    total_files = 0
    changed_files = 0

    # Fix all HTML files
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        # Skip hidden dirs and asset dirs
        dirnames[:] = [
            d for d in dirnames
            if not d.startswith('.')
            and d not in ('assets', 'node_modules', '__pycache__')
        ]
        for fname in filenames:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(dirpath, fname)
            total_files += 1
            changed, fixes = fix_html_file(fpath)
            if changed:
                changed_files += 1
                rel = os.path.relpath(fpath, ROOT_DIR)
                print(f'  [HTML] {rel} ({fixes} line(s) changed)')

    # Fix sitemap
    sitemap_path = os.path.join(ROOT_DIR, 'sitemap.xml')
    if os.path.exists(sitemap_path):
        if fix_sitemap(sitemap_path):
            print('  [XML]  sitemap.xml')

    print(f'\nDone. {changed_files}/{total_files} HTML files updated.')


if __name__ == '__main__':
    main()
