#!/usr/bin/env python3
"""Generates trail detail pages: SEO head + static editorial body + React SPA root."""
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

}  # end TRAIL_EDITORIAL


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
    geo = {"@type": "GeoCoordinates"}
    if t.get("lat") is not None and t.get("lng") is not None:
        geo["latitude"] = t["lat"]
        geo["longitude"] = t["lng"]
    data = {
        "@context": "https://schema.org",
        "@graph": [
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
                    {"@type": "ListItem", "position": 3, "name": t["name"], "item": canonical},
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
        ],
    }
    return json.dumps(data, ensure_ascii=False)


def build_editorial_section(t):
    slug = t["slug"]
    content = TRAIL_EDITORIAL.get(slug, "")
    if not content:
        return ""
    diff = DIFF_LABELS.get(t["difficulty"], t["difficulty"])
    return f"""\
<section id="trekko-editorial" aria-label="Guia editorial: {t['name']}">
  <div class="ei">
    {content}
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


def build_slug_page(t, redirect_script):
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
    editorial = build_editorial_section(t)

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
{EDITORIAL_CSS}
  {redirect_script}
  <script type="module" crossorigin src="/assets/index-DSKK19TW.js"></script>
  <link rel="modulepreload" crossorigin href="/assets/react-vendor-DViTTRkQ.js">
  <link rel="modulepreload" crossorigin href="/assets/radix-ui-D-C9zAgG.js">
  <link rel="stylesheet" crossorigin href="/assets/index-CKkMVUOE.css">
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <div id="root"></div>
  {editorial}
</body>
</html>"""


def build_numeric_page(t):
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
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
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
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'" />
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" /></noscript>
  <script defer src="/assets/trekko-analytics.js"></script>
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
