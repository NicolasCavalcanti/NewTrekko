#!/usr/bin/env python3
"""
TAREFA 4.4 — Checklist de vinculação Google Search Console + GA4

Uso:
    python _gsc_ga4_link.py

Este script imprime o passo a passo para:
  1. Verificar a propriedade trekko.com.br no Search Console
  2. Vincular Search Console ao GA4 (G-S816P190VN)
  3. Configurar relatório de páginas por impressões orgânicas
"""

GA4_ID   = "G-S816P190VN"
SITE_URL = "https://trekko.com.br"

STEPS = [
    (
        "ETAPA 1 — Verificar propriedade no Search Console",
        [
            f"Acesse https://search.google.com/search-console/welcome",
            f"Selecione 'Prefixo de URL' e insira: {SITE_URL}",
            "Escolha o método 'Tag HTML'",
            "Copie o token da meta tag exibido (ex: <meta name=\"google-site-verification\" content=\"ABC123...\">)",
            "No arquivo index.html (raiz do projeto), substitua a linha comentada:",
            "  <!-- <meta name=\"google-site-verification\" content=\"COLE_SEU_TOKEN_GSC_AQUI\"> -->",
            "  Por:",
            "  <meta name=\"google-site-verification\" content=\"SEU_TOKEN_REAL\">",
            "Faça commit e push → aguarde o deploy (Vercel/Netlify)",
            "Volte ao Search Console e clique 'Verificar' — deve aparecer status Verde",
        ],
    ),
    (
        "ETAPA 2 — Vincular Search Console ao GA4",
        [
            f"Acesse https://analytics.google.com → Propriedade {GA4_ID}",
            "Menu lateral → Admin (engrenagem) → Propriedade → Links do Search Console",
            "Clique em 'Vincular' → selecione a propriedade trekko.com.br",
            "Confirme o fluxo de dados web (trekko.com.br) e salve",
            "Aguarde até 48 h para os dados do GSC aparecerem nos relatórios do GA4",
        ],
    ),
    (
        "ETAPA 3 — Configurar relatório de impressões orgânicas no GA4",
        [
            "No GA4, acesse Relatórios → Aquisição → Aquisição de tráfego",
            "Adicione dimensão secundária: 'Página de destino'",
            "Filtre por canal: 'Pesquisa orgânica'",
            "Clique em 'Personalizar relatório' (ícone de lápis) → salve como 'Páginas por impressões orgânicas'",
            "Alternativa: Relatórios → Biblioteca → crie coleção 'SEO' com os cards:",
            "  · Páginas e telas (filtro: Organic Search)",
            "  · Consultas do Search Console (disponível após vinculação)",
            "  · Impressões vs Cliques por página de destino",
        ],
    ),
    (
        "ETAPA 4 — Verificar integração (após 48 h)",
        [
            "GA4 → Relatórios → Aquisição → Search Console",
            "Confirme que as dimensões 'Consultas' e 'Páginas de destino do Google Search Console' aparecem",
            "Se não aparecerem: verifique que a propriedade GSC é do tipo 'Domínio' ou 'Prefixo de URL'",
            "Critério de aceite (TAREFA 4.4): dados visíveis no GA4 dentro de 48 h da vinculação ✓",
        ],
    ),
]


def main():
    print("=" * 65)
    print("TAREFA 4.4 · Vinculação Search Console + GA4 — Checklist")
    print("=" * 65)
    print(f"  GA4 Measurement ID : {GA4_ID}")
    print(f"  Site               : {SITE_URL}")
    print()

    for title, items in STEPS:
        print(f"\n{'─' * 65}")
        print(f"  {title}")
        print(f"{'─' * 65}")
        for i, item in enumerate(items, 1):
            prefix = f"  {i:>2}. " if not item.startswith("  ") else ""
            print(f"{prefix}{item}")

    print(f"\n{'=' * 65}")
    print("  Links rápidos")
    print(f"{'=' * 65}")
    print("  GSC  → https://search.google.com/search-console")
    print("  GA4  → https://analytics.google.com")
    print(f"  Docs → https://support.google.com/analytics/answer/9379420")
    print()


if __name__ == "__main__":
    main()
