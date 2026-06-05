#!/usr/bin/env python3
"""Generates trail detail pages: SEO head + static editorial body + React SPA root."""
import json, math, os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "data", "trails.json")) as f:
    trails = json.load(f)

DIFF_LABELS = {
    "easy": "Fácil",
    "moderate": "Moderado",
    "hard": "Difícil",
    "expert": "Especialista",
}

UF_NAMES = {
    "RR": "Roraima",      "RJ": "Rio de Janeiro", "GO": "Goiás",
    "SP": "São Paulo",    "MG": "Minas Gerais",   "RS": "Rio Grande do Sul",
    "SC": "Santa Catarina","CE": "Ceará",          "PR": "Paraná",
    "BA": "Bahia",        "ES": "Espírito Santo", "MA": "Maranhão",
    "MS": "Mato Grosso do Sul", "MT": "Mato Grosso", "PE": "Pernambuco",
}
UF_SLUGS = {
    "RR": "roraima",         "RJ": "rio-de-janeiro", "GO": "goias",
    "SP": "sao-paulo",       "MG": "minas-gerais",   "RS": "rio-grande-do-sul",
    "SC": "santa-catarina",  "CE": "ceara",           "PR": "parana",
    "BA": "bahia",           "ES": "espirito-santo", "MA": "maranhao",
    "MS": "mato-grosso-do-sul", "MT": "mato-grosso", "PE": "pernambuco",
}

BREADCRUMB_CSS = """\
  <style>
    .trekko-bc{padding:.6rem 0;border-bottom:1px solid #e2e8f0;background:#fff;font-family:Inter,system-ui,sans-serif}
    .trekko-bc .container{max-width:1200px;margin:0 auto;padding:0 1rem}
    .trekko-bc ol{display:flex;flex-wrap:wrap;gap:.25rem;align-items:center;font-size:.8rem;color:#64748b;list-style:none;margin:0;padding:0}
    .trekko-bc li+li::before{content:"/";margin-right:.25rem;color:#94a3b8}
    .trekko-bc a{color:#64748b;text-decoration:none}
    .trekko-bc a:hover{color:#15803d}
    .trekko-bc [aria-current=page]{color:#1e293b;font-weight:500}
  </style>"""

EDITORIAL_CSS = """\
  <style>
    #trekko-editorial{font-family:Inter,system-ui,sans-serif;background:#f8fafc;border-top:4px solid #15803d;padding:3rem 1rem 4rem;color:#1e293b;line-height:1.8}
    #trekko-editorial .ei{max-width:800px;margin:0 auto}
    #trekko-editorial h2{font-family:Sora,system-ui,sans-serif;font-size:1.2rem;font-weight:700;color:#0f172a;margin:2rem 0 .6rem;border-left:4px solid #15803d;padding-left:.75rem}
    #trekko-editorial p{margin-bottom:1rem;font-size:.96rem;color:#334155}
    #trekko-editorial ul{padding-left:1.4rem;margin-bottom:1rem}
    #trekko-editorial ul li{margin-bottom:.35rem;font-size:.96rem;color:#334155}
    #trekko-editorial .ef{margin-top:2.5rem;padding-top:1.25rem;border-top:1px solid #e2e8f0;font-size:.82rem;color:#64748b}
    @media(max-width:640px){#trekko-editorial{padding:2rem .75rem 3rem}#trekko-editorial h2{font-size:1.05rem}}
  </style>"""

DISCLAIMER_CSS = """\
  <style>
    #trekko-disclaimer{font-family:Inter,system-ui,sans-serif;background:#f1f5f9;border-top:1px solid #e2e8f0;padding:2rem 1rem;color:#475569}
    #trekko-disclaimer .td-inner{max-width:800px;margin:0 auto;display:flex;gap:1rem;align-items:flex-start}
    #trekko-disclaimer .td-icon{font-size:1.4rem;flex-shrink:0;margin-top:.1rem}
    #trekko-disclaimer .td-text{font-size:.875rem;line-height:1.65}
    #trekko-disclaimer .td-text p{margin:0 0 .5rem}
    #trekko-disclaimer .td-text a{color:#15803d;text-decoration:underline}
    @media(max-width:640px){#trekko-disclaimer{padding:1.5rem .75rem}#trekko-disclaimer .td-inner{flex-direction:column;gap:.5rem}}
  </style>"""

NEARBY_CSS = """\
  <style>
    #trekko-nearby{font-family:Inter,system-ui,sans-serif;background:#fff;border-top:1px solid #e2e8f0;padding:3rem 1rem 3.5rem}
    #trekko-nearby .tn-inner{max-width:800px;margin:0 auto}
    #trekko-nearby h2{font-family:Sora,system-ui,sans-serif;font-size:1.2rem;font-weight:700;color:#0f172a;margin:0 0 1.5rem;border-left:4px solid #15803d;padding-left:.75rem}
    #trekko-nearby .tn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem}
    #trekko-nearby .tn-card{display:block;text-decoration:none;color:inherit;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;transition:box-shadow .2s,transform .2s}
    #trekko-nearby .tn-card:hover{box-shadow:0 4px 16px rgba(0,0,0,.1);transform:translateY(-2px)}
    #trekko-nearby .tn-card img{width:100%;height:140px;object-fit:cover;display:block}
    #trekko-nearby .tn-card-body{padding:.75rem 1rem .9rem}
    #trekko-nearby .tn-name{font-size:.92rem;font-weight:600;color:#0f172a;margin:0 0 .4rem;line-height:1.35}
    #trekko-nearby .tn-meta{display:flex;gap:.5rem;flex-wrap:wrap;align-items:center}
    #trekko-nearby .tn-badge{font-size:.72rem;font-weight:600;padding:.2rem .5rem;border-radius:4px;text-transform:uppercase;letter-spacing:.03em}
    #trekko-nearby .tn-badge-easy{background:#dcfce7;color:#166534}
    #trekko-nearby .tn-badge-moderate{background:#fef9c3;color:#854d0e}
    #trekko-nearby .tn-badge-hard{background:#fee2e2;color:#991b1b}
    #trekko-nearby .tn-badge-expert{background:#f3e8ff;color:#6b21a8}
    #trekko-nearby .tn-dist{font-size:.78rem;color:#64748b}
    @media(max-width:640px){#trekko-nearby{padding:2rem .75rem 2.5rem}#trekko-nearby .tn-grid{grid-template-columns:1fr 1fr}#trekko-nearby .tn-card img{height:110px}}
    @media(max-width:400px){#trekko-nearby .tn-grid{grid-template-columns:1fr}}
  </style>"""

