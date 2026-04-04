#!/usr/bin/env python3
"""
Trekko Programmatic SEO Page Generator
Generates pre-rendered HTML pages for organic search.
Run: python3 scripts/generate_seo_pages.py
"""

import json, re, math
from pathlib import Path
from collections import defaultdict
from datetime import date

BASE_URL = "https://trekko.com.br"
BASE_DIR = Path(__file__).parent.parent
TODAY = date.today().isoformat()

STATE_NAMES = {
    "AC":"Acre","AL":"Alagoas","AP":"Amapá","AM":"Amazonas","BA":"Bahia",
    "CE":"Ceará","DF":"Distrito Federal","ES":"Espírito Santo","GO":"Goiás",
    "MA":"Maranhão","MT":"Mato Grosso","MS":"Mato Grosso do Sul",
    "MG":"Minas Gerais","PA":"Pará","PB":"Paraíba","PR":"Paraná",
    "PE":"Pernambuco","PI":"Piauí","RJ":"Rio de Janeiro","RN":"Rio Grande do Norte",
    "RS":"Rio Grande do Sul","RO":"Rondônia","RR":"Roraima","SC":"Santa Catarina",
    "SP":"São Paulo","SE":"Sergipe","TO":"Tocantins"
}

DIFFICULTY = {
    "easy":    {"pt":"Fácil",       "color":"#16a34a","bg":"#dcfce7","desc":"Ideal para iniciantes e famílias. Terreno plano ou levemente ondulado, curta distância.","distance":"2–10 km","time":"1–3h","elevation":"até 200m","fitness":"Qualquer nível"},
    "moderate":{"pt":"Moderada",    "color":"#ca8a04","bg":"#fef9c3","desc":"Exige condicionamento físico básico. Alguns trechos íngremes e maior distância.","distance":"8–20 km","time":"3–6h","elevation":"200–600m","fitness":"Condicionamento básico a intermediário"},
    "hard":    {"pt":"Difícil",     "color":"#dc2626","bg":"#fee2e2","desc":"Exige bom preparo físico e experiência em trekking. Terreno acidentado e grande desnível.","distance":"15–35 km","time":"6–12h","elevation":"600–1500m","fitness":"Preparo físico avançado"},
    "expert":  {"pt":"Especialista","color":"#9333ea","bg":"#f3e8ff","desc":"Expedições de múltiplos dias em terreno extremo. Guia e equipamento completo obrigatórios.","distance":"30–100+ km","time":"vários dias","elevation":"1500m+","fitness":"Atlético, treinamento específico"},
}

GEAR = {
    "easy":    ["Tênis de caminhada","Mochila 10–15L","Água 1L","Protetor solar","Repelente","Lanche leve"],
    "moderate":["Bota de trilha","Mochila 20–30L","Água 2L+","Kit primeiros-socorros","Bastões","Capa de chuva","Lanterna"],
    "hard":    ["Bota impermeável","Mochila 30–50L","Água 3L+","Kit completo de primeiros-socorros","Bastões","Capa de chuva","Lanterna frontal","Saco de dormir","Barraca"],
    "expert":  ["Bota de montanhismo","Mochila 60–80L","Filtro de água","Kit sobrevivência","GPS","Rádio comunicador","Equipamento de escalada","Roupas técnicas em camadas"],
}

STATE_DESC = {
    "SP":"São Paulo concentra trilhas na Serra da Mantiqueira, Paranapiacaba e no Vale do Ribeira, com uma das comunidades de trekking mais ativas do país.",
    "RJ":"O Rio de Janeiro combina metrópole e natureza selvagem. O PARNASO com a Travessia Petrópolis–Teresópolis é a travessia mais icônica do Brasil.",
    "MG":"Minas Gerais abriga o Pico da Bandeira (2.892m), o Itacolomi e a Serra do Cipó — um paraíso para trekking com mais de 100 trilhas catalogadas.",
    "RS":"O Rio Grande do Sul surpreende com os Cânions Itaimbezinho e Fortaleza, entre os maiores do mundo, e a exuberante Serra Gaúcha.",
    "SC":"Santa Catarina vai do litoral à serra, da Trilha das Praias ao Parque de Aparados da Serra, com percursos para todos os níveis.",
    "GO":"Goiás é o coração do Cerrado. A Chapada dos Veadeiros, Patrimônio Natural da UNESCO, tem cachoeiras e formações rochosas únicas.",
    "RR":"Roraima guarda o Monte Roraima, o tepui mais famoso do mundo — uma das expedições mais épicas da América do Sul.",
    "BA":"A Chapada Diamantina na Bahia tem poços de cor, cachoeiras e grutas que parecem de outro mundo, destino obrigatório para aventureiros.",
    "PR":"O Paraná tem o Pico Paraná, ponto mais alto do sul do Brasil, e a histórica Serra do Mar com percursos deslumbrantes.",
    "ES":"O Espírito Santo tem trilhas no Caparaó, na Costa e na Mata Atlântica preservada do interior.",
    "PE":"Pernambuco oferece trilhas na Serra Negra, Chapada do Araripe e no arquipélago de Fernando de Noronha.",
    "CE":"Ceará tem percursos únicos no Parque Nacional de Ubajara, Chapada do Araripe e no litoral de dunas.",
    "AM":"O Amazonas é a fronteira máxima do ecoturismo — trilhas na floresta amazônica com biodiversidade incomparável.",
    "PA":"O Pará tem a Serra dos Carajás e percursos na Floresta Nacional Tapajós, dos destinos mais selvagens do Brasil.",
    "MT":"Mato Grosso abriga a Chapada dos Guimarães com formações rochosas e cachoeiras no coração do Brasil.",
    "MS":"Mato Grosso do Sul combina o Pantanal com a Serra da Bodoquena, onde grutas e rios de água cristalina encantam.",
}

pages_generated = []

def slugify(text):
    text = str(text).lower()
    for a, b in [("á","a"),("à","a"),("â","a"),("ã","a"),("ä","a"),
                 ("é","e"),("è","e"),("ê","e"),("ë","e"),
                 ("í","i"),("ì","i"),("î","i"),
                 ("ó","o"),("ò","o"),("ô","o"),("õ","o"),("ö","o"),
                 ("ú","u"),("ù","u"),("û","u"),("ü","u"),("ç","c"),("ñ","n")]:
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9\s\-]","",text)
    text = re.sub(r"[\s\-]+"," ",text).strip()
    return text.replace(" ","-")

def write_page(rel_path, html):
    p = BASE_DIR / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    pages_generated.append(str(rel_path))

def diff_badge(d):
    m = DIFFICULTY.get(d, DIFFICULTY["moderate"])
    return f'<span class="badge" style="background:{m["bg"]};color:{m["color"]}">{m["pt"]}</span>'


