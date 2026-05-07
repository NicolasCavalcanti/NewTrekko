#!/usr/bin/env python3
"""Generates static local-intent landing pages by state, city, park, and difficulty."""

import json, os, re, unicodedata
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "data", "trails.json")) as f:
    trails = [t for t in json.load(f) if t.get("status") == "published"]

print("Loading guides...")
with open(os.path.join(BASE, "data", "guides.json")) as f:
    all_guides = json.load(f)
print(f"Loaded {len(all_guides)} guides.")

# ── Constants ──────────────────────────────────────────────────────────────
DIFF_LABELS = {"easy": "Fácil", "moderate": "Moderado", "hard": "Difícil", "expert": "Especialista"}
DIFF_CSS    = {"easy": "easy", "moderate": "moderate", "hard": "hard", "expert": "expert"}
DIFF_SLUGS  = {"easy": "para-iniciantes", "moderate": "moderado", "hard": "dificil", "expert": "especialista"}

UF_NAMES = {
    "RR": "Roraima", "RJ": "Rio de Janeiro", "GO": "Goiás",
    "SP": "São Paulo", "MG": "Minas Gerais", "RS": "Rio Grande do Sul",
    "SC": "Santa Catarina", "CE": "Ceará",
}
UF_SLUGS = {
    "RR": "roraima",       "RJ": "rio-de-janeiro",  "GO": "goias",
    "SP": "sao-paulo",     "MG": "minas-gerais",     "RS": "rio-grande-do-sul",
    "SC": "santa-catarina","CE": "ceara",
}
UF_PREP = {
    "RR": "em Roraima",         "RJ": "no Rio de Janeiro",  "GO": "em Goiás",
    "SP": "em São Paulo",       "MG": "em Minas Gerais",     "RS": "no Rio Grande do Sul",
    "SC": "em Santa Catarina",  "CE": "no Ceará",
}
# Pages that already exist — skip
EXISTING_STATE_SLUGS = {"rio-de-janeiro", "sao-paulo", "minas-gerais"}
EXISTING_DIFF_SLUGS  = {"para-iniciantes"}

# ── Editorial content ──────────────────────────────────────────────────────
STATE_CONTENT = {
    "RR": {
        "subtitle": "O extremo norte do Brasil guarda um dos trekking mais épicos do planeta: o Monte Roraima, tepui milenar na tríplice fronteira.",
        "editorial": "Roraima é o estado mais ao norte do Brasil e abriga uma das expedições mais desafiadoras da América do Sul. O Monte Roraima, com seus 2.810 m de altitude, é uma das formações geológicas mais antigas da Terra — um tepui de aproximadamente 2 bilhões de anos que inspirou o romance 'O Mundo Perdido' e o filme 'UP'. A travessia de 48 km exige guia credenciado, boa condição física e planejamento logístico detalhado.",
        "tips": [
            ("Contrate guia obrigatório", "A trilha do Monte Roraima exige acompanhamento de guia indígena credenciado pela comunidade Ingarikó. Não há como fazer o percurso sem esse acompanhamento."),
            ("Planeje 6 a 8 dias", "A expedição completa leva de 6 a 8 dias, incluindo aclimatação e dias no topo do tepui. Não subestime o tempo necessário."),
            ("Prepare-se para altitude", "O topo do Roraima fica a 2.810 m. Leve camadas térmicas — as noites são frias mesmo na Amazônia tropical."),
            ("Acesso via Boa Vista ou Santa Elena", "A base da trilha fica em Uiramutã. O acesso costuma ser feito via Boa Vista (BR) ou pela Venezuela. Confirme logística com o guia."),
            ("Melhor época: outubro a abril", "O período com menos chuvas no topo é de outubro a abril. Evite maio a setembro, quando o tepui fica envolto em neblina densa e os caminhos ficam enlameados."),
            ("Equipamento completo de camping", "Leve barraca, saco de dormir (até 5°C), filtro de água e comida para todos os dias. Não há abastecimento no percurso."),
        ],
        "faqs": [
            ("O Monte Roraima realmente exige guia obrigatório?",
             "Sim. O acesso ao Monte Roraima no lado brasileiro passa pela Terra Indígena Raposa Serra do Sol e é obrigatório o acompanhamento de guia indígena credenciado pela comunidade. Sem isso, não há acesso legal à trilha."),
            ("Qual o melhor ponto de partida para o Monte Roraima?",
             "A base da trilha fica na aldeia de Paraitepui, no município de Uiramutã (RR). O acesso é geralmente feito via Boa Vista ou pela Venezuela (Santa Elena de Uairén). A maioria dos grupos parte de Boa Vista e faz a logística de veículo e guia com antecedência."),
            ("Quanto custa uma expedição ao Monte Roraima?",
             "O custo varia com o número de participantes, dias de expedição e pacote contratado. Uma expedição básica (6 dias, grupo de 4 pessoas) pode variar entre R$ 2.000 e R$ 4.000 por pessoa, incluindo guia, transporte interno e acampamentos. Consulte operadoras locais em Boa Vista."),
            ("Preciso de preparo físico especial para o Roraima?",
             "Sim. A trilha tem 48 km com trechos de escalada técnica (a 'Rampa'), carregamento de mochila pesada e noites em altitude. É fundamental ter condicionamento cardiovascular e experiência prévia em trekking de múltiplos dias."),
            ("Quais documentos preciso para entrar na terra indígena?",
             "Para brasileiros, basta RG ou CPF. Estrangeiros precisam de passaporte válido. Não é exigida autorização prévia da FUNAI para turistas acompanhados de guia indígena credenciado, mas confirme a regulamentação vigente com o guia ou operadora contratada."),
        ],
        "related_trails": "/trilhas",
        "hero_image": "/trails/x3cCqIWOMgkN.jpg",
    },
    "GO": {
        "subtitle": "O coração do Cerrado brasileiro abriga cachoeiras cristalinas, formações rochosas únicas e o Parque Nacional da Chapada dos Veadeiros.",
        "editorial": "Goiás é um dos destinos de ecoturismo mais completos do Brasil. A Chapada dos Veadeiros, no entorno de Alto Paraíso de Goiás, combina trilhas em campo cerrado, quedas d'água espetaculares e formações rochosas esculpidas por milhões de anos. O Parque Nacional da Chapada dos Veadeiros é Patrimônio Natural da Humanidade pela UNESCO e concentra algumas das paisagens mais marcantes do Planalto Central.",
        "tips": [
            ("Melhor época: maio a setembro", "O inverno do Cerrado oferece céu limpo e temperatura amena. Evite dezembro a março, quando chuvas tornam trilhas escorregadias e alguns atrativos ficam fechados."),
            ("Use protetor solar e chapéu", "O Cerrado tem incidência solar muito alta, especialmente em trilhas abertas. Leve protetor FPS 50+, óculos de sol e chapéu — obrigatórios."),
            ("Leve água suficiente", "Em algumas trilhas da Chapada, pontos de água potável são escassos. Carregue pelo menos 2 L por pessoa para trilhas de meio dia."),
            ("Confirme atrativos abertos", "O Parque Nacional da Chapada dos Veadeiros tem visitação controlada em alguns setores. Confirme disponibilidade e preços de entrada antes de partir."),
            ("Explore além do parque nacional", "A região tem atrativos na APA do Pouso Alto e em propriedades privadas com trilhas e cachoeiras. Pesquise operadoras locais em Alto Paraíso."),
            ("Atenção com a fauna", "O Cerrado tem diversidade de aves, macacos e até onças. Não alimente animais e respeite o ambiente natural."),
        ],
        "faqs": [
            ("Quais são as melhores trilhas na Chapada dos Veadeiros?",
             "O Vale da Lua e as cachoeiras do Parque Nacional da Chapada dos Veadeiros são os atrativos mais procurados. A Cachoeira Santa Bárbara, o Cânion das Antas e as Cachoeiras Almécegas I e II também são destaques. Para trilhas mais longas, os setores São Bento e Carrossel oferecem percursos de 10 a 20 km."),
            ("Preciso de guia para trilhas em Goiás?",
             "O Vale da Lua e as cachoeiras do Parque Nacional não exigem guia obrigatório por regulamento. No entanto, para trilhas mais longas ou fora do parque, guia local é altamente recomendado — especialmente na alta temporada, quando os grupos são maiores."),
            ("Como chegar a Alto Paraíso de Goiás?",
             "Alto Paraíso fica a aproximadamente 250 km de Brasília pela GO-118. O acesso de carro é relativamente fácil. Há também opções de van e ônibus partindo de Brasília. Alguns grupos alugam carro na capital para ter mais flexibilidade."),
            ("Qual a taxa de entrada do Parque Nacional da Chapada dos Veadeiros?",
             "A taxa de entrada é cobrada por pessoa e varia conforme o setor e o período. Consulte os valores atualizados no site do ICMBio antes de visitar. Há descontos para estudantes e isenção para crianças pequenas."),
            ("Existe boa infraestrutura de hospedagem em Alto Paraíso?",
             "Sim. Alto Paraíso tem boa oferta de pousadas, campings e chalés para todos os perfis. A cidade tem mercado, farmácias e restaurantes. São Jorge, a 36 km, é mais rústica mas fica mais próxima de alguns atrativos do parque."),
        ],
        "hero_image": "/trails/Y8KJdb96pKOX.jpg",
    },
    "RS": {
        "subtitle": "O Sul do Brasil guarda os maiores cânions da América Latina, com paredões de centenas de metros e trilhas que desafiam qualquer montanhista.",
        "editorial": "O Rio Grande do Sul é o estado dos grandes cânions brasileiros. Cambará do Sul, nas Serras Gaúchas, é o ponto de partida para o Parque Nacional de Aparados da Serra e o Parque Nacional da Serra Geral — que juntos formam o complexo de cânions mais impressionante do Brasil. O Cânion Itaimbezinho, com paredões de até 720 metros, é o maior cânion da América Latina e um dos destinos de trekking mais icônicos do país.",
        "tips": [
            ("Trilha do Rio do Boi exige guia", "Para descer ao fundo do Cânion Itaimbezinho pela Trilha do Rio do Boi, o guia é obrigatório. Contrate com antecedência — vagas são limitadas."),
            ("Melhor época: março a novembro", "O inverno gaúcho (junho a agosto) é frio mas oferece dias claros e visibilidade perfeita nos mirantes. Evite os meses de verão intenso (dezembro a fevereiro) quando chuvas são frequentes."),
            ("Vista do Cotovelo e do Vértice", "As trilhas do Cotovelo e do Vértice no Itaimbezinho são percursos de borda de cânion que não exigem guia e oferecem vistas espetaculares. Ótimas para iniciantes."),
            ("Cânion Fortaleza no Parque Serra Geral", "A 30 km do Itaimbezinho, o Cânion Fortaleza tem paredões ainda maiores. Combine os dois em dias consecutivos para a experiência completa dos cânions gaúchos."),
            ("Roupas para o frio", "No inverno, temperaturas negativas são possíveis em Cambará do Sul. Leve casaco térmico, luvas e touca mesmo que a previsão seja de sol."),
            ("Acesso por estrada de terra", "Parte do acesso entre atrativos é por estrada de terra. Veículo com boa tração é recomendado, especialmente após chuvas."),
        ],
        "faqs": [
            ("O Cânion Itaimbezinho realmente exige guia obrigatório?",
             "Para a Trilha do Rio do Boi, que desce ao fundo do cânion, o guia é obrigatório por regulamento do ICMBio. As trilhas de borda (Cotovelo e Vértice) não exigem guia. A exigência visa a segurança dos visitantes, já que a trilha do fundo atravessa o rio diversas vezes."),
            ("Qual a diferença entre o Parque Nacional de Aparados da Serra e o Parque Nacional da Serra Geral?",
             "Os dois parques são contíguos e formam o maior complexo de cânions do Brasil. Aparados da Serra abriga o Itaimbezinho; a Serra Geral abriga o Cânion Fortaleza e o Cânion da Josafá. Cada parque tem entrada e cobrança separadas. Juntos, cobrem mais de 100 mil hectares de Mata Atlântica e Campos de Cima da Serra."),
            ("Como chegar a Cambará do Sul?",
             "Cambará do Sul fica a cerca de 180 km de Caxias do Sul e a 210 km de Porto Alegre. O acesso mais comum é pela RS-020 a partir de Canela e São Francisco de Paula. O trecho final tem trechos de serra sinuosos — recomendado veículo com boa tração."),
            ("Há trilhas para iniciantes nos cânions gaúchos?",
             "Sim. As trilhas de borda do Cânion Itaimbezinho (Cotovelo: 1,6 km; Vértice: 2,4 km) são adequadas para iniciantes e oferecem vistas impressionantes sem exigir guia ou grande preparo físico. No Cânion Fortaleza, há mirantes de fácil acesso também."),
            ("Qual a melhor época para ver os cânions com névoa?",
             "A névoa que envolve os paredões é mais frequente no inverno (junho a agosto), especialmente ao amanhecer. Para vistas claras do fundo do cânion, os dias secos do outono e da primavera costumam ser os melhores."),
        ],
        "hero_image": "/trails/rXFyiCGZLcfZ.jpg",
    },
    "SC": {
        "subtitle": "O litoral sul catarinense combina praias paradisíacas, trilhas costeiras e o espetáculo natural das baleias-franca entre julho e novembro.",
        "editorial": "Santa Catarina é um estado de grande diversidade natural: do litoral de praias premiadas ao interior serrano com cachoeiras e montanhas. A Praia do Rosa, em Imbituba, é considerada uma das mais bonitas do Brasil e um dos melhores pontos de avistamento de baleias-franca do mundo. A trilha costeira que conecta a Rosa Norte à Rosa Sul é acessível para todos os perfis e recompensa com vistas de tirar o fôlego.",
        "tips": [
            ("Julho a novembro para baleias", "Entre julho e novembro, baleias-franca vêm à região reproduzir e dar à luz. É possível avistá-las da própria trilha costeira. Um dos poucos lugares no mundo onde isso acontece tão perto da costa."),
            ("Trilha é gratuita e acessível", "A trilha das praias Rosa Norte a Sul é gratuita, não exige guia e é acessível para caminhantes com pouca experiência. A dificuldade é baixa e o percurso pode ser feito em 2 a 3 horas."),
            ("Leve protetor solar e água", "O trecho costeiro tem pouca sombra. Leve protetor solar, chapéu e água suficiente — especialmente no verão (dezembro a fevereiro)."),
            ("Combine com surf e lagoa", "A Praia do Rosa é famosa pelo surf e pela Lagoa de Ibiraquera, ideal para stand-up paddle. Combine a trilha com uma tarde na lagoa para aproveitar ao máximo."),
            ("Hospedagem em Garopaba ou Imbituba", "A região tem boa infraestrutura de pousadas e campings. Garopaba e Imbituba têm opções para todos os perfis, incluindo mais alternativas de restaurante e serviços."),
            ("Acesse pela SC-434", "O acesso à Praia do Rosa é pela SC-434, a partir da BR-101. A estrada de terra na entrada tem trechos irregulares. Veículo com boa distância ao solo recomendado no inverno."),
        ],
        "faqs": [
            ("Qual a melhor época para visitar a Praia do Rosa?",
             "De julho a novembro para quem quer ver baleias-franca. O verão (dezembro a fevereiro) é a alta temporada com praias cheias e preços altos. O outono e a primavera oferecem boa relação entre clima, movimento e preço."),
            ("É possível ver baleias da trilha?",
             "Sim — é um dos pontos mais famosos do Brasil para isso. Baleias-franca chegam à região entre julho e novembro para reprodução. Os mirantes costeiros da trilha são pontos privilegiados de observação. O Projeto Baleia Franca, sediado em Imbituba, acompanha as baleias e pode indicar os melhores pontos de avistamento."),
            ("A trilha é adequada para famílias com crianças?",
             "Sim. A Trilha das Praias Rosa Norte a Sul tem dificuldade baixa, sem trechos técnicos. É adequada para crianças com boa disposição para caminhada. O terreno costeiro é relativamente estável, com alguns trechos de pedras e morro suave."),
            ("Há taxa de entrada na APA da Baleia Franca?",
             "A APA da Baleia Franca não cobra taxa de entrada para visitação regular. Algumas atividades específicas (como passeios de barco) podem ter custo. Confirme a regulamentação atual antes de visitar."),
            ("Quais outras trilhas e atrativos existem em Santa Catarina?",
             "Santa Catarina tem muito além do litoral: a Serra Catarinense (Urubici, São Joaquim) tem trilhas em altitude com neve esporádica no inverno. O Parque Estadual da Serra do Tabuleiro é a maior unidade de conservação do estado. As Cachoeiras do Rio do Rastro e a Serra do Rio do Rastro também são destinos de destaque."),
        ],
        "hero_image": "/trails/In5sfrVjooct.jpg",
    },
    "CE": {
        "subtitle": "O litoral cearense combina dunas brancas, lagoas interdunares e ventos constantes que tornam cada trilha uma experiência única no Nordeste.",
        "editorial": "O Ceará é um estado de paisagens nordestinas singulares: dunas costeiras que parecem desertos, lagoas de águas claras, ventanias refrescantes e um litoral de mais de 570 km. A APA das Dunas de Paracuru, com seus Lençóis Paracuruenses, oferece um trekking de cerca de 10 km por um ambiente dunar costeiro único. A exposição solar é intensa e o terreno arenoso exige preparo — mas a recompensa visual é extraordinária.",
        "tips": [
            ("Agosto a dezembro é a melhor época", "O período seco do Ceará (agosto a dezembro) é ideal para trilhas em dunas. As lagoas costumam estar cheias e o tempo tende a ser ensolarado com ventos refrescantes."),
            ("Prepare-se para o calor", "O sol nordestino é muito intenso. Leve protetor solar FPS 70+, chapéu de aba larga, óculos de sol e comece cedo (antes das 8h) para evitar o pior do calor."),
            ("A areia cansa mais que parece", "Caminhar em areia fofa aumenta muito o esforço físico. Mesmo trilhas de baixa altimetria demandam esforço considerável. Avalie seu condicionamento antes de partir."),
            ("Leve água e eletrólitos", "Em dunas, a transpiração é intensa. Leve pelo menos 2 L de água por pessoa e considere sachês de eletrólitos para trilhas acima de 3 horas."),
            ("Guia local é recomendado", "Nas dunas, a orientação é mais difícil pois as referências visuais mudam com o vento. Um guia local conhece os melhores pontos de parada, lagoas e atalhos."),
            ("Combine com o litoral cearense", "Paracuru fica a 85 km de Fortaleza. Combine a trilha com praias como Lagoinha, Mundaú e Flecheiras para um roteiro de litoral completo."),
        ],
        "faqs": [
            ("O que são os Lençóis Paracuruenses?",
             "Os Lençóis Paracuruenses são um campo de dunas costeiras na APA das Dunas de Paracuru, em Paracuru (CE). O nome vem da semelhança visual com os famosos Lençóis Maranhenses — campos de dunas brancas entremeados de lagoas interdunares. O percurso de cerca de 10 km conecta a Praia do Farol por trilha linear em ambiente dunar."),
            ("Qual a diferença entre os Lençóis Paracuruenses e os Lençóis Maranhenses?",
             "Os Lençóis Maranhenses (MA) são muito maiores e mais famosos, com cerca de 155 mil hectares. Os Paracuruenses (CE) são menores e menos turísticos, o que os torna mais tranquilos e autênticos. Ambos têm dunas e lagoas, mas a escala e a logística são muito diferentes."),
            ("Preciso de guia para a trilha dos Lençóis de Paracuru?",
             "Não há exigência oficial de guia, mas é altamente recomendado — especialmente para quem não conhece o terreno. Nas dunas, a orientação é difícil e as marcações podem desaparecer. Guias locais de Paracuru conhecem as lagoas e os melhores percursos."),
            ("Como chegar a Paracuru?",
             "Paracuru fica a 85 km de Fortaleza pela CE-085 (Estruturante). O acesso de carro dura cerca de 1h30. Há também vans e ônibus partindo da rodoviária de Fortaleza. Na cidade, carros de aplicativo ou mototáxi levam até o início da trilha."),
            ("As lagoas dos Lençóis Paracuruenses são potáveis?",
             "As lagoas interdunares não devem ser consumidas sem tratamento adequado. A água pode conter bactérias e contaminantes. Leve água potável suficiente para toda a trilha e não dependa das lagoas como fonte de hidratação."),
        ],
        "hero_image": "/trails/Ez5gj0ikDplH.jpg",
    },
}

