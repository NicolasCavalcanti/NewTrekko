#!/usr/bin/env python3
"""Generates static SEO trail pages and numeric redirect stubs."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "data", "trails.json")) as f:
    trails = json.load(f)

DIFF_LABELS = {
    "easy": "Fácil",
    "moderate": "Moderado",
    "hard": "Difícil",
    "expert": "Especialista",
}

SLUG_TO_ID = {t["slug"]: t["id"] for t in trails}

ANALYTICS = """\
<script>window.TREKKO_CONFIG={GA4_ID:'G-S816P190VN',GTM_ID:null,ADS_ID:'AW-355784943'};</script>
<script>(function(){var id=(window.TREKKO_CONFIG||{}).GTM_ID;if(!id)return;window.dataLayer=window.dataLayer||[];window.dataLayer.push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=document.getElementsByTagName('script')[0],j=document.createElement('script');j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+id;f.parentNode.insertBefore(j,f);})();</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S816P190VN"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-S816P190VN',{send_page_view:!(window.TREKKO_CONFIG&&window.TREKKO_CONFIG.GTM_ID)});</script>
<script src="/assets/trekko-analytics.js"></script>"""

FAVICONS = """\
<link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48">
<link rel="icon" href="/android-chrome-192x192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="/site.webmanifest">"""

FONTS = """\
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet">"""

SLUG_REDIRECT_JS = """\
<script>
(function(){
  var slugToId={%s};
  var m=window.location.pathname.match(/^\\/trilha\\/([^/]+)\\/?$/);
  if(m&&isNaN(parseInt(m[1],10))){var id=slugToId[m[1]];if(id)window.history.replaceState(null,'','/trilha/'+id);}
})();
</script>"""

REACT_SCRIPTS = """\
<script type="module" crossorigin src="/assets/index-DSKK19TW.js"></script>
<link rel="modulepreload" crossorigin href="/assets/react-vendor-DViTTRkQ.js">
<link rel="modulepreload" crossorigin href="/assets/radix-ui-D-C9zAgG.js">
<link rel="stylesheet" crossorigin href="/assets/index-CKkMVUOE.css">"""

