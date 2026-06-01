#!/usr/bin/env python3
"""
Add editorial calendar articles for weeks 9-10 to data/blog.json
and generate their HTML pages.
Run from repo root: python3 _add_editorial_week9_10.py
"""
import json, os, re

# ── Load existing blog data ────────────────────────────────────────────────
with open("data/blog.json", encoding="utf-8") as f:
    posts = json.load(f)

existing_slugs = {p["slug"] for p in posts}

# ── New articles ───────────────────────────────────────────────────────────
new_articles = [
    {
        "id": 35,
        "slug": "trilhas-espirito-santo-guia-completo",
        "title": "Melhores Trilhas do Espírito Santo: Pedra Azul, Forno Grande e Muito Mais",
        "subtitle": "Do litoral à Mata Atlântica serrana: um estado cheio de opções para trilheiros de todos os níveis",
        "content": """O Espírito Santo é um dos estados mais subestimados do trekking brasileiro. Espremido entre Rio de Janeiro e Bahia, carrega parques estaduais pouco divulgados, picos acima de 2.000 metros e cachoeiras que rivalizam com qualquer destino do sudeste. Este guia reúne as melhores trilhas capixabas para você planejar sua próxima aventura.

## Parque Estadual da Pedra Azul: A Joia da Coroa Capixaba

A Pedra Azul é o cartão-postal mais reconhecível do Espírito Santo. O monólito de granito azulado — a cor varia conforme a incidência de luz e umidade — domina a paisagem da Serra do Caparaó sul-capixaba e pode ser visto a quilômetros de distância na rodovia ES-164.

**Trilha para a Piscina Natural da Pedra Azul**
- Distância: 2,5 km circular
- Dificuldade: fácil a moderada
- Desnível: 250m
- Destaque: piscinas de água cristalina formadas em cavidades graníticas na base do monólito

A trilha é guiada obrigatoriamente — contrate na portaria do parque. O guia local é fundamental pois há trechos de escalada simples nas pedras molhadas. A água das piscinas é fria o ano inteiro, mas o banho compensa cada metro da subida.

**Melhor época:** abril a setembro (seco). Evite dezembro-fevereiro (chuvas intensas tornam as pedras escorregadias).

## Parque Estadual Forno Grande: O Vizinho Menos Famoso Mas Igualmente Impressionante

A apenas 30 km da Pedra Azul, o Parque Estadual Forno Grande reúne formações rochosas distintas em meio à Mata Atlântica densa da Serra do Caparaó. O nome vem do formato da principal formação rochosa, que lembra a boca de um forno de pedra.

**Trilha do Pico do Forno Grande (2.042m)**
- Distância: 8 km ida e volta
- Dificuldade: difícil
- Desnível: 700m
- Exige: bom condicionamento físico, calçado com aderência

O pico oferece vista panorâmica do maciço do Caparaó e, em dias claros, é possível enxergar até o litoral capixaba. A trilha cruza matas de neblina na faixa de altitude entre 1.400m e 2.000m — rica em bromélias, orquídeas e aves endêmicas da Mata Atlântica.

**Guia:** recomendado, mas não obrigatório em condições normais. A ACARENM (Associação de Condutores de Alto Caparaó) oferece guias para ambos os parques.

## Parque Nacional do Caparaó: Pico da Bandeira pelo Lado Capixaba

O [Pico da Bandeira (2.892m)](/blog/pico-da-bandeira-guia-completo), terceiro ponto mais alto do Brasil, tem seu acesso principal pelo lado mineiro, mas a vertente capixaba — via Alto Caparaó — oferece uma alternativa menos movimentada com paisagens igualmente espetaculares.

A trilha pela entrada capixaba tem 14 km (ida e volta) com desnível de 1.300m. O percurso passa pelos Vale dos Deuses e Cachoeira Bonita antes de encontrar a rota principal no Pico do Cristal. Menos frequentada que o lado mineiro, essa alternativa é ideal para quem quer mais silêncio e natureza sem multidão.

## Cachoeira do Riacho (Domingos Martins): Trekking Serrano com Sabor Germânico

O município de Domingos Martins, colonizado por imigrantes alemães no século XIX, combina arquitetura europeia com trilhas serradas que sobem a encosta da Serra do Mar capixaba.

**Trilha da Pedra dos Pontões**
- Distância: 6 km
- Dificuldade: moderada
- Desnível: 400m
- Destaque: formações rochosas pontiagudas únicas no Brasil, frequentadas por praticantes de escalada esportiva

Domingos Martins fica a 42 km de Vitória pela BR-262. A infraestrutura de hospedagem e gastronomia da cidade é excelente — boa base para explorar toda a região serrana capixaba.

## Santa Teresa: Biodiversidade e Trilhas no Quintal do Museu de Biologia

Santa Teresa é um município de 25.000 habitantes que abriga o Museu de Biologia Prof. Mello Leitão, um dos mais importantes centros de pesquisa de biodiversidade da Mata Atlântica. Ao redor do museu, trilhas interpretativas percorrem a zona de mata original da cidade.

A **Trilha das Bromélias** (3 km, fácil) é conduzida por pesquisadores do museu às sextas e sábados, com identificação de fauna e flora ao longo do percurso. Uma experiência educativa rara que combina natureza e ciência.

## Reserva Natural Vale (Linhares): Planície Costeira de Mata Atlântica

A Reserva Natural Vale, em Linhares, é a maior reserva particular de Mata Atlântica do Brasil. Com 23.000 hectares de floresta contínua no litoral norte capixaba, abriga espécies como o mutum-do-sudeste e o mico-de-cara-branca — aves e mamíferos em perigo de extinção.

As trilhas da reserva são abertas ao público mediante agendamento prévio no site da Vale. Os roteiros têm de 5 a 15 km e são acompanhados por guias biólogos — uma experiência completamente diferente das trilhas serranas.

## Como Planejar sua Visita ao Espírito Santo

**Acesso:** Vitória tem aeroporto com voos diretos de São Paulo, Rio de Janeiro, Belo Horizonte, Brasília e Salvador. De carro, a BR-101 conecta o estado a São Paulo (10h) e ao Rio (4h).

**Base de operações:** Domingos Martins (para Pedra Azul e Forno Grande) ou Alto Caparaó (para o Caparaó). Vitória é uma boa base para a Reserva Vale e Santa Teresa.

**Temporada:** abril a setembro é o período mais seco. O inverno capixaba (jun-ago) é ameno na faixa costeira, mas frio nas serras — leve agasalho para trilhas acima de 1.000m.

Para mais destinos do sudeste, confira as [melhores trilhas de Minas Gerais](/blog/melhores-trilhas-minas-gerais) e o guia completo das [trilhas do estado de São Paulo para iniciantes](/blog/trilhas-faceis-sao-paulo). Se planeja incluir o [Pico da Bandeira](/blog/pico-da-bandeira-guia-completo) no roteiro, leia o guia completo antes de partir.""",
        "excerpt": "Do monólito azulado da Pedra Azul aos picos acima de 2.000m do Caparaó: guia completo das melhores trilhas capixabas para todos os níveis.",
        "category": "trilhas-destinos",
        "imageUrl": "/trails/bCKTbP7YuBYO.jpg",
        "images": ["/trails/bCKTbP7YuBYO.jpg"],
        "authorId": 3,
        "authorSlug": "marcos-rodrigues",
        "authorName": "Marcos Rodrigues",
        "authorRole": "Guia de Turismo CADASTUR | Expedições Amazônicas",
        "authorBio": "Marcos Rodrigues é guia de turismo credenciado pelo CADASTUR com mais de 12 anos de atuação em expedições pela Amazônia e pelo Cerrado. Especialista em ecoturismo de base comunitária, já conduziu grupos em mais de 30 trilhas diferentes pelo Brasil.",
        "authorCredentials": "Guia CADASTUR credenciado | Certificação em Primeiros Socorros Wilderness",
        "readingTime": 7,
        "relatedTrailIds": [],
        "tags": ["espirito-santo", "pedra-azul", "caparao", "mata-atlantica", "sudeste"],
        "metaTitle": "Melhores Trilhas do Espírito Santo: Pedra Azul, Forno Grande e Caparaó | Trekko",
        "metaDescription": "Guia completo das melhores trilhas do Espírito Santo: Parque da Pedra Azul, Forno Grande, Pico da Bandeira e mais. Dicas de acesso, dificuldade e melhor época.",
        "featured": 0,
        "viewCount": 0,
        "status": "published",
        "publishedAt": "2026-06-02T10:00:00.000Z",
        "createdAt": "2026-06-02T10:00:00.000Z",
        "updatedAt": "2026-06-02T10:00:00.000Z",
    },
    {
        "id": 36,
        "slug": "orientacao-sem-gps-trilha",
        "title": "Como se Orientar em Trilhas Sem GPS ou Celular",
        "subtitle": "Bússola, mapa e marcos naturais: as técnicas que podem salvar sua vida quando a tecnologia falha",
        "content": """Seu celular está sem bateria. O GPS de bolso caiu no rio. Você está a 8 km do ponto de saída, o nevoeiro fechou e a trilha sumiu. O que você faz? Este guia ensina as técnicas de orientação que todo trilheiro deveria dominar antes de depender de qualquer aplicativo.

## Por Que a Orientação Manual Ainda é Essencial

O GPS e os aplicativos de mapas revolucionaram o trekking, mas criaram uma dependência perigosa. Baterias acabam, sinais de satélite falham em cânions ou sob cobertura densa de mata, e telas se quebram. Trilheiros que saem sem conhecimento básico de orientação estão apostando que nada vai dar errado.

A orientação com mapa e bússola não é um hobby de explorador vintage. É uma habilidade de segurança que complementa — e nunca substitui — a tecnologia. O objetivo é saber o que fazer quando a tecnologia falha.

## Entendendo o Mapa Topográfico

Um mapa topográfico representa o relevo por meio de curvas de nível: linhas que unem pontos de mesma altitude. Algumas regras básicas:

- **Curvas muito próximas** = terreno íngreme
- **Curvas espaçadas** = terreno suave
- **Curvas em "V" apontando para cima** = vale ou rio
- **Curvas em "V" apontando para baixo** = cume ou crista
- **Círculos concêntricos fechados** = pico ou colina

O **intervalo de curvas** (diferença de altitude entre curvas consecutivas) varia conforme a escala do mapa. Em mapas 1:25.000 o intervalo é geralmente 10m. Em 1:50.000 é 20m.

**Onde obter mapas topográficos do Brasil:** o IBGE disponibiliza gratuitamente mapas de todo o território nacional em seu geoportal. O serviço TOPODATA do INPE oferece dados altimétricos que podem ser visualizados no QGIS ou Google Earth.

## Como Usar a Bússola: Do Básico ao Essencial

A bússola de placa (tipo Suunto A-10 ou Silva Ranger) é a ferramenta padrão para orientação em campo. Ela tem três partes principais:

1. **Agulha magnética** — sempre aponta para o norte magnético
2. **Cápsula giratória** — com marcações de 0° a 360° e seta de orientação
3. **Placa base transparente** — com linhas de direção e escala

### Determinando o Norte e Orientando o Mapa

1. Coloque a bússola plana na mão ou sobre o mapa
2. Gire o corpo até a agulha vermelha alinhar com a seta norte da cápsula
3. O mapa está orientado quando as linhas norte-sul do mapa alinham com a agulha

**Declinação magnética:** o norte magnético (onde a agulha aponta) não coincide com o norte geográfico. No Brasil, a declinação varia de -5° a +3° dependendo da região. Mapas modernos indicam esse valor na legenda — corrija seu azimute adicionando ou subtraindo a declinação.

### Calculando um Azimute

O azimute é o ângulo entre o norte e a direção que você quer seguir, medido no sentido horário de 0° a 360°.

Para ir de um ponto A até um ponto B no mapa:
1. Coloque a borda da placa base conectando A e B
2. Gire a cápsula até as linhas norte-sul da cápsula ficarem paralelas às linhas norte-sul do mapa
3. Leia o azimute na seta de orientação da placa

Para seguir esse azimute em campo: segure a bússola na frente do corpo, gire todo o seu corpo até a agulha magnética alinhar com a seta norte da cápsula. A direção de viagem indicada pela seta da placa é o seu azimute.

## Triangulação: Descobrindo Onde Você Está

Se você sabe que está em algum lugar numa área mas não sabe exatamente onde, a triangulação resolve. Você precisa identificar dois ou três pontos visíveis no terreno que também apareçam no mapa (picos, torres, antenas, capelas).

1. Mirando o primeiro ponto visível, registre o azimute (ex: 045°)
2. No mapa, trace uma linha a partir desse ponto no azimute reverso (045° + 180° = 225°)
3. Repita para o segundo ponto visível
4. A interseção das duas linhas é sua posição aproximada

Com três pontos, o triângulo de erro formado pela interseção das três linhas indica a margem de imprecisão — quanto menor o triângulo, mais precisa é sua localização.

## Marcos Naturais como Referência

Antes de qualquer eletrônico, os navegadores usavam o terreno. Técnicas que funcionam sem equipamento:

**Seguindo um curso d'água:** rios sempre levam a áreas habitadas. Descer um riacho é frequentemente a opção mais segura quando a trilha some.

**Identificando o Sol:** o Sol nasce aproximadamente a leste e se põe a oeste. Ao meio-dia solar, o Sol está ao norte no hemisfério sul (ao sul no hemisfério norte). Use um galho vertical para projetar sombra e determinar os pontos cardeais.

**Usando estrelas:** o Cruzeiro do Sul aponta para o sul celeste. Prolongue o eixo maior da constelação 4,5 vezes — esse ponto imaginário é o sul.

**Vegetação e musgo:** em matas fechadas, o musgo tende a crescer mais abundantemente no lado que recebe menos luz direta — em nosso hemisfério, geralmente o lado sul (mais úmido e sombreado).

## Erros Mais Comuns de Orientação em Trilhas

**Não registrar o ponto de partida:** sempre marque ou anote a direção e azimute de volta ao começo antes de entrar em mata fechada.

**Ignorar a declinação magnética:** em áreas com alta declinação (interior do Brasil), ignorar esse ajuste gera desvios de centenas de metros ao longo de distâncias maiores.

**Confiar num único método:** sempre cruze informações. Se o mapa diz que há um rio à direita mas você está ouvindo água à esquerda, investigue antes de continuar.

**Entrar em pânico e continuar caminhando:** se você está perdido, PARE. Movimento aleatório aumenta a área de busca e o consumo de energia. Fique no lugar, faça barulho, sinalize.

## Equipamento Mínimo de Orientação

Leve sempre, mesmo nas trilhas "simples":
- Bússola de placa (R$ 50–200)
- Mapa topográfico impresso em papel impermeável ou plastificado
- Caneta para anotar coordenadas
- Bateria extra ou carregador portátil para o celular (backup do GPS)

Para trilhas de múltiplos dias em áreas remotas, considere um comunicador via satélite com GPS integrado. Em caso de emergência, saiba o número do [SAMU (192)](tel:192) e dos Bombeiros (193) — mesmo sem sinal, ligações de emergência podem funcionar com antenas de outras operadoras.

Aprimore sua preparação com nosso guia de [segurança em trilhas](/blog/seguranca-trilha-regras) e aprenda a montar o [kit de primeiros socorros para trilha](/blog/kit-primeiros-socorros-trilha) adequado para saídas multi-dia.""",
        "excerpt": "Bússola, mapa topográfico e marcos naturais: as técnicas que todo trilheiro deveria dominar para não depender exclusivamente de GPS e celular.",
        "category": "planejamento-seguranca",
        "imageUrl": "/trails/M5NbSJ18enIH.jpg",
        "images": ["/trails/M5NbSJ18enIH.jpg"],
        "authorId": 2,
        "authorSlug": "ana-beatriz-lima",
        "authorName": "Ana Beatriz Lima",
        "authorRole": "Especialista em Segurança de Montanha",
        "authorBio": "Ana Beatriz Lima é especialista em segurança de montanha com certificação pelo CBME e mais de 8 anos conduzindo trilhas técnicas no Brasil. Colaboradora do Trekko com foco em segurança, primeiros socorros e preparo físico para aventuras na natureza.",
        "authorCredentials": "Certificação CBME em Segurança de Montanha | Instrutora de Primeiros Socorros Wilderness",
        "readingTime": 8,
        "relatedTrailIds": [],
        "tags": ["seguranca", "orientacao", "bussola", "sobrevivencia", "tecnica"],
        "metaTitle": "Como se Orientar em Trilhas Sem GPS ou Celular | Trekko",
        "metaDescription": "Aprenda a usar bússola, mapa topográfico e marcos naturais para se orientar quando a tecnologia falha. Técnicas essenciais de orientação para trilheiros.",
        "featured": 0,
        "viewCount": 0,
        "status": "published",
        "publishedAt": "2026-06-05T10:00:00.000Z",
        "createdAt": "2026-06-05T10:00:00.000Z",
        "updatedAt": "2026-06-05T10:00:00.000Z",
    },
    {
        "id": 37,
        "slug": "pedra-do-bau-guia-completo",
        "title": "Pedra do Baú: Guia Completo para a Trilha Mais Alta de São Paulo",
        "subtitle": "2.033 metros de altitude, blocos de granito e vista panorâmica da Serra da Mantiqueira",
        "content": """A Pedra do Baú é o destino de trekking mais icônico de São Paulo. Com 2.033 metros de altitude e um topo de granito que parece desafiar a gravidade, o monólito domina a paisagem de São Bento do Sapucaí e atrai trilheiros do sudeste inteiro. Este guia cobre tudo que você precisa saber para fazer a trilha com segurança.

## O Que É a Pedra do Baú

A Pedra do Baú é um inselberg granítico — uma formação rochosa que se ergue abruptamente do planalto circundante, resultado da erosão diferencial que deixou o granito resistente exposto enquanto as rochas ao redor foram desgastadas. Visualmente, lembra um baú gigante de pedra, daí o nome.

O monólito fica dentro do Parque Natural Municipal Pedra do Baú, no município de São Bento do Sapucaí (SP), a 190 km de São Paulo pela Rodovia dos Tamoios (SP-099). A área abrange também a Pedra do Bauzinho (1.950m) e a Pedra do Selado.

## A Trilha Principal: Subida ao Topo

**Distância:** 7 km (ida e volta, saindo do Centro de Visitantes)
**Dificuldade:** moderada a difícil
**Desnível:** 550m
**Tempo médio:** 3–4 horas (ida e volta)
**Exige:** bom condicionamento, calçado com aderência, luvas e capacete recomendados para o trecho de escalada

O percurso é dividido em três segmentos:

**1. Trilha de acesso pela mata (3 km):** caminho bem demarcado por floresta ombrófila mista, com altitude crescendo progressivamente. Trechos com raízes e pedras soltas. Moderado.

**2. Base de granito até a "Janela":** a trilha encontra o granito exposto e começa a subida pelas placas de rocha. Há cabos de aço instalados pelo parque nos trechos mais verticais para auxiliar na escalada. Difícil. Aqui é obrigatório o uso de capacete.

**3. Da Janela ao Topo:** últimos 50m de subida pelo granito. A "Janela" é uma passagem estreita entre dois blocos rochosos por onde todos devem passar. Vertiginoso mas factível para quem não tem medo de altura.

**No topo:** plataforma de granito com vista de 360° para a Serra da Mantiqueira, o Vale do Paraíba e, em dias muito claros, o mar ao longe. Há uma estação meteorológica histórica e um vértice geodésico do IBGE.

## Logística e Regras do Parque

**Entrada:** A Pedra do Baú é administrada pela Prefeitura de São Bento do Sapucaí. A entrada no parque é cobrada (preços atualizados no site da prefeitura). Crianças até 12 anos não pagam.

**Capacete obrigatório:** o parque disponibiliza capacetes no Centro de Visitantes, mas é melhor trazer o seu. A obrigatoriedade existe para o trecho de granito exposto.

**Horário de funcionamento:** portões abrem às 8h e fecham às 17h. Não comece a subida depois das 14h — as tempestades da tarde são frequentes e o granito molhado é perigoso.

**Guia:** não obrigatório, mas recomendado para primeiro acesso. A Associação de Ecoturismo de São Bento do Sapucaí (AECOTUR) tem lista de guias locais disponível na prefeitura.

## Pedra do Bauzinho: A Alternativa Menos Badalada

A Pedra do Bauzinho (1.950m) pode ser alcançada por trilha que parte da mesma base, com percurso de 5 km (ida e volta) e desnível de 350m. A subida tem menos trechos de escalada e é adequada para trilheiros de nível intermediário. A vista do topo é menos aberta que a da Pedra do Baú principal, mas o ambiente é mais tranquilo e menos movimentado.

## A Combinação com o Pico Selado

Para trilheiros experientes, a **travessia Pedra do Baú + Pedra do Selado** em um dia (ou dois dias com camping) é um dos melhores roteiros da Mantiqueira paulista. A travessia tem 14 km com desnível acumulado de 900m.

Essa combinação exige condicionamento sólido, mapa topográfico e preferencialmente guia local, pois a interligação entre os picos passa por trechos sem marcação.

## Condições Climáticas e Segurança

**Inverno (jun-ago):** condição ideal. Dias secos, visibilidade máxima, madrugadas frias (pode nevar no entorno acima de 1.800m). Vista mais limpa do sul de Minas.

**Verão (dez-fev):** chuvas diárias, especialmente à tarde. Granito molhado = alta periculosidade. Se chover, desça imediatamente — raios em granito exposto são risco real.

**Ventos:** no topo, rajadas de vento são comuns mesmo com céu limpo. Guarde tudo na mochila — nada pode cair do alto do pico.

**Queda de pedras:** mantenha distância mínima de 5m de outros grupos nas subidas e descidas do granito. Pedras soltas podem ser deslocadas inadvertidamente.

## Hospedagem em São Bento do Sapucaí

O município tem boa infraestrutura de hospedagem com pousadas de charme na área rural e opções de camping próximas ao parque. A cidade fica a 190 km de São Paulo (2h30 pela Rodovia dos Tamoios) e a 250 km do Rio de Janeiro.

**Dica de roteiro:** combine a Pedra do Baú com a visita às fazendas históricas do Vale do Paraíba e às demais trilhas do [Parque Estadual da Serra do Mar](/blog/trilhas-litoral-norte-sp) para um fim de semana completo na região.

Para [preparo físico adequado](/blog/preparo-fisico-trekking) antes de encarar a subida, e para entender como montar o [equipamento certo para trekking](/blog/10-itens-essenciais-mochila-trekking), confira nossos guias específicos. Se planeja explorar mais a Mantiqueira, veja também as [trilhas do Parque Nacional do Caparaó](/blog/pico-da-bandeira-guia-completo).""",
        "excerpt": "2.033m de granito, cabos de aço e vista da Serra da Mantiqueira. Guia completo da Pedra do Baú em São Bento do Sapucaí: trilha, logística e segurança.",
        "category": "trilhas-destinos",
        "imageUrl": "/trails/JgU5fHD8luc1.jpg",
        "images": ["/trails/JgU5fHD8luc1.jpg"],
        "authorId": 1,
        "authorSlug": "rafael-dias",
        "authorName": "Rafael Dias",
        "authorRole": "Trilheiro e Escritor de Montanha",
        "authorBio": "Com mais de 15 anos percorrendo trilhas da Mata Atlântica, Rafael é colaborador técnico do Trekko especializado em rotas do Rio de Janeiro. Já completou a Travessia Petrópolis-Teresópolis seis vezes e documenta suas expedições com foco em segurança e acessibilidade para trilheiros de todos os níveis.",
        "authorCredentials": "Certificação em Primeiros Socorros de Montanha (Cruz Vermelha) | Instrutor de Trekking formado pelo CBME",
        "readingTime": 7,
        "relatedTrailIds": [],
        "tags": ["sao-paulo", "mantiqueira", "granito", "altitude", "sudeste"],
        "metaTitle": "Pedra do Baú: Guia Completo da Trilha Mais Alta de SP (2.033m) | Trekko",
        "metaDescription": "Tudo sobre a Pedra do Baú em São Bento do Sapucaí: trilha, capacete obrigatório, logística, melhor época e dicas de segurança para o monólito mais famoso de SP.",
        "featured": 0,
        "viewCount": 0,
        "status": "published",
        "publishedAt": "2026-06-09T10:00:00.000Z",
        "createdAt": "2026-06-09T10:00:00.000Z",
        "updatedAt": "2026-06-09T10:00:00.000Z",
    },
    {
        "id": 38,
        "slug": "hipotermia-trilha-prevencao-tratamento",
        "title": "Hipotermia em Trilhas: Como Prevenir e Agir em Caso de Emergência",
        "subtitle": "Sinais precoces, estágios clínicos e protocolo de tratamento no campo",
        "content": """Hipotermia mata. E não apenas em expedições árticas ou escaladas alpinas. Em trilhas brasileiras de altitude, ela pode ocorrer no inverno em condições que parecem inofensivas: chuva, vento e roupa inadequada são suficientes para que a temperatura corporal caia perigosamente. Este guia ensina a identificar, prevenir e tratar a hipotermia no campo.

## O Que É Hipotermia e Por Que É Perigosa

Hipotermia é a queda da temperatura corporal central abaixo de 35°C. O corpo humano mantém a temperatura interna em 36,5–37,5°C por meio de mecanismos de termorregulação. Quando a perda de calor supera a produção, esses mecanismos falham progressivamente.

A periculosidade da hipotermia está em sua progressão: os sinais iniciais são sutis e facilmente confundidos com cansaço ou desconforto. Um trilheiro hipotérmico pode não perceber que está em perigo — e seus companheiros precisam reconhecer o problema por ele.

No Brasil, casos graves ocorrem regularmente no Sul (parques do RS e SC), na Serra da Mantiqueira e no Caparaó, especialmente em trilhas de múltiplos dias com acampamento.

## Fatores de Risco em Trilhas Brasileiras

**Altitude combinada com chuva:** acima de 1.500m, a temperatura cai 2–3°C a cada 300m de subida. Uma roupa encharcada perde 90% da capacidade de isolamento térmico.

**Vento:** o fator wind chill amplifica a sensação de frio. A 20 km/h de vento com temperatura de 5°C, a sensação térmica cai para aproximadamente -3°C.

**Desidratação e baixo nível de glicose:** o corpo precisa de combustível para gerar calor. Trilheiros que não comem nem bebem adequadamente ficam mais vulneráveis à hipotermia.

**Fadiga:** músculos cansados tremem menos eficientemente e a percepção de frio diminui com o esgotamento físico.

## Estágios Clínicos e Como Reconhecer

### Hipotermia Leve (35–32°C)
- Tremores intensos e incontroláveis
- Pele pálida ou azulada nas extremidades
- Fala arrastada ou dificuldade de articular palavras
- Movimentos descoordenados (teste: peça para tocar o polegar com cada dedo)
- Irritabilidade, confusão leve

**Sinal de alerta clássico:** o "teste dos 4 Rs" — se a pessoa não consegue Rodar os tornozelos, Resistir a um leve empurrão, Responder perguntas simples ou Reconhecer os próprios dedos das mãos, ela está hipotérmica.

### Hipotermia Moderada (32–28°C)
- Tremores que param (sinal de piora, não de melhora)
- Sonolência, dificuldade de permanecer acordado
- Frequência cardíaca e respiratória reduzidas
- Rigidez muscular progressiva
- Comportamento paradoxal: a pessoa pode querer tirar a roupa ("undressing paradox")

### Hipotermia Grave (abaixo de 28°C)
- Perda de consciência
- Pulso fraco ou imperceptível
- Respiração superficial
- Pupilas dilatadas

**Regra de ouro:** "ninguém está morto até estar quente e morto". Pessoas em hipotermia grave com sinais de morte aparente podem ser reanimadas com êxito após reaquecimento — não abandone as manobras de ressuscitação prematuramente.

## Tratamento no Campo: O Protocolo Correto

### Hipotermia Leve – o que fazer

1. **Remova do frio e do vento** — procure abrigo imediato (barraca, saco de vivac, vegetação densa)
2. **Troque roupa molhada por seca** — com cuidado para não expor ao vento durante a troca
3. **Isolamento térmico** — saco de dormir, manta aluminizada, camadas de roupa seca ao redor
4. **Calor externo suave** — compressas mornas nas axilas, virilha e pescoço (onde há grandes vasos sanguíneos)
5. **Bebidas quentes e açucaradas** — se a pessoa está consciente e consegue engolir com segurança
6. **Atividade física leve** — se possível, exercícios suaves para gerar calor metabólico

### Hipotermia Moderada a Grave – o que NÃO fazer

- **Não friccione a pele** — vasodilatação periférica pode redirecionar sangue frio para o coração
- **Não dê bebidas alcoólicas** — o álcool causa vasodilatação e aumenta a perda de calor
- **Não force movimentação intensa** — sangue frio das extremidades pode causar colapso cardíaco ("afterdrop")
- **Não aplique calor direto** (água quente, fogueira direta) em casos moderados a graves
- **Não deixe a pessoa dormir** sozinha em hipotermia moderada

Para hipotermia moderada ou grave: **evacue imediatamente**. Mantenha isolamento térmico durante o transporte. Acione o resgate (193 Bombeiros, 192 SAMU) com o máximo de antecedência possível.

## Equipamento Preventivo Obrigatório

O [sistema de camadas de roupa](/blog/sistema-camadas-roupa-trekking) é a primeira linha de defesa:

- **Camada base:** lã merino ou sintético (nunca algodão — o algodão encharcado acelera a hipotermia)
- **Camada intermediária:** fleece ou lã mais espessa para isolamento
- **Camada externa:** capa impermeável e à prova de vento

Além das roupas:
- Manta aluminizada de emergência (pesa menos de 100g, cabe no bolso)
- Saco de vivac de emergência (alternativa mais completa à manta)
- Touca e luvas (a cabeça e as mãos perdem calor rápido)
- Garrafa térmica com bebida quente em trilhas de inverno

## Hipotermia x Exaustão por Calor: Não Confunda

Em trilhas de verão ou de baixa altitude, o risco inverso existe: a hipertermia (superaquecimento). Confundir os dois quadros é um erro grave. A hipotermia ocorre em ambientes frios e a pele fica pálida e fria; a hipertermia ocorre em calor intenso com atividade física e a pele fica quente e vermelha (ou paradoxalmente fria e seca em casos graves).

Para complementar seu preparo de segurança, veja nosso guia de [kit de primeiros socorros para trilha](/blog/kit-primeiros-socorros-trilha) e saiba como se [preparar fisicamente para o trekking](/blog/preparo-fisico-trekking). Para trilhas de inverno especificamente, consulte o guia de [como se preparar para trilhas de inverno](/blog/trilhas-inverno-como-se-preparar).""",
        "excerpt": "Sinais precoces, estágios clínicos e protocolo de tratamento no campo. Tudo que você precisa saber sobre hipotermia para trilhas de altitude e inverno.",
        "category": "planejamento-seguranca",
        "imageUrl": "/trails/NIqNdEU3BQqS.jpg",
        "images": ["/trails/NIqNdEU3BQqS.jpg"],
        "authorId": 2,
        "authorSlug": "ana-beatriz-lima",
        "authorName": "Ana Beatriz Lima",
        "authorRole": "Especialista em Segurança de Montanha",
        "authorBio": "Ana Beatriz Lima é especialista em segurança de montanha com certificação pelo CBME e mais de 8 anos conduzindo trilhas técnicas no Brasil. Colaboradora do Trekko com foco em segurança, primeiros socorros e preparo físico para aventuras na natureza.",
        "authorCredentials": "Certificação CBME em Segurança de Montanha | Instrutora de Primeiros Socorros Wilderness",
        "readingTime": 8,
        "relatedTrailIds": [],
        "tags": ["seguranca", "primeiros-socorros", "inverno", "altitude", "hipotermia"],
        "metaTitle": "Hipotermia em Trilhas: Sinais, Estágios e Como Tratar no Campo | Trekko",
        "metaDescription": "Guia completo sobre hipotermia em trilhas: como reconhecer os estágios, o que fazer e o que não fazer no campo, e equipamento preventivo essencial.",
        "featured": 0,
        "viewCount": 0,
        "status": "published",
        "publishedAt": "2026-06-12T10:00:00.000Z",
        "createdAt": "2026-06-12T10:00:00.000Z",
        "updatedAt": "2026-06-12T10:00:00.000Z",
    },
]