DIFF_CONTENT = {
    "moderate": {
        "title": "Trilhas Moderadas no Brasil",
        "slug": "moderado",
        "subtitle": "Percursos que exigem condicionamento básico e alguma experiência — ideais para quem quer evoluir além das trilhas fáceis.",
        "editorial": "Trilhas moderadas representam o equilíbrio entre acessibilidade e desafio. Exigem condicionamento físico acima da média, mas não requerem técnicas de montanhismo. São ideais para trilheiros que já têm algumas saídas na bagagem e querem ampliar o repertório com percursos mais longos, com mais desnível ou em ambientes mais exigentes.",
        "what_means": [
            ("Distância e desnível maiores", "Trilhas moderadas costumam ter entre 8 e 20 km e desnível entre 300 e 800 m. Exigem resistência aeróbica para manter o ritmo ao longo de várias horas."),
            ("Terreno variado", "Espere trechos de subida prolongada, solo irregular, pedras molhadas e passagens mais estreitas. Calçado de trekking com bom solado é essencial."),
            ("Autonomia básica", "Em trilhas moderadas, você precisa saber se orientar, carregar água e lanche suficientes e ter noção de clima e meteorologia da região."),
            ("Preparo recomendado", "2 a 3 meses de caminhadas regulares (30–60 min, 3x/semana) e algumas trilhas fáceis anteriores preparam bem o corpo para trilhas moderadas."),
        ],
        "faqs": [
            ("O que define uma trilha como 'moderada'?",
             "A classificação moderada considera distância (geralmente 8–20 km), desnível acumulado (300–800 m), duração (4–8 horas), tipo de terreno e nível de exposição. Trilhas moderadas são acessíveis para quem tem condicionamento regular, mas exigem preparo acima do básico."),
            ("Preciso de treino especial para trilhas moderadas?",
             "Não é preciso ser atleta, mas o preparo faz diferença. Recomenda-se: caminhadas de 5–10 km regulares, subidas de escadas e exercícios de resistência. Para trilhas em altitude (acima de 1.500 m), treino cardiovascular é especialmente importante."),
            ("Qual equipamento devo levar em trilhas moderadas?",
             "Calçado de trekking com bom grip, meia acolchoada, bastões (optativo, mas ajudam em descidas), mochila de 20–30 L, água (mínimo 1,5 L por pessoa), lanche energético, kit básico de primeiros socorros, mapa offline e agasalho."),
            ("Posso fazer trilhas moderadas sozinho?",
             "É possível, mas recomenda-se ir em dupla ou grupo. Avise alguém sobre a trilha que vai fazer e o horário previsto de retorno. Para trilhas moderadas em regiões remotas ou com altitude, guia local aumenta a segurança."),
            ("As trilhas moderadas são adequadas para adolescentes?",
             "Sim, para adolescentes a partir de 12–14 anos com boa disposição física. A chave é adequar o ritmo ao grupo mais lento e fazer paradas frequentes. Evite trilhas acima de 2.000 m de altitude com menores sem experiência prévia."),
        ],
    },
    "hard": {
        "title": "Trilhas Difíceis no Brasil",
        "slug": "dificil",
        "subtitle": "Para atletas e trilheiros experientes: percursos exigentes com desnível acentuado, distâncias longas e ambientes desafiadores.",
        "editorial": "Trilhas difíceis são o território dos montanhistas e trilheiros dedicados. Distâncias acima de 15 km, desníveis superiores a 1.000 m, trechos técnicos e condições climáticas adversas são comuns. No Brasil, trilhas difíceis como a Travessia Petrópolis×Teresópolis e a subida ao Pico da Bandeira estão entre os percursos mais icônicos do país — e os mais exigentes.",
        "what_means": [
            ("Alto desnível e longa distância", "Trilhas difíceis têm geralmente acima de 1.000 m de desnível acumulado e/ou distâncias de 15 km ou mais. Algumas são percursos de múltiplos dias."),
            ("Trechos técnicos", "Passagens em rocha, descidas íngremes com auxílio de cordas fixas ou escalada simples podem estar presentes. Experiência em terreno irregular é essencial."),
            ("Exposição a elementos", "Altitude, vento, chuva e neblina são fatores frequentes. A capacidade de tomar decisões em condições adversas é tão importante quanto o condicionamento físico."),
            ("Logística complexa", "Trilhas de múltiplos dias exigem planejamento de alimentos, água, camping e retorno. Errar nessa etapa pode comprometer toda a expedição."),
        ],
        "faqs": [
            ("Como sei se estou preparado para uma trilha difícil?",
             "Indicadores positivos: você faz trilhas moderadas regularmente sem dificuldade, tem experiência com percursos de 10+ km, sabe navegar com mapa e GPS, já fez pelo menos uma trilha de 2 dias. Se ainda está iniciando, construa a experiência gradualmente com trilhas moderadas."),
            ("É obrigatório ter guia em trilhas difíceis?",
             "Depende da trilha. Algumas, como a Travessia Petrópolis×Teresópolis, não têm guia obrigatório por regulamento, mas o recomendam para grupos sem experiência em longo curso. O Pico da Bandeira não exige guia, mas sua altitude (2.892 m) pede preparo e cuidado."),
            ("Qual equipamento é essencial para trilhas difíceis?",
             "Além do básico: calçado de trekking alto com boa estabilidade de tornozelo, bastões, mochila de 40–60 L para pernoites, saco de dormir adequado à temperatura prevista, barraca para travessias, kit de emergência completo, mapa e GPS offline."),
            ("O que fazer se as condições piorarem durante a trilha?",
             "Tenha sempre um plano de saída antecipada. Se o clima piorar drasticamente (tempestade, neblina densa), não hesite em retornar. Nenhuma vista ou objetivo vale riscos desnecessários. Compartilhe sua rota com alguém de fora antes de partir."),
            ("Devo contratar seguro de resgate para trilhas difíceis?",
             "Fortemente recomendado. Resgates em montanha podem custar milhares de reais sem seguro. Algumas apólices de saúde cobrem acidentes em atividades físicas — verifique a sua. Existem também seguros específicos para atividades outdoor com cobertura de helicóptero."),
        ],
    },
    "expert": {
        "title": "Trilhas de Especialista no Brasil",
        "slug": "especialista",
        "subtitle": "Expedições para montanhistas com experiência sólida: terreno técnico, altitude extrema e exigência física máxima.",
        "editorial": "Trilhas classificadas como 'especialista' ou 'extrema' são o topo da hierarquia do trekking brasileiro. Monte Roraima e Travessia Serra Fina estão nessa categoria — percursos que exigem planejamento de expedição, técnicas específicas de montanhismo e condicionamento físico de atleta. Não são recomendadas para iniciantes ou para quem nunca fez travessias de múltiplos dias.",
        "what_means": [
            ("Técnica de montanhismo", "Trechos de escalada, rapel ou uso de cordas fixas podem ser parte do percurso. Conhecimento básico de técnicas de montanha é necessário."),
            ("Altitude e aclimatação", "Percursos acima de 2.500 m exigem aclimatação prévia. Mal de montanha (altitude sickness) é um risco real que deve ser gerenciado com cautela."),
            ("Múltiplos dias de expedição", "Trilhas de especialista costumam durar 4 a 8 dias com pernoites em camping selvagem. Logística de alimentos, água e equipamento é parte fundamental do planejamento."),
            ("Guia especializado", "Para a maioria das trilhas de nível especialista no Brasil, guia credenciado e com experiência específica na rota é obrigatório ou fortemente recomendado."),
        ],
        "faqs": [
            ("Quais são as trilhas mais difíceis do Brasil?",
             "A Travessia Serra Fina (MG) é considerada a trilha mais difícil do Brasil — 45 km com 5 picos acima de 2.700 m. O Monte Roraima (RR) é a expedição mais remota e logisticamente complexa. Outros percursos de especialista incluem o Pico das Agulhas Negras (RJ/MG) e o Circuito da Canastra (MG)."),
            ("Quanto tempo preciso para me preparar para uma trilha de especialista?",
             "Para alguém já ativo fisicamente, pelo menos 6 a 12 meses de preparação específica são recomendados. Isso inclui trilhas moderadas e difíceis regulares, treinos de resistência, caminhadas com mochila pesada e, se possível, algumas noites de camping em montanha."),
            ("Guia é sempre obrigatório em trilhas de especialista?",
             "Depende. O Monte Roraima exige guia indígena credenciado por lei. A Travessia Serra Fina não tem regulamentação específica, mas é considerado imprudente sem guia especializado dado o terreno técnico e remoto. Verifique sempre a regulamentação vigente da trilha e da unidade de conservação."),
            ("Qual seguro devo contratar para expedições extremas?",
             "Procure apólices com cobertura de resgate em helicóptero, evacuação médica e acidentes em atividades de alto risco. Seguros internacionais (como Iati ou Chapka) costumam ter coberturas mais abrangentes. Confirme que a trilha específica está coberta antes de contratar."),
            ("Como escolher um guia confiável para trilhas de especialista?",
             "Verifique o registro no CADASTUR (Ministério do Turismo), experiência específica na trilha desejada, referências de clientes anteriores e certificações de primeiros socorros. Trilhas de especialista exigem guias com experiência sólida — não opte pelo mais barato sem verificar credenciais."),
        ],
    },
}