CSS = """\
<style>
:root{--primary:#15803d;--primary-dark:#166534;--primary-hover:#16a34a;--primary-light:#dcfce7;--primary-bg:#f0fdf4;--accent:#f59e0b;--text-primary:#1e293b;--text-secondary:#475569;--text-muted:#94a3b8;--border:#e2e8f0;--white:#fff;--bg-light:#f8fafc;--diff-easy:#15803d;--diff-moderate:#d97706;--diff-hard:#ea580c;--diff-expert:#dc2626;--shadow-sm:0 1px 3px rgba(0,0,0,.08);--shadow-md:0 4px 12px rgba(0,0,0,.1);--radius:8px;--font-body:'Inter',sans-serif;--font-heading:'Sora',sans-serif;--max-w:1200px;--gutter:1.25rem}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}body{font-family:var(--font-body);color:var(--text-primary);line-height:1.6;background:var(--white)}
img{max-width:100%;height:auto;display:block}a{color:inherit;text-decoration:none}
.container{max-width:var(--max-w);margin:0 auto;padding:0 var(--gutter)}
h1,h2,h3{font-family:var(--font-heading);line-height:1.25;color:var(--text-primary)}
h1{font-size:clamp(1.75rem,5vw,2.75rem);font-weight:700}h2{font-size:clamp(1.25rem,3vw,1.75rem);font-weight:700;margin-bottom:.75rem}h3{font-size:1.05rem;font-weight:600}
p{color:var(--text-secondary);line-height:1.7}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;padding:.75rem 1.5rem;border-radius:var(--radius);font-family:var(--font-body);font-weight:600;font-size:1rem;cursor:pointer;border:2px solid transparent;transition:all .2s;text-decoration:none}
.btn--primary{background:var(--primary);color:var(--white);border-color:var(--primary)}.btn--primary:hover{background:var(--primary-hover)}
.btn--outline{background:transparent;color:var(--primary);border-color:var(--primary)}.btn--outline:hover{background:var(--primary-light)}
.btn--lg{padding:1rem 2rem;font-size:1.1rem}.btn--sm{padding:.5rem 1rem;font-size:.875rem}
.site-header{position:sticky;top:0;z-index:100;background:var(--white);border-bottom:1px solid var(--border)}
.header-inner{display:flex;align-items:center;justify-content:space-between;height:64px;gap:1rem}
.logo{font-family:var(--font-heading);font-weight:700;font-size:1.4rem;color:var(--primary);display:flex;align-items:center;gap:.4rem}
.header-nav{display:none;gap:1.5rem}.header-nav a{color:var(--text-secondary);font-size:.95rem;font-weight:500;transition:color .2s}.header-nav a:hover{color:var(--primary)}
@media(min-width:768px){.header-nav{display:flex}}
.breadcrumb{background:var(--bg-light);border-bottom:1px solid var(--border);padding:.625rem 0}
.breadcrumb ol{display:flex;flex-wrap:wrap;gap:.25rem;align-items:center;font-size:.85rem}
.breadcrumb li{display:flex;align-items:center;gap:.25rem;color:var(--text-muted)}
.breadcrumb li a{color:var(--text-secondary);transition:color .15s}.breadcrumb li a:hover{color:var(--primary)}
.breadcrumb li:last-child{color:var(--text-primary);font-weight:500}
.trail-hero{background:linear-gradient(135deg,rgba(21,128,61,.88) 0%,rgba(20,83,45,.95) 100%),var(--hero-img) center/cover no-repeat;padding:4rem 0 3rem;color:var(--white)}
.trail-hero h1{color:var(--white);margin-bottom:.75rem}
.hero-sub{font-size:1.05rem;color:rgba(255,255,255,.88);margin-bottom:1.5rem}
.hero-meta{display:flex;flex-wrap:wrap;gap:.75rem;margin-bottom:2rem}
.hero-tag{display:inline-flex;align-items:center;gap:.35rem;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.25);border-radius:100px;padding:.3rem .85rem;font-size:.82rem;font-weight:500}
.hero-ctas{display:flex;flex-wrap:wrap;gap:.75rem}
.stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1rem;padding:2.5rem 0}
.stat-card{background:var(--bg-light);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;text-align:center}
.stat-card .val{font-family:var(--font-heading);font-size:1.3rem;font-weight:700;color:var(--primary)}
.stat-card .lbl{font-size:.8rem;color:var(--text-muted);margin-top:.25rem}
.section{padding:3rem 0}.section--alt{background:var(--bg-light)}
.highlights-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem;margin-top:1rem}
.highlight-item{display:flex;align-items:center;gap:.5rem;background:var(--primary-bg);border:1px solid var(--primary-light);border-radius:var(--radius);padding:.7rem 1rem;font-size:.9rem;font-weight:500;color:var(--primary-dark)}
.badge{display:inline-flex;align-items:center;border-radius:100px;padding:.25rem .7rem;font-size:.78rem;font-weight:600}
.badge--easy{background:#dcfce7;color:#15803d}.badge--moderate{background:#fef3c7;color:#b45309}.badge--hard{background:#ffedd5;color:#c2410c}.badge--expert{background:#fee2e2;color:#b91c1c}
.info-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:1rem;margin-top:1rem}
.info-item{border:1px solid var(--border);border-radius:var(--radius);padding:1rem}
.info-item .info-label{font-size:.78rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:.25rem}
.info-item .info-val{font-weight:600;color:var(--text-primary)}
.cta-section{background:linear-gradient(135deg,var(--primary) 0%,var(--primary-dark) 100%);padding:3.5rem 0;text-align:center;color:var(--white)}
.cta-section h2{color:var(--white);margin-bottom:.75rem}
.cta-section p{color:rgba(255,255,255,.85);max-width:560px;margin:0 auto 1.75rem}
.site-footer{background:#0f172a;color:#94a3b8;padding:2rem 0;text-align:center;font-size:.85rem}
.site-footer a{color:#64748b;transition:color .15s}.site-footer a:hover{color:var(--white)}
.footer-links{display:flex;flex-wrap:wrap;justify-content:center;gap:1.5rem;margin-bottom:.75rem}
/* Hide static content once React has mounted */
body.react-ready #trail-static{display:none}
</style>"""


def diff_badge(diff):
    return f'<span class="badge badge--{diff}">{DIFF_LABELS.get(diff, diff)}</span>'


def guide_tag(required):
    if required:
        return '<span class="hero-tag">🧭 Guia obrigatório</span>'
    return '<span class="hero-tag">🚶 Sem guia obrigatório</span>'


def build_slug_map():
    pairs = ", ".join(f"'{t['slug']}': {t['id']}" for t in trails)
    return SLUG_REDIRECT_JS % pairs