# ── Validate word counts ────────────────────────────────────────────────────
for a in new_articles:
    wc = len(a["content"].split())
    assert wc >= 800, f"ERRO: {a['slug']} tem apenas {wc} palavras (mínimo 800)"
    print(f"  ✓ {a['slug']} — {wc} palavras")

# ── Add to blog.json ────────────────────────────────────────────────────────
added = 0
for a in new_articles:
    if a["slug"] in existing_slugs:
        print(f"  SKIP (já existe): {a['slug']}")
        continue
    posts.append(a)
    added += 1

with open("data/blog.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print(f"\n{added} artigos adicionados ao data/blog.json")

# ── Generate HTML pages ────────────────────────────────────────────────────
BLOG_TEMPLATE = open("blog/melhores-trilhas-minas-gerais/index.html", encoding="utf-8").read()


def apply_inline(text):
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def md_to_html(text):
    lines = text.split("\n")
    html_lines = []
    in_ul = False
    buffer = []

    def flush_p():
        nonlocal buffer
        if buffer:
            para = " ".join(buffer).strip()
            if para:
                html_lines.append(f"    <p>{apply_inline(para)}</p>")
            buffer = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("## "):
            flush_p()
            if in_ul:
                html_lines.append("    </ul>")
                in_ul = False
            html_lines.append(f"    <h2>{apply_inline(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            flush_p()
            if in_ul:
                html_lines.append("    </ul>")
                in_ul = False
            html_lines.append(f"    <h3>{apply_inline(stripped[4:])}</h3>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            flush_p()
            if not in_ul:
                html_lines.append("    <ul>")
                in_ul = True
            html_lines.append(f"      <li>{apply_inline(stripped[2:])}</li>")
        elif stripped == "":
            flush_p()
            if in_ul:
                html_lines.append("    </ul>")
                in_ul = False
        else:
            buffer.append(stripped)

    flush_p()
    if in_ul:
        html_lines.append("    </ul>")

    return "\n".join(html_lines)


def build_html(post):
    title = post["title"]
    subtitle = post["subtitle"]
    slug = post["slug"]
    meta_title = post["metaTitle"]
    meta_desc = post["metaDescription"]
    pub = post["publishedAt"]
    author = post["authorName"]
    author_role = post["authorRole"]
    author_bio = post["authorBio"]
    reading_time = post["readingTime"]
    category = post["category"]
    excerpt = post["excerpt"]
    image = post["imageUrl"]
    tags = post.get("tags", [])
    tag_html = " ".join(f'<span class="tag">{t}</span>' for t in tags)

    cat_labels = {
        "trilhas-destinos": "Trilhas e Destinos",
        "planejamento-seguranca": "Planejamento e Segurança",
        "equipamentos": "Equipamentos",
        "guias-praticos": "Guias Práticos",
        "conservacao-ambiental": "Conservação Ambiental",
    }
    cat_label = cat_labels.get(category, category)
    pub_date = pub[:10]

    article_html = md_to_html(post["content"])

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta_title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://trekko.com.br/blog/{slug}">
<meta property="og:title" content="{meta_title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://trekko.com.br/blog/{slug}">
<meta property="og:image" content="https://trekko.com.br/images/trekko_logo_horizontal_color_transparent.png" />
<meta property="og:image:width" content="1024" /><meta property="og:image:height" content="1024" />
<meta property="article:published_time" content="{pub}">
<meta property="article:modified_time" content="{pub}">
<meta property="article:author" content="{author}">
<link rel="icon" href="/favicon-48x48.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap"></noscript>
<script>window.TREKKO_CONFIG={{GA4_ID:'G-S816P190VN',GTM_ID:null,ADS_ID:'AW-355784943'}};</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S816P190VN"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-S816P190VN');</script>
<script defer src="/assets/trekko-analytics.js"></script>
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@graph": [
  {{
   "@type": "Article",
   "@id": "https://trekko.com.br/blog/{slug}/#article",
   "headline": "{title}",
   "description": "{meta_desc}",
   "image": "https://trekko.com.br/images/trekko_logo_horizontal_color_transparent.png",
   "datePublished": "{pub[:10]}T10:00:00-03:00",
   "dateModified": "{pub[:10]}T10:00:00-03:00",
   "author": {{
    "@type": "Person",
    "name": "{author}",
    "description": "{author_role}"
   }},
   "publisher": {{
    "@type": "Organization",
    "name": "Trekko",
    "logo": "https://trekko.com.br/android-chrome-192x192.png",
    "url": "https://trekko.com.br"
   }},
   "mainEntityOfPage": "https://trekko.com.br/blog/{slug}"
  }},
  {{
   "@type": "BreadcrumbList",
   "itemListElement": [
    {{"@type": "ListItem","position": 1,"name": "Trekko","item": "https://trekko.com.br"}},
    {{"@type": "ListItem","position": 2,"name": "Blog","item": "https://trekko.com.br/blog"}},
    {{"@type": "ListItem","position": 3,"name": "{title}","item": "https://trekko.com.br/blog/{slug}"}}
   ]
  }}
 ]
}}
</script>
<style>
:root{{--primary:#15803d;--primary-dark:#166534;--primary-hover:#16a34a;--primary-light:#dcfce7;--primary-bg:#f0fdf4;--accent:#f59e0b;--accent-light:#fef3c7;--text-primary:#1e293b;--text-secondary:#475569;--text-muted:#94a3b8;--border:#e2e8f0;--white:#fff;--bg-light:#f8fafc;--shadow-sm:0 1px 3px rgba(0,0,0,.08);--shadow-md:0 4px 12px rgba(0,0,0,.1);--radius:8px;--radius-lg:16px;--font-body:'Inter',sans-serif;--font-heading:'Sora',sans-serif;--max-w:1200px;--gutter:1.25rem}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--font-body);color:var(--text-primary);background:var(--white);line-height:1.7;font-size:1rem}}
a{{color:var(--primary);text-decoration:none}}a:hover{{text-decoration:underline}}
.container{{max-width:var(--max-w);margin:0 auto;padding:0 var(--gutter)}}
header{{background:var(--white);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;padding:.75rem 0}}
.header-inner{{display:flex;align-items:center;justify-content:space-between;gap:1rem}}
.logo{{display:flex;align-items:center;gap:.5rem;font-family:var(--font-heading);font-weight:700;font-size:1.25rem;color:var(--primary)}}
.logo img{{height:32px}}
nav{{display:flex;gap:1.5rem;align-items:center}}
nav a{{font-size:.9rem;font-weight:500;color:var(--text-secondary)}}nav a:hover{{color:var(--primary);text-decoration:none}}
.btn-primary{{background:var(--primary);color:var(--white)!important;padding:.5rem 1rem;border-radius:var(--radius);font-size:.875rem;font-weight:600}}
.btn-primary:hover{{background:var(--primary-dark);text-decoration:none!important}}
.breadcrumb{{padding:.75rem 0;font-size:.8rem;color:var(--text-muted);display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}}
.breadcrumb a{{color:var(--text-muted)}}
.article-header{{padding:2rem 0 1.5rem}}
.article-category{{display:inline-block;background:var(--primary-light);color:var(--primary-dark);font-size:.75rem;font-weight:600;padding:.25rem .75rem;border-radius:999px;text-transform:uppercase;letter-spacing:.05em;margin-bottom:1rem}}
.article-title{{font-family:var(--font-heading);font-size:clamp(1.5rem,4vw,2.5rem);font-weight:700;line-height:1.2;margin-bottom:.75rem;color:var(--text-primary)}}
.article-subtitle{{font-size:1.1rem;color:var(--text-secondary);margin-bottom:1.25rem;line-height:1.5}}
.article-meta{{display:flex;gap:1rem;flex-wrap:wrap;font-size:.85rem;color:var(--text-muted);align-items:center}}
.article-meta span{{display:flex;align-items:center;gap:.3rem}}
.article-layout{{display:grid;grid-template-columns:1fr min(680px,100%) 1fr;gap:0}}
.article-layout>*{{grid-column:2}}
.article-body{{padding:1.5rem 0 2rem}}
.article-body h2{{font-family:var(--font-heading);font-size:1.4rem;font-weight:700;margin:2rem 0 .75rem;color:var(--text-primary)}}
.article-body h3{{font-family:var(--font-heading);font-size:1.15rem;font-weight:600;margin:1.5rem 0 .5rem;color:var(--text-primary)}}
.article-body p{{margin-bottom:1rem;color:var(--text-secondary)}}
.article-body ul{{padding-left:1.25rem;margin-bottom:1rem}}
.article-body li{{margin-bottom:.4rem;color:var(--text-secondary)}}
.article-body strong{{color:var(--text-primary);font-weight:600}}
.article-body a{{color:var(--primary);font-weight:500}}
.article-tags{{display:flex;gap:.5rem;flex-wrap:wrap;margin:1.5rem 0}}
.tag{{background:var(--bg-light);border:1px solid var(--border);color:var(--text-secondary);font-size:.75rem;padding:.2rem .6rem;border-radius:999px}}
.author-card{{background:var(--bg-light);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1.5rem;margin:2rem 0;display:flex;gap:1rem;align-items:flex-start}}
.author-avatar{{width:56px;height:56px;border-radius:50%;background:var(--primary-light);display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0}}
.author-info h4{{font-family:var(--font-heading);font-size:1rem;font-weight:700;margin-bottom:.25rem}}
.author-info p{{font-size:.85rem;color:var(--text-secondary);margin-bottom:.25rem}}
.author-credentials{{font-size:.75rem;color:var(--text-muted)}}
footer{{background:var(--text-primary);color:var(--text-muted);padding:3rem 0 2rem;margin-top:3rem}}
.footer-inner{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:2rem}}
.footer-brand h3{{font-family:var(--font-heading);color:var(--white);font-size:1.1rem;margin-bottom:.5rem}}
.footer-brand p{{font-size:.85rem;line-height:1.6}}
.footer-col h4{{font-family:var(--font-heading);color:var(--white);font-size:.9rem;margin-bottom:.75rem}}
.footer-col ul{{list-style:none}}
.footer-col li{{margin-bottom:.4rem}}
.footer-col a{{color:var(--text-muted);font-size:.85rem}}
.footer-col a:hover{{color:var(--white);text-decoration:none}}
.footer-bottom{{border-top:1px solid rgba(255,255,255,.1);margin-top:2rem;padding-top:1.5rem;text-align:center;font-size:.8rem}}
@media(max-width:768px){{nav{{display:none}}.article-title{{font-size:1.5rem}}.author-card{{flex-direction:column}}}}
</style>
</head>
<body>
<header>
  <div class="container header-inner">
    <a href="/" class="logo"><img src="/LOGOTREKKO2.png" alt="Trekko">Trekko</a>
    <nav>
      <a href="/blog">Blog</a>
      <a href="/trilhas">Trilhas</a>
      <a href="/guias">Guias</a>
      <a href="/seguranca-em-trilhas">Segurança</a>
      <a href="/equipamentos" class="btn-primary">Equipamentos</a>
    </nav>
  </div>
</header>

<div class="container">
  <nav class="breadcrumb" aria-label="breadcrumb">
    <a href="/">Trekko</a> › <a href="/blog">Blog</a> › {cat_label}
  </nav>
</div>

<main class="container">
  <div class="article-header">
    <span class="article-category">{cat_label}</span>
    <h1 class="article-title">{title}</h1>
    <p class="article-subtitle">{subtitle}</p>
    <div class="article-meta">
      <span>✍️ {author}</span>
      <span>📅 {pub_date}</span>
      <span>⏱ {reading_time} min de leitura</span>
    </div>
  </div>

  <div class="article-layout">
    <article class="article-body">
      <!-- article-content-start -->
{article_html}
      <!-- article-content-end -->
      <div class="article-tags">{tag_html}</div>
      <div class="author-card">
        <div class="author-avatar">🧭</div>
        <div class="author-info">
          <h4>{author}</h4>
          <p>{author_bio}</p>
          <p class="author-credentials">{post["authorCredentials"]}</p>
        </div>
      </div>
    </article>
  </div>
</main>

<footer>
  <div class="container">
    <div class="footer-inner">
      <div class="footer-brand">
        <h3>Trekko</h3>
        <p>O guia de trekking mais completo do Brasil. Trilhas, guias, equipamentos e segurança para aventureiros de todos os níveis.</p>
      </div>
      <div class="footer-col">
        <h4>Conteúdo</h4>
        <ul>
          <li><a href="/blog">Blog</a></li>
          <li><a href="/trilhas">Trilhas</a></li>
          <li><a href="/guias">Guias CADASTUR</a></li>
          <li><a href="/equipamentos">Equipamentos</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Segurança</h4>
        <ul>
          <li><a href="/seguranca-em-trilhas">Guia de Segurança</a></li>
          <li><a href="/blog/kit-primeiros-socorros-trilha">Primeiros Socorros</a></li>
          <li><a href="/blog/como-escolher-trilha-segura-brasil">Escolher Trilha Segura</a></li>
          <li><a href="/blog/animais-perigosos-trilhas-brasil">Animais Perigosos</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Institucional</h4>
        <ul>
          <li><a href="/politica-editorial">Política Editorial</a></li>
          <li><a href="/divulgacao-de-afiliados">Afiliados</a></li>
          <li><a href="/privacidade">Privacidade</a></li>
          <li><a href="/termos-de-uso">Termos de Uso</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 Trekko. Todos os direitos reservados.</p>
    </div>
  </div>
</footer>
</body>
</html>"""
    return html


# ── Write HTML files ────────────────────────────────────────────────────────
html_written = 0
for a in new_articles:
    slug = a["slug"]
    dir_path = os.path.join("blog", slug)
    html_path = os.path.join(dir_path, "index.html")

    if os.path.exists(html_path):
        print(f"  SKIP HTML (já existe): {slug}")
        continue

    os.makedirs(dir_path, exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_html(a))

    wc = len(a["content"].split())
    h2_count = a["content"].count("\n## ")
    links = len(re.findall(r'\]\(/', a["content"]))
    status = "✓" if (wc >= 800 and h2_count >= 5 and links >= 3) else f"⚠ h2={h2_count} links={links} words={wc}"
    print(f"  {status} {slug} — HTML gerado")
    html_written += 1

print(f"\n{html_written} páginas HTML criadas em blog/")