DISCLAIMER_HTML = """\
<section id="trekko-disclaimer" aria-label="Aviso de responsabilidade">
  <div class="td-inner">
    <span class="td-icon" aria-hidden="true">⚠️</span>
    <div class="td-text">
      <p><strong>Aviso de responsabilidade:</strong> Atividades ao ar livre envolvem riscos inerentes. O Trekko fornece informações de referência e não se responsabiliza por acidentes, condições climáticas adversas ou alterações nas trilhas. Sempre verifique as condições locais, informe alguém sobre seu roteiro e, quando possível, contrate um guia profissional certificado.</p>
      <p><a href="/aviso-de-responsabilidade/">Saiba mais</a></p>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------------------
# Per-trail editorial content — Brazilian Portuguese, trail-specific prose
# ---------------------------------------------------------------------------
TRAIL_EDITORIAL = {

"monte-roraima": """\
<h2>O que esperar da trilha</h2>
<p>O Monte Roraima não é uma trilha comum: é uma expedição a um mundo que existia antes dos dinossauros. O tepui — palavra indígena Pemón que significa "casa dos deuses" — ergue-se abruptamente da savana roraimense com paredes verticais de até 400 metros que cercam um planalto onde a geologia, a biologia e o clima operam por regras próprias. Nenhum outro percurso no Brasil combina tanta antiguidade geológica com tanta singularidade ecológica em uma única rota.</p>
<p>A expedição cobre 48 quilômetros de ida e volta pela Tríplice Fronteira entre Brasil, Venezuela e Guiana. O roteiro completo leva de 6 a 8 dias, com acampamentos na base e no próprio topo do tepui. A trilha começa na aldeia indígena Paraitepui, da etnia Pemón, obrigatório ponto de contratação de guia.</p>
<h2>Como é a experiência no percurso</h2>
<p>Os dois primeiros dias atravessam savanas abertas com visão constante do Roraima crescendo no horizonte. A vegetação muda conforme a altitude sobe: a savana dá lugar à floresta de galeria às margens dos rios Tek e Kukenán, que cruzam o caminho e servem como pontos de abastecimento. O terceiro dia traz a "Rampa" — o único acesso ao topo — íngreme, úmida e escorregadia, com trechos onde mãos e pés são necessários.</p>
<p>No alto, a paisagem muda completamente: formações rochosas esculpidas pela chuva em formas abstratas, poças de quartzito com água cristalina, cristais espalhados pelo chão e névoa que entra e sai em minutos. O "Hotel" — uma gruta natural — serve de abrigo para pernoite. As atrações do planalto incluem piscinas naturais, o Labirinto de cânions em miniatura, o ponto triplo das fronteiras e o Cotovelo, com vista de 180° sobre as savanas.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>A Rampa é o único trecho técnico, mas exige atenção absoluta. Após chuvas, as pedras musgosas tornam a progressão vagarosa; o guia conhece os apoios seguros. No topo, a navegação por GPS é pouco confiável pela névoa — o guia Pemón é indispensável. O ponto de tríplice fronteira fica a 3–4 horas de caminhada dentro do planalto.</p>
<h2>Melhor época para visitar</h2>
<p>Outubro a abril oferece dias mais secos e rios navegáveis. A estação chuvosa (maio a setembro) cria corredeiras nos vaus e torna a Rampa ainda mais perigosa. O topo tem microclima próprio: neblina e garoa são frequentes o ano todo e temperaturas à noite podem cair abaixo de 10 °C mesmo no verão. Planeje 7–8 dias para ter margem contra dias de mau tempo na base.</p>
<h2>Dicas de segurança</h2>
<p>O guia é exigência legal dentro do parque e da terra indígena. Leve filtro ou purificador de água — o abastecimento é feito nos rios da rota. Protetor solar de alta proteção é indispensável nas savanas; o sol equatorial é direto e intenso. Botas impermeáveis com bom agarre são o equipamento mais crítico para a Rampa. Leve camadas térmicas: a altitude e a umidade criam frio inesperado.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível especialista. A recomendação é ter completado ao menos uma travessia de três dias com mochila pesada antes de tentar o Roraima. Treino aeróbico consistente por quatro meses é mínimo. A altitude de 2.810 m raramente causa altitude sickness grave, mas a fadiga acumulada em seis dias de expedição é subestimada por caminhantes sem experiência em trekking de longa duração.</p>
<h2>Pontos de água e camping</h2>
<p>Rios Tek e Kukenán são os principais pontos de captação durante a aproximação. No topo, poças em bacias rochosas são abundantes na estação chuvosa. Os guias Pemón preparam alimentação básica para os acampamentos, mas levar liofilizados complementares é recomendado para percursos de mais de seis dias.</p>
<h2>Contexto local: bioma e parque</h2>
<p>O parque nacional fica dentro do território indígena Raposa Serra do Sol. A contratação obrigatória de guia Pemón em Paraitepui sustenta diretamente a economia da comunidade. O tepui abriga espécies endêmicas de insetos, orquídeas e plantas carnívoras que não existem em nenhum outro lugar — não colete nada do ambiente e saia com todo o lixo que entrou.</p>""",

"travessia-petropolis-teresopolis": """\
<h2>O que esperar da trilha</h2>
<p>A Travessia Petrópolis–Teresópolis é a trilha de longo curso mais clássica do Brasil. São 30 quilômetros de caminhada pelo Parque Nacional da Serra dos Órgãos conectando duas cidades que foram capitais do Império — um percurso que mistura história, Mata Atlântica preservada e alguns dos picos mais emblemáticos do Rio de Janeiro. A travessia é um rito de passagem para o caminhante brasileiro.</p>
<p>O percurso é feito em três dias, com pernoite nos Abrigos 1 e 2 (ou 4), estruturas simples mantidas pelo ICMBio com teto, água e banheiros. Não há necessidade de guia obrigatório, mas a orientação de alguém com experiência na travessia é valiosa especialmente para a navegação entre o Abrigo 2 e os Castelos do Açu.</p>
<h2>Como é a experiência no percurso</h2>
<p>O primeiro dia, de Petrópolis ao Abrigo 1, atravessa floresta densa de altitude com trechos razoavelmente exigentes e algumas cachoeiras ao longo do caminho. O segundo dia é o coração da travessia: a subida à Pedra do Sino (2.263 m) e a descida pelos Castelos do Açu, com vistas panorâmicas sobre o litoral fluminense nos dias claros. O Dedo de Deus aparece lateralmente neste trecho — uma aparição que justifica a reputação da Serra dos Órgãos no imaginário do alpinismo brasileiro.</p>
<p>O terceiro dia é mais tranquilo: a descida gradual em direção a Teresópolis atravessa florestas de altitude com trechos de beleza delicada, onde bromélias, orquídeas e samambaias arborescentes cobrem cada centímetro disponível de rocha e galho. A chegada ao portão de Teresópolis tem o gosto particular das grandes travessias concluídas.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho entre o Abrigo 2 e o topo da Pedra do Sino concentra a maior exigência física. A subida final ao Sino tem passagens expostas onde o vento pode ser forte. Após chuvas, os trechos de laje molhada perto dos Castelos do Açu exigem cautela. A navegação entre o Abrigo 2 e Teresópolis tem pontos de bifurcação que confundiram grupos sem GPS carregado previamente.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a outubro corresponde à estação mais seca e é quando a visibilidade nos cumes é melhor. O verão (dezembro a fevereiro) traz chuvas fortes à tarde, trilha encharcada e risco de tempestades no alto. Fins de semana longos superlotam os abrigos — faça reserva com antecedência pelo sistema ICMBio e evite feriados se possível.</p>
<h2>Dicas de segurança</h2>
<p>Reserve os abrigos com antecedência pelo portal do ICMBio — não há camping livre autorizado na travessia. Leve bastões: o impacto nas descidas longas do segundo dia é considerável. Roupa impermeável é indispensável mesmo em época seca, pois a neblina e a garoa são imprevisíveis na Serra dos Órgãos. Inicie o primeiro dia cedo para garantir luz suficiente para instalar no Abrigo 1.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil. Caminhantes com boa condição aeróbica e experiência em trilhas de um dia completo conseguem completar a travessia, mas o acúmulo de desnível em três dias (2.100 m de ganho total) é exigente. Quem nunca dormiu em abrigo de montanha deve planejar um teste de pernoite antes da travessia principal.</p>
<h2>Pontos de água</h2>
<p>Os três abrigos têm abastecimento de água. Ao longo do percurso, riachos e cachoeiras oferecem opções de reabastecimento, mas o tratamento é recomendado. Nos trechos de campo aberto entre o Abrigo 2 e o Sino, não há fontes próximas — saia do abrigo com pelo menos dois litros.</p>""",

"vale-da-lua-e-cachoeiras": """\
<h2>O que esperar da trilha</h2>
<p>A Chapada dos Veadeiros guarda em seu interior uma das paisagens mais peculiares do Brasil: o Vale da Lua, onde o Rio São Miguel esculpiu o quartzito por mais de 600 milhões de anos criando piscinas, corredeiras e relevos que parecem saídos de outro planeta. Combinada com as cachoeiras da região, a trilha de 12 quilômetros mostra o melhor do Cerrado preservado em um único dia de caminhada.</p>
<p>O percurso circular parte da sede do Parque Nacional da Chapada dos Veadeiros em Alto Paraíso de Goiás, passando pelo Vale da Lua, mirantes sobre o Rio São Miguel e chegando às cachoeiras Santa Bárbara e Almécegas — duas das quedas d'água mais bonitas do Planalto Central. A entrada é paga e o número de visitantes por dia é controlado.</p>
<h2>Como é a experiência no percurso</h2>
<p>O Vale da Lua surpreende qualquer caminhante que chega pela primeira vez. As pedras de quartzito, polidas por séculos de correnteza, formam bacias, tubos e plataformas de contornos suaves que a luz do sol torna iridescentes no final da manhã. Nas piscinas, a água fria e transparente convida ao mergulho antes de continuar o percurso. O som do rio acompanha quase todo o trecho.</p>
<p>Após o Vale da Lua, a trilha sobe por Cerrado aberto com vistas para os chapadões ao redor. A vegetação típica — ipês, buriti, murici, lobeira — compõe uma paleta diferente a cada estação. Na época da florada (julho a setembro), os campos ficam amarelos de ipês e a paisagem atinge seu ponto mais fotogênico.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O acesso às piscinas do Vale da Lua exige descida por pedras úmidas — calçado com solado antiderrapante é obrigatório. Nas cachoeiras Santa Bárbara e Almécegas, correntes fortes no período das chuvas tornam o mergulho perigoso; siga a orientação dos fiscais do parque. O sol no Cerrado é intenso das 10h às 15h — leve chapéu, protetor e água além do que parece necessário.</p>
<h2>Melhor época para visitar</h2>
<p>Maio a setembro é a estação seca: água cristalina, trilha seca e temperatura agradável durante o dia. De outubro a abril, as chuvas enchem os rios e tornam as cachoeiras mais volumosas, mas as piscinas ficam turvas e alguns trechos são fechados por segurança. A Chapada tem uma energia mística especialmente intensa no solstício de inverno (junho), quando grupos espirituais se reúnem na região.</p>
<h2>Dicas de segurança</h2>
<p>Mergulhar apenas nas áreas sinalizadas pelo parque — a correnteza nos tubulões do Vale da Lua é traiçoeira mesmo com volume baixo. Não pise nas formações rochosas fora das trilhas marcadas: o quartzito leva séculos para se regenerar. Em dias quentes, a hidratação é crítica; o esforço no Cerrado costuma ser subestimado por visitantes acostumados a trilhas de montanha com sombra constante.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado. A trilha é acessível para famílias com crianças acima de 8 anos e para pessoas com condicionamento físico médio. O desnível de 400 metros é distribuído ao longo dos 12 quilômetros sem trechos muito abruptos. A maior dificuldade é o calor do Cerrado: inicie cedo, preferencialmente antes das 8h, para completar o trecho mais exposto antes do pico do calor.</p>
<h2>Contexto local: bioma e cidade</h2>
<p>Alto Paraíso de Goiás é uma das cidades mais particulares do Brasil interior — polo de espiritualidade, permacultura e turismo de natureza que atrai desde mochileiros jovens até grupos de meditação. A cidade tem boa infraestrutura de pousadas e restaurantes, além de guias credenciados que oferecem trilhas noturnas para observação de estrelas. O Cerrado do parque é Patrimônio Mundial da UNESCO e abriga 30% da biodiversidade brasileira.</p>""",

"pedra-do-bau": """\
<h2>O que esperar da trilha</h2>
<p>A Pedra do Baú é um monólito de granito que domina o horizonte de São Bento do Sapucaí como uma catedral de pedra. Com 1.950 metros de altitude e uma escadaria de 600 degraus cravada na rocha viva, a subida ao topo é uma das experiências mais icônicas da Serra da Mantiqueira paulista — e uma das mais recompensadoras. A vista 360° do cume abrange um horizonte de serras que não se vê de nenhum outro ponto da região.</p>
<p>A trilha de 8 quilômetros parte do Complexo do Baú, propriedade privada com estrutura de visitação, portaria e camping na base. O percurso é linear (ida e volta) e pode ser completado em 4 a 6 horas dependendo do ritmo e do tempo de permanência no topo.</p>
<h2>Como é a experiência no percurso</h2>
<p>O começo da trilha traversa mata de araucária e capões de floresta da Mata Atlântica de altitude, com alguns trechos de campo aberto que já permitem vislumbres da Pedra ao fundo. Conforme a trilha sobe, a vegetação abre e o monólito começa a impor sua escala real — muito maior do que parece nas fotografias.</p>
<p>A escadaria é o momento mais memorável e mais exigente. Os 600 degraus não são uniformes: alguns são curtos, outros exigem passadas largas; alguns são lisos e escorregadios com umidade, outros têm corrimão instalado. A progressão é lenta e o esforço muscular é real. No topo, uma plataforma rochosa exposta com visão de 360° recompensa cada degrau: a Pedra do Bauzinho e Ana Chata ao lado, o vale de São Bento do Sapucaí embaixo, e a Serra da Mantiqueira se espalhando até onde a vista alcança.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho final da escadaria é o mais exposto e, após chuvas, as pedras ficam cobertas por uma película de umidade que as torna escorregadias. A descida é mais traiçoeira do que a subida — concentração total é necessária. Pessoas com acrofobia severa devem avaliar antes de ir: alguns trechos da escadaria têm exposição lateral considerável. A plataforma do topo é exposta ao vento e pode ser fria mesmo em dias quentes no vale.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a outubro é o período mais seguro, com menos chuvas e rocha mais seca. O pôr do sol da Pedra do Baú é um dos mais belos da Mantiqueira — quem planeja o horário de chegada ao topo para as 17h em diante vive uma experiência completamente diferente da caminhada diurna. O complexo tem regras de horário; verifique a operação atualizada antes de ir.</p>
<h2>Dicas de segurança</h2>
<p>Botas de trilha com solado de borracha são obrigatórias — chinelos e tênis de corrida falham na escadaria molhada. Leve bastões para a descida: o impacto nos joelhos em 600 degraus de descida é considerável. Hidratação constante é fundamental; não há fontes de água ao longo da trilha. Crianças pequenas devem ser avaliadas caso a caso — a escadaria exposta não é adequada para menores de 10 anos sem supervisão direta.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil pelo esforço concentrado da escadaria e pela exposição. Caminhantes com experiência em trilhas de montanha e boa condição nas pernas completam o percurso sem grandes dificuldades. Para iniciantes, a escadaria é viável mas exige paciência e descanso nos patamares ao longo do caminho.</p>
<h2>Contexto local: Serra da Mantiqueira</h2>
<p>São Bento do Sapucaí é uma cidade serrana pequena e preservada, com boa rede de pousadas e um calendário de turismo ativo. A Pedra do Baú é parte de um complexo que inclui a Pedra do Bauzinho e trilhas secundárias de menor dificuldade — um destino com opções para diferentes perfis de caminhante em um único fim de semana.</p>""",

"pico-da-bandeira": """\
<h2>O que esperar da trilha</h2>
<p>O Pico da Bandeira, com 2.892 metros de altitude, é o terceiro ponto mais alto do Brasil e o mais alto totalmente fora do domínio amazônico. A subida ao cume é o objetivo mais procurado do Parque Nacional do Caparaó, que fica na divisa entre Minas Gerais e Espírito Santo. O grande atrativo é o nascer do sol do cume: quando o mar de nuvens se estende até o horizonte e o céu muda de preto para dourado, a experiência é de difícil tradução em palavras.</p>
<p>A trilha tem 12 quilômetros de ida e volta e pode ser feita em um único dia (com partida de madrugada) ou em dois dias com pernoite nos campings de Tronqueira ou Terreirão. A segunda opção é mais recomendada: permite aclimatação à altitude e garante presença no cume no amanhecer.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha começa no centro de visitantes em Alto Caparaó, em torno de 1.000 metros de altitude, e sobe progressivamente por Mata Atlântica densa até atingir os campos de altitude. A vegetação muda marcantemente a partir dos 2.200 metros: a floresta se abre em campos rupestres com canelas-de-ema, sempre-vivas e bromélias rasteiras. O vento começa a dominar e a temperatura cai visivelmente.</p>
<p>O Terreirão (2.350 m) é o último camping antes do cume e o ponto de partida para a subida de madrugada. O trecho final, de 2.350 m a 2.892 m, é o mais exigente: solo irregular de rocha e campos rupestres, vento cortante e, muitas vezes, temperatura abaixo de 5 °C. Mas a chegada ao cume antes do sol romper o horizonte — com o mar de nuvens embaixo e as primeiras cores pintando o céu — é uma das experiências mais transformadoras que a natureza brasileira oferece.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho entre o Terreirão e o cume (cerca de 3 km) não tem marcadores muito claros no escuro — leve lanterna frontal e um GPS com a rota carregada. No cume, a exposição ao vento é total e a sensação térmica pode cair muito abaixo da temperatura do ar. Hipotermia é um risco real no inverno mineiro: camadas térmicas e capa impermeável são obrigatórias, não opcionais.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a outubro é o período seco, com céu mais limpo para o nascer do sol e trilha mais acessível. O inverno (junho a agosto) traz as noites mais frias — geada é comum acima de 2.500 m — mas também os céus mais claros e as vistas mais nítidas. O verão chuvoso (dezembro a fevereiro) traz nuvens que frequentemente encobrem o cume no amanhecer, frustrando quem subiu especificamente para a cena do nascer do sol.</p>
<h2>Dicas de segurança</h2>
<p>Aclimatação importa: chegue a Alto Caparaó pelo menos no dia anterior e descanse antes da subida. Leve no mínimo três litros de água — os pontos de reabastecimento são nos campings, não no trecho final. Camadas térmicas de base, fleece e capa impermeável devem ir na mochila mesmo que a previsão indique dia claro. A altitude de 2.892 m é suficiente para causar cefaleia e náusea em pessoas não adaptadas.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil. A distância total não é extrema, mas a altitude e o desnível de 1.000 m tornam o percurso exigente. Caminhantes com experiência em trilhas de montanha de um dia conseguem completar a subida, especialmente se optarem por dois dias com pernoite no Terreirão. A subida noturna sem experiência prévia em trilhas escuras não é recomendada.</p>
<h2>Camping e apoio</h2>
<p>Os campings de Tronqueira e Terreirão são estruturados com sanitários e água potável. O parque exige reserva prévia online e cobra taxa de acampamento separada da entrada. Leve barracas adequadas para ventos fortes: as noites em altitude no Caparaó testam equipamentos de qualidade média.</p>""",

"canion-itaimbezinho": """\
<h2>O que esperar da trilha</h2>
<p>O Cânion Itaimbezinho é a maior fenda geológica da América Latina, com 5,8 quilômetros de extensão e paredões que atingem 720 metros de altura. Localizado no Parque Nacional de Aparados da Serra, na divisa entre Rio Grande do Sul e Santa Catarina, o cânion foi escavado ao longo de milhões de anos pelo Rio do Boi nas rochas de basalto da Serra Geral. A experiência de estar dentro dele — com as paredes se erguendo verticalmente em ambos os lados — é de uma escala que nenhuma fotografia reproduz fielmente.</p>
<p>O parque oferece duas opções de trilha: as trilhas do topo (Vértice e Cotovelo, sem guia obrigatório) e a Trilha do Rio do Boi, que desce ao interior do cânion e exige guia credenciado. A Trilha do Rio do Boi, de 14 quilômetros, é a experiência mais completa e a que recomendamos para quem quer realmente conhecer o cânion por dentro.</p>
<h2>Como é a experiência no percurso</h2>
<p>A descida ao interior do cânion começa em campo aberto de araucárias, a vegetação símbolo do Planalto Sul-brasileiro. Rapidamente a vegetação muda conforme a trilha desce pelas encostas: Mata Atlântica densa substitui os campos, a temperatura cai e o barulho do rio começa a preencher o silêncio. O Rio do Boi é atravessado diversas vezes ao longo do percurso — em épocas de maior volume, as travessias ficam na altura do joelho ou da cintura.</p>
<p>Dentro do cânion, a escala das paredes de basalto é avassaladora. Olhar para cima é ver uma faixa de céu recortada por paredes escuras e verticais. As cachoeiras que despencam do alto — algumas secas na estiagem, outras perenes — adicionam camadas sonoras ao ambiente. O silêncio dentro do cânion, quando o grupo para para ouvir, é de uma profundidade rara.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>As travessias do Rio do Boi exigem sapatos que possam molhar (não use botas impermeáveis que enchem com água). O guia define quais travessias são seguras conforme o volume do dia — na dúvida, confie no guia. Nos meses de verão, a chuva pode subir o nível do rio rapidamente e interromper a trilha antes do previsto.</p>
<h2>Melhor época para visitar</h2>
<p>Março a novembro oferece melhores condições. O verão (dezembro a fevereiro) é a época de maior risco de fechamento por chuvas e rio cheio. O inverno gaúcho traz geada no planalto mas dias secos e claros que mostram o cânion com visibilidade máxima. As cachoeiras do interior têm mais água entre março e maio.</p>
<h2>Dicas de segurança</h2>
<p>A Trilha do Rio do Boi só pode ser feita com guia credenciado pelo parque. Leve calçado para molhar, roupas que sequem rápido e uma muda seca na mochila impermeabilizada. A saída do cânion tem subida exigente; reserva de energia para o retorno é fundamental. Não tente fazer a trilha do Rio do Boi após chuvas fortes — o nível do rio sobe em horas.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado a difícil. A trilha do topo (Vértice/Cotovelo) é acessível para caminhantes iniciantes. A Trilha do Rio do Boi exige condição física para 14 km com terreno irregular e travessias de rio. A emoção compensa em ambos os casos, mas para a experiência completa do cânion, o percurso interior não tem substituto.</p>
<h2>Contexto: araucárias e Serra Geral</h2>
<p>O Planalto da Serra Geral é um dos últimos refúgios significativos da Floresta de Araucária no Brasil. As araucárias centenárias nos campos acima do cânion fazem parte do ecossistema que o parque protege junto com a formação geológica. Cambará do Sul, a cidade mais próxima, é um polo de turismo serrano com boa oferta de pousadas e guias especializados nos dois parques da região (Aparados da Serra e Serra Geral).</p>""",

"trilha-das-praias-rosa-norte-sul": """\
<h2>O que esperar da trilha</h2>
<p>A Praia do Rosa não é apenas uma das praias mais bonitas do Brasil: é um dos raros lugares do mundo onde baleias-franca-do-sul vêm dar à luz a poucos metros da costa. A trilha costeira que conecta a Rosa Norte à Rosa Sul, passando por costões rochosos e mirantes naturais, é o melhor modo de conhecer a paisagem da APA da Baleia Franca — uma área de proteção ambiental criada exatamente para preservar o habitat de reprodução dessas baleias no litoral catarinense.</p>
<p>O percurso de 6 quilômetros é tranquilo, adequado para caminhantes de todos os perfis. A trilha segue pela beira da praia, sobe costões para mirantes e atravessa trechos de vegetação de restinga. Não há taxa de entrada e o percurso não exige guia obrigatório, o que o torna um dos destinos mais acessíveis desta lista.</p>
<h2>Como é a experiência no percurso</h2>
<p>A caminhada começa com a amplitude da praia aberta: areia fina, mar com ondas vindas do Atlântico Sul e, entre julho e novembro, a possibilidade real de avistar baleias-franca na superfície da água a menos de 200 metros da costa. Filhotes recém-nascidos acompanhando as mães são avistamentos frequentes nesse período — um espetáculo que para qualquer caminhante no meio do percurso.</p>
<p>Os costões rochosos que dividem os trechos da praia exigem atenção com o horário da maré — em maré alta, alguns trechos ficam inacessíveis. Os mirantes naturais sobre os costões oferecem ângulos privilegiados para fotografar as baleias e as praias. A Lagoa de Ibiraquera, avistada do mirante mais alto, é outro elemento paisagístico que define a identidade da região.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>Consulte a tábua de marés antes de sair — a travessia de alguns costões é feita apenas na maré baixa. O sol da tarde no verão é muito intenso no trecho aberto da praia; protetor solar e chapéu são fundamentais. Em dias de vento Sul forte, a areia bate na pele com força suficiente para incomodar.</p>
<h2>Melhor época para visitar</h2>
<p>A Praia do Rosa tem dois momentos especiais: o verão austral (dezembro a março) para praias em alta temporada com mar mais calmo, e julho a novembro para o avistamento de baleias. Este segundo período, na contra-estação, tem a vantagem das praias desertas e da paisagem mais selvagem, com o mar mais bravio que no verão. Para quem vai especificamente pelas baleias, agosto e setembro são o pico da temporada.</p>
<h2>Dicas de segurança</h2>
<p>O avistamento de baleias da praia é passivo — não entre no mar para se aproximar de baleias ou filhotes. A legislação do ICMBio proíbe aproximação por embarcações a menos de 200 metros; na praia, o recuo é ainda mais recomendado para não perturbar as fêmeas com filhotes. A trilha dos costões tem trechos sem demarcação clara — siga as marcações naturais e não saia do percurso consolidado.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível fácil. A trilha é adequada para qualquer pessoa com mobilidade razoável. Crianças e idosos completam o percurso sem dificuldade significativa. A única condição é atenção à maré para os trechos de costão. Tênis de caminhada com solado antiderrapante é suficiente — não há necessidade de botas específicas.</p>
<h2>Contexto: APA da Baleia Franca e o Rosa</h2>
<p>A Praia do Rosa é um dos poucos lugares do Brasil onde turismo de massa nunca se instalou de forma definitiva — a topografia isolada e a regulamentação da APA protegeram o lugar de um desenvolvimento predatório. A vila mantém um perfil de pousadas boutique, surf camps e restaurantes de qualidade. A baleia-franca-do-sul (Eubalaena australis) esteve ameaçada de extinção no século XX; a proteção do litoral catarinense foi fundamental para sua recuperação populacional.</p>""",

"travessia-serra-fina": """\
<h2>O que esperar da trilha</h2>
<p>A Travessia da Serra Fina é amplamente considerada a trilha mais difícil do Brasil. São 45 quilômetros pela crista da Serra da Mantiqueira, percorrendo cinco picos acima de 2.700 metros — incluindo a Pedra da Mina (2.798 m), o quarto ponto mais alto do país. A travessia não é apenas fisicamente exigente: é tecnicamente complexa, com trechos de escalada, navegação em crista exposta e condições climáticas que mudam em minutos. É um percurso para montanhistas com experiência consolidada, não para alpinistas iniciantes buscando uma aventura difícil.</p>
<p>O roteiro clássico vai de Passa Quatro (MG) a Itamonte (MG), levando de 4 a 5 dias. A travessia exige guia especializado e experiência prévia em montanhismo de altitude com pernoite em condições expostas.</p>
<h2>Como é a experiência no percurso</h2>
<p>Do primeiro dia, quando a trilha ainda está nos vales e na floresta de araucária, até o segundo dia, quando a crista é atingida e o mundo se resume à linha do horizonte das serras, a mudança de perspectiva é radical. Na crista, a largura do caminho se reduz a metros — de um lado, os vales de Minas; do outro, os vales do interior paulista. O vento é constante e o sol, quando não há neblina, é implacável.</p>
<p>Os picos se sucedem: Pedra da Mina, Pico dos Três Estados, Pedra do Selado, Marins e outros. Cada um tem seu próprio caráter: alguns com trechos de rocha exposta que exigem mãos, outros com campos de altitude que parecem gentis mas escondem buracos e pedras instáveis sob a vegetação rasteira. O camping de altitude — a 2.500 ou 2.700 metros, com barulho do vento e temperatura que pode cair abaixo de zero — é parte essencial da experiência.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho da crista entre a Pedra da Mina e o Pico dos Três Estados concentra os maiores riscos: exposição lateral, rocha molhada e ausência de saída rápida em caso de deterioração do tempo. Tempestades de verão se formam em menos de 30 minutos na crista — o guia deve ser consultado sobre condições meteorológicas na véspera de cada etapa. O Marins, no trecho sul, tem passagens de escalada que requerem uso de mãos de forma constante.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a setembro é o período mais seguro. O verão (dezembro a março) é absolutamente contraindicado pela frequência de tempestades elétricas na crista. Maio e junho oferecem dias mais longos e secos; julho e agosto trazem frio intenso (-5 °C à noite não é raro), o que eleva a exigência de equipamento térmico mas garante os dias mais estáveis.</p>
<h2>Dicas de segurança</h2>
<p>Guia especializado é obrigatório pela dificuldade técnica e pela navegação em crista — não pelo regulamento do parque. Leve equipamento para temperatura negativa independentemente da época. Barracas de quatro estações ou expedição são recomendadas; barracas leves de trilha não resistem ao vento das cristas. Carregue comida para um dia extra além do planejado.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível especialista. A Serra Fina é para montanhistas com pelo menos 5 a 10 travessias de múltiplos dias no currículo, incluindo experiência em altitude acima de 2.500 m. Caminhantes que fizeram apenas trilhas de um dia ou a Petró–Teresópolis não estão prontos para a Serra Fina sem transição por rotas intermediárias como o Pico da Bandeira ou o Circuito do Itatiaia.</p>
<h2>Camping e pontos de apoio</h2>
<p>Os acampamentos são feitos em pontos ao longo da crista — Pedra da Mina, Pico dos Três Estados e Marins são os mais utilizados. Não há infraestrutura (sem banheiros, sem água tratada): toda a água vem de nascentes ao longo da crista que devem ser filtradas. O peso da mochila com equipamento de frio, comida para cinco dias e filtro de água pode facilmente superar 18–20 kg — gestão do peso é parte do planejamento da travessia.</p>""",

"lencois-de-paracuru": """\
<h2>O que esperar da trilha</h2>
<p>Os Lençóis de Paracuru são um campo de dunas costeiras no litoral do Ceará que guarda uma surpresa para quem chega esperando apenas areia: as lagoas interdunares, bolsões de água doce de coloração esverdeada e azulada que aparecem entre as dunas mais altas. A trilha de aproximadamente 10 quilômetros pela APA das Dunas de Paracuru oferece uma caminhada incomum — sem sombra, sem trilha demarcada e com o sol equatorial como companhia constante — mas com recompensas paisagísticas que justificam o esforço.</p>
<p>O percurso é linear, partindo próximo à Praia do Farol e seguindo pela sequência de campos de dunas até o ponto final. A baixa altimetria (ganho acumulado de apenas 59 m) é enganosa: a areia fofa aumenta o esforço de cada passada em 30 a 50% em relação ao mesmo percurso em solo firme.</p>
<h2>Como é a experiência no percurso</h2>
<p>Caminhar em dunas é diferente de qualquer outra trilha. O horizonte muda a cada crista vencida: uma nova duna revela outra lagoa, outro ângulo do litoral, outra perspectiva do oceano. A luz do Ceará — intensa, direta e quase sem filtro — cria sombras dramáticas sobre as formas suaves das dunas que mudam de aparência a cada hora do dia. O final da tarde dourea a areia e transforma o campo de dunas em um cenário de cinema.</p>
<p>As lagoas são o ponto alto do percurso. Algumas são permanentes, outras aparecem apenas no período de maior pluviosidade (março a julho); suas cores variam conforme a vegetação subaquática e a profundidade. Aerogeradores no horizonte marcam a presença da modernidade sem eliminar o caráter selvagem do lugar.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>A navegação sem trilha marcada é o principal desafio: leve GPS com rota carregada ou contrate guia local que conhece os caminhos seguros entre as lagoas. Algumas áreas da APA têm restrições de acesso para proteger a vegetação de fixação das dunas — siga as indicações de guia ou pesquise as zonas de visitação antes de ir. A areia pode atingir 60 °C na superfície em dias de sol forte.</p>
<h2>Melhor época para visitar</h2>
<p>Agosto a dezembro é o período mais indicado: as chuvas do semestre anterior (janeiro a junho) enchem as lagoas, que ainda estão presentes com bom volume. O período de janeiro a junho tem mais lagoas, mas também mais calor úmido e ventos fortes. O verão cearense (dezembro a março) tem temperaturas extremas que tornam a caminhada de 10 km em areia solta muito exigente sem início muito cedo.</p>
<h2>Dicas de segurança</h2>
<p>Hidratação é a prioridade absoluta: leve pelo menos três litros por pessoa. A água das lagoas não é potável sem filtração. Protetor solar FPS 50+ deve ser reaplicado a cada duas horas na exposição total das dunas. Calçado que prenda areia — sandálias de trekking ou tênis fechado de caminhada — reduz o desconforto da areia quente nos pés. Inicie antes das 8h para completar o percurso antes do pico de calor.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado. A distância e o desnível seriam fáceis em solo firme, mas a areia fofa eleva a dificuldade para moderado. Caminhantes com experiência regular em trilhas de um dia completam o percurso sem grandes dificuldades desde que a hidratação e o horário de início sejam respeitados. Crianças menores de 10 anos podem ter dificuldade com a areia — avalie com base na disposição física do grupo.</p>
<h2>Contexto: APA das Dunas e litoral cearense</h2>
<p>Paracuru é uma cidade de pescadores e kite-surfistas a 75 km de Fortaleza, conhecida pelas condições de vento que atraem praticantes de esportes aquáticos de todo o Brasil. A APA das Dunas protege um ecossistema frágil que enfrenta pressão crescente de loteamentos e tráfego de veículos nas dunas — respeitar as zonas de visitação e não usar veículos de tração nas dunas são atitudes fundamentais para a preservação do lugar.</p>""",

"circuito-5-lagos-pedra-do-altar": """\
<h2>O que esperar da trilha</h2>
<p>A Parte Alta do Parque Nacional do Itatiaia é um mundo à parte dentro do parque. Enquanto a Parte Baixa é dominada por cachoeiras e floresta densa, o planalto acima de 1.900 metros oferece campos de altitude abertos, formações rochosas monumentais e, no Circuito dos 5 Lagos, uma sequência de espelhos d'água de montanha que não tem equivalente em outro parque nacional brasileiro. A Pedra do Altar, no ponto mais alto do circuito (2.665 m), adiciona ao roteiro uma subida com vista para as Agulhas Negras e a planície abaixo.</p>
<p>O circuito percorre aproximadamente 9,5 km com 392 metros de ganho de elevação. A altitude inicial já elevada (saída a cerca de 1.900 m) significa que o esforço percebido é maior do que o desnível sugere. O percurso é adequado para um dia completo de caminhada com início cedo.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha começa em campo aberto com visão imediata das serras ao redor. Os cinco lagos surgem em sequência ao longo do percurso — cada um com suas próprias dimensões e humor dependendo da estação: mais cheios e de cor mais profunda no período chuvoso, mais claros e rasos na seca. A borda dos lagos é coberta por vegetação aquática e campos úmidos de altitude.</p>
<p>A subida à Pedra do Altar é o trecho mais exigente do circuito: rocha exposta com trechos onde as mãos são necessárias. No cume, a vista abre para as Agulhas Negras à nordeste, as Prateleiras ao sul e o vale do Itatiaia 700 metros abaixo. Em dias claros, o litoral paulista aparece no horizonte.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho de rocha exposta antes do cume da Pedra do Altar é o mais técnico — úmido após chuva recente, fica mais difícil e exige atenção redobrada. No planalto, a neblina pode entrar em minutos e reduzir visibilidade a poucos metros: tenha a rota carregada no GPS mesmo em dias que parecem estáveis. O vento no planalto pode ser forte e frio mesmo em dias de sol pleno.</p>
<h2>Melhor época para visitar</h2>
<p>Maio a setembro é o período seco com melhores condições. O verão (novembro a março) traz chuvas intensas à tarde e neblina frequente — as vistas do cume ficam comprometidas e o risco de tempestade elétrica na rocha exposta é real. O inverno apresenta temperaturas que podem cair abaixo de zero à noite; se for acampar no Abrigo Rebouças, equipamento térmico robusto é indispensável.</p>
<h2>Dicas de segurança</h2>
<p>A altitude de 2.665 m é suficiente para causar fadiga acelerada em pessoas não aclimatadas — reserve pelo menos uma noite na Parte Alta antes de fazer o circuito. Leve roupa de vento e camada impermeável independentemente da previsão. O sol de altitude queima com intensidade maior que no nível do mar; protetor solar FPS 50 e óculos UV são importantes. Bastões reduzem o impacto na descida da Pedra do Altar.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado para o circuito dos lagos. A subida à Pedra do Altar eleva para moderado a difícil. Caminhantes com experiência em trilhas de dia completo e algum contato com altitude conseguem completar o circuito completo. Para o cume da Pedra do Altar, é recomendável ter experiência prévia com pelo menos uma subida a terreno rochoso exposto.</p>
<h2>Pontos de apoio e camping</h2>
<p>O Abrigo Rebouças, a 2.350 m de altitude, está próximo ao circuito e oferece pernoite básico mediante reserva prévia ao parque. O camping da Parte Alta tem estrutura simples com sanitários. Água dos lagos não é potável sem filtração; leve o suficiente do portão de entrada ou do hotel na Parte Alta.</p>""",

"morro-do-pai-inacio": """\
<h2>O que esperar da trilha</h2>
<p>O Morro do Pai Inácio é o ponto mais fotografado do Parque Nacional da Chapada Diamantina — uma afirmação que se comprova em qualquer dia de fim de semana, quando grupos chegam para assistir o pôr do sol mais famoso do Brasil. O que talvez surpreenda quem visita pela primeira vez é que o mirante está no alto de uma formação de quartzito isolada que domina visualmente toda a extensão do Vale do Capão, criando uma perspectiva de 360° sobre o planalto baiano que não tem paralelo na Chapada.</p>
<p>A trilha tem 5,5 quilômetros e pode ser feita em 2 a 3 horas. É acessível para a maioria dos perfis de caminhante, embora o trecho final de subida na própria rocha exija atenção e calçado adequado. O acesso é gratuito pelo parque.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha começa no estacionamento próximo à BR-242 e sobe gradualmente por campos de quartzito e vegetação de caatinga e campos rupestres. A vista do Pai Inácio aparece rapidamente — a formação rochosa isolada se destaca do horizonte como uma sentinela do planalto. O trecho de aproximação pelo campo aberto tem vistas progressivas do Vale do Capão à esquerda e das serras ao redor.</p>
<p>A subida final é pela própria rocha, com apoios naturais e algumas fissuras que facilitam o progresso. No topo, a plataforma rochosa aberta revela o panorama em todas as direções: o Vale do Capão com a vila de Caeté-Açu embaixo, a Serra do Sincorá ao fundo, o Morro do Camelo ao norte e o oceano de morros que se estende em todas as direções até o horizonte. No pôr do sol, esse oceano de morros ganha tons de laranja e cobre que mudam minuto a minuto.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho de rocha final exige sapato com solado aderente — em dia de chuva ou após chuva recente, as pedras ficam escorregadias e a subida deve ser feita com cuidado redobrado. No topo, a plataforma é exposta e sem grades de proteção: crianças pequenas devem ser supervisionadas próximo às bordas. No pôr do sol, a aglomeração de pessoas no topo é considerável nos fins de semana.</p>
<h2>Melhor época para visitar</h2>
<p>Maio a setembro é a estação seca da Chapada Diamantina, com os dias mais claros e as vistas mais nítidas. O verão (outubro a abril) traz chuvas que às vezes encobrem o mirante no final da tarde, justamente no horário do pôr do sol. Para o nascer do sol — um espetáculo menos popular mas igualmente impressionante — chegue ao estacionamento antes das 5h e suba no escuro com lanterna frontal.</p>
<h2>Dicas de segurança</h2>
<p>Leve água suficiente para a ida e a volta — não há fontes no percurso. O sol da tarde na Chapada é intenso; protetor solar e chapéu são necessários mesmo em dias nublados. Se for no pôr do sol, leve uma camada extra de roupa: o vento no topo fica frio rapidamente após o sol se pôr e a descida é feita no escuro sem lanternas.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado. A trilha é adequada para a maioria dos caminhantes, incluindo famílias com crianças acima de 7–8 anos. O trecho de rocha pode ser intimidador para quem não tem experiência com superfícies expostas, mas não exige habilidades técnicas de escalada. Calçado de trilha ou tênis com boa aderência é suficiente.</p>
<h2>Contexto: Vale do Capão e Chapada Diamantina</h2>
<p>O Vale do Capão, ao pé do Pai Inácio, é um dos polos de turismo alternativo mais ativos do Brasil — uma mistura de trilheiros, artistas, agricultores orgânicos e comunidades que chegaram nos anos 1970 em busca de um modo de vida diferente. A Chapada Diamantina foi declarada parque nacional em 1985 e abrange 152 mil hectares de cerrado, campos rupestres e floresta de galeria, com mais de 400 espécies de aves catalogadas.</p>""",

"cachoeira-da-fumaca": """\
<h2>O que esperar da trilha</h2>
<p>A Cachoeira da Fumaça tem 340 metros de queda livre — a maior queda livre do Brasil — e o efeito que deu seu nome: o volume d'água se transforma em névoa antes de atingir o fundo do cânion, criando uma nuvem permanente que paira sobre a base da cachoeira como fumaça de uma fogueira gigante. Qualquer fotografia que você tenha visto da Fumaça subestima a escala real. Ver um fio d'água desaparecer 340 metros abaixo, transformando-se em névoa antes de chegar ao chão, é uma das experiências visuais mais impactantes disponíveis em trilha no Brasil.</p>
<p>A rota mais acessível é pelo topo, partindo do Vale do Capão (Caeté-Açu) com 12 km de ida e volta. Existe também o acesso pela base, que exige guia obrigatório e desce ao interior do cânion por terreno técnico. As duas rotas revelam perspectivas completamente diferentes da mesma cachoeira.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha pelo topo atravessa campos rupestres abertos com vegetação típica da Chapada: sempre-vivas, bromélias, cipós e espécies endêmicas dos afloramentos rochosos. O percurso sobe progressivamente com vistas crescentes das serras ao redor do Vale do Capão. Há trechos de mata de galeria ao longo dos riachos — a vegetação mais densa que marca a presença de água no relevo árido dos campos rupestres.</p>
<p>O mirante no topo da cachoeira chega de forma quase abrupta: de repente a trilha termina na borda de um precipício e lá embaixo, centenas de metros, a névoa da Fumaça preenche o fundo do cânion. O impacto é imediato e difícil de descrever — a mente demora um momento para processar a escala do que está vendo. Na estação chuvosa, o volume é máximo e a nuvem de névoa se estende para além do cânion.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O mirante do topo não tem grades; respeite os limites de segurança e não se aproxime da borda em terreno molhado. A trilha pelo topo pode ser feita sem guia, mas o acompanhamento é recomendado pelo ICMBio para quem não conhece o percurso. O acesso pela base é tecnicamente exigente com passagens de escalada — guia credenciado é obrigatório e não negociável.</p>
<h2>Melhor época para visitar</h2>
<p>Janeiro a março é o período de maior volume da cachoeira: o efeito de névoa é mais dramático e o impacto visual é máximo. De maio a setembro (seca), o volume diminui e em anos de seca prolongada a cachoeira pode reduzir significativamente sua vazão. Para campos rupestres com florada de sempre-vivas, agosto e setembro são os meses mais coloridos.</p>
<h2>Dicas de segurança</h2>
<p>Na trilha pelo topo, leve água para o dia inteiro — não há fontes confiáveis sem filtração ao longo do caminho. O sol sobre os campos rupestres é intenso: chapéu e protetor solar são indispensáveis. Para a rota pela base, contrate guia com antecedência (a demanda nos meses de alta temporada é alta) e confirme condições de acesso — o nível do Rio Capão pode impedir a travessia após chuvas fortes.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado pelo topo. A rota pelo topo é acessível para caminhantes com experiência básica em trilhas de meio dia. A rota pela base é nível difícil: exige condição física para terreno técnico, travessias de rio e trechos de escalada guiada. Para quem está na Chapada pela primeira vez, o topo oferece uma experiência completa sem as exigências técnicas da rota inferior.</p>
<h2>Contexto: campos rupestres e Chapada Diamantina</h2>
<p>Os campos rupestres da Chapada Diamantina são um dos ecossistemas com maior endemismo florístico do Brasil: centenas de espécies de plantas existem apenas neste tipo de ambiente, adaptadas ao solo pobre dos afloramentos rochosos e às estações secas prolongadas. A Cachoeira da Fumaça está dentro do Parque Nacional da Chapada Diamantina, criado em 1985 para proteger esse patrimônio natural único do sertão baiano.</p>""",

"travessia-lencois-maranhenses": """\
<h2>O que esperar da trilha</h2>
<p>Os Lençóis Maranhenses existem pela combinação improvável de dois fenômenos geográficos: um imenso campo de dunas de quartzo branco acumuladas pelos ventos do Atlântico e um regime de chuvas que, ao contrário do que seria esperado em um ambiente de dunas, enche o espaço entre elas com centenas de lagoas de água doce de coloração turquesa e esmeralda. O resultado é um dos cenários mais surreais do planeta — e a Travessia dos Lençóis Maranhenses, cobrindo 75 km entre Barreirinhas e Atins em 3 a 4 dias, é a forma mais imersiva de conhecê-lo.</p>
<p>Não existe trilha marcada. A navegação é feita pelos guias locais que conhecem a lógica das dunas, os caminhos entre as lagoas e os pontos seguros de travessia do Rio Preguiças. Sem guia, a orientação nos Lençóis é virtualmente impossível — as dunas se parecem umas com as outras e o vento apaga qualquer rastro em horas.</p>
<h2>Como é a experiência no percurso</h2>
<p>Caminhar em dunas é diferente de qualquer outro tipo de trilha: cada passada em areia fofa exige mais esforço do que parece, os músculos das panturrilhas e tornozelos trabalham de forma incomum e o ritmo de avanço é menor do que a distância plana sugeriria. Apesar disso — ou por causa disso — a caminhada tem um aspecto meditativo: o branco das dunas, o silêncio rompido apenas pelo vento e o contraste das lagoas turquesas criam um ambiente que desacelera o pensamento.</p>
<p>O acampamento nas dunas ao lado de uma lagoa, sob um céu repleto de estrelas sem nenhuma poluição luminosa por quilômetros em todas as direções, é um dos momentos mais memoráveis da travessia. O contraste entre o branco absoluto das dunas durante o dia e a imensidão do céu noturno é algo que os caminhantes descrevem como transformador.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>A gestão de água é crítica: nem todas as lagoas são potáveis sem filtração, e o guia indica quais fontes são adequadas para consumo. A areia pode atingir temperatura de superfície acima de 60 °C no meio do dia — caminhar nas horas centrais sem calçado adequado causa queimaduras. A travessia do Rio Preguiças, dependendo da época, pode exigir barco ou canoa local.</p>
<h2>Melhor época para visitar</h2>
<p>Janeiro a julho é o período com lagoas cheias — o pico é de março a junho, quando as lagoas atingem volume máximo após as chuvas do verão maranhense. De agosto a dezembro, as lagoas progressivamente desaparecem e a travessia perde boa parte do elemento mais icônico do percurso. Há anos em que lagoas ainda estão presentes em agosto e setembro; confirme condições atuais com operadores locais antes de planejar a viagem.</p>
<h2>Dicas de segurança</h2>
<p>O guia é obrigatório pela regulamentação do parque e pela necessidade prática. Leve protetor solar FPS 50+ para reaplicação frequente — a areia reflete a radiação solar e aumenta a exposição total. Calçado de duna (sapatilha leve ou sandália de trekking) é mais adequado do que botas pesadas. Carregue filtro de água e reserve capacidade extra para trechos entre lagoas.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil pela distância (75 km em 3–4 dias) e pela exigência física da areia fofa. Caminhantes sem experiência em múltiplos dias de caminhada devem fazer uma versão abreviada antes de tentar a travessia completa. Fisicamente, o maior desafio não é o desnível (praticamente nulo) mas a fadiga muscular acumulada de caminhar em areia por dias consecutivos.</p>
<h2>Camping e apoio</h2>
<p>Os acampamentos são feitos nas dunas próximas às lagoas ou no vilarejo de Queimada dos Britos, a meio caminho. Em Atins, pousadas simples recebem os caminhantes ao final da travessia. Barreirinhas tem boa infraestrutura de hotéis e restaurantes para a noite anterior à largada. Os guias locais geralmente incluem alimentação no pacote de travessia.</p>""",

"morro-dois-irmaos": """\
<h2>O que esperar da trilha</h2>
<p>O Morro Dois Irmãos é a trilha urbana mais dramática do Rio de Janeiro. A subida começa na comunidade do Vidigal, encravada entre o asfalto da Zona Sul e as formações rochosas da Serra da Carioca, e termina em uma plataforma rochosa de 537 metros com uma das vistas mais fotogênicas do Brasil: Ipanema e Leblon abertas abaixo, o Pão de Açúcar ao norte, o Cristo sobre o Corcovado à esquerda e o Atlântico se estendendo ao sul. Tudo em um único enquadramento impossível que só existe desse ângulo.</p>
<p>A trilha tem cerca de 5 km e um desnível de 537 metros — mais exigente do que parece para uma caminhada urbana. O percurso começa no acesso oficial pela comunidade do Vidigal, onde guias locais organizam grupos regularmente. Não há taxa de entrada, mas a contratação de guia local é recomendada e apoia diretamente a economia da comunidade.</p>
<h2>Como é a experiência no percurso</h2>
<p>A subida pelo Vidigal é em si uma imersão em uma outra faceta do Rio de Janeiro: becos, escadarias e vielas que sobem pela encosta com vistas progressivas sobre o mar. A comunidade recebe caminhantes com familiaridade — o turismo é parte da vida econômica do Vidigal há anos. Conforme a trilha sobe para além da área habitada, a vegetação de Mata Atlântica toma conta e os sons da cidade vão ficando embaixo.</p>
<p>O trecho final na rocha exposta tem passagens que exigem mãos e pés. O cume não é uma plataforma ampla — é uma série de lajes rochosas com boas opções de posicionamento para fotografia. A vista é imediata e avassaladora em todas as direções: a Lagoa Rodrigo de Freitas à esquerda, as praias de Ipanema e Leblon à frente, o oceano Atlântico e as ilhas Cagarras no horizonte sul.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho de rocha exposta antes do cume é escorregadio após chuva recente. A rocha úmida combina mal com calçado de sola lisa — tênis de trilha ou tênis com boa aderência são necessários. No cume, a ausência de grades de proteção exige atenção, especialmente com crianças. O horário de alta demanda (fins de semana, pôr do sol) cria fila no trecho final de rocha — paciência e espaçamento entre grupos são necessários.</p>
<h2>Melhor época para visitar</h2>
<p>Maio a outubro oferece as condições mais estáveis: menos chuvas, rocha mais seca e visibilidade mais consistente para o horizonte. O verão (dezembro a março) tem risco maior de chuvas passageiras e névoa que podem encobrir a vista do cume. O amanhecer (chegada ao cume antes das 6h30) oferece uma perspectiva diferente do pôr do sol — luz dourada horizontal e, com sorte, o mar de nuvens preso nos vales da Tijuca enquanto o Rio acorda.</p>
<h2>Dicas de segurança</h2>
<p>Informe-se sobre o acesso atual pelo Vidigal antes de ir — o percurso oficial pode ter alterações. Leve água suficiente para a subida e descida. Não faça a trilha em dia de chuva ou imediatamente após chuvas — a rocha molhada no trecho final é o maior risco da trilha. Deixe objetos de valor no hotel; leve apenas o necessário para a caminhada.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado. A trilha não é tecnicamente difícil, mas o desnível de 537 metros em 2,5 km de subida é exigente para pessoas sem condicionamento regular. Quem faz caminhadas urbanas de uma hora por semana vai sentir as pernas no dia seguinte. Calçado adequado é o fator mais importante — o trecho de rocha exposta com sapato inadequado transforma a trilha de moderada para arriscada.</p>
<h2>Contexto: Vidigal e a cidade</h2>
<p>O Vidigal é uma das comunidades mais organizadas para o turismo no Rio de Janeiro, com hostels, restaurantes e bares no mirante inferior que oferecem uma perspectiva única da cidade. Contratar guia local não é apenas uma questão de segurança — é uma forma de distribuir o benefício econômico do turismo para quem vive e conhece o morro. O Parque Nacional da Tijuca, que cobre 32 km² no coração urbano do Rio, é o maior parque nacional urbano do mundo e o contexto ambiental em que trilhas como o Dois Irmãos existem.</p>""",

"fernando-de-noronha-baia-do-sancho": """\
<h2>O que esperar da trilha</h2>
<p>Chegar à Baía do Sancho de barco é uma opção turística. Chegar a pé, descendo pelas frestas de rocha vulcânica que cortam o basalto da costa noronhense, é outra experiência inteiramente. A trilha até a praia eleita repetidamente a mais bela do mundo pelo TripAdvisor não é longa — cerca de 3,5 km — mas é memorável pelo acesso: escadas de madeira instaladas dentro de fissuras naturais no basalto, paredes rochosas a centímetros de cada lado, o barulho do mar chegando de baixo antes de a praia aparecer. O percurso combina aventura e paraíso em uma rota que não tem paralelo no Brasil.</p>
<p>O acesso é controlado pelo Parque Nacional Marinho de Fernando de Noronha. A taxa de visitação do parque é obrigatória e o número de visitantes por dia é limitado. Guia credenciado é exigência do parque.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha começa próxima ao Mirante dos Golfinhos, um dos pontos de avistamento de golfinhos-nariz-de-garrafa mais confiáveis do Brasil, onde a entrada de centenas de golfinhos na baía ao amanhecer é um espetáculo diário. O percurso desce pela encosta da ilha com visão crescente do Mar de Fora — o oceano Atlântico aberto, com sua coloração profunda de azul-cobalto — até atingir o acesso das frestas.</p>
<p>A descida pelas frestas é o momento mais memorável: o basalto, rocha vulcânica solidificada há milhões de anos, rachou criando corredores estreitos por onde a erosão instalou escadas. A descida é lenta, excitante e exige atenção com as mãos. Na base, a Baía do Sancho se abre com sua areia branca e água de clareza excepcional, em tons que variam do turquesa ao azul profundo dependendo da hora e da incidência de luz.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>As escadas nas frestas podem estar molhadas e escorregadias — o spray do mar e a umidade do basalto são constantes. Calçado fechado com boa aderência é obrigatório; sandálias e havaianas são inadequadas. Na praia, a areia é fina e o sol de Fernando de Noronha — a apenas 4 graus de latitude sul — queima com intensidade que surpreende mesmo quem está acostumado com praia. Protetor solar biodegradável é obrigatório dentro do parque marinho; os protetores com oxibenzona são proibidos para proteger os corais.</p>
<h2>Melhor época para visitar</h2>
<p>Setembro a março é o período de menor agitação do mar e melhor visibilidade para snorkeling. O Mar de Dentro, que banha a Baía do Sancho, tem mergulho incrível com tartarugas marinhas (Chelonia mydas), arraias e cardumes coloridos. De abril a agosto, o vento e o swell do Sul aumentam, mas a ilha tem menos turistas e preços mais acessíveis — uma troca interessante para quem não está focado exclusivamente no snorkeling.</p>
<h2>Dicas de segurança e regulamentos do parque</h2>
<p>Respeite rigorosamente os limites de visitantes por dia — não tente entrar na baía fora do horário ou sem taxa paga. O parque marinho tem fiscalização ativa e multas elevadas. Não pise nos corais nem nos animais marinhos. Saída de areia e pedras da ilha é crime ambiental. Todo lixo sai com o visitante. As tartarugas que sobem nas praias à noite para desovar são protegidas — não as iluminem com lanternas ou flashes.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível fácil a moderado. A distância curta e o desnível modesto tornam a trilha acessível para a maioria dos visitantes. A descida pelas frestas pode ser intimidadora para pessoas com claustrofobia ou acrofobia, mas não é tecnicamente difícil. O maior desafio físico é a subida de volta — especialmente depois de algumas horas na praia sob o sol de Noronha.</p>
<h2>Contexto: arquipélago e conservação</h2>
<p>Fernando de Noronha é um arquipélago vulcânico de 26 ilhas e ilhotas a 350 km do litoral pernambucano. É Patrimônio Natural da Humanidade pela UNESCO e uma das áreas marinhas protegidas mais importantes do Atlântico Sul. A economia local depende inteiramente do turismo controlado — a taxa ambiental (TAXA de Preservação Ambiental, TPA) aumenta progressivamente a cada dia de permanência na ilha para limitar o fluxo de visitantes e financiar a conservação.</p>""",

"canion-fortaleza": """\
<h2>O que esperar da trilha</h2>
<p>O Cânion Fortaleza é o segundo maior cânion do Brasil — mas é frequentemente o primeiro em surpresa para quem chega sem expectativas altas. Enquanto o vizinho Itaimbezinho concentra a maioria dos visitantes dos Aparados da Serra, o Fortaleza permanece mais tranquilo, o que significa uma imersão mais silenciosa dentro de paredes de basalto que atingem 900 metros de altura e 7 quilômetros de extensão. A Cascata do Avencal, escondida dentro da garganta, aguarda aqueles que chegam até o fundo.</p>
<p>A trilha mais completa percorre cerca de 12 km entre o mirante superior e o interior do cânion, saindo de Praia Grande (SC) com acesso pelo Parque Nacional de Aparados da Serra e Serra Geral. O guia é obrigatório para o acesso ao interior do cânion.</p>
<h2>Como é a experiência no percurso</h2>
<p>O percurso começa no planalto, onde campos de altitude com araucárias centenárias dominam a paisagem. Conforme a trilha avança em direção à borda do cânion, o corte geológico vai se revelando: primeiro como uma linha distante no campo, depois como uma fenda que cresce até tomar proporções que simplesmente não cabem no campo visual. O contraste entre o planalto aberto e horizontal e a verticalidade das paredes do cânion é o impacto visual mais imediato do Fortaleza.</p>
<p>A descida pela borda do cânion leva ao interior da garganta, onde a Mata Atlântica de encosta substitui os campos de altitude. O microclima muda completamente: mais úmido, mais fresco, com a vegetação adensada e o barulho do Rio Josafaz acompanhando o percurso. A Cascata do Avencal se anuncia pelo barulho antes de aparecer — uma queda de água que despeja dentro do próprio cânion, em uma parede lateral de basalto coberta de musgos e avencas.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>A descida ao interior do cânion tem trechos de barro escorregadio e raízes expostas — calçado de trilha com bom agarre é indispensável. Em dias de chuva ou imediatamente após, o acesso ao interior pode ser fechado por risco de deslizamento; confirme condições com o parque antes de partir de Praia Grande. O retorno pelo mesmo caminho tem subida exigente — reserve energia.</p>
<h2>Melhor época para visitar</h2>
<p>Setembro a março é o período com melhores condições de acesso ao interior do cânion. O inverno gaúcho-catarinense (junho a agosto) traz frio intenso no planalto e eventuais geadas que cobrem os campos de araucária com uma camada branca — visualmente espetacular, mas que torna o percurso mais exigente e lento. As cachoeiras dentro do cânion têm mais volume de março a junho.</p>
<h2>Dicas de segurança</h2>
<p>A trilha ao interior exige guia obrigatório — não por burocracia, mas porque a orientação dentro do cânion é genuinamente difícil sem referências conhecidas. Leve roupas impermeáveis mesmo em dia sem previsão de chuva: o microclima do interior do cânion é diferente do planalto e a névoa pode molhar completamente sem chuva declarada. Botas impermeáveis são a escolha mais segura para o trecho de interior.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado para as trilhas do topo (sem guia, vista do planalto). O acesso ao interior com descida à cascata eleva para moderado a difícil, pela exigência física do retorno e pelas condições de terreno. O Cânion Fortaleza é uma boa opção para quem já visitou o Itaimbezinho e quer uma perspectiva mais imersiva e mais tranquila da mesma formação geológica.</p>
<h2>Contexto: basalto, Serra Geral e araucárias</h2>
<p>Os cânions dos Aparados da Serra foram formados pelo derramamento de lava basáltica que criou o Planalto Meridional durante o Cretáceo. Erosão fluvial ao longo de dezenas de milhões de anos cortou as rochas criando as gargantas. O Parque Nacional de Serra Geral, criado em 1992 para complementar o Parque de Aparados da Serra, protege a área de entorno dos cânions, incluindo a Floresta de Araucária — um dos ecossistemas mais ameaçados do Sul do Brasil.</p>""",

"pedra-do-sino": """\
<h2>O que esperar da trilha</h2>
<p>A Pedra do Sino é o ponto culminante da Serra dos Órgãos, a 2.263 metros de altitude no Parque Nacional homônimo. É também uma das trilhas mais longas e exigentes do Rio de Janeiro: 14 quilômetros com 1.650 metros de desnível acumulado, que levam de 8 a 10 horas dependendo do ritmo. O percurso passa ao lado do Dedo de Deus — o pico de quartzito em forma de dedo que virou símbolo da serrania fluminense — e termina em um cume com vista para o oceano Atlântico e a Serra da Mantiqueira.</p>
<p>A trilha é iniciada em Teresópolis, pela entrada do Parque Nacional da Serra dos Órgãos (PARNASO). Não há guia obrigatório, mas a trilha é longa e requer planejamento sério. A opção de pernoite no Abrigo da Pedra do Sino permite subir no segundo dia ao amanhecer com o mar de nuvens.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha começa na Mata Atlântica densa de altitude, onde a umidade e a sombra criam um ambiente de floresta típico da Serra dos Órgãos. A vegetação vai abrindo progressivamente conforme a altitude sobe: samambaias arborescentes dão lugar a campos de altitude com bromélias e musgos que cobrem cada pedra disponível. O Dedo de Deus aparece em perspectiva lateral em determinado ponto do caminho — uma das visões mais icônicas do montanhismo brasileiro.</p>
<p>O trecho final, acima de 2.000 metros, é em campo aberto e rocha exposta. O vento pode ser intenso e a sensação térmica cai consideravelmente. O cume da Pedra do Sino é uma plataforma rochosa com exposição total em todas as direções. Nos dias claros, a Baía de Guanabara aparece ao sul e a Serra da Mantiqueira se perfila no horizonte norte.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho entre 1.800 m e o cume é o mais exposto ao vento e ao frio. A neblina pode entrar rapidamente — tenha a rota salva no GPS. Os riachos ao longo do percurso têm água disponível, mas devem ser filtrados. A descida pelo mesmo caminho tem impacto considerável nos joelhos — bastões são altamente recomendados para o retorno.</p>
<h2>Melhor época para visitar</h2>
<p>Maio a outubro é o período mais seguro, com menos chuvas e melhor visibilidade. O verão (dezembro a março) traz tempestades intensas à tarde que podem pegar caminhantes no trecho exposto do cume — a saída deve ser antes das 13h. Para o mar de nuvens no amanhecer, a opção de pernoite no Abrigo é necessária: chegue ao abrigo no final da tarde e suba os últimos 3 km ao cume antes do sol nascer.</p>
<h2>Dicas de segurança</h2>
<p>Reserve o Abrigo da Pedra do Sino com antecedência pelo portal do PARNASO — a capacidade é limitada e os fins de semana esgotam rapidamente. Leve camadas térmicas e impermeável para a subida: mesmo em meses secos, o vento e a garoa no cume criam condições de frio inesperadas para quem saiu com tempo quente na cidade. Inicie cedo: a trilha de 14 km não permite começos tardios sem risco de escuridão na descida.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil. O desnível de 1.650 m em trilha de 14 km é uma das subidas mais exigentes do Rio de Janeiro sem necessidade de técnica de escalada. Caminhantes que completaram a Travessia Petrópolis–Teresópolis estão bem preparados para a Pedra do Sino. Para quem está fazendo a primeira trilha de dia longo, a Pedra do Sino não é o começo recomendado.</p>
<h2>Contexto: Serra dos Órgãos e PARNASO</h2>
<p>O Parque Nacional da Serra dos Órgãos foi criado em 1939 — é um dos parques nacionais mais antigos do Brasil. Os picos da Serra dos Órgãos (Dedo de Deus, Pedra do Sino, Agulhas do Diabo) foram o berço do montanhismo brasileiro organizado no século XX. O parque protege um dos trechos mais preservados de Mata Atlântica de altitude no Sudeste, com alta endemismo de epífitas, anfíbios e aves.</p>""",

"chapada-dos-guimaraes-circuito-cachoeiras": """\
<h2>O que esperar da trilha</h2>
<p>A Chapada dos Guimarães é um planalto de arenito e quartzito que se eleva abruptamente 800 metros acima da planície pantaneira no centro de Mato Grosso. O Circuito das Cachoeiras reúne em 18 quilômetros os pontos mais icônicos do Parque Nacional: o Véu de Noiva com seus 86 metros de queda livre sobre arenito vermelho, a Piscina do Amor em anfiteatro rochoso de água turquesa, o Geodésico do Centro Geográfico do Brasil e, no final, a vista do mirante sobre o Pantanal. É um roteiro que combina espetáculo hídrico, curiosidade geográfica e um dos panoramas mais impactantes do Centro-Oeste.</p>
<p>A trilha circular parte da sede do parque e tem guia obrigatório. A entrada é paga e sujeita a atualização — confirme valores atuais no site do ICMBio antes da visita.</p>
<h2>Como é a experiência no percurso</h2>
<p>O Véu de Noiva é o primeiro grande impacto: a cachoeira despeja sobre uma parede de arenito vermelho em uma ravina coberta de vegetação, com o mirante frontal permitindo ver a queda em toda a extensão. O arenito muda de cor conforme a luz: laranja pela manhã, vermelho-vivo no meio do dia, dourado no final da tarde.</p>
<p>A Piscina do Amor, em um anfiteatro rochoso mais adiante, é o ponto de pausa obrigatório. A água turquesa em uma bacia de pedra, cercada por paredes curvas de arenito, cria um ambiente de privacidade visual inesperada no meio da chapada. O mergulho na Piscina é o momento mais procurado do circuito.</p>
<p>O Geodésico marca o centro geográfico do Brasil — um marco físico de algo que normalmente existe apenas como conceito. E o mirante do Planalto, no trecho final, abre uma vista de 180 graus sobre a planície pantaneira: a chapada termina abruptamente e o Pantanal se estende até o horizonte como um mapa sem fronteiras. A diferença de altitude entre o planalto e a planície — 800 metros — é visível com clareza.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho de maior exigência física é entre a Piscina do Amor e o mirante do Planalto, com subida em terreno de arenito solto. O sol no cerrado mato-grossense é particularmente intenso — o circuito deve ser iniciado cedo para completar os trechos mais expostos antes das 11h. Na estação seca (maio a setembro), o Véu de Noiva tem menos volume mas ainda é belo; na estação chuvosa (outubro a abril), o volume aumenta mas alguns trechos da trilha ficam enlameados.</p>
<h2>Melhor época para visitar</h2>
<p>Maio a setembro é o período mais confortável pelo calor mais suave e trilha mais seca. O período chuvoso tem cachoeiras mais volumosas, mas temperaturas mais altas e trechos de trilha embarrados. O inverno mato-grossense (junho a agosto) tem temperaturas amenas e umidade baixa — as condições mais favoráveis para um circuito longo.</p>
<h2>Dicas de segurança</h2>
<p>Leve no mínimo dois litros de água por pessoa — o calor do Centro-Oeste acelera a desidratação. O guia é obrigatório e orienta nos pontos de risco do percurso. Protetor solar FPS 50+ e chapéu são indispensáveis nos trechos abertos. Calçado de trilha é necessário para o arenito solto e os trechos de laje molhada nas cachoeiras.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado. O circuito completo de 18 km é adequado para caminhantes com condicionamento regular. A distância pode ser reduzida fazendo apenas os primeiros atrativos (Véu de Noiva e Piscina do Amor) e retornando, em um percurso de cerca de 10 km. Para o mirante do Planalto e a vista completa, o circuito inteiro é necessário.</p>
<h2>Contexto: Chapada dos Guimarães e o Centro-Oeste</h2>
<p>A Chapada dos Guimarães fica a apenas 65 km de Cuiabá, a capital do Mato Grosso — o que a torna um dos destinos de ecoturismo mais acessíveis do Centro-Oeste. O Parque Nacional foi criado em 1989 e abrange 33 mil hectares de cerrado, matas ciliares e formações rochosas que representam o limite entre o Cerrado e o Pantanal. A cidade de Chapada dos Guimarães tem infraestrutura completa de hotéis e pousadas para qualquer padrão.</p>""",

"pico-das-agulhas-negras": """\
<h2>O que esperar da trilha</h2>
<p>O Pico das Agulhas Negras é o segundo ponto mais alto do Brasil, com 2.791 metros no Parque Nacional do Itatiaia. A trilha para o cume parte da Parte Alta do parque em uma altitude já elevada — cerca de 1.900 metros — e atravessa a paisagem mais característica da Serra da Mantiqueira: campos de altitude abertos, afloramentos rochosos de origem vulcânica e vegetação rasteira de campos rupestres que cobre o terreno irregular. É uma das subidas mais acessíveis a um dos picos mais altos do Brasil, o que explica a popularidade crescente da montanha.</p>
<p>O percurso tem cerca de 12 km com 1.200 metros de desnível acumulado. A trilha é classificada como difícil pelo trecho final exposto, mas não exige técnica de escalada — apenas atenção e boa condição física. O trecho culminante usa as mãos para progredir pela rocha.</p>
<h2>Como é a experiência no percurso</h2>
<p>A saída da Parte Alta já coloca o caminhante em altitude e paisagem aberta. Os primeiros quilômetros pelo planalto do Itatiaia revelam o caráter único desta região: rocha vulcânica com formas irregulares, lagoas de altitude, campos abertos com vento constante e visão das Agulhas Negras crescendo no horizonte conforme a trilha avança.</p>
<p>O Lago Guarda Mor, no percurso, é um dos pontos mais fotogênicos: um espelho d'água de altitude com as formações rochosas refletidas na superfície calma. Mais adiante, a trilha sobe em direção ao cume com trechos cada vez mais expostos. O trecho final, na rocha escura (fonólito e sienito — rochas vulcânicas que dão o tom escuro e o nome "Agulhas Negras"), exige progressão lenta com apoio das mãos.</p>
<p>No cume, a vista é de 360° sobre a Mantiqueira: as Prateleiras ao leste, a Pedra da Mina ao norte, o litoral paulista e a Baía de Ilha Grande no horizonte sul em dias excepcionalmente claros. O mar de nuvens ao amanhecer — quando funciona — é o espetáculo mais celebrado da montanha.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho final de rocha exposta acima de 2.600 m é o mais técnico: mãos necessárias, rocha escorregadia quando molhada, exposição ao vento. Tempestades de altitude se formam muito rapidamente no Itatiaia — a saída do cume deve ser feita antes das 14h em qualquer época. O vento no cume pode criar sensação térmica abaixo de 0 °C mesmo em dias de sol.</p>
<h2>Melhor época para visitar</h2>
<p>Maio a setembro é o período mais estável. O verão (novembro a março) traz tempestades intensas à tarde — subidas de madrugada com chegada ao cume antes das 9h são a estratégia dos frequentadores experientes nessa época. O inverno tem as temperaturas mais baixas (geada no cume é comum em julho), mas os dias mais claros e os mares de nuvens mais consistentes ao amanhecer.</p>
<h2>Dicas de segurança</h2>
<p>Leve roupa impermeável e camadas térmicas independentemente da previsão. O clima de altitude muda em minutos. Inicie a trilha antes das 6h para ter margem de tempo segura antes das tempestades da tarde. Leve GPS com a rota salva: a neblina pode encobrir a trilha rapidamente no trecho de campo aberto. Não force a subida ao cume se o céu estiver fechando — a relâmpagos são frequentes na rocha exposta.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil. O desnível total e o trecho técnico do cume colocam a trilha fora do alcance de caminhantes com pouca experiência. Quem completou o Pico da Bandeira ou a Pedra do Sino está preparado. Para o pernoite no Abrigo Massena, condições de acampamento de altitude são necessárias — o frio noturno pode ser intenso e barracas de qualidade são fundamentais.</p>
<h2>Pontos de apoio e camping</h2>
<p>O Abrigo Massena, a cerca de 2.350 m, é o ponto de acampamento mais próximo do cume e requer reserva prévia ao parque. O Camping da Parte Alta, na altitude de saída da trilha, tem estrutura mais completa com sanitários. O Lago Guarda Mor, no percurso, tem água que deve ser filtrada antes do consumo.</p>""",

"travessia-vale-do-pati": """\
<h2>O que esperar da trilha</h2>
<p>O Vale do Pati é considerado por muitos o mais belo vale da Chapada Diamantina — e um dos mais belos do Brasil. Encaixado entre serras que superam 1.630 metros, o vale permanece isolado do asfalto e só pode ser acessado a pé, o que preservou tanto a paisagem quanto a comunidade de moradores que habitam suas encostas há gerações. A Travessia do Vale do Pati, de 60 quilômetros em 4 a 5 dias, é o trekking mais épico da Bahia e um dos roteiros de referência do montanhismo nordestino.</p>
<p>A travessia conecta Andaraí ao vilarejo de Guiné (ou ao Mucugezinho), com variações de roteiro que dependem do guia e das condições climáticas. O guia é obrigatório tanto por regulamentação do parque quanto por necessidade prática — sem conhecimento local, navegar o vale é virtualmente impossível.</p>
<h2>Como é a experiência no percurso</h2>
<p>A entrada no vale a partir de Andaraí desce por encosta coberta de caatinga e mata de galeria, com o vale se abrindo gradualmente como um anfiteatro de granito e quartzito. Os primeiros avistamentos das serras circundantes — com suas paredes verticais e os campos rupestres no topo — estabelecem a escala do que está por vir.</p>
<p>Dentro do vale, o ritmo muda. A planície aberta com palmeiras buriti, o Rio Pati e seus córregos tributários, e as casas de pedra das famílias que habitam o vale criam um ambiente de outro tempo. As pousadas comunitárias (onde as famílias do vale hospedam os caminhantes em quartos simples e servem refeições com o que cultivam) são parte fundamental da experiência — não apenas abrigo, mas ponto de contato com uma forma de vida que a modernidade não alcançou completamente.</p>
<p>A Cachoeira do Buracão, com 80 metros de queda, é o espetáculo hídrico mais dramático da travessia: a água precipita em um anfiteatro rochoso de paredes altas que abriga também uma praia de areia branca ao fundo. O céu noturno do vale — longe de qualquer poluição luminosa — é de uma limpidez difícil de descrever para quem vive em cidade.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>As travessias de rios são frequentes e podem estar na altura da cintura no período chuvoso — calçado impermeável é essencial. O percurso tem trechos de subida consideráveis entre os pontos de hospedagem e os mirantes nas serras; reserve energia para essas variações fora do fundo de vale. O guia conhece o nível dos rios e pode ajustar o roteiro conforme as condições.</p>
<h2>Melhor época para visitar</h2>
<p>Maio a setembro é o período ideal: rios em nível navegável, clima ameno e trilha mais seca. O verão (novembro a março) tem chuvas frequentes que enchem os rios e tornam algumas travessias perigosas. Nos meses mais secos (agosto e setembro), o Rio Pati tem volume menor, o que facilita as travessias mas reduz as cachoeiras. O céu estrelado de inverno (junho a agosto) é o mais espetacular.</p>
<h2>Dicas de segurança</h2>
<p>A mochila deve ser leve — cada quilo a mais cobra seu preço em 60 km de terreno variado. Calçado impermeável é a escolha mais importante do equipamento. As pousadas comunitárias incluem refeições, mas confirme com o guia o que é necessário carregar de alimentos complementares. Leve dinheiro em espécie: não há nenhum serviço eletrônico de pagamento no vale.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil. A distância de 60 km em 4–5 dias com mochila e terreno variado exige condicionamento físico sólido e experiência prévia em trekking de múltiplos dias. Caminhantes que completaram a Travessia Petrópolis–Teresópolis ou o Pico da Bandeira com pernoite têm base adequada para o Pati. Para quem não tem essa experiência, uma versão de 2–3 dias dentro do vale (sem a travessia completa) é uma alternativa excelente.</p>
<h2>Comunidade e turismo responsável</h2>
<p>O turismo no Vale do Pati é uma das formas mais bem-sucedidas de turismo de base comunitária no Brasil. As famílias do vale construíram suas pousadas com o apoio de ONGs e mantêm a hospedagem com recursos próprios. Contratar guia local, hospedar-se nas pousadas comunitárias e pagar os valores pedidos sem barganhar são as formas concretas de garantir que o vale continue habitado e preservado para as próximas gerações.</p>""",

"trilha-cotovelo-vertice-itaimbezinho-cambara-do-sul-rs": """\
<h2>Como é a Trilha do Cotovelo e Vértice</h2>
<p>A Trilha do Cotovelo e Vértice é uma das melhores portas de entrada para quem quer conhecer os cânions de Cambará do Sul sem encarar uma caminhada técnica. O percurso acontece na parte alta do Cânion Itaimbezinho, em área estruturada do Parque Nacional de Aparados da Serra, e entrega o que muita gente busca na primeira visita aos Aparados: mirantes amplos, paredões gigantes, araucárias, cachoeiras e aquela sensação de estar diante de uma paisagem que não cabe na foto.</p>
<p>A experiência combinada soma cerca de 7,5 a 8 km. O Vértice é o trecho mais curto e contemplativo, com mirantes para o início da fenda do cânion e quedas como a Cascata das Andorinhas e a Véu de Noiva. Já o Cotovelo é mais longo, mas ainda leve, seguindo por uma antiga estrada interna e depois pela borda do cânion até uma das vistas mais clássicas do Itaimbezinho.</p>
<h2>Mirantes do Vértice</h2>
<p>O Vértice é o ponto de partida mais acessível para quem chega ao parque. A trilha curta e bem sinalizada leva até mirantes que revelam o início da fenda do Itaimbezinho — e é lá que as primeiras quedas d'água aparecem. A Cascata das Andorinhas e a Véu de Noiva despencam das bordas do planalto enquanto o abismo do cânion se abre em toda a sua extensão abaixo. É o trecho ideal para quem quer uma caminhada rápida, uma fotografia inesquecível e a sensação de estar no topo de algo grandioso sem muito esforço.</p>
<h2>Mirante do Cotovelo</h2>
<p>O Cotovelo é a caminhada mais longa das duas, mas o terreno permanece amigável: boa parte do percurso segue por uma antiga estrada interna de terra e trechos de campo próximos à borda do cânion. A recompensa é a vista clássica dos paredões do Itaimbezinho vistos de cima — as paredes verticais de basalto com o Rio do Boi lá no fundo, em uma escala que justifica qualquer quilômetro percorrido. É o ângulo mais fotografado do parque e um dos pontos mais marcantes de todos os Campos de Cima da Serra.</p>
<h2>Informações técnicas</h2>
<p>Distância total somando Cotovelo e Vértice: aproximadamente 7,5 a 8 km. Ganho de altitude acumulado: cerca de 130 m. Duração média: 2h30 a 3h30 com pausas para fotos e mirantes. O percurso acontece na parte alta do parque, com pouco desnível relevante. O esforço é baixo a moderado leve. Há trechos abertos em campos de altitude e pontos com vegetação de araucária, com exposição moderada ao sol.</p>
<p>O terreno do Cotovelo segue em grande parte por antiga estrada interna de terra/cascalho e trechos de campo próximos à borda do cânion. O Vértice tem trechos mais estruturados, mirantes e caminhada leve. Em ambos os percursos, a sinalização é boa e as trilhas estão demarcadas.</p>
<h2>Melhor época para visitar</h2>
<p>Outono e inverno tendem a oferecer clima mais seco e menor incidência de neblina. A visitação pela manhã é fortemente recomendada: as chances de boa visibilidade costumam ser melhores no início do dia, e o visitante evita a pressa do retorno. A trilha pode ser feita ao longo do ano, mas julho e inverno em geral são frequentemente destacados como favoráveis para visualização dos cânions. O clima dos Campos de Cima da Serra muda rápido — neblina, vento e chuva podem surgir mesmo em dias previstos como estáveis.</p>
<h2>Segurança e boas práticas</h2>
<p>Os principais cuidados são neblina, vento, chuva, mudança brusca de clima, bordas de cânion, pedras escorregadias e baixa visibilidade. Antes de sair, cheque a previsão do tempo e evite iniciar a trilha com risco de temporal, raios, vento forte ou neblina densa. Avise alguém sobre seu roteiro e horário previsto de retorno. Não ultrapasse cercas, não se aproxime demais das bordas e não saia da trilha demarcada para tirar fotos. Em áreas de cânion, a percepção de distância e profundidade pode enganar, principalmente com vento ou baixa visibilidade.</p>
<p>Traga todo o lixo de volta, não alimente animais, respeite a vegetação e siga as regras do parque. Pets não são permitidos dentro do Parque Nacional de Aparados da Serra. Não planeje reabastecimento de água no percurso — leve sua própria água do início ao fim.</p>
<h2>Trilha com crianças e iniciantes</h2>
<p>É uma trilha indicada para iniciantes, famílias, casais, viajantes solo e trilheiros intermediários que querem um passeio de alta recompensa visual sem grande exigência física. Com crianças, é necessária supervisão constante especialmente próximo às bordas do cânion. O clima muda rápido e a neblina pode comprometer a visibilidade — mantenha o grupo junto e planeje a saída com antecedência.</p>
<h2>Vale contratar guia local?</h2>
<p>Para Vértice e Cotovelo, o guia costuma ser recomendado, mas não obrigatório — confirme a regra vigente antes da visita, pois políticas do parque podem ser atualizadas. Um guia local ajuda a escolher o melhor horário, ajustar o ritmo do grupo, explicar a formação dos cânions, indicar os melhores mirantes, orientar sobre clima e oferecer suporte em caso de imprevistos. Para visitantes de primeira viagem, famílias, pessoas com receio de trilhas ou quem quer fotografar melhor o Itaimbezinho, a presença de um guia traz mais tranquilidade e contexto.</p>
<h2>Contexto: Cânion Itaimbezinho e Cambará do Sul</h2>
<p>O Cânion Itaimbezinho é frequentemente descrito como o maior cânion da América Latina, com paredões que atingem até 720 metros de altura e 5,8 km de extensão. O parque fica na Serra Geral, no planalto sul-rio-grandense, e é acessado a partir de Cambará do Sul — uma das cidades-base mais completas para o turismo serrano do Sul do Brasil, com boa oferta de pousadas e guias especializados. A Floresta com Araucárias que domina o planalto acima do cânion é um dos biomas mais ameaçados do Brasil, e o parque é um dos últimos refúgios significativos dessas árvores centenárias.""",

"pico-parana-serra-do-ibitiraquire": """\
<h2>O que esperar da trilha</h2>
<p>O Pico Paraná é o ponto mais alto da Região Sul do Brasil, com 1.877 metros de altitude na Serra do Ibitiraquire, entre Campina Grande do Sul e Antonina, no Paraná. Não é apenas a maior montanha do Sul: é um dos grandes clássicos do montanhismo brasileiro, uma rota que mistura Mata Atlântica densa, terreno bruto e mirantes que revelam o conjunto imponente da Serra do Ibitiraquire. Quem chega ao cume carrega mais do que o cansaço de uma trilha longa — carrega a experiência de ter conquistado algo real.</p>
<p>A rota clássica é feita em ida e volta, com distância aproximada de 15 a 17 km e ganho acumulado entre 1.200 e 1.400 metros. O AllTrails registra 15,1 km e 1.284 m de ganho. Para bate-volta, considere entre 10 e 14 horas dependendo do ritmo, clima e paradas. A opção em 2 dias com pernoite autorizado pelo IAT é mais segura e menos desgastante — especialmente para quem nunca fez alta montanha no Sul.</p>
<h2>Como é a experiência no percurso</h2>
<p>O percurso sai da base do IAT e avança por mata fechada desde os primeiros metros. Raízes expostas, barro, degraus naturais e subidas persistentes definem o primeiro trecho. Conforme a altitude aumenta, a Floresta Ombrófila Densa muda de fisionomia: a floresta se torna mais rala, os galhos mais retorcidos e a sensação de estar em outro ambiente começa a se firmar.</p>
<p>Nos trechos mais altos, mirantes revelam o maciço do Pico Paraná e as montanhas vizinhas da Serra do Ibitiraquire — Caratuva, Itapiroca, União, Camapuã. Em dias limpos, a vista compensa cada metro de subida. No cume, o silêncio e a amplitude do horizonte transformam a chegada em algo difícil de descrever: uma das experiências mais emblemáticas do montanhismo paranaense.</p>
<h2>Distância, altimetria e esforço físico</h2>
<p>A distância total em ida e volta está entre 15 e 17 km, dependendo do ponto de início, do tracklog seguido e de eventuais variações para áreas de camping ou mirantes. O ganho de altitude aproximado é de 1.200 a 1.400 metros — número expressivo para uma trilha de dia ou de dois dias, com subida persistente ao longo de quase toda a extensão. O AllTrails classifica a rota como difícil e registra 1.284 m de ganho de elevação.</p>
<p>O esforço é alto e constante: não há trecho fácil de alívio prolongado. A subida é progressiva, com desnível acumulando ao longo de toda a rota. Para bate-volta, nível de condicionamento acima da média e experiência prévia em trilhas de montanha são requisitos sérios, não recomendações opcionais.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O percurso não é tecnicamente complexo como escalada, mas combina terreno bruto com esforço físico alto durante horas. Raízes, pedras, barro e trechos rochosos exigem atenção constante. Há partes em que as mãos são necessárias para apoio. A sinalização é parcial — fitas e marcações ajudam, mas a atenção à rota e um tracklog salvo offline são indispensáveis.</p>
<p>O IAT orienta caminhar preferencialmente sobre rochas já expostas, manter-se na trilha principal e evitar desvios para reduzir impacto ambiental. Não abra atalhos, não saia da trilha demarcada e não ignore o cadastro de entrada — ele é obrigatório e parte do sistema de segurança do parque.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a setembro costuma ser o período mais favorável para montanhas no Paraná — clima mais frio e seco, menor risco de chuvas e melhor estabilidade de tempo. Mas mesmo na estação seca, o clima na serra pode mudar com rapidez. Chuva, neblina e queda de temperatura são possíveis em qualquer época do ano na altitude de 1.877 metros.</p>
<p>O IAT é claro: a visitação nas trilhas não é permitida em dias de chuva, com reabertura apenas após 24 horas sem precipitação. Antes de ir, cheque a previsão do tempo e não insista em condições desfavoráveis. O Pico Paraná sem visibilidade e com chuva não é apenas frustrante — é perigoso.</p>
<h2>Como chegar ao Pico Paraná</h2>
<p>O acesso oficial é pela BR-116. A referência informada pelo IAT é passar pelo Posto do Tio Doca, entrar na Ponte do Rio Tucum e seguir aproximadamente 6 km por estrada rural até a base do IAT do Parque Estadual Pico Paraná. Curitiba é a melhor base logística para quem vem de fora do estado.</p>
<p>A estrada final tem características rurais e pode estar comprometida após chuvas. Chegue cedo para o cadastro, organização do grupo e início seguro. Não utilize acessos clandestinos ou atalhos fora da trilha oficial — o IAT fiscaliza e bloqueia acessos irregulares.</p>
<h2>Dicas de segurança na alta montanha</h2>
<p>Faça o cadastro obrigatório na entrada e a baixa do cadastro na saída. Avise alguém sobre o roteiro, horário previsto de retorno e nomes do grupo antes de entrar na trilha. Leve água suficiente — os pontos de água existem, mas não devem ser tratados como garantia; trate qualquer água coletada em córregos. O IAT recomenda bota adequada, roupas apropriadas, lanterna, pilhas, roupas extras e anorak impermeável.</p>
<p>Para bate-volta, inicie antes do amanhecer ou nas primeiras horas da manhã, com tracklog salvo offline e margem para retorno com luz. O IAT alerta para temperaturas baixas à noite, calor durante o dia, tempestades repentinas, queda de temperatura e animais peçonhentos. Não improvise: fadiga, neblina, frio e erro de navegação podem transformar uma trilha mal planejada em risco real.</p>
<h2>Vale a pena contratar guia para o Pico Paraná?</h2>
<p>O guia não é obrigatório pelo IAT para o Pico Paraná, mas a própria unidade recomenda condutores para visitantes com pouca experiência em ambiente de montanha. Um guia local conhece o terreno, interpreta o clima, ajuda no ritmo e no planejamento, orienta nos pontos de decisão e dá apoio em situações de emergência.</p>
<p>Para trilheiros intermediários bem condicionados e com experiência em navegação, é possível fazer a trilha sem guia com planejamento sólido. Para iniciantes, grupos sem experiência em montanha ou qualquer pessoa em dúvida sobre a rota: guia não é burocracia, é segurança e melhor aproveitamento da aventura.</p>
<h2>Pontos de água e camping</h2>
<p>Existem pontos de água relatados ao longo do percurso, mas não devem ser considerados garantidos. Leve água suficiente desde a base e trate toda água coletada em córregos. O acampamento é permitido apenas nas áreas estabelecidas pelo IAT. Fogueiras são proibidas; fogareiro é permitido com afastamento mínimo de vegetação; o kit dejetos é obrigatório para pernoites e travessias. Confirme quais áreas estão liberadas antes de ir.</p>""",


"chapada-diamantina-vale-do-capao": """\
<h2>O que esperar da trilha</h2>
<p>O Vale do Capão é a porta de entrada mais selvagem da Chapada Diamantina. Diferente da movimentada Lençóis, a Vila de Capão tem uma atmosfera própria — uma comunidade alternativa aninhada num vale cercado por paredões de arenito que fazem a paisagem parecer pintada à mão. A trilha principal do vale conecta esse refúgio à Cachoeira da Fumaça, o maior salto livre do Brasil, com 340 metros de queda que só podem ser vistos por inteiro de cima — do mirante do Pai Inácio — ou de baixo, onde a névoa de água cria um microclima permanentemente úmido.</p>
<p>O percurso de 18 quilômetros é circular e pode ser feito em dois a três dias, com acampamento no próprio vale ou nas proximidades da cachoeira. A densidade de paisagens é extraordinária: em um único trecho é possível ver paredões de quartzito avermelhado, campos rupestres com orquídeas e canelas-de-ema, nascentes de água cristalina e o som constante do Rio Capão que atravessa a vila. O guia é obrigatório dentro do parque e essencial para navegar os atalhos que encurtam a rota sem sacrificar os melhores pontos.</p>
<h2>Como é a experiência no percurso</h2>
<p>A partida da Vila de Capão já é uma experiência em si: ruas de terra, casas coloridas, uma praça onde permacultores e mochileiros se misturam com moradores nativos. A trilha sai pelo fundo da vila e começa subindo entre cercas de pedra seca até abrir nos campos rupestres. A vegetação baixa dos campos permite visões dos paredões de arenito que enquadram o vale como uma catedral natural.</p>
<p>O trecho mais longo vai em direção à Cachoeira da Fumaça, passando por trechos de mata ciliar ao longo do Rio Capão. A aproximação pela base da cachoeira é feita por uma trilha íngreme que termina num anfiteatro de rocha úmido e nebuloso — mesmo em dias de sol, a névoa gerada pelos 340 metros de queda cria um ambiente permanentemente suave e difuso. Quem sobe ao mirante superior (trecho separado de 8 km) tem uma perspectiva completamente diferente: o volume d'água visto de cima parece uma fita branca desaparecendo no abismo.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>A subida para o mirante da Fumaça é o trecho mais exigente, com desnível de cerca de 600 metros em terreno irregular de campos rupestres. No período seco, a cachoeira pode estar com volume muito reduzido ou quase seca — o nome "Fumaça" vem da névoa gerada pelo impacto com o ar, que persiste mesmo com pouca água, mas o visual é muito mais dramático na estação chuvosa. Verifique as condições com o guia antes de definir o roteiro.</p>
<p>Na Vila de Capão, a orientação para trilhas começa nas agências locais ou com guias independentes cadastrados pelo ICMBio. Não entre no parque por trilhas não sinalizadas sem guia — o território é vasto, a vegetação rupestre dificulta a orientação e os parques da Chapada têm histórico de visitantes perdidos que tentaram economizar no guia.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a outubro é a estação seca, com trilhas transitáveis, água cristalina nos rios e temperatura mais amena — as noites no vale podem ser frias, especialmente em julho. A Cachoeira da Fumaça atinge seu pico de volume entre janeiro e março, logo após as chuvas, mas o acesso é mais difícil. Junho e julho concentram o maior número de visitantes na Chapada; se buscar silêncio, vá em setembro ou outubro, quando o fluxo cai e as flores dos campos rupestres ainda estão no auge.</p>
<h2>Dicas de segurança</h2>
<p>Protetor solar de alto fator é indispensável nos campos rupestres — a vegetação baixa não oferece sombra e o sol da Bahia é intenso durante todo o ano. Leve pelo menos dois litros de água para os trechos entre pontos de abastecimento. O calçado mais importante é a bota de trilha: as pedras de quartzito são cortantes e o terreno irregular castiga tornozelos sem suporte adequado. No camping, guarde alimentos em sacos herméticos — as cutias do parque são especialistas em acessar mochilas abertas.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado, mas o acúmulo de dois a três dias com mochila carregada eleva a exigência. Caminhantes com experiência em trilhas de um dia conseguem adaptar o ritmo, especialmente se dividirem o percurso em etapas curtas. A Vila de Capão tem ótima infraestrutura de pousadas para quem prefere fazer as trilhas mais leves sem carregar equipamento de camping.</p>
<h2>Pontos de água e camping</h2>
<p>O Rio Capão é a principal fonte de água ao longo do percurso. Os campings mais utilizados ficam na própria vila e nas proximidades da base da cachoeira. Trate sempre a água coletada nos rios — a Chapada recebe cada vez mais visitantes e a contaminação por coliformes tem sido registrada em pontos de maior frequência. Fogareiro e kit dejetos são obrigatórios para pernoites fora de área urbana.</p>
<h2>Contexto local: bioma e comunidade</h2>
<p>A Vila de Capão — oficialmente Caeté-Açu — é uma das comunidades mais peculiares do interior da Bahia: mistura de agricultores tradicionais, artistas, permacultores e praticantes de espiritualidades alternativas que chegaram nos anos 1980 e 1990 fugindo do ritmo urbano. Hoje convivem em harmonia razoável e criaram uma rede de pousadas, restaurantes e artesanato que sustenta a economia local sem destruir o que os trouxe até ali. O bioma é o Cerrado da Chapada — uma das formações mais biodiversas do planeta, com flora e fauna altamente endêmicas e ameaçadas.""",

"pico-dos-marins": """\
<h2>O que esperar da trilha</h2>
<p>O Pico dos Marins, segundo ponto mais alto de São Paulo com 2.420 metros, é um dos grandes segredos do montanhismo paulistano. Enquanto o Pico do Papagaio e a Serra Fina acumulam fama e filas de espera, os Marins permanece relativamente pouco visitado — o que significa silêncio nos campos de altitude, acesso descomplicado e a sensação genuína de conquista que se perde nos destinos mais turísticos. A trilha de 14 quilômetros (ida e volta) com 1.250 metros de desnível é uma das mais exigentes de São Paulo, mas também uma das mais recompensadoras.</p>
<p>O percurso começa em Piquete, município no Vale do Paraíba paulista na divisa com Minas Gerais, e sobe consistentemente por Mata Atlântica de altitude e campos rupestres até o cume com visão de 360° sobre a Mantiqueira. A trilha pode ser feita como bate-volta exigente (8-10 horas) ou em dois dias com bivaque próximo ao cume — a segunda opção é muito superior para quem quer viver o nascer do sol no topo.</p>
<h2>Como é a experiência no percurso</h2>
<p>O começo da trilha atravessa propriedades rurais e mata secundária, com subida progressiva que vai abrindo a vegetação conforme a altitude aumenta. Na faixa dos 1.500 metros, a Mata Atlântica começa a se transformar: árvores menores, mais retorcidas pelo vento, cobertas de musgos e bromélias. Aos 1.800 metros, o ambiente muda completamente — campos rupestres abertos com visão para os vales abaixo e, em dias claros, para o Pico da Bandeira ao sudeste.</p>
<p>O trecho final ao cume é o mais exposto e, por isso, o mais emocionante. As últimas centenas de metros sobem por um campo aberto onde o vento domina e o horizonte vai se expandindo em todas as direções. No cume, a vista abrange a Serra da Mantiqueira em toda a sua extensão — um horizonte de serras sobrepostas que se estende até onde a névoa permite ver. Em dias de clareza excepcional, é possível identificar o Pico do Papagaio, o Pico da Bandeira e a Serra do Papagaio numa única volta de 360°.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho entre 1.800 metros e o cume não tem sombra e é totalmente exposto ao vento. Em dias de vento forte, a progressão fica lenta e a sensação térmica cai muito abaixo da temperatura marcada no termômetro. Capa impermeável e camadas térmicas devem estar acessíveis na mochila em qualquer época do ano. A trilha não tem marcação profissional em toda a extensão — GPS com rota carregada é recomendado para o trecho superior.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a setembro é a janela ideal: estação seca com trilha mais firme, vento moderado e clareza superior para as vistas. O inverno (junho-agosto) pode trazer geada no cume — temperaturas abaixo de zero são registradas em noites claras de julho. O verão (dezembro-fevereiro) traz chuvas periódicas, trovões em altitude e solo enlameado que dificultam a subida. Setembro e outubro têm floração intensa nos campos de altitude, transformando o percurso em uma galeria de cores.</p>
<h2>Dicas de segurança</h2>
<p>Saia antes das 7h para bate-volta: a janela segura de 10 horas é justa e qualquer imprevisto com saída tardia coloca o retorno no escuro. Para quem vai bivouacar, leve saco de dormir para temperaturas negativas e barraca com bom sistema de tensionamento — o vento em altitude nos Marins é real e forte. Não há serviço de emergência próximo ao cume; grupo mínimo recomendado é de duas pessoas.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil. O desnível de 1.250 metros em 7 quilômetros de subida é o parâmetro principal: não é uma trilha para quem está começando. Caminhantes que já fizeram travessias de dois dias e dominam o ritmo de mochila pesada conseguem concluir o bate-volta confortavelmente. Para a opção de dois dias com bivaque, acrescente experiência em camping de altitude e leitura de tempo de montanha.</p>
<h2>Contexto local: Mantiqueira e Piquete</h2>
<p>Piquete é uma cidade do Vale do Paraíba com história ligada à aviação — sede do Instituto de Fomento e Coordenação Industrial (IFI) do Exército. A cidade tem boa infraestrutura de hospedagem e serve de ponto logístico para o pico. A APA da Serra da Mantiqueira, onde o pico está inserido, é uma das áreas de proteção mais importantes do corredor ecológico da Mata Atlântica do Sudeste, conectando fragmentos florestais de São Paulo, Minas Gerais e Rio de Janeiro.""",

"gruta-do-lapao": """\
<h2>O que esperar da trilha</h2>
<p>A Gruta do Lapão é um destino que surpreende até quem já visitou outras grutas e cavernas brasileiras. Diferente das cavernas calcárias com suas estalactites e estalagmites, o Lapão foi esculpido inteiramente no arenito — processo geológico raro que cria cavidades com geometrias e texturas completamente diferentes. Com 1.120 metros de extensão e galeria principal de até 70 metros de largura, o Lapão é a maior gruta em arenito do Brasil e uma das maiores do mundo nessa categoria de rocha.</p>
<p>A trilha de acesso tem apenas 4 quilômetros (ida e volta) e parte diretamente da cidade de Lençóis, tornando o Lapão acessível para praticamente todos os perfis de visitante — famílias com crianças, idosos com boa condição física e grupos sem experiência em trilhas de montanha. Mas a simplicidade do acesso não prepara ninguém para a escala da experiência dentro da gruta: entrar na galeria principal é como entrar numa catedral que a natureza levou milhões de anos para construir.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha começa na orla de Lençóis e sobe suavemente por mata ciliar às margens de um riacho de água clara. O arenito avermelhado aparece gradualmente, primeiro como blocos soltos entre as raízes das árvores, depois como paredões que crescem à medida que a trilha sobe. A entrada da gruta é identificada pelo som — um silêncio diferente, abafado, que se contrapõe ao canto dos pássaros da floresta em volta.</p>
<p>A galeria principal é longa o suficiente para que a luz natural do exterior suma completamente antes de chegar ao fundo. O guia é obrigatório e leva lanternas para iluminar as formações internas: colunas de arenito, nichos escavados pela água, pontos de luz que entram por fraturas no teto criando efeitos de iluminação únicos. A "Janela" — uma abertura natural na parede da gruta — enquadra a paisagem da chapada como uma pintura. Sentar em frente a ela e olhar para fora é um dos momentos mais silenciosos e contemplativos que a Chapada Diamantina oferece.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O interior da gruta tem trechos com piso irregular e pedras soltas — calçado fechado de solado firme é obrigatório. O guia orienta os pontos seguros de pisada e as formações que não devem ser tocadas. No período das chuvas, o nível de água dentro da gruta pode subir e fechar o acesso a alguns trechos internos; o guia verifica as condições antes de avançar. Fotografia interna é permitida — leve lanterna própria para complementar a iluminação do guia e conseguir fotos melhores.</p>
<h2>Melhor época para visitar</h2>
<p>A Gruta do Lapão pode ser visitada durante o ano inteiro, mas a estação seca (abril a outubro) oferece melhores condições de acesso ao interior. No período das chuvas (novembro a março), o piso interno fica mais escorregadio e alguns trechos podem ficar alagados. A trilha externa é sombreada e agradável em qualquer época. O horário mais recomendado é o período da manhã, quando a luz que entra pela Janela da gruta cria os melhores efeitos fotográficos.</p>
<h2>Dicas de segurança</h2>
<p>Nunca entre na Gruta do Lapão sem guia — o interior tem ramificações e trechos escuros onde a desorientação é rápida sem referências externas. Não toque nas paredes da gruta: os óleos da pele aceleram a erosão do arenito, que é muito mais frágil que o calcário. Evite luz de flash direta nas formações para fotografar — use iluminação indireta. Crianças menores de 5 anos têm acesso restrito a alguns trechos internos.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível fácil. A trilha de acesso é curta e de baixo desnível, acessível para qualquer pessoa com mobilidade básica. O interior da gruta exige apenas atenção para onde pisar. O Lapão é uma das poucas atrações da Chapada Diamantina que combina acessibilidade total com impacto visual de primeiríssima linha — um destino perfeito para quem viaja com crianças ou com pessoas que não praticam trekking regularmente.</p>
<h2>Contexto local: Lençóis e a Chapada</h2>
<p>Lençóis é o principal centro de visitação da Chapada Diamantina, com infraestrutura completa de pousadas, restaurantes, agências de turismo e guias credenciados. A cidade histórica, com casarões do século XIX da era do garimpo de diamantes, é Patrimônio Histórico Nacional e vale ser explorada antes ou depois das trilhas. A Gruta do Lapão fica a apenas 2 quilômetros do centro histórico — é possível ir caminhando diretamente do centro da cidade, tornando-a ideal como primeira atividade ao chegar ou última antes de partir.""",

"canion-do-sumidouro": """\
<h2>O que esperar da trilha</h2>
<p>O Cânion do Sumidouro é um segredo geográfico guardado pela Serra Gaúcha que ainda não entrou no roteiro massificado do turismo sul-brasileiro. Escavado pelo Rio Antas ao longo de milhões de anos no basalto da Serra Geral, o cânion tem paredões que atingem 150 metros e uma extensão de vários quilômetros onde o rio desaparece literalmente sob as rochas — daí o nome "Sumidouro". A trilha de 8 quilômetros atravessa mata nativa de araucárias e campos de altitude até os mirantes que revelam a magnitude do corte geológico.</p>
<p>O acesso é feito por propriedade privada na região de São Marcos, cidade no meio da Serra Gaúcha entre Caxias do Sul e Bento Gonçalves. A área é menos estruturada que o Cânion Itaimbezinho, mas essa rusticidade é parte do apelo — o Sumidouro ainda tem aquele caráter de descoberta que os destinos mais famosos perderam. O percurso combina floresta de araucária, campos abertos com visão panorâmica e o próprio cânion, cujo silêncio só é quebrado pelo som distante do rio no fundo.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha começa na beira da propriedade de acesso, atravessa uma porteira de madeira e entra imediatamente em floresta de araucária — uma das formações vegetais mais características e ameaçadas do Sul do Brasil. O piso é de agulhas de araucária sobre um colchão de musgo, macio e silencioso. A medida que a trilha avança, a floresta abre espaço para clareiras com visão das bordas do cânion ao longe.</p>
<p>O primeiro mirante chega após cerca de 3 quilômetros e a vista é imediata: o cânion se abre abruptamente, com paredes verticais de basalto escuro descendo em linha reta até o Rio Antas, que em alguns trechos desaparece sob blocos de rocha desmoronados — o ponto do "Sumidouro" propriamente dito. A continuação da trilha percorre a borda do cânion com mirantes sucessivos que revelam ângulos diferentes do corte geológico. Em dias claros, é possível ver até Caxias do Sul nos campos ao fundo.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>A borda do cânion não tem guarda-corpo ou sinalização de segurança em todos os pontos — mantenha distância segura das bordas, especialmente com crianças. O terreno em alguns trechos de campo fica enlameado após chuvas, tornando o acesso aos mirantes escorregadio. No interior do cânion (acesso avançado para grupos experientes), as rochas úmidas e o rio em volume alto após chuvas criam condições perigosas que exigem avaliação cuidadosa.</p>
<h2>Melhor época para visitar</h2>
<p>Setembro a novembro e março a maio são os melhores períodos: temperatura amena, vegetação verde e o Rio Antas com volume moderado — suficiente para ser bonito, não tanto a ponto de criar risco. O inverno gaúcho (junho-agosto) pode trazer frio intenso e geada que torna o percurso desafiador, mas a paisagem de cânion com névoa da manhã é extraordinariamente fotogênica. O verão (dezembro-fevereiro) é quente e úmido, com possibilidade de chuvas fortes que aumentam o caudal do rio.</p>
<h2>Dicas de segurança</h2>
<p>Não se aproxime das bordas do cânion além do que os mirantes sinalizados permitem — acidentes acontecem por excesso de confiança. Leve capa impermeável mesmo em dias de sol: o microclima da Serra Gaúcha pode mudar rapidamente. O acesso ao fundo do cânion pelo leito do Rio Antas deve ser feito apenas com conhecimento da área e acompanhamento de alguém familiarizado com as condições locais. Não nade no rio sem checar o volume e a correnteza com antecedência.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado. A trilha de borda é acessível para caminhantes com condição física regular, mas o terreno irregular e algumas subidas curtas exigem atenção. Para quem quer descer ao fundo do cânion, o nível de exigência sobe para difícil — essa variante exige experiência em trilhas técnicas e, preferencialmente, acompanhamento de guia local com conhecimento específico do cânion.</p>
<h2>Contexto local: Serra Gaúcha</h2>
<p>A região de São Marcos fica no coração da Serra Gaúcha vitivinícola, entre Caxias do Sul e Bento Gonçalves. Combinar a visita ao Cânion do Sumidouro com uma passagem pelas vinícolas e pelos municípios de colonização italiana da região é um roteiro completo de fim de semana. A cidade de São Marcos tem pousadas simples e gastronomia colonial italiana que complementa bem a experiência de trilha.""",

"serra-da-canastra": """\
<h2>O que esperar da trilha</h2>
<p>A Serra da Canastra guarda dois dos marcos mais simbólicos do Brasil central: a nascente do Rio São Francisco — o Velho Chico, o rio que abasteceu a sertaneja por séculos — e a Cachoeira Casca D'Anta, com 186 metros de queda que a tornam uma das maiores do país. Percorrer os 22 quilômetros da trilha principal entre a portaria de São Roque de Minas e a Casca D'Anta é atravessar o Cerrado mineiro em seu estado mais puro: campos rupestres intermináveis, lobos-guará que cruzam o caminho ao entardecer e silêncio de chapada que a cidade nunca oferece.</p>
<p>O parque fica a aproximadamente 500 quilômetros de Belo Horizonte e a 350 quilômetros de Brasília, o que o torna um destino logisticamente viável de fim de semana longo. A infraestrutura é bem organizada pelo ICMBio, com campings estruturados, sinalização de trilhas e fiscalização ativa. A Canastra recebe menos visitantes que parques mais famosos do Sudeste, o que preserva aquela qualidade de silêncio e imersão que está desaparecendo dos destinos mais populares.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha começa na portaria de São Roque de Minas e atravessa imediatamente os campos de altitude da chapada. A vegetação é a marca: campos sujos com murunduns, veredas de buritis, manchas de cerrado sensu stricto com seus ipês retorcidos e os campos rupestres nas cotas mais altas. Em julho e agosto, as canelas-de-ema atingem seus dois metros de altura e os campos ficam salpicados de amarelo e branco das flores silvestres.</p>
<p>A nascente do Rio São Francisco fica a aproximadamente 8 quilômetros da portaria — um ponto de peregrinação para quem cresceu no Nordeste ou em Minas Gerais com o Velho Chico no imaginário cultural. A água brota de uma rocha numa quantidade modesta que dificilmente faz imaginar o rio caudaloso que ela vai se tornar 2.800 quilômetros depois. Mas a emoção do lugar vem precisamente dessa escala: ver onde começa o que alimentou tantas histórias e tantas vidas.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho entre a nascente do São Francisco e a Cachoeira Casca D'Anta é o mais longo e menos frequentado. A sinalização existe mas é mais esparsa — GPS com rota previamente carregada é recomendado. As estradas de terra dentro do parque podem ser cortadas pelas chuvas no verão, tornando alguns trechos inacessíveis de carro; confirme as condições de acesso com o ICMBio antes de planejar visitas entre novembro e março.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a outubro é a estação seca, com trilhas transitáveis e temperatura agradável durante o dia. As noites de inverno na chapada são frias — geada é registrada no planalto em julho. A floração do Cerrado acontece principalmente de julho a setembro, quando o visual dos campos é excepcional. O verão chuvoso (dezembro a março) transforma as cachoeiras em espetáculos de volume, mas dificulta o acesso a algumas áreas do parque. A Cachoeira Casca D'Anta atinge seu máximo de volume entre janeiro e março.</p>
<h2>Dicas de segurança</h2>
<p>O sol do Cerrado é direto e intenso: protetor solar de fator 50, chapéu de aba larga e camiseta manga longa são equipamentos, não opcionais. A hidratação nos campos abertos é consumida mais rapidamente do que parece. Leve mínimo de dois litros para os trechos entre fontes. No entardecer, o lobo-guará cruza os campos com frequência — não se aproxime, não ofereça alimento e aproveite o privilégio de observar de longe.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado. O terreno da Canastra não apresenta trechos técnicos, mas o percurso de 22 quilômetros com mochila de dois dias em campo aberto é exigente pelo volume total e pelo calor. Caminhantes com experiência em trilhas de um dia conseguem completar em dois dias com ritmo tranquilo. A opção de fazer percursos parciais saindo e voltando pela portaria é válida para quem quer conhecer o parque sem o desafio da travessia completa.</p>
<h2>Pontos de água e camping</h2>
<p>Os riachos do parque fornecem água ao longo do percurso, mas o tratamento é obrigatório — filtro ou purificador é item essencial. O Camping Casca D'Anta, próximo à cachoeira, é o mais estruturado do parque e serve de base para quem divide a travessia em dois dias. Reserve com antecedência pelo sistema ICMBio, especialmente em feriados e fins de semana de julho e agosto, quando o parque recebe o maior fluxo de visitantes.""",

