#!/usr/bin/env python3
"""
Gera sitemap.xml dinâmico para trekko.com.br.
Lê dados de data/trails.json, data/blog.json, data/authors.json e
combina com páginas estáticas para produzir um sitemap completo.

Uso: python3 _generate_sitemap.py
"""

import json
import os
from datetime import datetime, date

BASE_URL = "https://www.trekko.com.br"
TODAY = date.today().isoformat()
OUTPUT_FILE = "sitemap.xml"

# Diretórios especiais que não são slugs de estado
TRILHAS_NON_STATE_DIRS = {
    "cidades", "parques", "data", "index.html",
    "para-iniciantes", "moderado", "dificil", "especialista",
    "com-guia", "com-cachoeira", "rj",
    "trilha-cotovelo-vertice-itaimbezinho-cambara-do-sul-rs",
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fmt_date(iso_str):
    """Retorna apenas a parte YYYY-MM-DD de uma string ISO."""
    if not iso_str:
        return TODAY
    return iso_str[:10]


def url_entry(loc, lastmod, changefreq, priority, extra=""):
    return (
        f"  <url>\n"
        f"    <loc>{BASE_URL}{loc}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        f"{extra}"
        f"  </url>\n"
    )


def news_block(pub_date, title):
    safe = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f"    <news:news>\n"
        f"      <news:publication>\n"
        f"        <news:name>Blog do Trekko</news:name>\n"
        f"        <news:language>pt</news:language>\n"
        f"      </news:publication>\n"
        f"      <news:publication_date>{pub_date}</news:publication_date>\n"
        f"      <news:title>{safe}</news:title>\n"
        f"    </news:news>\n"
    )


def scan_listing_dirs(base_dir, url_prefix, exclude=None):
    """Retorna lista de slugs encontrados em base_dir, excluindo exclude."""
    exclude = exclude or set()
    entries = []
    if not os.path.isdir(base_dir):
        return entries
    for name in sorted(os.listdir(base_dir)):
        if name in exclude:
            continue
        if os.path.isdir(os.path.join(base_dir, name)):
            entries.append(f"{url_prefix}/{name}")
    return entries