# ── Shared HTML fragments ──────────────────────────────────────────────────
ANALYTICS_BLOCK = (
    "<script>window.TREKKO_CONFIG={GA4_ID:'G-S816P190VN',GTM_ID:null,ADS_ID:'AW-355784943'};</script>\n"
    "<script>(function(){var id=(window.TREKKO_CONFIG||{}).GTM_ID;if(!id)return;"
    "window.dataLayer=window.dataLayer||[];"
    "window.dataLayer.push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
    "var f=document.getElementsByTagName('script')[0],j=document.createElement('script');"
    "j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+id;"
    "f.parentNode.insertBefore(j,f);})();</script>\n"
    "<script async src=\"https://www.googletagmanager.com/gtag/js?id=G-S816P190VN\"></script>\n"
    "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
    "gtag('js',new Date());gtag('config','G-S816P190VN',"
    "{send_page_view:!(window.TREKKO_CONFIG&&window.TREKKO_CONFIG.GTM_ID)});</script>\n"
    "<script src=\"/assets/trekko-analytics.js\"></script>"
)

FONTS_BLOCK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
    '&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet">'
)

FAVICONS_BLOCK = (
    '<link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48">\n'
    '<link rel="icon" href="/android-chrome-192x192.png" type="image/png" sizes="192x192">\n'
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">\n'
    '<link rel="manifest" href="/site.webmanifest">'
)

TESTIMONIALS = [
    {
        "name": "Fernanda O.",
        "initial": "F",
        "trail": "Travessia Petrópolis-Teresópolis",
        "quote": "A ficha do Trekko foi minha referência para preparar a travessia. Distância, desnível, estimativa de horas — cada dado estava correto. Voltei com as botas gastas e o coração cheio.",
        "stars": 5,
    },
    {
        "name": "Carlos M.",
        "initial": "C",
        "trail": "Monte Roraima, Roraima",
        "quote": "Precisava confirmar se o guia era obrigatório no Roraima. O Trekko tinha a resposta com todo o contexto. Encontrei o guia pelo site e a expedição de 7 dias foi a melhor da minha vida.",
        "stars": 5,
    },
    {
        "name": "Ana Paula R.",
        "initial": "A",
        "trail": "Chapada dos Veadeiros, GO",
        "quote": "Como iniciante, os filtros do Trekko me ajudaram a escolher uma trilha no meu nível. Fiz minha primeira trilha com cachoeira em Goiás e já estou planejando a próxima.",
        "stars": 5,
    },
]