"parque-nacional-superagui": """\
<h2>O que esperar da trilha</h2>
<p>Chegar ao Parque Nacional de Superagui exige uma decisão que filtra por si só o perfil do visitante: sem estrada, sem sinal de celular confiável, acessível apenas por barco a partir de Guaraqueçaba, no litoral norte do Paraná. Essa inacessibilidade é a maior proteção de um dos últimos grandes remanescentes de Mata Atlântica costeira do Brasil — e Patrimônio Mundial da UNESCO desde 1999. Quem decide encontrar Superagui encontra também um dos lugares mais silenciosos e biologicamente ricos do litoral sul-sudeste.</p>
<p>O parque abrange a Ilha de Superagui e a Ilha das Peças, com uma rede de trilhas, canais e praias que se estende por dezenas de quilômetros. A Praia Deserta — 40 quilômetros de areia fina sem acesso por terra — é o símbolo maior do parque: uma das praias mais preservadas do Brasil, sem quiosques, sem voadores de boia, sem presença humana permanente. A trilha principal percorre a ilha de Superagui da vila até a borda da Praia Deserta, cruzando manguezais, restingas e mata atlântica de restinga num percurso de 12 quilômetros que parece de outro tempo.</p>
<h2>Como é a experiência no percurso</h2>
<p>A Vila de Superagui — uma comunidade de pescadores artesanais caiçaras com cerca de 1.000 moradores — é o ponto de partida e chegada. A vida na vila acontece em ritmo de maré: as saídas e chegadas dos barcos de pesca, a fumaça das casas de farinha, as crianças que andam descalças pelas vielas de terra. Essa imersão na cultura caiçara é parte indissociável da experiência de Superagui — não é um parque com vila adjacente, é uma vila dentro de um parque onde a relação entre humanos e natureza nunca foi cortada.</p>
<p>A trilha sai pela borda da vila e entra imediatamente em mata fechada de restinga. A vegetação é densa, baixa e intrincada, com epífitas em abundância e o som constante de pássaros que nem os mais experientes birdwatchers conseguem identificar todos. Após aproximadamente 4 quilômetros, a mata abre abruptamente para a Praia Deserta: o impacto é imediato. Quarenta quilômetros de areia branca sem nenhum sinal humano visível nos dois sentidos. O oceano Atlântico de frente, a restinga de costas, e o silêncio — exceto pelo vento e pelas ondas.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>A trilha em mata de restinga é bem definida mas pode ficar enlameada após chuvas. O guia é obrigatório para a trilha interna — além da exigência legal, o conhecimento do guia local sobre fauna, flora e pontos de passagem da maré é insubstituível. Na Praia Deserta, cuidado com a ressaca oceânica: as ondas são abertas, sem proteção de recifes, e podem ser fortes. Não nade nos pontos de corrente de retorno — o guia indica os locais seguros.</p>
<h2>Melhor época para visitar</h2>
<p>Março a novembro tem menor volume de chuvas e mares mais calmos para a travessia de barco. Dezembro a fevereiro é alta temporada com mais visitantes e mar potencialmente mais agitado para a chegada. O inverno (junho-agosto) é frio no litoral paranaense mas com dias claros e oceano calmo. Para observação de aves, agosto a outubro é o período ideal — espécies migratórias chegam ao litoral e o papagaio-de-cara-roxa está mais ativo.</p>
<h2>Dicas de segurança</h2>
<p>O barco de acesso a Superagui pode ser afetado por tempo adverso — tenha flexibilidade de datas para acomodar cancelamentos por mau tempo marítimo. Na ilha, não há farmácia ou pronto-socorro — leve kit de primeiros socorros completo e qualquer medicação necessária para a estadia. A água potável na vila é de qualidade variável; leve purificador ou compre garrafas na cidade antes do embarque. Repelente forte é obrigatório — os mosquitos de manguezal são diferentes dos urbanos.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível fácil a moderado para a trilha principal. O maior desafio não é físico, mas logístico: chegar requer organização, o retorno depende de horário de barco e a permanência exige autossuficiência básica. Para quem aceita essas condições, Superagui oferece uma imersão de natureza que poucos destinos no Brasil ainda proporcionam.</p>
<h2>Contexto local: cultura caiçara e preservação</h2>
<p>Os moradores de Superagui vivem uma tensão histórica com o parque — parte das restrições de uso afeta diretamente suas práticas de pesca e agricultura tradicionais. A visita consciente, que valoriza a hospedagem e os serviços dos caiçaras, é a forma mais direta de contribuir para que a comunidade se beneficie do turismo e encontre razões para preservar, ao invés de resistir, ao parque que cerca suas vidas. O papagaio-de-cara-roxa — endêmico e criticamente ameaçado — depende tanto da floresta quanto da convivência pacífica com os moradores.""",