def build_jsonld(t):
    canonical = f"https://trekko.com.br/trilha/{t['slug']}"
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Trekko", "item": "https://trekko.com.br"},
                    {"@type": "ListItem", "position": 2, "name": "Trilhas", "item": "https://trekko.com.br/trilhas"},
                    {"@type": "ListItem", "position": 3, "name": t["name"], "item": canonical},
                ],
            },
            {
                "@type": "TouristDestination",
                "@id": canonical,
                "name": t["name"],
                "description": t["shortDescription"],
                "url": canonical,
                "image": f"https://trekko.com.br{t['imageUrl']}",
                "touristType": "Trilha / Trekking",
                "geo": {"@type": "GeoCoordinates"},
                "containedInPlace": {
                    "@type": "Place",
                    "name": t["region"],
                    "address": {"@type": "PostalAddress", "addressCountry": "BR", "addressRegion": t["uf"]},
                },
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False, indent=None)


def highlights_html(t):
    if not t.get("highlights"):
        return ""
    items = "".join(f'<li class="highlight-item">✓ {h}</li>' for h in t["highlights"])
    return f"""
<section class="section">
<div class="container">
<h2>Destaques da trilha</h2>
<ul class="highlights-list">{items}</ul>
</div>
</section>"""


def info_items(t):
    items = [
        ("Distância", f'{t["distanceKm"]} km'),
        ("Desnível", f'+{t["elevationGain"]} m'),
        ("Altitude máx.", f'{t["maxAltitude"]} m'),
        ("Duração", t["estimatedTime"]),
        ("Melhor época", t["bestSeason"]),
        ("Taxa de entrada", t["entranceFee"]),
    ]
    html = ""
    for label, val in items:
        html += f'<div class="info-item"><div class="info-label">{label}</div><div class="info-val">{val}</div></div>'
    return html


REACT_MOUNT_SCRIPT = """\
<script>
(function(){
  var ro=new MutationObserver(function(mutations){
    for(var i=0;i<mutations.length;i++){
      var nodes=mutations[i].addedNodes;
      for(var j=0;j<nodes.length;j++){
        if(nodes[j].nodeType===1&&nodes[j].id!=='trail-static'){
          document.body.classList.add('react-ready');
          ro.disconnect();return;
        }
      }
    }
  });
  var root=document.getElementById('root');
  if(root) ro.observe(root,{childList:true});
})();
</script>"""