CSS = """<style>
:root{--primary:#15803d;--primary-dark:#166534;--primary-hover:#16a34a;--primary-light:#dcfce7;--primary-bg:#f0fdf4;--accent:#f59e0b;--accent-light:#fef3c7;--text-primary:#1e293b;--text-secondary:#475569;--text-muted:#94a3b8;--border:#e2e8f0;--white:#fff;--bg-light:#f8fafc;--diff-easy:#15803d;--diff-moderate:#d97706;--diff-hard:#ea580c;--diff-expert:#dc2626;--shadow-sm:0 1px 3px rgba(0,0,0,.08);--shadow-md:0 4px 12px rgba(0,0,0,.1);--shadow-lg:0 8px 24px rgba(0,0,0,.12);--radius:8px;--radius-lg:16px;--font-body:'Inter',sans-serif;--font-heading:'Sora',sans-serif;--max-w:1200px;--gutter:1.25rem}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}body{font-family:var(--font-body);color:var(--text-primary);line-height:1.6;background:var(--white)}
img{max-width:100%;height:auto;display:block}a{color:inherit;text-decoration:none}ul{list-style:none}
.container{max-width:var(--max-w);margin:0 auto;padding:0 var(--gutter)}
.section{padding:4rem 0}.section--alt{background:var(--bg-light)}.section--green{background:var(--primary-bg)}
h1,h2,h3,h4{font-family:var(--font-heading);line-height:1.25;color:var(--text-primary)}
h1{font-size:clamp(1.75rem,5vw,2.75rem);font-weight:700}h2{font-size:clamp(1.35rem,3.5vw,2rem);font-weight:700;margin-bottom:1rem}h3{font-size:1.1rem;font-weight:600}
p{color:var(--text-secondary);line-height:1.7}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;padding:.75rem 1.5rem;border-radius:var(--radius);font-family:var(--font-body);font-weight:600;font-size:1rem;cursor:pointer;border:2px solid transparent;transition:all .2s;text-decoration:none;line-height:1}
.btn--primary{background:var(--primary);color:var(--white);border-color:var(--primary)}.btn--primary:hover{background:var(--primary-hover);border-color:var(--primary-hover)}
.btn--outline{background:transparent;color:var(--primary);border-color:var(--primary)}.btn--outline:hover{background:var(--primary-light)}
.btn--outline-white{background:transparent;color:var(--white);border-color:rgba(255,255,255,.7)}.btn--outline-white:hover{background:rgba(255,255,255,.1)}
.btn--white{background:var(--white);color:var(--primary);border-color:var(--white)}.btn--white:hover{background:var(--primary-light)}
.btn--lg{padding:1rem 2rem;font-size:1.1rem}.btn--sm{padding:.5rem 1rem;font-size:.875rem}
.btn:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.site-header{position:sticky;top:0;z-index:100;background:var(--white);border-bottom:1px solid var(--border);transition:box-shadow .2s}
.site-header.scrolled{box-shadow:var(--shadow-md)}
.header-inner{display:flex;align-items:center;justify-content:space-between;height:64px;gap:1rem}
.logo{font-family:var(--font-heading);font-weight:700;font-size:1.4rem;color:var(--primary);display:flex;align-items:center;gap:.4rem}
.logo-icon{width:28px;height:28px;flex-shrink:0}
.header-nav{display:none;gap:1.5rem}.header-nav a{color:var(--text-secondary);font-size:.95rem;font-weight:500;transition:color .2s}.header-nav a:hover{color:var(--primary)}
@media(min-width:768px){.header-nav{display:flex}}
.breadcrumb{background:var(--bg-light);border-bottom:1px solid var(--border);padding:.625rem 0}
.breadcrumb ol{display:flex;flex-wrap:wrap;gap:.25rem;align-items:center;font-size:.85rem}
.breadcrumb li{display:flex;align-items:center;gap:.25rem;color:var(--text-muted)}
.breadcrumb li a{color:var(--text-secondary);transition:color .15s}.breadcrumb li a:hover{color:var(--primary)}
.breadcrumb li:last-child{color:var(--text-primary);font-weight:500}
.hero{background:linear-gradient(135deg,rgba(21,128,61,.9) 0%,rgba(20,83,45,.95) 100%),var(--hero-bg,url('/trails/bCKTbP7YuBYO.jpg')) center/cover no-repeat;padding:5rem 0 4rem;color:var(--white)}
.hero-inner{max-width:760px}
.hero-badge{display:inline-flex;align-items:center;gap:.4rem;background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);border-radius:100px;padding:.35rem 1rem;font-size:.85rem;font-weight:500;margin-bottom:1.5rem;backdrop-filter:blur(4px)}
.hero h1{color:var(--white);margin-bottom:1rem}
.hero-subtitle{font-size:1.1rem;color:rgba(255,255,255,.9);max-width:620px;margin-bottom:2rem;line-height:1.7}
.hero-ctas{display:flex;flex-wrap:wrap;gap:.75rem;margin-bottom:1.5rem}
.hero-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:3rem;max-width:520px}
.stat{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:var(--radius);padding:.875rem 1rem;text-align:center;backdrop-filter:blur(4px)}
.stat strong{display:block;font-family:var(--font-heading);font-size:1rem;font-weight:700;color:var(--white)}
.stat span{font-size:.78rem;color:rgba(255,255,255,.8)}
.editorial{max-width:800px}.editorial p+p{margin-top:1rem}
.filters-wrap{background:var(--white);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1.5rem;margin-bottom:2rem;box-shadow:var(--shadow-sm)}
.filters-title{font-size:.9rem;font-weight:600;color:var(--text-primary);margin-bottom:1rem}
.filters-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem}
@media(min-width:600px){.filters-grid{grid-template-columns:repeat(3,1fr)}}
@media(min-width:900px){.filters-grid{grid-template-columns:repeat(4,1fr)}}
.filter-select{width:100%;padding:.6rem .875rem;border:1.5px solid var(--border);border-radius:var(--radius);font-family:var(--font-body);font-size:.875rem;color:var(--text-primary);background:var(--white);appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M2 4l4 4 4-4' stroke='%2394a3b8' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right .75rem center;cursor:pointer;transition:border-color .2s}
.filter-select:focus{outline:none;border-color:var(--primary)}
.filter-reset{padding:.6rem 1rem;font-size:.875rem;color:var(--text-secondary);background:var(--bg-light);border:1.5px solid var(--border);border-radius:var(--radius);cursor:pointer;font-family:var(--font-body);transition:all .2s}
.filter-reset:hover{background:var(--primary-light);border-color:var(--primary);color:var(--primary)}
.filter-count{font-size:.85rem;color:var(--text-muted);margin-top:.75rem}
.trails-grid{display:grid;grid-template-columns:1fr;gap:1.5rem}
@media(min-width:600px){.trails-grid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:1000px){.trails-grid{grid-template-columns:repeat(3,1fr)}}
.trail-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius-lg);overflow:hidden;transition:box-shadow .2s,transform .2s;display:flex;flex-direction:column}
.trail-card:hover{box-shadow:var(--shadow-lg);transform:translateY(-3px)}
.trail-img{position:relative;aspect-ratio:16/9;overflow:hidden;background:var(--primary-bg)}
.trail-img img{width:100%;height:100%;object-fit:cover;transition:transform .3s}
.trail-card:hover .trail-img img{transform:scale(1.05)}
.diff-badge{position:absolute;top:.75rem;left:.75rem;padding:.25rem .75rem;border-radius:100px;font-size:.75rem;font-weight:600;color:var(--white);text-transform:uppercase;letter-spacing:.03em}
.diff-easy{background:var(--diff-easy)}.diff-moderate{background:var(--diff-moderate)}.diff-hard{background:var(--diff-hard)}.diff-expert{background:var(--diff-expert)}
.trail-body{padding:1.25rem;flex:1;display:flex;flex-direction:column;gap:.75rem}
.trail-name{font-family:var(--font-heading);font-size:1.05rem;font-weight:700;color:var(--text-primary);line-height:1.3}
.trail-location{display:flex;align-items:center;gap:.35rem;font-size:.82rem;color:var(--text-muted)}
.trail-desc{font-size:.875rem;color:var(--text-secondary);line-height:1.6;flex:1}
.trail-meta{display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem}
.meta-item{background:var(--bg-light);border-radius:var(--radius);padding:.5rem;text-align:center}
.meta-label{display:block;font-size:.7rem;color:var(--text-muted);margin-bottom:.15rem;text-transform:uppercase;letter-spacing:.04em}
.meta-value{display:block;font-size:.85rem;font-weight:600;color:var(--text-primary)}
.trail-footer{border-top:1px solid var(--border);padding-top:.875rem;margin-top:auto}
.no-results{text-align:center;padding:3rem 1rem;color:var(--text-muted)}
.how-grid{display:grid;grid-template-columns:1fr;gap:1rem;margin-top:1.5rem}
@media(min-width:600px){.how-grid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:900px){.how-grid{grid-template-columns:repeat(3,1fr)}}
.how-item{display:flex;align-items:flex-start;gap:1rem;background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem}
.how-num{flex-shrink:0;width:36px;height:36px;background:var(--primary);color:var(--white);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--font-heading);font-size:.9rem;font-weight:700}
.how-text h4{font-size:.95rem;font-weight:600;margin-bottom:.25rem;color:var(--text-primary)}.how-text p{font-size:.875rem;margin:0}
.guides-grid{display:grid;grid-template-columns:1fr;gap:1.25rem;margin-top:1.5rem}
@media(min-width:600px){.guides-grid{grid-template-columns:repeat(2,1fr)}}
@media(min-width:900px){.guides-grid{grid-template-columns:repeat(3,1fr)}}
.guide-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1.5rem;transition:box-shadow .2s;display:flex;flex-direction:column;gap:.75rem}
.guide-card:hover{box-shadow:var(--shadow-md)}
.guide-avatar{width:48px;height:48px;background:var(--primary-bg);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--font-heading);font-weight:700;font-size:1.1rem;color:var(--primary);flex-shrink:0}
.guide-header{display:flex;align-items:center;gap:.875rem}
.guide-info{flex:1;min-width:0}
.guide-name{font-size:.95rem;font-weight:700;color:var(--text-primary);line-height:1.3}
.guide-city{font-size:.82rem;color:var(--text-muted)}
.guide-status{display:inline-flex;align-items:center;gap:.3rem;font-size:.75rem;font-weight:500;padding:.2rem .6rem;border-radius:100px;background:var(--accent-light);color:#92400e}
.guide-cats{display:flex;flex-wrap:wrap;gap:.35rem}
.guide-cat{font-size:.75rem;padding:.2rem .6rem;background:var(--bg-light);border-radius:100px;color:var(--text-secondary)}
.guide-cadastur{font-size:.78rem;color:var(--text-muted)}
.guide-actions{display:flex;gap:.5rem;margin-top:.25rem}
.trust-box{background:var(--accent-light);border-left:4px solid var(--accent);border-radius:0 var(--radius) var(--radius) 0;padding:1.5rem 2rem}
.trust-box h3{color:var(--text-primary);margin-bottom:.75rem}.trust-box p{font-size:.9rem}.trust-box p+p{margin-top:.5rem}
.faq-list{margin-top:1.5rem;max-width:820px}
.faq-item{border:1px solid var(--border);border-radius:var(--radius);margin-bottom:.625rem;overflow:hidden}
.faq-q{width:100%;background:var(--white);border:none;padding:1.1rem 1.25rem;text-align:left;font-family:var(--font-body);font-size:.95rem;font-weight:600;color:var(--text-primary);cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:1rem;transition:background .15s}
.faq-q:hover{background:var(--bg-light)}
.faq-arrow{flex-shrink:0;transition:transform .25s;color:var(--primary)}
.faq-item.open .faq-arrow{transform:rotate(180deg)}
.faq-a{max-height:0;overflow:hidden;transition:max-height .35s ease}
.faq-item.open .faq-a{max-height:500px}
.faq-a-inner{padding:.25rem 1.25rem 1.1rem;font-size:.9rem;color:var(--text-secondary);line-height:1.7}
.cta-final{background:linear-gradient(135deg,var(--primary) 0%,var(--primary-dark) 100%);padding:4.5rem 0;text-align:center;color:var(--white)}
.cta-final h2{color:var(--white);margin-bottom:.875rem}
.cta-final p{color:rgba(255,255,255,.85);max-width:560px;margin:0 auto 2rem}
.cta-btns{display:flex;flex-wrap:wrap;gap:.75rem;justify-content:center}
.related-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;margin-top:1rem}
@media(min-width:600px){.related-grid{grid-template-columns:repeat(3,1fr)}}
.related-link{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:.75rem 1rem;display:flex;align-items:center;gap:.5rem;font-size:.875rem;font-weight:500;color:var(--text-primary);transition:all .2s}
.related-link:hover{background:var(--primary-bg);border-color:var(--primary);color:var(--primary)}
.site-footer{background:#0f172a;color:#94a3b8;padding:3rem 0}
.footer-inner{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:2rem;margin-bottom:2rem}
@media(max-width:900px){.footer-inner{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.footer-inner{grid-template-columns:1fr}}
.footer-logo{font-family:var(--font-heading);font-size:1.3rem;font-weight:700;color:var(--white);margin-bottom:.5rem}
.footer-tagline{font-size:.875rem;line-height:1.6;margin-bottom:.75rem;color:#94a3b8}
.footer-email a{color:#64748b;font-size:.875rem}.footer-email a:hover{color:var(--white)}
.footer-col h4{color:var(--white);font-size:.875rem;font-weight:600;margin-bottom:.875rem}
.footer-col ul li{margin-bottom:.5rem}
.footer-col ul li a{color:#64748b;font-size:.875rem;transition:color .15s}.footer-col ul li a:hover{color:var(--white)}
.footer-bottom{border-top:1px solid #1e293b;padding-top:1.5rem;text-align:center;font-size:.8rem}
.header-cta-btn{display:none!important}
@media(min-width:768px){.header-cta-btn{display:inline-flex!important}}
.menu-toggle{display:flex;align-items:center;justify-content:center;background:none;border:none;cursor:pointer;padding:.4rem;color:var(--text-primary);min-width:44px;min-height:44px;-webkit-tap-highlight-color:transparent;border-radius:6px}
.menu-toggle:hover{background:var(--bg-light)}
@media(min-width:768px){.menu-toggle{display:none}}
.mm{position:fixed;inset:0;background:var(--white);z-index:9999;display:none;flex-direction:column;padding:1.25rem;overflow-y:auto}
.mm.open{display:flex}
.mm-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:2rem}
.mm-close{background:none;border:none;cursor:pointer;padding:.4rem;border-radius:6px;color:var(--text-primary);min-width:44px;min-height:44px;display:flex;align-items:center;justify-content:center}
.mm-nav{display:flex;flex-direction:column;gap:.25rem;flex:1}
.mm-nav a{display:flex;align-items:center;min-height:48px;padding:.75rem 1rem;border-radius:8px;font-size:1rem;font-weight:500;color:var(--text-primary);transition:background .15s}
.mm-nav a:hover{background:var(--primary-bg);color:var(--primary)}
.mm-foot{padding-top:1.5rem;border-top:1px solid var(--border);margin-top:auto;display:flex;flex-direction:column;gap:.75rem}
.sticky-bar{position:fixed;bottom:0;left:0;right:0;z-index:200;background:var(--white);border-top:2px solid var(--border);padding:.75rem 1rem;padding-bottom:calc(.75rem + env(safe-area-inset-bottom,0px));display:flex;gap:.5rem;box-shadow:0 -4px 20px rgba(0,0,0,.12)}
.sticky-bar.hidden{opacity:0;visibility:hidden;pointer-events:none}
@media(min-width:768px){.sticky-bar{display:none!important}}
.sticky-bar .btn{flex:1;min-height:48px;font-size:.875rem;padding:.75rem .375rem;white-space:normal;text-align:center;line-height:1.3}
@media(max-width:767px){body{padding-bottom:calc(76px + env(safe-area-inset-bottom,0px))}}
.sp-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-bottom:2.5rem}
@media(max-width:600px){.sp-stats{grid-template-columns:1fr;gap:1rem}}
.sp-stat{text-align:center;padding:1.5rem 1rem;background:var(--primary-bg);border-radius:var(--radius-lg);border:1px solid var(--primary-light)}
.sp-stat-num{font-family:var(--font-heading);font-size:2rem;font-weight:700;color:var(--primary);line-height:1;display:block}
.sp-stat-label{font-size:.85rem;color:var(--text-secondary);margin-top:.375rem;display:block}
.testimonials-grid{display:grid;grid-template-columns:1fr;gap:1.25rem;margin-top:1.75rem}
@media(min-width:700px){.testimonials-grid{grid-template-columns:repeat(3,1fr)}}
.testimonial-card{background:var(--white);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1.5rem;display:flex;flex-direction:column;gap:.875rem;box-shadow:var(--shadow-sm)}
.t-stars{display:flex;gap:.15rem;line-height:1}
.t-star{color:#f59e0b;font-size:1rem}
.t-quote{font-size:.9rem;color:var(--text-secondary);line-height:1.7;flex:1;font-style:italic;margin:0}
.t-footer{display:flex;align-items:center;gap:.75rem;border-top:1px solid var(--border);padding-top:.875rem;margin-top:auto}
.t-avatar{width:40px;height:40px;border-radius:50%;background:var(--primary-bg);display:flex;align-items:center;justify-content:center;font-family:var(--font-heading);font-weight:700;font-size:.9rem;color:var(--primary);flex-shrink:0}
.t-name{font-size:.875rem;font-weight:600;color:var(--text-primary);line-height:1.2}
.t-trail{font-size:.78rem;color:var(--text-muted)}
.sp-trust{display:flex;flex-wrap:wrap;gap:.625rem;margin-top:2rem}
.sp-badge{display:inline-flex;align-items:center;gap:.375rem;padding:.45rem .875rem;background:var(--bg-light);border:1px solid var(--border);border-radius:100px;font-size:.8rem;font-weight:500;color:var(--text-secondary)}
</style>"""