"pico-do-caraca": """\
<h2>O que esperar da trilha</h2>
<p>O Pico do Caraça não é apenas uma trilha — é uma experiência que combina montanhismo, história colonial e um dos espetáculos faunísticos mais incomuns do Brasil: os lobos-guará que aparecem ao entardecer no claustro de uma igreja do século XVIII para ser alimentados pelos frades lazaristas. Esta combinação única de cume de 2.072 metros, santuário histórico preservado e encontro programado com o maior canídeo sul-americano faz do Caraça um destino absolutamente singular no país.</p>
<p>O Santuário do Caraça, em Catas Altas, no Quadrilátero Ferrífero mineiro, é uma reserva particular administrada pela Congregação da Missão. O colégio histórico — fundado em 1820 — ainda funciona como pousada, com hospedagem em quartos simples nos próprios corredores do colégio e refeições no refeitório original. Dormir no Santuário do Caraça é experimentar uma das acomodações mais inusitadas do Brasil, com os sinos da igreja marcando as horas e as janelas dando para jardins de mata atlântica preservada.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha sai da sede do Santuário e sobe por Mata Atlântica densa de altitude nos primeiros quilômetros. A floresta é extraordinariamente preservada — sem caça, sem extrativismo, protegida pelos frades por mais de 200 anos — e a diversidade de aves é notável: o andorinhão-de-coleira, o tucano-de-bico-preto e várias espécies de beija-flor acompanham a subida. Bromélias, orquídeas e samambaias arborescentes cobrem cada tronco disponível.</p>
<p>Acima de 1.600 metros, a mata vai cedendo espaço para campos rupestres com a flora típica do Quadrilátero Ferrífero: canelas-de-ema, sempre-vivas e cactos de campos de altitude. O vento aumenta conforme o cume se aproxima. No topo, com 2.072 metros, a vista abrange o Quadrilátero Ferrífero ao sul, a Serra do Espinhaço ao norte e, em dias excepcionais de visibilidade, o horizonte onde Belo Horizonte brilla ao longe. O silêncio é total — e o contraste com a capital a 120 quilômetros é deliberado e libertador.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho final ao cume, acima dos 1.800 metros, é exposto ao vento e sem sombra. Após chuvas, as pedras de campo rupestre ficam escorregadias — botas com solado de borracha são indispensáveis. A trilha tem bifurcações com sinalização nem sempre atualizada; o mapa fornecido pelo Santuário é suficiente, mas GPS offline é uma garantia adicional útil. Inicie a subida no máximo às 8h para ter tempo de retorno antes do anoitecer — a caminhada de 12 km leva de 6 a 8 horas em ritmo razoável.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a outubro é a estação seca e mais segura. O inverno (junho-agosto) pode trazer geada nos campos do cume — temperaturas abaixo de 5 °C são registradas em noites claras de julho — mas os dias são ensolarados e as vistas excepcionalmente claras. O verão chuvoso (dezembro-março) tem flores nos campos rupestres, mas a névoa frequente pode limitar as vistas do cume. Os lobos-guará aparecem no Santuário durante o ano todo; o horário de alimentação varia com a estação e é informado na recepção.</p>
<h2>Dicas de segurança</h2>
<p>Hospede-se no Santuário para viver a experiência completa: a caminhada de ida e volta ao cume no mesmo dia que se vem de Belo Horizonte é logisticamente possível mas cansativa. Para o espetáculo dos lobos-guará, o horário é tipicamente entre 18h30 e 20h, no jardim do claustro — o Santuário orienta onde e como esperar. Não persiga ou alimente os lobos fora do ritual coordenado pelos frades: eles são animais silvestres e a habitualidade com humanos é resultado de décadas de condicionamento controlado.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil pelo desnível de 830 metros em 6 quilômetros de subida. Caminhantes com experiência regular em trilhas de montanha e boa condição aeróbica completam o percurso confortavelmente. Para iniciantes, é possível fazer a trilha com ritmo lento e descansos frequentes, mas o retorno antes do anoitecer exige gestão cuidadosa do tempo. Bastões de trekking são recomendados para a descida, especialmente para proteger os joelhos no trecho de maior inclinação.</p>
<h2>Contexto histórico: o Santuário e os frades</h2>
<p>O Colégio do Caraça foi fundado em 1820 pelos padres lazaristas e formou gerações de estudantes mineiros até o incêndio de 1968, que destruiu grande parte do edifício central. A reconstrução manteve a essência histórica, e hoje a Congregação da Missão administra tanto a reserva natural quanto a pousada e o museu histórico. A biblioteca e a coleção de objetos coloniais merecem uma tarde de exploração antes ou depois da subida.""",

