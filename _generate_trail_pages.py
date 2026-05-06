#!/usr/bin/env python3
"""Generates trail detail pages: SEO head + React SPA body (slug and numeric)."""
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

# Pre-boot script: translates /trilha/{slug} → /trilha/{id} in history
# so React Router's /trilha/:id route renders the correct component.
def slug_redirect_script(trails):
    pairs = ", ".join(f"'{t['slug']}': {t['id']}" for t in trails)
    return (
        "<script>\n"
        "(function(){\n"
        "  var m=window.location.pathname.match(/^\\/trilha\\/([^/]+)\\/?$/);\n"
        "  if(m&&isNaN(parseInt(m[1],10))){\n"
        "    var map={" + pairs + "};\n"
        "    var id=map[m[1]];\n"
        "    if(id)window.history.replaceState(null,'','/trilha/'+id);\n"
        "  }\n"
        "})();\n"
        "</script>"
    )


def build_jsonld(t):
    slug = t["slug"]
    canonical = "https://trekko.com.br/trilha/" + slug
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
                "image": "https://trekko.com.br" + t["imageUrl"],
                "touristType": "Trilha / Trekking",
                "containedInPlace": {
                    "@type": "Place",
                    "name": t["region"],
                    "address": {
                        "@type": "PostalAddress",
                        "addressCountry": "BR",
                        "addressRegion": t["uf"],
                    },
                },
            },
        ],
    }
    return json.dumps(data, ensure_ascii=False)


def build_slug_page(t, redirect_script):
    """React SPA page with trail-specific SEO head. Body = React root only."""
    slug = t["slug"]
    canonical = "https://trekko.com.br/trilha/" + slug
    diff = DIFF_LABELS.get(t["difficulty"], t["difficulty"])
    title = t["name"] + " — " + t["region"] + " (" + t["uf"] + ") | Trekko"
    desc = (
        t["shortDescription"]
        + " Dificuldade: " + diff
        + ". Distância: " + str(t["distanceKm"]) + " km."
        + " Duração: " + t["estimatedTime"] + "."
    )
    image = "https://trekko.com.br" + t["imageUrl"]
    jsonld = build_jsonld(t)

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta name="google-adsense-account" content="ca-pub-2482023752745520">
  <script>
    window.TREKKO_CONFIG = {{
      GA4_ID: 'G-S816P190VN',
      GTM_ID: null,
      ADS_ID: 'AW-355784943'
    }};
  </script>
  <script>(function(){{var id=(window.TREKKO_CONFIG||{{}}).GTM_ID;if(!id)return;window.dataLayer=window.dataLayer||[];window.dataLayer.push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=document.getElementsByTagName('script')[0],j=document.createElement('script');j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+id;f.parentNode.insertBefore(j,f);}})();</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-S816P190VN"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-S816P190VN',{{send_page_view:!(window.TREKKO_CONFIG&&window.TREKKO_CONFIG.GTM_ID)}});</script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{t['shortDescription']}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{image}" />
  <link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48" />
  <link rel="icon" href="/android-chrome-192x192.png" type="image/png" sizes="192x192" />
  <link rel="icon" href="/android-chrome-512x512.png" type="image/png" sizes="512x512" />
  <link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32" />
  <link rel="icon" href="/favicon-16x16.png" type="image/png" sizes="16x16" />
  <link rel="icon" href="/favicon.ico" type="image/x-icon" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180" />
  <link rel="shortcut icon" href="/favicon-48x48.png" type="image/png" />
  <link rel="manifest" href="/site.webmanifest" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <script type="application/ld+json">{jsonld}</script>
  <script src="/assets/trekko-analytics.js"></script>
  {redirect_script}
  <script type="module" crossorigin src="/assets/index-DSKK19TW.js"></script>
  <link rel="modulepreload" crossorigin href="/assets/react-vendor-DViTTRkQ.js">
  <link rel="modulepreload" crossorigin href="/assets/radix-ui-D-C9zAgG.js">
  <link rel="stylesheet" crossorigin href="/assets/index-CKkMVUOE.css">
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <div id="root"></div>
</body>
</html>"""


def build_numeric_page(t):
    """Numeric-ID page: same as slug page but canonical points to slug URL."""
    slug = t["slug"]
    canonical_slug = "https://trekko.com.br/trilha/" + slug
    title = t["name"] + " — " + t["region"] + " | Trekko"
    image = "https://trekko.com.br" + t["imageUrl"]

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta name="google-adsense-account" content="ca-pub-2482023752745520">
  <script>
    window.TREKKO_CONFIG = {{
      GA4_ID: 'G-S816P190VN',
      GTM_ID: null,
      ADS_ID: 'AW-355784943'
    }};
  </script>
  <script>(function(){{var id=(window.TREKKO_CONFIG||{{}}).GTM_ID;if(!id)return;window.dataLayer=window.dataLayer||[];window.dataLayer.push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=document.getElementsByTagName('script')[0],j=document.createElement('script');j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+id;f.parentNode.insertBefore(j,f);}})();</script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-S816P190VN"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-S816P190VN',{{send_page_view:!(window.TREKKO_CONFIG&&window.TREKKO_CONFIG.GTM_ID)}});</script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{t['shortDescription']}" />
  <link rel="canonical" href="{canonical_slug}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{t['shortDescription']}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical_slug}" />
  <meta property="og:image" content="{image}" />
  <link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48" />
  <link rel="icon" href="/android-chrome-192x192.png" type="image/png" sizes="192x192" />
  <link rel="icon" href="/android-chrome-512x512.png" type="image/png" sizes="512x512" />
  <link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32" />
  <link rel="icon" href="/favicon-16x16.png" type="image/png" sizes="16x16" />
  <link rel="icon" href="/favicon.ico" type="image/x-icon" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180" />
  <link rel="shortcut icon" href="/favicon-48x48.png" type="image/png" />
  <link rel="manifest" href="/site.webmanifest" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <script src="/assets/trekko-analytics.js"></script>
  <script type="module" crossorigin src="/assets/index-DSKK19TW.js"></script>
  <link rel="modulepreload" crossorigin href="/assets/react-vendor-DViTTRkQ.js">
  <link rel="modulepreload" crossorigin href="/assets/radix-ui-D-C9zAgG.js">
  <link rel="stylesheet" crossorigin href="/assets/index-CKkMVUOE.css">
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <div id="root"></div>
</body>
</html>"""


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path.replace(BASE, '')}")


print("Generating trail pages...")
redirect_script = slug_redirect_script(trails)
for t in trails:
    write(os.path.join(BASE, "trilha", t["slug"], "index.html"), build_slug_page(t, redirect_script))
    write(os.path.join(BASE, "trilha", str(t["id"]), "index.html"), build_numeric_page(t))

print(f"\nDone: {len(trails)*2} files ({len(trails)} slug + {len(trails)} numeric)")
