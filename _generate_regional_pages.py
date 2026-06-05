#!/usr/bin/env python3
"""Generates regional landing pages: /trilhas/sp, /trilhas/mg, /trilhas/cerrado."""

import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

# Re-use all helpers and constants from the main generator
from _generate_landing_pages import (
    trails, all_guides, guides_by_uf, by_uf,
    build_head, build_header, build_breadcrumb,
    build_trail_card, build_trails_section,
    build_tips_section, build_guides_section,
    build_testimonials_section, build_faq_section,
    build_cta_section, build_faq_jsonld, build_item_list_jsonld,
    write_file, PAGE_JS, FOOTER_HTML, STICKY_BAR,
    SP_TRAIL_COUNT, SP_GUIDE_COUNT, SP_STATE_COUNT,
)

# ── Regional page definitions ──────────────────────────────────────────────────

REGIONS = {
    "sp": {
        "slug": "sp",
        "name": "São Paulo",
        "prep": "em SP",
        "title": "Trilhas em SP — São Paulo: Melhores Roteiros | Trekko",
        "desc": "Trilhas em SP (São Paulo): Pedra do Baú, Pico dos Marins e mais roteiros com fichas detalhadas, dificuldade e guias certificados CADASTUR.",
        "hero_image": "/trails/xQQ123BhBF2H.jpg",
        "badge": "📍 São Paulo · SP",
        "uf_filter": ["SP"],
        "subtitle": "São Paulo concentra trekking de alto nível a poucas horas de 22 milhões de pessoas — do Pico dos Marins às rochas vulcânicas da Pedra do Baú.",
        "editorial": (
            "O estado de São Paulo surpreende quem busca trilhas de qualidade próximas à maior metrópole da América do Sul. "
            "A Serra da Mantiqueira, que corta o sul e o leste do estado, oferece travessias alpinas com altitude superior a 2.000 m, "
            "campos de altitude e vistas únicas do Vale do Paraíba. O Pico dos Marins (2.420 m), em Piquete, e a Pedra do Baú "
            "(1.950 m), em São Bento do Sapucaí, são os ícones do trekking paulista — ambos exigem bom condicionamento físico e "
            "resposta ágil a variações climáticas típicas da Mantiqueira. Para além das montanhas, o estado tem parques litorâneos, "
            "cânions e cachoeiras na Serra da Bocaina."
        ),
        "tips": [
            ("Melhor época: abril a outubro", "O inverno paulista é seco e fresco na serra — ideal para longas caminhadas. Evite dezembro a março, quando chuvas intensas tornam trilhas escorregadias e aumentam o risco de raios nos picos."),
            ("Leve camadas de frio na Mantiqueira", "Mesmo no verão, noites nos picos da Mantiqueira podem chegar a 5°C. Leve casaco impermeável e camiseta de lã merino para qualquer saída acima de 1.500 m."),
            ("Respeite a legislação estadual", "Muitas trilhas em SP passam por APPs (Áreas de Preservação Permanente). Não faça trilhas fora dos trajetos demarcados e não deixe lixo no percurso."),
            ("Confirme acesso antes de partir", "Acessos à Pedra do Baú (São Bento do Sapucaí) e ao Pico dos Marins (Piquete) passam por propriedades privadas. Confirme condições e taxas com a Prefeitura ou associações locais."),
            ("Condicionamento físico", "O Pico dos Marins tem 12 km e 1.200 m de ganho de altitude — exige preparo. Faça trilhas menores antes e use os dados de elevação na ficha de cada trilha para calibrar o esforço."),
            ("Guias locais para trilhas técnicas", "Para a Travessia Serra Fina (que passa por SP e MG), guia especializado é altamente recomendado — trechos de escalada e cristas expostas exigem orientação experiente."),
        ],
        "faqs": [
            ("Quais são as melhores trilhas em São Paulo?",
             "O Trekko destaca o Pico dos Marins (2.420 m, em Piquete) e a Pedra do Baú (1.950 m, em São Bento do Sapucaí) como as principais trilhas de montanha do estado. Há também opções no Parque Estadual da Serra do Mar e na Serra da Bocaina."),
            ("A trilha do Pico dos Marins exige guia?",
             "A trilha do Pico dos Marins não exige guia obrigatório por regulamento, mas o percurso de 12 km com 1.200 m de ganho de altitude é desafiador. Para grupos sem experiência em alta montanha, contratar um guia local aumenta segurança e aproveitamento."),
            ("Como chegar a São Bento do Sapucaí para a Pedra do Baú?",
             "São Bento do Sapucaí fica a cerca de 170 km de São Paulo capital pela Rodovia Presidente Dutra (BR-116) com desvio por Taubaté. De carro leva aproximadamente 2h30. Há ônibus saindo do Terminal Rodoviário do Tietê com parada na cidade."),
            ("Qual a diferença entre /trilhas/sp e /trilhas/sao-paulo?",
             "As duas páginas cobrem trilhas do estado de São Paulo. A URL /trilhas/sp usa abreviação e aponta para o mesmo conteúdo editorial regional, sendo útil para buscas com a sigla do estado."),
            ("Existe trilha em São Paulo para iniciantes?",
             "Sim. A Pedra do Baú tem rota alternativa pela face leste com menor dificuldade. Em parques estaduais como o Parque Estadual Cantareira (na Grande SP) há trilhas sinalizadas adequadas para iniciantes e famílias."),
        ],
        "related": [
            ("/trilhas/sao-paulo", "Trilhas em São Paulo (nome completo)"),
            ("/trilhas/minas-gerais", "Minas Gerais"),
            ("/trilhas/rio-de-janeiro", "Rio de Janeiro"),
            ("/trilhas/para-iniciantes", "Trilhas para iniciantes"),
            ("/trilhas/moderado", "Trilhas moderadas"),
            ("/trilhas/cerrado", "Cerrado"),
        ],
    },
    "mg": {
        "slug": "mg",
        "name": "Minas Gerais",
        "prep": "em MG",
        "title": "Trilhas em MG — Minas Gerais: Roteiros e Guias | Trekko",
        "desc": "Trilhas em MG (Minas Gerais): Pico da Bandeira, Travessia Serra Fina e mais rotas com fichas detalhadas, guias CADASTUR e dicas de planejamento.",
        "hero_image": "/trails/Y8KJdb96pKOX.jpg",
        "badge": "📍 Minas Gerais · MG",
        "uf_filter": ["MG"],
        "subtitle": "Minas Gerais tem o topo do Sudeste — o Pico da Bandeira (2.892 m) — e travessias alpinas que figuram entre as mais exigentes do Brasil.",
        "editorial": (
            "Minas Gerais é o estado com maior diversidade de trekking do Sudeste brasileiro. "
            "A Serra do Caparaó abriga o Pico da Bandeira (2.892 m), o terceiro pico mais alto do Brasil, "
            "com trilha de acesso bem sinalizada e infraestrutura de camping organizada pelo ICMBio. "
            "A Travessia Serra Fina — que começa em MG e termina em SP — é considerada uma das mais "
            "técnicas do país, com cristas estreitas, trechos de escalada e exigência de guia. "
            "Além das montanhas, o estado tem trilhas no Vale do Jequitinhonha, nas serras do Espinhaço "
            "e na Chapada Diamantina (fronteira com BA). As cidades históricas como Ouro Preto e "
            "Diamantina servem de base para caminhadas culturais de alto valor."
        ),
        "tips": [
            ("Melhor época para o Caparaó: abril a setembro", "O inverno mineiro é seco e frio na alta altitude. Noites no refugio do Caparaó chegam a -5°C. Leve saco de dormir adequado e camadas térmicas."),
            ("Registro obrigatório no ICMBio", "O Parque Nacional do Caparaó exige registro de entrada e saída. Informe seu plano de rota ao ICMBio antes de iniciar qualquer travessia."),
            ("Guia obrigatório na Serra Fina", "A Travessia Serra Fina exige guia habilitado por lei — trechos com vertentes expostas e cristas de 10 cm de largura não permitem erros de navegação."),
            ("Altitude e aclimatação", "O Pico da Bandeira fica a 2.892 m. Para quem vem do litoral ou do planalto baixo, um dia de aclimatação em Manhumirim ou Espera Feliz ajuda na adaptação."),
            ("Trilhas em parques estaduais", "Minas tem parques estaduais bem estruturados como o Parque Estadual do Ibitipoca — trilhas sinalizadas, cachoeiras e cachoeirões acessíveis para diferentes níveis."),
            ("Cidades históricas como base", "Ouro Preto e Tiradentes ficam próximas a trilhas e serras com menos de 1h de carro. Combine trekking com cultura e gastronomia mineira."),
        ],
        "faqs": [
            ("Quais são as melhores trilhas em Minas Gerais?",
             "O Trekko destaca o Pico da Bandeira (2.892 m, no Parque Nacional do Caparaó) e a Travessia Serra Fina como as principais rotas técnicas do estado. O Parque Estadual do Ibitipoca também oferece trilhas excelentes para todos os níveis."),
            ("O Pico da Bandeira exige guia obrigatório?",
             "A trilha normal do Pico da Bandeira, pelo Parque Nacional do Caparaó (lado MG), não exige guia obrigatório por regulamento, mas é fortemente recomendado para grupos sem experiência em alta montanha. A Travessia Serra Fina, que inclui o Pico das Agulhas Negras, exige guia por lei."),
            ("Como chegar ao Parque Nacional do Caparaó?",
             "A sede do parque no lado mineiro fica em Alto Caparaó, a cerca de 360 km de Belo Horizonte pela BR-116 e estradas vicinais. O acesso de carro é o mais prático. Há pousadas e camping no entorno da sede."),
            ("Qual a diferença entre /trilhas/mg e /trilhas/minas-gerais?",
             "Ambas cobrem o mesmo conteúdo de trilhas em Minas Gerais. A URL /trilhas/mg usa a sigla do estado e é útil para buscas com abreviação."),
            ("Quais trilhas em MG são adequadas para iniciantes?",
             "O Parque Estadual do Ibitipoca (Lima Duarte) tem trilhas bem sinalizadas com distâncias menores e menos desnível. O Pico da Bandeira também tem uma versão diurna de subida e volta no mesmo dia, indicada para quem tem boa condição física mas pouca experiência técnica."),
        ],
        "related": [
            ("/trilhas/minas-gerais", "Trilhas em Minas Gerais (nome completo)"),
            ("/trilhas/sao-paulo", "São Paulo"),
            ("/trilhas/rio-de-janeiro", "Rio de Janeiro"),
            ("/trilhas/especialista", "Trilhas especialista"),
            ("/trilhas/dificil", "Trilhas difíceis"),
            ("/trilhas/cerrado", "Cerrado"),
        ],
    },
    "cerrado": {
        "slug": "cerrado",
        "name": "Cerrado",
        "prep": "no Cerrado",
        "title": "Trilhas no Cerrado — Chapada, Cachoeiras e Savana | Trekko",
        "desc": "Trilhas no Cerrado: Chapada dos Veadeiros, Chapada dos Guimarães, Bonito e mais roteiros com fichas detalhadas, guias CADASTUR e informações de acesso.",
        "hero_image": "/trails/Y8KJdb96pKOX.jpg",
        "badge": "🌿 Bioma Cerrado",
        "uf_filter": ["GO", "MT", "MS", "MG", "BA", "MA"],
        "subtitle": "O Cerrado é o segundo maior bioma do Brasil — uma savana tropical com cachoeiras cristalinas, cânions de arenito e uma biodiversidade sem igual.",
        "editorial": (
            "O Cerrado ocupa 23% do território nacional e abrange estados como Goiás, Mato Grosso, Mato Grosso do Sul, "
            "sul do Maranhão e grande parte de Minas Gerais. Longe da imagem árida que o nome sugere, o bioma combina "
            "campos abertos com vegetação retorcida, veredas úmidas, cachoeiras de água cristalina e formações rochosas "
            "esculpidas por milhões de anos de erosão. "
            "A Chapada dos Veadeiros (GO), Patrimônio Natural da UNESCO, é o epicentro do trekking no Cerrado — "
            "trilhas com quedas d'água espetaculares, quartzitos brilhantes e flora endêmica. "
            "A Chapada dos Guimarães (MT) oferece cânions e mirantes com vistas do Pantanal. "
            "Em Bonito (MS), o ecoturismo de base científica preserva rios de visibilidade excepcional. "
            "O Cerrado é também o berço das águas — grandes bacias como o São Francisco, o Tocantins-Araguaia e o "
            "Paraná nascem aqui, abastecendo metade do Brasil."
        ),
        "tips": [
            ("Melhor época: maio a setembro", "O inverno do Cerrado é seco e com menos calor — ideal para trilhas. Evite dezembro a março, quando as chuvas intensas tornam alguns atrativos inacessíveis e o calor úmido esgota rapidamente."),
            ("Proteção solar é obrigatória", "O Cerrado tem incidência solar muito alta, especialmente em trilhas abertas sem sombra. FPS 50+, óculos de sol e chapéu são indispensáveis em qualquer saída."),
            ("Leve água suficiente", "Algumas trilhas no Cerrado têm longos trechos sem água potável. Carregue no mínimo 2 L por pessoa para saídas de meio dia, e use filtro em travessias longas."),
            ("Respeite a fauna", "O Cerrado tem onça, lobo-guará, tamanduá-bandeira e diversas cobras. Não alimente animais silvestres, use calçado fechado e fique nos trileiros demarcados."),
            ("Confirme atrativos abertos", "Parques como a Chapada dos Veadeiros têm visitação controlada por setores. Confirme disponibilidade e eventuais cotas de acesso antes de partir."),
            ("Explore além dos parques nacionais", "As APAs e propriedades privadas com ecoturismo no entorno dos parques oferecem cachoeiras e trilhas com menos visitação e experiência mais imersiva."),
        ],
        "faqs": [
            ("Quais são as melhores trilhas no Cerrado?",
             "O Trekko destaca a Chapada dos Veadeiros (GO) com trilhas como o Vale da Lua e as Cachoeiras São Bento e Carioquinhas, a Chapada dos Guimarães (MT) com o Cânion do Rio Claro, e Bonito (MS) com flutuação na Lagoa Azul. Há também opções excelentes na Serra da Canastra (MG)."),
            ("Preciso de guia para trilhas no Cerrado?",
             "Depende do atrativo. O Vale da Lua na Chapada dos Veadeiros não exige guia, mas muitas cachoeiras particulares e trilhas no interior do Parque Nacional exigem acompanhamento. Em Bonito (MS), guia local é obrigatório em praticamente todos os atrativos por regulamento municipal."),
            ("Qual a melhor base para explorar o Cerrado?",
             "Alto Paraíso de Goiás é a principal base para a Chapada dos Veadeiros, a 250 km de Brasília. Cuiabá serve para a Chapada dos Guimarães e o Pantanal. Bonito tem boa infraestrutura própria. Campo Grande é boa base para o sul do MS."),
            ("O Cerrado é apenas vegetação rasteira?",
             "Não. O Cerrado tem enorme diversidade de fitofisionomias: campo limpo aberto, cerradão (com árvores densas), veredas com buriti (palmeiras de até 15 m), matas de galeria em vales úmidos e campos rupestres nas chapadas. A paisagem varia muito dentro do bioma."),
            ("Quando o Cerrado está com mais água nas cachoeiras?",
             "As cachoeiras têm mais volume entre dezembro e março, no auge das chuvas — espetacular visualmente, mas com trilhas mais escorregadias. No período seco (maio-setembro), a água fica mais cristalina e as trilhas mais seguras. Cada atrativo tem seu pico ideal; confirme com guias locais."),
        ],
        "related": [
            ("/trilhas/goias", "Trilhas em Goiás"),
            ("/trilhas/mato-grosso", "Mato Grosso"),
            ("/trilhas/mato-grosso-do-sul", "Mato Grosso do Sul"),
            ("/trilhas/minas-gerais", "Minas Gerais"),
            ("/trilhas/com-cachoeira", "Trilhas com cachoeira"),
            ("/trilhas/mg", "Trilhas MG"),
        ],
    },
}