"lagoa-azul-bonito": """\
<h2>O que esperar da trilha</h2>
<p>A Lagoa Azul é o cartão postal mais famoso de Bonito e, para muitos visitantes, a revelação de que a realidade pode superar as fotografias. A água da lagoa é de um azul-turquesa tão saturado e translúcido que parece retocada digitalmente — mas é física e química: as partículas de calcário em suspensão na água refratam a luz criando essa tonalidade que varia de turquesa claro na superfície para azul-cobalto nas profundezas. A visibilidade chega a 30 metros, tornando o snorkeling numa experiência de flutuação sobre o abismo.</p>
<p>O fenômeno mais esperado de Bonito é o raio de sol que penetra pela abertura da gruta e ilumina as stalactites subaquáticas em azul intenso — esse espetáculo acontece apenas de junho a julho, entre 9h e 10h da manhã, quando o ângulo solar é preciso o suficiente para que a luz desça exatamente pelo buraco na rocha. Mas a Lagoa Azul é impactante em qualquer horário e época do ano: a clareza da água, os cardumes de piraputanga e dourado que nadam em torno dos visitantes e as stalactites parcialmente submersas criam um ambiente que não tem equivalente em nenhum outro ponto do Brasil.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha de acesso, com 3 quilômetros, parte da área de recepção e percorre mata ciliar preservada da Bacia do Rio Miranda. O caminho é plano e bem mantido, com o guia explicando a formação geológica da área e as espécies de flora ao longo do percurso. A chegada é impactante: após uma última curva, a abertura da gruta aparece e, alguns metros abaixo, a lagoa azul se estende em toda a sua dimensão. A descida até a beira da água é feita por uma rampa de madeira que respeita o ângulo da rocha.</p>
<p>O tempo de snorkeling é cronometrado pelo operador — geralmente 30 a 40 minutos — com colete salva-vidas obrigatório e nadadeiras para ajudar a flutuar sem esforço. Dentro da água, cardumes de centenas de peixes nativos circulam ao redor dos visitantes com absoluta indiferença — o peixe de Bonito não tem predador humano há décadas e perdeu o instinto de fuga. A experiência de estar rodeado por uma nuvem de peixe dourado em água de cristal com stalactites ao fundo é genuinamente surreal.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>Bonito funciona com um sistema único de controle de visitação: todas as atrações exigem agência ou guia credenciado e o número de visitantes por dia é limitado por cada atrativo. Reserve com antecedência — especialmente em julho, dezembro e janeiro, quando a Lagoa Azul pode atingir capacidade máxima com semanas de antecedência. A entrada sem reserva não é possível. O acesso à Lagoa Azul não é adequado para pessoas com claustrofobia severa ou dificuldade de mobilidade.</p>
<h2>Melhor época para visitar</h2>
<p>A Lagoa é visitável o ano inteiro, mas outubro a março oferece a maior diversidade de piraputanga nos cardumes e temperaturas de água mais amenas. De junho a julho, quem quer ver o raio de sol nas stalactites deve reservar para o horário entre 9h e 10h — é quando o fenômeno acontece. Julho é também alta temporada com preços elevados e atrações lotadas. Para uma experiência mais tranquila, vá em setembro, outubro ou novembro.</p>
<h2>Dicas de segurança</h2>
<p>Use apenas protetor solar biodegradável dentro da água — os protetores comuns contaminam o calcário e destroem a transparência que torna a lagoa única. O protetor convencional é proibido em todas as atrações aquáticas de Bonito. Não toque nas stalactites ou nas paredes da gruta dentro da água. Comer dentro da lagoa ou levar comida para próximo da água também é proibido. Siga rigorosamente as instruções do guia — as regras de Bonito são rígidas e fazem parte do motivo pelo qual o destino continua tão preservado após décadas de visitação.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível fácil. A trilha de acesso não exige preparo físico e o snorkeling com colete não requer habilidade de natação avançada. A Lagoa Azul é um dos destinos mais acessíveis e democráticos de Bonito — adequada para crianças a partir de aproximadamente 5 anos, adultos sem condição física para trilhas mais exigentes e idosos com mobilidade razoável. O principal pré-requisito é não ter medo de água e conseguir usar snorkel.""",

"pedra-azul": """\
<h2>O que esperar da trilha</h2>
<p>A Pedra Azul é um monólito granítico que domina o horizonte da Serra do Espírito Santo como um farol de rocha: 1.822 metros de altitude, 300 metros de altura visível desde a base e uma coloração que muda ao longo do dia — do cinza-rosado da manhã para o azul-acinzentado do entardecer que deu nome à pedra. O Parque Estadual da Pedra Azul protege o monólito e a Mata Atlântica de altitude que o envolve, com uma trilha de 6 quilômetros que chega às piscinas naturais esculpidas na rocha na base do granito.</p>
<p>O parque fica em Domingos Martins, município da região serrana capixaba a 75 quilômetros de Vitória — uma das distâncias mais curtas entre uma capital brasileira e uma área de proteção com trilha de montanha. Essa proximidade faz da Pedra Azul o destino favorito dos vitorienses e uma parada obrigatória para quem passa pela BR-262 entre o Espírito Santo e Minas Gerais.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha parte do Centro de Visitantes e adentra imediatamente uma Mata Atlântica de altitude extraordinariamente preservada. A floresta tem uma densidade de bromélias, orquídeas e samambaias que transforma os troncos em jardins verticais. O som de pássaros é constante — o Parque Estadual da Pedra Azul tem uma das listas mais ricas de avifauna do Espírito Santo, com espécies endêmicas da Mata Atlântica que não existem em nenhum outro bioma.</p>
<p>Após aproximadamente 2 quilômetros, a trilha abre para a área das piscinas naturais: concavidades esculpidas pelo intemperismo na superfície do granito, preenchidas por água de nascentes que desce pelo monólito. A água é fria, transparente e perfeitamente azul-esverdeada pelo reflexo do granito molhado. As piscinas de diferentes tamanhos criam um complexo natural de banhistas que nenhum resort conseguiria replicar. A Pedra Azul ao fundo, mudando de cor conforme o sol se move, é o enquadramento perfeito.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>As rochas em torno das piscinas ficam extremamente escorregadias quando molhadas — acidentes por queda são a principal ocorrência nos registros do parque. Calçado aquático com solado antiderrapante ou sandália de trekking com boa aderência é mais seguro do que andar descalço. O guia é obrigatório para a trilha e orienta os pontos seguros de entrada e saída das piscinas. O sol na face sul do monólito cria sombra nas piscinas a partir das 15h — chegue cedo para aproveitar o sol na água.</p>
<h2>Melhor época para visitar</h2>
<p>Maio a setembro é a estação seca, com trilha mais transitável, piscinas limpas e o efeito da coloração azul da pedra mais pronunciado nos entardeceres. O verão (outubro a abril) tem chuvas frequentes que podem fechar a trilha por segurança e turvar as piscinas. A floração das bromélias e orquídeas da Mata Atlântica acontece principalmente entre agosto e outubro — o percurso nessa época é especialmente rico em detalhes botânicos. A Pedra Azul tem lotação máxima em fins de semana de julho — chegue antes das 8h para evitar filas.</p>
<h2>Dicas de segurança</h2>
<p>Não suba na face vertical do monólito fora dos pontos autorizados pelo parque — a rocha parece mais fácil de escalar do que é, e acidentes graves já aconteceram em tentativas não autorizadas. O mergulho nas piscinas é permitido apenas nas áreas sinalizadas; a profundidade varia muito entre concavidades e algumas têm fundos irregulares. Protetores solares convencionais são proibidos nas piscinas — use somente protetor mineral ou biodegradável. Leve água suficiente para o percurso — as fontes ao longo da trilha não devem ser usadas sem tratamento.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível moderado. A trilha não tem trechos técnicos, mas o desnível de 520 metros em 3 quilômetros de subida exige boa condição aeróbica. Crianças acima de 8 anos geralmente completam o percurso sem dificuldade, desde que o ritmo seja adaptado. Para visitantes que buscam apenas as piscinas sem a subida completa, existe um acesso mais curto pela área de uso intensivo — consulte o Centro de Visitantes.</p>
<h2>Contexto local: serra capixaba</h2>
<p>A região serrana do Espírito Santo, colonizada predominantemente por imigrantes alemães e italianos no século XIX, tem uma identidade cultural distinta do litoral capixaba. Domingos Martins é conhecida pelo festival de cultura germânica, pela gastronomia de influência europeia e pela arquitetura das casas de campo que salpicam as encostas entre o Parque da Pedra Azul e a cidade. Combinar a trilha com uma passagem pelo centro histórico de Pedra Azul (vilarejo no entorno do parque) e um almoço nas pousadas da região é o itinerário mais completo para a região.""",

"pedra-da-gavea": """\
<h2>O que esperar da trilha</h2>
<p>A Pedra da Gávea é a trilha urbana mais icônica do Brasil — e possivelmente do mundo. Com 844 metros de altitude, o cume do maciço granítico está a apenas 12 quilômetros em linha reta do centro do Rio de Janeiro, e a vista do topo combina o que nenhum outro ponto da cidade consegue oferecer: Cristo Redentor, Pão de Açúcar, Lagoa Rodrigo de Freitas, Ipanema, Leblon e o oceano Atlântico numa panorâmica de 360° que tem poucos equivalentes em metrópoles do mundo. A subida, contudo, não é uma caminhada casual — inclui um trecho de escalada com corda fixada que filtra quem chega ao cume.</p>
<p>A trilha está dentro do Parque Nacional da Tijuca — a maior floresta urbana do mundo — e exige guia credenciado pelo ICMBio, tanto por questão de segurança no trecho técnico quanto por ser norma do parque. A distância de 10 quilômetros (ida e volta) não é o parâmetro principal: o desnível de 820 metros em terreno irregular de floresta densa e, especialmente, o trecho de escalada são o que determinam o perfil do caminhante adequado para a Gávea.</p>
<h2>Como é a experiência no percurso</h2>
<p>A trilha começa na Estrada da Gávea, no bairro da Gávea, e entra imediatamente na Floresta da Tijuca — uma imersão instantânea de mata atlântica a metros do bairro de São Conrado. A floresta é exuberante e barulhenta com aves, macacos-pregos e saguis que acompanham a subida com curiosidade e sem medo. O percurso sobe consistentemente por singletrack de terra e raízes por cerca de 3 quilômetros até chegar ao início do trecho técnico.</p>
<p>O trecho de escalada é o coração da experiência. Uma fenda vertical na rocha granítica — com cordas fixas instaladas pelo parque — exige subir pelo próprio corpo usando apoios na pedra. O guia instrui os movimentos e garante a segurança, mas é necessária disposição física e psicológica para encarar alguns metros de exposição vertical. Para quem supera esse momento, a chegada ao cume é correspondentemente dramática: o plateau granítico se abre em visão total de 360° do Rio de Janeiro que literalmente tira o fôlego.</p>
<h2>Principais trechos e pontos de atenção</h2>
<p>O trecho de escalada é o único ponto sem alternativa — quem não conseguir ou não quiser fazê-lo não chega ao cume. A escalada não é tecnicamente difícil, mas exige força de braço e resistência a alturas. Pessoas com acrofobia severa devem ser honestas consigo mesmas antes de tentar. O cume é totalmente exposto ao vento e ao sol — leve camadas e protetor solar. Em dias de nevoeiro, a visibilidade do topo pode ser zero; o guia avalia as condições antes de iniciar e pode recomendar cancelamento em dias de má visibilidade.</p>
<h2>Melhor época para visitar</h2>
<p>Abril a outubro tem menos chuvas e maior probabilidade de visibilidade limpa no cume. O verão carioca (dezembro-março) traz chuvas frequentes, rocha molhada que torna o trecho de escalada mais perigoso e névoa que cobre o topo com frequência. Os meses de julho e agosto têm os dias mais claros e o vento mais favorável — os melhores para fotografar o panorama completo do Rio. Saia antes das 7h para evitar o calor do meio-dia no trecho de subida e para ter mais chances de estar no cume sem névoa.</p>
<h2>Dicas de segurança</h2>
<p>Nunca faça a Pedra da Gávea sem guia credenciado — além de ser obrigatório, o trecho de escalada sem orientação adequada é genuinamente perigoso. Calçado de trilha com bom solado de borracha é fundamental para aderência na rocha; tênis de corrida e sapatilhas de skatista são inadequados. Não suba em dias de chuva ou com previsão de tempestade — a rocha molhada no trecho técnico cria risco real de queda. Leve no mínimo dois litros de água — o calor e o esforço na subida consomem mais do que parece.</p>
<h2>Nível de preparo recomendado</h2>
<p>Nível difícil. O desnível de 820 metros e o trecho de escalada colocam a Pedra da Gávea bem acima das trilhas de montanha convencionais. Caminhantes com experiência em trilhas moderadas a difíceis e sem fobia de altura conseguem completar o percurso com guia. Para quem nunca escalou nada e tem pouca experiência em trilhas, a recomendação é começar por trilhas mais simples do Parque da Tijuca antes de tentar a Gávea. A sensação de chegada ao cume, contudo, é uma das mais inesquecíveis que qualquer trilha no Brasil oferece.</p>
<h2>Contexto local: Parque Nacional da Tijuca</h2>
<p>O Parque Nacional da Tijuca é a maior floresta urbana do mundo e um dos exemplos mais bem-sucedidos de reflorestamento da história: a mata atual foi replantada no século XIX após o desmatamento da era colonial que ameaçava o abastecimento de água do Rio de Janeiro. Hoje a floresta abriga mais de 200 espécies de aves, 70 espécies de mamíferos e uma diversidade de flora que rivaliza com florestas primárias do Brasil. A Pedra da Gávea é apenas a ponta mais alta de um parque que merece mais de uma visita.""",

}  # end TRAIL_EDITORIAL

