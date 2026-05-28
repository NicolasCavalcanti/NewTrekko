#!/usr/bin/env python3
"""
DEV-15 – Google Search Console: validação do sitemap e lista de 20 URLs para indexação manual.

Uso:
    python _gsc_index_check.py

Saída:
    - Valida estrutura do sitemap.xml (contagem, duplicatas, bloqueios por robots.txt)
    - Imprime as 20 URLs de maior prioridade para solicitar indexação manual no GSC
"""

import xml.etree.ElementTree as ET
from pathlib import Path

SITEMAP = Path(__file__).parent / "sitemap.xml"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

ROBOTS_DISALLOW = [
    "/perfil", "/checkout", "/reservas", "/admin",
    "/api/", "/guia/", "/expedicao/", "/component-showcase",
]
ROBOTS_ALLOW_EXCEPTIONS = ["/guias/ativar-perfil"]

# 20 URLs mais importantes para indexação manual no GSC — ordenadas por prioridade/impacto SEO
PRIORITY_URLS = [
    # Página principal
    ("Homepage",                    "https://trekko.com.br/"),
    # Seção central de conteúdo
    ("Trilhas – índice",            "https://trekko.com.br/trilhas/"),
    ("Blog – índice",               "https://trekko.com.br/blog/"),
    # Top 5 trilhas com maior volume de busca
    ("Travessia Petrópolis–Teresópolis", "https://trekko.com.br/trilha/travessia-petropolis-teresopolis/"),
    ("Monte Roraima",               "https://trekko.com.br/trilha/monte-roraima/"),
    ("Pico da Bandeira",            "https://trekko.com.br/trilha/pico-da-bandeira/"),
    ("Pico das Agulhas Negras",     "https://trekko.com.br/trilha/pico-das-agulhas-negras/"),
    ("Travessia Vale do Pati",      "https://trekko.com.br/trilha/travessia-vale-do-pati/"),
    # Top 5 artigos do blog mais recentes (Sprint 3)
    ("Blog: Trilhas Nordeste Brasil",       "https://trekko.com.br/blog/trilhas-nordeste-brasil/"),
    ("Blog: Preparo Físico Trekking",       "https://trekko.com.br/blog/preparo-fisico-trekking/"),
    ("Blog: Melhores Trilhas RS Canyons",   "https://trekko.com.br/blog/melhores-trilhas-rs-canyons/"),
    ("Blog: Como Encontrar Guia Cadastur",  "https://trekko.com.br/blog/guia-cadastur-como-encontrar/"),
    ("Blog: Como Planejar Trilha em Grupo", "https://trekko.com.br/blog/como-planejar-trilha-grupo/"),
    # Páginas institucionais (task DEV-15)
    ("Sobre",                       "https://trekko.com.br/sobre/"),
    ("Contato",                     "https://trekko.com.br/contato/"),
    # Páginas de alta intenção — filtros por estado
    ("Trilhas Rio de Janeiro",      "https://trekko.com.br/trilhas/rio-de-janeiro/"),
    ("Trilhas São Paulo",           "https://trekko.com.br/trilhas/sao-paulo/"),
    ("Trilhas Minas Gerais",        "https://trekko.com.br/trilhas/minas-gerais/"),
    # Equipamentos (alta conversão)
    ("Equipamentos – índice",       "https://trekko.com.br/equipamentos/"),
    # Conteúdo de segurança (E-E-A-T)
    ("Segurança em Trilhas",        "https://trekko.com.br/seguranca-em-trilhas/"),
]


def load_sitemap_urls():
    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    urls = []
    for url_el in root.findall("sm:url", NS):
        loc = url_el.findtext("sm:loc", namespaces=NS)
        if loc:
            urls.append(loc)
    return urls


def is_blocked(url: str) -> bool:
    path = url.replace("https://trekko.com.br", "")
    for exc in ROBOTS_ALLOW_EXCEPTIONS:
        if path.startswith(exc):
            return False
    for dis in ROBOTS_DISALLOW:
        if path.startswith(dis):
            return True
    return False


def validate(urls: list[str]) -> dict:
    seen, dups, blocked = set(), [], []
    for u in urls:
        if u in seen:
            dups.append(u)
        seen.add(u)
        if is_blocked(u):
            blocked.append(u)
    return {"total": len(urls), "duplicates": dups, "blocked_by_robots": blocked}


def main():
    print("=" * 60)
    print("DEV-15 · Google Search Console – Validação do sitemap")
    print("=" * 60)

    urls = load_sitemap_urls()
    report = validate(urls)

    print(f"\n✓ Total de URLs no sitemap : {report['total']}")
    if report["duplicates"]:
        print(f"✗ URLs duplicadas          : {len(report['duplicates'])}")
        for u in report["duplicates"]:
            print(f"    {u}")
    else:
        print("✓ Nenhuma URL duplicada")

    if report["blocked_by_robots"]:
        print(f"✗ URLs bloqueadas (robots) : {len(report['blocked_by_robots'])}")
        for u in report["blocked_by_robots"]:
            print(f"    {u}")
    else:
        print("✓ Nenhuma URL bloqueada pelo robots.txt")

    print("\n" + "=" * 60)
    print("20 URLs para Inspeção de URL → Solicitar indexação no GSC")
    print("=" * 60)
    for i, (label, url) in enumerate(PRIORITY_URLS, 1):
        in_sitemap = "✓" if url in set(urls) else "✗ NÃO ESTÁ NO SITEMAP"
        print(f"{i:>2}. [{in_sitemap}] {label}")
        print(f"      {url}")

    print("\nPasso a passo no Search Console:")
    print("  1. Acesse https://search.google.com/search-console")
    print("  2. Sitemaps → confirme https://trekko.com.br/sitemap.xml → clique 'Reenviar'")
    print("  3. Para cada URL acima: Inspeção de URL → cole a URL → 'Solicitar indexação'")
    print("  4. Verifique Cobertura para garantir ausência de novos erros\n")


if __name__ == "__main__":
    main()
