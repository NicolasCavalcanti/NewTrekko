#!/usr/bin/env python3
"""
DEV-09: Injetar conteúdo editorial nas páginas de cidades
Garante:
 - ≥ 400 palavras de texto visível no HTML estático
 - grep -c "<p>" retorna ≥ 8
 - Texto visível sem JavaScript
"""

import os
import re

BASE_DIR = os.path.join(os.path.dirname(__file__), "trilhas", "cidades")

# ---------------------------------------------------------------------------
# Conteúdo editorial por cidade
# Cada entrada tem: title, paragraphs (lista de parágrafos bare <p>)
# Os parágrafos são divididos em grupos por heading H2
# ---------------------------------------------------------------------------
CITY_CONTENT = {
    "rio-de-janeiro": {
        "sections": [
            {
                "h2": "Natureza e aventura urbana no Rio de Janeiro",
                "paragraphs": [
                    "O Rio de Janeiro é uma das poucas metrópoles do mundo onde a natureza selvagem e o ambiente urbano coexistem a poucos minutos de distância. A cidade é cercada por maciços, morros cobertos de Mata Atlântica e áreas de proteção ambiental que abrigam trilhas para todos os níveis de experiência, do iniciante ao alpinista experiente.",
                    "O Morro Dois Irmãos é talvez a trilha urbana mais icônica do Rio. Partindo da comunidade do Vidigal, o percurso de aproximadamente 5 km escala até um mirante que oferece uma das vistas mais espetaculares da cidade: Ipanema, Leblon, a Lagoa Rodrigo de Freitas, o Pão de Açúcar e o Corcovado, tudo em um único panorama de 360 graus que deixa qualquer trilheiro sem fôlego.",
                    "Além do Morro Dois Irmãos, o maciço da Tijuca abriga dezenas de trilhas dentro do maior parque florestal urbano do mundo. Picos como a Pedra da Gávea, o Bico do Papagaio e as cachoeiras do Taunay e Cascatinha Taunay são destinos clássicos que atraem moradores e turistas o ano inteiro. O Parque Estadual da Pedra Branca, na Zona Oeste, complementa o cardápio com trilhas ainda mais remotas e menos frequentadas.",
                ],
            },
            {
                "h2": "Como se preparar para trilhar no Rio de Janeiro",
                "paragraphs": [
                    "As trilhas cariocas exigem atenção especial à hidratação: o calor tropical pode ser intenso, especialmente entre outubro e março, e algumas subidas são bastante expostas ao sol. Leve ao menos 1,5 litro de água por pessoa para percursos de até 3 horas, e protetor solar com alto fator de proteção. Saias sem o sol a pino — o ideal é partir antes das 8h da manhã.",
                    "Calçado com boa aderência é fundamental nas trilhas do Rio, pois muitos trechos passam por rocha exposta que pode ficar escorregadia após a chuva. Tênis de trilha leve ou bota low-cut funcionam bem na maioria dos percursos. Para o Morro Dois Irmãos e trilhas similares no nível moderado, bastão de caminhada é optativo, mas ajuda nas descidas mais íngremes.",
                    "Antes de partir, informe-se sobre o estado das trilhas com o ICMBio, a Secretaria Municipal de Meio Ambiente ou guias locais certificados. Condições climáticas mudam rapidamente no verão carioca, e é comum que trilhas sejam fechadas temporariamente após chuvas fortes. Ir acompanhado é sempre mais seguro, especialmente para trilhas fora dos parques mais movimentados.",
                ],
            },
            {
                "h2": "Melhor época para visitar e trilhar no Rio de Janeiro",
                "paragraphs": [
                    "O período de maio a setembro corresponde ao inverno carioca — seco, com temperaturas amenas (18 a 28°C) e céu azul a maior parte do tempo. É a melhor janela para trilhas, pois o mato está menos denso, o terreno está mais firme e as vistas dos mirantes são mais nítidas, sem a neblina típica dos dias úmidos.",
                    "O verão (dezembro a março) traz calor intenso, chuvas concentradas à tarde e maior risco de deslizamentos nas encostas. Apesar disso, muitos trilheiros experientes aproveitam a estação chuvosa: a vegetação fica exuberante, as cachoeiras enchem e o verde da Mata Atlântica fica ainda mais vibrante. O segredo é sair cedo e ficar atento à previsão do tempo.",
                    "O Rio de Janeiro atrai visitantes o ano inteiro, e trilhas populares como o Morro Dois Irmãos costumam estar cheias aos finais de semana. Para uma experiência mais tranquila, prefira os dias úteis pela manhã. Guias locais habilitados pelo CADASTUR conhecem os melhores horários e as rotas alternativas para fugir do fluxo intenso de visitantes.",
                ],
            },
        ]
    },
    "alto-caparao": {
        "sections": [
            {
                "h2": "O teto do Sul do Brasil: trilhas em Alto Caparaó",
                "paragraphs": [
                    "Alto Caparaó, no sul de Minas Gerais, é a porta de entrada para o Parque Nacional do Caparaó e o destino obrigatório de quem quer alcançar o Pico da Bandeira — com seus 2.891 metros, o ponto mais alto de todo o Sul e Sudeste do Brasil. A região combina altiplano campestre, veredas de mata nebular e uma sensação de isolamento do mundo que poucos destinos do país conseguem oferecer.",
                    "O percurso clássico ao Pico da Bandeira parte do vale do Macieira e sobe por uma estrada de terra e depois trilha, passando pelo Vale das Agulhas Negras e pelo Pico do Calçado antes de atingir o cume. São aproximadamente 22 km de ida e volta com desnível acumulado superior a 1.800 metros — uma trilha longa e exigente que recompensa com uma vista que, em dias claros, alcança o oceano Atlântico.",
                    "O Parque Nacional do Caparaó é também conhecido pelos campos de altitude cobertos de capim-dourado, pelas espécies endêmicas de flora do cerrado de altitude e pela rica avifauna. Pássaros como o gavião-de-penacho, o pinto-do-mato e diversas espécies de beija-flor raramente vistas em outros lugares do país habitam as encostas do maciço e encantam observadores de aves que chegam à região.",
                ],
            },
            {
                "h2": "Planejamento e logística para trilhar em Alto Caparaó",
                "paragraphs": [
                    "Alto Caparaó fica a cerca de 350 km de Belo Horizonte e pode ser acessado de ônibus ou carro. A entrada principal do parque está a 5 km do centro da cidade, e o acesso de veículo até o portal do parque só é permitido até determinado horário. Para trilhas ao cume, o ideal é pernoitar em Caparaó Caparão — a cidade do lado sul do parque, em território do Espírito Santo — ou em Alto Caparaó mesmo, partindo cedo na manhã seguinte.",
                    "Agasalhos e roupas impermeáveis são essenciais: no topo do Pico da Bandeira a temperatura pode cair abaixo de zero no inverno, e a neblina pode surgir rapidamente mesmo em dias ensolarados. A caminhada ao cume é longa e a exposição ao frio e ao vento aumenta muito acima dos 2.500 metros. Guias habilitados pelo CADASTUR conhecem as variações climáticas e ajudam a planejar o melhor momento para a subida.",
                ],
            },
            {
                "h2": "Melhor época para visitar Alto Caparaó",
                "paragraphs": [
                    "A melhor época para trilhar em Alto Caparaó é de abril a setembro, período seco que garante visibilidade ótima no cume e condições de caminhada mais seguras. As madrugadas de inverno chegam a -5°C no alto do maciço, o que torna a experiência única — inclusive com geada e, raramente, neve. Leve saco de dormir de qualidade se planeja acampar no platô.",
                    "O verão (outubro a março) traz chuvas intensas e pode fechar as trilhas por tempo indeterminado. O parque permanece aberto, mas a subida ao Pico da Bandeira fica desaconselhada em dias de muita precipitação pelo risco de relâmpagos no cume exposto. Mesmo no período chuvoso, as cachoeiras da região inferior do parque ficam mais belas e acessíveis.",
                    "A alta temporada turística coincide com julho e as festas de fim de ano. Reserve acomodação com antecedência nesses períodos. Fora deles, o parque fica muito menos movimentado e a experiência na natureza ganha em qualidade — menos gente na trilha e mais chances de avistar a fauna local.",
                ],
            },
        ]
    },
    "alto-paraiso-de-goias": {
        "sections": [
            {
                "h2": "Chapada dos Veadeiros: natureza ancestral em Alto Paraíso",
                "paragraphs": [
                    "Alto Paraíso de Goiás é a principal cidade de acesso ao Parque Nacional da Chapada dos Veadeiros, reconhecido como Patrimônio Natural da Humanidade pela UNESCO. A região está situada no coração do cerrado brasileiro — o bioma mais ameaçado do planeta e um dos mais biodiversos do mundo — e reúne cânions de quartzo, cachoeiras de águas cristalinas e campos de altitude que parecem ter saído de outro tempo.",
                    "As trilhas da Chapada são marcadas pelo visual único dos cânions esculpidos pelo Rio Preto e afluentes: formações rochosas de quartzo branco e rosado, quedas d'água que caem dezenas de metros em piscinas naturais de água transparente. Os Saltos do Rio Preto, a Cachoeira das Cariocas e os Cânions I e II são os percursos mais famosos, mas a região guarda muitos outros roteiros para quem quer escapar do circuito turístico convencional.",
                    "A vida noturna no cerrado da Chapada é outra experiência à parte: a altitude de 1.200 metros e o baixo índice de poluição luminosa tornam a região um dos melhores pontos de observação astronômica do Brasil Central. Guias especializados oferecem passeios noturnos onde é possível ver nebulosas e galáxias a olho nu — uma experiência que complementa perfeitamente a imersão na natureza diurna.",
                ],
            },
            {
                "h2": "Como se preparar para trilhar em Alto Paraíso de Goiás",
                "paragraphs": [
                    "A maioria das trilhas na Chapada dos Veadeiros exige guia habilitado — uma exigência do parque nacional para proteger o ecossistema frágil do cerrado. Contrate sempre um guia registrado no CADASTUR antes de partir. Além de garantir sua segurança nas trilhas mais remotas, o guia é fundamental para interpretar a ecologia local e respeitar as regras de uso do parque.",
                    "Leve protetor solar de alto fator, chapéu e camisetas de manga longa: o sol do planalto central é intenso e a maioria das trilhas tem poucos trechos de sombra. A água das cachoeiras é potável em muitos pontos, mas carregue ao menos 2 litros por pessoa para trilhas de meio período. Sandálias de neoprene ou tênis que molham são úteis nos percursos que cruzam rios.",
                    "Alto Paraíso de Goiás está a cerca de 230 km de Brasília, com estrada pavimentada até a sede do município. O parque fica a mais 35 km, em São Jorge — vilarejo que serve de base para a maioria das trilhas. São Jorge tem pousadas simples e restaurantes; reserve com antecedência nos feriados prolongados, quando o movimento é intenso.",
                ],
            },
            {
                "h2": "Melhor época para visitar a Chapada dos Veadeiros",
                "paragraphs": [
                    "O período seco, de maio a setembro, oferece as melhores condições para trilhar: sem chuva, rios mais baixos para cruzar com segurança e temperatura agradável entre 15°C e 28°C. As cachoeiras ficam levemente menores, mas o acesso é mais fácil e as piscinas naturais ficam cristalinas. É também o período com mais turistas, então planejamento antecipado é essencial.",
                    "A estação chuvosa (outubro a abril) transforma a Chapada: o cerrado fica verde-vivo, as cachoeiras ficam majestosas e as flores do cerrado cobrem os campos. O Parque Nacional pode fechar trilhas temporariamente por risco de enchentes nos rios. Para quem quer escapar das multidões e ver o cerrado em sua exuberância máxima, março e abril — quando as chuvas já diminuem — são ótimas janelas.",
                ],
            },
        ]
    },
    "andarai-mucuge": {
        "sections": [
            {
                "h2": "Chapada Diamantina: história e natureza entre Andaraí e Mucugê",
                "paragraphs": [
                    "Andaraí e Mucugê são dois dos mais charmosos municípios da Chapada Diamantina, no interior da Bahia, e compõem um dos roteiros de trilha mais ricos e variados do Nordeste brasileiro. A região foi palco da febre do diamante no século XIX, e a história garimpeira ainda marca profundamente a paisagem: grotas escavadas manualmente, ruínas de garimpos e cidades centenárias que parecem paradas no tempo.",
                    "O Parque Nacional da Chapada Diamantina, criado em 1985, protege 152 mil hectares de cerrado de altitude, caatinga, mata ciliar e campo rupestre — um mosaico de ecossistemas que abriga centenas de espécies endêmicas. As trilhas na área de Andaraí incluem percursos até a Cachoeira do Ramalho, a Gruta da Lapa Doce e o Vale do Pati, considerado um dos mais belos trekking de vários dias do Brasil.",
                    "Mucugê, com seu cemitério tombado pelo Patrimônio Histórico Nacional e suas ruas de pedra, é ponto de partida para trilhas até a Cachoeira do Ferro Doido, a Serra do Sincorá e o belíssimo Pai Inácio — um paredão rochoso com vista panorâmica da chapada que, ao entardecer, tinge de laranja e vermelho toda a paisagem em volta.",
                ],
            },
            {
                "h2": "Logística e dicas para trilhar entre Andaraí e Mucugê",
                "paragraphs": [
                    "O Vale do Pati — o mais famoso trekking de vários dias da Chapada — é uma travessia de 3 a 5 dias entre Andaraí e a região de Guiné, passando por fazendas históricas e mirantes de tirar o fôlego. A trilha é obrigatoriamente feita com guia habilitado, e o volume de visitantes é limitado por dia para proteger o ecossistema frágil do vale. Reserve com meses de antecedência nos períodos de alta temporada.",
                    "O acesso a Andaraí e Mucugê é feito por ônibus a partir de Salvador (cerca de 6 horas) ou de carro pela BR-242. A estrada que liga as duas cidades é parcialmente não pavimentada e pode ser intransitável após chuvas fortes. Veículo com tração e boa altura ao solo é recomendado para os acessos aos pontos mais remotos da chapada.",
                    "Mucugê tem infraestrutura turística mais desenvolvida, com pousadas de boa qualidade e restaurantes que servem a gastronomia baiana do sertão — com destaque para a carne de bode, o milho cozido e as cachaças artesanais da região. Andaraí é menor, mas tem pousadas aconchegantes e acesso mais direto às trilhas do vale.",
                ],
            },
            {
                "h2": "Melhor época para visitar Andaraí e Mucugê",
                "paragraphs": [
                    "O inverno baiano, de junho a novembro, é o período ideal para trilhar na Chapada Diamantina. As chuvas são raras, o calor é suportável (20°C a 30°C) e os rios mantêm um volume adequado nas cachoeiras sem o risco de enchentes. Os campos rupestres ficam floridos em julho e agosto, tornando o cenário ainda mais espetacular.",
                    "O verão (dezembro a abril) traz chuvas intensas que podem interromper trilhas, alagar estradas e tornar algumas travessias perigosas. O Parque Nacional restringe o acesso a certas áreas nesse período. Dito isso, a chapada chuvosa tem seu charme: a vegetação fica exuberante e as cachoeiras atingem seu volume máximo, com quedas impressionantes.",
                ],
            },
        ]
    },
    "barreirinhas-atins": {
        "sections": [
            {
                "h2": "Lençóis Maranhenses: dunas e lagoas entre Barreirinhas e Atins",
                "paragraphs": [
                    "O Parque Nacional dos Lençóis Maranhenses é um dos destinos mais surreais do Brasil: 155 mil hectares de dunas brancas que, após as chuvas, formam centenas de lagoas de água doce e transparente entre vales de areia. Barreirinhas, na foz do Rio Preguiças, é a principal cidade de acesso ao parque, enquanto Atins — uma vila de pescadores acessível somente por barco ou 4x4 — fica dentro ou às margens do parque, oferecendo uma experiência ainda mais imersiva.",
                    "As trilhas nos Lençóis são diferentes de qualquer outra no Brasil: sem sombra, sem vegetação densa, sem trilha marcada na areia. Caminha-se sobre as dunas orientando-se pelos pontos cardeais e pela posição do sol. A dificuldade varia com a temperatura — de manhã cedo, a areia ainda está fria e o caminhar é prazeroso; ao meio-dia, sem proteção, a areia pode passar dos 50°C e queimar através de sandálias finas.",
                    "Além das dunas, a região oferece passeios de barco pelo Rio Preguiças, cujas margens são cobertas de manguezais, buritizais e pequenas comunidades de pescadores. O sobrevoo de ultraleve ou parapente sobre os lençóis é uma experiência que muda a perspectiva do lugar: do ar, o contraste entre o branco das dunas e o azul-turquesa das lagoas é absolutamente único.",
                ],
            },
            {
                "h2": "Como se preparar para os Lençóis Maranhenses",
                "paragraphs": [
                    "Protetor solar com fator altíssimo (FPS 70 ou mais), óculos de sol com proteção UV e chapéu de abas largas são itens indispensáveis. O reflexo da areia branca amplifica os raios ultravioleta e queimaduras de pele graves são comuns entre visitantes desprevenidos. Prefira roupas leves de cores claras que cubram braços e pernas.",
                    "Leve água em quantidade generosa — ao menos 2 litros por pessoa para caminhadas de até 4 horas. Nas trilhas mais longas pelos lençóis, reabastecimento é impossível. Guias locais conhecem as lagoas de água potável e os pontos de apoio das comunidades dentro do parque; contratá-los aumenta muito a segurança e a qualidade da experiência.",
                    "Barreirinhas está a 260 km de São Luís, capital do Maranhão. O transporte mais comum é de van ou carro 4x4, já que parte da estrada pode ficar em más condições na época chuvosa. Atins é acessada de barco pelo Rio Preguiças (2 horas) ou de 4x4 pela faixa de praia na maré baixa. Organize o transporte com antecedência, especialmente nos meses de alta temporada.",
                ],
            },
            {
                "h2": "Melhor época para visitar os Lençóis Maranhenses",
                "paragraphs": [
                    "O período de junho a setembro é considerado o melhor para visitar os Lençóis: as lagoas estão no nível máximo, cheias de água doce acumulada pelas chuvas de março a maio, e o tempo está seco e ensolarado. As lagoas maiores, como a Lagoa Bonita e a Lagoa Azul, ficam com profundidade suficiente para nadar e mergulhar com os olhos abertos, revelando o fundo de areia branca.",
                    "Nos meses de outubro a fevereiro, as lagoas secam progressivamente e muitas desaparecem por completo. A paisagem muda mas mantém a beleza: os padrões geométricos das dunas ficam mais visíveis sem as lagoas e os pôr do sol sobre a areia branca são espetaculares. Quem visita nesse período costuma ter menos concorrência por passeios e preços mais baixos.",
                ],
            },
        ]
    },
    "cambara-do-sul": {
        "sections": [
            {
                "h2": "Cânions e campos do Sul: trilhas em Cambará do Sul",
                "paragraphs": [
                    "Cambará do Sul, no nordeste do Rio Grande do Sul, é uma das cidades mais frias e charmosas da Serra Gaúcha — e o ponto de acesso aos cânions mais profundos do Brasil. O Cânion Itaimbezinho, no Parque Nacional da Serra Geral, tem paredes verticais de arenito vermelho que descem 720 metros até o vale do Rio Pelotas. O espetáculo visual é diferente de qualquer outro no país: de cima, você olha para a eternidade verde lá embaixo.",
                    "O Parque Nacional da Serra Geral abriga também o Cânion Fortaleza — menos visitado, mais selvagem e igualmente impressionante. A trilha até a beira do Cânion Fortaleza tem cerca de 7 km de ida e volta e passa por campos de araucária antes de chegar a uma escarpa vertiginosa com vista de 360 graus sobre os campos de cima da serra e o vale lá abaixo. Ao entardecer, a luz dourada banha as paredes do cânion de forma absolutamente cinematográfica.",
                    "Cambará do Sul também é famosa pelo Parque Estadual do Tainhas e pela Rota das Cascatas, um circuito de cachoeiras entre a serra e o litoral gaúcho. Mas são os cânions que colocam a cidade no mapa da aventura nacional — e internacional. Trilheiros de vários países vêm especificamente para contemplar e fotografar essas formações que levaram milhões de anos para tomar a forma atual.",
                ],
            },
            {
                "h2": "Planejamento para trilhar nos cânions de Cambará do Sul",
                "paragraphs": [
                    "O Cânion Itaimbezinho tem duas trilhas principais: a Trilha do Cotovelo (2 km, fácil, até o mirante principal) e a Trilha do Vértice (8 km, moderada, com mais pontos de observação). Ambas estão dentro do Parque Nacional e exigem agendamento prévio pelo site do ICMBio, especialmente nos feriados e julho, quando o fluxo é intenso. Chegue cedo — o parque abre às 8h e as trilhas fecham no meio da tarde.",
                    "O frio em Cambará do Sul é sério: geadas são comuns de maio a agosto, e a temperatura pode cair para vários graus negativos. Mesmo no verão, a temperatura é amena (máxima de 20 a 25°C) e a chuva é frequente. Leve corta-vento impermeável, calça comprida e bota de trilha com bom tornozelamento. A lama nas trilhas após chuva pode ser traiçoeira.",
                    "Cambará do Sul fica a 230 km de Caxias do Sul e 190 km de Florianópolis. O acesso é por estrada asfaltada com trechos de serra. A cidade tem boa infraestrutura de pousadas e restaurantes que servem a culinária gaúcha tradicional — o churrasco e o carneiro no buraco são imperdíveis após um dia de trilha.",
                ],
            },
            {
                "h2": "Melhor época para os cânions de Cambará do Sul",
                "paragraphs": [
                    "O verão austral (outubro a março) é o período mais quente e com mais turistas. As trilhas estão em melhor condição, a vegetação dos campos fica verde e os rios estão mais cheios — o que cria cachoeiras mais vibrantes na base dos cânions. Julho é o pico do turismo de inverno, atraindo quem quer ver geada e, raramente, neve nos campos de altitude.",
                    "A primavera (setembro e outubro) é especialmente bonita: os campos da serra ficam cobertos de flores silvestres, a temperatura é agradável e os cânions têm uma luminosidade suave que favorece a fotografia. O outono (abril e maio) oferece as cores laranjas e vermelhas das araucárias e uma tranquilidade que os feriados de verão e julho raramente permitem.",
                ],
            },
        ]
    },
    "campina-grande-do-sul-antonina": {
        "sections": [
            {
                "h2": "Serra do Mar paranaense: trilhas entre Campina Grande do Sul e Antonina",
                "paragraphs": [
                    "A Serra do Mar do Paraná é um dos últimos grandes remanescentes de Mata Atlântica em estado relativamente preservado do Sul do Brasil. Entre Campina Grande do Sul, no planalto, e Antonina, no litoral, a escarpa da serra cria um gradiente altitudinal impressionante — de 1.100 metros até o nível do mar em menos de 60 km em linha reta — que resulta em uma biodiversidade extraordinária e paisagens que mudam completamente em cada trecho da descida.",
                    "O Parque Estadual do Pico do Paraná, que inclui o ponto mais alto do estado (1.876 m), e o Parque Nacional Saint-Hilaire/Lange são as principais unidades de conservação da região. As trilhas variam de percursos de baixa dificuldade em meio à floresta ombrófila densa até escaladas técnicas que chegam aos cumes mais elevados da Serra do Mar paranaense. A Trilha dos Sete Picos e a subida ao Pico Paraná são os percursos mais procurados.",
                    "Antonina, na Baía de Paranaguá, é também o ponto de chegada de uma das maiores travessias de serra do Sul do Brasil: o Caminho do Anhanguera, que liga o planalto ao litoral seguindo antigas trilhas indígenas e coloniais por dentro da Mata Atlântica. A travessia leva de 3 a 5 dias e oferece uma imersão profunda em um dos ambientes mais ricos do Brasil.",
                ],
            },
            {
                "h2": "Como se preparar para trilhar na Serra do Mar paranaense",
                "paragraphs": [
                    "A Serra do Mar paranaense é uma das áreas com maior pluviosidade do Brasil — precipitação anual pode ultrapassar 3.000 mm. Isso significa que chuva é uma possibilidade real em qualquer época do ano, e roupa impermeável de qualidade é indispensável. Prefira equipamento de trekking com membranas impermeáveis respiráveis e evite roupas de algodão, que ficam pesadas e frias quando molhadas.",
                    "Para a subida ao Pico do Paraná e trilhas longas na serra, contrate guia habilitado pelo CADASTUR. Os caminhos cruzam áreas sem sinalização clara e podem ficar com visibilidade zero em dias de neblina densa — uma situação comum na face atlântica da serra. Comunicação pelo celular é inexistente em grande parte das trilhas.",
                    "Campina Grande do Sul está a 55 km de Curitiba pela BR-116 e serve de base para o acesso ao planalto. Antonina fica na BR-277, a cerca de 80 km de Curitiba, e é acessível de ônibus ou carro. A combinação ideal para travessias de vários dias é chegar de carro, deixar um veículo em um dos extremos e caminhar de uma cidade à outra — ou organizar o shuttle com operadoras locais.",
                ],
            },
            {
                "h2": "Melhor época para trilhar entre Campina Grande do Sul e Antonina",
                "paragraphs": [
                    "De abril a setembro, as chuvas diminuem ligeiramente e os dias com sol são mais frequentes. Mesmo nesse período, é comum haver dias de neblina e garoa, especialmente na face atlântica da serra. O frio nos cumes pode ser intenso de junho a agosto — leve casaco de pluma ou forro polar para as noites nas trilhas de vários dias.",
                    "O verão (outubro a março) concentra as maiores precipitações e torna algumas trilhas técnicas de difícil acesso. As cachoeiras ficam cheias e a floresta atinge seu ápice de exuberância. Para trilhas de baixa e média dificuldade na borda do planalto, o verão pode ser uma ótima época, desde que se evite sair nos picos de tempestade.",
                ],
            },
        ]
    },
    "chapada-dos-guimaraes": {
        "sections": [
            {
                "h2": "O coração geodésico do Brasil: Chapada dos Guimarães",
                "paragraphs": [
                    "A Chapada dos Guimarães, no Mato Grosso, ocupa um lugar geográfico e simbólico único no Brasil: é o ponto geodésico considerado o centro da América do Sul e abriga o Parque Nacional da Chapada dos Guimarães, um dos mais visitados do Centro-Oeste. O planalto de arenito vermelho, com altitude média de 800 metros acima da cidade de Cuiabá, cria uma paisagem de mesas, cânions, cachoeiras e campos de cerrado que contrasta radicalmente com o pantanal e as planícies ao redor.",
                    "A Cachoeira Véu de Noiva, com seus 86 metros de queda livre em um anfiteatro natural de rochas avermelhadas, é o cartão-postal do parque. Mas o roteiro completo da chapada inclui dezenas de outras cachoeiras, mirantes e formações rochosas: a Cidade de Pedra, o Mirante do Vale do Rio Claro, a Caverna Aroe Jari e a Lagoa Azul são apenas alguns dos destinos que fazem a chapada mato-grossense uma das mais ricas e variadas do Brasil.",
                    "A chapada também tem um papel cultural e espiritual importante: é considerada área de poder energético por diversas tradições, e a arquitetura urbana de Chapada dos Guimarães mistura igrejas coloniais do século XVIII com lojas de cristais e centros de meditação. O sincretismo é parte do charme da cidade, que atrai tanto trilheiros quanto buscadores espirituais.",
                ],
            },
            {
                "h2": "Trilhas e logística na Chapada dos Guimarães",
                "paragraphs": [
                    "A maioria das trilhas dentro do Parque Nacional da Chapada dos Guimarães é de acesso livre, mas algumas requerem agendamento pelo ICMBio. Para grupos maiores e trilhas mais remotas, o acompanhamento de guia habilitado é obrigatório. Contrate guias locais com registro no CADASTUR — eles conhecem as atualizações das condições das trilhas e os pontos fora do roteiro turístico convencional.",
                    "Chapada dos Guimarães fica a 70 km de Cuiabá e o acesso é por estrada asfaltada em boas condições. A cidade tem boa oferta de pousadas, restaurantes e agências de ecoturismo. O calor em Cuiabá é legendariamente intenso (uma das cidades mais quentes do Brasil), mas na chapada a altitude suaviza a temperatura em pelo menos 5 a 8°C.",
                    "Leve protetor solar de alto fator e muita água: o sol do cerrado mato-grossense é implacável, mesmo com nuvens. Para trilhas que cruzam os arenitos úmidos, calçado de boa aderência é fundamental — a rocha avermelhada fica extremamente escorregadia quando molhada. O período após a chuva, portanto, exige atenção redobrada nos trechos de rocha exposta.",
                ],
            },
            {
                "h2": "Melhor época para visitar a Chapada dos Guimarães",
                "paragraphs": [
                    "De maio a outubro, o período seco do Centro-Oeste, as condições são ideais: calor moderado (25 a 35°C), ausência de chuvas e cachoeiras com volume bom. O céu aberto permite vistas panorâmicas dos mirantes e facilita a longa caminhada entre atrações. É o período de maior fluxo turístico, especialmente julho.",
                    "A estação chuvosa (novembro a abril) transforma o cerrado: o verde explode em tons intensos, as cachoeiras atingem seu volume máximo e as flores do cerrado cobrem os campos. Algumas trilhas ficam temporariamente fechadas por risco de deslizamento. Visitar no início da seca (maio) oferece o melhor dos dois mundos: natureza ainda viçosa com condições de trilha melhores.",
                ],
            },
        ]
    },
    "fernando-de-noronha": {
        "sections": [
            {
                "h2": "O arquipélago mais preservado do Brasil: Fernando de Noronha",
                "paragraphs": [
                    "Fernando de Noronha, arquipélago no Oceano Atlântico a 545 km do Recife, é considerado um dos destinos de natureza mais extraordinários do Brasil e da América do Sul. Patrimônio Natural da Humanidade pela UNESCO, o arquipélago tem trilhas costeiras únicas: caminhos de terra entre falésias, praias desertas e mirantes sobre o oceano que revelam um azul de tirar o fôlego em todas as direções.",
                    "As trilhas em Noronha percorrem principalmente a parte terrestre da Área de Proteção Ambiental (APA), que compreende a maior parte da ilha principal. O Pico, ponto mais alto do arquipélago com 323 metros, oferece uma vista de 360 graus sobre todas as ilhotas, praias e o imenso azul do Atlântico. A Enseada do Sueste, o Boldró e o Leão são outros mirantes acessíveis por trilhas relativamente curtas que recompensam com paisagens incomparáveis.",
                    "A fauna terrestre e marinha de Noronha é uma das grandes atrações: golfinhos-rotadores chegam às dezenas de milhares na Baía dos Golfinhos ao amanhecer, tartarugas marinhas desovam nas praias de setembro a março, e polvos, arraias e tubarões-limão podem ser observados em snorkeling. As trilhas costeiras frequentemente terminam em praias onde é possível nadar com animais selvagens.",
                ],
            },
            {
                "h2": "Logística para visitar Fernando de Noronha",
                "paragraphs": [
                    "O acesso a Fernando de Noronha é exclusivamente por avião, com voos a partir de Recife e Natal. O número de visitantes diários é limitado pelo governo e todos os turistas pagam a Taxa de Preservação Ambiental (TPA), calculada por dia de permanência e que aumenta a partir do quarto dia na ilha. Isso torna Noronha um destino relativamente caro, mas o investimento justifica-se pela experiência única.",
                    "Na ilha, o deslocamento é feito a pé, de buggy, moto ou táxi. Aluguel de buggy é a opção mais popular e prática para acessar as praias e trilhas mais remotas. Algumas trilhas dentro do Parque Nacional (que cobre cerca de 70% da ilha principal) exigem acompanhamento de guia habilitado — verifique as exigências de cada percurso antes de partir.",
                    "A acomodação vai de pousadas simples a resorts, mas os preços são significativamente mais altos do que no continente. Reserve com muita antecedência, especialmente para os meses de pico (julho, dezembro e janeiro). A gastronomia da ilha é limitada mas tem boas opções de frutos do mar frescos — o lagostim e o atum grelhado são especialidades locais.",
                ],
            },
            {
                "h2": "Melhor época para visitar Fernando de Noronha",
                "paragraphs": [
                    "De agosto a janeiro, a estação seca de Noronha oferece as melhores condições para mergulho e snorkeling: visibilidade subaquática pode ultrapassar 50 metros, os ventos são moderados e as praias ficam com ondas mais calmas. É também o período de reprodução das tartarugas, com desovas que podem ser observadas à noite com guia autorizado.",
                    "De fevereiro a julho, a estação chuvosa traz mar mais agitado e menor visibilidade para atividades náuticas. As trilhas terrestres, no entanto, ficam mais verdes e o calor é ligeiramente mais suave. Os preços caem consideravelmente nesse período e a ilha recebe menos visitantes — uma vantagem para quem quer experiências mais tranquilas nas trilhas e praias.",
                ],
            },
        ]
    },
    "imbituba": {
        "sections": [
            {
                "h2": "Baleias e trilhas costeiras: Imbituba e o litoral sul catarinense",
                "paragraphs": [
                    "Imbituba, no litoral sul de Santa Catarina, é reconhecida como a capital nacional da observação de baleias-francas. Entre julho e novembro, as fêmeas da baleia-franca-austral chegam às baías abrigadas da costa catarinense para parir e amamentar seus filhotes — e Imbituba, com sua baía em formato de anfiteatro natural, é um dos melhores pontos do mundo para observar esse fenômeno a partir de terra firme, sem precisar embarcar em barco.",
                    "As trilhas litorâneas de Imbituba percorrem costões rochosos, dunas fixas cobertas de vegetação de restinga e mirantes naturais sobre a baía onde as baleias aparecem. A Praia do Rosa, enclave de luxo e surfe de classe mundial dentro do município, tem trilhas que contornam os morros da orla oferecendo vistas para ambos os lados da costa. O Parque Estadual da Serra do Tabuleiro, que toca os limites do município, adiciona mais opções de trilha em ambiente de mata atlântica.",
                    "Imbituba tem também um porto industrial ativo e uma história ligada à mineração de carvão, o que cria uma combinação interessante de natureza preservada e identidade industrial que distingue a cidade dos balneários puramente turísticos do litoral catarinense. A Lagoa de Ibiraquera, parcialmente dentro do município, é destino de kitesurf e windsurf e adiciona mais uma dimensão de aventura à região.",
                ],
            },
            {
                "h2": "Dicas para trilhar e observar baleias em Imbituba",
                "paragraphs": [
                    "A observação de baleias-francas em Imbituba é gratuita a partir de pontos terrestres como o Patacho, o Morro do Mirim e a Praia da Vila. Binoculares aumentam muito a experiência. No período de pico (agosto e setembro), é comum ver várias baleias simultaneamente com filhotes nadando ao lado — um espetáculo que não exige equipamento especial nem aptidão física.",
                    "Para as trilhas da região, tênis de caminhada ou sandálias de trilha são suficientes na maioria dos percursos. O litoral catarinense tem variações climáticas bruscas — um dia ensolarado pode virar nublado e frio em poucas horas, especialmente no inverno quando as baleias estão presentes. Leve corta-vento e protetor solar independentemente da estação.",
                    "Imbituba está a 90 km de Florianópolis pela BR-101. A cidade tem opções de acomodação para todos os orçamentos, com concentração de pousadas nas praias. Os restaurantes da região servem frutos do mar frescos, especialmente no período de verão. No inverno das baleias, o turismo é mais calmo e os preços mais acessíveis do que no verão catarinense.",
                ],
            },
            {
                "h2": "Melhor época para visitar Imbituba",
                "paragraphs": [
                    "Julho a novembro é a temporada das baleias — e o principal atrativo de Imbituba para turistas de natureza. O inverno catarinense pode ser frio (10 a 18°C) e com vento, mas as baleias compensam qualquer desconforto climático. Setembro é geralmente o mês com maior concentração de animais na baía.",
                    "O verão (dezembro a fevereiro) é a alta temporada das praias: calor (25 a 32°C), mar agradável e movimento intenso. As trilhas costeiras são mais aprazíveis com o calor, mas o fluxo de turistas nas praias mais conhecidas é grande. Março e abril oferecem um equilíbrio — mar ainda quente, menos gente e início das preparações para a temporada das baleias.",
                ],
            },
        ]
    },
    "itatiaia": {
        "sections": [
            {
                "h2": "O parque mais antigo do Brasil: trilhas em Itatiaia",
                "paragraphs": [
                    "O Parque Nacional do Itatiaia, criado em 1937 como o primeiro parque nacional do Brasil, é uma das áreas protegidas mais importantes da Mata Atlântica e um destino clássico para trilheiros de todo o país. Localizado na divisa entre Rio de Janeiro e Minas Gerais, na Serra da Mantiqueira, o parque abriga o Pico das Agulhas Negras (2.791 m) e o Pico do Itatiaia (2.787 m) — dois dos pontos mais altos da região Sudeste.",
                    "O parque é dividido em duas partes distintas com características muito diferentes. A parte baixa, com entrada pelo município de Itatiaia (RJ), tem trilhas em meio à floresta densa de Mata Atlântica, cachoeiras como a Véu de Noiva e o Poranga, lagos e a sede do parque onde está o Museu de História Natural. A parte alta, acessada pela estrada que sobe até 2.200 metros, revela os campos de altitude, as chamadas agulhas de rocha e os abrigos montanhosos que servem de base para a subida aos picos.",
                    "A biodiversidade do Itatiaia é excepcional: são registradas mais de 500 espécies de aves, incluindo o beija-flor-de-barriga-azul endêmico, e a flora dos campos de altitude inclui canelas-de-ema, bromélias e orquídeas que florescem apenas no ambiente de altitude. O parque é considerado um dos melhores destinos de observação de aves do Sudeste brasileiro.",
                ],
            },
            {
                "h2": "Trilhas e como se preparar para o Itatiaia",
                "paragraphs": [
                    "A subida ao Pico das Agulhas Negras é a trilha mais famosa do parque: parte do abrigo Rebouças (2.350 m) e sobe por 2,5 km até o cume a 2.791 m. O percurso exige experiência em trilha de altitude, equipamento adequado para frio e vento intenso, e geralmente é realizado em uma noite de acampamento no abrigo. A entrada no trecho de cume é permitida somente com guia habilitado.",
                    "Para a parte baixa do parque, trilhas como o Caminho das Mariposas, a trilha do Lago Azul e o percurso até a Cachoeira Poranga são acessíveis para iniciantes e famílias. O calçado deve ter boa aderência e o terreno pode estar úmido mesmo em dias sem chuva, dada a umidade constante da Mata Atlântica. Repelente de insetos é recomendado.",
                    "Itatiaia (RJ) está a cerca de 165 km do Rio de Janeiro pela BR-354 e 280 km de São Paulo pela Dutra. A região tem boa infraestrutura de pousadas e hotéis, especialmente em Itatiaia e na vizinha Penedo. O Abrigo Rebouças, dentro do parque na parte alta, oferece acomodação básica com reserva antecipada — indispensável para quem planeja a subida ao cume.",
                ],
            },
            {
                "h2": "Melhor época para trilhar no Itatiaia",
                "paragraphs": [
                    "De abril a setembro, a estação seca do Sudeste, é o melhor período para trilhas na parte alta do parque. O frio é intenso no inverno (podendo chegar a -5°C no cume), mas o céu limpo compensa e a visibilidade nos mirantes é máxima. Leve agasalhos em camadas, capa de chuva e saco de dormir adequado para temperatura negativa se for acampar.",
                    "De outubro a março, as chuvas de verão podem afetar as trilhas da parte alta, tornando o terreno escorregadio e perigoso. A parte baixa do parque fica exuberante com o verde da mata após as chuvas, e as cachoeiras atingem seu volume máximo. Para trilhas na floresta, o verão chuvoso é muito agradável — basta evitar os horários de tempestade típicos da tarde.",
                    "A alta temporada do Itatiaia coincide com julho e o carnaval: o parque recebe um fluxo enorme de visitantes e o limite diário de entrada pode ser atingido. Chegue cedo ou visite nos dias de semana para evitar filas e ter mais sossego nas trilhas. Nos fins de semana de feriado prolongado, o agendamento prévio pelo site do ICMBio é indispensável.",
                ],
            },
        ]
    },
    "palmeiras": {
        "sections": [
            {
                "h2": "Palmeiras e o coração da Chapada Diamantina",
                "paragraphs": [
                    "Palmeiras, pequena cidade no centro geográfico da Bahia, é um dos núcleos históricos da Chapada Diamantina e ponto de convergência de diversas trilhas clássicas da região. O Morro do Pai Inácio — um paredão tabular de 1.120 metros de altitude que domina a paisagem local — é talvez a imagem mais icônica de toda a chapada: ao pôr do sol, sua sombra projetada sobre o vale dos Lençóis cria um espetáculo que trilheiros e fotógrafos perseguem ano após ano.",
                    "O acesso ao topo do Morro do Pai Inácio é feito por uma trilha de 45 minutos de moderada dificuldade, com trechos de rocha e exposição ao sol. No cume, a vista panorâmica revela o mosaico de cerrado, campo rupestre e matas ciliares que compõe a paisagem da chapada. É possível ver o Vale do Capão, a Serra do Sincorá ao fundo e, em dias claros, as cidades de Lençóis e Palmeiras lá embaixo.",
                    "Além do Pai Inácio, Palmeiras está próxima das cachoeiras do Mixilá, da Serrano e do Buracão — esta última uma espetacular garganta por onde o Rio Andaraí mergulha em uma fenda de rocha. A trilha ao Buracão passa por mata ciliar e campo rupestre e termina em um anfiteatro geológico único que exige bom preparo físico para ser explorado completamente.",
                ],
            },
            {
                "h2": "Dicas para trilhar em Palmeiras e arredores",
                "paragraphs": [
                    "O acesso ao Morro do Pai Inácio está dentro do Parque Nacional da Chapada Diamantina e exige pagamento de taxa de entrada. Trilhas mais longas e remotas da região requerem guia habilitado — contrate sempre um guia registrado no CADASTUR para garantir sua segurança e cumprir as regras do parque. Os guias de Palmeiras e Lençóis são reconhecidos pela qualidade do conhecimento local.",
                    "Palmeiras está a cerca de 15 km de Lençóis pela BA-850, uma estrada com trechos não pavimentados que pode ficar intransitável após chuvas fortes. De ônibus, acesse por Feira de Santana ou Salvador. A cidade tem pousadas simples e aconchegantes, e o convívio com a comunidade local — que mantém viva a cultura garimpeira e a gastronomia baiana do interior — é parte da experiência.",
                    "A hidratação é crucial nas trilhas da chapada: o sol é intenso e o vento do nordeste resseca rapidamente a garganta. Leve ao menos 2 litros de água por pessoa para qualquer saída. O calçado deve ter boa aderência pois as trilhas frequentemente cruzam lajes de rocha quartzítica que podem estar úmidas mesmo fora da época de chuvas.",
                ],
            },
            {
                "h2": "Quando visitar Palmeiras e a Chapada Diamantina",
                "paragraphs": [
                    "De junho a novembro, o inverno baiano oferece as melhores condições para trilhar: calor suave (22 a 32°C), baixa umidade, céu sem nuvens e cachoeiras com volume razoável. Os campos rupestres ficam floridos em julho e agosto, com uma profusão de sempre-vivas, cactos em flor e orquídeas que torna a caminhada ainda mais especial.",
                    "De dezembro a maio, as chuvas são mais frequentes e intensas. O verde da chapada fica mais vibrante, as cachoeiras enchem e a vegetação esconde alguns percursos de rocha. Algumas trilhas ficam interditadas por segurança. O início de junho, logo após as chuvas, é uma excelente janela: natureza ainda viçosa com condições já favoráveis para caminhar.",
                ],
            },
        ]
    },
    "paracuru": {
        "sections": [
            {
                "h2": "Vento, mar e dunas: aventura em Paracuru, Ceará",
                "paragraphs": [
                    "Paracuru, no litoral oeste do Ceará, é um destino que combina praias selvagens, dunas móveis, lagoas de água doce e o vento constante do nordeste que a tornou um dos melhores pontos de kitesurf e windsurf do Brasil. As trilhas da região acompanham a orla entre praias desertas e dunas em movimento, criando percursos que mudam de forma a cada estação à medida que o vento remodela a paisagem de areia.",
                    "A Praia de Paracuru, a Praia do Pecém e a Praia do Coqueiro formam um circuito costeiro que pode ser percorrido a pé entre o amanhecer e o anoitecer em dias de maré baixa. A caminhada pelas dunas é tecnicamente simples mas fisicamente exigente: areia fofa, sol intenso e distâncias enganosas que parecem menores do que são. As lagoas interdunas, formadas pelas chuvas de março a maio, são oásis frescos perfeitos para uma pausa no meio do percurso.",
                    "Paracuru é também reconhecida como destino de surf: as ondas formadas na ponta da cidade atraem surfistas de todo o Brasil, e os ventos do nordeste que sopram consistentemente de agosto a janeiro criam condições perfeitas para esportes de vela. Quem gosta de combinar caminhada com esportes de aventura encontra em Paracuru um cardápio completo.",
                ],
            },
            {
                "h2": "Como aproveitar Paracuru com segurança",
                "paragraphs": [
                    "As caminhadas pelas dunas de Paracuru exigem proteção solar intensa: protetor FPS 70 ou mais, chapéu de abas largas, camiseta com manga longa e óculos de sol com proteção UV são itens básicos. O reflexo da areia amplifica a radiação solar e queimaduras podem ocorrer mesmo em dias com neblina leve. Leve bastante água — as caminhadas pelas dunas não têm fontes de abastecimento.",
                    "Para os percursos mais longos pela orla, verifique a tábua de marés: trechos de praia que ficam sob água na maré alta são transitáveis apenas na maré baixa. Os buggueiros locais conhecem os melhores horários e podem servir de transporte de retorno quando a caminhada é unidirecional. Calcule bem o tempo de volta para não ser pego pela maré.",
                    "Paracuru está a 80 km de Fortaleza pela CE-085. O acesso é fácil de carro ou de ônibus a partir da capital cearense. A cidade tem pousadas simples e restaurantes com frutos do mar frescos — a lagosta e o camarão locais são famosos pela qualidade. O custo de vida é bem mais baixo do que em outros destinos litorâneos do nordeste.",
                ],
            },
            {
                "h2": "Melhor época para visitar Paracuru",
                "paragraphs": [
                    "O período de agosto a janeiro é o chamado 'nordeste' do Ceará: ventos constantes de 25 a 40 km/h que criam condições perfeitas para kitesurf, windsurf e passeios de barco à vela. As dunas ficam modeladas pelo vento em formas geométricas perfeitas e as lagoas interdunas já estão secando mas ainda têm água na maioria dos pontos.",
                    "De fevereiro a julho, o inverno cearense (paradoxalmente chamado de inverno, embora não seja frio) traz as chuvas que enchem as lagoas e transformam o verde dos coqueirais. A paisagem fica mais úmida e colorida, o mar pode ficar mais agitado e os ventos mais irregulares. Para caminhadas tranquilas na praia, esse período costuma ter madrugadas e manhãs com temperatura agradável antes do calor da tarde.",
                ],
            },
        ]
    },
    "passa-quatro-itamonte": {
        "sections": [
            {
                "h2": "Serra da Mantiqueira: trilhas entre Passa Quatro e Itamonte",
                "paragraphs": [
                    "Passa Quatro e Itamonte, no sul de Minas Gerais, são duas cidades irmãs encravadas na Serra da Mantiqueira que oferecem acesso a alguns dos terrenos de montanha mais desafiadores e recompensadores do Sudeste brasileiro. A região inclui o Parque Nacional do Itatiaia pelo lado mineiro e a APA da Serra da Mantiqueira, com picos acima dos 2.700 metros e campos de altitude cobertos de vegetação rupestre.",
                    "O Pico das Agulhas Negras (2.791 m) pode ser acessado tanto pelo lado fluminense (Itatiaia/RJ) quanto pelo lado mineiro, partindo de Itamonte. A rota mineira é menos conhecida mas oferece uma perspectiva diferente do maciço e, em alguns trechos, é mais íngreme e menos movimentada. Para alpinistas experientes, o acesso pela face sul do pico é um clássico da montanha capixaba.",
                    "Além das rotas ao Agulhas Negras, a região de Passa Quatro tem trilhas em mata ciliar ao longo do Rio Sapucaí e percursos nos arredores da Serra dos Aiuruocas. A cidade vizinha de Visconde de Mauá, a poucos quilômetros, complementa o roteiro com suas cachoeiras e o charme de um vilarejo de montanha com culinária suíça trazida pelos colonizadores europeus do século XX.",
                ],
            },
            {
                "h2": "Preparação e logística para trilhar em Passa Quatro e Itamonte",
                "paragraphs": [
                    "Para as trilhas de alta altitude da região, prepare-se para frio intenso: no inverno (junho a agosto), a temperatura pode cair abaixo de zero nos picos e a ocorrência de geada é comum nos campos de altitude. Leve agasalhos de forro polar, capa de chuva impermeável e calça de montanha. O aquecimento em camadas é a estratégia mais eficiente.",
                    "A subida ao Pico das Agulhas Negras pelo lado mineiro requer experiência em montanha e, nos últimos trechos técnicos, capacidade de progressão em rocha. Guia com formação em montanhismo é altamente recomendado para quem não tem experiência prévia. Contrate sempre guias registrados no CADASTUR e que conheçam especificamente a rota mineira do Agulhas Negras.",
                    "Passa Quatro está a 280 km de São Paulo e 310 km do Rio de Janeiro, com bom acesso pelas rodovias Presidente Dutra (BR-116) e conexões locais. A cidade tem pousadas de qualidade e restaurantes com culinária mineira — queijo, pão de queijo e feijão tropeiro são a base do alimento após um dia intenso de trilha. Em Itamonte, a infraestrutura é mais simples mas o ambiente é mais próximo da natureza.",
                ],
            },
            {
                "h2": "Melhor época para trilhar na região de Passa Quatro",
                "paragraphs": [
                    "De abril a setembro, o tempo seco favorece as trilhas de altitude. O frio do inverno mineiro pode ser rigoroso, mas o céu limpo garante vistas inesquecíveis nos cumes. Julho concentra o maior fluxo de visitantes — para um ambiente mais tranquilo, prefira abril, maio ou setembro, quando as condições são igualmente boas.",
                    "O verão (outubro a março) traz chuvas frequentes à tarde que tornam os terrenos de alta altitude escorregadios e perigosos. Trilhas na mata mais baixa, porém, ficam mais bonitas com o verde intenso da Mata Atlântica após as chuvas. Para iniciantes, o período de transição entre a seca e a chuva (março/abril e setembro/outubro) oferece condições agradáveis para trilhas de baixa e média dificuldade.",
                ],
            },
        ]
    },
    "petropolis-teresopolis": {
        "sections": [
            {
                "h2": "A Travessia Clássica: Petrópolis a Teresópolis pela Serra dos Órgãos",
                "paragraphs": [
                    "A Travessia Petrópolis-Teresópolis é o grande clássico do trekking de vários dias no Brasil: 42 quilômetros que cruzam o Parque Nacional da Serra dos Órgãos de ponta a ponta, em três dias de caminhada por um dos trechos mais preservados de Mata Atlântica da Serra do Mar fluminense. O percurso passa por cristas, picos rochosos, campos de altitude e matas densas que oferecem uma imersão completa na biodiversidade da Mata Atlântica.",
                    "Petrópolis, a cidade imperial às portas da Serra dos Órgãos, serve de ponto de partida para a travessia. A rota sobe da encosta atlântica até as cristas do parque, passando pelo Posto Soberbo (onde está o mirante mais famoso do parque, com vista para o maciço que inclui o Dedo de Deus) antes de mergulhar nos campos de altitude e picos rochosos que marcam o coração do parque.",
                    "A Serra dos Órgãos abriga uma das maiores diversidades de orquídeas do mundo e é considerada área prioritária para a conservação da Mata Atlântica. Durante a travessia, é comum avistar tucanos, papagaios, arapongas e, com sorte, o raro Gavião-pato ou o Muriqui — o maior primata das Américas, que ainda sobrevive nas matas serranas do Rio de Janeiro.",
                ],
            },
            {
                "h2": "Como planejar a Travessia Petrópolis-Teresópolis",
                "paragraphs": [
                    "A travessia é realizada de norte a sul (Petrópolis → Teresópolis) ou de sul a norte. O sentido mais comum é de Teresópolis para Petrópolis, com pernoites nos abrigos do Açu e Pedra do Sino. É obrigatório fazer o trajeto com guia habilitado e registrar a entrada no ICMBio. O número máximo de pessoas por grupo é limitado para proteger o ecossistema.",
                    "O equipamento para a travessia inclui mochila de 60 a 80 litros, saco de dormir adequado para temperaturas entre 5°C e 15°C, roupa impermeável, bota de trilha cano alto e comida para três dias. Os abrigos do parque fornecem dormitório básico e pontos de água, mas não há venda de alimentos dentro do parque. Leve ração de montanha ou alimentos leves e calóricos.",
                    "Petrópolis está a 65 km do Rio de Janeiro pela BR-040. Teresópolis fica a 90 km do Rio pela BR-116 (Via Dutra). O transporte entre as duas cidades para deixar veículo ou fazer o retorno pode ser organizado com operadoras de turismo ou de forma independente pelos motoristas locais.",
                ],
            },
            {
                "h2": "Melhor época para a Travessia Petrópolis-Teresópolis",
                "paragraphs": [
                    "De maio a setembro, o clima seco e ameno da Serra dos Órgãos cria as melhores condições para a travessia: trilha firme, visibilidade nos picos e temperaturas agradáveis para caminhar. O frio noturno nos abrigos pode chegar a 5°C ou menos — saco de dormir adequado é indispensável. Os dias mais longos de sol permitem mais horas de caminhada produtiva.",
                    "O verão (novembro a março) traz chuvas diárias que tornam os caminhos enlameados e reduzem a visibilidade nas cristas. Apesar disso, a mata em seu ápice verde é deslumbrante. A travessia é tecnicamente possível no verão, mas exige mais experiência e equipamento robusto para chuva. O ICMBio pode restringir o acesso a certos trechos após eventos de chuva intensa.",
                ],
            },
        ]
    },
    "praia-grande": {
        "sections": [
            {
                "h2": "Cânion Malacara e os abismos de Praia Grande, Santa Catarina",
                "paragraphs": [
                    "Praia Grande, no extremo sul de Santa Catarina, é o ponto de acesso ao Cânion Malacara — uma das formações geológicas mais impressionantes do Sul do Brasil. Com paredes de arenito que caem abruptamente mais de 500 metros, o Malacara é parte do complexo de cânions da Serra Geral que inclui os famosos Itaimbezinho (em Cambará do Sul) e Fortaleza. A perspectiva de baixo, acessível por trilhas que descem ao vale do Rio Mampituba, é radicalmente diferente — e igualmente impactante — à visão de cima.",
                    "A Trilha do Malacara, com seus 14 km de percurso que desce ao fundo do vale e sobe novamente para o mirante superior, é a principal aventura de Praia Grande. A descida envolve trechos com corda fixada em rocha e atravessias de rio — tornando o percurso técnico o suficiente para ser feito somente com guia habilitado. A recompensa é uma perspectiva rara das paredes do cânion que, de baixo, parecem tocar as nuvens.",
                    "Praia Grande também oferece acesso ao Parque Nacional da Serra Geral pelo lado catarinense, com trilhas que alcançam os campos de altitude da borda do planalto. Os campos de araucárias, espécie símbolo do Sul do Brasil, cobrem o topo da serra e criam uma paisagem completamente diferente do que se vê nos vales abaixo. O contraste entre o topo e o fundo dos cânions é parte da magia da região.",
                ],
            },
            {
                "h2": "Logística e preparação para os cânions de Praia Grande",
                "paragraphs": [
                    "A Trilha do Malacara exige boa condição física e experiência mínima em trilhas de dificuldade moderada a alta. Os trechos com corda e a travessia do rio com pedras escorregadias tornam o uso de bota de cano alto com sola de borracha boa essencial — tênis de corrida não são adequados para esse terreno. Leve roupa que possa molhar e troque de calçado na travessia ou use sandália de neoprene.",
                    "A trilha ao Malacara pode durar de 6 a 8 horas de caminhada efetiva. Leve ao menos 3 litros de água por pessoa, alimentos energéticos para o dia todo e protetor solar. O vale do Malacara é mais protegido do vento mas pode ficar muito quente ao meio-dia no verão — planeje a saída para as primeiras horas da manhã.",
                    "Praia Grande está a 310 km de Florianópolis pela BR-101 Sul e a 200 km de Porto Alegre. A cidade é pequena e a infraestrutura turística é modesta — há pousadas simples e restaurantes com culinária do Sul. As agências locais de ecoturismo organizam o transporte até a trilha e fornecem guias habilitados. Contrate sempre com antecedência nos fins de semana de alta temporada.",
                ],
            },
            {
                "h2": "Melhor época para visitar os cânions de Praia Grande",
                "paragraphs": [
                    "Outubro a abril é o período com temperaturas mais amenas para a caminhada e o vale. O verão (dezembro a fevereiro) traz mais calor e a possibilidade de tomar banho nas piscinas naturais do Rio Mampituba no fundo do cânion — um bônus que torna a trilha ainda mais agradável. O fluxo de visitantes é maior nesse período.",
                    "No inverno (junho a agosto), o frio sul-catarinense pode ser rigoroso — geadas e até neve rara nos campos de cima da serra. A Trilha do Malacara é mais fria no fundo do vale e o rio pode estar mais volumoso, tornando as travessias mais desafiadoras. Para trilhas nos campos de altitude, o inverno tem a beleza das paisagens cobertas de geada ao amanhecer.",
                ],
            },
        ]
    },
    "sao-bento-do-sapucai": {
        "sections": [
            {
                "h2": "Pedra do Baú e a Mantiqueira paulista: São Bento do Sapucaí",
                "paragraphs": [
                    "São Bento do Sapucaí, no Vale do Paraíba paulista, é um dos principais destinos de montanhismo e trekking do estado de São Paulo. A cidade é dominada pela silhueta inconfundível da Pedra do Baú — um batólito granítico que se eleva 1.950 metros sobre o nível do mar e 900 metros acima do vale, visível de dezenas de quilômetros de distância. A subida ao cume da Pedra do Baú é considerada uma das trilhas mais icônicas do Estado de São Paulo.",
                    "O percurso até o cume da Pedra do Baú tem cerca de 8 km de ida e volta com desnível de 900 metros. No terço final da subida, a trilha transforma-se em escalada classe III em rocha exposta, onde são utilizadas correntes e escadas fixadas na parede de granito para facilitar a progressão. Do cume, a vista abrange o Vale do Paraíba, as cidades de São José dos Campos e Taubaté ao fundo e, em dias claros, a Serra dos Órgãos no Rio de Janeiro.",
                    "Além da Pedra do Baú, São Bento do Sapucaí tem outros atrativos para trilheiros: a Pedra do Bauzinho (pico adjacente, com rota alternativa de escalada), a Cachoeira do Pachecos, a Trilha do Monjolo e os mirantes naturais que pontuam a estrada de acesso ao vale. A cidade tem também uma produção artesanal de queijos e doces da Mantiqueira que encanta os visitantes.",
                ],
            },
            {
                "h2": "Como se preparar para a Pedra do Baú",
                "paragraphs": [
                    "A subida à Pedra do Baú é classificada como moderada a difícil pela presença dos trechos com correntes e escadas. Não é tecnicamente escalada com equipamentos, mas exige controle de altura e boa condição física. Pessoas com acrofobia (medo de altura) podem sentir desconforto nos trechos expostos — avalie honestamente suas limitações antes de partir. Crianças acima de 10 anos geralmente conseguem completar o percurso com acompanhamento adulto.",
                    "A trilha começa em propriedade privada e a entrada é paga mediante cadastro dos visitantes. Guias locais conhecem os melhores horários para subir (evitando o sol forte do meio-dia e chegando ao cume para o fim de tarde), as condições atuais da trilha e os pontos de fotografia mais impactantes. A subida com guia é altamente recomendada para quem não conhece o percurso.",
                    "São Bento do Sapucaí está a 180 km de São Paulo e 250 km do Rio de Janeiro, com acesso pela SP-171 (Rodovia Pedro Eroles). A cidade tem pousadas de charme e restaurantes com boa culinária da Mantiqueira. O Circuito das Frutas da região e as feiras de artesanato complementam o roteiro para quem deseja combinar natureza e cultura.",
                ],
            },
            {
                "h2": "Melhor época para visitar São Bento do Sapucaí",
                "paragraphs": [
                    "De abril a setembro, o período seco do Vale do Paraíba, as trilhas estão em melhores condições: terreno firme, visibilidade máxima no cume e temperatura agradável para caminhar (15 a 25°C). O inverno paulista pode ser frio à noite (próximo de 10°C), mas os dias são ensolarados e a vista do cume fica nítida sem névoa.",
                    "O verão (outubro a março) traz chuvas frequentes que podem tornar os trechos de rocha da Pedra do Baú escorregadios e perigosos. A trilha pode ser fechada em dias de chuva forte por razões de segurança. A vegetação da Mantiqueira fica exuberante e as cachoeiras da região atingem seu volume máximo — ótima época para trilhas mais baixas ao redor da cidade.",
                    "São Bento do Sapucaí recebe mais visitantes nos fins de semana de outubro a fevereiro (primavera e verão), quando o clima agradável de montanha atrai moradores de São Paulo e do Vale do Paraíba. Para uma experiência mais tranquila na Pedra do Baú, prefira os finais de semana do período seco e evite os feriados prolongados.",
                ],
            },
        ]
    },
    "teresopolis": {
        "sections": [
            {
                "h2": "Serra dos Órgãos: o playground de montanha do Rio de Janeiro",
                "paragraphs": [
                    "Teresópolis, a 90 km do Rio de Janeiro, é a porta de entrada para o Parque Nacional da Serra dos Órgãos pelo lado norte — e uma das melhores bases para montanhismo e trekking do Sudeste brasileiro. A Serra dos Órgãos deve seu nome ao conjunto de picos rochosos que, vistos de longe, lembram os tubos de um órgão musical: Dedo de Deus (1.692 m), Pedra do Sino (2.263 m), Agulha do Diabo e dezenas de outras formações que desafiam alpinistas de todos os níveis.",
                    "O Dedo de Deus é o símbolo mais reconhecível do parque: um dedo de granito que se projeta do topo da serra e pode ser visto da Rodovia Teresópolis-Friburgo. A trilha ao sopé do Dedo de Deus (sem escalar a formação em si, que exige alpinismo técnico) tem 8 km de ida e volta com desnível de 700 metros e passa por trechos de floresta atlântica densa com bromélias e orquídeas em todos os ramos.",
                    "Para os montanhistas, a Serra dos Órgãos é um clássico absoluto: a Pedra do Sino (2.263 m), o ponto mais alto do parque, tem uma trilha de 14 km com desnível acumulado de 1.800 metros — a mais longa e desafiadora trilha de dia inteiro do parque. A vista do cume abrange toda a Serra do Mar, o litoral fluminense e, em dias de excepcional visibilidade, o Rio de Janeiro e o Pão de Açúcar lá embaixo.",
                ],
            },
            {
                "h2": "Como trilhar no Parque Nacional da Serra dos Órgãos",
                "paragraphs": [
                    "O Parque Nacional da Serra dos Órgãos tem entrada pela sede em Teresópolis e pela sub-sede de Petrópolis. As trilhas de curta e média distância (Trilha do Suspiro, Trilha da Pedreira, Trilha do Retiro) são acessíveis para iniciantes e não exigem guia. Para trilhas longas como a Pedra do Sino e a Travessia Petrópolis-Teresópolis, o guia habilitado é obrigatório pelo ICMBio.",
                    "O equipamento essencial para Teresópolis inclui bota de trilha cano médio ou alto, capa de chuva (a neblina aparece rapidamente na serra), agasalho para o final da tarde e repelente de insetos. A umidade da Mata Atlântica é alta e o terreno pode estar molhado mesmo sem chuva recente. Leve sempre mais água do que pensa precisar.",
                    "Teresópolis tem boa infraestrutura de pousadas e restaurantes. A cidade é conhecida pela qualidade dos produtos orgânicos da região serrana — hortaliças, cogumelos e laticínios que abastecem mercados do Rio de Janeiro. A Feira do Nogueira, realizada aos domingos, é uma experiência gastronômica e cultural que complementa perfeitamente um fim de semana de trilha.",
                ],
            },
            {
                "h2": "Melhor época para trilhar em Teresópolis",
                "paragraphs": [
                    "De maio a setembro, o período seco, as trilhas estão em melhores condições: menos lama, maior visibilidade nos picos e temperatura agradável (10 a 22°C). O frio de julho e agosto pode surpreender quem não está acostumado com altitude — leve agasalhos mesmo que a previsão do Rio de Janeiro pareça amena. A Serra dos Órgãos cria seu próprio microclima.",
                    "O verão (outubro a março) concentra as chuvas e pode fechar trilhas temporariamente por risco de deslizamento. A beleza da mata atlântica depois da chuva e as cachoeiras cheias compensam as dificuldades. Para trilhas de baixa dificuldade no interior da floresta, o verão é agradável — basta evitar as horas de tempestade da tarde e checar as condições com o ICMBio antes de partir.",
                    "Teresópolis recebe fluxo intenso nos fins de semana de julho e nos feriados, quando famílias do Rio de Janeiro sobem em busca do frescor da serra. Para quem busca trilhas com mais tranquilidade, os dias úteis de qualquer época do ano são a melhor opção. O parque abre às 8h e a maioria das trilhas deve ser iniciada até as 10h para garantir o retorno antes do escurecer.",
                ],
            },
        ]
    },
    "uiramuta": {
        "sections": [
            {
                "h2": "Monte Roraima: o topo do mundo a partir de Uiramutã",
                "paragraphs": [
                    "Uiramutã, no extremo norte de Roraima, é o município brasileiro mais próximo do Monte Roraima — o tepui de 2.810 metros que marca o ponto tríplice entre Brasil, Venezuela e Guiana. O Roraima é uma das formações geológicas mais antigas e espetaculares do planeta: seu platô de arenito negro, sempre envolto em nuvens, abriga ecossistemas únicos com plantas endêmicas que não existem em nenhum outro lugar da Terra.",
                    "A trilha ao Monte Roraima parte da Venezuela (lado mais acessível) ou do Brasil, passando pela Terra Indígena Raposa Serra do Sol. A rota brasileira é mais selvagem, menos infraestruturada e exige autorização especial para transitar pela terra indígena — uma aventura que preserva o espírito exploratório que a montanha inspirou em escritores como Arthur Conan Doyle, que a imortalizou como inspiração para 'O Mundo Perdido'.",
                    "O platô do Roraima é um mundo à parte: sem vegetação arbórea, coberto de plantas carnívoras, cristais de quartzo e formações rochosas esculpidas pela chuva e pelo vento ao longo de bilhões de anos. A Janela (uma formação que emoldura a paisagem da Venezuela) e a Jacuzzi Natural são os pontos mais fotografados. Caminhar pelo platô é uma experiência de outra dimensão — literalmente acima das nuvens durante parte da travessia.",
                ],
            },
            {
                "h2": "Como se preparar para o Monte Roraima",
                "paragraphs": [
                    "A expedição ao Roraima pelo lado brasileiro é uma das mais complexas e exigentes do Brasil: exige autorização da FUNAI para a terra indígena Raposa Serra do Sol, guia indígena Pemón credenciado, equipamento de acampamento de alta qualidade e condição física de atleta. O percurso total varia de 8 a 12 dias dependendo da rota e do tempo no platô.",
                    "O equipamento essencial inclui tenda resistente ao vento e à chuva, saco de dormir quente (a temperatura no platô pode cair abaixo de 10°C à noite), botas impermeáveis de cano alto, bastões de caminhada e roupas em camadas. A chuva é uma certeza no Roraima — o tepui cria seu próprio sistema meteorológico e chove em praticamente todos os dias. Roupas impermeáveis de qualidade profissional são indispensáveis.",
                    "O acesso a Uiramutã é por estrada não pavimentada a partir de Boa Vista, capital de Roraima, em percurso de 5 a 6 horas de 4x4. A maioria das expedições parte de Boa Vista, onde há operadoras especializadas. A logística é complexa e o planejamento deve começar com pelo menos 3 meses de antecedência, especialmente para garantir as autorizações necessárias.",
                ],
            },
            {
                "h2": "Melhor época para o Monte Roraima",
                "paragraphs": [
                    "De janeiro a maio, durante a estação menos chuvosa de Roraima (o 'verão' local), as condições de caminhada são ligeiramente melhores — os rios no percurso estão mais baixos e transitáveis, as trilhas menos enlameadas e os dias têm algumas janelas de sol que permitem vistas do platô. Dito isso, não existe 'época seca' no Monte Roraima: chuva é sempre uma probabilidade alta.",
                    "De junho a dezembro, as chuvas são mais intensas e os rios na rota de acesso podem ficar intransitáveis. O platô fica ainda mais nublado e frio. Apesar das dificuldades, aventureiros experientes realizam expedições o ano inteiro ao Roraima — a montanha tem uma atração irresistível que não reconhece estações. Quem vai deve estar preparado para qualquer condição climática em qualquer mês.",
                ],
            },
        ]
    },
    "vale-do-capao-palmeiras": {
        "sections": [
            {
                "h2": "Vale do Capão: a alma da Chapada Diamantina",
                "paragraphs": [
                    "O Vale do Capão, oficialmente Caeté-Açu, é um dos destinos mais especiais da Chapada Diamantina baiana — um vale encaixado entre morros de quartzito onde uma comunidade alternativa e acolhedora coexiste com uma natureza de beleza extraordinária. O vale é o ponto de partida para algumas das trilhas mais espetaculares da chapada, incluindo a subida ao Morro do Castelo, a travessia do Pai Inácio e o acesso aos cânions da Serra do Sincorá.",
                    "O Morro do Castelo, que domina o horizonte do vale com sua forma de mesa, tem uma trilha de aproximadamente 7 km com desnível de 650 metros. No cume, uma plataforma rochosa oferece uma das vistas mais abrangentes da chapada: o Vale do Capão lá embaixo, os morros circulares ao redor e, ao fundo, a Serra do Sincorá com seus picos mais altos. Ao pôr do sol, as cores são tão intensas que parecem pintadas.",
                    "O Vale do Capão tem também acesso à famosa Cachoeira da Fumaça, a maior queda d'água da Bahia com 340 metros de altura. A trilha de cima (mirante) é de fácil acesso; a trilha de baixo, para chegar ao sopé da queda, é uma aventura de dia inteiro que exige boa condição física e guia habilitado. A névoa criada pelo impacto da água no fundo é o que dá o nome à cachoeira.",
                ],
            },
            {
                "h2": "Dicas para trilhar no Vale do Capão",
                "paragraphs": [
                    "O Vale do Capão tem uma infraestrutura turística crescente mas ainda artesanal: pousadas construídas com materiais naturais, restaurantes com culinária orgânica e saúde, e uma atmosfera de comunidade que valoriza a convivência e o respeito à natureza. A vila não tem banco nem caixa eletrônico — leve dinheiro em espécie suficiente para toda a estadia.",
                    "A grande maioria das trilhas da região exige guia habilitado e registrado no CADASTUR. O Vale do Capão tem uma associação de guias locais com longa tradição na Chapada Diamantina — contrate com antecedência, pois os melhores guias ficam agendados rapidamente nos períodos de alta temporada (julho, carnaval e festas de fim de ano).",
                    "Para trilhas de vários dias como o Vale do Pati (que tem ponto de entrada próximo ao Vale do Capão), o planejamento deve incluir carregadores ou mulas para o bagageiro se o grupo não tiver experiência em expedições. A trilha atravessa fazendas onde os moradores recebem trilheiros com alimentação e pernoite simples — uma forma de turismo de base comunitária que merece apoio.",
                ],
            },
            {
                "h2": "Quando visitar o Vale do Capão",
                "paragraphs": [
                    "De junho a novembro, a Chapada Diamantina vive seu melhor momento para trilhas: tempo seco, calor moderado e os campos rupestres cobertos de sempre-vivas e orquídeas. O Vale do Capão especificamente tem noites mais frescas do que Lençóis e Palmeiras por sua altitude e pelo efeito vale que refresca o ar ao anoitecer — agasalho leve é bem-vindo.",
                    "De dezembro a maio, as chuvas transformam a paisagem e algumas trilhas ficam fechadas ou muito difíceis. A Cachoeira da Fumaça fica ainda mais poderosa com a água das chuvas — o volume de queda aumenta muito e o efeito névoa se intensifica. Para quem quer ver a queda no máximo de sua potência e está preparado para trilhar no barro, fevereiro e março têm um charme especial.",
                    "O Vale do Capão é acessível de carro ou ônibus a partir de Palmeiras (15 km) e de Lençóis (45 km). A estrada de acesso tem trecho não pavimentado que pode ficar difícil na época de chuva. Veículos com boa altura ao solo são recomendados para chegar à vila. Alguns visitantes optam por entrar de Lençóis e sair pelo vale (ou vice-versa), fazendo uma bela travessia de 2 dias.",
                ],
            },
        ]
    },
}