# ---------------------------------------------------------------------------
# Per-trail FAQ content — 5–7 Q&A pairs, answers ≥ 60 words each
# ---------------------------------------------------------------------------
TRAIL_FAQ = {

"monte-roraima": [
    {
        "q": "Precisa de guia para fazer o Monte Roraima?",
        "a": "Sim, o guia é obrigatório por lei. A trilha atravessa a Terra Indígena Raposa Serra do Sol e o Parque Nacional do Monte Roraima, e a contratação de um guia Pemón é exigida para entrar na área. Além da exigência legal, o guia é indispensável na prática: a navegação no planalto nevado de névoa constante é inviável sem alguém que conheça os marcos. Os guias são contratados na aldeia de Paraitepui, ponto de partida oficial da expedição.",
    },
    {
        "q": "Quanto custa a entrada no Monte Roraima?",
        "a": "Não existe cobrança de ingresso federal avulso para o Monte Roraima, mas os custos envolvem a contratação obrigatória do guia Pemón (valores negociados diretamente na aldeia de Paraitepui, geralmente entre R$ 200 e R$ 400 por dia por grupo), além de transporte até a aldeia e alimentação ao longo dos 6 a 8 dias de expedição. Há também a taxa de uso de acampamento no parque, cobrada pela ICMBio. Confirme os valores atualizados diretamente com operadoras locais em Boa Vista (RR).",
    },
    {
        "q": "Qual a melhor época para visitar o Monte Roraima?",
        "a": "O período mais favorável vai de outubro a abril, quando as chuvas são menos frequentes e os rios da rota estão em nível seguro para vadeamento. A estação chuvosa, entre maio e setembro, torna os vaus mais perigosos e a subida pela Rampa escorregadia. O topo do tepui tem microclima próprio com neblina e garoa praticamente o ano todo, então não espere dias completamente secos mesmo na alta temporada. Leve equipamento impermeável independentemente da época.",
    },
    {
        "q": "É possível acampar no Monte Roraima?",
        "a": "Sim, o acampamento é parte essencial da expedição. O roteiro padrão prevê pelo menos duas noites no próprio planalto, com pernoite no abrigo natural chamado de 'Hotel', uma gruta que protege do vento e da garoa. Durante a aproximação, há áreas de acampamento às margens dos rios Tek e Kukenán. Os guias Pemón indicam os locais permitidos; montar barraca fora das áreas estabelecidas é proibido. Fogueiras abertas são vetadas; use fogareiro.",
    },
    {
        "q": "Qual a dificuldade real do Monte Roraima para iniciantes?",
        "a": "O Monte Roraima é classificado como nível especialista e não é recomendado para iniciantes. A combinação de 6 a 8 dias de caminhada com mochila pesada, altitude de 2.810 metros, travessias de rios, trechos íngremes na Rampa e temperaturas noturnas abaixo de 10 °C exige experiência prévia em trekking de longa duração. A recomendação mínima é ter completado ao menos uma travessia de três dias antes, com treinamento aeróbico consistente por quatro meses.",
    },
    {
        "q": "Quantos dias dura a expedição ao Monte Roraima?",
        "a": "O roteiro completo leva de 6 a 8 dias. Os dois primeiros são de aproximação pelas savanas até a base do tepui; o terceiro é a subida pela Rampa até o planalto. Os dias seguintes são dedicados à exploração do topo — piscinas naturais, labirinto de cânions, ponto tríplice fronteira — antes da descida e retorno à aldeia. Planejar 8 dias dá margem de segurança para dias de mau tempo ou imprevistos no percurso.",
    },
    {
        "q": "O que levar na mochila para o Monte Roraima?",
        "a": "Os itens essenciais incluem: botas impermeáveis com bom agarre (prioritário para a Rampa), camadas térmicas para temperaturas abaixo de 10 °C à noite, capa de chuva e proteção impermeável para mochila, filtro ou purificador de água, protetor solar fator alto para as savanas, barraca de três estações resistente ao vento, saco de dormir para temperaturas negativas, liofilizados para complementar a alimentação preparada pelos guias, kit de primeiros socorros e lanterna frontal com baterias extras.",
    },
],

"travessia-petropolis-teresopolis": [
    {
        "q": "Precisa de guia para a Travessia Petrópolis–Teresópolis?",
        "a": "Não é obrigatório por lei, mas é fortemente recomendado para quem faz a travessia pela primeira vez. O percurso atravessa o interior do Parque Nacional da Serra dos Órgãos, com bifurcações que podem confundir mesmo trilheiros experientes. Um guia credenciado pelo ICMBio garante segurança na orientação, conhece os pontos de água, os refúgios e as saídas de emergência. Para grupos iniciantes ou em qualquer época de chuva intensa, a presença de guia é praticamente indispensável.",
    },
    {
        "q": "Quanto custa a entrada na Travessia Petrópolis–Teresópolis?",
        "a": "A entrada no Parque Nacional da Serra dos Órgãos é cobrada separadamente em cada sede: a taxa de acesso ao parque gira em torno de R$ 30 a R$ 40 por pessoa (valores sujeitos a reajuste pela ICMBio). A travessia exige pagamento adicional específico para pernoite nos refúgios ou acampamentos ao longo do percurso. Confirme os valores e disponibilidade de vagas diretamente no portal do ICMBio ou nas sedes do parque, pois há limite de visitantes por dia.",
    },
    {
        "q": "Qual a melhor época para a Travessia Petrópolis–Teresópolis?",
        "a": "Os meses de abril a setembro, período mais seco na Serra dos Órgãos, oferecem as melhores condições. O verão serrano (dezembro a março) traz chuvas intensas e frequentes, que transformam trechos de terra em lamaçais e aumentam o risco de deslizamentos e enchentes súbitas nos córregos. Mesmo na seca, leve equipamento impermeável: a neblina matinal é constante na altitude. Verifique sempre o boletim meteorológico antes de partir e consulte se o parque está aberto.",
    },
    {
        "q": "É possível acampar na Travessia Petrópolis–Teresópolis?",
        "a": "Sim. O percurso tem dois dias de duração padrão, com pernoite obrigatório nos refúgios ou áreas de acampamento credenciadas dentro do parque — o Refúgio dos Buracos e o Refúgio Rebouças são os mais utilizados. O acampamento selvagem fora das áreas delimitadas é proibido. As vagas nos refúgios são limitadas e devem ser reservadas com antecedência. Fogueiras abertas são vetadas em todo o parque; leve fogareiro e combustível sólido.",
    },
    {
        "q": "Qual a dificuldade real da Travessia Petrópolis–Teresópolis para iniciantes?",
        "a": "A travessia é classificada como difícil e não é ideal para quem nunca fez trekking com mochila carregada. O percurso de aproximadamente 42 quilômetros concentra desníveis acentuados, especialmente nos trechos de acesso ao Nariz do Frade e ao Dedo de Deus. A altitude média acima de 1.000 metros e o terreno rochoso exigem boa condição física e botas de cano alto. Iniciantes devem fazer ao menos algumas trilhas de dia inteiro antes de tentar a travessia.",
    },
    {
        "q": "Quantos dias dura a Travessia Petrópolis–Teresópolis?",
        "a": "O roteiro padrão leva dois dias completos. O primeiro dia cobre a entrada pela sede de Petrópolis até o acampamento ou refúgio de pernoite. O segundo dia conclui o percurso com chegada à sede de Teresópolis. Grupos mais lentos ou que desejam explorar desvios opcionais podem estender para três dias. O transporte de retorno entre as cidades deve ser planejado com antecedência, pois as sedes ficam a cerca de 60 km entre si.",
    },
    {
        "q": "Onde comprar o ingresso para a Travessia Petrópolis–Teresópolis?",
        "a": "As entradas e reservas de pernoite são feitas pelo sistema online do ICMBio (gov.br/icmbio) com antecedência, especialmente nos fins de semana e feriados, quando as vagas esgotam rapidamente. Também é possível comprar presencialmente nas sedes do parque, sujeito à disponibilidade do dia. O número de visitantes é limitado por dia para preservação ambiental, por isso reserve com pelo menos uma semana de antecedência em períodos de alta demanda.",
    },
],

"pico-da-bandeira": [
    {
        "q": "Precisa de guia para fazer o Pico da Bandeira?",
        "a": "Não é obrigatório, mas é recomendado para quem não tem experiência em trekking de altitude. O acesso principal é pela Vila do Caparaó (MG), dentro do Parque Nacional do Caparaó. A trilha é bem sinalizada até o pico, mas os trechos acima de 2.500 metros exigem atenção ao microclima e à orientação em dias com neblina. Para grupos com crianças ou pessoas sem experiência prévia, contratar um guia local aumenta significativamente a segurança.",
    },
    {
        "q": "Quanto custa a entrada no Pico da Bandeira?",
        "a": "O Parque Nacional do Caparaó cobra taxa de entrada por pessoa, atualmente em torno de R$ 30 a R$ 40 (valor sujeito a reajuste anual pelo ICMBio). Há também cobrança de estacionamento e, para quem deseja pernoitar nos abrigos dentro do parque, é necessário fazer reserva e pagar taxa adicional de acampamento. Confirme os valores atualizados e a disponibilidade de vagas diretamente no portal do ICMBio ou na portaria do parque antes de planejar a visita.",
    },
    {
        "q": "Qual a melhor época para visitar o Pico da Bandeira?",
        "a": "Maio a setembro é o período ideal: dias mais secos, visibilidade excelente no cume e menor risco de temporais elétricos. O verão capixaba-mineiro (novembro a março) traz chuvas pesadas à tarde, com raios que representam risco real acima de 2.800 metros — o cume é o ponto mais alto da região e atrai descargas com frequência. Mesmo na seca, inicie a caminhada cedo para descer antes de qualquer formação de nuvens no período da tarde.",
    },
    {
        "q": "É possível acampar no Pico da Bandeira?",
        "a": "Sim, o parque oferece áreas de acampamento credenciadas e abrigos para pernoite ao longo da trilha. Os abrigos Tronqueira e Terreirão são os mais usados para quem faz o pico em dois dias. As vagas são limitadas e precisam ser reservadas previamente pelo sistema do ICMBio. Acampamento selvagem fora das áreas designadas é proibido. Fogueiras abertas também são vetadas em todo o parque; leve fogareiro com combustível sólido para preparar refeições.",
    },
    {
        "q": "Qual a dificuldade real do Pico da Bandeira para iniciantes?",
        "a": "O Pico da Bandeira é classificado como moderado a difícil. O percurso de subida tem aproximadamente 17 quilômetros de ida e volta com ganho de altitude significativo, chegando a 2.892 metros — o terceiro ponto mais alto do Brasil. Iniciantes com boa condição física conseguem completar o percurso em um dia longo, mas devem estar preparados para desconforto com altitude, frio inesperado e terreno rochoso no trecho final. Experiência prévia em trilhas de dia inteiro é recomendada.",
    },
    {
        "q": "Qual a altitude do Pico da Bandeira e há risco de mal de altitude?",
        "a": "O Pico da Bandeira tem 2.892 metros de altitude, sendo o terceiro pico mais alto do Brasil. Nessa altitude, o mal de montanha grave é raro mas não impossível — alguns visitantes relatam dor de cabeça, náusea e tontura no cume, especialmente se subiram muito rápido sem aclimatação. O segredo é subir em ritmo moderado, manter boa hidratação e não forçar o ritmo nos trechos finais. Pessoas com condições cardiorrespiratórias devem consultar médico antes.",
    },
    {
        "q": "Quanto tempo leva para subir e descer o Pico da Bandeira?",
        "a": "A partir do Abrigo Tronqueira, a subida até o cume leva entre 3 e 4 horas para um ritmo médio; a descida, cerca de 2 a 3 horas. Quem faz o percurso completo a partir da portaria principal deve considerar entre 8 e 12 horas de caminhada no total, dependendo do ritmo e paradas. A maioria dos trilheiros opta por pernoitar em um dos abrigos para distribuir o esforço em dois dias e aproveitar o amanhecer no cume.",
    },
],

"canion-itaimbezinho": [
    {
        "q": "Precisa de guia para visitar o Cânion Itaimbezinho?",
        "a": "Não é obrigatório para as trilhas de borda (Trilha do Vértice e Trilha da Cotovias), que são auto-guiadas e bem sinalizadas dentro do Parque Nacional dos Aparados da Serra. Para a descida ao interior do cânion — percurso técnico que exige rapel — o guia especializado é indispensável e deve ser contratado com antecedência. Essa modalidade de descida só é permitida com empresa credenciada pelo ICMBio e condições climáticas favoráveis.",
    },
    {
        "q": "Quanto custa a entrada no Cânion Itaimbezinho?",
        "a": "A entrada no Parque Nacional dos Aparados da Serra custa em torno de R$ 25 a R$ 35 por pessoa (valor atualizado pelo ICMBio anualmente). O parque também cobra estacionamento. Para a descida técnica ao interior do cânion, as empresas credenciadas cobram valores extras que variam conforme o pacote e o número de participantes. Reserve sempre com antecedência, especialmente em fins de semana e feriados, quando o limite de visitantes é atingido rapidamente.",
    },
    {
        "q": "Qual a melhor época para visitar o Cânion Itaimbezinho?",
        "a": "O outono e o inverno sul-brasileiros (abril a agosto) oferecem a melhor visibilidade e menor incidência de neblina densa, que pode cobrir completamente o cânion nos meses mais úmidos. A primavera (setembro a novembro) é agradável, mas já traz chuvas. O verão (dezembro a março) tem risco de chuvas fortes que fecham o parque por segurança. Em qualquer época, vá cedo pela manhã: a neblina matinal costuma dissipar entre 9h e 10h, revelando a paisagem completa.",
    },
    {
        "q": "É possível acampar no Cânion Itaimbezinho?",
        "a": "O camping dentro do Parque Nacional dos Aparados da Serra é permitido apenas nas áreas credenciadas. Não há estrutura de acampamento próxima às bordas do cânion. A maioria dos visitantes se hospeda nas pousadas de Cambará do Sul (RS), cidade-base a cerca de 18 km do parque, que oferece boa infraestrutura com opções para todos os bolsos. A cidade é ponto de partida para outros cânions da região, como o Fortaleza.",
    },
    {
        "q": "Qual a dificuldade real do Cânion Itaimbezinho para iniciantes?",
        "a": "As trilhas de borda são acessíveis para iniciantes com boa condição física. A Trilha do Vértice (1,4 km) e a Trilha da Cotovias (3,8 km) são caminhadas relativamente planas ao longo das bordas do cânion, sem trechos técnicos. O terreno de grama e pedras é estável na seca. Já a descida ao interior do cânion tem grau técnico elevado e exige treinamento em rapel — não é recomendada para iniciantes sem experiência prévia em escalada ou rappel.",
    },
    {
        "q": "Quanto tempo leva para visitar o Cânion Itaimbezinho?",
        "a": "As trilhas de borda levam entre 2 e 4 horas para completar com tranquilidade, incluindo paradas para fotografar e apreciar as vistas. É possível fazer a visita em meio dia. Para quem deseja fazer a descida técnica ao interior do cânion, reserve o dia inteiro — o percurso leva entre 6 e 8 horas com as empresas credenciadas. A visita ao cânion vizinho, Fortaleza, pode ser combinada no mesmo dia ou no dia seguinte.",
    },
],

"travessia-serra-fina": [
    {
        "q": "Precisa de guia para a Travessia Serra Fina?",
        "a": "Sim, o guia é fortemente recomendado e praticamente indispensável. A Travessia Serra Fina é uma das mais exigentes de São Paulo e Minas Gerais, com trechos sem trilha definida, navegação em campo de altitude e passagens expostas em cristas estreitas. O Agulhas Negras e os trechos acima de 2.700 metros de altitude exigem habilidade de orientação mesmo com GPS. Muitos grupos contratam guias especializados em trekking de altitude para garantir segurança e logística adequada.",
    },
    {
        "q": "Quanto custa fazer a Travessia Serra Fina?",
        "a": "Não há ingresso único: a travessia começa em Passa Quatro (MG) ou Piquete (SP) e termina no lado oposto, cruzando áreas de diferentes gestores. Os custos incluem transporte até os pontos de entrada e saída, alimentação e equipamento para dois a três dias, guia especializado (preço varia por empresa e tamanho do grupo) e eventual taxa de acesso em propriedades privadas que margeiam o percurso. O custo total por pessoa gira em torno de R$ 800 a R$ 2.000 dependendo da organização.",
    },
    {
        "q": "Qual a melhor época para a Travessia Serra Fina?",
        "a": "Junho a agosto é o período mais seguro: menor precipitação, campos abertos com visibilidade máxima e ventos moderados. O verão serrano (dezembro a março) é proibido na prática: chuvas diárias intensas, raios em altitude e solo encharcado tornam os trechos expostos extremamente perigosos. Maio e setembro são meses de transição aceitáveis, mas exigem monitoramento do tempo. O inverno pode ter temperaturas próximas a 0 °C no bivaque — prepare equipamento térmico adequado.",
    },
    {
        "q": "É possível acampar na Travessia Serra Fina?",
        "a": "Sim, o pernoite em bivaque é parte obrigatória da travessia. Não há refúgios estruturados ao longo do percurso, então cada grupo monta acampamento nas áreas planas nos campos de altitude. O local mais comum de bivaque fica próximo à borda do planalto, com visão privilegiada. Fogueiras são proibidas pelo risco de incêndio nos campos. Leve fogareiro a gás, saco de dormir de frio extremo e barraca resistente a ventos fortes.",
    },
    {
        "q": "Qual a dificuldade real da Travessia Serra Fina para iniciantes?",
        "a": "A Travessia Serra Fina é classificada como extremamente difícil e não é adequada para iniciantes em hipótese alguma. O percurso exige experiência comprovada em trekking de múltiplos dias, navegação por bússola e GPS em terreno sem trilha, passagens em cristas expostas com risco de queda, resistência para carregar mochila pesada em altitudes acima de 2.700 metros e capacidade de improviso em emergências longe de qualquer resgate rápido. Pré-requisito mínimo: dois anos de prática regular em trekking.",
    },
    {
        "q": "Qual a distância e o desnível da Travessia Serra Fina?",
        "a": "A distância total varia entre 25 e 35 quilômetros dependendo da variante escolhida, com desnível acumulado de aproximadamente 2.000 metros. O ponto mais alto ultrapassa os 2.700 metros de altitude. O terreno inclui campos rupestres, trechos de mata de altitude, cristas rochosas e zonas de difícil orientação. O percurso não deve ser subestimado pela distância — a combinação de desnível, altitude e ausência de trilha definida torna o esforço muito superior a trilhas de mesma extensão no litoral.",
    },
],

"trilha-das-praias-rosa-norte-sul": [
    {
        "q": "Precisa de guia para a Trilha das Praias Rosa Norte–Sul?",
        "a": "Não é obrigatório. A Trilha das Praias, que conecta diversas praias selvagens ao longo do litoral sul de Santa Catarina, é auto-guiada e relativamente bem sinalizada nos trechos principais. No entanto, alguns trechos pelo costão rochoso e pela mata atlântica fechada podem confundir. Para quem faz o percurso completo de vários dias pela primeira vez, um guia local ou o uso de aplicativo de trilhas offline com as rotas salvas é altamente recomendado.",
    },
    {
        "q": "Quanto custa fazer a Trilha das Praias Rosa Norte–Sul?",
        "a": "O acesso às praias em si é gratuito. Os custos envolvem transporte até o ponto de partida (Praia do Rosa), alimentação (há pousadas e restaurantes ao longo do percurso em algumas praias), equipamento para pernoite se optar por acampar e transporte de retorno do ponto final. Não há taxa de entrada específica para a trilha. O custo total varia muito conforme a escolha entre acampar ou se hospedar nas pousadas das praias intermediárias.",
    },
    {
        "q": "Qual a melhor época para a Trilha das Praias Rosa Norte–Sul?",
        "a": "Março a junho e setembro a novembro são os períodos ideais: o mar costuma estar mais calmo para as travessias de costão, o calor é suportável e as praias estão menos lotadas. O verão (dezembro a fevereiro) é alta temporada com grande concentração de turistas, especialmente na Praia do Rosa. O inverno pode ter vento sul intenso e mar agitado que dificulta ou impossibilita o percurso nos trechos de costão. Verifique a previsão do mar antes de sair.",
    },
    {
        "q": "É possível acampar na Trilha das Praias Rosa Norte–Sul?",
        "a": "Há áreas de acampamento em algumas praias ao longo do percurso, mas a situação de cada ponto muda com frequência de acordo com regulamentações municipais e ambientais. Algumas praias têm camping estruturado com banheiro e chuveiro; outras permitem acampamento rústico na praia ou na mata. Confirme os locais permitidos antes de sair e respeite as sinalizações de área de proteção ambiental. Muitos trilheiros optam pelas pousadas simples das comunidades locais.",
    },
    {
        "q": "Qual a dificuldade real da Trilha das Praias Rosa Norte–Sul para iniciantes?",
        "a": "A trilha tem dificuldade moderada e é acessível para pessoas com condição física razoável. Os trechos pelo costão rochoso exigem atenção ao estado do mar e ao horário da maré — alguns pontos só são passáveis com maré baixa. A mata atlântica entre praias pode ser úmida e escorregadia. Não há altitudes elevadas, mas o terreno variado entre areia, pedras e floresta cansa mais do que parece em um dia longo. Verifique a tabua de marés antes de sair.",
    },
    {
        "q": "Quantos dias dura a Trilha das Praias Rosa Norte–Sul?",
        "a": "O percurso completo pode ser feito em 2 a 4 dias dependendo do ritmo e do número de praias visitadas. A versão mais curta, entre as duas ou três praias mais próximas, pode ser feita em um único dia. O roteiro estendido que conecta todas as praias de Rosa até o sul exige pelo menos três dias com pernoite. É possível fragmentar o percurso e fazer cada trecho em visitas separadas, voltando por trilha ou barco entre os pontos.",
    },
],

"vale-da-lua-e-cachoeiras": [
    {
        "q": "Precisa de guia para visitar o Vale da Lua e Cachoeiras?",
        "a": "Não é obrigatório para o Vale da Lua, que fica dentro da Chapada dos Veadeiros (GO) com acesso bem demarcado. Para as cachoeiras mais remotas da região, como o Salto do Rio Preto e as cachoeiras do Parque Estadual, um guia local é recomendado. Algumas cachoeiras fora do parque nacional ficam em propriedades privadas que exigem contratação de guia para acesso legal e seguro. Informe-se sobre cada ponto específico antes de partir.",
    },
    {
        "q": "Quanto custa a entrada no Vale da Lua e Cachoeiras?",
        "a": "O Vale da Lua fica dentro do Parque Nacional da Chapada dos Veadeiros; a entrada custa em torno de R$ 25 a R$ 35 por pessoa (valor ICMBio, sujeito a reajuste). As cachoeiras do parque estão incluídas no mesmo ingresso. Cachoeiras fora do parque, em propriedades privadas ou áreas de acesso pago, têm cobranças separadas que variam entre R$ 15 e R$ 50 por ponto. São Jorge (GO) é a vila base; há passeios organizados saindo de lá com preços por pessoa.",
    },
    {
        "q": "Qual a melhor época para visitar o Vale da Lua e Cachoeiras?",
        "a": "Maio a setembro é a melhor época: o período seco do cerrado garante rios com água cristalina, sem a turbidez que as chuvas provocam. O Vale da Lua fica ainda mais bonito com a água baixa, que expõe as formações rochosas completamente. O verão (novembro a março) tem chuvas que podem fechar o parque por dias. Dezembro a março têm menor visibilidade nas formações e maior risco de enchentes rápidas nas trilhas próximas ao Rio Preto.",
    },
    {
        "q": "É possível acampar no Vale da Lua e Cachoeiras?",
        "a": "O camping dentro do Parque Nacional da Chapada dos Veadeiros é permitido apenas em áreas designadas e com reserva prévia pelo sistema ICMBio. Não é possível acampar às margens do Rio Preto ou no Vale da Lua diretamente. A vila de São Jorge tem campings particulares bem estruturados a poucos quilômetros da entrada do parque, que servem como base para visitar o Vale da Lua, o Salto do Rio Preto e as cachoeiras. Fogueiras são proibidas no parque.",
    },
    {
        "q": "Qual a dificuldade real do Vale da Lua para iniciantes?",
        "a": "O Vale da Lua é acessível para a maioria dos visitantes. A trilha até as formações rochosas é curta e relativamente plana, com cerca de 1 a 2 quilômetros de caminhada leve. O desafio está nas pedras escorregadias próximas à água — sandálias com aderência ou tênis de borracha são melhores que chinelos. Para as cachoeiras mais distantes do parque, a dificuldade aumenta para moderada, com trechos de mata e desníveis. Crianças e idosos conseguem visitar o Vale com tranquilidade.",
    },
    {
        "q": "O que visitar além do Vale da Lua na Chapada dos Veadeiros?",
        "a": "A região concentra alguns dos mais belos atrativos do cerrado brasileiro. O Salto do Rio Preto, com queda de 120 metros, é considerado um dos mais impressionantes do Brasil. As Cariocas, as cachoeiras do Garimpão e os cânions do São Miguel completam o roteiro dentro do parque. Fora dele, a Chapada tem cachoeiras particulares como a Santa Bárbara (acesso pago), os cerradões da APA e as trilhas noturnas de observação de pirilampos, únicas no mundo.",
    },
],

"pico-parana-serra-do-ibitiraquire": [
    {
        "q": "Precisa de guia para o Pico Paraná?",
        "a": "Não é legalmente obrigatório, mas é altamente recomendado. O Pico Paraná, o mais alto do sul do Brasil com 1.877 metros, fica em área de mata atlântica densa com trilha parcialmente sinalizada. Trechos acima de 1.600 metros na Serra do Ibitiraquire podem perder marcação em dias com neblina intensa, que é frequente. Para quem faz o percurso pela primeira vez, um guia credenciado aumenta muito a segurança — especialmente nos campos de altitude do último terço da subida.",
    },
    {
        "q": "Quanto custa fazer o Pico Paraná?",
        "a": "Não há ingresso formal para o acesso ao Pico Paraná via a trilha principal que sai de Campina Grande do Sul (PR). Os custos envolvem transporte até o ponto de partida (Véu da Noiva), alimentação para o dia ou os dias de percurso e, se contratar guia, os honorários do profissional. Algumas pousadas na região oferecem pacotes com guia incluso. Verifique se o acesso pela propriedade privada que margeia a trilha cobra taxa — esse status muda com frequência.",
    },
    {
        "q": "Qual a melhor época para o Pico Paraná?",
        "a": "Junho a setembro oferece as melhores condições: frio seco, chance de geada nos campos de altitude (o que é uma atração em si) e menor precipitação. A mata atlântica paranaense tem chuva distribuída o ano todo, mas o inverno é visivelmente mais seco. O verão (novembro a março) traz chuvas torrenciais e neblina quase constante, que frequentemente fecham a visibilidade no cume a menos de 10 metros. Para quem quer ver o Paraná inteiro a seus pés, o inverno é a única opção segura.",
    },
    {
        "q": "É possível acampar no Pico Paraná?",
        "a": "Sim. A maioria dos trilheiros faz o Pico Paraná em dois dias com acampamento na Serra do Ibitiraquire, em área plana nos campos de altitude antes do cume. O camping selvagem é tolerado nesses campos, mas fogueiras são proibidas pelo risco de incêndio na vegetação de altitude. Leve fogareiro e combustível. Saco de dormir para temperaturas negativas é obrigatório no inverno — já foram registradas temperaturas de -5 °C nos campos. A opção de um dia exige saída antes das 5h.",
    },
    {
        "q": "Qual a dificuldade real do Pico Paraná para iniciantes?",
        "a": "O Pico Paraná é classificado como difícil e não é recomendado para iniciantes absolutos. A subida tem aproximadamente 10 quilômetros de ida com ganho de altitude de cerca de 800 metros, trechos de mata fechada com raízes e pedras e passagens expostas nos campos de altitude. A altitude de 1.877 metros é relativamente baixa para altitude sickness, mas a umidade da mata atlântica e o esforço físico acumulado são subestimados. Tenha pelo menos 6 meses de prática regular antes de tentar.",
    },
    {
        "q": "Qual é o ponto de partida para o Pico Paraná?",
        "a": "O acesso mais utilizado é pela cachoeira Véu da Noiva, em Campina Grande do Sul (PR), a cerca de 60 quilômetros de Curitiba. Outro acesso existe pelo lado de Antonina, mais longo e menos utilizado. O ponto de partida fica a cerca de 1 hora de carro do centro de Curitiba, tornando a trilha uma das mais acessíveis do Paraná em termos de logística. O estacionamento na base é informal; grupos grandes devem combinar transporte com antecedência.",
    },
],

"morro-dois-irmaos": [
    {
        "q": "Precisa de guia para o Morro Dois Irmãos?",
        "a": "Sim, o guia é obrigatório para a trilha que sobe ao topo do Morro Dois Irmãos, em Fernando de Noronha (PE). O percurso atravessa área de preservação ambiental permanente e o acesso só é permitido com guia credenciado pela administração do Parque Nacional Marinho de Fernando de Noronha. A contratação deve ser feita com antecedência, pois o número de visitantes por dia é limitado e as vagas esgotam rapidamente na alta temporada.",
    },
    {
        "q": "Quanto custa a entrada no Morro Dois Irmãos?",
        "a": "Além da Taxa de Preservação Ambiental (TPA) obrigatória para todos os visitantes de Fernando de Noronha — cobrada diariamente em valores progressivos — o acesso ao Morro Dois Irmãos exige o pagamento adicional ao guia credenciado, que varia entre R$ 150 e R$ 300 por pessoa dependendo do grupo e da empresa. A TPA começa em torno de R$ 100 por dia e aumenta conforme o número de dias na ilha. Verifique os valores atualizados no site oficial da Administração de Fernando de Noronha.",
    },
    {
        "q": "Qual a melhor época para visitar o Morro Dois Irmãos?",
        "a": "Agosto a fevereiro é a estação seca de Noronha, com menor precipitação e mar mais tranquilo. O período de dezembro a março tem visibilidade excepcional e é ideal para quem quer aproveitar o visual do topo do Morro Dois Irmãos. A estação chuvosa (março a julho) traz chuvas diárias que podem cancelar a subida por segurança. A trilha só é feita em condições de visibilidade segura; a administração da ilha pode vetar o acesso em dias de chuva intensa ou vento forte.",
    },
    {
        "q": "É possível acampar no Morro Dois Irmãos?",
        "a": "Não. O camping em Fernando de Noronha é proibido em toda a ilha — não há áreas de acampamento credenciadas. Os visitantes se hospedam nas pousadas da ilha, que vão de opções simples a resorts de luxo. A hospedagem é parte importante do custo da viagem: Fernando de Noronha é um dos destinos mais caros do Brasil, e os preços das pousadas, especialmente na alta temporada, podem ultrapassar R$ 1.000 a diária por pessoa em pacotes.",
    },
    {
        "q": "Qual a dificuldade real do Morro Dois Irmãos para iniciantes?",
        "a": "A trilha ao Morro Dois Irmãos tem dificuldade moderada e é acessível para pessoas com boa condição física. O percurso de subida leva cerca de 1 hora em ritmo tranquilo, com trechos de terra e rocha que exigem atenção. A altitude máxima é 325 metros, sem risco de altitude sickness. O trecho mais desafiador é o final, com inclinação acentuada e terreno instável. Use tênis de trilha — sandálias e chinelos são inadequados para o percurso.",
    },
    {
        "q": "O que ver no topo do Morro Dois Irmãos?",
        "a": "O topo do Morro Dois Irmãos oferece um dos panoramas mais fotografados do Brasil: de lá é possível ver a Baía do Sancho — frequentemente eleita a praia mais bonita do mundo —, a Praia do Leão, a Enseada dos Golfinhos, o Arquipélago das Rocas ao fundo e todo o perímetro da ilha em 360 graus. Nos meses de dezembro a fevereiro, a visibilidade pode alcançar dezenas de quilômetros em dias sem neblina. Leve câmera com lente grande-angular.",
    },
],

"fernando-de-noronha-baia-do-sancho": [
    {
        "q": "Precisa de guia para ir à Baía do Sancho em Fernando de Noronha?",
        "a": "Não é obrigatório para a descida à praia pela trilha (via escadaria na rocha) ou pelo barco. O acesso à Baía do Sancho é controlado pelo Parque Nacional Marinho, mas não exige guia para a visita simples à praia. Contudo, o número de visitantes simultâneos é limitado e a entrada pode ser negada se o limite do dia já tiver sido atingido. Para atividades como snorkeling guiado, mergulho com cilindro e trilhas ecológicas dentro do parque, guia credenciado é obrigatório.",
    },
    {
        "q": "Quanto custa visitar a Baía do Sancho em Fernando de Noronha?",
        "a": "Além da Taxa de Preservação Ambiental (TPA), cobrada diariamente para todos os visitantes da ilha (valores progressivos a partir de aproximadamente R$ 100 por dia), há taxa de entrada ao Parque Nacional Marinho que deve ser paga por visita. O acesso pelo barco inclui o custo da embarcação, em geral parte de passeios de volta à ilha que custam entre R$ 200 e R$ 400 por pessoa. Verifique os valores atualizados no portal da Administração de Fernando de Noronha.",
    },
    {
        "q": "Qual a melhor época para visitar a Baía do Sancho?",
        "a": "Agosto a fevereiro é a estação seca, com mares calmos, água cristalina e visibilidade subaquática excepcional — chegando a 30 metros em dias ideais. O período de agosto a outubro ainda tem ondas menores e menos turistas que dezembro e janeiro. A estação chuvosa (março a julho) tem mar mais agitado, menor visibilidade para mergulho e mais dias encobertos, mas preços de hospedagem mais baixos. Mesmo na seca, vá cedo à praia: o limite de visitantes é atingido antes do meio-dia na alta temporada.",
    },
    {
        "q": "É possível acampar em Fernando de Noronha ou na Baía do Sancho?",
        "a": "Não. O camping é absolutamente proibido em Fernando de Noronha, incluindo qualquer praia ou área do parque. Não existem campings nem áreas de bivaque na ilha. A hospedagem é feita exclusivamente nas pousadas e hotéis credenciados, que têm capacidade limitada como parte do controle ambiental da ilha. Essa é uma das medidas de preservação do arquipélago, que recebe número máximo de visitantes por dia. O custo de hospedagem é significativamente mais alto que em outros destinos brasileiros.",
    },
    {
        "q": "Qual a dificuldade real de chegar à Baía do Sancho?",
        "a": "A Baía do Sancho tem dois acessos: pela trilha com descida por uma fenda na rocha com escadas (fácil a moderado, cerca de 15 minutos de caminhada) ou pelo mar via passeio de barco. A descida pela fenda rochosa é a experiência clássica e acessível para a maioria das pessoas com mobilidade normal. Crianças pequenas e pessoas com dificuldade de mobilidade devem usar o acesso por barco. O principal desafio é o sol intenso e o calor — vá cedo e use protetor solar fator 50+.",
    },
    {
        "q": "O que fazer além da Baía do Sancho em Fernando de Noronha?",
        "a": "Fernando de Noronha concentra experiências únicas: observação de golfinhos-rotadores na Enseada dos Golfinhos ao amanhecer (gratuita e sem entrada na água), mergulho com cilindro nas Pedras Secas e na Laje Dois Irmãos, snorkeling na Praia do Atalaia (vagas limitadas, acesso controlado), trilha ao Morro Dois Irmãos com guia, passeio histórico às ruínas do Forte dos Remédios e observação de tartarugas nas praias do Leão e da Conceição nos meses de reprodução (novembro a março).",
    },
    {
        "q": "Como chegar a Fernando de Noronha e à Baía do Sancho?",
        "a": "Fernando de Noronha só tem acesso aéreo: voos saem de Recife (PE) e Natal (RN) com duração de aproximadamente 1h30. As companhias que operam a rota mudam conforme a temporada; reserve com antecedência, especialmente na alta temporada (dezembro a fevereiro), quando as passagens dobram de preço. Dentro da ilha, o deslocamento é feito por buggy alugado (limitado a visitantes cadastrados), moto, bicicleta elétrica ou transporte coletivo. Não existe acesso por barco de passageiros de forma regular.",
    },
],


"chapada-diamantina-vale-do-capao": [
    {
        "q": "Precisa de guia para trilhar no Vale do Capão na Chapada Diamantina?",
        "a": "Sim. O guia é obrigatório dentro dos limites do Parque Nacional da Chapada Diamantina, incluindo as trilhas da Cachoeira da Fumaça e da área do Vale do Capão. A exigência legal existe para proteger tanto os visitantes quanto o bioma — a Chapada é vasta, a vegetação rupestre dificulta a orientação e casos de pessoas perdidas sem guia têm histórico documentado. Os guias credenciados são contratados diretamente na Vila de Capão, nas agências de turismo locais ou pela internet com antecedência.",
    },
    {
        "q": "Qual a melhor forma de chegar ao Vale do Capão na Chapada Diamantina?",
        "a": "O Vale do Capão fica a aproximadamente 75 quilômetros de Lençóis, o principal hub aéreo da Chapada. De Lençóis, o acesso é feito por estrada de terra que pode ser difícil em épocas de chuva — carro com tração ou ônibus de van que sai diariamente de Lençóis são as melhores opções. De Salvador, são aproximadamente 450 quilômetros pela BR-116 e BA-148. A Vila de Capão tem boa infraestrutura de pousadas e é um destino por si só, mesmo para quem não vai fazer trilhas longas.",
    },
    {
        "q": "A Cachoeira da Fumaça tem água o ano todo?",
        "a": "Não. A Cachoeira da Fumaça varia muito de volume conforme a estação. No período das chuvas (novembro a março), o volume é máximo e o visual é dramático — a névoa gerada pelo impacto com o ar cria uma nuvem permanente na base. Na estação seca (especialmente agosto a outubro), a cachoeira pode ficar com volume muito reduzido ou praticamente seca no salto principal, com apenas um fio de água descendo. O guia informa as condições atuais antes de incluir a Fumaça no roteiro.",
    },
    {
        "q": "O que é melhor: ver a Cachoeira da Fumaça de cima ou de baixo?",
        "a": "São experiências completamente diferentes e complementares. De cima, do mirante do Pai Inácio (trecho separado de 8 km), a vista do salto livre de 340 metros é impressionante pela escala — um fio de água que cai e some na névoa abaixo. De baixo, a perspectiva é mais íntima e mais úmida: a névoa gerada pela queda cria um microclima permanente, a acústica é impressionante e a escala das paredões ao redor é de difícil compreensão. Se o tempo permitir, fazer as duas perspectivas em dias diferentes é o ideal.",
    },
    {
        "q": "Qual a melhor época para visitar o Vale do Capão?",
        "a": "Abril a outubro é a estação seca, com trilhas mais transitáveis, água cristalina nos rios e temperatura amena. Julho concentra o maior fluxo de visitantes — a Vila de Capão fica movimentada mas ainda tem a atmosfera própria. Para quem busca silêncio, setembro e outubro são excelentes: o fluxo cai e os campos rupestres ainda têm flores. A estação chuvosa (novembro-março) tem o benefício de ver a Fumaça em volume máximo, mas as trilhas ficam enlameadas e o acesso a alguns pontos pode ser bloqueado.",
    },
    {
        "q": "Quanto tempo preciso reservar para o Vale do Capão?",
        "a": "O mínimo recomendado é dois dias completos: um para a trilha da base da Cachoeira da Fumaça (aproximadamente 12 km, 6-8 horas) e outro para explorar os arredores da vila e um banho no Rio Capão. Para quem quer incluir o mirante da Fumaça pelo Pai Inácio, acrescente mais um dia. O Vale do Capão recompensa quem desacelera — a Vila tem uma energia particular que convida à permanência, e a diversidade de trilhas de diferentes dificuldades permite uma semana inteira de programação.",
    },
],

"pico-dos-marins": [
    {
        "q": "Precisa de guia para subir o Pico dos Marins?",
        "a": "Não é obrigatório legalmente, mas fortemente recomendado para quem não tem experiência em trilhas de altitude sem marcação profissional. O trecho superior do Pico dos Marins, acima dos 1.800 metros, tem marcação menos definida e a orientação por GPS é necessária em trechos onde o caminho se confunde com trilhas de gado. Um guia local de Piquete conhece os atalhos, os pontos de água e as melhores janelas de tempo para o cume — informações que valem mais do que qualquer aplicativo em campo.",
    },
    {
        "q": "Qual a dificuldade real do Pico dos Marins para quem nunca subiu um pico de 2.000 metros?",
        "a": "O Pico dos Marins é classificado como difícil principalmente pelo desnível de 1.250 metros em 7 quilômetros de subida — equivalente a escalar um prédio de 400 andares. Para quem nunca subiu acima de 1.500 metros, a altitude em si não é problema nos Marins, mas o acúmulo de esforço físico ao longo de horas de subida contínua é subestimado por caminhantes iniciantes. Preparação com caminhadas de treino progressivo por pelo menos dois meses antes da subida é o mínimo recomendado.",
    },
    {
        "q": "É possível fazer o Pico dos Marins em bate-volta no mesmo dia?",
        "a": "Sim, mas é exigente. O bate-volta leva de 8 a 10 horas dependendo do ritmo e do tempo no cume. Saída às 6h da manhã é o ideal para ter luz suficiente, evitar o calor do meio-dia na subida e chegar ao cume antes de eventual névoa da tarde. Caminhantes em boa condição física completam o percurso confortavelmente nesse horário. Para quem não tem experiência em ritmo de subida contínua, a opção de dois dias com bivaque próximo ao cume é muito mais segura e prazerosa.",
    },
    {
        "q": "Qual o melhor horário para estar no cume do Pico dos Marins?",
        "a": "O nascer do sol no cume é a experiência mais valorizada: a vista da Serra da Mantiqueira com o céu mudando de preto para dourado e o horizonte de serras emergindo da névoa é de rara beleza. Para viver esse momento, é necessário bivouacar na noite anterior próximo ao cume e subir o trecho final antes das 6h. Alternativamente, o entardecer também oferece iluminação dramática — mas o retorno no escuro exige lanterna frontal e conhecimento do caminho ou acompanhamento de guia.",
    },
    {
        "q": "Que equipamento levar para o Pico dos Marins?",
        "a": "Bota de trilha com solado de borracha é obrigatória — o terreno irregular e molhado do trecho superior não é compatível com tênis de corrida. Capa impermeável e camadas térmicas devem estar na mochila mesmo em dias de sol — o vento no cume de 2.420 metros cria sensação térmica muito menor que a temperatura do ar. Para o bate-volta: mínimo de 2,5 litros de água, protetor solar de alto fator, lanche energético e bastões para a descida. Para o bivaque: saco de dormir para temperaturas abaixo de zero, barraca com tensionamento para vento e fogareiro.",
    },
    {
        "q": "Como chegar até o início da trilha do Pico dos Marins?",
        "a": "O ponto de partida fica em Piquete, município do Vale do Paraíba paulista, a aproximadamente 200 quilômetros de São Paulo e 270 quilômetros do Rio de Janeiro. De carro, a rota mais usada é pela Rodovia Presidente Dutra (BR-116) com saída em Guaratinguetá e depois Piquete. O início da trilha fica a alguns quilômetros do centro da cidade, acessível por estrada de terra. Piquete tem hospedagem simples para quem chega na véspera. Transporte público até Piquete existe via ônibus de Guaratinguetá.",
    },
],

"gruta-do-lapao": [
    {
        "q": "Qual é a diferença entre a Gruta do Lapão e as outras cavernas da Chapada Diamantina?",
        "a": "A principal diferença é o tipo de rocha. A maioria das grutas famosas do Brasil é formada em calcário, onde a dissolução química cria estalactites e estalagmites. A Gruta do Lapão foi escavada no arenito — processo de erosão física que cria cavidades com geometrias mais arredondadas, paredes texturizadas em camadas horizontais e ausência de formações calcárias internas. O resultado é uma caverna com escala maior e aparência completamente diferente das grutas calcárias, sendo a maior do Brasil nessa categoria de rocha.",
    },
    {
        "q": "Precisa de guia para visitar a Gruta do Lapão?",
        "a": "Sim, o guia é obrigatório para acessar a Gruta do Lapão. A exigência existe por razões de segurança — o interior é extenso e escuro, e alguns trechos exigem conhecimento da rota — e por preservação: o guia impede o toque nas formações e garante que os visitantes sigam os caminhos que minimizam o impacto sobre o arenito, que é mais frágil que o calcário. Os guias são contratados em Lençóis, com saídas diárias organizadas por agências ou guias independentes credenciados.",
    },
    {
        "q": "Quanto tempo leva a visita à Gruta do Lapão?",
        "a": "A visita completa, incluindo a trilha de ida e volta (4 km) e a exploração do interior da gruta, leva de 3 a 4 horas. O percurso de acesso é tranquilo e serve de contexto geológico antes da gruta. No interior, o tempo varia conforme o interesse: quem vai fotografar cada ângulo passa mais tempo, quem vai em grupo com crianças tem ritmo diferente de quem vai para contemplação. A Gruta do Lapão é perfeitamente combinável com outras atrações de Lençóis no mesmo dia.",
    },
    {
        "q": "A Gruta do Lapão é adequada para crianças?",
        "a": "Sim, a Gruta do Lapão é uma das atrações mais adequadas para crianças de toda a Chapada Diamantina. A trilha de acesso é curta e plana, a gruta não tem trechos de escalada ou passagens muito estreitas, e o impacto visual é imediato — crianças ficam impressionadas com a escala da galeria principal. O guia geralmente tem repertório de explicações adaptadas para crianças sobre a formação geológica. A recomendação é levar lanterna própria para cada criança — iluminar a própria caverna aumenta muito o engajamento.",
    },
    {
        "q": "Qual a melhor época para visitar a Gruta do Lapão?",
        "a": "A Gruta do Lapão pode ser visitada durante o ano inteiro, o que a torna uma das poucas atrações da Chapada que funciona bem em qualquer estação. Na estação seca (abril a outubro), o acesso externo é mais fácil e o interior está menos úmido. Na estação chuvosa, o nível de água interna pode subir e restringir alguns trechos, mas a vegetação ao redor está mais exuberante. Para fotografar o efeito de luz na Janela da gruta, o período da manhã é o melhor em qualquer época do ano.",
    },
    {
        "q": "Como se chega à Gruta do Lapão saindo de Lençóis?",
        "a": "A Gruta do Lapão fica a aproximadamente 4 quilômetros do centro de Lençóis, acessível a pé pela trilha que sai da cidade ou de carro até o início do percurso. A maioria dos visitantes vai com o guia contratado, que organiza o transporte e acompanha durante toda a visita. Para quem prefere ir a pé diretamente do centro, o trajeto é bem sinalizado e faz parte da própria experiência — atravessar as ruas de Lençóis, sair pelo bairro do Rosário e seguir pelo caminho de terra até a entrada da gruta é uma introdução agradável ao ritmo da cidade.",
    },
],

"canion-do-sumidouro": [
    {
        "q": "Como chegar ao Cânion do Sumidouro no Rio Grande do Sul?",
        "a": "O Cânion do Sumidouro fica na área rural de São Marcos, município da Serra Gaúcha entre Caxias do Sul e Bento Gonçalves. O acesso é feito por estrada de terra a partir da cidade de São Marcos, com o último trecho passando por propriedade privada. Carro próprio é a forma mais prática de chegar. Caxias do Sul, com aeroporto e rodoviária, é a referência logística mais próxima — de lá são aproximadamente 35 quilômetros. Confirme o acesso com os proprietários da área antes de ir, pois a rota pode ter variações de acordo com a temporada.",
    },
    {
        "q": "O Cânion do Sumidouro é diferente do Cânion Itaimbezinho?",
        "a": "Sim, são experiências bastante diferentes. O Cânion Itaimbezinho é maior, mais famoso e mais estruturado — Parque Nacional com acesso regulamentado, trilhas marcadas e grande fluxo de visitantes. O Cânion do Sumidouro é menor, menos conhecido e mais rústico, com acesso por propriedade privada e estrutura mínima. O Itaimbezinho impressiona pela escala; o Sumidouro impacta pelo isolamento e pela sensação de descoberta. Para quem quer conhecer os cânions gaúchos, os dois se complementam perfeitamente num roteiro de dois a três dias na região.",
    },
    {
        "q": "É possível descer ao fundo do Cânion do Sumidouro?",
        "a": "O acesso ao fundo do cânion pelo leito do Rio Antas é possível em condições específicas de volume do rio e nível de experiência. Em épocas de estiagem, quando o rio está baixo, grupos experientes conseguem acessar o interior do cânion por caminhadas no leito rochoso. No entanto, esse acesso não é marcado oficialmente, exige conhecimento prévio da área e avaliação das condições hídricas. Após chuvas intensas ou no período de enchente do rio, o acesso ao fundo é perigoso e não recomendado.",
    },
    {
        "q": "Qual a melhor época para visitar o Cânion do Sumidouro?",
        "a": "Setembro a novembro e março a maio são os períodos mais recomendados: temperatura amena, vegetação verde e o Rio Antas com volume moderado. O verão gaúcho (dezembro-fevereiro) tem calor intenso e chuvas frequentes que aumentam o volume do rio e podem tornar o acesso a alguns mirantes escorregadio. O inverno (junho-agosto) pode trazer frio intenso e geada, mas os dias claros e a paisagem com névoa matinal tornam a experiência fotogêfica particularmente rica para quem não se importa com o frio.",
    },
    {
        "q": "O que ver na região além do Cânion do Sumidouro?",
        "a": "A região de São Marcos e da Serra Gaúcha oferece um roteiro complementar rico. Bento Gonçalves e Garibaldi, a poucos quilômetros, são o coração vitivinícola do Brasil — com visitas a vinícolas históricas e espumantes premiados. Caxias do Sul tem o Parque da Região Colonial Italiana e o Museu do Imigrante. Para quem quer mais natureza, os Cânions da Fortaleza e Itaimbezinho ficam a aproximadamente 100 quilômetros, na direção de Cambará do Sul — um roteiro de três dias que cobre os três cânions e a vinicultura gaúcha.",
    },
    {
        "q": "Precisa de guia para visitar o Cânion do Sumidouro?",
        "a": "Não é obrigatório para a trilha de borda, mas recomendado para quem quer acessar os pontos mais remotos ou descer ao fundo do cânion. O proprietário da área de acesso geralmente fornece orientações básicas sobre a trilha. Para a trilha padrão de borda, caminhantes com experiência em trilhas moderadas conseguem navegar sem guia usando GPS e o mapa da rota. Para grupos sem experiência em trilhas ou para quem quer fazer o acesso ao interior do cânion, um guia local de São Marcos é a escolha mais segura.",
    },
],

"serra-da-canastra": [
    {
        "q": "O que é possível ver na nascente do Rio São Francisco na Serra da Canastra?",
        "a": "A nascente do Rio São Francisco, chamada de Casca D'Anta, fica na zona de uso especial do Parque Nacional da Serra da Canastra. O broto da nascente é modesto em volume — um fio de água saindo de uma fenda na rocha — mas o significado simbólico é imenso. O Rio São Francisco percorrerá 2.863 quilômetros até chegar ao Oceano Atlântico entre Alagoas e Sergipe, passando por cinco estados e abastecendo dezenas de cidades nordestinas. Um painel interpretativo no local contextualiza a importância histórica e hídrica do ponto.",
    },
    {
        "q": "Qual é a Cachoeira Casca D'Anta e como chegar até ela?",
        "a": "A Cachoeira Casca D'Anta é a maior do Parque Nacional da Serra da Canastra, com 186 metros de queda, formada pelo próprio Rio São Francisco nos primeiros quilômetros após a nascente. É uma das poucas cachoeiras do Brasil onde é possível ver um rio grande — não apenas um riacho — despencando em queda livre de grande altura. O acesso é feito a partir da portaria de São Roque de Minas ou pelo trecho final da trilha principal do parque. A cachoeira tem capacidade de visitação controlada — chegue cedo em finais de semana.",
    },
    {
        "q": "É possível ver lobo-guará e tamanduá-bandeira na Serra da Canastra?",
        "a": "Sim. A Serra da Canastra tem uma das populações mais estáveis de lobo-guará e tamanduá-bandeira do Brasil, beneficiadas pela extensão dos campos preservados dentro do parque. O lobo-guará é crepuscular — visto principalmente ao amanhecer e ao entardecer, cruzando os campos na busca por lobeira (fruta-do-lobo, sua alimentação principal). O tamanduá-bandeira é mais difícil de avistar mas está presente. Capivaras, emas, seriemas e diversas espécies de gavião são comuns durante as caminhadas nos campos.",
    },
    {
        "q": "Precisa de guia para visitar o Parque Nacional da Serra da Canastra?",
        "a": "O guia não é obrigatório para as trilhas marcadas do parque. A entrada é feita pelas portarias, com pagamento da taxa de ingresso e orientação dos fiscais do ICMBio sobre as trilhas disponíveis. Para a trilha completa de 22 quilômetros até a Casca D'Anta, um guia ou mapa offline detalhado é recomendado para os trechos menos frequentados onde a sinalização é mais esparsa. Para visitas de um dia às principais cachoeiras, o auto-guiamento é tranquilo com os mapas fornecidos na portaria.",
    },
    {
        "q": "Quais são as melhores trilhas de um dia no Parque Nacional da Serra da Canastra?",
        "a": "Para visitas de um dia, as trilhas mais acessíveis saem da portaria de São Roque de Minas. A trilha da nascente do Rio São Francisco (16 km ida e volta) é a mais simbólica. A trilha da Cachoeira Casca D'Anta (acesso pela estrada interna do parque) permite ver a maior cachoeira sem grande percurso a pé. Para quem busca campos rupestres com fauna, a trilha do Mirante da Bandeirinha oferece vista panorâmica do planalto com boa probabilidade de avistar emas e lobos-guará no entardecer.",
    },
    {
        "q": "Como chegar ao Parque Nacional da Serra da Canastra?",
        "a": "O principal acesso é pela cidade de São Roque de Minas, a aproximadamente 330 quilômetros de Belo Horizonte e 480 quilômetros de Brasília. De BH, a rota mais comum é pela BR-262 até Piumhi e depois estrada estadual até São Roque de Minas. De carro é o transporte mais prático — o transporte público para a região é limitado. São Roque de Minas tem pousadas e restaurantes para hospedagem próximo ao parque. Sacramento, Delfinópolis e Medeiros são outras cidades com acesso às portarias secundárias do parque.",
    },
],

"parque-nacional-superagui": [
    {
        "q": "Como chegar ao Parque Nacional de Superagui?",
        "a": "O Parque Nacional de Superagui só tem acesso por barco — não existe estrada. O ponto de partida é Guaraqueçaba, município do litoral norte do Paraná, a aproximadamente 120 quilômetros de Curitiba (via Antonina ou via Morretes). Barcos regulares e lanchas fretadas conectam Guaraqueçaba à Vila de Superagui em trajeto de aproximadamente 1h30. De Curitiba, a opção mais prática é dirigir até Guaraqueçaba, pernoitar e pegar o barco no dia seguinte. Confirme horários de barco antes de partir — são limitados e dependem do clima.",
    },
    {
        "q": "Precisa de guia para trilhar no Parque Nacional de Superagui?",
        "a": "Sim. O guia é obrigatório para as trilhas dentro do Parque Nacional de Superagui. Os guias são moradores e ex-moradores da Vila de Superagui credenciados pelo ICMBio — contratar seus serviços é também uma forma direta de apoiar a economia da comunidade caiçara que vive dentro do parque. A contratação pode ser feita antecipadamente por agências de ecoturismo de Guaraqueçaba ou Curitiba, ou diretamente com os guias locais ao chegar na vila.",
    },
    {
        "q": "O que é o papagaio-de-cara-roxa e como avistá-lo em Superagui?",
        "a": "O papagaio-de-cara-roxa (Amazona brasiliensis) é uma espécie endêmica da Mata Atlântica costeira do sul do Brasil — ocorre apenas em um estreito trecho do litoral entre São Paulo e Santa Catarina. Está classificado como criticamente ameaçado e Superagui é o local com maior concentração da espécie. O avistamento é mais fácil no entardecer, quando bandos chegam para o dormitório coletivo nas árvores do manguezal — um dos espetáculos de natureza mais impressionantes do Sul do Brasil. O guia local conhece os melhores pontos de observação.",
    },
    {
        "q": "Qual a duração mínima recomendada para visitar Superagui?",
        "a": "Dois dias completos é o mínimo para uma experiência significativa, mas três a quatro dias permitem conhecer as trilhas da mata, a Praia Deserta, os canais de manguezal de barco e o espetáculo noturno dos papagaios-de-cara-roxa. A hospedagem na Vila de Superagui é simples e acolhedora — pousadas familiares geridas por moradores locais. Uma noite não compensa a logística de chegar e ir embora em menos de 24 horas; aproveite para desacelerar no ritmo da ilha.",
    },
    {
        "q": "A Praia Deserta de Superagui realmente não tem acesso por terra?",
        "a": "Corretamente descrita: a Praia Deserta de Superagui tem 40 quilômetros de extensão e não tem acesso por terra de nenhuma estrada pública ou trilha de veículos. O único acesso é por barco pela face oceânica ou pela trilha interna da ilha, que conecta a Vila de Superagui à borda da praia após aproximadamente 4-5 quilômetros de mata de restinga. Essa inacessibilidade é o que a mantém completamente intocada: sem infraestrutura turística, sem quiosques, sem trilha de buggy — apenas areia, vento e oceano.",
    },
    {
        "q": "Qual a melhor época para visitar o Parque Nacional de Superagui?",
        "a": "Março a novembro é o período com menor volume de chuvas e mar mais calmo para a travessia de barco. O inverno paranaense (junho-agosto) tem temperaturas mais baixas no litoral, mas dias claros e mar tranquilo. O verão (dezembro-fevereiro) é quente e chuvoso, com eventual mar agitado que pode atrasar ou cancelar barcos. Para observação de aves, especialmente o papagaio-de-cara-roxa, setembro e outubro são excelentes. Para quem quer praias desertas com sol, dezembro a fevereiro tem os dias mais quentes, apesar do risco de chuva.",
    },
],

"pico-do-caraca": [
    {
        "q": "Os lobos-guará aparecem todo dia no Santuário do Caraça?",
        "a": "A aparição dos lobos-guará no claustro da Igreja Nossa Senhora Mãe dos Homens é regular mas não garantida em cada noite. Os frades colocam alimento no horário específico informado pela recepção (geralmente entre 18h30 e 20h conforme a estação), e os lobos aparecem com frequência alta — mas são animais silvestres com comportamento próprio. A taxa de aparição reportada por visitantes é alta, mas dias de lua cheia, barulho excessivo ou presença de muita gente podem alterar o comportamento. A recepção do Santuário informa se houve aparição nas noites anteriores.",
    },
    {
        "q": "Como funciona a hospedagem no Santuário do Caraça?",
        "a": "O Santuário do Caraça oferece hospedagem no próprio Colégio histórico, em quartos simples com banheiro compartilhado ou privativo, refeições no refeitório original e café da manhã incluso. A experiência é austera e encantadora: silêncio, sinos de igreja, jardins históricos e a atmosfera de um lugar onde o tempo parece diferente. A capacidade é limitada e a reserva com antecedência é fundamental, especialmente em finais de semana, julho e feriados. O Santuário é fechado às segundas-feiras para visitação. Consulte a disponibilidade pelo site ou telefone da Congregação da Missão.",
    },
    {
        "q": "Qual a dificuldade real da subida ao Pico do Caraça?",
        "a": "O Pico do Caraça é classificado como trilha difícil pelo desnível de 830 metros em 6 quilômetros de subida e pelo terreno irregular de Mata Atlântica e campos rupestres. Não há trechos de escalada, mas a inclinação é constante e exigente. Caminhantes com condição física regular e alguma experiência em trilhas de montanha conseguem completar sem grandes dificuldades em 3 a 4 horas de subida. A descida, pelo mesmo caminho, pode ser mais exigente para os joelhos — bastões de trekking são recomendados.",
    },
    {
        "q": "Precisa de guia para subir ao Pico do Caraça?",
        "a": "O guia não é obrigatório para a trilha ao Pico do Caraça. O Santuário fornece mapa do percurso na recepção e a trilha tem sinalização razoável. Caminhantes com experiência em trilhas de montanha conseguem navegar sem acompanhamento. Para grupos sem experiência prévia ou para quem quer informações sobre a fauna e flora da reserva ao longo do caminho, guias locais contratados pelo Santuário são disponíveis. Confirme com a recepção as condições da trilha antes de sair — alguns trechos podem estar interditados após chuvas.",
    },
    {
        "q": "O que ver no Santuário do Caraça além da trilha e dos lobos?",
        "a": "O Santuário do Caraça tem muito mais para oferecer além da trilha principal e do espetáculo dos lobos. A Igreja Nossa Senhora Mãe dos Homens, do século XIX, tem acervo histórico valioso. O Museu do Caraça expõe objetos e documentos do colégio desde sua fundação em 1820. O lago do Santuário tem trilha circular de baixa dificuldade com vistas dos paredões rochosos. As trilhas secundárias dentro da reserva levam a cascatas e mirantes com menos visitantes. A biblioteca histórica e os jardins são abertos para contemplação.",
    },
    {
        "q": "Qual a melhor época para visitar o Pico do Caraça?",
        "a": "Abril a outubro é a estação seca, com trilha mais transitável e visibilidade máxima do cume. O inverno (junho-agosto) pode trazer frio intenso e geada nos campos do pico, mas os dias são claros e as vistas excepcionais. A floração dos campos rupestres acontece principalmente entre agosto e outubro — o percurso fica colorido de sempre-vivas e outras espécies endêmicas. O verão chuvoso (novembro-março) tem a reserva mais verde e algumas cachoeiras com mais volume, mas o pico frequentemente fica coberto de névoa.",
    },
],

"lagoa-azul-bonito": [
    {
        "q": "Por que a água da Lagoa Azul de Bonito é tão azul?",
        "a": "A cor azul-turquesa da Lagoa Azul é resultado da química da água, não de tintura ou efeito especial. As águas de Bonito são extremamente ricas em carbonato de cálcio (calcário) dissolvido, que precipita em forma de partículas microscópicas em suspensão. Essas partículas refratam a luz solar de maneira específica, absorvendo as frequências do vermelho e refletindo as do azul — o mesmo princípio que torna o céu azul. Quanto mais calcário e mais luz, mais intenso o azul. A visibilidade de até 30 metros é resultado dessa mesma pureza.",
    },
    {
        "q": "Quando acontece o raio de sol na Lagoa Azul de Bonito?",
        "a": "O famoso fenômeno do raio de sol que ilumina as stalactites subaquáticas da Lagoa Azul acontece no período de junho a julho, entre aproximadamente 9h e 10h da manhã. Nesse período do ano e nesse horário específico, o ângulo solar é preciso o suficiente para que a luz penetre pela abertura da gruta, atravesse a superfície da lagoa e ilumine as estalactites submersas em azul intenso — criando um efeito que parece de ficção científica mas é puramente astronômico e geológico. Para ver esse espetáculo, reserve exatamente para esse horário e período.",
    },
    {
        "q": "Quanto custa visitar a Lagoa Azul em Bonito?",
        "a": "O pacote da Lagoa Azul inclui a trilha de acesso, o snorkeling com equipamento (máscara, snorkel e colete) e o guia obrigatório. O preço varia por agência e temporada, mas gira em torno de R$ 160 a R$ 250 por pessoa na alta temporada. Reserva com antecedência é fundamental — o número de vagas diárias é limitado e a Lagoa Azul esgota rapidamente em julho e nos meses de férias. As agências em Bonito organizam o pacote completo, frequentemente combinado com outras atrações da cidade.",
    },
    {
        "q": "O que ver além da Lagoa Azul em Bonito?",
        "a": "Bonito tem um dos cardápios de turismo de natureza mais completos do Brasil. O Rio da Prata é o flutuoduto mais famoso — nadar com flutuadores num rio de visibilidade cristalina com cardumes de dourado. A Gruta do Mimoso tem uma das piscinas subterrâneas mais bonitas do interior do país. O Abismo Anhumas combina rapel numa gruta e mergulho em lago subterrâneo para perfis mais aventureiros. A Serra da Bodoquena tem trilhas e cachoeiras no entorno. Um roteiro de quatro a cinco dias em Bonito consegue combinar as principais atrações sem pressa.",
    },
    {
        "q": "É possível mergulhar com cilindro na Lagoa Azul?",
        "a": "O mergulho autônomo com cilindro não é permitido na Lagoa Azul — apenas snorkeling de superfície é autorizado para o público geral. O mergulho com cilindro em Bonito é feito em outros pontos específicos da região, como o Abismo Anhumas, que exige certificação de mergulho e treino prévio. Para snorkeling iniciante, a Lagoa Azul é perfeita — o colete salva-vidas fornecido mantém o visitante na superfície sem esforço e a visibilidade de 30 metros permite ver todo o fundo da lagoa e as stalactites subaquáticas confortavelmente.",
    },
    {
        "q": "A Lagoa Azul é adequada para crianças?",
        "a": "Sim, a Lagoa Azul é adequada para crianças a partir de aproximadamente 5 anos que não tenham medo de água. O colete salva-vidas é obrigatório para todos e garante segurança mesmo para quem não sabe nadar. A trilha de acesso de 3 quilômetros é plana e fácil para crianças com disposição básica. O snorkeling em água turquesa com cardumes de peixe é uma experiência marcante que crianças geralmente adoram. Certifique-se de usar apenas protetor solar biodegradável ou mineral — os protetores convencionais são proibidos na lagoa.",
    },
],

"pedra-azul": [
    {
        "q": "Por que a Pedra Azul muda de cor?",
        "a": "A coloração azul-acinzentada da Pedra Azul é resultado da combinação entre a composição mineralógica do granito, a umidade superficial da rocha e o ângulo de incidência da luz. O granito do monólito tem composição específica que, quando úmido — o que é frequente na Mata Atlântica de altitude — e iluminado pela luz rasante do entardecer, reflete tonalidades no espectro do azul e cinza. O efeito é mais pronunciado nas horas finais da tarde e em dias com umidade elevada. Ao meio-dia com sol direto, a pedra aparece mais cinza-claro.",
    },
    {
        "q": "Precisa de guia para visitar o Parque Estadual da Pedra Azul?",
        "a": "Sim, o guia é obrigatório para a trilha principal do Parque Estadual da Pedra Azul. A exigência existe para controlar o fluxo de visitantes, proteger a vegetação nativa e garantir segurança nas áreas das piscinas, onde as rochas molhadas representam risco de queda. Os guias são credenciados pelo Instituto Estadual de Meio Ambiente e Recursos Hídricos (IEMA) e contratados no Centro de Visitantes do parque ou previamente por agências da região.",
    },
    {
        "q": "Qual a melhor trilha e o melhor horário para ver a Pedra Azul?",
        "a": "A trilha principal de 6 quilômetros que leva às piscinas naturais na base do monólito é a experiência central do parque. O melhor horário para ver o efeito de coloração azul da pedra é entre 15h e 18h, quando a luz rasante do final da tarde bate na face sul do granito. Para as piscinas com sol, chegue antes das 13h — a face das piscinas fica em sombra a partir do meio da tarde. Quem consegue fazer os dois momentos — as piscinas pela manhã e o entardecer contemplando o monólito de longe — tem a experiência mais completa.",
    },
    {
        "q": "Como chegar ao Parque Estadual da Pedra Azul?",
        "a": "O Parque Estadual da Pedra Azul fica em Domingos Martins, a aproximadamente 75 quilômetros de Vitória pela BR-262, a rodovia que liga o Espírito Santo a Minas Gerais. De carro, é facilmente acessível como passeio de um dia saindo de Vitória. De ônibus, a linha Vitória-Domingos Martins passa pela BR-262 próximo ao parque. A região de Pedra Azul (o bairro no entorno do parque) tem pousadas, restaurantes e estrutura turística bem desenvolvida para quem quer pernoitar.",
    },
    {
        "q": "As piscinas naturais da Pedra Azul são abertas para banho?",
        "a": "Sim, as piscinas naturais na base do monólito são o principal atrativo do parque e o banho é permitido nas áreas sinalizadas. As piscinas são concavidades naturais no granito preenchidas por água de nascente, com temperatura fria e aparência de turquesa pelo reflexo da rocha e da vegetação. O guia indica quais piscinas estão abertas para banho em cada visita — o volume de água e as condições de segurança variam conforme a estação. Protetores solares convencionais são proibidos; use apenas protetor mineral ou solar biodegradável.",
    },
    {
        "q": "Qual a melhor época para visitar o Parque Estadual da Pedra Azul?",
        "a": "Maio a setembro é a estação seca, com trilha mais transitável, piscinas mais limpas e o efeito de coloração azul da pedra mais intenso — a umidade específica que potencializa a cor é mais frequente nesse período. O verão capixaba (outubro a março) tem chuvas que podem fechar a trilha temporariamente e turvar as piscinas. A floração da Mata Atlântica de altitude acontece principalmente entre setembro e novembro, tornando o percurso especialmente rico em bromélias e orquídeas com flores. Os finais de semana de julho têm alta demanda — chegue antes das 8h ou reserve com antecedência.",
    },
],

"pedra-da-gavea": [
    {
        "q": "Precisa de guia para subir a Pedra da Gávea?",
        "a": "Sim. O guia credenciado pelo ICMBio é obrigatório para a trilha da Pedra da Gávea — exigência tanto legal quanto de segurança real. O trecho de escalada com corda fixada não é tecnicamente muito difícil, mas exige orientação adequada para ser executado com segurança. Guias sem credenciamento ICMBio operam ilegalmente e não têm seguro ou capacitação verificada para o trecho técnico. A contratação é feita por agências de trilhas no Rio de Janeiro com antecedência — não há guia de plantão no início da trilha.",
    },
    {
        "q": "Qual a diferença entre a Pedra da Gávea e o Pão de Açúcar como mirante do Rio de Janeiro?",
        "a": "São experiências completamente diferentes. O Pão de Açúcar (396 metros) é acessado por bondinho e recebe dezenas de milhares de visitantes por mês — é turismo de massa com conforto total. A Pedra da Gávea (844 metros) exige 5 a 7 horas de trilha exigente com trecho de escalada e recebe apenas grupos pequenos — é trekking de montanha. A vista da Gávea é mais alta e mais abrangente: é possível ver o Pão de Açúcar de cima. Quem sobe a Gávea por esforço próprio tem uma conexão com a cidade completamente diferente de quem sobe de bondinho.",
    },
    {
        "q": "O trecho de escalada da Pedra da Gávea é perigoso para quem nunca escalou?",
        "a": "O trecho de escalada da Gávea é de grau técnico baixo — não requer treinamento de escalada prévia — mas envolve exposição vertical que pode ser desafiadora psicologicamente para quem tem acrofobia. A fenda na rocha com corda fixada tem apoios suficientes para progressão segura com orientação do guia. O risco principal não é técnico, mas de pânico em altitude em pessoas que não se conhecem bem em situações de exposição. Seja honesto com o guia sobre seu histórico com alturas antes de começar a subida.",
    },
    {
        "q": "Qual a melhor época para subir a Pedra da Gávea?",
        "a": "Abril a outubro é a janela mais segura: menor probabilidade de chuva, rocha mais seca e maior clareza para a vista do cume. O verão carioca (dezembro-março) tem chuvas frequentes à tarde e neblina matinal que pode cobrir o topo completamente. Julho é o mês mais seco e tem os melhores dias para visibilidade máxima do Rio. Suba sempre de manhã — a chuva no Rio de Janeiro típicamente acontece à tarde e a névoa matinal geralmente se dissipa até às 9h. O guia cancela a trilha em caso de chuva ou previsão de tempestade.",
    },
    {
        "q": "A Pedra da Gávea é a trilha mais difícil do Parque Nacional da Tijuca?",
        "a": "Sim, a Pedra da Gávea é a trilha mais exigente do Parque Nacional da Tijuca pelo desnível de 820 metros, o terreno irregular e o trecho de escalada. Outras trilhas do parque, como o Pico da Tijuca (1.021 metros, o ponto mais alto do parque), são mais altas em altitude mas têm acesso menos técnico. Para quem quer começar pelo Parque da Tijuca antes de tentar a Gávea, as trilhas da Cascatinha Taunay, Corcovado a pé e Pico da Tijuca são progressões naturais de dificuldade crescente.",
    },
    {
        "q": "Quanto tempo leva a trilha da Pedra da Gávea?",
        "a": "O percurso completo de ida e volta leva de 5 a 7 horas dependendo do ritmo, do tempo no cume e das paradas para descanso e fotografias. A subida leva de 3 a 4 horas, com o trecho de escalada consumindo de 30 a 60 minutos dependendo do grupo. A descida leva de 2 a 3 horas. A recomendação é sair no máximo às 7h para garantir chegada ao cume antes de eventual névoa da tarde e retorno antes do anoitecer. Não faça o percurso com previsão de retorno no escuro sem experiência e equipamento adequado de iluminação.",
    },
],

}  # end TRAIL_FAQ