LOGO_SVG = (
    '<svg class="logo-icon" viewBox="0 0 28 28" fill="none" aria-hidden="true">'
    '<circle cx="14" cy="14" r="14" fill="#dcfce7"/>'
    '<path d="M7 20L12 10l3 5 2-3 4 8H7z" fill="#15803d"/>'
    '<circle cx="18" cy="8" r="2" fill="#15803d"/>'
    '</svg>'
)

PIN_ICON = (
    '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">'
    '<path d="M6 1C4.067 1 2.5 2.567 2.5 4.5c0 2.786 3.5 6.5 3.5 6.5s3.5-3.714 3.5-6.5C9.5 2.567 7.933 1 6 1z" stroke="#94a3b8" stroke-width="1.2"/>'
    '<circle cx="6" cy="4.5" r="1.25" stroke="#94a3b8" stroke-width="1.2"/>'
    '</svg>'
)

FAQ_ARROW = (
    '<svg class="faq-arrow" width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">'
    '<path d="M4 7l5 5 5-5" stroke="#15803d" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    '</svg>'
)

FOOTER_HTML = """
<footer class="site-footer">
<div class="container">
  <div class="footer-inner">
    <div class="footer-brand">
      <p class="footer-logo">Trekko</p>
      <p class="footer-tagline">A plataforma para quem vive a trilha.<br>Descubra, planeje e conecte-se com guias.</p>
      <p class="footer-email"><a href="mailto:contato@trekko.com.br">contato@trekko.com.br</a></p>
    </div>
    <div class="footer-col">
      <h4>Trilhas por estado</h4>
      <ul>
        <li><a href="/trilhas/sao-paulo">São Paulo</a></li>
        <li><a href="/trilhas/rio-de-janeiro">Rio de Janeiro</a></li>
        <li><a href="/trilhas/minas-gerais">Minas Gerais</a></li>
        <li><a href="/trilhas/goias">Goiás</a></li>
        <li><a href="/trilhas/rio-grande-do-sul">Rio Grande do Sul</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Por dificuldade</h4>
      <ul>
        <li><a href="/trilhas/para-iniciantes">Para iniciantes</a></li>
        <li><a href="/trilhas/moderado">Moderado</a></li>
        <li><a href="/trilhas/dificil">Difícil</a></li>
        <li><a href="/trilhas/especialista">Especialista</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Trekko</h4>
      <ul>
        <li><a href="/sobre">Sobre o Trekko</a></li>
        <li><a href="/guias/ativar-perfil">Ativar perfil de guia</a></li>
        <li><a href="/seguranca-em-trilhas">Segurança em trilhas</a></li>
        <li><a href="/privacidade">Privacidade</a></li>
        <li><a href="/termos-de-uso">Termos de uso</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 Trekko. Todos os direitos reservados.</p>
  </div>
</div>
</footer>"""

PAGE_JS = """\
<script>
(function(){{
var h=document.getElementById('site-header');
if(h)window.addEventListener('scroll',function(){{h.classList.toggle('scrolled',window.scrollY>50);}},{{passive:true}});
}})();
(function(){{
document.querySelectorAll('.faq-q').forEach(function(btn){{
  btn.addEventListener('click',function(){{
    var item=this.closest('.faq-item');
    var isOpen=item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(function(i){{
      i.classList.remove('open');i.querySelector('.faq-q').setAttribute('aria-expanded','false');
    }});
    if(!isOpen){{item.classList.add('open');this.setAttribute('aria-expanded','true');}}
  }});
}});
}})();
(function(){{
var cards=Array.from(document.querySelectorAll('.trail-card'));
if(!cards.length)return;
var fD=document.getElementById('f-diff'),fDi=document.getElementById('f-dist'),fT=document.getElementById('f-type');
var cnt=document.getElementById('filter-count'),noRes=document.getElementById('no-results');
if(!fD)return;
function run(){{var diff=fD.value,dist=fDi.value,type=fT.value,vis=0;
cards.forEach(function(c){{var ok=true;
if(diff&&c.dataset.difficulty!==diff)ok=false;
if(dist){{var km=parseFloat(c.dataset.distance);if(dist==='short'&&km>=5)ok=false;if(dist==='medium'&&(km<5||km>=15))ok=false;if(dist==='long'&&km<15)ok=false;}}
if(type&&c.dataset.type!==type)ok=false;
c.style.display=ok?'':'none';if(ok)vis++;}});
if(noRes)noRes.style.display=vis===0?'block':'none';
if(cnt)cnt.textContent=vis===cards.length?'':('Exibindo '+vis+' de '+cards.length+' trilha'+(cards.length!==1?'s':''));
}}
if(fD)fD.addEventListener('change',run);
if(fDi)fDi.addEventListener('change',run);
if(fT)fT.addEventListener('change',run);
var rst=document.getElementById('filter-reset');
if(rst)rst.addEventListener('click',function(){{fD.value='';if(fDi)fDi.value='';if(fT)fT.value='';run();}});
run();
}})();
(function(){{
var toggle=document.getElementById('menu-toggle');
var menu=document.getElementById('mobile-menu');
var close=document.getElementById('mm-close');
if(!toggle||!menu)return;
function openMenu(){{menu.classList.add('open');document.body.style.overflow='hidden';toggle.setAttribute('aria-expanded','true');}}
function closeMenu(){{menu.classList.remove('open');document.body.style.overflow='';toggle.setAttribute('aria-expanded','false');}}
toggle.addEventListener('click',openMenu);
if(close)close.addEventListener('click',closeMenu);
document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&menu.classList.contains('open'))closeMenu();}});
}})();
(function(){{
var bar=document.getElementById('sticky-bar');
if(!bar)return;
document.querySelectorAll('input,select,textarea').forEach(function(inp){{
  inp.addEventListener('focus',function(){{bar.classList.add('hidden');}});
  inp.addEventListener('blur',function(){{setTimeout(function(){{bar.classList.remove('hidden');}},150);}});
}});
}})();
window.addEventListener('load',function(){{
  if(typeof gtag!=='undefined')gtag('event',{event_name!r},{event_params!r});
}});
</script>"""

STICKY_BAR = """\
<div class="sticky-bar" id="sticky-bar" role="complementary" aria-label="Ações rápidas">
  <a href="#trilhas" class="btn btn--primary">Explorar trilhas</a>
  <a href="/guias" class="btn btn--outline">Ver guias</a>
</div>"""