def build_sitemap():
    urls = []

    # ── Páginas estáticas principais ─────────────────────────────────────────
    static_core = [
        ("/",                                      TODAY,        "weekly",  "1.0"),
        ("/trilhas",                               TODAY,        "weekly",  "0.9"),
        ("/blog",                                  TODAY,        "weekly",  "0.85"),
        ("/sobre",                                 "2026-05-29", "monthly", "0.8"),
        ("/contato",                               "2026-01-01", "monthly", "0.6"),
        ("/seguranca-em-trilhas",                  "2026-01-01", "monthly", "0.8"),
        ("/privacidade",                           "2026-01-01", "yearly",  "0.4"),
        ("/termos-de-uso",                         "2026-01-01", "yearly",  "0.4"),
        ("/politica-de-guias",                     "2026-01-01", "yearly",  "0.4"),
        ("/politica-editorial",                    "2026-01-01", "yearly",  "0.5"),
        ("/remocao-ou-atualizacao-de-dados",       "2026-01-01", "yearly",  "0.3"),
        ("/politica-de-cookies",                   "2026-01-01", "yearly",  "0.4"),
        ("/divulgacao-de-afiliados",               "2026-01-01", "yearly",  "0.4"),
    ]
    for loc, lastmod, freq, pri in static_core:
        urls.append(url_entry(loc, lastmod, freq, pri))

    # ── Equipamentos ─────────────────────────────────────────────────────────
    equipamentos = [
        ("/equipamentos",                                                   TODAY,        "weekly",  "0.95"),
        ("/equipamentos/mochilas",                                          TODAY,        "weekly",  "0.85"),
        ("/equipamentos/botas-e-tenis",                                     TODAY,        "weekly",  "0.85"),
        ("/equipamentos/bastoes-de-caminhada",                              TODAY,        "weekly",  "0.8"),
        ("/equipamentos/guias",                                             TODAY,        "weekly",  "0.85"),
        ("/equipamentos/guias/como-escolher-mochila-de-trilha",             "2026-05-28", "monthly", "0.85"),
        ("/equipamentos/guias/o-que-levar-em-uma-trilha-de-um-dia",        "2026-05-28", "monthly", "0.85"),
        ("/equipamentos/guias/kit-primeiros-socorros-para-trilha",          "2026-05-12", "monthly", "0.85"),
        ("/equipamentos/comparativos",                                      TODAY,        "weekly",  "0.8"),
        ("/equipamentos/comparativos/melhores-mochilas-de-ataque",          "2026-05-28", "monthly", "0.85"),
        ("/equipamentos/comparativos/melhores-kits-primeiros-socorros-trilha", "2026-05-12", "monthly", "0.85"),
        ("/equipamentos/como-escolhemos",                                   "2026-05-28", "yearly",  "0.6"),
    ]
    for loc, lastmod, freq, pri in equipamentos:
        urls.append(url_entry(loc, lastmod, freq, pri))

    # ── Guias ─────────────────────────────────────────────────────────────────
    urls.append(url_entry("/guias/ativar-perfil", "2026-01-01", "monthly", "0.6"))

    # ── Autores ───────────────────────────────────────────────────────────────
    try:
        authors = load_json("data/authors.json")
        for author in authors:
            slug = author.get("slug")
            if slug:
                urls.append(url_entry(f"/autores/{slug}", "2026-01-01", "monthly", "0.65"))
    except FileNotFoundError:
        pass

    # ── Trilhas por estado (varrendo /trilhas/) ───────────────────────────────
    state_slugs = scan_listing_dirs("trilhas", "/trilhas", exclude=TRILHAS_NON_STATE_DIRS)
    for loc in state_slugs:
        urls.append(url_entry(loc, TODAY, "weekly", "0.85"))

    # ── Trilhas por dificuldade / tipo ────────────────────────────────────────
    difficulty_pages = [
        ("/trilhas/para-iniciantes", "0.85"),
        ("/trilhas/moderado",        "0.8"),
        ("/trilhas/dificil",         "0.8"),
        ("/trilhas/especialista",    "0.8"),
        ("/trilhas/com-guia",        "0.75"),
        ("/trilhas/com-cachoeira",   "0.75"),
    ]
    for loc, pri in difficulty_pages:
        urls.append(url_entry(loc, TODAY, "weekly", pri))

    # ── Trilhas por cidade ────────────────────────────────────────────────────
    city_slugs = scan_listing_dirs("trilhas/cidades", "/trilhas/cidades")
    for loc in city_slugs:
        urls.append(url_entry(loc, TODAY, "monthly", "0.75"))

    # ── Trilhas por parque ────────────────────────────────────────────────────
    park_slugs = scan_listing_dirs("trilhas/parques", "/trilhas/parques")
    for loc in park_slugs:
        urls.append(url_entry(loc, TODAY, "monthly", "0.75"))

    # ── Trilhas individuais (data/trails.json) ────────────────────────────────
    trails = load_json("data/trails.json")
    published_trails = [t for t in trails if t.get("status", "published") == "published"]
    for trail in published_trails:
        slug = trail.get("slug")
        if not slug:
            continue
        updated = fmt_date(trail.get("updatedAt") or trail.get("publishedAt"))
        if updated == TODAY:
            updated = "2026-05-28"  # fallback para trilhas sem data explícita
        urls.append(url_entry(f"/trilha/{slug}", updated, "monthly", "0.8"))

    # ── Blog posts (data/blog.json) ───────────────────────────────────────────
    posts = load_json("data/blog.json")
    published_posts = [p for p in posts if p.get("status") == "published"]
    for post in published_posts:
        slug = post.get("slug")
        if not slug:
            continue
        published_at = fmt_date(post.get("publishedAt"))
        updated_at = fmt_date(post.get("updatedAt") or post.get("publishedAt"))
        title = post.get("title", "")
        extra = news_block(published_at, title)
        urls.append(url_entry(f"/blog/{slug}", updated_at, "monthly", "0.8", extra=extra))

    return urls


def write_sitemap(urls):
    header = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"\n'
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n\n'
    )
    footer = "</urlset>\n"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(header)
        for entry in urls:
            f.write(entry)
        f.write(footer)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    urls = build_sitemap()
    write_sitemap(urls)
    print(f"✅  sitemap.xml gerado com {len(urls)} URLs → {OUTPUT_FILE}")