_ADSENSE_CLIENT = "ca-pub-2482023752745520"
_AD_SLOT_MID    = "3721854690"   # TRAIL_AFTER_INTRO — after 3rd paragraph
_AD_SLOT_END    = "5038274619"   # GUIDES_AFTER_EDITORIAL — end of editorial

AD_CSS = """\
  <style>
    .trekko-ad{max-width:800px;margin:1.75rem auto;overflow:hidden;text-align:center}
    .trekko-ad ins{display:block!important;max-width:100%}
    @media(max-width:640px){.trekko-ad{margin:1.25rem auto}}
  </style>"""

_AD_LAZY_SCRIPT = """\
  <script>
  (function(){
    if(!("IntersectionObserver"in window))return;
    var els=document.querySelectorAll("#trekko-editorial .trekko-ad ins.adsbygoogle");
    if(!els.length)return;
    var seen=new WeakSet();
    var obs=new IntersectionObserver(function(entries,o){
      entries.forEach(function(e){
        if(!e.isIntersecting||seen.has(e.target))return;
        seen.add(e.target);o.unobserve(e.target);
        try{(window.adsbygoogle=window.adsbygoogle||[]).push({});}catch(err){}
      });
    },{rootMargin:"300px"});
    els.forEach(function(el){obs.observe(el);});
  })();
  </script>"""


