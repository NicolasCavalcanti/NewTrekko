#!/usr/bin/env python3
"""Add Google Ads compliance fixes:
1. Safety disclaimer to all /trilhas listing pages
2. Affiliate banner to equipment pages missing it
"""

import os
import re

SAFETY_DISCLAIMER_HTML = """
<section class="trekko-safety-notice" aria-label="Aviso de segurança">
  <div class="container">
    <div class="trekko-safety-inner">
      <span class="trekko-safety-icon" aria-hidden="true">⚠️</span>
      <p><strong>Aviso de segurança:</strong> Atividades ao ar livre envolvem riscos inerentes. Antes de sair, avalie suas condições físicas, consulte um guia certificado CADASTUR e verifique as condições locais. A Trekko fornece informações de referência e não se responsabiliza por acidentes ou condições adversas. <a href="/aviso-de-responsabilidade/">Saiba mais</a>.</p>
    </div>
  </div>
</section>"""

SAFETY_DISCLAIMER_CSS = """
<style id="trekko-safety-css">
.trekko-safety-notice{background:#fffbeb;border-top:3px solid #f59e0b;border-bottom:1px solid #fde68a;padding:12px 0}
.trekko-safety-inner{display:flex;align-items:flex-start;gap:10px;max-width:1140px;margin:0 auto;padding:0 20px}
.trekko-safety-icon{font-size:1.1rem;flex-shrink:0;margin-top:1px}
.trekko-safety-notice p{font-size:.83rem;color:#78350f;line-height:1.5;margin:0}
.trekko-safety-notice a{color:#92400e;font-weight:600;text-decoration:underline}
</style>
"""

AFFILIATE_BANNER_CSS = """    .affiliate-banner{background:var(--earth-light,#fef9ed);border-bottom:1px solid #e8d5a0;padding:8px 0;font-size:.78rem;color:#78530a;text-align:center}
    .affiliate-banner a{color:#7f4413;font-weight:600}
"""

AFFILIATE_BANNER_HTML = """<div class="affiliate-banner" role="note">
  <div class="container"><p>Este artigo contém <strong>links de afiliados</strong>. Se você comprar através deles, recebemos uma comissão sem custo adicional para você. <a href="/divulgacao-de-afiliados">Saiba mais</a>.</p></div>
</div>"""


def has_safety_disclaimer(content):
    return 'trekko-safety-notice' in content or 'aviso-de-responsabilidade' in content


def add_safety_disclaimer_to_trilhas_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_safety_disclaimer(content):
        return False

    # Insert CSS before </head>
    if SAFETY_DISCLAIMER_CSS.strip() not in content:
        content = content.replace('</head>', SAFETY_DISCLAIMER_CSS + '</head>', 1)

    # Insert disclaimer before the footer
    if '<footer class="site-footer">' in content:
        content = content.replace(
            '<footer class="site-footer">',
            SAFETY_DISCLAIMER_HTML + '\n\n<footer class="site-footer">',
            1
        )
    elif '</main>' in content:
        content = content.replace('</main>', SAFETY_DISCLAIMER_HTML + '\n</main>', 1)
    else:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def add_affiliate_banner(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'affiliate-banner' in content:
        return False

    # Add CSS
    if '.affiliate-banner' not in content:
        # Insert before </style> in the first style block
        content = re.sub(r'(</style>)', AFFILIATE_BANNER_CSS + r'\1', content, count=1)

    # Insert after breadcrumb nav or after header
    if '<nav class="breadcrumb"' in content:
        # Find end of breadcrumb nav
        idx = content.find('</nav>', content.find('<nav class="breadcrumb"'))
        if idx != -1:
            insert_pos = idx + len('</nav>')
            content = content[:insert_pos] + '\n' + AFFILIATE_BANNER_HTML + '\n' + content[insert_pos:]
    elif '</header>' in content:
        content = content.replace('</header>', '</header>\n' + AFFILIATE_BANNER_HTML, 1)
    else:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    base = os.path.dirname(os.path.abspath(__file__))

    # Fix trilhas listing pages
    trilhas_dir = os.path.join(base, 'trilhas')
    fixed_trilhas = 0
    for root, dirs, files in os.walk(trilhas_dir):
        for fname in files:
            if fname == 'index.html':
                fp = os.path.join(root, fname)
                if add_safety_disclaimer_to_trilhas_page(fp):
                    fixed_trilhas += 1
                    print(f'  + safety disclaimer: {fp[len(base):]}')
    print(f'Added safety disclaimer to {fixed_trilhas} trilhas pages.')

    # Fix equipment pages missing affiliate banner
    equip_dirs = [
        os.path.join(base, 'equipamentos', 'como-escolhemos'),
        os.path.join(base, 'equipamentos', 'comparativos'),
        os.path.join(base, 'equipamentos', 'guias'),
        os.path.join(base, 'equipamentos', 'seguranca-em-trilhas'),
    ]
    fixed_equip = 0
    for d in equip_dirs:
        fp = os.path.join(d, 'index.html')
        if os.path.exists(fp):
            if add_affiliate_banner(fp):
                fixed_equip += 1
                print(f'  + affiliate banner: {fp[len(base):]}')
    print(f'Added affiliate banner to {fixed_equip} equipment pages.')


if __name__ == '__main__':
    main()