# ── Helpers ─────────────────────────────────────────────────────────────────
def slugify(text):
    text = unicodedata.normalize("NFD", str(text))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path.replace(BASE, '')}")

def build_head(title, desc, canonical, og_image, jsonld):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="robots" content="index,follow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://trekko.com.br{og_image}">
{FAVICONS_BLOCK}
{FONTS_BLOCK}
{ANALYTICS_BLOCK}
<script type="application/ld+json">{jsonld}</script>
{CSS}
</head>"""

def build_header(active_href=None):
    return f"""<header class="site-header" id="site-header" role="banner">
  <div class="container header-inner">
    <a href="/" class="logo" aria-label="Trekko — página inicial">{LOGO_SVG}Trekko</a>
    <nav class="header-nav" aria-label="Navegação principal">
      <a href="/trilhas">Trilhas</a>
      <a href="/guias">Guias</a>
      <a href="/contato">Contato</a>
    </nav>
    <a href="#trilhas" class="btn btn--primary header-cta-btn">Explorar trilhas</a>
    <button class="menu-toggle" id="menu-toggle" aria-label="Abrir menu" aria-expanded="false" aria-controls="mobile-menu">
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none" aria-hidden="true"><path d="M3 6h16M3 11h16M3 16h16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>
<div class="mm" id="mobile-menu" role="dialog" aria-label="Menu de navegação">
  <div class="mm-head">
    <a href="/" class="logo">{LOGO_SVG}Trekko</a>
    <button class="mm-close" id="mm-close" aria-label="Fechar menu">
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none" aria-hidden="true"><path d="M5 5l12 12M17 5L5 17" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
    </button>
  </div>
  <nav class="mm-nav">
    <a href="/trilhas">Trilhas</a>
    <a href="/guias">Guias</a>
    <a href="/contato">Contato</a>
    <a href="/sobre">Sobre o Trekko</a>
  </nav>
  <div class="mm-foot">
    <a href="#trilhas" class="btn btn--primary">Explorar trilhas</a>
    <a href="/guias/ativar-perfil" class="btn btn--outline">Sou guia — ativar perfil</a>
  </div>
</div>"""

def build_breadcrumb(items):
    lis = ""
    for i, (label, href) in enumerate(items):
        if i < len(items) - 1:
            lis += f'<li><a href="{href}">{label}</a> <span aria-hidden="true">›</span></li>\n'
        else:
            lis += f'<li>{label}</li>\n'
    return f'<nav class="breadcrumb" aria-label="Localização na página"><div class="container"><ol>{lis}</ol></div></nav>'

def build_trail_card(t):
    diff = t["difficulty"]
    diff_label = DIFF_LABELS.get(diff, diff)
    diff_css = DIFF_CSS.get(diff, diff)
    dist_str = f'{t["distanceKm"]} km'
    elev_str = f'+{t["elevationGain"]:,} m'.replace(",", ".")
    return f"""
      <article class="trail-card" data-difficulty="{diff}" data-distance="{t['distanceKm']}" data-type="{t.get('trailType','linear')}">
        <div class="trail-img">
          <img src="{t['imageUrl']}" alt="{t['name']}" loading="lazy" width="400" height="225">
          <span class="diff-badge diff-{diff_css}">{diff_label}</span>
        </div>
        <div class="trail-body">
          <h3 class="trail-name">{t['name']}</h3>
          <div class="trail-location">{PIN_ICON} {t['city']} · {t['region']} · {t['uf']}</div>
          <p class="trail-desc">{t['shortDescription']}</p>
          <div class="trail-meta">
            <div class="meta-item"><span class="meta-label">Distância</span><span class="meta-value">{dist_str}</span></div>
            <div class="meta-item"><span class="meta-label">Duração</span><span class="meta-value">{t['estimatedTime']}</span></div>
            <div class="meta-item"><span class="meta-label">Desnível</span><span class="meta-value">{elev_str}</span></div>
          </div>
          <div class="trail-footer">
            <a href="/trilha/{t['slug']}" class="btn btn--primary btn--sm" style="width:100%">Ver detalhes da trilha</a>
          </div>
        </div>
      </article>"""

def build_trails_section(trails_list, heading, section_id="trilhas"):
    cards_html = "".join(build_trail_card(t) for t in trails_list)
    n = len(trails_list)
    filter_html = ""
    if n > 1:
        filter_html = f"""
    <div class="filters-wrap">
      <p class="filters-title">Filtrar trilhas</p>
      <div class="filters-grid">
        <select class="filter-select" id="f-diff" aria-label="Dificuldade">
          <option value="">Dificuldade</option>
          <option value="easy">Fácil</option>
          <option value="moderate">Moderado</option>
          <option value="hard">Difícil</option>
          <option value="expert">Especialista</option>
        </select>
        <select class="filter-select" id="f-dist" aria-label="Distância">
          <option value="">Distância</option>
          <option value="short">Até 5 km</option>
          <option value="medium">5–15 km</option>
          <option value="long">Acima de 15 km</option>
        </select>
        <select class="filter-select" id="f-type" aria-label="Tipo">
          <option value="">Tipo</option>
          <option value="linear">Linear</option>
          <option value="circular">Circular</option>
          <option value="traverse">Travessia</option>
        </select>
        <button class="filter-reset" id="filter-reset">Limpar filtros</button>
      </div>
      <p class="filter-count" id="filter-count" aria-live="polite"></p>
    </div>"""
    return f"""<section class="section" id="{section_id}" aria-labelledby="trails-h2">
  <div class="container">
    <h2 id="trails-h2">{heading}</h2>
    {filter_html}
    <div class="trails-grid" id="trails-grid">{cards_html}
    </div>
    <div id="no-results" class="no-results" style="display:none" role="status" aria-live="polite">
      <p style="font-size:1rem;font-weight:600;margin-bottom:.5rem">Nenhuma trilha encontrada com esses filtros.</p>
      <p><button onclick="document.getElementById('filter-reset').click()" style="background:none;border:none;color:var(--primary);font-size:.95rem;cursor:pointer;font-family:var(--font-body);font-weight:600;padding:0">Limpar filtros</button></p>
    </div>
  </div>
</section>"""

def build_guide_card(g):
    name = g.get("name", "Guia")
    initial = name[0].upper() if name else "G"
    city = g.get("city", "")
    uf = g.get("uf", "")
    cats = g.get("categories", [])
    cadastur = g.get("cadasturNumber", "")
    valid = g.get("validUntil", "")
    cats_html = "".join(f'<span class="guide-cat">{c}</span>' for c in cats[:2])
    return f"""
      <div class="guide-card">
        <div class="guide-header">
          <div class="guide-avatar" aria-hidden="true">{initial}</div>
          <div class="guide-info">
            <div class="guide-name">{name.title()}</div>
            <div class="guide-city">{city} · {uf}</div>
          </div>
        </div>
        <span class="guide-status">Em validação</span>
        <div class="guide-cats">{cats_html}</div>
        <div class="guide-cadastur">CADASTUR: {cadastur} · válido até {valid[:7] if valid else 'consulte'}</div>
        <div class="guide-actions"><a href="/guias/ativar-perfil" class="btn btn--outline btn--sm">Ver perfil</a></div>
      </div>"""

def build_guides_section(guides_list, context_label, uf=None):
    if not guides_list:
        return ""
    cards_html = "".join(build_guide_card(g) for g in guides_list[:3])
    region_text = f" {context_label}" if context_label else ""
    return f"""<section class="section section--green" id="guias" aria-labelledby="guides-h2">
  <div class="container">
    <h2 id="guides-h2">Guias que atuam{region_text}</h2>
    <p style="margin-bottom:0;max-width:680px">Encontre guias com CADASTUR certificado para acompanhar sua trilha com segurança e experiência local.</p>
    <div class="guides-grid">{cards_html}
    </div>
    <div class="trust-box" style="margin-top:2rem;max-width:720px">
      <h3>Perfis em validação</h3>
      <p>Os perfis acima foram importados da base pública do CADASTUR e estão em processo de validação. Guias que ativarem seu perfil no Trekko aparecem com informações completas e canal de contato habilitado.</p>
      <div style="margin-top:1rem"><a href="/guias/ativar-perfil" class="btn btn--primary btn--sm">Ativar perfil de guia</a></div>
    </div>
  </div>
</section>"""

def build_tips_section(tips, heading):
    items = ""
    for i, (title, text) in enumerate(tips, 1):
        items += f"""
      <div class="how-item">
        <div class="how-num" aria-hidden="true">{i}</div>
        <div class="how-text"><h4>{title}</h4><p>{text}</p></div>
      </div>"""
    return f"""<section class="section" aria-labelledby="tips-h2">
  <div class="container">
    <h2 id="tips-h2">{heading}</h2>
    <div class="how-grid">{items}
    </div>
  </div>
</section>"""

def build_testimonials_section(trail_count, guide_count, state_count):
    guide_display = f"{guide_count // 1000}k+" if guide_count >= 1000 else str(guide_count)
    stars = '<div class="t-stars" aria-label="5 estrelas">' + '<span class="t-star" aria-hidden="true">★</span>' * 5 + '</div>'
    cards = ""
    for t in TESTIMONIALS:
        cards += f"""
      <article class="testimonial-card">
        {stars}
        <p class="t-quote">"{t['quote']}"</p>
        <footer class="t-footer">
          <div class="t-avatar" aria-hidden="true">{t['initial']}</div>
          <div>
            <div class="t-name">{t['name']}</div>
            <div class="t-trail">{t['trail']}</div>
          </div>
        </footer>
      </article>"""
    return f"""<section class="section section--alt" aria-labelledby="sp-h2">
  <div class="container">
    <h2 id="sp-h2">Por que trilheiros confiam no Trekko</h2>
    <p style="max-width:640px;margin-bottom:2rem">Fichas com dados reais de campo, guias certificados CADASTUR e informações verificadas para você planejar com segurança.</p>
    <div class="sp-stats" role="list" aria-label="Números do Trekko">
      <div class="sp-stat" role="listitem">
        <span class="sp-stat-num">{trail_count}+</span>
        <span class="sp-stat-label">trilhas com fichas detalhadas</span>
      </div>
      <div class="sp-stat" role="listitem">
        <span class="sp-stat-num">{guide_display}</span>
        <span class="sp-stat-label">guias CADASTUR cadastrados</span>
      </div>
      <div class="sp-stat" role="listitem">
        <span class="sp-stat-num">{state_count}</span>
        <span class="sp-stat-label">estados com trilhas listadas</span>
      </div>
    </div>
    <div class="testimonials-grid" aria-label="Depoimentos de trilheiros">{cards}
    </div>
    <div class="sp-trust" role="list" aria-label="Selos de confiança">
      <span class="sp-badge" role="listitem">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M7 1l1.5 4.5H13L9 8l1.5 4.5L7 10l-3.5 2.5L5 8 1 5.5h4.5L7 1z" stroke="#15803d" stroke-width="1.3" stroke-linejoin="round" fill="none"/></svg>
        Guias certificados CADASTUR
      </span>
      <span class="sp-badge" role="listitem">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="5.5" stroke="#15803d" stroke-width="1.3"/><path d="M4.5 7l2 2 3-3" stroke="#15803d" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Fichas verificadas por especialistas
      </span>
      <span class="sp-badge" role="listitem">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M7 2a5 5 0 100 10A5 5 0 007 2z" stroke="#15803d" stroke-width="1.3"/><path d="M7 4.5v3L9 9" stroke="#15803d" stroke-width="1.3" stroke-linecap="round"/></svg>
        Estimativas de tempo reais de campo
      </span>
      <span class="sp-badge" role="listitem">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2 7h10M2 4h10M2 10h6" stroke="#15803d" stroke-width="1.3" stroke-linecap="round"/></svg>
        Informações atualizadas regularmente
      </span>
    </div>
  </div>
