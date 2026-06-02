#!/usr/bin/env python3
"""UX-02 — Redesign footer on all static HTML pages."""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# ─── New footer HTML ────────────────────────────────────────────────────────

INSTAGRAM_SVG = '<svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clip-rule="evenodd"/></svg>'

TIKTOK_SVG = '<svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>'

YOUTUBE_SVG = '<svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'

NEW_FOOTER = f'''<footer class="site-footer">
<div class="container">
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="/" class="footer-logo-link" aria-label="Trekko — página inicial">
        <img src="/images/trekko_logo_horizontal_color_transparent.png" alt="Trekko" class="footer-logo-img" width="130" height="44" loading="lazy">
      </a>
      <p class="footer-tagline">A plataforma para quem vive a trilha.<br>Descubra, planeje e conecte-se com guias.</p>
    </div>
    <div class="footer-col">
      <h4>Sobre o Trekko</h4>
      <ul>
        <li><a href="/sobre">Sobre nós</a></li>
        <li><a href="/contato">Contato</a></li>
        <li><a href="/blog">Blog &amp; Guias</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Trilhas</h4>
      <ul>
        <li><a href="/trilhas">Ver trilhas</a></li>
        <li><a href="/guias">Guias</a></li>
        <li><a href="/trilhas#estados">Por estado</a></li>
        <li><a href="/trilhas#dificuldade">Por dificuldade</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <ul>
        <li><a href="/privacidade">Política de Privacidade</a></li>
        <li><a href="/termos-de-uso">Termos de Uso</a></li>
        <li><a href="/politica-de-cookies">Política de Cookies</a></li>
        <li><a href="/aviso-de-responsabilidade">Aviso de Responsabilidade</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 Trekko. Todos os direitos reservados.</p>
    <div class="footer-social">
      <a href="https://www.instagram.com/trekko.com.br/" target="_blank" rel="noopener noreferrer" aria-label="Siga o Trekko no Instagram">{INSTAGRAM_SVG}</a>
      <a href="https://www.tiktok.com/@trekko.com.br" target="_blank" rel="noopener noreferrer" aria-label="Siga o Trekko no TikTok">{TIKTOK_SVG}</a>
      <a href="https://www.youtube.com/@trekkooficial" target="_blank" rel="noopener noreferrer" aria-label="Siga o Trekko no YouTube">{YOUTUBE_SVG}</a>
    </div>
  </div>
</div>
</footer>'''

# ─── New footer CSS ─────────────────────────────────────────────────────────

NEW_FOOTER_CSS = (
    "/* Footer */\n"
    ".site-footer{background:var(--text-primary);color:rgba(255,255,255,.65);padding:3rem 0 2rem}\n"
    ".footer-inner{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:2rem}\n"
    ".footer-brand{grid-column:1/2}\n"
    ".footer-logo-link{display:inline-flex;align-items:center;margin-bottom:.75rem}\n"
    ".footer-logo-img{height:38px;width:auto;filter:brightness(0) invert(1)}\n"
    ".footer-tagline{font-size:.85rem;line-height:1.6;margin-bottom:.5rem}\n"
    ".footer-col h4{color:#fff;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.75rem}\n"
    ".footer-col ul li+li{margin-top:.4rem}\n"
    ".footer-col a{font-size:.85rem;color:rgba(255,255,255,.65);transition:color .15s}.footer-col a:hover{color:#fff}\n"
    ".footer-bottom{border-top:1px solid rgba(255,255,255,.1);margin-top:2rem;padding-top:1.5rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.75rem;font-size:.8rem}\n"
    ".footer-social{display:flex;gap:1rem;align-items:center}\n"
    ".footer-social a{display:flex;align-items:center;color:rgba(255,255,255,.55);transition:color .15s}.footer-social a:hover{color:#fff}\n"
    "@media(max-width:900px){.footer-inner{grid-template-columns:1fr 1fr}}\n"
    "@media(max-width:600px){.footer-inner{grid-template-columns:1fr}.footer-bottom{flex-direction:column;text-align:center}}"
)

# Patterns to detect/remove old footer CSS declarations in <style> blocks.
# IMPORTANT: use [^{}]+ (not [^\n]+) so we never consume more than one level
# of braces — otherwise the pattern eats the closing } of an enclosing @media
# block when the footer rule happens to be the last declaration on that line.
OLD_CSS_LINE_PATTERNS = [
    re.compile(r'\.footer-logo\{[^{}]+\}'),
    re.compile(r'\.footer-email[^\n]+\n?'),
    re.compile(r'\/\* Footer social \*\/\n?'),
    re.compile(r'\/\* Footer \*\/\n?'),
    # standalone footer property declarations
    re.compile(r'\.site-footer\{[^{}]+\}'),
    re.compile(r'\.footer-inner\{[^{}]+\}'),     # safe: stops at first }
    re.compile(r'\.footer-brand\{[^{}]+\}'),
    re.compile(r'\.footer-tagline\{[^{}]+\}'),
    re.compile(r'\.footer-logo-link\{[^{}]+\}'),
    re.compile(r'\.footer-logo-img\{[^{}]+\}'),
    re.compile(r'\.footer-col [^\n]+\n?'),
    re.compile(r'\.footer-bottom\{[^{}]+\}'),
    re.compile(r'\.footer-social\{[^{}]+\}'),
    re.compile(r'\.footer-social a\{[^{}]+\}'),
    re.compile(r'\.footer-social a:hover\{[^{}]+\}'),
]

# Regex to match the whole <footer ...> block
FOOTER_BLOCK_RE = re.compile(
    r'<footer[^>]*class="site-footer"[^>]*>.*?</footer>',
    re.DOTALL
)

# ─── CSS injection helper ────────────────────────────────────────────────────

def replace_footer_css(html: str) -> str:
    """Replace old footer CSS inside <style> tags with new CSS."""
    def patch_style(m):
        content = m.group(1)
        # Remove all old footer-related CSS lines
        for pat in OLD_CSS_LINE_PATTERNS:
            content = pat.sub('', content)
        # Append new footer CSS just before closing </style>
        content = content.rstrip() + '\n' + NEW_FOOTER_CSS + '\n'
        return f'<style>{content}</style>'

    return re.sub(r'<style>(.*?)</style>', patch_style, html, flags=re.DOTALL)


def replace_footer_html(html: str) -> str:
    if FOOTER_BLOCK_RE.search(html):
        return FOOTER_BLOCK_RE.sub(NEW_FOOTER, html)
    return html


def patch_file(path: str) -> bool:
    with open(path, encoding='utf-8') as f:
        original = f.read()

    if '<footer' not in original:
        return False

    patched = replace_footer_css(original)
    patched = replace_footer_html(patched)

    if patched == original:
        return False

    with open(path, 'w', encoding='utf-8') as f:
        f.write(patched)
    return True


# ─── Walk all HTML files ─────────────────────────────────────────────────────

updated, skipped = [], []

for dirpath, dirnames, filenames in os.walk(ROOT):
    # Skip admin and assets directories
    dirnames[:] = [d for d in dirnames if d not in ('admin', 'assets', '.git', 'docs')]
    for fname in filenames:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        try:
            if patch_file(fpath):
                updated.append(os.path.relpath(fpath, ROOT))
            else:
                skipped.append(os.path.relpath(fpath, ROOT))
        except Exception as e:
            print(f'ERROR {fpath}: {e}', file=sys.stderr)

print(f'Updated : {len(updated)} files')
print(f'Skipped : {len(skipped)} files (no footer or no change)')
if '--verbose' in sys.argv:
    for p in sorted(updated):
        print(f'  ✓ {p}')