# ---------------------------------------------------------------------------
# Geração do HTML da seção editorial
# ---------------------------------------------------------------------------
def build_editorial_html(city_slug: str, data: dict) -> str:
    lines = [
        f'<section class="section section--alt" id="sobre-{city_slug}" aria-labelledby="editorial-h2-{city_slug}">',
        '  <div class="container">',
        '    <div class="editorial">',
    ]
    for i, section in enumerate(data["sections"]):
        anchor_id = f'editorial-h2-{city_slug}-{i}'
        lines.append(f'      <h2 id="{anchor_id}">{section["h2"]}</h2>')
        for para in section["paragraphs"]:
            lines.append(f'      <p>{para}</p>')
    lines += [
        '    </div>',
        '  </div>',
        '</section>',
    ]
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------------
# Ponto de injeção: antes da seção "Por que trilheiros confiam no Trekko"
# ---------------------------------------------------------------------------
INJECTION_MARKER = '<section class="section section--alt" aria-labelledby="sp-h2">'


def inject_into_file(filepath: str, city_slug: str, content_data: dict) -> bool:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    if INJECTION_MARKER not in html:
        print(f"  [WARN] Ponto de injeção não encontrado em {filepath}")
        return False

    # Verificar se o conteúdo já foi injetado
    marker_id = f'id="sobre-{city_slug}"'
    if marker_id in html:
        print(f"  [SKIP] Conteúdo já injetado em {filepath}")
        return False

    editorial_html = build_editorial_html(city_slug, content_data)
    new_html = html.replace(INJECTION_MARKER, editorial_html + INJECTION_MARKER, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    cities = sorted(os.listdir(BASE_DIR))
    print(f"Processando {len(cities)} cidades em {BASE_DIR}\n")

    injected = 0
    skipped = 0
    missing_content = []

    for city_slug in cities:
        city_dir = os.path.join(BASE_DIR, city_slug)
        index_file = os.path.join(city_dir, "index.html")

        if not os.path.isfile(index_file):
            print(f"[SKIP] {city_slug}: index.html não encontrado")
            skipped += 1
            continue

        if city_slug not in CITY_CONTENT:
            print(f"[MISSING] {city_slug}: conteúdo editorial não definido")
            missing_content.append(city_slug)
            continue

        print(f"[OK] Injetando conteúdo em: {city_slug}")
        ok = inject_into_file(index_file, city_slug, CITY_CONTENT[city_slug])
        if ok:
            injected += 1
        else:
            skipped += 1

    print(f"\n✅ Injetados: {injected}")
    print(f"⏭  Pulados: {skipped}")
    if missing_content:
        print(f"❌ Sem conteúdo definido: {', '.join(missing_content)}")

    # Validação rápida
    print("\n--- Validação ---")
    for city_slug in cities:
        index_file = os.path.join(BASE_DIR, city_slug, "index.html")
        if not os.path.isfile(index_file):
            continue
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        p_count = content.count('<p>')
        word_count = sum(
            len(line.split())
            for line in content.split('\n')
            if '<p>' in line and not '<p><button' and not '<p>©'
        )
        status_p = '✅' if p_count >= 8 else '❌'
        print(f"  {status_p} {city_slug}: {p_count} <p> tags")


if __name__ == "__main__":
    main()