# ─── Shared HTML Components ───────────────────────────────────────────────────

STYLES = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--g:#16a34a;--gd:#15803d;--tx:#111827;--tm:#6b7280;--bg:#fff;--bgm:#f9fafb;--br:#e5e7eb;--r:8px;--sh:0 1px 3px rgba(0,0,0,.12)}
body{font-family:'Inter',system-ui,sans-serif;color:var(--tx);background:var(--bg);line-height:1.65}
a{color:var(--g);text-decoration:none}a:hover{text-decoration:underline}
img{max-width:100%;height:auto}
.wrap{max-width:1200px;margin:0 auto;padding:0 1rem}
.nav{background:#fff;border-bottom:1px solid var(--br);position:sticky;top:0;z-index:100;box-shadow:var(--sh)}
.nav-in{max-width:1200px;margin:0 auto;padding:0 1rem;display:flex;align-items:center;justify-content:space-between;height:64px}
.nav-logo{display:flex;align-items:center;gap:.5rem;font-weight:700;font-size:1.25rem;color:var(--g)}
.nav-logo img{height:32px;width:auto}
.nav-links{list-style:none;display:flex;gap:2rem}
.nav-links a{color:var(--tx);font-weight:500;font-size:.95rem}
.nav-links a:hover{color:var(--g)}
.hero{position:relative;background:#0f1f0f;color:#fff;min-height:360px}
.hero-img{width:100%;height:420px;object-fit:cover;opacity:.6;display:block}
.hero-over{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:2rem;background:linear-gradient(0deg,rgba(0,0,0,.75) 0%,transparent 60%)}
.hero h1{font-size:2.25rem;font-weight:800;line-height:1.2;margin:.5rem 0}
.hero-sub{font-size:1.05rem;opacity:.88;max-width:680px}
.crumb{font-size:.82rem;color:rgba(255,255,255,.75)}
.crumb a{color:rgba(255,255,255,.75)}
.crumb a:hover{color:#fff}
.stats-bar{background:var(--g);color:#fff;padding:.875rem 0}
.stats-in{max-width:1200px;margin:0 auto;padding:0 1rem;display:flex;flex-wrap:wrap;gap:1.5rem}
.stat{display:flex;flex-direction:column;gap:.15rem}
.stat-l{font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;opacity:.75}
.stat-v{font-size:1rem;font-weight:700}
.grid-2{display:grid;grid-template-columns:1fr 320px;gap:2.5rem;padding:2.5rem 0}
.main h2{font-size:1.4rem;font-weight:700;margin:2rem 0 .875rem;color:var(--tx)}
.main h3{font-size:1.1rem;font-weight:600;margin:1.5rem 0 .5rem}
.main p{margin-bottom:1rem;color:#374151}
.main ul{margin:0 0 1rem 1.25rem;color:#374151}
.main ul li{margin-bottom:.35rem}
.aside{}
.card{background:var(--bgm);border:1px solid var(--br);border-radius:var(--r);padding:1.25rem;margin-bottom:1.25rem}
.card h3{font-size:.95rem;font-weight:700;margin-bottom:.875rem}
.btn{display:block;background:var(--g);color:#fff;text-align:center;padding:.875rem 1rem;border-radius:var(--r);font-weight:700;font-size:.95rem;margin-top:1rem;cursor:pointer;border:none;width:100%}
.btn:hover{background:var(--gd);text-decoration:none;color:#fff}
.btn-out{display:block;background:#fff;color:var(--g);border:2px solid var(--g);text-align:center;padding:.75rem 1rem;border-radius:var(--r);font-weight:700;font-size:.9rem;margin-top:.625rem}
.btn-out:hover{background:var(--bgm);text-decoration:none}
.badge{display:inline-block;padding:.2rem .65rem;border-radius:999px;font-size:.78rem;font-weight:600}
.info-table{width:100%;border-collapse:collapse}
.info-table tr{border-bottom:1px solid var(--br)}
.info-table tr:last-child{border:none}
.info-table td{padding:.55rem .25rem;font-size:.9rem}
.info-table td:first-child{color:var(--tm)}
.info-table td:last-child{font-weight:600;text-align:right}
.tag-row{display:flex;flex-wrap:wrap;gap:.4rem;margin:.625rem 0}
.tag{background:var(--bgm);border:1px solid var(--br);border-radius:999px;padding:.2rem .65rem;font-size:.78rem;color:var(--tm)}
.trail-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:1.25rem;margin:1rem 0}
.tc{border:1px solid var(--br);border-radius:var(--r);overflow:hidden;box-shadow:var(--sh);background:#fff}
.tc:hover{box-shadow:0 4px 12px rgba(0,0,0,.15)}
.tc img{width:100%;height:170px;object-fit:cover;display:block}
.tc-body{padding:.875rem}
.tc-title{font-size:.95rem;font-weight:700;color:var(--tx);margin-bottom:.4rem}
.tc-meta{font-size:.8rem;color:var(--tm);display:flex;flex-wrap:wrap;gap:.625rem}
.tc-link{display:block;margin-top:.625rem;font-size:.82rem;font-weight:600;color:var(--g)}
.faq{}
.faq-item{border-bottom:1px solid var(--br);padding:1rem 0}
.faq-q{font-weight:600;margin-bottom:.4rem}
.faq-a{color:#374151;font-size:.95rem}
.guide-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1rem;margin:1rem 0}
.gc{border:1px solid var(--br);border-radius:var(--r);padding:1rem;background:#fff}
.gc-name{font-weight:700;margin-bottom:.25rem;font-size:.95rem}
.gc-meta{font-size:.82rem;color:var(--tm)}
.gc-badge{display:inline-block;background:#dcfce7;color:#15803d;font-size:.72rem;font-weight:700;padding:.15rem .5rem;border-radius:4px;margin-top:.5rem}
.section-header{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:1rem}
.section-header h2{margin:0}
.see-all{font-size:.85rem;font-weight:600;color:var(--g)}
.hero-badges{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:.75rem}
.state-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.75rem;margin:1rem 0}
.state-card{border:1px solid var(--br);border-radius:var(--r);padding:.875rem;text-align:center;background:#fff}
.state-card a{color:var(--tx);font-weight:600;font-size:.9rem}
.state-card .count{font-size:.8rem;color:var(--tm);display:block;margin-top:.2rem}
.intro-box{background:var(--bgm);border-left:4px solid var(--g);padding:1rem 1.25rem;border-radius:0 var(--r) var(--r) 0;margin-bottom:1.5rem}
footer{background:#0f172a;color:#94a3b8;padding:3rem 0 1.5rem;margin-top:4rem}
.foot-in{max-width:1200px;margin:0 auto;padding:0 1rem;display:grid;grid-template-columns:1fr 2fr;gap:3rem;margin-bottom:2rem}
.foot-brand p{margin-top:.75rem;font-size:.875rem}
.foot-links{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem}
.foot-links h4{color:#fff;font-size:.875rem;margin-bottom:.75rem}
.foot-links ul{list-style:none}
.foot-links ul li{margin-bottom:.35rem}
.foot-links a{color:#94a3b8;font-size:.82rem}
.foot-links a:hover{color:#fff}
.foot-bot{max-width:1200px;margin:0 auto;padding:1rem;border-top:1px solid #1e293b;font-size:.78rem;color:#64748b}
@media(max-width:768px){
  .hero h1{font-size:1.6rem}
  .grid-2{grid-template-columns:1fr}
  .aside{order:-1}
  .nav-links{display:none}
  .foot-in{grid-template-columns:1fr}
  .foot-links{grid-template-columns:1fr 1fr}
}
"""

def nav():
    return """<nav class="nav"><div class="nav-in">
  <a href="/" class="nav-logo"><img src="/LOGOTREKKO2.png" alt="Trekko">Trekko</a>
  <ul class="nav-links">
    <li><a href="/trilhas">Trilhas</a></li>
    <li><a href="/guias">Guias</a></li>
    <li><a href="/blog">Blog</a></li>
  </ul>
</div></nav>"""

def footer():
    return """<footer><div class="foot-in">
  <div class="foot-brand">
    <img src="/LOGOTREKKO2.png" alt="Trekko" style="height:28px">
    <p>A maior plataforma de descoberta de trilhas e trekking do Brasil.</p>
  </div>
  <div class="foot-links">
    <div><h4>Explorar</h4><ul>
      <li><a href="/trilhas">Todas as trilhas</a></li>
      <li><a href="/trilhas/dificuldade/easy">Trilhas fáceis</a></li>
      <li><a href="/trilhas/dificuldade/hard">Trilhas difíceis</a></li>
      <li><a href="/guias">Guias certificados</a></li>
    </ul></div>
    <div><h4>Estados</h4><ul>
      <li><a href="/trilhas/estado/sp">São Paulo</a></li>
      <li><a href="/trilhas/estado/rj">Rio de Janeiro</a></li>
      <li><a href="/trilhas/estado/mg">Minas Gerais</a></li>
      <li><a href="/trilhas/estado/rs">Rio Grande do Sul</a></li>
    </ul></div>
    <div><h4>Trekko</h4><ul>
      <li><a href="/sobre">Sobre</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/contato">Contato</a></li>
      <li><a href="/privacidade">Privacidade</a></li>
    </ul></div>
  </div>
</div><div class="foot-bot"><p>© 2025 Trekko. Todos os direitos reservados.</p></div></footer>"""

def base_html(title, desc, canonical, og_image, body, schema_ld=None, extra_head=""):
    schema_block = f'<script type="application/ld+json">{json.dumps(schema_ld, ensure_ascii=False, indent=None)}</script>' if schema_ld else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{BASE_URL}{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{BASE_URL}{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="icon" href="/favicon-48x48.png" type="image/png">
{schema_block}
{extra_head}
<style>{STYLES}</style>
</head>
<body>
{nav()}
{body}
{footer()}
</body>
</html>"""

def trail_cards(trail_list, heading=None):
    if not trail_list:
        return ""
    cards = ""
    for t in trail_list[:9]:
        d = DIFFICULTY.get(t["difficulty"], DIFFICULTY["moderate"])
        dist = t.get("distanceKm","?")
        cards += f"""<div class="tc">
  <a href="/trilha/{t['slug']}"><img src="{BASE_URL}{t['imageUrl']}" alt="Trilha {t['name']} - {t['city']}, {STATE_NAMES.get(t['uf'],t['uf'])}" loading="lazy" width="540" height="340"></a>
  <div class="tc-body">
    <div class="tc-title">{t['name']}</div>
    <div class="tc-meta">
      <span>{t['city']}, {t['uf']}</span>
      <span>{dist} km</span>
      {diff_badge(t['difficulty'])}
    </div>
    <a href="/trilha/{t['slug']}" class="tc-link">Ver trilha →</a>
  </div>
</div>"""
    h = f"<h2>{heading}</h2>" if heading else ""
    return f"{h}<div class='trail-grid'>{cards}</div>"


# ─── Trail Detail Pages ────────────────────────────────────────────────────────

def gen_trail_pages(trails):
    print("Generating trail pages...")
    for t in trails:
        slug = t["slug"]
        state_name = STATE_NAMES.get(t["uf"], t["uf"])
        d = DIFFICULTY.get(t["difficulty"], DIFFICULTY["moderate"])
        dist = t.get("distanceKm","?")
        elev = t.get("elevationGain","?")
        alt  = t.get("maxAltitude","?")
        time_ = t.get("estimatedTime","?")
        fee  = t.get("entranceFee","Consultar")
        park = t.get("park","")
        region = t.get("region","")
        season = t.get("bestSeason","Consultar")
        guide_req = "Sim" if t.get("guideRequired") else "Não"
        trail_type_map = {"linear":"Linear","circular":"Circular","traverse":"Travessia","loop":"Loop"}
        trail_type = trail_type_map.get(t.get("trailType","linear"), t.get("trailType","Linear"))
        highlights = t.get("highlights",[])
        water = t.get("waterPoints",[])
        camping = t.get("campingPoints",[])
        images = t.get("images",[t["imageUrl"]])

        title = f"{t['name']} - Trilha em {t['city']}, {state_name} | Trekko"
        desc  = (t.get("shortDescription","") or t.get("description",""))[:158]

        # Schema.org
        schema = {
            "@context":"https://schema.org",
            "@type":"TouristAttraction",
            "name": t["name"],
            "description": t.get("description",""),
            "url": f"{BASE_URL}/trilha/{slug}",
            "image": [f"{BASE_URL}{img}" for img in images[:4]],
            "address": {
                "@type":"PostalAddress",
                "addressLocality": t["city"],
                "addressRegion": t["uf"],
                "addressCountry":"BR"
            },
            "containedInPlace": {"@type":"Park","name": park} if park else None,
        }
        schema = {k:v for k,v in schema.items() if v}

        # Breadcrumb schema
        breadcrumb_schema = {
            "@context":"https://schema.org",
            "@type":"BreadcrumbList",
            "itemListElement":[
                {"@type":"ListItem","position":1,"name":"Home","item":BASE_URL+"/"},
                {"@type":"ListItem","position":2,"name":"Trilhas","item":BASE_URL+"/trilhas"},
                {"@type":"ListItem","position":3,"name":state_name,"item":f"{BASE_URL}/trilhas/estado/{t['uf'].lower()}"},
                {"@type":"ListItem","position":4,"name":t["name"],"item":f"{BASE_URL}/trilha/{slug}"}
            ]
        }

        # FAQ
        faqs = [
            {"q": f"É necessário guia para fazer a trilha {t['name']}?",
             "a": f"{'Sim, guia é obrigatório para a ' + t['name'] + '. Contrate um guia certificado CADASTUR para maior segurança.' if t.get('guideRequired') else 'Não é obrigatório guia para ' + t['name'] + ', mas recomendamos contratar um guia local certificado para a primeira visita.'}"},
            {"q": f"Qual a melhor época para fazer a trilha {t['name']}?",
             "a": f"A melhor época para visitar é {season}. Evite períodos de chuva intensa que podem tornar os acessos perigosos."},
            {"q": f"Qual a distância e tempo da trilha {t['name']}?",
             "a": f"A trilha tem {dist} km e o tempo estimado de conclusão é {time_}. O tempo pode variar conforme ritmo, condições climáticas e paradas para descanso."},
            {"q": f"Qual é o valor da entrada para {park or t['name']}?",
             "a": f"A taxa de entrada é {fee}. Verifique junto ao parque se há descontos para estudantes ou moradores locais."},
            {"q": f"Qual o nível de dificuldade da trilha {t['name']}?",
             "a": f"A trilha é classificada como {d['pt']}. {d['desc']}"},
        ]
        if water:
            faqs.append({"q":"Há pontos de água potável na trilha?",
                         "a": f"Sim. Os pontos de água são: {', '.join(water)}. Leve sempre água extra e purificador por segurança."})

        faq_html = "".join(f'<div class="faq-item"><div class="faq-q">{f["q"]}</div><div class="faq-a">{f["a"]}</div></div>' for f in faqs)
        faq_schema = {
            "@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":f["q"],"acceptedAnswer":{"@type":"Answer","text":f["a"]}} for f in faqs]
        }

        highlights_html = "".join(f"<li>{h}</li>" for h in highlights)
        water_html = "".join(f"<li>{w}</li>" for w in water) if water else "<li>Leve água suficiente</li>"
        camping_html = "".join(f"<li>{c}</li>" for c in camping) if camping else "<li>Sem acampamento na trilha</li>"
        gear_html = "".join(f"<li>{g}</li>" for g in GEAR.get(t["difficulty"], GEAR["moderate"]))

        # Gallery
        gallery_imgs = "".join(f'<img src="{BASE_URL}{img}" alt="{t["name"]} - foto {i+1}" loading="lazy" style="width:100%;height:180px;object-fit:cover;border-radius:var(--r)">' for i,img in enumerate(images[:4]))

        extra_schema = f'<script type="application/ld+json">{json.dumps(breadcrumb_schema,ensure_ascii=False)}</script>\n<script type="application/ld+json">{json.dumps(faq_schema,ensure_ascii=False)}</script>'

        body = f"""
<div class="hero">
  <img class="hero-img" src="{BASE_URL}{t['imageUrl']}" alt="Trilha {t['name']} em {t['city']}, {state_name}" width="1200" height="420">
  <div class="hero-over">
    <nav class="crumb" aria-label="breadcrumb">
      <a href="/">Home</a> › <a href="/trilhas">Trilhas</a> › <a href="/trilhas/estado/{t['uf'].lower()}">{state_name}</a> › {t['name']}
    </nav>
    <div class="hero-badges">
      {diff_badge(t['difficulty'])}
      <span class="badge" style="background:rgba(255,255,255,.2);color:#fff">{trail_type}</span>
      {'<span class="badge" style="background:#dc2626;color:#fff">Guia obrigatório</span>' if t.get("guideRequired") else ""}
    </div>
    <h1>{t['name']}</h1>
    <p class="hero-sub">{t.get('shortDescription','')}</p>
  </div>
</div>

<div class="stats-bar">
  <div class="stats-in">
    <div class="stat"><span class="stat-l">Distância</span><span class="stat-v">{dist} km</span></div>
    <div class="stat"><span class="stat-l">Desnível</span><span class="stat-v">{elev} m</span></div>
    <div class="stat"><span class="stat-l">Altitude máx.</span><span class="stat-v">{alt} m</span></div>
    <div class="stat"><span class="stat-l">Duração</span><span class="stat-v">{time_}</span></div>
    <div class="stat"><span class="stat-l">Dificuldade</span><span class="stat-v">{d['pt']}</span></div>
    <div class="stat"><span class="stat-l">Entrada</span><span class="stat-v">{fee}</span></div>
  </div>
</div>

<div class="wrap">
<div class="grid-2">
<div class="main">

<div class="intro-box"><p>{t.get('hookText','')}</p></div>

<h2>Sobre a Trilha</h2>
<p>{t.get('description','')}</p>

<h2>Destaques</h2>
<ul>{highlights_html}</ul>

<h2>Detalhes da Trilha</h2>
<table class="info-table">
  <tr><td>Tipo</td><td>{trail_type}</td></tr>
  <tr><td>Distância</td><td>{dist} km</td></tr>
  <tr><td>Desnível positivo</td><td>{elev} m</td></tr>
  <tr><td>Altitude máxima</td><td>{alt} m</td></tr>
  <tr><td>Duração estimada</td><td>{time_}</td></tr>
  <tr><td>Dificuldade</td><td>{d['pt']}</td></tr>
  <tr><td>Guia obrigatório</td><td>{guide_req}</td></tr>
  <tr><td>Taxa de entrada</td><td>{fee}</td></tr>
  <tr><td>Melhor época</td><td>{season}</td></tr>
  <tr><td>Parque / Área</td><td>{park}</td></tr>
  <tr><td>Região</td><td>{region}</td></tr>
</table>

<h2>Pontos de Água</h2>
<ul>{water_html}</ul>

<h2>Pontos de Camping</h2>
<ul>{camping_html}</ul>

<h2>Galeria de Fotos</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:.625rem;margin:1rem 0">{gallery_imgs}</div>

<h2>Como Chegar</h2>
<p>A trilha {t['name']} está localizada em <strong>{t['city']}</strong>, {state_name}, dentro do {park or 'parque / área natural da região'}. A cidade mais próxima é {t['city']}. Recomendamos verificar o acesso via GPS ou com o guia local antes da saída.</p>
<p>Coordenadas gerais: {t['city']}, {state_name}, Brasil. Use o aplicativo do Trekko para o mapa offline completo.</p>

<h2>Melhor Época para Visitar</h2>
<p>A melhor época para realizar a trilha {t['name']} é <strong>{season}</strong>. Fora desse período podem ocorrer condições climáticas adversas, como chuvas fortes, que aumentam o risco de acidentes e dificultam o acesso.</p>

<h2>Dicas de Segurança</h2>
<ul>
  <li>Avise alguém de confiança sobre seu roteiro e horário previsto de retorno</li>
  <li>Verifique a previsão do tempo antes de sair — nunca trilhe em caso de tempestade</li>
  {'<li>Contrate um guia certificado CADASTUR obrigatoriamente</li>' if t.get('guideRequired') else '<li>Considere contratar um guia local para sua primeira visita</li>'}
  <li>Leve mais água do que você acha que vai precisar</li>
  <li>Não trilhe sozinho — pelo menos duas pessoas ou em grupo</li>
  <li>Carregue kit básico de primeiros socorros</li>
  <li>Respeite a sinalização e não abandone o percurso marcado</li>
</ul>

<h2>Equipamentos Recomendados</h2>
<ul>{gear_html}</ul>

<h2>Perguntas Frequentes</h2>
<div class="faq">{faq_html}</div>

</div><!-- .main -->

<aside class="aside">
  <div class="card">
    <h3>Planeje sua Trilha</h3>
    <table class="info-table">
      <tr><td>Distância</td><td>{dist} km</td></tr>
      <tr><td>Duração</td><td>{time_}</td></tr>
      <tr><td>Dificuldade</td><td>{diff_badge(t['difficulty'])}</td></tr>
      <tr><td>Entrada</td><td>{fee}</td></tr>
    </table>
    <a href="/trilhas" class="btn">Ver no app Trekko</a>
    <a href="/guias" class="btn-out">Encontrar guia certificado</a>
  </div>
  <div class="card">
    <h3>Localização</h3>
    <p style="font-size:.875rem;color:var(--tm)">{t['city']}, {state_name}<br>{park}</p>
    <a href="/trilhas/estado/{t['uf'].lower()}" class="btn-out">Mais trilhas em {state_name}</a>
  </div>
  <div class="card">
    <h3>Melhor Época</h3>
    <p style="font-size:.875rem;color:var(--tm)">{season}</p>
  </div>
</aside>
</div><!-- .grid-2 -->
</div><!-- .wrap -->"""

        html = base_html(title, desc, f"/trilha/{slug}/", f"{BASE_URL}{t['imageUrl']}", body,
                         schema_ld=schema, extra_head=extra_schema)
        write_page(f"trilha/{slug}/index.html", html)
    print(f"  ✓ {len(trails)} trail pages")


# ─── Geographic Pages ──────────────────────────────────────────────────────────

def gen_state_pages(trails):
    print("Generating state pages...")
    by_state = defaultdict(list)
    for t in trails:
        by_state[t["uf"]].append(t)
    for uf, t_list in by_state.items():
        state = STATE_NAMES.get(uf, uf)
        uf_l = uf.lower()
        n = len(t_list)
        desc_extra = STATE_DESC.get(uf, f"Descubra trilhas e trekking em {state}.")
        title = f"Trilhas em {state} - Melhores Trilhas e Trekking | Trekko"
        desc  = f"Descubra as melhores trilhas em {state}. {n} trilha{'s' if n>1 else ''} com mapas, dificuldade, distância e guias certificados CADASTUR."[:158]
        canonical = f"/trilhas/estado/{uf_l}/"

        parks_in_state = list({t.get("park","") for t in t_list if t.get("park")})
        regions_in_state = list({t.get("region","") for t in t_list if t.get("region")})

        parks_links = " · ".join(f'<a href="/trilhas/parque/{slugify(p)}">{p}</a>' for p in parks_in_state[:6])
        regions_links = " · ".join(f'<a href="/trilhas/regiao/{slugify(r)}">{r}</a>' for r in regions_in_state[:6])

        diff_counts = defaultdict(int)
        for t in t_list:
            diff_counts[t["difficulty"]] += 1
        diff_filter = " ".join(f'<a href="/trilhas/dificuldade/{k}" class="badge" style="background:{DIFFICULTY[k]["bg"]};color:{DIFFICULTY[k]["color"]}">{DIFFICULTY[k]["pt"]} ({v})</a>' for k,v in diff_counts.items())

        schema = {
            "@context":"https://schema.org","@type":"ItemList",
            "name": f"Trilhas em {state}",
            "description": desc,
            "url": f"{BASE_URL}{canonical}",
            "numberOfItems": n,
            "itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE_URL}/trilha/{t['slug']}","name":t["name"]} for i,t in enumerate(t_list)]
        }

        body = f"""
<div class="hero" style="min-height:260px">
  <img class="hero-img" src="{BASE_URL}{t_list[0]['imageUrl']}" alt="Trilhas em {state}" width="1200" height="420" style="height:300px">
  <div class="hero-over">
    <nav class="crumb"><a href="/">Home</a> › <a href="/trilhas">Trilhas</a> › {state}</nav>
    <h1>Trilhas em {state}</h1>
    <p class="hero-sub">{n} trilha{'s' if n>1 else ''} catalogada{'s' if n>1 else ''} com mapas, fotos e guias certificados</p>
  </div>
</div>
<div class="wrap" style="padding-top:2rem">
  <div class="intro-box"><p>{desc_extra}</p></div>
  <p style="margin-bottom:1rem"><strong>Filtrar por dificuldade:</strong> {diff_filter}</p>
  {f'<p style="margin-bottom:.5rem"><strong>Parques:</strong> {parks_links}</p>' if parks_links else ""}
  {f'<p style="margin-bottom:1.5rem"><strong>Regiões:</strong> {regions_links}</p>' if regions_links else ""}
  {trail_cards(t_list)}
  <div style="margin-top:2.5rem;padding:1.5rem;background:var(--bgm);border-radius:var(--r)">
    <h2 style="margin-bottom:.75rem">Guias Certificados em {state}</h2>
    <p style="color:var(--tm);margin-bottom:1rem">Encontre guias de trilha certificados pelo Ministério do Turismo (CADASTUR) em {state} para sua próxima aventura.</p>
    <a href="/guias/{uf_l}" class="btn" style="display:inline-block;width:auto;padding:.75rem 1.5rem">Ver guias em {state}</a>
  </div>
</div>"""

        write_page(f"trilhas/estado/{uf_l}/index.html",
                   base_html(title, desc, canonical, f"{BASE_URL}{t_list[0]['imageUrl']}", body, schema_ld=schema))
    print(f"  ✓ {len(by_state)} state pages")


def gen_difficulty_pages(trails):
    print("Generating difficulty pages...")
    for level, meta in DIFFICULTY.items():
        t_list = [t for t in trails if t["difficulty"] == level]
        title = f"Trilhas {meta['pt']}s no Brasil - Trekking {meta['pt']} | Trekko"
        desc  = f"{meta['desc']} {len(t_list)} trilha{'s' if len(t_list)!=1 else ''} {meta['pt'].lower()}{'s' if len(t_list)!=1 else ''} catalogada{'s' if len(t_list)!=1 else ''} no Trekko."[:158]
        canonical = f"/trilhas/dificuldade/{level}/"
        gear_items = "".join(f"<li>{g}</li>" for g in GEAR[level])

        schema = {
            "@context":"https://schema.org","@type":"ItemList",
            "name": f"Trilhas {meta['pt']}s",
            "description": desc,
            "url": f"{BASE_URL}{canonical}",
            "itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE_URL}/trilha/{t['slug']}","name":t["name"]} for i,t in enumerate(t_list)]
        }

        hero_img = t_list[0]["imageUrl"] if t_list else "/android-chrome-512x512.png"
        body = f"""
<div class="hero" style="min-height:240px">
  <img class="hero-img" src="{BASE_URL}{hero_img}" alt="Trilhas {meta['pt']}s" width="1200" height="300" style="height:280px">
  <div class="hero-over">
    <nav class="crumb"><a href="/">Home</a> › <a href="/trilhas">Trilhas</a> › Dificuldade {meta['pt']}</nav>
    <h1>Trilhas {meta['pt']}s</h1>
    <p class="hero-sub">{meta['desc']}</p>
  </div>
</div>
<div class="wrap" style="padding-top:2rem">
  <div class="intro-box">
    <h2 style="margin-bottom:.5rem">O que esperar de uma trilha {meta['pt'].lower()}?</h2>
    <table class="info-table" style="margin-top:.5rem">
      <tr><td>Distância típica</td><td>{meta['distance']}</td></tr>
      <tr><td>Tempo médio</td><td>{meta['time']}</td></tr>
      <tr><td>Desnível</td><td>{meta['elevation']}</td></tr>
      <tr><td>Condicionamento</td><td>{meta['fitness']}</td></tr>
    </table>
  </div>
  <h2>Equipamentos Recomendados</h2>
  <ul style="margin-bottom:1.5rem">{gear_items}</ul>
  {trail_cards(t_list, f"Trilhas {meta['pt']}s Catalogadas ({len(t_list)})" if t_list else "")}
  {'<p style="color:var(--tm);margin-top:1rem">Mais trilhas sendo adicionadas em breve.</p>' if not t_list else ""}
</div>"""

        write_page(f"trilhas/dificuldade/{level}/index.html",
                   base_html(title, desc, canonical, f"{BASE_URL}{hero_img}", body, schema_ld=schema))
    print(f"  ✓ 4 difficulty pages")


def gen_park_pages(trails):
    print("Generating park pages...")
    by_park = defaultdict(list)
    for t in trails:
        if t.get("park"):
            by_park[t["park"]].append(t)
    for park, t_list in by_park.items():
        park_slug = slugify(park)
        state_name = STATE_NAMES.get(t_list[0]["uf"], t_list[0]["uf"])
        title = f"Trilhas no {park} - Guia Completo de Trekking | Trekko"
        desc  = f"Guia completo das trilhas no {park}, {state_name}. {len(t_list)} trilha{'s' if len(t_list)!=1 else ''} com dificuldade, distância, mapas e guias certificados."[:158]
        canonical = f"/trilhas/parque/{park_slug}/"
        schema = {
            "@context":"https://schema.org","@type":"Park",
            "name": park,
            "url": f"{BASE_URL}{canonical}",
            "containsPlace":[{"@type":"TouristAttraction","name":t["name"],"url":f"{BASE_URL}/trilha/{t['slug']}"} for t in t_list]
        }
        body = f"""
<div class="hero" style="min-height:240px">
  <img class="hero-img" src="{BASE_URL}{t_list[0]['imageUrl']}" alt="Trilhas no {park}" width="1200" height="300" style="height:280px">
  <div class="hero-over">
    <nav class="crumb"><a href="/">Home</a> › <a href="/trilhas">Trilhas</a> › <a href="/trilhas/estado/{t_list[0]['uf'].lower()}">{state_name}</a> › {park}</nav>
    <h1>Trilhas no {park}</h1>
    <p class="hero-sub">{len(t_list)} trilha{'s' if len(t_list)!=1 else ''} catalogada{'s' if len(t_list)!=1 else ''} em {state_name}</p>
  </div>
</div>
<div class="wrap" style="padding-top:2rem">
  <div class="intro-box"><p>O <strong>{park}</strong> está localizado em {state_name} e é um dos principais destinos de ecoturismo da região. Explore as trilhas abaixo com mapas, fotos e informações completas.</p></div>
  {trail_cards(t_list)}
  <p style="margin-top:1.5rem"><a href="/trilhas/estado/{t_list[0]['uf'].lower()}">← Ver todas as trilhas em {state_name}</a></p>
</div>"""
        write_page(f"trilhas/parque/{park_slug}/index.html",
                   base_html(title, desc, canonical, f"{BASE_URL}{t_list[0]['imageUrl']}", body, schema_ld=schema))
    print(f"  ✓ {len(by_park)} park pages")


def gen_region_pages(trails):
    print("Generating region pages...")
    by_region = defaultdict(list)
    for t in trails:
        if t.get("region"):
            by_region[t["region"]].append(t)
    for region, t_list in by_region.items():
        region_slug = slugify(region)
        state_name = STATE_NAMES.get(t_list[0]["uf"], t_list[0]["uf"])
        title = f"Trilhas na {region} - Trekking e Ecoturismo | Trekko"
        desc  = f"As melhores trilhas na {region}. {len(t_list)} trilha{'s' if len(t_list)!=1 else ''} com mapas detalhados, dificuldade, distância e guias certificados."[:158]
        canonical = f"/trilhas/regiao/{region_slug}/"
        schema = {
            "@context":"https://schema.org","@type":"ItemList",
            "name": f"Trilhas na {region}",
            "url": f"{BASE_URL}{canonical}",
            "itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE_URL}/trilha/{t['slug']}","name":t["name"]} for i,t in enumerate(t_list)]
        }
        body = f"""
<div class="hero" style="min-height:240px">
  <img class="hero-img" src="{BASE_URL}{t_list[0]['imageUrl']}" alt="Trilhas na {region}" width="1200" height="300" style="height:280px">
  <div class="hero-over">
    <nav class="crumb"><a href="/">Home</a> › <a href="/trilhas">Trilhas</a> › {region}</nav>
    <h1>Trilhas na {region}</h1>
    <p class="hero-sub">Explore as melhores trilhas e destinos de trekking na {region}</p>
  </div>
</div>
<div class="wrap" style="padding-top:2rem">
  <div class="intro-box"><p>A <strong>{region}</strong> é uma das regiões mais procuradas pelos amantes de trekking e ecoturismo no Brasil. Confira abaixo as trilhas catalogadas pelo Trekko com informações completas.</p></div>
  {trail_cards(t_list)}
</div>"""
        write_page(f"trilhas/regiao/{region_slug}/index.html",
                   base_html(title, desc, canonical, f"{BASE_URL}{t_list[0]['imageUrl']}", body, schema_ld=schema))
    print(f"  ✓ {len(by_region)} region pages")


def gen_city_pages(trails):
    print("Generating near-city pages...")
    by_city = defaultdict(list)
    for t in trails:
        if t.get("city"):
            cities = [c.strip() for c in t["city"].split("/")]
            for c in cities:
                by_city[c].append(t)
    count = 0
    for city, t_list in by_city.items():
        city_slug = slugify(city)
        state_name = STATE_NAMES.get(t_list[0]["uf"], t_list[0]["uf"])
        title = f"Trilhas Perto de {city} - Hiking e Trekking | Trekko"
        desc  = f"As melhores trilhas e caminhadas perto de {city}, {state_name}. {len(t_list)} opção{'ões' if len(t_list)!=1 else ''} com mapas, dificuldade e guias certificados."[:158]
        canonical = f"/perto-de/{city_slug}/"
        schema = {
            "@context":"https://schema.org","@type":"ItemList",
            "name": f"Trilhas perto de {city}",
            "url": f"{BASE_URL}{canonical}",
            "itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE_URL}/trilha/{t['slug']}","name":t["name"]} for i,t in enumerate(t_list)]
        }
        body = f"""
<div class="hero" style="min-height:240px">
  <img class="hero-img" src="{BASE_URL}{t_list[0]['imageUrl']}" alt="Trilhas perto de {city}" width="1200" height="300" style="height:280px">
  <div class="hero-over">
    <nav class="crumb"><a href="/">Home</a> › <a href="/trilhas">Trilhas</a> › Perto de {city}</nav>
    <h1>Trilhas Perto de {city}</h1>
    <p class="hero-sub">Hiking e trekking próximos a {city}, {state_name}</p>
  </div>
</div>
<div class="wrap" style="padding-top:2rem">
  <div class="intro-box"><p>Encontre as melhores trilhas de caminhada e trekking perto de <strong>{city}</strong>. Abaixo listamos todas as opções catalogadas pelo Trekko na região, com informações completas de distância, dificuldade e como chegar.</p></div>
  {trail_cards(t_list)}
  <p style="margin-top:1.5rem"><a href="/guias/{t_list[0]['uf'].lower()}">Encontrar guia de trilha em {state_name} →</a></p>
</div>"""
        write_page(f"perto-de/{city_slug}/index.html",
                   base_html(title, desc, canonical, f"{BASE_URL}{t_list[0]['imageUrl']}", body, schema_ld=schema))
        count += 1
    print(f"  ✓ {count} near-city pages")


# ─── Guide Discovery Pages ─────────────────────────────────────────────────────

def guide_card(g):
    cats = ", ".join(g.get("categories",[]))
    phone = g.get("phone","")
    valid = g.get("validUntil","")
    return f"""<div class="gc">
  <div class="gc-name">{g['name'].title()}</div>
  <div class="gc-meta">{g['city']}, {g['uf']}</div>
  <div class="gc-meta" style="margin-top:.25rem">{cats}</div>
  {'<div class="gc-meta" style="margin-top:.25rem">📞 ' + phone + '</div>' if phone else ''}
  <span class="gc-badge">CADASTUR Verificado</span>
</div>"""

def gen_guide_state_pages(guides, trails):
    print("Generating guide state pages...")
    by_state = defaultdict(list)
    for g in guides:
        by_state[g["uf"]].append(g)
    trails_by_state = defaultdict(list)
    for t in trails:
        trails_by_state[t["uf"]].append(t)

    count = 0
    for uf, g_list in by_state.items():
        state = STATE_NAMES.get(uf, uf)
        uf_l = uf.lower()
        n = len(g_list)
        title = f"Guias de Trilha em {state} - Certificados CADASTUR | Trekko"
        desc  = f"Encontre guias de trilha certificados pelo Ministério do Turismo (CADASTUR) em {state}. {n} guia{'s' if n!=1 else ''} disponível{'eis' if n!=1 else ''} para caminhadas e trekking."[:158]
        canonical = f"/guias/{uf_l}/"

        # Cities in this state
        cities_count = defaultdict(int)
        for g in g_list:
            if g.get("city"):
                cities_count[g["city"]] += 1
        top_cities = sorted(cities_count.items(), key=lambda x: -x[1])[:12]
        city_links = " · ".join(f'<a href="/guias/{uf_l}/{slugify(c)}">{c} ({cnt})</a>' for c,cnt in top_cities)

        sample_guides = g_list[:12]
        cards_html = "".join(guide_card(g) for g in sample_guides)

        state_trails = trails_by_state.get(uf, [])
        trail_section = trail_cards(state_trails, f"Trilhas em {state}") if state_trails else ""

        schema = {
            "@context":"https://schema.org","@type":"ItemList",
            "name": f"Guias de Trilha em {state}",
            "url": f"{BASE_URL}{canonical}",
            "numberOfItems": n,
            "itemListElement":[{"@type":"ListItem","position":i+1,"name":g["name"].title(),"description":g.get("city","")} for i,g in enumerate(sample_guides)]
        }

        body = f"""
<div class="hero" style="min-height:220px;background:var(--g)">
  <div class="hero-over" style="position:relative;padding:3rem 0;background:none">
    <div class="wrap">
      <nav class="crumb"><a href="/">Home</a> › <a href="/guias">Guias</a> › {state}</nav>
      <h1 style="margin-top:.5rem">Guias de Trilha em {state}</h1>
      <p class="hero-sub">{n:,} guia{'s' if n!=1 else ''} certificado{'s' if n!=1 else ''} pelo Ministério do Turismo (CADASTUR)</p>
    </div>
  </div>
</div>
<div class="wrap" style="padding-top:2rem">
  <div class="intro-box">
    <p>Todos os guias listados aqui são registrados no <strong>CADASTUR</strong> (Cadastro de Prestadores de Serviços de Turismo) do Ministério do Turismo do Brasil, garantindo profissionalismo e segurança para sua aventura em {state}.</p>
  </div>

  <h2>Cidades com Guias em {state}</h2>
  <p style="margin-bottom:1.5rem;color:var(--tm)">{city_links}</p>

  <div class="section-header">
    <h2>Guias Certificados em {state}</h2>
    <span style="color:var(--tm);font-size:.875rem">{n:,} no total</span>
  </div>
  <div class="guide-grid">{cards_html}</div>
  {'<p style="color:var(--tm);margin-top:.5rem;font-size:.875rem">Mostrando 12 de ' + f'{n:,}' + ' guias. Use o app Trekko para ver todos.</p>' if n > 12 else ''}

  <div style="margin-top:1.5rem">
    <a href="/guias" class="btn" style="display:inline-block;width:auto;padding:.75rem 1.5rem">Ver todos os guias no app</a>
  </div>

  {trail_section}
</div>"""

        write_page(f"guias/{uf_l}/index.html",
                   base_html(title, desc, canonical, f"{BASE_URL}/android-chrome-512x512.png", body, schema_ld=schema))
        count += 1
    print(f"  ✓ {count} guide state pages")
    return by_state


def gen_guide_city_pages(guides, min_guides=5):
    print("Generating guide city pages...")
    by_state_city = defaultdict(lambda: defaultdict(list))
    for g in guides:
        if g.get("uf") and g.get("city"):
            by_state_city[g["uf"]][g["city"]].append(g)

    count = 0
    for uf, cities in by_state_city.items():
        state = STATE_NAMES.get(uf, uf)
        uf_l = uf.lower()
        for city, g_list in cities.items():
            if len(g_list) < min_guides:
                continue
            city_slug = slugify(city)
            n = len(g_list)
            title = f"Guias de Trilha em {city}, {state} - CADASTUR | Trekko"
            desc  = f"{n} guia{'s' if n!=1 else ''} de trilha certificado{'s' if n!=1 else ''} em {city}, {state}. Profissionais CADASTUR para caminhadas, trekking e ecoturismo."[:158]
            canonical = f"/guias/{uf_l}/{city_slug}/"

            cards_html = "".join(guide_card(g) for g in g_list[:20])
            schema = {
                "@context":"https://schema.org","@type":"ItemList",
                "name": f"Guias de Trilha em {city}",
                "url": f"{BASE_URL}{canonical}",
                "numberOfItems": n,
            }
            body = f"""
<div class="hero" style="min-height:180px;background:var(--g)">
  <div class="hero-over" style="position:relative;padding:2.5rem 0;background:none">
    <div class="wrap">
      <nav class="crumb"><a href="/">Home</a> › <a href="/guias">Guias</a> › <a href="/guias/{uf_l}">{state}</a> › {city}</nav>
      <h1 style="margin-top:.5rem">Guias de Trilha em {city}</h1>
      <p class="hero-sub">{n} guia{'s' if n!=1 else ''} certificado{'s' if n!=1 else ''} CADASTUR em {city}, {state}</p>
    </div>
  </div>
</div>
<div class="wrap" style="padding-top:2rem">
  <div class="intro-box"><p>Contrate um guia de trilha certificado em <strong>{city}</strong> para uma experiência segura e inesquecível. Todos os profissionais abaixo são registrados no CADASTUR.</p></div>
  <div class="guide-grid">{cards_html}</div>
  {'<p style="color:var(--tm);font-size:.875rem;margin-top:.5rem">Mostrando ' + str(min(20,n)) + ' de ' + str(n) + ' guias.</p>' if n > 20 else ''}
  <p style="margin-top:1.5rem"><a href="/guias/{uf_l}">← Ver todos os guias em {state}</a></p>
</div>"""
            write_page(f"guias/{uf_l}/{city_slug}/index.html",
                       base_html(title, desc, canonical, f"{BASE_URL}/android-chrome-512x512.png", body, schema_ld=schema))
            count += 1
    print(f"  ✓ {count} guide city pages (cities with {min_guides}+ guides)")


# ─── Sitemap ────────────────────────────────────────────────────────────────────

def gen_sitemap(trails):
    print("Generating sitemap.xml...")
    entries = []

    def add(url, priority, freq):
        entries.append(f"""  <url>
    <loc>{BASE_URL}{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{freq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    # Static pages
    add("/", "1.0", "daily")
    add("/trilhas", "0.9", "daily")
    add("/guias", "0.9", "daily")
    add("/blog", "0.8", "weekly")

    # Trail pages
    for t in trails:
        add(f"/trilha/{t['slug']}/", "0.9", "weekly")

    # State pages
    for url in [p for p in pages_generated if p.startswith("trilhas/estado/")]:
        uf = url.split("/")[2]
        add(f"/trilhas/estado/{uf}/", "0.8", "monthly")

    # Difficulty pages
    for level in DIFFICULTY:
        add(f"/trilhas/dificuldade/{level}/", "0.8", "monthly")

    # Park pages
    for url in [p for p in pages_generated if p.startswith("trilhas/parque/")]:
        slug = url.split("/")[2]
        add(f"/trilhas/parque/{slug}/", "0.7", "monthly")

    # Region pages
    for url in [p for p in pages_generated if p.startswith("trilhas/regiao/")]:
        slug = url.split("/")[2]
        add(f"/trilhas/regiao/{slug}/", "0.7", "monthly")

    # City pages
    for url in [p for p in pages_generated if p.startswith("perto-de/")]:
        slug = url.split("/")[1]
        add(f"/perto-de/{slug}/", "0.7", "monthly")

    # Guide state pages
    for url in [p for p in pages_generated if p.startswith("guias/") and p.count("/") == 2]:
        uf = url.split("/")[1]
        add(f"/guias/{uf}/", "0.8", "monthly")

    # Guide city pages
    for url in [p for p in pages_generated if p.startswith("guias/") and p.count("/") == 3]:
        parts = url.split("/")
        add(f"/guias/{parts[1]}/{parts[2]}/", "0.7", "monthly")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(entries)
    xml += "\n</urlset>"

    (BASE_DIR / "sitemap.xml").write_text(xml, encoding="utf-8")
    print(f"  ✓ sitemap.xml with {len(entries)} URLs")


# ─── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\n🚀 Trekko SEO Page Generator\n" + "="*40)

    # Load data
    with open(BASE_DIR / "data" / "trails.json") as f:
        all_trails = json.load(f)
    with open(BASE_DIR / "data" / "guides.json") as f:
        all_guides = json.load(f)

    trails = [t for t in all_trails if t.get("status") == "published"]
    print(f"Loaded {len(trails)} published trails, {len(all_guides):,} guides\n")

    # Generate all page types
    gen_trail_pages(trails)
    gen_state_pages(trails)
    gen_difficulty_pages(trails)
    gen_park_pages(trails)
    gen_region_pages(trails)
    gen_city_pages(trails)
    gen_guide_state_pages(all_guides, trails)
    gen_guide_city_pages(all_guides, min_guides=5)
    gen_sitemap(trails)

    print(f"\n{'='*40}")
    print(f"✅ Done! {len(pages_generated)} pages generated")
    print(f"\nBreakdown:")
    cats = defaultdict(int)
    for p in pages_generated:
        top = p.split("/")[0]
        cats[top] += 1
    for k,v in sorted(cats.items(), key=lambda x:-x[1]):
        print(f"  {k:30s} {v:>4} pages")
    print(f"\nSitemap: {BASE_URL}/sitemap.xml")


if __name__ == "__main__":
    main()
