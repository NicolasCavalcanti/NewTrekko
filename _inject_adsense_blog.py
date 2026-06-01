#!/usr/bin/env python3
"""
Inject AdSense ad blocks into blog post HTML files.

Placement rules (non-negotiable):
- No ads on pages with fewer than 400 editorial words
- Max 3 ad blocks per page
- No ads before the first paragraph
- Positions: after 2nd paragraph, between H2 sections (middle), end of article
- Content/ad ratio must remain > 3:1
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE, "blog")

PUB_ID   = "ca-pub-2482023752745520"
SLOT_MID = "8145037926"   # BLOG_MID_ARTICLE
SLOT_END = "2907631548"   # BLOG_END_ARTICLE

MIN_WORDS = 400
MAX_ADS   = 3

ADSENSE_SCRIPT = (
    f'<script async src="https://pagead2.googlesyndication.com/pagead/js/'
    f'adsbygoogle.js?client={PUB_ID}" crossorigin="anonymous"></script>'
)

AD_CSS = (
    ".ad-block{margin:2rem 0;text-align:center;clear:both;min-height:90px}\n"
    ".ad-block--labeled::before{content:'Publicidade';display:block;"
    "font-size:.7rem;color:#94a3b8;text-transform:uppercase;"
    "letter-spacing:.05em;margin-bottom:.35rem}"
)


def make_ad(slot):
    return (
        f'  <div class="ad-block ad-block--labeled" aria-label="Publicidade">\n'
        f'    <ins class="adsbygoogle"\n'
        f'         style="display:block"\n'
        f'         data-ad-client="{PUB_ID}"\n'
        f'         data-ad-slot="{slot}"\n'
        f'         data-ad-format="auto"\n'
        f'         data-full-width-responsive="true"></ins>\n'
        f'    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>\n'
        f'  </div>'
    )


def count_words(html_fragment):
    """Count plain-text words in an HTML fragment."""
    text = re.sub(r'<[^>]+>', ' ', html_fragment)
    return len(text.split())


def extract_article_inner(content):
    """Return (art_start, art_end, inner_html) or (None, None, None)."""
    OPEN  = '<article class="post-body">'
    CLOSE = '</article>'
    s = content.find(OPEN)
    if s == -1:
        return None, None, None
    e = content.find(CLOSE, s)
    if e == -1:
        return None, None, None
    inner = content[s + len(OPEN):e]
    return s, e, inner


def inject_ads(content):
    """
    Inject up to 3 ad blocks into the article body.
    Returns (new_content, n_ads_added).
    """
    art_start, art_end, inner = extract_article_inner(content)
    if inner is None:
        return content, 0

    # --- Position 1: after 2nd </p> ---
    p_ends = [m.end() for m in re.finditer(r'</p>', inner)]
    if len(p_ends) < 2:
        return content, 0
    pos1 = p_ends[1]  # character offset inside `inner`

    # --- Position 2: just before a middle H2 (between sections) ---
    h2_starts = [m.start() for m in re.finditer(r'<h2>', inner)]
    pos2 = None
    if len(h2_starts) >= 2:
        mid = len(h2_starts) // 2
        candidate = h2_starts[mid]
        # Must be meaningfully after position 1 (at least 300 chars of content)
        if candidate > pos1 + 300:
            pos2 = candidate

    # Build insertion list (descending order to preserve offsets)
    insertions = []
    if pos2 is not None:
        insertions.append((pos2, '\n' + make_ad(SLOT_MID) + '\n'))
    insertions.append((pos1, '\n' + make_ad(SLOT_MID) + '\n'))

    for pos, ad_html in sorted(insertions, key=lambda x: x[0], reverse=True):
        inner = inner[:pos] + ad_html + inner[pos:]

    # --- Position 3: just before </article> ---
    inner += '\n' + make_ad(SLOT_END) + '\n'

    n_ads = len(insertions) + 1  # capped at MAX_ADS by construction (max 3)

    OPEN  = '<article class="post-body">'
    CLOSE = '</article>'
    new_article = OPEN + inner + CLOSE
    new_content = content[:art_start] + new_article + content[art_end + len(CLOSE):]
    return new_content, n_ads


def add_adsense_to_head(content):
    """Add AdSense <script> before </head>; return (new_content, added_bool)."""
    if PUB_ID in content:
        return content, False
    idx = content.find('</head>')
    if idx == -1:
        return content, False
    return content[:idx] + ADSENSE_SCRIPT + '\n' + content[idx:], True


def add_ad_css(content):
    """Append ad CSS to the last </style> in <head>."""
    if 'ad-block' in content:
        return content
    idx = content.rfind('</style>')
    if idx == -1:
        return content
    return content[:idx] + AD_CSS + '\n' + content[idx:]


def process_file(html_path):
    with open(html_path, encoding='utf-8') as f:
        content = f.read()

    # Already processed?
    if 'adsbygoogle' in content:
        return 'SKIP', 'already has AdSense'

    # Word count check
    _, _, inner = extract_article_inner(content)
    if inner is None:
        return 'WARN', 'no <article class="post-body"> found'

    words = count_words(inner)
    if words < MIN_WORDS:
        return 'SKIP', f'only {words} words (min {MIN_WORDS})'

    content, _ = add_adsense_to_head(content)
    content     = add_ad_css(content)
    content, n  = inject_ads(content)

    if n == 0:
        return 'WARN', 'could not find injection points'

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return 'OK', f'{words} words, {n} ads injected'


if __name__ == '__main__':
    ok = skip = warn = 0
    for slug in sorted(os.listdir(BLOG_DIR)):
        html_path = os.path.join(BLOG_DIR, slug, 'index.html')
        if not os.path.exists(html_path):
            continue
        status, msg = process_file(html_path)
        icon = '✓' if status == 'OK' else ('⚠' if status == 'WARN' else '–')
        print(f'  {icon} {slug}: {msg}')
        if status == 'OK':    ok   += 1
        elif status == 'WARN': warn += 1
        else:                  skip += 1

    print(f'\nDone: {ok} processed, {skip} skipped, {warn} with warnings')
