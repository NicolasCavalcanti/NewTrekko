#!/usr/bin/env python3
"""
DEV-15 – Google Search Console: validação de sitemap, meta tag GSC e checklist de configuração.

Uso:
    python _gsc_index_check.py

Saída:
    - Valida estrutura do sitemap.xml (contagem, duplicatas, bloqueios por robots.txt)
    - Verifica se a meta tag de verificação GSC está ativa no index.html
    - Verifica se GTM_ID e GA4_ID estão configurados
    - Confirma se Core Web Vitals tracking (initCoreWebVitals) está presente
    - Imprime as 20 URLs de maior prioridade para solicitar indexação manual no GSC
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

BASE   = Path(__file__).parent
SITEMAP = BASE / "sitemap.xml"
INDEX   = BASE / "index.html"
ANALYTICS_JS = BASE / "assets" / "trekko-analytics.js"
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


def check_index_html() -> dict:
    """Check GSC meta tag, GA4_ID and GTM_ID status in index.html."""
    if not INDEX.exists():
        return {"error": "index.html not found"}
    content = INDEX.read_text(encoding="utf-8")

    # GSC verification meta tag
    placeholder_commented = "<!-- <meta name=\"google-site-verification\" content=\"COLE_SEU_TOKEN_GSC_AQUI\">" in content
    active_gsc = bool(re.search(
        r'<meta\s+name="google-site-verification"\s+content="(?!COLE_SEU_TOKEN_GSC_AQUI)[^"]{10,}"',
        content
    ))

    # GA4_ID
    ga4_match = re.search(r"GA4_ID:\s*'([^']+)'", content)
    ga4_id = ga4_match.group(1) if ga4_match else None

    # GTM_ID
    gtm_match = re.search(r"GTM_ID:\s*'([^']+)'", content)
    gtm_id = gtm_match.group(1) if gtm_match else None

    return {
        "gsc_meta_active": active_gsc,
        "gsc_placeholder_present": placeholder_commented,
        "ga4_id": ga4_id,
        "gtm_id": gtm_id,
    }


def check_cwv_tracking() -> bool:
    """Verify initCoreWebVitals is present in trekko-analytics.js."""
    if not ANALYTICS_JS.exists():
        return False
    return "initCoreWebVitals" in ANALYTICS_JS.read_text(encoding="utf-8")


def main():
    print("=" * 60)
    print("DEV-15 · Google Search Console – Validação completa")
    print("=" * 60)

    # ── Sitemap ────────────────────────────────────────────────
    urls = load_sitemap_urls()
    report = validate(urls)

    print(f"\n{'─'*60}")
    print("  SITEMAP")
    print(f"{'─'*60}")
    print(f"  ✓ Total de URLs           : {report['total']}")
    if report["duplicates"]:
        print(f"  ✗ URLs duplicadas         : {len(report['duplicates'])}")
        for u in report["duplicates"]:
            print(f"      {u}")
    else:
        print("  ✓ Sem URLs duplicadas")

    if report["blocked_by_robots"]:
        print(f"  ✗ URLs bloqueadas (robots): {len(report['blocked_by_robots'])}")
        for u in report["blocked_by_robots"]:
            print(f"      {u}")
    else:
        print("  ✓ Nenhuma URL bloqueada pelo robots.txt")

    # ── index.html ────────────────────────────────────────────
    idx = check_index_html()
    print(f"\n{'─'*60}")
    print("  INDEX.HTML — Configuração")
    print(f"{'─'*60}")

    if idx.get("error"):
        print(f"  ✗ {idx['error']}")
    else:
        if idx["gsc_meta_active"]:
            print("  ✓ GSC meta tag de verificação: ATIVA")
        elif idx["gsc_placeholder_present"]:
            print("  ✗ GSC meta tag: PLACEHOLDER (ação necessária)")
            print("    → Obtenha o token em Search Console → Configurações → Verificação")
            print("    → Substitua COLE_SEU_TOKEN_GSC_AQUI pelo token real em index.html")
        else:
            print("  ✗ GSC meta tag: NÃO ENCONTRADA")

        if idx["ga4_id"]:
            print(f"  ✓ GA4_ID configurado          : {idx['ga4_id']}")
        else:
            print("  ✗ GA4_ID não configurado")

        if idx["gtm_id"]:
            print(f"  ✓ GTM_ID configurado          : {idx['gtm_id']}")
        else:
            print("  ⚠ GTM_ID: null (GA4 direct mode ativo — GTM opcional)")
            print("    → Para ativar GTM: defina GTM_ID em window.TREKKO_CONFIG em index.html")

    # ── Core Web Vitals ───────────────────────────────────────
    cwv_ok = check_cwv_tracking()
    print(f"\n{'─'*60}")
    print("  CORE WEB VITALS")
    print(f"{'─'*60}")
    if cwv_ok:
        print("  ✓ initCoreWebVitals presente em trekko-analytics.js")
        print("    Métricas enviadas ao GA4: LCP, CLS, INP, FCP, TTFB")
        print("    Relatório disponível: GA4 → Relatórios → Core web vitals")
    else:
        print("  ✗ initCoreWebVitals NÃO encontrada em trekko-analytics.js")

    print("\n" + "=" * 60)
    print("  20 URLs para Inspeção → Solicitar indexação no GSC")
    print("=" * 60)
    sitemap_set = set(urls)
    sitemap_set_norm = {u.rstrip('/').replace('://trekko.com.br', '://www.trekko.com.br') for u in sitemap_set}
    for i, (label, url) in enumerate(PRIORITY_URLS, 1):
        url_norm = url.rstrip('/').replace('://trekko.com.br', '://www.trekko.com.br')
        in_sitemap = "✓" if url_norm in sitemap_set_norm else "✗ NÃO ESTÁ NO SITEMAP"
        print(f"{i:>2}. [{in_sitemap}] {label}")
        print(f"      {url}")

    print("\nPasso a passo no Search Console:")
    print("  1. Acesse https://search.google.com/search-console")
    print("  2. Sitemaps → confirme https://trekko.com.br/sitemap.xml → clique 'Reenviar'")
    print("  3. Para cada URL acima: Inspeção de URL → cole a URL → 'Solicitar indexação'")
    print("  4. Verifique Cobertura para garantir ausência de novos erros\n")


if __name__ == "__main__":
    main()
