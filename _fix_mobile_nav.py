#!/usr/bin/env python3
"""
UX-01: Inject hamburger menu into all static HTML pages.
Also fixes: touch targets, viewport overflow, mobile form usability.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).parent

# ── Mobile nav CSS to inject (inside existing <style> or appended) ─────────
MOBILE_NAV_CSS = """
/* ── Mobile nav (UX-01) ── */
.nav-toggle{display:none;align-items:center;justify-content:center;width:44px;height:44px;border:none;background:transparent;cursor:pointer;padding:0;color:inherit;flex-shrink:0}
.nav-toggle svg{display:block}
@media(max-width:767px){
  .nav-toggle{display:flex}
  .site-nav{display:none!important;position:fixed;inset:0;top:64px;background:#fff;z-index:200;flex-direction:column!important;align-items:stretch!important;gap:0!important;padding:1rem 0;overflow-y:auto;box-shadow:0 8px 24px rgba(0,0,0,.12)}
  .site-nav.nav-open{display:flex!important}
  .site-nav a{padding:.85rem 1.5rem;font-size:1rem!important;color:var(--text-primary,#1a1a1a)!important;border-bottom:1px solid var(--border,#e5e7eb);display:block;min-height:44px;display:flex;align-items:center}
  .site-nav a:last-child{border-bottom:none}
  .header-cta .btn--outline{display:none}
  .header-cta .btn--primary{min-height:44px;min-width:44px}
  .nav-overlay{display:none;position:fixed;inset:0;top:64px;background:rgba(0,0,0,.35);z-index:190}
  .nav-overlay.nav-open{display:block}
}
"""

# For dark-background headers (trilhas page)
MOBILE_NAV_CSS_DARK = """
/* ── Mobile nav dark header (UX-01) ── */
.nav-toggle{display:none;align-items:center;justify-content:center;width:44px;height:44px;border:none;background:transparent;cursor:pointer;padding:0;color:#fff;flex-shrink:0}
.nav-toggle svg{display:block}
@media(max-width:767px){
  .nav-toggle{display:flex}
  .site-header nav{display:none!important;position:fixed;inset:0;top:60px;background:#fff;z-index:200;flex-direction:column!important;align-items:stretch!important;gap:0!important;padding:1rem 0;overflow-y:auto;box-shadow:0 8px 24px rgba(0,0,0,.12)}
  .site-header nav.nav-open{display:flex!important}
  .site-header nav a{padding:.85rem 1.5rem;font-size:1rem!important;color:#0d542b!important;border-bottom:1px solid #e5e7eb;display:flex;align-items:center;min-height:44px;margin-left:0!important}
  .site-header nav a:last-child{border-bottom:none}
  .nav-overlay{display:none;position:fixed;inset:0;top:60px;background:rgba(0,0,0,.35);z-index:190}
  .nav-overlay.nav-open{display:block}
}
"""

# ── Hamburger button HTML ────────────────────────────────────────────────────
HAMBURGER_BTN = '''<button class="nav-toggle" id="nav-toggle" aria-label="Abrir menu de navegação" aria-expanded="false" aria-controls="main-nav">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
        <line class="bar1" x1="3" y1="6" x2="21" y2="6"/>
        <line class="bar2" x1="3" y1="12" x2="21" y2="12"/>
        <line class="bar3" x1="3" y1="18" x2="21" y2="18"/>
      </svg>
    </button>'''

OVERLAY_HTML = '<div class="nav-overlay" id="nav-overlay" aria-hidden="true"></div>'

# ── Toggle JS ────────────────────────────────────────────────────────────────
TOGGLE_JS = """
(function(){
  var btn=document.getElementById('nav-toggle');
  var nav=document.getElementById('main-nav');
  var overlay=document.getElementById('nav-overlay');
  if(!btn||!nav)return;
  function openMenu(){
    nav.classList.add('nav-open');
    if(overlay)overlay.classList.add('nav-open');
    btn.setAttribute('aria-expanded','true');
    btn.setAttribute('aria-label','Fechar menu de navegação');
    document.body.style.overflow='hidden';
  }
  function closeMenu(){
    nav.classList.remove('nav-open');
    if(overlay)overlay.classList.remove('nav-open');
    btn.setAttribute('aria-expanded','false');
    btn.setAttribute('aria-label','Abrir menu de navegação');
    document.body.style.overflow='';
  }
  btn.addEventListener('click',function(){
    nav.classList.contains('nav-open')?closeMenu():openMenu();
  });
  if(overlay)overlay.addEventListener('click',closeMenu);
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeMenu();});
})();
"""

# For trilhas page (no id="main-nav")
TOGGLE_JS_DARK = """
(function(){
  var btn=document.getElementById('nav-toggle');
  var nav=document.querySelector('.site-header nav');
  var overlay=document.getElementById('nav-overlay');
  if(!btn||!nav)return;
  function openMenu(){
    nav.classList.add('nav-open');
    if(overlay)overlay.classList.add('nav-open');
    btn.setAttribute('aria-expanded','true');
    btn.setAttribute('aria-label','Fechar menu de navegação');
    document.body.style.overflow='hidden';
  }
  function closeMenu(){
    nav.classList.remove('nav-open');
    if(overlay)overlay.classList.remove('nav-open');
    btn.setAttribute('aria-expanded','false');
    btn.setAttribute('aria-label','Abrir menu de navegação');
    document.body.style.overflow='';
  }
  btn.addEventListener('click',function(){
    nav.classList.contains('nav-open')?closeMenu():openMenu();
  });
  if(overlay)overlay.addEventListener('click',closeMenu);
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeMenu();});
})();
"""

# ── Global mobile fixes CSS (overflow, images, touch targets) ───────────────
GLOBAL_MOBILE_FIXES = """
/* ── Global mobile fixes (UX-01) ── */
@media(max-width:767px){
  html,body{max-width:100%;overflow-x:hidden}
  img{max-width:100%;height:auto}
  .btn,.quick-link,button,a[role="button"]{min-height:44px;min-width:44px}
  .form-row{grid-template-columns:1fr!important}
  .contact-layout{grid-template-columns:1fr!important}
  table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
}
"""

def has_hamburger(html: str) -> bool:
    return 'nav-toggle' in html or 'hamburger' in html

def inject_css_before_style_close(html: str, css: str) -> str:
    """Append CSS before the last </style> in <head>."""
    # Find last </style> before </head>
    head_end = html.lower().find('</head>')
    if head_end == -1:
        return html
    segment = html[:head_end]
    last_style_close = segment.rfind('</style>')
    if last_style_close == -1:
        # No style block, inject before </head>
        return html[:head_end] + f'<style>{css}</style>\n' + html[head_end:]
    return html[:last_style_close] + css + html[last_style_close:]

def inject_js_before_body_close(html: str, js: str) -> str:
    body_close = html.rfind('</body>')
    if body_close == -1:
        return html + f'<script>{js}</script>'
    return html[:body_close] + f'<script>{js}</script>\n' + html[body_close:]

def inject_overlay_before_body_close(html: str) -> str:
    body_close = html.rfind('</body>')
    if body_close == -1:
        return html + OVERLAY_HTML
    return html[:body_close] + OVERLAY_HTML + '\n' + html[body_close:]

def process_standard_header(html: str) -> str:
    """
    For pages using .site-nav + .header-inner pattern.
    Adds id="main-nav" to site-nav, injects hamburger button into header-inner.
    """
    # Add id to site-nav if not present
    html = re.sub(
        r'(<nav\b[^>]*class="[^"]*site-nav[^"]*"[^>]*)(?!.*id=)',
        lambda m: m.group(0).rstrip('>') + ' id="main-nav">',
        html,
        count=1
    )
    # Also handle site-nav without id="main-nav" already
    if 'id="main-nav"' not in html:
        html = html.replace('class="site-nav"', 'class="site-nav" id="main-nav"', 1)

    # Inject hamburger button before </div> that closes header-inner
    # Find the header-inner div closing tag by inserting before the first nav/header closing sequence
    # Strategy: insert hamburger right before </div> of .header-inner
    # The header-inner contains: logo | site-nav | header-cta
    # We insert hamburger right before the closing </div> of header-inner (before header-cta or after site-nav)

    # Insert hamburger after site-nav closing tag
    html = re.sub(
        r'(</nav>)(\s*\n?\s*<div class="header-cta")',
        r'\1\n    ' + HAMBURGER_BTN + r'\2',
        html,
        count=1
    )
    # If no header-cta, insert before header-inner closing </div>
    if 'nav-toggle' not in html:
        # Find header-inner and insert hamburger before its closing </div>
        # This is tricky without a proper parser; use a simpler heuristic
        html = re.sub(
            r'(<header[^>]*>.*?</nav>)',
            r'\1\n    ' + HAMBURGER_BTN,
            html,
            count=1,
            flags=re.DOTALL
        )

    html = inject_overlay_before_body_close(html)
    html = inject_css_before_style_close(html, MOBILE_NAV_CSS + GLOBAL_MOBILE_FIXES)
    html = inject_js_before_body_close(html, TOGGLE_JS)
    return html

def process_dark_header(html: str) -> str:
    """For trilhas/index.html with dark green header and simple <nav>."""
    # Add hamburger after the nav closing tag inside site-header
    html = re.sub(
        r'(</nav>)(\s*\n?\s*</header>)',
        r'\1\n    ' + HAMBURGER_BTN + r'\2',
        html,
        count=1
    )
    html = inject_overlay_before_body_close(html)
    html = inject_css_before_style_close(html, MOBILE_NAV_CSS_DARK + GLOBAL_MOBILE_FIXES)
    html = inject_js_before_body_close(html, TOGGLE_JS_DARK)
    return html

def process_site_header_inner(html: str) -> str:
    """For pages using .site-header-inner (guias/index.html pattern)."""
    # Add id to nav if not present
    if 'id="main-nav"' not in html:
        html = re.sub(
            r'(<nav\b)([^>]*>)',
            r'\1 id="main-nav"\2',
            html,
            count=1
        )
    # Insert hamburger after nav closing tag
    html = re.sub(
        r'(</nav>)(\s*\n?\s*</div>)',  # </nav> then </div> (closes site-header-inner)
        r'\1\n        ' + HAMBURGER_BTN + r'\2',
        html,
        count=1
    )
    html = inject_overlay_before_body_close(html)
    html = inject_css_before_style_close(html, MOBILE_NAV_CSS + GLOBAL_MOBILE_FIXES)
    html = inject_js_before_body_close(html, TOGGLE_JS)
    return html

def process_file(path: Path) -> bool:
    html = path.read_text(encoding='utf-8')

    if has_hamburger(html):
        # Already has hamburger — just add global mobile fixes if missing
        if 'Global mobile fixes' not in html:
            html = inject_css_before_style_close(html, GLOBAL_MOBILE_FIXES)
            path.write_text(html, encoding='utf-8')
        return True  # already done

    if 'site-header' not in html:
        return False  # no header to process

    original = html

    # Determine which pattern
    if 'header-inner' in html and 'site-nav' in html:
        html = process_standard_header(html)
    elif 'site-header-inner' in html:
        html = process_site_header_inner(html)
    elif 'site-header' in html:
        # Could be dark/simple header or other variant
        if 'MOBILE_NAV_CSS_DARK' not in html and '<nav' in html:
            html = process_dark_header(html)

    if html != original:
        path.write_text(html, encoding='utf-8')
        return True
    return False

def main():
    html_files = list(ROOT.rglob('*.html'))
    # Exclude node_modules, admin, generated Python scripts' outputs we don't want
    html_files = [f for f in html_files if 'node_modules' not in str(f)]

    processed = 0
    skipped = 0
    for f in sorted(html_files):
        result = process_file(f)
        if result:
            processed += 1
        else:
            skipped += 1

    print(f"Processed: {processed} files")
    print(f"Skipped (no header or already done): {skipped} files")

if __name__ == '__main__':
    main()
