#!/usr/bin/env python3
import json

with open('data/blog.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

expansions = {}

# A18 - preparo-fisico-trekking (id=27, 85w -> 1000w)
expansions[27] = """Uma das crenças mais comuns e mais prejudiciais sobre o trekking é que "qualquer pessoa pode ir, é só caminhar". Caminhar sim — mas caminhar em terreno irregular por 6 horas com mochila de 8 kg e 600 metros de desnível acumulado é muito diferente de uma caminhada urbana de 30 minutos. A falta de preparo físico adequado é responsável por boa parte do sofrimento desnecessário e das lesões que afastam iniciantes para sempre da prática.

A boa notícia: você não precisa ser atleta para fazer trekking. Mas precisa de uma base mínima de condicionamento — e essa base se constrói de forma simples, progressiva e sem academia cara.

## Por Que o Trekking Exige Preparo Específico

O trekking trabalha grupos musculares e padrões de movimento que o exercício urbano típico não treina:

**Subidas longas** ativam intensamente quadríceps, glúteos e panturrilhas. Quem não treina especificamente essas regiões para esforço prolongado vai sentir fadiga muscular prematura e dificuldade nas descidas.

**Descidas** são tecnicamente mais difíceis que subidas para articulações. O joelho absorve forças de até 3 a 5 vezes o peso corporal em cada passo numa descida longa com mochila. Sem preparo, a dor nos joelhos começa a aparecer depois de 2 a 3 horas.

**Terreno irregular** exige estabilizadores do tornozelo e core ativo constantemente. Quem treina apenas em esteira ou piso plano não desenvolve essa estabilidade — e vai tropeçar mais.

**Carga nas costas** muda completamente a biomecânica da caminhada. Uma mochila de 8 kg aumenta o esforço de cada passo e o impacto nas articulações.

## Avaliando Seu Nível Atual

Antes de começar qualquer programa, saiba onde você está. Um indicador simples:

**Sedentário:** não pratica atividade física regular. Precisa de 8 a 12 semanas de condicionamento básico antes da primeira trilha moderada.

**Ativo casual:** caminha ou faz atividade leve 2 a 3 vezes por semana. Precisa de 4 a 6 semanas de preparo específico para trilhas de 1 dia com desnível.

**Ativo regular:** pratica esporte ou academia regularmente. Pode começar com trilhas moderadas imediatamente, mas precisa treinar especificamente subidas e descidas.

## Programa de 8 Semanas Para Iniciantes

Este programa não requer academia. Tudo pode ser feito em ambiente urbano ou em parques.

**Semanas 1–2: Base Cardiovascular**
- 3 sessões por semana de caminhada de 45–60 minutos em ritmo moderado
- Inclua qualquer subida disponível (escadas, rampas, pontes)
- Alongamento de 10 minutos ao final de cada sessão focando quadríceps, panturrilha e lombar

**Semanas 3–4: Aumento de Volume e Desnível**
- 3 sessões de caminhada de 60–90 minutos
- Priorize rotas com subidas e descidas repetidas
- Adicione 2 sessões semanais de fortalecimento: agachamentos (3 séries de 15), afundo (3 séries de 12 por perna), panturrilha em degrau (3 séries de 20)

**Semanas 5–6: Simulação de Trilha**
- 1 saída longa por semana (3–4 horas) em parque ou área com verde
- Comece a usar a mochila com carga progressiva: semana 5 com 4 kg, semana 6 com 6 kg
- 2 sessões semanais de musculação com foco em posterior de coxa e glúteo

**Semanas 7–8: Trilhas Curtas de Teste**
- Faça 1 a 2 trilhas reais de 6 a 10 km com desnível de 200–400m
- Use todo o equipamento que vai usar nas trilhas maiores (calçado, mochila, roupas)
- Avalie o que dói, o que cansa primeiro e ajuste o plano para os próximos meses

## Exercícios Prioritários Para Trilheiros

Se você só tiver tempo para um treino de força por semana, esses cinco exercícios cobrem o essencial:

**Agachamento búlgaro:** simula o movimento de subida em terreno irregular com foco em quadríceps e glúteo. 3 séries de 12 por perna.

**Step-up em degrau alto com carga:** sobe e desce de uma cadeira firme ou degrau de 40–50cm com peso nas mãos. Perfeito para simular subida em terreno.

**Afundo com passada:** fortalece posterior de coxa e glúteo, importantes na descida. 3 séries de 12 por perna.

**Elevação de panturrilha em degrau:** pé em degrau, sobe e desce o calcanhar amplitude máxima. Previne câimbras e fortalece para terreno irregular. 3 séries de 20.

**Prancha com variações:** core forte protege a lombar com mochila pesada. Prancha frontal, lateral e variação de movimento rotacional. 3 séries de 30–45 segundos.

## A Importância do Treinamento de Descida

A descida é onde ocorrem a maioria das lesões em trilhas — e paradoxalmente é o aspecto menos treinado pelos trilheiros iniciantes. Subir cansa; descer machuca.

Para treinar descida especificamente: inclua corridas e caminhadas em declive no seu programa. Se você mora em cidade plana, escadas são um substituto funcional. Desça escadas com controle, não rapidamente, absorvendo o impacto com a musculatura, não com o joelho.

Bastões de trekking reduzem significativamente o impacto nos joelhos na descida — em trilhas com muito desnível, reduzem em até 25% a carga articular. Se você tem qualquer histórico de dor nos joelhos, bastões são equipamento, não acessório.

## Hidratação e Nutrição no Treinamento

O preparo físico para trekking inclui treinar a estratégia de hidratação e nutrição, não apenas o corpo. Treinar em jejum ou sem hidratação adequada compromete a adaptação e aumenta o risco de lesão.

Duranta as sessões longas de simulação (semanas 5 a 8), pratique beber de forma proativa a cada 20 minutos e leve comida para comer a cada 60 a 90 minutos de atividade. Isso treina o hábito antes da trilha real.

Para saber mais sobre nutrição e hidratação em campo, leia nosso guia de [hidratação em trilha: quantos litros levar](/blog/hidratacao-trilha-quantos-litros) e, quando estiver pronto para sua primeira saída, confira [como escolher a trilha certa para o seu nível](/blog/como-escolher-trilha-segura-brasil)."""

# A19 - trilhas-nordeste-brasil (id=28, 85w -> 1000w)
expansions[28] = """O Nordeste brasileiro carrega um estigma injusto quando o assunto é trekking: a região é conhecida pelas praias e pela gastronomia, mas raramente é o primeiro destino que vem à cabeça de um trilheiro sério. Isso é um erro que as gerações de trilheiros mais jovens estão corrigindo rapidamente. A região tem destinos de trekking de nível mundial — da maior cachoeira livre do Brasil ao sítio arqueológico mais importante da América do Sul — e uma vantagem climática que o Sudeste não consegue replicar: sol garantido durante meses.

## Chapada Diamantina — Bahia: O Coração do Trekking Nordestino

A Chapada Diamantina é o destino de trekking mais completo do Nordeste e um dos melhores do Brasil. Localizada no centro da Bahia, a região concentra cachoeiras espetaculares, grutas, morros com vista panorâmica e uma das trilhas de longo curso mais belas do Brasil — a Travessia do Vale do Pati.

**[Morro do Pai Inácio](/trilha/morro-do-pai-inacio):** o mirante mais icônico da Chapada, com vista de 360° para o plateau de arenito. Trilha de 3 km moderada — ideal como primeiro destino em Lençóis.

**[Cachoeira da Fumaça](/trilha/cachoeira-da-fumaca):** a maior cachoeira de queda livre do Brasil (340m), com o efeito visual da água sendo empurrada de volta pelo vento. Acessível pela trilha do mirante superior (12 km moderado) ou pela trilha da base (mais longa e exigente).

**Travessia do Vale do Pati:** 55 km em 4–5 dias pelo vale mais remoto da Chapada. Exige guia credenciado, excelente condicionamento e equipamento de camping. Considerada por muitos a trilha mais bela do Brasil.

**Melhor época:** junho a novembro (seco, cachoeiras cheias das chuvas de março a maio).

## Lençóis Maranhenses — Maranhão: Paisagem Lunar com Lagoas

Os Lençóis Maranhenses são um fenômeno geográfico único no planeta: 155.000 hectares de dunas brancas cortadas por lagoas de água doce de cor turquesa formadas pelas chuvas de dezembro a maio.

A [Travessia dos Lençóis Maranhenses](/trilha/travessia-lencois-maranhenses) — de Atins até Barreirinhas ou vice-versa, passando pela área central das dunas — é uma das experiências de trekking mais singulares do Brasil. O percurso tem entre 3 e 5 dias, dependendo da rota escolhida, com pernoite em vilarejos de pescadores ao longo do caminho.

**Quando ir:** julho e agosto, quando as lagoas estão cheias das chuvas e o sol já garantido. Fora dessa janela, as lagoas somem e o que resta é areia quente.

**Guia obrigatório:** a desorientação nas dunas é real — sem referências visuais fixas, as dunas se parecem idênticas em todas as direções.

## Serra da Capivara — Piauí: Trekking com 40.000 Anos de História

O Parque Nacional da Serra da Capivara, no sudeste do Piauí, é o sítio arqueológico mais importante da América do Sul — com mais de 1.100 sítios arqueológicos catalogados e pinturas rupestres de até 40.000 anos, que desafiam as teorias convencionais sobre a chegada do ser humano às Américas.

As trilhas do parque percorrem cânions de arenito vermelho com paredes cobertas de pinturas rupestres de figuras humanas, animais e cenas do cotidiano pré-histórico. É uma experiência que mistura trekking e arqueologia de forma única.

**Trilha do Baixão da Pedra Furada:** 6 km com visita a múltiplos sítios arqueológicos. Guia obrigatório — é ele que sabe identificar e contextualizar as pinturas.

**Melhor época:** abril a setembro (clima seco, temperatura ainda tolerável pela manhã).

## Fernando de Noronha — Pernambuco: Trilhas no Paraíso

Fernando de Noronha tem uma das poucas oportunidades de trekking em ilha oceânica do Brasil. A [Trilha da Baía do Sancho](/trilha/fernando-de-noronha-baia-do-sancho), que desce por escadas e tunnels na rocha até o que é frequentemente eleita a mais bela praia do Brasil, é curta (3 km) mas memorável.

O Pico dos Dois Irmãos (321m) tem trilha de 4 km com uma das melhores vistas do arquipélago, incluindo a visão simultânea do Mar de Dentro e do Mar de Fora.

**Nota:** Noronha exige TPA (Taxa de Preservação Ambiental) e reserva de hospedagem com muito antecedência — especialmente em alta temporada (dezembro a fevereiro).

## Lençóis de Paracuru — Ceará: Dunas e Mar

Os [Lençóis de Paracuru](/trilha/lencois-de-paracuru), no Ceará, são uma versão menor e mais acessível dos Lençóis Maranhenses. A trilha de dunas e lagoas entre Paracuru e Trairi tem 30 km e pode ser feita em 2 dias, com hospedagem em pousadas rústicas ao longo do caminho.

**Melhor época:** fevereiro a maio (lagoas cheias) ou julho e agosto (ventos alisos, clima perfeito).

## Dicas Práticas Para Trekking no Nordeste

**Calor é o principal desafio:** em destinos como Serra da Capivara e Lençóis Maranhenses, a temperatura passa de 35°C facilmente. Saia antes das 7h, volte antes das 11h e retome após as 16h.

**Hidratação redobrada:** no Nordeste, a necessidade de água é consideravelmente maior do que em trilhas do Sudeste. Calcule no mínimo 1 litro por hora de caminhada em dias quentes.

**Guias locais são fundamentais:** o conhecimento do território, das condições e da logística local que esses profissionais têm é insubstituível em destinos remotos como os Lençóis Maranhenses e a Serra da Capivara.

Para saber a melhor janela climática para cada destino nordestino, consulte nosso guia completo sobre [a melhor época para trilhas no Brasil](/blog/melhor-epoca-trilhas-brasil). E para começar a planejar, leia nosso guia de [como escolher uma trilha segura](/blog/como-escolher-trilha-segura-brasil)."""

# A20 - trilhas-faceis-rio-de-janeiro (id=11, 87w -> 1000w)
expansions[11] = """O Rio de Janeiro é uma das poucas metrópoles do mundo onde você pode sair de casa de metrô, percorrer trilhas de mata atlântica com fauna exuberante e ainda ter vista para o oceano — tudo no mesmo dia. O Parque Nacional da Tijuca, a maior floresta urbana do planeta, fica inteiramente dentro dos limites da cidade e oferece dezenas de trilhas para todos os níveis de experiência.

Mas o Rio não se resume à Tijuca. O estado tem uma das maiores concentrações de trilhas por quilômetro quadrado do Brasil, com opções que vão da caminhada urbana ao trekking técnico em altitude.

## Parque Nacional da Tijuca — O Pulmão do Rio

O Parque Nacional da Tijuca é o ponto de partida perfeito para trilheiros cariocas e visitantes. Com 3.960 hectares de Mata Atlântica no coração da maior metrópole do hemisfério sul, o parque tem sinalização bem mantida, rotas para todos os níveis e pontos de referência famosos no horizonte.

**Pico da Tijuca (1.021m):** a trilha mais clássica do parque. São 4 km ida e volta com desnível de 400m — moderado para qualquer pessoa com algum condicionamento. No topo, vista de 360° com a cidade ao fundo e o Atlântico no horizonte. Acesso pela entrada do Alto da Boa Vista.

**Cascatinha de Taunay:** 1,5 km fácil, adequada para crianças e idosos. Uma das cachoeiras mais acessíveis do parque, com sombra e frescor ao longo do caminho.

**Pedra da Gávea:** trilha mais difícil do parque — 9 km com desnível de 840m, com trechos de escalada e exposição ao vazio que exigem boa condição física e nada de vertigem. Apenas para trilheiros experientes.

**Horário:** o parque abre às 8h. Chegar cedo garante estacionamento e evita o calor do meio-dia.

## Pedra Bonita e Pedra da Gávea — São Conrado

A [Pedra Bonita](/trilha/pedra-do-bau) é o ponto de partida dos voos de asa-delta e parapente mais famosos do Brasil — mas também tem uma trilha de acesso excelente para pedestres.

**Trilha da Pedra Bonita:** 2,5 km ida e volta, fácil a moderada, com desnível de 220m. No topo, vista para a Pedra da Gávea, São Conrado e o Oceano Atlântico. Acessível de metrô até a estação São Conrado + táxi ou Uber.

## Serra dos Órgãos — Teresópolis e Petrópolis

A menos de 2 horas da capital, o Parque Nacional da Serra dos Órgãos concentra algumas das trilhas mais espetaculares do Brasil — e diversas opções fáceis para quem está começando.

**Trilha da Pedra do Sino (1.692m):** não é fácil — são 14 km com 1.400m de desnível — mas é uma das trilhas mais clássicas do estado para trilheiros intermediários a avançados. A vista do topo inclui as formações rochosas características da Serra dos Órgãos.

**Gruta do Inferno e Mirante das Andorinhas:** trilha de 4 km fácil na sede de Petrópolis do parque. Adequada para iniciantes e famílias.

**[Pedra do Sino](/trilha/pedra-do-sino-serra-dos-orgaos):** inclusa em nossas trilhas catalogadas, é uma referência para trilheiros do Rio.

## Morro Dois Irmãos — Vidigal

O [Morro Dois Irmãos](/trilha/morro-dois-irmaos) é possivelmente a trilha urbana mais icônica do Brasil. A caminhada começa na favela do Vidigal e sobe até o topo dos dois morros com a melhor vista da zona sul do Rio — Ipanema, Leblon, Lagoa Rodrigo de Freitas e o Pão de Açúcar no horizonte.

**Distância:** 4 km ida e volta | **Desnível:** 450m | **Dificuldade:** moderado

**Como acessar:** subida de van ou moto-táxi até o topo do Vidigal (necessário pedir aos moradores), depois caminhada de 1 hora até o mirante. Grupos organizados com guias locais do Vidigal oferecem a experiência com toda a contextualização da comunidade.

## Parque Estadual da Pedra Branca

Menor visitado que a Tijuca mas maior em área (12.500 ha vs 3.960 ha), o Parque Estadual da Pedra Branca fica na Zona Oeste do Rio e oferece ambiente de mata atlântica mais denso e menos urbanizado.

**Pico da Pedra Branca (1.025m):** ponto culminante da cidade do Rio de Janeiro. A trilha tem 8 km ida e volta com desnível de 700m — desafiadora mas recompensadora com vista que poucos cariocas já tiveram.

## Trilhas da Região dos Lagos

A Região dos Lagos — Arraial do Cabo, Cabo Frio, Búzios — tem trilhas costeiras de mata de restinga com vista para o oceano que são excelentes para iniciantes.

**Ponta do Atalaia (Arraial do Cabo):** 3 km fácil com vista para o azul impossível do Mar das Agulhas e a Ilha do Caboclo.

**Trilha da Praia do Forno:** 2 km de restinga chegando a uma praia isolada acessível apenas a pé. Fácil, perfeita para o final da tarde.

## Dicas Práticas Para Trilhas no Rio

**Horário:** saia antes das 8h. O calor carioca depois das 10h transforma trilhas moderadas em experiências extenuantes — especialmente no verão.

**Segurança:** nos parques da Tijuca e Pedra Branca, siga sempre as trilhas sinalizadas e, preferencialmente, vá em grupo. Trilhas mais remotas dentro do parque têm histórico de assaltos eventuais — evite celular na mão.

**Reserva:** o Parque Nacional da Serra dos Órgãos exige reserva pelo ICMBio para a maioria das trilhas. O Parque Nacional da Tijuca tem acesso livre na maioria dos setores.

Para mais informações sobre equipamentos e segurança, consulte nosso guia dos [10 itens essenciais para trilha](/blog/10-itens-essenciais-mochila-trekking) e, se quiser avançar para a trilha mais clássica do Rio, leia nosso guia completo da [Travessia Petrópolis x Teresópolis](/blog/travessia-petropolis-teresopolis-guia-completo)."""

# A21 - kit-primeiros-socorros-trilha (id=12, 88w -> 1000w)
expansions[12] = """De todos os itens da mochila de um trilheiro, o kit de primeiros socorros é o que mais pessoas levam por obrigação e menos pessoas sabem usar. Um kit de R$ 80 com os itens certos pode ser a diferença entre uma lesão menor tratada no campo e uma emergência que exige resgate. Este guia vai te ajudar a montar um kit funcional e entender para que serve cada item.

Antes de listar os itens, um princípio fundamental: kit de primeiros socorros sem treinamento básico tem valor limitado. Considere fazer um curso básico de primeiros socorros — a Cruz Vermelha, o SAMU e diversas associações de montanhismo oferecem cursos de 8 a 16 horas que ensinam o que realmente precisa ser feito em campo.

## Os Itens Essenciais Por Categoria

### Controle de Sangramento

**Gaze estéril (pelo menos 4 unidades de 7,5×7,5cm):** para cobrir feridas abertas, absorver sangramento e proteger de contaminação.

**Atadura de crepe (2 rolos de 5cm e 1 de 10cm):** para fixar a gaze, imobilizar articulações entorcidas e criar compressão.

**Esparadrapo de tecido (1 rolo):** mais versátil que o de plástico, adere melhor em pele úmida ou suada.

**Curativo adesivo variado (10 a 15 unidades):** para ferimentos pequenos e bolhas. Inclua curativos menores e maiores.

**Fita de compressão ou hemostático (opcional, mas valioso):** para cortes profundos com sangramento intenso. Produtos como o QuikClot são usados em campo por paramédicos e valem o investimento para trilhas remotas.

### Antissépticos e Limpeza de Feridas

**Soro fisiológico 0,9% (ampola de 10ml, pelo menos 3):** para lavar feridas e limpar olhos. Mais seguro do que água de torneira ou de rio para limpeza de ferimentos.

**Povidona-iodo (iodopovidona, sachês unitários):** antisséptico tópico para aplicar após a limpeza da ferida. Evite álcool — irrita tecido e retarda a cicatrização.

**Gaze não aderente:** para colocar sobre feridas abertas antes da gaze absorvente — evita que a gaze cole no tecido em regeneração.

### Dor, Inflamação e Reações Alérgicas

**Ibuprofeno ou dipirona (comprimidos):** para dor muscular, dor de cabeça (frequentemente sinal de desidratação), entorses e febre.

**Anti-histamínico (loratadina ou cetirizina):** para reações alérgicas leves a picadas de insetos ou plantas.

**Antidiarreico (loperamida):** diarreia em campo causa desidratação rápida — ter o medicamento pode evitar uma evacuação de emergência.

**Sal de reidratação oral (2 a 3 sachês):** para repor eletrólitos em casos de diarreia, vômito ou desidratação intensa.

### Imobilização de Articulações

**Bandagem elástica autoadesiva (Coban ou similar):** para imobilizar tornozelos entorcidos sem apertar excessivamente. Levíssima e não precisa de pino ou clipe.

**Fita silver tape (30cm dobrados):** um dos itens mais versáteis da mochila. Serve para fixar bandagens, improvisar talas, reparar equipamento, evitar bolhas preventivamente.

**Improviso de tala:** em caso de suspeita de fratura, imobilize com o que tiver — galhos firmes, bastões de trekking, rolo de revista — antes de evacuar.

### Ferramenta e Equipamento

**Tesoura de ponta romba:** para cortar curativos, roupas e bandagens sem risco. Indispensável.

**Pinça de pontas finas:** para remoção de farpas, espinhos e — principalmente — carrapatos. A pinça é o método mais seguro de remoção de carrapatos.

**Termômetro clínico digital:** febre acima de 39°C com outros sintomas (dor de cabeça intensa, manchas na pele) após exposição a carrapatos pode indicar febre maculosa — busque atendimento médico imediatamente.

**Luvas de procedimento (3 pares):** para proteger quem presta o socorro de contato com sangue ou fluidos corporais.

**Manta aluminizada de emergência:** pesa apenas 80g e pode salvar alguém em hipotermia. A manta reflete o calor corporal de volta e cria barreira contra vento e chuva.

## Como Organizar o Kit

Use uma bolsa impermeável com zíper. Organize por categorias em saquinhos ziplock menores: "curativos", "medicamentos", "ferramentas". Isso permite encontrar o que precisa em segundos, mesmo no escuro ou sob pressão.

Escreva na tampa ou em um cartão dentro do kit: nome de cada medicamento, dose e indicação. Em situação de stress, a memória falha.

## Tamanho do Kit Por Tipo de Trilha

**Trilha de 1 dia simples (até 8 km, área frequentada):**
Kit compacto — curativos, gaze, esparadrapo, soro fisiológico, ibuprofeno, anti-histamínico, pinça, luvas. Cabe em bolsa de 200ml e pesa menos de 200g.

**Trilha de 1 dia desafiadora (desnível, área remota):**
Kit intermediário — tudo acima + atadura de crepe, manta aluminizada, sal de reidratação, antidiarreico, fita silver tape.

**Trilhas de múltiplos dias:**
Kit completo — todos os itens listados neste guia + medicamentos para condições pessoais específicas (alergia severa, diabetes, hipertensão).

## O Que Fazer em Situações Comuns

**Entorse de tornozelo:** aplique gelo se disponível, envolva com bandagem elástica em compressão moderada (não apertada), eleve o pé durante o descanso. Se a pessoa não consegue apoiar peso no tornozelo, suspeite de fratura e organize evacuação.

**Corte profundo com sangramento:** compressão direta com gaze por pelo menos 10 minutos sem tirar para ver. Se o sangue atravessar a gaze, adicione mais gaze por cima sem remover a de baixo. Se o sangramento não parar após 15 a 20 minutos, evacue.

**Picada de cobra:** imobilize o membro, mantenha abaixo do nível do coração, remova anéis e pulseiras, não faça torniquete nem tente sugar o veneno. Busque atendimento médico o mais rápido possível.

Para complementar o kit com conhecimento de campo, leia nosso guia sobre [animais perigosos nas trilhas brasileiras](/blog/animais-perigosos-trilhas-brasil) e as [regras de segurança que todo trilheiro precisa conhecer](/blog/seguranca-trilha-regras)."""

# A22 - melhores-trilhas-rs-canyons (id=26, 88w -> 1000w)
expansions[26] = """O Rio Grande do Sul é um dos estados mais subestimados do Brasil para trekking — e quem o conhece tende a voltar. A combinação de cânions espetaculares no planalto, campos de altitude com flora única, florestas de araucária e a infraestrutura turística desenvolvida da Serra Gaúcha cria um conjunto difícil de superar. E o estado tem uma vantagem logística real: está a 1 hora de voo de São Paulo e a 2 horas do Rio, com voos diretos para Porto Alegre e Caxias do Sul.

Neste guia, apresento os melhores destinos de trekking do Rio Grande do Sul, com foco nos cânions do Planalto das Araucárias e nas trilhas de múltiplos dias disponíveis.

## Cânion Itaimbezinho — A Jóia do Sul

O [Cânion Itaimbezinho](/trilha/canion-itaimbezinho), no Parque Nacional de Aparados da Serra, é o destino mais emblemático do trekking gaúcho. Sua fenda de 5,8 km de comprimento — com paredes de basalto colunar que chegam a 720 metros — é uma das formações geológicas mais impressionantes do continente.

**Trilha do Cotovelo:** 2,4 km ida e volta ao primeiro mirante. Fácil, com desnível mínimo, adequada para todas as idades. A vista da fenda do cânion já a partir desse ponto é suficiente para justificar a viagem.

**Trilha do Vértice:** 6 km circular com múltiplos mirantes ao longo do paredão. Moderada, desnível de 200m. Recomendada para grupos com algum condicionamento.

**A trilha da base (interior do cânion):** acessível pelo lado catarinense em Praia Grande (SC), a trilha de 21 km até a base das cachoeiras é uma das mais exigentes do Sul — exige guia e ótimo condicionamento físico.

**Reserva:** obrigatória pelo ICMBio. A demanda é alta nos fins de semana — reserve com 2 a 3 semanas de antecedência. A [Trilha do Cotovelo e Vértice](/trilha/trilha-cotovelo-vertice-itaimbezinho-cambara-do-sul-rs) está em nosso catálogo de trilhas com informações completas de acesso.

## Cânion Fortaleza — Maior Profundidade do Brasil

O [Cânion Fortaleza](/trilha/canion-fortaleza), a 30 km do Itaimbezinho, supera o vizinho em profundidade: 900 metros de paredão em alguns pontos. Tecnicamente, é o maior cânion em profundidade do Brasil.

A trilha principal tem 8 km ida e volta com vista para a Cachoeira do Tigre Preto — queda d'água de 800 metros em queda livre, das mais altas do Brasil.

O Fortaleza é menos visitado que o Itaimbezinho, o que garante uma experiência mais tranquila e a sensação de maior isolamento. Em dias claros, a visibilidade a partir do mirante chega a dezenas de quilômetros.

**Dica:** o pôr do sol no Cânion Fortaleza, quando o sol poente tinge os paredões de basalto em tons de laranja, é uma das experiências visuais mais marcantes do Sul.

## Cambará do Sul: A Base Logística dos Cânions

Cambará do Sul é o município gaúcho mais próximo dos cânions e a base logística natural para qualquer visita. A cidade tem infraestrutura completa para trilheiros: pousadas, camping, restaurantes e guias locais credenciados.

Os guias de Cambará do Sul conhecem os cânions como ninguém — inclusive rotas alternativas, condições sazonais e os melhores horários para fotografia. Vale contratar especialmente para a trilha da base do Itaimbezinho.

## Serra Gaúcha: Trilhas com Vista para os Vales

A Serra Gaúcha — região de imigração italiana e alemã com Gramado, Canela e São Francisco de Paula — tem trilhas com caráter completamente diferente dos cânions basálticos.

**Parque do Caracol (Canela):** a Cascata do Caracol (131m de queda) é a principal atração, mas o parque tem 9 km de trilhas bem sinalizadas pela mata de araucárias. Adequado para iniciantes e famílias.

**Trilha da Ferradura (Gramado):** percurso de 8 km em formato de ferradura pelo Vale dos Vinhedos e mirantes sobre o Vale do Rio das Antas. Vista clássica da Serra Gaúcha com cantinas e vinícolas no percurso.

**Morro Pelado (São Francisco de Paula):** 12 km com desnível de 600m, vista panorâmica do Planalto das Araucárias. Trilha pouco frequentada que oferece uma perspectiva diferente da Serra.

## Parque Estadual do Tainhas

O Parque Estadual do Tainhas, em São Francisco de Paula, é uma das últimas florestas de araucária primárias do Rio Grande do Sul. As trilhas do parque (10 a 15 km, moderadas) passam por ervais nativos, araucárias centenárias e córregos de água cristalina.

O parque é muito menos visitado que os cânions — perfeito para quem quer experiência de natureza sem multidão.

## Quando Visitar o Rio Grande do Sul

**Setembro a março:** primavera e verão gaúcho — temperatura agradável, dias longos, campos floridos. Melhor período para cânions e trilhas de altitude.

**Junho e julho:** o inverno gaúcho pode trazer geada e temperatura negativa nos cânions, criando paisagens de neblina e gelo únicas — mas as trilhas ficam escorregadias e a neblina pode fechar os mirantes por dias. Apenas para trilheiros experientes e bem equipados para frio.

**Evitar:** períodos com chuva intensa (especialmente novembro e dezembro), quando os cânions ficam com neblina densa e as trilhas molhadas.

## Como Chegar e Se Deslocar

**De avião:** voo para Porto Alegre ou Caxias do Sul, depois carro alugado. Cambará do Sul fica a 210 km de Porto Alegre pela RS-235, com trechos de estrada de campo no final.

**De ônibus:** há linhas de Porto Alegre para Cambará do Sul, com algumas saídas diárias — verifique horários atualizados nas rodoviárias.

**Aluguel de carro:** necessário para acessar o Cânion Fortaleza e o Parque Estadual do Tainhas, que não têm transporte público.

Para mais trilhas no Sul do Brasil, confira nosso guia de [trilhas em Santa Catarina](/blog/trilhas-santa-catarina) — especialmente o Cânion Itaimbezinho pelo lado catarinense. E, se planeja visitar no inverno, não deixe de ler sobre [a melhor época para trilhas em cada região](/blog/melhor-epoca-trilhas-brasil)."""

print("Batch 5 expansions defined.")

for post in data:
    if post['id'] in expansions:
        post['content'] = expansions[post['id']]

with open('data/blog.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Batch 5 written to blog.json")

for post in data:
    if post['id'] in expansions:
        words = len(post['content'].split())
        print(f"ID {post['id']} | {words}w | {post['slug']}")