</section>"""

def build_faq_section(faqs, heading):
    items = ""
    for i, (q, a) in enumerate(faqs, 1):
        items += f"""
      <div class="faq-item">
        <button class="faq-q" aria-expanded="false" aria-controls="faq-a{i}" id="faq-q{i}">
          {q}{FAQ_ARROW}
        </button>
        <div class="faq-a" id="faq-a{i}" role="region" aria-labelledby="faq-q{i}">
          <div class="faq-a-inner">{a}</div>
        </div>
      </div>"""
    return f"""<section class="section section--alt" aria-labelledby="faq-h2">
  <div class="container">
    <h2 id="faq-h2">{heading}</h2>
    <div class="faq-list">{items}
    </div>
  </div>
</section>"""

def build_cta_section(h2, p, path, btn1_label="Explorar trilhas", btn2_label="Ver guias certificados"):
    return f"""<section class="cta-final" aria-labelledby="cta-h2">
  <div class="container">
    <h2 id="cta-h2">{h2}</h2>
    <p>{p}</p>
    <div class="cta-btns">
      <a href="#trilhas" class="btn btn--white btn--lg">{btn1_label}</a>
      <a href="/guias" class="btn btn--outline-white btn--lg">{btn2_label}</a>
    </div>
  </div>
</section>"""

def build_faq_jsonld(faqs, canonical):
    faq_items = [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Trekko", "item": "https://trekko.com.br"},
                    {"@type": "ListItem", "position": 2, "name": "Trilhas", "item": "https://trekko.com.br/trilhas"},
                    {"@type": "ListItem", "position": 3, "name": canonical.split("/")[-1] or canonical, "item": f"https://trekko.com.br{canonical}"},
                ],
            },
            {"@type": "FAQPage", "mainEntity": faq_items},
        ],
    }
    return json.dumps(data, ensure_ascii=False)

def build_item_list_jsonld(trails_list, canonical, list_name):
    elements = [
        {
            "@type": "ListItem",
            "position": i + 1,
            "url": f"https://trekko.com.br/trilha/{t['slug']}",
            "name": t["name"],
        }
        for i, t in enumerate(trails_list)
    ]
    data = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": list_name,
        "url": f"https://trekko.com.br{canonical}",
        "numberOfItems": len(trails_list),
        "itemListElement": elements,
    }
    return json.dumps(data, ensure_ascii=False)

# ── Group data ───────────────────────────────────────────────────────────────
by_uf   = defaultdict(list)
by_diff = defaultdict(list)
by_city = {}   # city_slug -> {"name", "uf", "trails"}
by_park = {}   # park_slug -> {"name", "trails"}

for t in trails:
    by_uf[t["uf"]].append(t)
    by_diff[t["difficulty"]].append(t)
    cs = slugify(t["city"])
    if cs not in by_city:
        by_city[cs] = {"name": t["city"], "uf": t["uf"], "trails": []}
    by_city[cs]["trails"].append(t)
    ps = slugify(t["park"])
    if ps not in by_park:
        by_park[ps] = {"name": t["park"], "trails": []}
    by_park[ps]["trails"].append(t)

# Sample guides per UF (max 3)
guides_by_uf = defaultdict(list)
for g in all_guides:
    uf = g.get("uf", "").upper()
    if uf and len(guides_by_uf[uf]) < 3:
        guides_by_uf[uf].append(g)

SP_TRAIL_COUNT = len(trails)
SP_GUIDE_COUNT = len(all_guides)
SP_STATE_COUNT = len(by_uf)

# ── State pages ──────────────────────────────────────────────────────────────
def build_state_page(uf, uf_trails):
    uf_name = UF_NAMES[uf]
    uf_slug = UF_SLUGS[uf]
    uf_prep = UF_PREP[uf]
    content = STATE_CONTENT.get(uf, {})
    canonical_path = f"/trilhas/{uf_slug}"
    canonical = f"https://trekko.com.br{canonical_path}"
    title = f"Trilhas {uf_prep}: roteiros, parques e guias | Trekko"
    desc = f"Descubra as melhores trilhas {uf_prep}. Roteiros por dificuldade, distância e parques. Guias certificados CADASTUR prontos para acompanhar você."
    hero_img = content.get("hero_image", uf_trails[0]["imageUrl"] if uf_trails else "/trails/bCKTbP7YuBYO.jpg")
    n_trails = len(uf_trails)
    n_guides = len(guides_by_uf.get(uf, []))
    parks = list({t["park"] for t in uf_trails})
    faqs = content.get("faqs", [
        (f"Quais são as melhores trilhas {uf_prep}?",
         f"O Trekko lista {n_trails} trilha{'s' if n_trails>1 else ''} catalogada{'s' if n_trails>1 else ''} {uf_prep}. Confira as opções acima filtradas por dificuldade e distância."),
        (f"Preciso de guia para trilhas {uf_prep}?",
         "Depende da trilha. Algumas exigem guia obrigatório por regulamento do parque; outras apenas recomendam. Verifique a ficha de cada trilha para informação atualizada."),
        (f"Qual a melhor época para trilhar {uf_prep}?",
         "A melhor época varia por trilha e região. Consulte a seção 'Melhor época' em cada ficha de trilha para informação específica."),
    ])
    jsonld = build_faq_jsonld(faqs, canonical_path)
    head = build_head(title, desc, canonical, hero_img, jsonld)
    header = build_header()
    breadcrumb = build_breadcrumb([
        ("Trekko", "/"), ("Trilhas", "/trilhas"), (f"Trilhas {uf_prep}", canonical_path)
    ])
    hero = f"""<section class="hero" style="--hero-bg:url('{hero_img}')">
  <div class="container">
    <div class="hero-inner">
      <div class="hero-badge">📍 {uf_name}</div>
      <h1>Trilhas {uf_prep}</h1>
      <p class="hero-subtitle">{content.get('subtitle', f'Explore trilhas {uf_prep} — roteiros detalhados, dificuldades, parques e guias certificados.')}</p>
      <div class="hero-ctas">
        <a href="#trilhas" class="btn btn--white btn--lg">Ver trilhas</a>
        <a href="/guias" class="btn btn--outline-white btn--lg">Encontrar guias</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><strong>{n_trails}</strong><span>trilha{'s' if n_trails>1 else ''}</span></div>
        <div class="stat"><strong>{len(parks)}</strong><span>parque{'s' if len(parks)>1 else ''}</span></div>
        <div class="stat"><strong>CADASTUR</strong><span>guias certificados</span></div>
      </div>
    </div>
  </div>
</section>"""
    editorial_text = content.get("editorial", "")
    editorial_html = ""
    if editorial_text:
        editorial_html = f"""<section class="section">
  <div class="container editorial">
    <h2>Trekking {uf_prep}</h2>
    <p>{editorial_text}</p>
  </div>
</section>"""
    trails_section = build_trails_section(
        uf_trails, f"Trilhas {uf_prep} ({n_trails})")
    tips = content.get("tips", [])
    tips_section = build_tips_section(tips, f"Como planejar sua trilha {uf_prep}") if tips else ""
    testimonials_section = build_testimonials_section(SP_TRAIL_COUNT, SP_GUIDE_COUNT, SP_STATE_COUNT)
    guides = guides_by_uf.get(uf, [])
    guides_section = build_guides_section(guides, uf_prep) if guides else ""
    faq_section = build_faq_section(faqs, f"Perguntas frequentes sobre trilhas {uf_prep}")
    cta_section = build_cta_section(
        f"Encontre sua próxima trilha {uf_prep}",
        f"Compare roteiros, veja dificuldade, parques e guias. Planeje com informação e segurança.",
        canonical_path,
    )
    js = PAGE_JS.format(
        event_name="page_view_trail_landing",
        event_params={"state": uf_slug, "page_type": "trail_state_landing"},
    )
    return "\n".join([
        head, "<body>", header, breadcrumb, hero,
        editorial_html, trails_section, tips_section,
        testimonials_section, guides_section, faq_section, cta_section,
        FOOTER_HTML, js, STICKY_BAR, "</body>\n</html>",
    ])

# ── City pages ───────────────────────────────────────────────────────────────
def build_city_page(city_slug, city_name, uf, city_trails):
    uf_name = UF_NAMES.get(uf, uf)
    canonical_path = f"/trilhas/cidades/{city_slug}"
    canonical = f"https://trekko.com.br{canonical_path}"
    parks = list({t["park"] for t in city_trails})
    park_str = " e ".join(parks[:2])
    title = f"Trilhas em {city_name}, {uf} — {park_str} | Trekko"
    desc = f"Trilhas em {city_name} ({uf}): roteiros no {park_str}. Dificuldade, distância, guias certificados e tudo que você precisa para planejar."
    hero_img = city_trails[0]["imageUrl"]
    n = len(city_trails)
    faqs = [
        (f"Como chegar a {city_name} ({uf})?",
         f"{city_name} é a base para trilhas no {parks[0]}. Consulte rotas de acesso na ficha de cada trilha e com guias locais."),
        (f"Preciso de guia para trilhar em {city_name}?",
         f"{'Sim, guia é obrigatório para pelo menos uma das trilhas em ' + city_name if any(t.get('guideRequired') for t in city_trails) else 'Nenhuma trilha em ' + city_name + ' exige guia por regulamento, mas o acompanhamento é recomendado para maior segurança.'}"),
        (f"Qual o melhor período para visitar {city_name}?",
         f"Consulte a seção 'Melhor época' na ficha de cada trilha em {city_name} para recomendações atualizadas por percurso."),
        (f"Há acomodações disponíveis em {city_name}?",
         f"{city_name} tem opções de hospedagem para trilheiros. Para locais muito remotos, camping pode ser a principal alternativa."),
    ]
    jsonld = build_faq_jsonld(faqs, canonical_path)
    head = build_head(title, desc, canonical, hero_img, jsonld)
    header = build_header()
    breadcrumb = build_breadcrumb([
        ("Trekko", "/"), ("Trilhas", "/trilhas"),
        (f"Cidades", "/trilhas"), (city_name, canonical_path),
    ])
    hero = f"""<section class="hero" style="--hero-bg:url('{hero_img}')">
  <div class="container">
    <div class="hero-inner">
      <div class="hero-badge">📍 {city_name}, {uf_name}</div>
      <h1>Trilhas em {city_name}</h1>
      <p class="hero-subtitle">{park_str} · {n} trilha{'s' if n>1 else ''} catalogada{'s' if n>1 else ''} no Trekko</p>
      <div class="hero-ctas">
        <a href="#trilhas" class="btn btn--white btn--lg">Ver trilhas</a>
        <a href="/guias" class="btn btn--outline-white btn--lg">Encontrar guias</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><strong>{n}</strong><span>trilha{'s' if n>1 else ''}</span></div>
        <div class="stat"><strong>{len(parks)}</strong><span>parque{'s' if len(parks)>1 else ''}</span></div>
        <div class="stat"><strong>{uf}</strong><span>{uf_name}</span></div>
      </div>
    </div>
  </div>