# ── Build page HTML ────────────────────────────────────────────────────────────

def build_related_section(links):
    items = ""
    for href, label in links:
        items += f'<a href="{href}" class="related-link">→ {label}</a>\n'
    return f"""<section class="section section--alt" aria-labelledby="related-h2">
  <div class="container">
    <h2 id="related-h2">Explore outras regiões</h2>
    <div class="related-grid">{items}</div>
  </div>
</section>"""


def build_regional_page(cfg):
    slug = cfg["slug"]
    canonical_path = f"/trilhas/{slug}"
    canonical = f"https://trekko.com.br{canonical_path}"

    # Filter trails for this region
    uf_filters = cfg["uf_filter"]
    region_trails = [t for t in trails if t.get("uf") in uf_filters and t.get("status") == "published"]

    n_trails = len(region_trails)
    parks = list({t["park"] for t in region_trails})

    faqs = cfg["faqs"]
    jsonld = build_faq_jsonld(faqs, canonical_path)
    item_list_jsonld = build_item_list_jsonld(region_trails, canonical_path, f"Trilhas {cfg['prep']}")

    head = build_head(cfg["title"], cfg["desc"], canonical, cfg["hero_image"], jsonld, extra_jsonld=item_list_jsonld)
    header = build_header()
    breadcrumb = build_breadcrumb([
        ("Trekko", "/"), ("Trilhas", "/trilhas"), (cfg["name"], canonical_path)
    ])

    hero = f"""<section class="hero" style="--hero-bg:url('{cfg['hero_image']}')">
  <div class="container">
    <div class="hero-inner">
      <div class="hero-badge">{cfg['badge']}</div>
      <h1>Trilhas {cfg['prep']}</h1>
      <p class="hero-subtitle">{cfg['subtitle']}</p>
      <div class="hero-ctas">
        <a href="#trilhas" class="btn btn--white btn--lg">Ver trilhas</a>
        <a href="/guias" class="btn btn--outline-white btn--lg">Encontrar guias</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><strong>{n_trails}</strong><span>trilha{'s' if n_trails != 1 else ''}</span></div>
        <div class="stat"><strong>{len(parks)}</strong><span>parque{'s' if len(parks) != 1 else ''}</span></div>
        <div class="stat"><strong>CADASTUR</strong><span>guias certificados</span></div>
      </div>
    </div>
  </div>
</section>"""

    editorial_html = f"""<section class="section">
  <div class="container editorial">
    <h2>Trekking {cfg['prep']}</h2>
    <p>{cfg['editorial']}</p>
  </div>
</section>"""

    trails_section = build_trails_section(region_trails, f"Trilhas {cfg['prep']} ({n_trails})")
    tips_section = build_tips_section(cfg["tips"], f"Como planejar sua trilha {cfg['prep']}")

    testimonials_section = build_testimonials_section(SP_TRAIL_COUNT, SP_GUIDE_COUNT, SP_STATE_COUNT)

    # Guides from relevant UFs
    all_region_guides = []
    seen = set()
    for uf in uf_filters:
        for g in guides_by_uf.get(uf, []):
            gid = g.get("cadasturNumber", g.get("name"))
            if gid not in seen:
                seen.add(gid)
                all_region_guides.append(g)
    guides_section = build_guides_section(all_region_guides[:3], cfg["prep"]) if all_region_guides else ""

    faq_section = build_faq_section(faqs, f"Perguntas frequentes sobre trilhas {cfg['prep']}")
    related_section = build_related_section(cfg["related"])
    cta_section = build_cta_section(
        f"Encontre sua próxima trilha {cfg['prep']}",
        "Compare roteiros, veja dificuldade, parques e guias. Planeje com informação e segurança.",
        canonical_path,
    )

    js = PAGE_JS.format(
        event_name="page_view_trail_landing",
        event_params={"region": slug, "page_type": "trail_regional_landing"},
    )

    return "\n".join([
        head, "<body>", header, breadcrumb, hero,
        editorial_html, trails_section, tips_section,
        testimonials_section, guides_section, faq_section,
        related_section, cta_section,
        FOOTER_HTML, js, STICKY_BAR, "</body>\n</html>",
    ])


# ── Main ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Generating regional landing pages…")
    for slug, cfg in REGIONS.items():
        html = build_regional_page(cfg)
        out_path = os.path.join(BASE, "trilhas", slug, "index.html")
        write_file(out_path, html)
    print("Done.")
