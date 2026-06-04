#!/usr/bin/env python3
"""Generate blog category index pages at /blog/{category}/index.html."""
import json, os

BASE_URL = "https://trekko.com.br"

CATEGORIES = {
    "equipamentos":           ("Equipamentos", "Guias de equipamentos para trekking e trilhas: botas, mochilas, camadas de roupa, bastões e tudo que você precisa saber antes de escolher seu gear."),
    "conservacao-ambiental":  ("Conservação Ambiental", "Artigos sobre conservação de trilhas, parques nacionais e boas práticas para quem ama a natureza e quer preservá-la."),
    "planejamento-seguranca": ("Planejamento e Segurança", "Guias de planejamento e segurança para trekking: como se preparar, o que levar, primeiros socorros e como evitar acidentes em trilhas."),
    "guias-praticos":         ("Guias Práticos", "Guias práticos para trilheiros de todos os níveis: como começar, escolher trilha, contratar guia e aproveitar ao máximo cada aventura."),
    "trilhas-destinos":       ("Trilhas e Destinos", "Roteiros e guias dos melhores destinos de trekking no Brasil: Chapada Diamantina, Lençóis Maranhenses, cânions do Sul e muito mais."),
}

TEMPLATE = """\
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | Blog Trekko</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title} | Blog Trekko">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://trekko.com.br/images/trekko_logo_horizontal_color_transparent.png">
<link rel="icon" href="/favicon-48x48.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap"></noscript>
<script>window.TREKKO_CONFIG={{GA4_ID:'G-S816P190VN',GTM_ID:null,ADS_ID:'AW-355784943'}};</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S816P190VN"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-S816P190VN');</script>
<script defer src="/assets/trekko-analytics.js"></script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type": "ListItem", "position": 1, "name": "Trekko", "item": "https://trekko.com.br"}},
        {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://trekko.com.br/blog"}},
        {{"@type": "ListItem", "position": 3, "name": "{label}", "item": "{canonical}"}}
      ]
    }}
  ]
}}
</script>
<style>
  .bc{{padding:.6rem 0;border-bottom:1px solid #e2e8f0;font-family:Inter,system-ui,sans-serif}}
  .bc .container{{max-width:1200px;margin:0 auto;padding:0 1rem}}
  .bc ol{{display:flex;flex-wrap:wrap;gap:.25rem;align-items:center;font-size:.8rem;color:#64748b;list-style:none;margin:0;padding:0}}
  .bc li+li::before{{content:"/";margin-right:.25rem;color:#94a3b8}}
  .bc a{{color:#64748b;text-decoration:none}}
  .bc a:hover{{color:#15803d}}
  .bc [aria-current=page]{{color:#1e293b;font-weight:500}}
  #root{{min-height:100svh}}
</style>
<script type="module" crossorigin src="/assets/index-DSKK19TW.js"></script>
<link rel="modulepreload" crossorigin href="/assets/react-vendor-DViTTRkQ.js">
<link rel="modulepreload" crossorigin href="/assets/radix-ui-D-C9zAgG.js">
<link rel="stylesheet" crossorigin href="/assets/index-CKkMVUOE.css">
</head>
<body>
<nav class="bc" aria-label="Navegação estrutural">
  <div class="container"><ol>
    <li><a href="/">Trekko</a></li>
    <li><a href="/blog">Blog</a></li>
    <li><span aria-current="page">{label}</span></li>
  </ol></div>
</nav>
<div id="root"></div>
</body>
</html>"""

with open("data/blog.json", encoding="utf-8") as f:
    posts = json.load(f)

for slug, (label, desc) in CATEGORIES.items():
    canonical = f"{BASE_URL}/blog/{slug}"
    html = TEMPLATE.format(title=label, desc=desc, canonical=canonical, label=label)
    out_path = os.path.join("blog", slug, "index.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  wrote {out_path}")

print("\nDone: 5 category pages generated")
