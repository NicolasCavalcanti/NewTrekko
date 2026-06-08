#!/usr/bin/env python3
"""
Inject AdSense ad blocks into trail detail HTML pages.

Template: static slug-based pages with #trekko-editorial section.
Placement rules:
- Max 2 ad blocks per page (editorial section is shorter than blog posts)
- Position 1: after the 3rd paragraph inside #trekko-editorial (.ei div)
- Position 2: before the .ef (editorial footer) element
- Skips pages with fewer than 200 words in the editorial body
- Never inserts twice (idempotent)
"""
import os, re

BASE      = os.path.dirname(os.path.abspath(__file__))
TRAIL_DIR = os.path.join(BASE, "trilha")

PUB_ID    = "ca-pub-2482023752745520"
SLOT_MID  = "3721854690"   # TRAIL_MID_EDITORIAL
SLOT_END  = "5038274619"   # TRAIL_END_EDITORIAL

MIN_WORDS = 200
MAX_ADS   = 2

ADSENSE_SCRIPT = (
    f'<script async src="https://pagead2.googlesyndication.com/pagead/js/'
    f'adsbygoogle.js?client={PUB_ID}" crossorigin="anonymous"></script>'
)

AD_CSS = (
    ".trekko-ad{max-width:800px;margin:1.75rem auto;overflow:hidden;text-align:center}\n"
    ".trekko-ad ins{display:block!important;max-width:100%}\n"
    "@media(max-width:640px){.trekko-ad{margin:1.25rem auto}}"
)

LAZY_INIT_JS = """\
<script>
(function(){
  if(!("IntersectionObserver"in window))return;
  var els=document.querySelectorAll("#trekko-editorial .trekko-ad ins.adsbygoogle");
  if(!els.length)return;
  var obs=new IntersectionObserver(function(entries,o){
    entries.forEach(function(e){
      if(!e.isIntersecting)return;
      (adsbygoogle=window.adsbygoogle||[]).push({});
      o.unobserve(e.target);
    });
  },{rootMargin:"200px"});
  els.forEach(function(el){obs.observe(el);});
})();
</script>"""


def make_ad(slot):
    return (
        f'<div class="trekko-ad" aria-label="Anúncio">'
        f'<ins class="adsbygoogle" style="display:block" '
        f'data-ad-client="{PUB_ID}" '
        f'data-ad-slot="{slot}" '
        f'data-ad-format="auto" '
        f'data-full-width-responsive="true"></ins>'
        f'</div>'
    )


def count_words(html_fragment):
    text = re.sub(r'<[^>]+>', ' ', html_fragment)
    return len(text.split())


def extract_editorial_inner(content):
    """Return (sec_start, sec_end, ei_inner, ei_inner_start) or Nones."""
    OPEN  = 'id="trekko-editorial"'
    CLOSE = '</section>'
    s = content.find(OPEN)
    if s == -1:
        return None, None, None, None
    # Find the enclosing section tag start
    tag_start = content.rfind('<section', 0, s)
    if tag_start == -1:
        return None, None, None, None
    e = content.find(CLOSE, s)
    if e == -1:
        return None, None, None, None
    section_inner = content[tag_start:e + len(CLOSE)]
    # Try to narrow to .ei inner div for word count and insertion
    ei_m = re.search(r'<div class="ei">(.*?)</div>', section_inner, re.DOTALL)
    if ei_m:
        ei_inner      = ei_m.group(1)
        ei_inner_start = tag_start + ei_m.start(1)
    else:
        ei_inner      = section_inner
        ei_inner_start = tag_start
    return tag_start, e + len(CLOSE), ei_inner, ei_inner_start


def inject_ads(content):
    """Inject up to 2 ad blocks. Returns (new_content, n_added)."""
    tag_start, sec_end, ei_inner, ei_inner_start = extract_editorial_inner(content)
    if ei_inner is None:
        return content, 0

    # Position 1: after 3rd </p>
    p_ends = [m.end() for m in re.finditer(r'</p>', ei_inner)]
    if len(p_ends) < 3:
        # Fall back to after 2nd paragraph
        if len(p_ends) < 2:
            return content, 0
        pos1 = p_ends[1]
    else:
        pos1 = p_ends[2]

    # Position 2: just before .ef footer (or before </div> closing .ei)
    ef_m = re.search(r'<div class="ef">', ei_inner)
    pos2 = ef_m.start() if ef_m else None

    # Build insertions (descending to preserve offsets)
    insertions = []
    if pos2 is not None and pos2 > pos1 + 200:
        insertions.append((ei_inner_start + pos2, '\n' + make_ad(SLOT_END) + '\n'))
    insertions.append((ei_inner_start + pos1, '\n' + make_ad(SLOT_MID) + '\n'))

    for abs_pos, ad_html in sorted(insertions, reverse=True):
        content = content[:abs_pos] + ad_html + content[abs_pos:]

    n_ads = len(insertions)

    # Append lazy-init script before </body> if not present
    if 'IntersectionObserver' not in content:
        body_end = content.rfind('</body>')
        if body_end != -1:
            content = content[:body_end] + LAZY_INIT_JS + '\n' + content[body_end:]

    return content, n_ads


def add_adsense_to_head(content):
    if PUB_ID in content:
        return content, False
    idx = content.find('</head>')
    if idx == -1:
        return content, False
    return content[:idx] + ADSENSE_SCRIPT + '\n' + content[idx:], True


def add_ad_css(content):
    if 'trekko-ad' in content:
        return content
    idx = content.rfind('</style>')
    if idx == -1:
        return content
    return content[:idx] + AD_CSS + '\n' + content[idx:]


def process_file(html_path):
    with open(html_path, encoding='utf-8') as f:
        content = f.read()

    if 'adsbygoogle' in content and 'trekko-ad' in content:
        return 'SKIP', 'already has AdSense'

    _, _, ei_inner, _ = extract_editorial_inner(content)
    if ei_inner is None:
        return 'WARN', 'no #trekko-editorial section found'

    words = count_words(ei_inner)
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
    for slug in sorted(os.listdir(TRAIL_DIR)):
        # Skip legacy numeric-ID pages (React SPA shells, redirect to slugs)
        if slug.isdigit():
            continue
        html_path = os.path.join(TRAIL_DIR, slug, 'index.html')
        if not os.path.exists(html_path):
            continue
        status, msg = process_file(html_path)
        icon = '✓' if status == 'OK' else ('⚠' if status == 'WARN' else '–')
        print(f'  {icon} {slug}: {msg}')
        if status == 'OK':     ok   += 1
        elif status == 'WARN': warn += 1
        else:                  skip += 1

    print(f'\nDone: {ok} processed, {skip} skipped, {warn} with warnings')