def build_slug_page(t):
    slug = t["slug"]
    canonical = "https://trekko.com.br/trilha/" + slug
    title = t["name"] + " — Trilha em " + t["region"] + " (" + t["uf"] + ") | Trekko"
    desc = t["shortDescription"]
    image = "https://trekko.com.br" + t["imageUrl"]
    diff = DIFF_LABELS.get(t["difficulty"], t["difficulty"])

    slug_map = build_slug_map()
    jsonld = build_jsonld(t)

    parts = [
        '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n',
        '<meta charset="UTF-8">\n',
        '<meta name="viewport" content="width=device-width,initial-scale=1.0">\n',
        f'<title>{title}</title>\n',
        f'<meta name="description" content="{desc}">\n',
        f'<link rel="canonical" href="{canonical}">\n',
        f'<meta property="og:title" content="{title}">\n',
        f'<meta property="og:description" content="{desc}">\n',
        '<meta property="og:type" content="website">\n',
        f'<meta property="og:url" content="{canonical}">\n',
        f'<meta property="og:image" content="{image}">\n',
        FAVICONS + "\n",
        FONTS + "\n",
        ANALYTICS + "\n",
        f'<script type="application/ld+json">{jsonld}</script>\n',
        CSS + "\n",
        REACT_SCRIPTS + "\n",
        slug_map + "\n",
        '</head>\n<body>\n',
        '<div id="trail-static">\n',
        '<header class="site-header">\n<div class="container">\n<div class="header-inner">\n',
        '<a href="/" class="logo">',
        '<svg class="logo-icon" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">',
        '<path d="M16 3L4 12v17h8v-9h8v9h8V12L16 3z" fill="currentColor" opacity=".15"/>',
        '<path d="M16 3L4 12v17h8v-9h8v9h8V12L16 3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
        '</svg>Trekko</a>\n',
        '<nav class="header-nav" aria-label="Menu principal">',
        '<a href="/trilhas">Trilhas</a><a href="/guias">Guias</a><a href="/sobre">Sobre</a>',
        '</nav>\n</div>\n</div>\n</header>\n',
        '<nav class="breadcrumb" aria-label="Localização na página">\n<div class="container">\n<ol>\n',
        '<li><a href="/">Trekko</a> <span aria-hidden="true">›</span></li>\n',
        '<li><a href="/trilhas">Trilhas</a> <span aria-hidden="true">›</span></li>\n',
        f'<li>{t["name"]}</li>\n',
        '</ol>\n</div>\n</nav>\n',
        f'<section class="trail-hero" style="--hero-img:url(\'{t["imageUrl"]}\')\">\n<div class="container">\n',
        '<div class="hero-meta">\n',
        diff_badge(t["difficulty"]) + "\n",
        f'<span class="hero-tag">\U0001f4cd {t["region"]}, {t["uf"]}</span>\n',
        f'<span class="hero-tag">\U0001f4cf {t["distanceKm"]} km</span>\n',
        guide_tag(t["guideRequired"]) + "\n",
        '</div>\n',
        f'<h1>{t["name"]}</h1>\n',
        f'<p class="hero-sub">{t["hookText"]}</p>\n',
        '<div class="hero-ctas">\n',
        '<a href="/guias" class="btn btn--primary btn--lg">Encontrar guia para esta trilha</a>\n',
        '<a href="/trilhas" class="btn btn--outline-white btn--lg" style="color:#fff;border-color:rgba(255,255,255,.7)">Ver todas as trilhas</a>\n',
        '</div>\n</div>\n</section>\n',
        '<div class="container">\n<div class="stats-grid">\n',
        f'<div class="stat-card"><div class="val">{t["distanceKm"]} km</div><div class="lbl">Distância</div></div>\n',
        f'<div class="stat-card"><div class="val">+{t["elevationGain"]} m</div><div class="lbl">Desnível</div></div>\n',
        f'<div class="stat-card"><div class="val">{t["maxAltitude"]} m</div><div class="lbl">Altitude máx.</div></div>\n',
        f'<div class="stat-card"><div class="val">{diff}</div><div class="lbl">Dificuldade</div></div>\n',
        f'<div class="stat-card"><div class="val">{t["estimatedTime"]}</div><div class="lbl">Duração</div></div>\n',
        '</div>\n</div>\n',
        '<section class="section">\n<div class="container">\n',
        '<h2>Sobre a trilha</h2>\n',
        f'<p>{t["description"]}</p>\n',
        '</div>\n</section>\n',
        highlights_html(t) + "\n",
        '<section class="section section--alt">\n<div class="container">\n',
        '<h2>Informações práticas</h2>\n',
        '<div class="info-grid">\n',
        info_items(t) + "\n",
        '</div>\n</div>\n</section>\n',
        '<section class="cta-section">\n<div class="container">\n',
        f'<h2>Pronto para explorar {t["name"]}?</h2>\n',
        f'<p>{t["ctaText"]}</p>\n',
        '<a href="/guias" class="btn btn--white btn--lg">Encontrar guias certificados CADASTUR</a>\n',
        '</div>\n</section>\n',
        '<footer class="site-footer">\n<div class="container">\n',
        '<div class="footer-links">',
        '<a href="/sobre">Sobre</a><a href="/contato">Contato</a>',
        '<a href="/termos-de-uso">Termos de uso</a><a href="/privacidade">Privacidade</a>',
        '</div>\n<p>© 2025 Trekko · Todos os direitos reservados</p>\n',
        '</div>\n</footer>\n',
        '</div>\n',
        '<div id="root"></div>\n',
        REACT_MOUNT_SCRIPT + "\n",
        '</body>\n</html>',
    ]
    return "".join(parts)


def build_numeric_page(t):
    """Simple React SPA stub with trail-specific meta for numeric-ID URLs."""
    title = f'{t["name"]} — {t["region"]} | Trekko'
    desc = t["shortDescription"]
    image = f"https://trekko.com.br{t['imageUrl']}"
    canonical_slug = f"https://trekko.com.br/trilha/{t['slug']}"

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical_slug}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
{FAVICONS}
{FONTS}
{ANALYTICS}
{REACT_SCRIPTS}
</head>
<body>
<div id="root"></div>
</body>
</html>"""


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path.replace(BASE, '')}")


print("Generating trail pages...")
for t in trails:
    slug = t["slug"]
    tid = t["id"]

    # Slug-based SEO page
    write(os.path.join(BASE, "trilha", slug, "index.html"), build_slug_page(t))

    # Numeric-ID stub (fixes existing links, canonical points to slug)
    write(os.path.join(BASE, "trilha", str(tid), "index.html"), build_numeric_page(t))

print(f"\nDone: {len(trails)*2} files generated ({len(trails)} slug pages + {len(trails)} numeric stubs)")
