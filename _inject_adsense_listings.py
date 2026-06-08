#!/usr/bin/env python3
"""
Inject a single responsive AdSense banner into trail listing pages
(state, difficulty, type, and category pages under /trilhas/).

Placement rule:
- One ad between the editorial section (</section>) and the trails section
- Uses "auto" responsive format
- Idempotent: skips pages that already have adsbygoogle
"""
import os, re

BASE      = os.path.dirname(os.path.abspath(__file__))
LIST_DIR  = os.path.join(BASE, "trilhas")

PUB_ID    = "ca-pub-2482023752745520"
# Reuse TRAIL_MID slot for listing pages.
# Create a dedicated "Listing Banner" unit in AdSense for better attribution.
SLOT_LIST = "3721854690"   # TRAIL_MID (replace with dedicated LISTING slot ID)

ADSENSE_SCRIPT = (
    f'<script async src="https://pagead2.googlesyndication.com/pagead/js/'
    f'adsbygoogle.js?client={PUB_ID}" crossorigin="anonymous"></script>'
)

AD_CSS = (
    ".listing-ad{max-width:1200px;margin:0 auto 2rem;padding:0 1rem;"
    "text-align:center;overflow:hidden}\n"
    ".listing-ad ins{display:block!important;max-width:100%}"
)

AD_HTML = (
    '\n<div class="listing-ad" aria-label="Publicidade">\n'
    f'  <ins class="adsbygoogle"\n'
    f'       style="display:block"\n'
    f'       data-ad-client="{PUB_ID}"\n'
    f'       data-ad-slot="{SLOT_LIST}"\n'
    f'       data-ad-format="auto"\n'
    f'       data-full-width-responsive="true"></ins>\n'
    f'  <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>\n'
    '</div>\n'
)


def add_adsense_to_head(content):
    if PUB_ID in content:
        return content, False
    idx = content.find('</head>')
    if idx == -1:
        return content, False
    return content[:idx] + ADSENSE_SCRIPT + '\n' + content[idx:], True


def add_ad_css(content):
    if 'listing-ad' in content:
        return content
    idx = content.rfind('</style>')
    if idx == -1:
        return content
    return content[:idx] + AD_CSS + '\n' + content[idx:]


def inject_listing_ad(content):
    """
    Insert one ad block between the editorial section and the trails section.
    Falls back to inserting before the trails section if no editorial found.
    Returns (new_content, inserted_bool).
    """
    # Primary: after the editorial </section> that precedes the #trilhas section
    trilhas_section = content.find('id="trilhas"')
    if trilhas_section == -1:
        # Try generic trail list markers
        trilhas_section = content.find('class="trail-list"')
        if trilhas_section == -1:
            trilhas_section = content.find('class="trails-grid"')
    if trilhas_section == -1:
        return content, False

    # Walk backwards from #trilhas to find the preceding </section>
    preceding_close = content.rfind('</section>', 0, trilhas_section)
    if preceding_close == -1:
        return content, False

    insert_at = preceding_close + len('</section>')
    content = content[:insert_at] + AD_HTML + content[insert_at:]
    return content, True


def process_file(html_path):
    with open(html_path, encoding='utf-8') as f:
        content = f.read()

    if 'adsbygoogle' in content:
        return 'SKIP', 'already has AdSense'

    content, _ = add_adsense_to_head(content)
    content     = add_ad_css(content)
    content, ok = inject_listing_ad(content)

    if not ok:
        return 'WARN', 'could not locate insertion point (#trilhas / trail-list)'

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return 'OK', 'listing ad injected'


if __name__ == '__main__':
    ok = skip = warn = 0
    for name in sorted(os.listdir(LIST_DIR)):
        if name == 'data':
            continue
        html_path = os.path.join(LIST_DIR, name, 'index.html')
        if not os.path.exists(html_path):
            continue
        status, msg = process_file(html_path)
        icon = '✓' if status == 'OK' else ('⚠' if status == 'WARN' else '–')
        print(f'  {icon} {name}: {msg}')
        if status == 'OK':     ok   += 1
        elif status == 'WARN': warn += 1
        else:                  skip += 1

    print(f'\nDone: {ok} processed, {skip} skipped, {warn} with warnings')