def _ad_html(slot):
    return (
        f'\n<div class="trekko-ad" aria-label="Anúncio">'
        f'<ins class="adsbygoogle" style="display:block"'
        f' data-ad-client="{_ADSENSE_CLIENT}"'
        f' data-ad-slot="{slot}"'
        f' data-ad-format="auto"'
        f' data-full-width-responsive="true"></ins></div>\n'
    )


def _inject_editorial_ads(content):
    """Insert ad after 3rd </p> and append one at end of content."""
    # Mid-content: after 3rd closing paragraph tag
    count, pos = 0, 0
    while count < 3:
        idx = content.find("</p>", pos)
        if idx == -1:
            break
        count += 1
        pos = idx + 4
    if count == 3:
        content = content[:pos] + _ad_html(_AD_SLOT_MID) + content[pos:]
    # End-of-content ad
    content += _ad_html(_AD_SLOT_END)
    return content


FAQ_CSS = """\
  <style>
    #trekko-faq{font-family:Inter,system-ui,sans-serif;background:#fff;border-top:4px solid #15803d;padding:3rem 1rem 4rem;color:#1e293b;line-height:1.8}
    #trekko-faq .fq{max-width:800px;margin:0 auto}
    #trekko-faq h2{font-family:Sora,system-ui,sans-serif;font-size:1.35rem;font-weight:700;color:#0f172a;margin:0 0 1.5rem}
    #trekko-faq details{border:1px solid #e2e8f0;border-radius:8px;margin-bottom:.75rem;overflow:hidden}
    #trekko-faq details[open]{border-color:#15803d}
    #trekko-faq summary{font-weight:600;font-size:.97rem;color:#0f172a;padding:.9rem 1.1rem;cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:.5rem}
    #trekko-faq summary::-webkit-details-marker{display:none}
    #trekko-faq summary::after{content:'+';font-size:1.25rem;color:#15803d;flex-shrink:0;transition:transform .2s}
    #trekko-faq details[open] summary::after{content:'−'}
    #trekko-faq .fa{padding:.1rem 1.1rem 1rem;font-size:.93rem;color:#334155}
    @media(max-width:640px){#trekko-faq{padding:2rem .75rem 3rem}#trekko-faq h2{font-size:1.15rem}#trekko-faq summary{font-size:.92rem}}
  </style>"""


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


def _is_free(fee):
    if not fee:
        return True
    return fee.strip().lower() in ("gratuito", "gratuita", "grátis", "gratis",
                                   "gratuito (guia obrigatório)", "gratuito (guia obrigatorio)")


def build_jsonld(t):
    slug = t["slug"]
    canonical = "https://trekko.com.br/trilha/" + slug
    geo = {"@type": "GeoCoordinates"}
    if t.get("lat") is not None and t.get("lng") is not None:
        geo["latitude"] = t["lat"]
        geo["longitude"] = t["lng"]
    graph = [
        {
            "@type": "Organization",
            "@id": "https://trekko.com.br/#organization",
            "name": "Trekko",
            "url": "https://trekko.com.br",
            "logo": "https://trekko.com.br/android-chrome-512x512.png",
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Trekko", "item": "https://trekko.com.br"},
                {"@type": "ListItem", "position": 2, "name": "Trilhas", "item": "https://trekko.com.br/trilhas"},
                {"@type": "ListItem", "position": 3, "name": UF_NAMES.get(t["uf"], t["uf"]), "item": "https://trekko.com.br/trilhas/" + UF_SLUGS.get(t["uf"], t["uf"].lower())},
                {"@type": "ListItem", "position": 4, "name": t["name"], "item": canonical},
            ],
        },
        {
            "@type": "TouristAttraction",
            "@id": canonical,
            "name": t["name"],
            "description": t["shortDescription"],
            "url": canonical,
            "image": "https://trekko.com.br" + t["imageUrl"],
            "touristType": "Trilha / Trekking",
            "isAccessibleForFree": _is_free(t.get("entranceFee", "")),
            "geo": geo,
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "BR",
                "addressRegion": t["uf"],
                "addressLocality": t["city"],
            },
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
    ]
    faqs = TRAIL_FAQ.get(slug)
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": faq["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": faq["a"]},
                }
                for faq in faqs
            ],
        })
    data = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(data, ensure_ascii=False)


def build_faq_section(t):
    faqs = TRAIL_FAQ.get(t["slug"])
    if not faqs:
        return ""
    items = "\n".join(
        f'  <details itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">\n'
        f'    <summary itemprop="name">{faq["q"]}</summary>\n'
        f'    <div class="fa" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">'
        f'<p itemprop="text">{faq["a"]}</p></div>\n'
        f'  </details>'
        for faq in faqs
    )
    return (
        f'<section id="trekko-faq" aria-label="Perguntas frequentes sobre {t["name"]}"'
        f' itemscope itemtype="https://schema.org/FAQPage">\n'
        f'  <div class="fq">\n'
        f'    <h2>Perguntas frequentes sobre {t["name"]}</h2>\n'
        f'{items}\n'
        f'  </div>\n'
        f'</section>'
    )


def build_editorial_section(t):
    slug = t["slug"]
    content = TRAIL_EDITORIAL.get(slug, "")
    if not content:
        return ""
    diff = DIFF_LABELS.get(t["difficulty"], t["difficulty"])
    content_with_ads = _inject_editorial_ads(content)
    return f"""\
<section id="trekko-editorial" aria-label="Guia editorial: {t['name']}">
  <div class="ei">
    {content_with_ads}
    <div class="ef">
      <span>Trilha: <strong>{t['name']}</strong></span> &nbsp;·&nbsp;
      <span>Dificuldade: <strong>{diff}</strong></span> &nbsp;·&nbsp;
      <span>Distância: <strong>{t['distanceKm']} km</strong></span> &nbsp;·&nbsp;
      <span>Duração estimada: <strong>{t['estimatedTime']}</strong></span><br>
      <span>Informações verificadas em: <strong>Maio de 2025</strong></span> &nbsp;·&nbsp;
      <span>Fonte editorial: Trekko — trilhas verificadas no Brasil</span>
    </div>
  </div>
</section>"""


def _haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


_DIFF_BADGE = {
    "easy": ("Fácil", "easy"),
    "moderate": ("Moderado", "moderate"),
    "hard": ("Difícil", "hard"),
    "expert": ("Especialista", "expert"),
}


def build_nearby_section(t, all_trails):
    lat, lng = t.get("lat"), t.get("lng")
    if lat is None or lng is None:
        return ""

    candidates = []
    for other in all_trails:
        if other["slug"] == t["slug"]:
            continue
        olat, olng = other.get("lat"), other.get("lng")
        if olat is None or olng is None:
            continue
        if other.get("uf") != t.get("uf"):
            continue
        dist = _haversine_km(lat, lng, olat, olng)
        if dist <= 100:
            candidates.append((dist, other))

    candidates.sort(key=lambda x: x[0])
    candidates = candidates[:6]

    if len(candidates) < 2:
        return ""

    cards = []
    for dist_km, other in candidates:
        label, css_key = _DIFF_BADGE.get(other["difficulty"], (other["difficulty"], "moderate"))
        dist_str = f"{dist_km:.0f} km de distância"
        cards.append(f"""\
      <a class="tn-card" href="/trilha/{other['slug']}/" aria-label="{other['name']}">
        <img src="{other['imageUrl']}" alt="{other['name']}" loading="lazy" width="400" height="140">
        <div class="tn-card-body">
          <p class="tn-name">{other['name']}</p>
          <div class="tn-meta">
            <span class="tn-badge tn-badge-{css_key}">{label}</span>
            <span class="tn-dist">{dist_str}</span>
          </div>
        </div>
      </a>""")

    cards_html = "\n".join(cards)
    return f"""\
<section id="trekko-nearby" aria-label="Trilhas próximas">
  <div class="tn-inner">
    <h2>Trilhas próximas</h2>
    <div class="tn-grid">
{cards_html}
    </div>
  </div>
</section>"""


def make_trail_title(t):
    """Build SEO title ≤ 60 chars: name — city, UF | Trekko (with fallbacks)."""
    name = t["name"]
    uf = t["uf"]
    city = t["city"]

    candidate = f"{name} — {city}, {uf} | Trekko"
    if len(candidate) <= 60:
        return candidate

    if " / " in city:
        first_city = city.split(" / ")[0]
        candidate = f"{name} — {first_city}, {uf} | Trekko"
        if len(candidate) <= 60:
            return candidate

    candidate = f"{name}, {uf} | Trekko"
    if len(candidate) <= 60:
        return candidate

    suffix = f", {uf} | Trekko"
    return name[: 60 - len(suffix)].rstrip() + suffix


def make_trail_desc(t):
    """Build description following the standard template."""
    diff = DIFF_LABELS.get(t["difficulty"], t["difficulty"]).lower()
    city = t["city"].split(" / ")[0] if " / " in t["city"] else t["city"]
    return (
        f"Faça a {t['name']}: {t['distanceKm']}km, nível {diff}, em {city}. "
        f"Veja roteiro completo, como chegar, equipamentos e guias disponíveis."
    )


def build_slug_page(t, redirect_script, all_trails=None):
    slug = t["slug"]
    canonical = "https://trekko.com.br/trilha/" + slug
    title = make_trail_title(t)
    desc = make_trail_desc(t)
    image = "https://trekko.com.br" + t["imageUrl"]
    jsonld = build_jsonld(t)
    editorial = build_editorial_section(t)
    faq = build_faq_section(t)
    nearby = build_nearby_section(t, all_trails or [])

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
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{t['shortDescription']}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{image}" />
  <link rel="preload" as="image" href="{t['imageUrl']}" fetchpriority="high">
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
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" /></noscript>
  <script type="application/ld+json">{jsonld}</script>
  <script defer src="/assets/trekko-analytics.js"></script>
  <style>#root{{min-height:100svh}}</style>
{EDITORIAL_CSS}
{FAQ_CSS}
{NEARBY_CSS}
{DISCLAIMER_CSS}

{BREADCRUMB_CSS}
{AD_CSS}

  {redirect_script}
  <script type="module" crossorigin src="/assets/index-DSKK19TW.js"></script>
  <link rel="modulepreload" crossorigin href="/assets/react-vendor-DViTTRkQ.js">
  <link rel="modulepreload" crossorigin href="/assets/radix-ui-D-C9zAgG.js">
  <link rel="stylesheet" crossorigin href="/assets/index-CKkMVUOE.css">
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <nav class="trekko-bc" aria-label="Navegação estrutural">
    <div class="container"><ol>
      <li><a href="/">Trekko</a></li>
      <li><a href="/trilhas">Trilhas</a></li>
      <li><a href="/trilhas/{UF_SLUGS.get(t['uf'], t['uf'].lower())}">{UF_NAMES.get(t['uf'], t['uf'])}</a></li>
      <li><span aria-current="page">{t['name']}</span></li>
    </ol></div>
  </nav>
  <div id="root"></div>
  {editorial}
  {faq}
  {nearby}
  {DISCLAIMER_HTML}
{_AD_LAZY_SCRIPT}
</body>
</html>"""


def build_numeric_page(t):
    slug = t["slug"]
    canonical_slug = "https://trekko.com.br/trilha/" + slug
    title = make_trail_title(t)
    desc = make_trail_desc(t)
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
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex, follow" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{canonical_slug}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical_slug}" />
  <meta property="og:image" content="{image}" />
  <link rel="preload" as="image" href="{t['imageUrl']}" fetchpriority="high">
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
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" /></noscript>
  <script defer src="/assets/trekko-analytics.js"></script>
  <style>#root{{min-height:100svh}}</style>
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
    write(os.path.join(BASE, "trilha", t["slug"], "index.html"), build_slug_page(t, redirect_script, trails))
    write(os.path.join(BASE, "trilha", str(t["id"]), "index.html"), build_numeric_page(t))

print(f"\nDone: {len(trails)*2} files ({len(trails)} slug + {len(trails)} numeric)")
