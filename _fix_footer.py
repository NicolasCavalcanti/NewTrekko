#!/usr/bin/env python3
"""Standardize footer nav, legal links, and social icons across all static pages."""

import re
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

CANONICAL_FOOTER = '''<footer class="site-footer">
<div class="container">
  <div class="footer-inner">
    <div class="footer-brand">
      <p class="footer-logo">Trekko</p>
      <p class="footer-tagline">A plataforma para quem vive a trilha.<br>Descubra, planeje e conecte-se com guias.</p>
      <p class="footer-email"><a href="mailto:contato@trekko.com.br">contato@trekko.com.br</a></p>
    </div>
    <div class="footer-col">
      <h4>Trilhas</h4>
      <ul>
        <li><a href="/trilhas/sao-paulo">São Paulo</a></li>
        <li><a href="/trilhas/rio-de-janeiro">Rio de Janeiro</a></li>
        <li><a href="/trilhas/minas-gerais">Minas Gerais</a></li>
        <li><a href="/trilhas/para-iniciantes">Para iniciantes</a></li>
        <li><a href="/trilhas/com-guia">Com guia</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Trekko</h4>
      <ul>
        <li><a href="/sobre">Sobre o Trekko</a></li>
        <li><a href="/contato">Contato</a></li>
        <li><a href="/guias/ativar-perfil">Ativar perfil de guia</a></li>
        <li><a href="/seguranca-em-trilhas">Segurança em trilhas</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Legal</h4>
      <ul>
        <li><a href="/privacidade">Política de Privacidade</a></li>
        <li><a href="/termos-de-uso">Termos de Uso</a></li>
        <li><a href="/politica-de-guias">Política de Guias</a></li>
        <li><a href="/politica-editorial">Política Editorial</a></li>
        <li><a href="/remocao-ou-atualizacao-de-dados">Remoção ou atualização de dados</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 Trekko. Todos os direitos reservados.</p>
    <div class="footer-social">
      <a href="https://www.instagram.com/trekko.com.br/" target="_blank" rel="noopener noreferrer" aria-label="Siga o Trekko no Instagram">
        <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clip-rule="evenodd"/></svg>
        @trekko.com.br
      </a>
      <a href="https://www.tiktok.com/@trekko.com.br" target="_blank" rel="noopener noreferrer" aria-label="Siga o Trekko no TikTok">
        <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
        @trekko.com.br
      </a>
    </div>
  </div>
</div>
</footer>'''

CANONICAL_LEGAL = '''      <h4>Legal</h4>
      <ul>
        <li><a href="/privacidade">Política de Privacidade</a></li>
        <li><a href="/termos-de-uso">Termos de Uso</a></li>
        <li><a href="/politica-de-guias">Política de Guias</a></li>
        <li><a href="/politica-editorial">Política Editorial</a></li>
        <li><a href="/remocao-ou-atualizacao-de-dados">Remoção ou atualização de dados</a></li>
      </ul>
    </div>'''

CANONICAL_FOOTER_BOTTOM = '''  <div class="footer-bottom">
    <p>© 2026 Trekko. Todos os direitos reservados.</p>
    <div class="footer-social">
      <a href="https://www.instagram.com/trekko.com.br/" target="_blank" rel="noopener noreferrer" aria-label="Siga o Trekko no Instagram">
        <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path fill-rule="evenodd" d="M12.315 2c2.43 0 2.784.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.784.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clip-rule="evenodd"/></svg>
        @trekko.com.br
      </a>
      <a href="https://www.tiktok.com/@trekko.com.br" target="_blank" rel="noopener noreferrer" aria-label="Siga o Trekko no TikTok">
        <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
        @trekko.com.br
      </a>
    </div>
  </div>'''


def fix_blog_footer(html, filepath):
    """Replace entire footer block for blog pages."""
    old = html
    html = re.sub(
        r'<footer class="site-footer">.*?</footer>',
        CANONICAL_FOOTER,
        html,
        flags=re.DOTALL
    )
    changed = html != old
    return html, changed


def fix_legal_section(html, filepath):
    """Fix pages with old trail legal pattern (4 links, missing politica-editorial)."""
    old = html

    # Pattern: has politica-de-guias but NOT politica-editorial in Legal section
    # Replace the entire Legal column closing </div>
    html = re.sub(
        r'(\s+<h4>Legal</h4>\s+<ul>\s+'
        r'<li><a href="/privacidade">Política de Privacidade</a></li>\s+'
        r'<li><a href="/termos-de-uso">Termos de Uso</a></li>\s+'
        r'<li><a href="/politica-de-guias">Política de Guias</a></li>\s+'
        r'<li><a href="/remocao-ou-atualizacao-de-dados">Remoção ou atualização de dados</a></li>\s+'
        r'</ul>\s+</div>)',
        CANONICAL_LEGAL,
        html,
        flags=re.DOTALL
    )
    changed = html != old
    return html, changed


def fix_footer_social(html, filepath):
    """Add social icons to footer-bottom where missing."""
    if 'footer-social' in html:
        return html, False

    old = html

    # Pattern A: single-line footer-bottom (blog old style)
    html = re.sub(
        r'  <div class="footer-bottom"><p>© 2026 Trekko\. Todos os direitos reservados\.</p></div>',
        CANONICAL_FOOTER_BOTTOM,
        html
    )

    if html == old:
        # Pattern B: multi-line footer-bottom without social
        html = re.sub(
            r'  <div class="footer-bottom">\s+<p>© 2026 Trekko\. Todos os direitos reservados\.</p>\s+</div>',
            CANONICAL_FOOTER_BOTTOM,
            html,
            flags=re.DOTALL
        )

    changed = html != old
    return html, changed


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    if '<h4>Legal</h4>' not in html and 'site-footer' not in html:
        return False, []

    changes = []
    is_blog_page = '/blog/' in filepath or filepath.endswith('/blog/index.html')

    if is_blog_page and '<h4>Blog</h4>' in html:
        html, changed = fix_blog_footer(html, filepath)
        if changed:
            changes.append('replaced full blog footer (Blog→Trekko column, fixed legal, added social)')

    if not changes:
        # Fix legal section for old trail pattern
        if '<h4>Legal</h4>' in html and 'politica-editorial' not in html:
            html, changed = fix_legal_section(html, filepath)
            if changed:
                changes.append('added politica-editorial to Legal section')

        # Add social icons if missing
        html, changed = fix_footer_social(html, filepath)
        if changed:
            changes.append('added social icons to footer-bottom')

    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True, changes

    return False, []


def main():
    import glob
    files = glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
    files.sort()

    total_changed = 0
    for filepath in files:
        # Skip the main React app and 404
        rel = os.path.relpath(filepath, ROOT)
        if rel in ('index.html', '404.html'):
            continue

        changed, reasons = process_file(filepath)
        if changed:
            total_changed += 1
            print(f'  FIXED: {rel}')
            for r in reasons:
                print(f'         - {r}')

    print(f'\nTotal files updated: {total_changed}')


if __name__ == '__main__':
    main()