</section>"""
    trails_section = build_trails_section(
        city_trails, f"Trilhas em {city_name} ({n})")
    testimonials_section = build_testimonials_section(SP_TRAIL_COUNT, SP_GUIDE_COUNT, SP_STATE_COUNT)
    guides = guides_by_uf.get(uf, [])
    guides_section = build_guides_section(guides, f"em {city_name} e região") if guides else ""
    faq_section = build_faq_section(faqs, f"Perguntas frequentes sobre trilhas em {city_name}")
    cta_section = build_cta_section(
        f"Planeje sua trilha em {city_name}",
        f"Compare roteiros no {park_str} e encontre guias certificados para acompanhar você.",
        canonical_path,
    )
    js = PAGE_JS.format(
        event_name="page_view_trail_landing",
        event_params={"city": city_slug, "page_type": "trail_city_landing"},
    )
    return "\n".join([
        head, "<body>", header, breadcrumb, hero,
        trails_section, testimonials_section, guides_section, faq_section, cta_section,
        FOOTER_HTML, js, STICKY_BAR, "</body>\n</html>",
    ])

# ── Park pages ───────────────────────────────────────────────────────────────
def build_park_page(park_slug, park_name, park_trails):
    canonical_path = f"/trilhas/parques/{park_slug}"
    canonical = f"https://trekko.com.br{canonical_path}"
    ufs = list({t["uf"] for t in park_trails})
    uf_names = " / ".join(UF_NAMES.get(u, u) for u in ufs)
    hero_img = park_trails[0]["imageUrl"]
    n = len(park_trails)
    diffs = list({t["difficulty"] for t in park_trails})
    diff_labels = " · ".join(DIFF_LABELS.get(d, d) for d in diffs)
    title = f"Trilhas no {park_name} — Roteiros, guias e acesso | Trekko"
    desc = f"Trilhas no {park_name} ({uf_names}): roteiros, dificuldade, taxa de entrada, melhor época e guias certificados CADASTUR."
    is_apa = "APA" in park_name or "Área de Proteção" in park_name
    park_type = "APA" if is_apa else "Parque Nacional"
    faqs = [
        (f"Como visitar o {park_name}?",
         f"O {park_name} fica em {uf_names}. O acesso varia conforme a trilha escolhida. Consulte a ficha de cada trilha para informações atualizadas sobre acesso, taxa de entrada e horários."),
        (f"Preciso pagar entrada no {park_name}?",
         f"{'APAs geralmente não cobram taxa de entrada para acesso geral. Confirme se há cobrança para áreas específicas.' if is_apa else 'Sim, parques nacionais cobram taxa de entrada. O valor é atualizado periodicamente pelo ICMBio. Consulte a ficha de cada trilha ou o site oficial do parque para o valor vigente.'}"),
        (f"Preciso de guia no {park_name}?",
         f"{'Pelo menos uma trilha neste parque exige guia obrigatório. Verifique a ficha de cada percurso.' if any(t.get('guideRequired') for t in park_trails) else 'Nenhuma trilha exige guia obrigatório por regulamento, mas o acompanhamento profissional é recomendado para maior segurança e experiência.'}"),
        (f"Qual a melhor época para visitar o {park_name}?",
         f"A melhor época varia conforme a trilha. Consulte a seção 'Melhor época' em cada ficha de trilha para recomendações específicas."),
        (f"Quais trilhas existem no {park_name}?",
         f"O Trekko lista {n} trilha{'s' if n>1 else ''} no {park_name}. Veja as fichas completas acima."),
    ]
    jsonld = build_faq_jsonld(faqs, canonical_path)
    head = build_head(title, desc, canonical, hero_img, jsonld)
    header = build_header()
    breadcrumb = build_breadcrumb([
        ("Trekko", "/"), ("Trilhas", "/trilhas"),
        ("Parques", "/trilhas"), (park_name, canonical_path),
    ])
    hero = f"""<section class="hero" style="--hero-bg:url('{hero_img}')">
  <div class="container">
    <div class="hero-inner">
      <div class="hero-badge">🌿 {park_type}</div>
      <h1>Trilhas no {park_name}</h1>
      <p class="hero-subtitle">{uf_names} · {diff_labels} · {n} trilha{'s' if n>1 else ''} catalogada{'s' if n>1 else ''}</p>
      <div class="hero-ctas">
        <a href="#trilhas" class="btn btn--white btn--lg">Ver trilhas</a>
        <a href="/guias" class="btn btn--outline-white btn--lg">Encontrar guias</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><strong>{n}</strong><span>trilha{'s' if n>1 else ''}</span></div>
        <div class="stat"><strong>{len(ufs)}</strong><span>estado{'s' if len(ufs)>1 else ''}</span></div>
        <div class="stat"><strong>ICMBio</strong><span>unidade de conservação</span></div>
      </div>
    </div>
  </div>
</section>"""
    trails_section = build_trails_section(
        park_trails, f"Trilhas no {park_name} ({n})")
    testimonials_section = build_testimonials_section(SP_TRAIL_COUNT, SP_GUIDE_COUNT, SP_STATE_COUNT)
    guides = []
    for uf in ufs:
        guides.extend(guides_by_uf.get(uf, []))
    guides_section = build_guides_section(guides[:3], f"no {park_name} e região") if guides else ""
    faq_section = build_faq_section(faqs, f"Perguntas frequentes sobre o {park_name}")
    cta_section = build_cta_section(
        f"Prepare sua visita ao {park_name}",
        "Compare trilhas, veja dificuldades e encontre guias certificados para uma experiência segura e memorável.",
        canonical_path,
    )
    js = PAGE_JS.format(
        event_name="page_view_trail_landing",
        event_params={"park": park_slug, "page_type": "trail_park_landing"},
    )
    return "\n".join([
        head, "<body>", header, breadcrumb, hero,
        trails_section, testimonials_section, guides_section, faq_section, cta_section,
        FOOTER_HTML, js, STICKY_BAR, "</body>\n</html>",
    ])

# ── Difficulty pages ──────────────────────────────────────────────────────────
def build_difficulty_page(diff_key, diff_trails):
    content = DIFF_CONTENT[diff_key]
    slug = content["slug"]
    title_str = content["title"]
    canonical_path = f"/trilhas/{slug}"
    canonical = f"https://trekko.com.br{canonical_path}"
    diff_label = DIFF_LABELS[diff_key]
    hero_img = diff_trails[0]["imageUrl"] if diff_trails else "/trails/bCKTbP7YuBYO.jpg"
    n = len(diff_trails)
    ufs = list({t["uf"] for t in diff_trails})
    title = f"{title_str} — Roteiros e guias | Trekko"
    desc = f"Encontre trilhas {diff_label.lower()}s no Brasil: roteiros em {', '.join(UF_NAMES.get(u,u) for u in ufs[:3])} e mais. Dificuldade, distância e guias certificados CADASTUR."
    faqs = content.get("faqs", [])
    jsonld = build_faq_jsonld(faqs, canonical_path)
    head = build_head(title, desc, canonical, hero_img, jsonld)
    header = build_header()
    breadcrumb = build_breadcrumb([
        ("Trekko", "/"), ("Trilhas", "/trilhas"),
        (f"Trilhas {diff_label}s", canonical_path),
    ])
    hero = f"""<section class="hero" style="--hero-bg:url('{hero_img}')">
  <div class="container">
    <div class="hero-inner">
      <div class="hero-badge">⛰️ Nível: {diff_label}</div>
      <h1>{title_str}</h1>
      <p class="hero-subtitle">{content['subtitle']}</p>
      <div class="hero-ctas">
        <a href="#trilhas" class="btn btn--white btn--lg">Ver trilhas</a>
        <a href="/guias" class="btn btn--outline-white btn--lg">Encontrar guias</a>
      </div>
      <div class="hero-stats">
        <div class="stat"><strong>{n}</strong><span>trilha{'s' if n>1 else ''}</span></div>
        <div class="stat"><strong>{len(ufs)}</strong><span>estado{'s' if len(ufs)>1 else ''}</span></div>
        <div class="stat"><strong>{diff_label}</strong><span>nível</span></div>
      </div>
    </div>
  </div>
</section>"""
    editorial_html = f"""<section class="section">
  <div class="container editorial">
    <h2>{title_str}</h2>
    <p>{content['editorial']}</p>
  </div>
</section>"""
    trails_section = build_trails_section(
        diff_trails, f"Trilhas {diff_label}s no Brasil ({n})")
    what_means = content.get("what_means", [])
    what_section = build_tips_section(what_means, f"O que significa trilha {diff_label.lower()}?") if what_means else ""
    # aggregate guides from all states represented
    testimonials_section = build_testimonials_section(SP_TRAIL_COUNT, SP_GUIDE_COUNT, SP_STATE_COUNT)
    guides = []
    for uf in ufs:
        guides.extend(guides_by_uf.get(uf, []))
    guides_section = build_guides_section(guides[:3], f"em trilhas {diff_label.lower()}s") if guides else ""
    faq_section = build_faq_section(faqs, f"Perguntas frequentes sobre trilhas {diff_label.lower()}s")
    cta_section = build_cta_section(
        f"Pronto para uma trilha {diff_label.lower()}?",
        "Compare roteiros, avalie dificuldade e encontre guias certificados para sua próxima aventura.",
        canonical_path,
    )
    js = PAGE_JS.format(
        event_name="page_view_trail_landing",
        event_params={"difficulty": diff_key, "page_type": "trail_diff_landing"},
    )
    return "\n".join([
        head, "<body>", header, breadcrumb, hero,
        editorial_html, trails_section, what_section,
        testimonials_section, guides_section, faq_section, cta_section,
        FOOTER_HTML, js, STICKY_BAR, "</body>\n</html>",
    ])

# ── Generate all pages ────────────────────────────────────────────────────────
total = 0

print("\nGenerating state pages...")
for uf, uf_trails in by_uf.items():
    slug = UF_SLUGS.get(uf)
    if not slug or slug in EXISTING_STATE_SLUGS:
        print(f"  skip  /trilhas/{slug}/ (already exists)")
        continue
    html = build_state_page(uf, uf_trails)
    write_file(os.path.join(BASE, "trilhas", slug, "index.html"), html)
    total += 1

print("\nGenerating difficulty pages...")
for diff_key, diff_trails in by_diff.items():
    slug = DIFF_SLUGS.get(diff_key)
    if not slug or slug in EXISTING_DIFF_SLUGS:
        print(f"  skip  /trilhas/{slug}/ (already exists)")
        continue
    if diff_key not in DIFF_CONTENT:
        continue
    html = build_difficulty_page(diff_key, diff_trails)
    write_file(os.path.join(BASE, "trilhas", slug, "index.html"), html)
    total += 1

print("\nGenerating city pages...")
for city_slug, city_data in by_city.items():
    html = build_city_page(
        city_slug, city_data["name"], city_data["uf"], city_data["trails"])
    write_file(os.path.join(BASE, "trilhas", "cidades", city_slug, "index.html"), html)
    total += 1

print("\nGenerating park pages...")
for park_slug, park_data in by_park.items():
    html = build_park_page(park_slug, park_data["name"], park_data["trails"])
    write_file(os.path.join(BASE, "trilhas", "parques", park_slug, "index.html"), html)
    total += 1

print(f"\nDone: {total} landing pages generated.")
