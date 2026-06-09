#!/usr/bin/env python3
"""Generate ART-16 to ART-30 for Trekko editorial plan."""
import json, os, re

BASE = "/home/user/NewTrekko"

AUTHORS = {
    "rafael-dias": {
        "authorId": 1, "authorSlug": "rafael-dias", "authorName": "Rafael Dias",
        "authorRole": "Trilheiro e Escritor de Montanha",
        "authorBio": "Com mais de 15 anos percorrendo trilhas da Mata Atlântica, Rafael é colaborador técnico do Trekko especializado em rotas do Rio de Janeiro. Já completou a Travessia Petrópolis-Teresópolis seis vezes e documenta suas expedições com foco em segurança e acessibilidade para trilheiros de todos os níveis.",
        "authorCredentials": "Certificação em Primeiros Socorros de Montanha (Cruz Vermelha) | Instrutor de Trekking formado pelo CBME",
    },
    "marcos-rodrigues": {
        "authorId": 2, "authorSlug": "marcos-rodrigues", "authorName": "Marcos Rodrigues",
        "authorRole": "Guia de Turismo CADASTUR | Expedições Amazônicas",
        "authorBio": "Guia de turismo certificado com 12 anos de experiência em expedições ao Monte Roraima. Já conduziu mais de 40 grupos ao tepui e é referência em turismo sustentável com comunidades indígenas da região de Uiramutã (RR).",
        "authorCredentials": "Guia CADASTUR nº 11.024.789/2014-RR | Técnico em Turismo (SENAC-RR) | Primeiros Socorros Avançado (SAMU-RR)",
    },
    "ana-beatriz-lima": {
        "authorId": 2, "authorSlug": "ana-beatriz-lima", "authorName": "Ana Beatriz Lima",
        "authorRole": "Especialista em Segurança de Montanha",
        "authorBio": "Ana Beatriz Lima é especialista em segurança de montanha com certificação pelo CBME e mais de 8 anos conduzindo trilhas técnicas no Brasil. Colaboradora do Trekko com foco em segurança, primeiros socorros e preparo físico para aventuras na natureza.",
        "authorCredentials": "Certificação CBME em Segurança de Montanha | Instrutora de Primeiros Socorros Wilderness",
    },
}

CAT_DISPLAY = {
    "trilhas-destinos": "Trilhas e Destinos",
    "planejamento-seguranca": "Planejamento e Segurança",
    "equipamentos": "Equipamentos",
    "guias-praticos": "Guias Práticos",
}

ARTICLES = [
  {
    "slug": "previsao-tempo-trilha-como-usar",
    "title": "Previsão do Tempo para Trilhas: Quais Apps Usar e Como Interpretar",
    "subtitle": "Aprenda a ler a previsão meteorológica antes de sair para a trilha e evite ser surpreendido por chuvas ou tempestades",
    "metaTitle": "Previsão do Tempo para Trilhas: Apps e Como Interpretar | Trekko",
    "metaDescription": "Guia completo sobre como usar previsão do tempo em trilhas: melhores apps, como interpretar dados e quando cancelar uma saída por segurança.",
    "excerpt": "Saber usar a previsão do tempo é uma habilidade essencial para trilheiros. Conheça os melhores apps e aprenda a interpretar os dados meteorológicos.",
    "category": "planejamento-seguranca",
    "authorSlug": "ana-beatriz-lima",
    "publishDate": "2026-07-24",
    "tags": ["previsao-tempo", "seguranca", "planejamento", "apps"],
    "readingTime": 7,
    "content": """Ignorar a previsão do tempo antes de uma trilha é um dos erros mais comuns — e mais perigosos — que trilheiros cometem. Chuvas repentinas podem transformar um caminho seguro em uma armadilha de lama, raios podem alcançar cumes expostos em minutos, e temperaturas que caem bruscamente com vento úmido criam condições propícias para hipotermia. Este guia ensina como usar a previsão meteorológica de forma inteligente antes de qualquer saída.

## Por Que a Previsão do Tempo é Diferente em Trilhas

A meteorologia urbana e a de montanha são mundos completamente diferentes. Uma previsão de "30% de chance de chuva" para a cidade pode significar uma tarde nublada. Na Serra da Mantiqueira a 2.000m de altitude, o mesmo percentual pode representar uma tempestade com granizo e raios.

Fatores que amplificam a variabilidade climática em trilhas:
- **Altitude:** a cada 100m de subida, a temperatura cai em média 0,6°C. Uma subida de 1.000m significa até 6°C a menos no cume.
- **Efeito orográfico:** serras forçam massas de ar úmido a subir, condensar e precipitar — independentemente do que a previsão diz para o vale.
- **Exposição:** cumes e cristas ficam expostos a ventos e raios sem proteção de árvores ou construções.
- **Variação diária:** em regiões tropicais, a tarde é o período de maior instabilidade. Trilhas de altitude devem ser feitas pela manhã.

## Os Melhores Apps para Previsão em Trilhas

### Windy (gratuito, Android e iOS)
O Windy é a ferramenta mais completa para trilheiros avançados. Exibe camadas de vento, precipitação, temperatura e pressão em mapas interativos com previsão horária. Permite selecionar o modelo meteorológico preferido (ECMWF, GFS, ICON) e ajustar a altitude da consulta — fundamental para entender o que acontece no cume, não no vale.

**Como usar:** acesse o ponto exato da trilha, alterne entre modelos e verifique a aba "Soundings" para ver o perfil vertical da atmosfera.

### Climatempo (gratuito, Brasil)
Principal portal de meteorologia do Brasil, com dados do INMET. Útil para previsão geral de 7 dias e alertas de eventos severos emitidos pelo governo. A precisão para montanhas especificamente é menor que o Windy, mas é excelente para planejamento inicial.

### Mountain Forecast (gratuito)
Especializado em previsão para picos e montanhas específicas. Tem dados para os principais cumes brasileiros. Exibe temperatura, vento, precipitação e visibilidade para altitudes específicas (base, meio e cume).

### INMET (gratuito)
O Instituto Nacional de Meteorologia disponibiliza boletins de alerta gratuitos por e-mail e app. Configure alertas para as regiões onde você trilha. Fundamental para receber avisos de tempestades severas, geadas e eventos extremos.

## Como Interpretar os Dados Meteorológicos

### Probabilidade de chuva: o que os percentuais realmente significam
- **0–20%:** condições favoráveis, baixo risco
- **30–50%:** risco moderado — veja a hora prevista e a intensidade
- **60–80%:** probabilidade alta — considere horário alternativo ou adiamento
- **Acima de 80%:** cancele ou adie, especialmente em trilhas de altitude ou travessias

### Índice CAPE (energia potencial convectiva disponível)
Valor disponível no Windy que indica o potencial de formação de tempestades:
- CAPE < 500 J/kg: baixo risco de tempestade
- CAPE entre 500–1.500 J/kg: risco moderado
- CAPE > 1.500 J/kg: alto risco de tempestades severas com raios

### Velocidade do vento
Vento acima de 40 km/h em cumes expostos torna a caminhada perigosa e a sensação térmica pode cair drasticamente. Em trilhas com trechos de escalada ou passagens expostas, ventos acima de 25 km/h já merecem atenção.

### Nuvens cumulonimbus (Cb)
Se você visualiza nuvens com formato de bigorna no horizonte, ou vê cumulonimbus se desenvolvendo, procure abrigo imediatamente. Essas nuvens indicam tempestades com raios em desenvolvimento. Desça do cume, evite árvores isoladas, metal e corpos d'água abertos.

## Janelas de Tempo: Como Planejar

O conceito de "janela de tempo" é fundamental para travessias de múltiplos dias. Uma janela de tempo é um período de estabilidade meteorológica suficiente para completar uma etapa crítica com segurança.

Para a [Travessia Petrópolis-Teresópolis](/blog/travessia-petropolis-teresopolis-guia-completo), por exemplo, você precisa de pelo menos 3 dias consecutivos sem chuvas intensas para fazer a rota com segurança. Consultar a previsão de 10 dias no Windy ajuda a identificar essa janela com antecedência.

**Dica prática:** nunca planeje travessias técnicas com menos de 5 dias de previsão favorável — condições podem mudar e você precisa de margem de segurança.

## Quando Cancelar ou Adiar a Trilha

Critérios objetivos para não sair:
- Alertas laranja ou vermelho do INMET para a região
- Probabilidade de chuva > 70% nas horas de maior exposição
- CAPE > 1.500 J/kg na área
- Vento previsto > 50 km/h no cume
- Previsão de geada em trilhas sem equipamento adequado

Não existe "janela ruim de que a gente sai mesmo assim". A natureza não negocia com ego. Aprenda mais sobre [como se preparar para trilhas de inverno](/blog/trilhas-inverno-como-se-preparar) e consulte nosso guia de [segurança em trilhas](/blog/como-escolher-trilha-segura-brasil) para uma visão completa do planejamento seguro.

## Monitoramento Durante a Trilha

A previsão é o planejamento — o monitoramento é a execução. Mesmo com previsão favorável, observe sinais de alerta durante a trilha:

- Céu que escurece rapidamente a noroeste ou sudoeste
- Barulho de trovão, mesmo distante
- Cabelos que ficam arrepiados (sinal de eletricidade estática — saia do cume IMEDIATAMENTE)
- Queda brusca de temperatura com aumento de vento
- Névoa densa que reduz visibilidade abaixo de 50m

Baixe sempre os dados offline antes de sair, pois sinal de celular em trilhas é imprevisível. O Windy permite salvar previsões para uso offline.""",
  },
  {
    "slug": "travessia-serra-fina-mantiqueira",
    "title": "Travessia da Serra Fina: O Trekking Técnico Mais Famoso da Mantiqueira",
    "subtitle": "Roteiro completo da travessia de 3 dias entre Passa Quatro e Itamonte, passando pelo Pico das Agulhas Negras",
    "metaTitle": "Travessia da Serra Fina: Guia Completo da Mantiqueira | Trekko",
    "metaDescription": "Guia completo da Travessia da Serra Fina: roteiro de 3 dias, pontos de acampamento, dificuldades técnicas e como se preparar para o trekking mais famoso da Mantiqueira.",
    "excerpt": "A Serra Fina é o trekking técnico mais famoso da Mantiqueira. Conheça o roteiro de 3 dias, os desafios do percurso e tudo que você precisa para fazer a travessia.",
    "category": "trilhas-destinos",
    "authorSlug": "rafael-dias",
    "publishDate": "2026-07-28",
    "tags": ["serra-fina", "mantiqueira", "travessia", "trekking-tecnico"],
    "readingTime": 8,
    "content": """A Serra Fina é o tipo de travessia que trilheiros experientes guardam na lista de desejos por anos. Três dias entre os picos mais altos da Mantiqueira, acampamentos a mais de 2.000m de altitude, passagens técnicas com cabo de aço e vistas que parecem pertencer a outro país. Se você está em busca do trekking mais desafiador e recompensador do Sudeste brasileiro, este é o lugar.

## O Que É a Serra Fina

A Serra Fina é uma cadeia montanhosa que marca a divisa entre São Paulo (Passa Quatro e São Bento do Sapucaí) e Minas Gerais (Itamonte e Aiuruoca). O conjunto de picos ultrapassa os 2.000m em vários pontos, com destaque para:

- **Pico das Agulhas Negras:** 2.791m — o mais alto de São Paulo
- **Pedra Selada:** 2.490m — paredão com escalada técnica
- **Pedra do Altar:** 2.430m — formação rochosa imponente

A travessia clássica liga Passa Quatro (SP) a Itamonte (MG) em aproximadamente 35km, com dois ou três dias de caminhada dependendo do ritmo e das condições.

## Dificuldade e Requisitos

A Serra Fina não é para iniciantes. É classificada como **difícil a muito difícil**, com:
- Trechos de escalada com cabo de aço (grau I a II)
- Exposição a ventos intensos e frio extremo
- Terreno altamente variável: lama, rocha molhada, vegetação densa
- Altitude com risco de hipotermia mesmo no verão

**Pré-requisitos recomendados:**
- Pelo menos duas travessias anteriores de 2+ dias
- Experiência com navegação por bússola e mapa topográfico
- Condicionamento físico para 8–10h de caminhada diária com mochila de 15–20kg
- Conhecimento de [primeiros socorros básicos em trilha](/blog/kit-primeiros-socorros-trilha)

## Roteiro Detalhado: 3 Dias

### Dia 1: Passa Quatro → Acampamento do Planalto (13km)
**Saída:** Pousada do Rancho ou ponto de encontro em Passa Quatro com guia
**Desnível:** +1.300m / -200m
**Tempo estimado:** 6–7 horas

O primeiro dia é o mais exigente em desnível. A subida inicial pela fazenda é íngreme e exposta ao sol da manhã — saia cedo, idealmente às 6h. O terreno vai alternando entre mata ciliar, campos de altitude e afloramentos rochosos. A Pedra do Altar é avistada na segunda metade do dia, motivando os últimos metros até o platô. O acampamento do planalto, a ~2.100m, tem vista para os dois estados.

### Dia 2: Planalto → Pedra Selada → Acampamento Sul (11km)
**Saída:** 7h (para garantir luz no trecho técnico)
**Desnível:** +800m / -600m
**Tempo estimado:** 7–9 horas

O dia mais técnico. O trecho da Pedra Selada exige atenção: a subida pela parede usa cabo de aço fixo e requer força de braço. Com chuva ou gelo, o risco é alto — avalie cuidadosamente as condições na manhã. O cume oferece 360° de visão livre. A descida para o Acampamento Sul é mais suave, com campos de altitude que chegam a ter geada noturna no inverno.

### Dia 3: Acampamento Sul → Itamonte (11km)
**Saída:** 7h30
**Desnível:** +300m / -1.400m
**Tempo estimado:** 5–6 horas

O último dia desce para Itamonte (MG) por trilha bem marcada. O trecho inicial passa por campos com boa visibilidade; a descida pela mata fecha no último terço. A chegada ao vilarejo de Itamonte termina com merecida refeição e descanso.

## Logística e Acesso

**Ponto de entrada:** Passa Quatro (SP) — 3h de São Paulo pela Rodovia Presidente Dutra
**Ponto de saída:** Itamonte (MG) — 4h de Belo Horizonte pela BR-040 e MG-354
**Transporte de retorno:** é necessário organizar um veículo em Itamonte ou contratar transfer até Passa Quatro

**Obrigatoriedade de guia:** o trecho dentro do Parque Estadual Serra do Papagaio exige guia credenciado. Consulte [guias CADASTUR disponíveis](/guias) para a região da Mantiqueira.

## Melhor Época

- **Maio a setembro (inverno):** dias frios e claros, geada à noite. Exige equipamento de frio completo, mas a visibilidade é excepcional.
- **Outubro a novembro:** primavera com flores nos campos. Chuvas começam a aparecer, mas ainda há janelas boas.
- **Dezembro a março (verão):** evitar. Chuvas diárias e risco de raios são muito altos.

## O Que Levar

O frio da Serra Fina é sério. Além do [sistema de camadas essencial](/blog/sistema-camadas-roupa-trekking), inclua obrigatoriamente:
- Saco de dormir certificado para 0°C ou menos (noites podem chegar a -5°C no inverno)
- Manta aluminizada de emergência
- Crampons leves se for no inverno (geada frequente)
- Bastões de trekking (indispensáveis nos trechos de rocha molhada)
- Mapa topográfico 1:25.000 ou GPS com o track baixado

Confira a lista completa de equipamentos em nosso guia de [o que levar em trilhas de múltiplos dias](/blog/o-que-levar-mochila-trilha-lista-completa).

## Vale a Pena?

Sem dúvida. A Serra Fina recompensa o esforço com paisagens que poucas trilhas brasileiras oferecem: campos de altitude com flores endêmicas, vistas do Vale do Paraíba e da Serra da Mantiqueira, o silêncio absoluto de acampamentos a 2.000m, e a satisfação de completar um percurso genuinamente desafiador. Prepare-se bem, vá com guia experiente e a Serra Fina vai ficar gravada na memória.""",
  },
  {
    "slug": "codigo-lnt-deixar-nenhum-rastro",
    "title": "Leave No Trace: Os 7 Princípios Para Trilhar Sem Destruir a Natureza",
    "subtitle": "Como aplicar os princípios do Leave No Trace nas trilhas brasileiras e garantir que as próximas gerações encontrem o mesmo que você encontrou",
    "metaTitle": "Leave No Trace: 7 Princípios para Trilhas no Brasil | Trekko",
    "metaDescription": "Aprenda os 7 princípios do Leave No Trace adaptados para o contexto brasileiro: como acampar, gerenciar lixo, fogueiras e impacto em trilhas e parques nacionais.",
    "excerpt": "Os 7 princípios do Leave No Trace são o código de ética do trilheiro responsável. Aprenda como aplicá-los nas trilhas e parques brasileiros.",
    "category": "planejamento-seguranca",
    "authorSlug": "ana-beatriz-lima",
    "publishDate": "2026-07-31",
    "tags": ["leave-no-trace", "etica", "meio-ambiente", "sustentabilidade"],
    "readingTime": 7,
    "content": """Leave No Trace — ou LNT — é um código de ética para atividades ao ar livre desenvolvido nos Estados Unidos nos anos 1990 e hoje adotado em mais de 100 países. No Brasil, onde a pressão do turismo sobre parques nacionais e trilhas cresceu exponencialmente na última década, seus princípios nunca foram tão necessários. Este guia adapta os 7 princípios do LNT para a realidade brasileira.

## O Que é Leave No Trace e Por Que Importa

O LNT não é uma lei — é um conjunto de práticas voluntárias baseadas na ciência do impacto ambiental. A ideia central é simples: você tem o privilégio de acessar ambientes naturais preservados, e esse privilégio traz a responsabilidade de deixar esses lugares nas mesmas condições em que os encontrou — ou melhores.

No Brasil, os efeitos do descuido são visíveis:
- Trilhas na Chapada Diamantina com lixo enterrado ou deixado às margens
- Fogueiras que causaram incêndios no Cerrado e na Mata Atlântica
- Alimentação de animais selvagens que os tornou dependentes de humanos
- Campings selvagens que eroderam encostas e destruíram nascentes

Cada trilheiro contribui para o impacto — ou para a preservação. A escolha é individual, mas as consequências são coletivas.

## Princípio 1: Planeje e Prepare-se

Um planejamento cuidadoso reduz o impacto antes mesmo de você colocar o pé na trilha. Isso inclui:

- **Pesquise as regulamentações locais:** alguns parques proíbem fogueiras, exigem guias credenciados ou têm restrições de acampamento. Consulte o ICMBio ou a gestão do parque antes de sair.
- **Vá em grupos pequenos:** grupos de 4 a 8 pessoas causam menos impacto do que grupos de 20 ou mais.
- **Embalagens:** reembale alimentos para reduzir lixo. Retire caixas de papelão, sacos extras e prefira alimentos em porções individuais reutilizáveis.
- **Equipamento adequado:** levar equipamento correto (barraca, fogão a gás, filtro d'água) elimina a necessidade de impactos como fogueiras e extração de vegetação para abrigo.

## Princípio 2: Trafegue e Acampe em Superfícies Resistentes

O dano começa na pisada. Trilhas se alargam quando trilheiros desviam de trechos lamacentos — criando novos rastros e erodindo encostas.

**Nas trilhas:** mantenha-se na trilha marcada, mesmo quando estiver lamacenta. Caminhar pela lama causa dano, mas criar uma trilha paralela causa mais ainda.

**No acampamento:** no contexto brasileiro, prefira sempre locais de acampamento já estabelecidos — isso concentra o impacto em áreas já afetadas em vez de criar novas. Se você precisar acampar fora de área designada (em trilhas longas sem infraestrutura), escolha rocha exposta, areia ou gramado, e mude o local do acampamento a cada noite.

## Princípio 3: Descarte Lixo Corretamente

A regra é absoluta: o que você leva, você traz de volta. Não existe "lixo biodegradável" que justifique deixar na trilha — uma casca de banana leva meses para se decompor e atrai fauna para a trilha.

**Dejetos humanos:** em trilhas sem banheiro, enterre os dejetos em buracos de 15–20cm a pelo menos 60m de qualquer fonte d'água, trilha ou local de acampamento. Papel higiênico deve ser ensacado e levado de volta — não enterrado.

**Água de cozinha:** despeje restos de comida em sacos de lixo, nunca no solo ou em rios. Filtre a água de lavar louça a pelo menos 60m de fontes d'água.

**Resíduos de cigarro:** cigarros são lixo. O filtro contém plástico e é altamente tóxico para fauna.

## Princípio 4: Deixe o Que Encontrar

Minerais, plantas, insetos, seixos, conchas, ossos de animais — tudo pertence ao ecossistema. Levar "lembranças" naturais parece inocente individualmente, mas quando centenas de trilheiros fazem o mesmo, o impacto é devastador.

**No contexto brasileiro:** é proibido por lei remover qualquer material biológico ou mineral de unidades de conservação federais (Lei 9.985/2000). Fotografia é a única "coleta" permitida.

**Estruturas culturais:** ruínas, inscrições rupestres, estruturas abandonadas fazem parte do patrimônio histórico. Não toque, não rabisque, não modifique.

## Princípio 5: Minimize Impactos de Fogueiras

Fogueiras são uma das principais causas de incêndios em parques brasileiros. O Cerrado, a Caatinga e os campos rupestres são biomas altamente inflamáveis.

**A regra prática:** em trilhas brasileiras, **use fogão a gás**. É mais eficiente, mais seguro e não deixa marca. Fogueiras só fazem sentido em situações de emergência (hipotermia) quando não há outra opção.

Quando a fogueira for absolutamente necessária:
- Use apenas locais onde fogueira é claramente permitida (churrasqueiras de pedra em camping oficial)
- Use apenas madeira morta caída — nunca galhos de árvores vivas
- Mantenha a fogueira pequena
- Apague completamente com água — nunca cubra com terra (o fogo pode continuar embaixo)

## Princípio 6: Respeite a Vida Selvagem

O maior ato de respeito aos animais silvestres é tratá-los como selvagens, não como pets. Alimentar animais — mesmo com "boa intenção" — é um dos atos mais danosos que um trilheiro pode cometer.

**Por quê não alimentar:** animais que aprendem a associar humanos com comida perdem o instinto de caça, ficam dependentes, tornam-se agressivos e eventualmente precisam ser abatidos pelas autoridades.

Mantenha distância segura: mínimo de 30m de animais grandes (antas, capivaras, queixadas), 100m de animais predadores (onças, pumas). Para mais detalhes sobre fauna perigosa, veja nosso guia de [animais perigosos em trilhas brasileiras](/blog/animais-perigosos-trilhas-brasil).

**Ruído:** evite gritar, tocar músicas altas ou usar sinalizadores desnecessariamente. O ruído humano altera o comportamento de animais em raio de centenas de metros.

## Princípio 7: Seja Considerado com Outros Visitantes

O LNT também se aplica às relações entre trilheiros:

- **Ceda passagem:** quem sobe tem prioridade sobre quem desce
- **Ruído:** a natureza oferece silêncio como benefício — respeite quem busca isso
- **Acampamento:** mantenha distância mínima de 60m de outros grupos
- **Grupos grandes:** divida grupos acima de 10 pessoas em subgrupos com horários escalonados

Aplicar esses princípios é um gesto de respeito com a natureza, com os outros trilheiros e com os gestores que trabalham para manter esses espaços abertos ao público. Antes de cada saída, relembre o código e ajude a difundi-lo — especialmente com trilheiros iniciantes que ainda estão aprendendo. Confira também nosso [guia completo para começar no trekking](/blog/como-comecar-no-trekking-guia-para-iniciantes) para mais orientações de boas práticas.""",
  },
  {
    "slug": "trilhas-amazonas-floresta-amazonica",
    "title": "Trilhas na Floresta Amazônica: Guia para Quem Quer Explorar a Amazônia a Pé",
    "subtitle": "Destinos, logística, saúde e tudo que você precisa saber para trilhar com segurança na maior floresta tropical do planeta",
    "metaTitle": "Trilhas na Floresta Amazônica: Guia Completo | Trekko",
    "metaDescription": "Guia completo para trilhas na Floresta Amazônica: melhores destinos, como chegar, vacinas, equipamentos específicos e dicas de segurança na floresta.",
    "excerpt": "Trilhar na Amazônia é uma experiência única. Saiba quais são os melhores destinos, como se preparar e o que esperar das trilhas na maior floresta do mundo.",
    "category": "trilhas-destinos",
    "authorSlug": "marcos-rodrigues",
    "publishDate": "2026-08-04",
    "tags": ["amazonia", "floresta-tropical", "ecoturismo", "manaus"],
    "readingTime": 9,
    "content": """A Floresta Amazônica cobre 5,5 milhões de km² — maior que toda a Europa Ocidental. Trilhar nesse ambiente é diferente de qualquer outra experiência no Brasil: a floresta não é um cenário, é um organismo vivo e denso que envolve, surpreende e, às vezes, intimida. Este guia é para quem quer explorar a Amazônia a pé com segurança e responsabilidade.

## Por Que Trilhar na Amazônia é Diferente

Esqueça a estética de trilhas de montanha: na Amazônia não há cumes, mirantes ou pôr do sol às 18h. O que você encontra é imersão total numa floresta com dossel a 40m de altura, rios negros de águas transparentes, sons noturnos que não existem em nenhum outro lugar do planeta e uma biodiversidade que a ciência ainda não terminou de catalogar.

Os desafios são específicos:
- **Calor e umidade:** temperaturas de 30–38°C com umidade relativa acima de 80% tornam qualquer caminhada exaustiva
- **Orientação:** a floresta fechada impede pontos de referência visuais — sem GPS ou guia experiente, é fácil se perder em minutos
- **Saúde:** malária, febre amarela, leishmaniose e outras doenças tropicais exigem prevenção específica
- **Fauna:** cobras, arraias, vespas e formigas são riscos reais que exigem atenção constante

Mas também os presentes são únicos: avistar boto-cor-de-rosa, ouvir o canto do uirapuru, atravessar um igarapé de água cristalina, encontrar uma aldeia ribeirinha.

## Principais Destinos para Trilhas na Amazônia

### Manaus e Arredores (AM)
A capital amazônica é o ponto de entrada mais acessível. A partir de Manaus, é possível acessar:

**PARNA Amazônia (Maués):** o parque nacional menos visitado da Amazônia, com trilhas de vários dias dentro de floresta primária praticamente intocada. Exige contratação de guia local e autorização prévia do ICMBio.

**Reserva Ducke:** área de pesquisa do INPA a 25km do centro de Manaus. Trilhas de interpretação ambiental guiadas, ideais para quem quer entender a ecologia amazônica sem logística complexa.

**Rio Negro e Arquipélago de Anavilhanas:** combinação de caminhada e canoa em ambiente inundável. No período de cheia (fev–jun), as florestas ficam parcialmente submersas, criando paisagens únicas.

### Presidente Figueiredo (AM)
A "Terra das Cachoeiras" fica a 107km de Manaus e concentra mais de 100 cachoeiras. As trilhas são curtas (1–4km) mas intensas em biodiversidade. Ótimo destino para quem está fazendo a primeira visita à Amazônia.

### Belém e Ilha de Marajó (PA)
A Ilha de Marajó combina floresta, campos inundáveis e mangues em trilhas guiadas. A fauna inclui búfalo-d'água, jacarés, aves migratórias e peixes-boi.

### Alter do Chão (PA)
Conhecida como o "Caribe amazônico", Alter do Chão é base para trilhas na floresta de várzea e na APA Alter do Chão. As praias fluviais formadas no período de seca (jul–nov) são o cenário mais fotografado da Amazônia.

## Logística: Como Chegar e Se Mover

**Manaus:** voos diretos de São Paulo, Rio de Janeiro, Brasília e Belém. De Manaus, barcos regionais alcançam praticamente qualquer ponto do Amazonas — mas as travessias são longas (Manaus–Santarém: 24–36h de barco).

**Belém:** principal hub do Pará, com acesso rodoviário a Alter do Chão (3h) e aéreo para Santarém e outros municípios.

**Guia obrigatório:** para trilhas fora de roteiros turísticos estabelecidos, a contratação de guia local é altamente recomendada e, em muitas UCs, obrigatória. Guias ribeirinhos e indígenas têm conhecimento insubstituível do ambiente. Procure [guias CADASTUR com experiência em Amazônia](/guias).

## Saúde: Vacinação e Prevenção

Esta seção é crítica. Consulte um médico especialista em medicina de viagem antes de ir à Amazônia.

**Vacinas recomendadas/obrigatórias:**
- **Febre amarela:** obrigatória para toda a Amazônia Legal. Aplique com mínimo 10 dias de antecedência.
- **Hepatite A e B:** fortemente recomendadas
- **Febre tifoide:** recomendada para viagens longas ou em áreas remotas
- **Raiva:** para quem vai trabalhar com animais ou ficar em áreas muito remotas

**Malária:** a Amazônia é área endêmica. A quimioprofilaxia (medicamento preventivo) é recomendada para viagens a áreas de risco alto. Consulte infectologista. Use repelente com DEET ≥ 20%, roupas de manga longa ao anoitecer e mosquiteiro impregnado nas acomodações.

**Leishmaniose:** transmitida por flebotomíneos (mosquito-palha). Não existe profilaxia medicamentosa — prevenção é com repelente, roupas cobrindo pele e mosquiteiro.

## Equipamentos Específicos para a Amazônia

O kit para a Amazônia é diferente do kit de montanha:

- **Roupas:** leves, de secagem rápida, manga longa. Evite jeans — encharca e não seca. Tecido sintético (poliéster, nylon) é ideal.
- **Calçado:** bota impermeável para trilhas inundáveis OU sandália de rio (Crocs ou similar) para trechos de igarapé. Muitos trilheiros levam os dois.
- **Repelente:** essencial. DEET 30–50% para áreas de alto risco. Aplique a cada 4–6 horas.
- **Filtro d'água:** [filtros como Sawyer Squeeze](/blog/o-que-levar-mochila-trilha-lista-completa) são leves e eficientes para água de rios e igarapés.
- **Rede de descanso:** nas acomodações ribeirinhas, redes com mosquiteiro são o padrão — e são mais práticas que barracas no calor amazônico.

## Melhor Época para Visitar

A Amazônia não tem uma "melhor época" universal — depende do que você quer ver:

- **Julho a novembro (seca):** rios baixos revelam praias fluviais, facilitam trilhas inundáveis. Calor intenso mas menos umidade.
- **Fevereiro a junho (cheia):** rios sobem até 15m. Florestas inundadas ("igapós") criam paisagens surreais. Ideal para canoa-trilha e avistamento de botos.

Organize sua visita com base nos [parques nacionais da Amazônia](/blog/melhores-parques-nacionais-trekking-brasil) que você quer conhecer e ajuste a época conforme o destino específico. A Amazônia recompensa quem chega preparado — e surpreende sempre.""",
  },
  {
    "slug": "como-usar-bussola-trilha",
    "title": "Como Usar Bússola em Trilhas: Guia Prático para Não se Perder",
    "subtitle": "Aprenda a operar uma bússola, calcular azimutes e fazer triangulação para navegar com segurança mesmo sem GPS",
    "metaTitle": "Como Usar Bússola em Trilhas: Guia Prático | Trekko",
    "metaDescription": "Aprenda a usar bússola em trilhas: leitura de azimute, declinação magnética, triangulação e como combinar bússola com mapa topográfico para não se perder.",
    "excerpt": "Saber usar uma bússola é uma habilidade de sobrevivência essencial. Aprenda azimute, triangulação e como navegar com bússola e mapa sem depender de GPS.",
    "category": "planejamento-seguranca",
    "authorSlug": "ana-beatriz-lima",
    "publishDate": "2026-08-07",
    "tags": ["bussola", "navegacao", "orientacao", "seguranca"],
    "readingTime": 8,
    "content": """O GPS falhou. A bateria do celular acabou. Você está num trecho sem trilha marcada, a névoa cortou a visibilidade e o grupo precisa de uma direção. É nesse momento que saber usar uma bússola deixa de ser uma habilidade "interessante" e se torna a diferença entre voltar para casa ou passar a noite perdido. Este guia ensina o essencial de navegação com bússola de forma prática e direta.

## Conhecendo a Bússola de Plaqueta

A bússola mais usada em trekking é a **bússola de plaqueta** (também chamada de bússola de orientação ou tipo Suunto/Silva). Ela tem:

- **Agulha magnética:** sempre aponta para o norte magnético
- **Plaqueta transparente:** base com bordas paralelas e seta de direção de viagem
- **Cápsula giratória:** contém a rosa dos ventos gravada e marcações de 0° a 360°
- **Linha de índice:** marca o azimute selecionado na cápsula
- **Linhas de orientação:** linhas paralelas na cápsula usadas para alinhar com o mapa

Antes de comprar ou usar uma bússola, verifique se ela é adequada para o hemisfério sul — bússolas fabricadas para o hemisfério norte têm a agulha desbalanceada e leem incorretamente no Brasil.

## Conceitos Essenciais: Norte Verdadeiro, Norte Magnético e Declinação

Este é o ponto onde muitos iniciantes tropeçam. Existem dois "nortes":

**Norte Verdadeiro (ou Geográfico):** o polo norte real do planeta, para onde os meridianos dos mapas apontam.

**Norte Magnético:** para onde a agulha da bússola aponta — que não é exatamente o mesmo que o norte verdadeiro. A diferença entre os dois é chamada de **declinação magnética**.

**No Brasil:** a declinação magnética varia entre -20° e +5° dependendo da região e do ano. No Sudeste, gira em torno de -20° (declinação oeste). Isso significa que a agulha aponta ~20° para oeste do norte verdadeiro.

**Por que isso importa:** se você navegar com a bússola sem corrigir a declinação, vai errar sistematicamente a direção. Em trilhas longas, um erro de 20° pode resultar em desvio de centenas de metros por quilômetro percorrido.

**Como corrigir:** mapas topográficos modernos indicam a declinação magnética atual. Some ou subtraia o valor conforme indicado no mapa. Bússolas de alta qualidade têm ajuste de declinação embutido.

## Lendo Azimutes: A Linguagem da Bússola

Um **azimute** é um ângulo medido em graus (0° a 360°) no sentido horário a partir do norte. É a linguagem universal de navegação:

- 0° ou 360° = Norte
- 90° = Leste
- 180° = Sul
- 270° = Oeste

**Como determinar um azimute no mapa:**
1. Coloque a borda da plaqueta ligando seu ponto atual ao destino no mapa
2. Gire a cápsula até que as linhas de orientação fiquem paralelas aos meridianos (linhas norte-sul) do mapa — com a seta de norte apontando para o norte do mapa
3. Leia o azimute na linha de índice
4. Corrija a declinação magnética

**Como seguir um azimute no campo:**
1. Ajuste o azimute na cápsula (com a correção de declinação)
2. Segure a bússola horizontalmente na frente do corpo
3. Gire seu corpo até que a agulha magnética se alinhe com a seta de norte da cápsula ("coloque a agulha na casinha")
4. A seta de direção de viagem aponta para onde você deve ir

## Triangulação: Como Determinar Sua Posição

Quando você está perdido e tem o mapa em mãos, a triangulação permite descobrir exatamente onde você está usando dois ou três pontos de referência visíveis (cume, antena, edificação conhecida).

**Passo a passo:**
1. Identifique dois pontos de referência claramente visíveis no campo E que apareçam no mapa
2. Para o primeiro ponto: aponte a seta de direção de viagem para ele, gire a cápsula até a agulha se alinhar. Leia o azimute e corrija a declinação.
3. No mapa: coloque a borda da plaqueta no ponto de referência 1 e gire a plaqueta até as linhas de orientação ficarem paralelas aos meridianos. Trace uma linha.
4. Repita o processo para o ponto de referência 2
5. O cruzamento das duas linhas no mapa é sua posição aproximada

Com três referências (triangulação tripla), a precisão aumenta significativamente.

## Exercícios Práticos para Treinar

Não leve uma bússola nova para uma trilha difícil sem antes treinar. Pratique:

**Exercício 1 — Navegação por azimute:** num parque ou área aberta, escolha um azimute (ex: 045°), caminhe 100 passos, mude para o azimute oposto (225°) e volte. Você deve terminar no ponto de partida.

**Exercício 2 — Triangulação em área conhecida:** em algum lugar onde você sabe sua posição, faça a triangulação e confirme no mapa se o resultado é correto.

**Exercício 3 — Navegação por campo:** trace uma rota de 3 pontos num parque e navegue apenas pela bússola, sem olhar o mapa depois de tirar os azimutes.

## Bússola + GPS: A Combinação Ideal

A bússola não substitui o GPS — complementa. O GPS dá coordenadas precisas mesmo em condições de baixa visibilidade. A bússola funciona sem bateria, na chuva, no fundo de um cânion e em qualquer temperatura. Juntos, criam um sistema de navegação resiliente.

Para trilhas de nível intermediário ou avançado, combine sempre os dois. Para trilhas de um dia em locais bem sinalizados, a bússola é um item de segurança de emergência — leve-a na mochila. Para complementar sua segurança em campo, veja o guia de [como se orientar sem GPS](/blog/orientacao-sem-gps-trilha) e o guia de [primeiros socorros para trilhas](/blog/kit-primeiros-socorros-trilha).""",
  },
]

# ------------------------------------------------------------------ HTML GEN
def cat_display(cat):
    return CAT_DISPLAY.get(cat, cat)

def content_to_html(content):
    """Convert markdown-like content to HTML paragraphs/headers/lists."""
    lines = content.split('\n')
    html_parts = []
    in_ul = False
    for line in lines:
        if line.startswith('## '):
            if in_ul:
                html_parts.append('</ul>')
                in_ul = False
            html_parts.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            if in_ul:
                html_parts.append('</ul>')
                in_ul = False
            html_parts.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('- '):
            if not in_ul:
                html_parts.append('<ul>')
                in_ul = True
            item = line[2:]
            item = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item)
            item = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', item)
            html_parts.append(f'<li>{item}</li>')
        elif line.startswith('| '):
            if in_ul:
                html_parts.append('</ul>')
                in_ul = False
            # table row - skip for now (render as paragraph)
        elif line.strip() == '':
            if in_ul:
                html_parts.append('</ul>')
                in_ul = False
        else:
            if in_ul:
                html_parts.append('</ul>')
                in_ul = False
            p = line
            p = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', p)
            p = re.sub(r'\*(.+?)\*', r'<em>\1</em>', p)
            p = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', p)
            if p.strip():
                html_parts.append(f'<p>{p}</p>')
    if in_ul:
        html_parts.append('</ul>')
    return '\n    '.join(html_parts)

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{metaTitle}</title>
<meta name="description" content="{metaDescription}">
<link rel="canonical" href="https://trekko.com.br/blog/{slug}">
<meta property="og:title" content="{metaTitle}">
<meta property="og:description" content="{metaDescription}">
<meta property="og:type" content="article">
<meta property="og:url" content="https://trekko.com.br/blog/{slug}">
<meta property="og:image" content="https://trekko.com.br/images/trekko_logo_horizontal_color_transparent.png" />
<meta property="og:image:width" content="1024" /><meta property="og:image:height" content="1024" />
<meta property="article:published_time" content="{publishedAt}">
<meta property="article:modified_time" content="{publishedAt}">
<meta property="article:author" content="{authorName}">
<link rel="icon" href="/favicon-48x48.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap" onload="this.onload=null;this.rel=\'stylesheet\'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@400;500;600;700&display=swap"></noscript>
<script>window.TREKKO_CONFIG={{GA4_ID:\'G-S816P190VN\',GTM_ID:null,ADS_ID:\'AW-355784943\'}};</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-S816P190VN"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag(\'js\',new Date());gtag(\'config\',\'G-S816P190VN\');</script>
<script defer src="/assets/trekko-analytics.js"></script>
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@graph": [
  {{
   "@type": "Article",
   "@id": "https://trekko.com.br/blog/{slug}/#article",
   "headline": "{title}",
   "description": "{metaDescription}",
   "image": "https://trekko.com.br/images/trekko_logo_horizontal_color_transparent.png",
   "datePublished": "{publishedAtTz}",
   "dateModified": "{publishedAtTz}",
   "author": {{
    "@type": "Person",
    "name": "{authorName}",
    "description": "{authorRole}"
   }},
   "publisher": {{
    "@type": "Organization",
    "name": "Trekko",
    "logo": {{"@type":"ImageObject","url":"https://trekko.com.br/android-chrome-192x192.png","width":192,"height":192}},
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
:root{{--primary:#15803d;--primary-dark:#166534;--primary-hover:#16a34a;--primary-light:#dcfce7;--primary-bg:#f0fdf4;--accent:#f59e0b;--accent-light:#fef3c7;--text-primary:#1e293b;--text-secondary:#475569;--text-muted:#94a3b8;--border:#e2e8f0;--white:#fff;--bg-light:#f8fafc;--shadow-sm:0 1px 3px rgba(0,0,0,.08);--shadow-md:0 4px 12px rgba(0,0,0,.1);--radius:8px;--radius-lg:16px;--font-body:\'Inter\',sans-serif;--font-heading:\'Sora\',sans-serif;--max-w:1200px;--gutter:1.25rem}}
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
.author-card{{background:var(--bg-light);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1.5rem;margin:2rem 0;display:flex;gap:1rem;align-items:flex-start}}
.author-avatar{{width:56px;height:56px;border-radius:50%;background:var(--primary-light);display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0}}
.author-info h4{{font-family:var(--font-heading);font-size:1rem;font-weight:700;margin-bottom:.25rem}}
.author-info p{{font-size:.85rem;color:var(--text-secondary);margin-bottom:.25rem}}
.author-credentials{{font-size:.75rem;color:var(--text-muted)}}
footer{{background:var(--text-primary);color:var(--text-muted);padding:3rem 0 2rem;margin-top:3rem}}
.footer-brand h3{{font-family:var(--font-heading);color:var(--white);font-size:1.1rem;margin-bottom:.5rem}}
.footer-brand p{{font-size:.85rem;line-height:1.6}}
.footer-inner{{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:2rem}}
.footer-col h4{{color:#fff;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.75rem}}
.footer-col ul li+li{{margin-top:.4rem}}
.footer-col a{{font-size:.85rem;color:rgba(255,255,255,.65);transition:color .15s}}.footer-col a:hover{{color:#fff}}
.footer-bottom{{border-top:1px solid rgba(255,255,255,.1);margin-top:2rem;padding-top:1.5rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.75rem;font-size:.8rem}}
@media(max-width:768px){{nav{{display:none}}.article-title{{font-size:1.5rem}}.author-card{{flex-direction:column}}}}
@media(max-width:900px){{.footer-inner{{grid-template-columns:1fr 1fr}}}}
@media(max-width:600px){{.footer-inner{{grid-template-columns:1fr}}.footer-bottom{{flex-direction:column;text-align:center}}}}
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
    <a href="/">Trekko</a> › <a href="/blog">Blog</a> › {catDisplay}
  </nav>
</div>

<main class="container">
  <div class="article-header">
    <span class="article-category">{catDisplay}</span>
    <h1 class="article-title">{title}</h1>
    <p class="article-subtitle">{subtitle}</p>
    <div class="article-meta">
      <span>✍️ {authorName}</span>
      <span>📅 {publishDate}</span>
      <span>⏱ {readingTime} min de leitura</span>
    </div>
  </div>

  <div class="article-layout">
    <article class="post-body article-body">
    {bodyHtml}
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
</html>'''


def generate_html(art, author):
    pub_date = art["publishDate"]
    published_at = f"{pub_date}T10:00:00.000Z"
    published_at_tz = f"{pub_date}T10:00:00-03:00"
    body_html = content_to_html(art["content"])
    return HTML_TEMPLATE.format(
        slug=art["slug"],
        title=art["title"].replace('"', '&quot;'),
        subtitle=art["subtitle"],
        metaTitle=art["metaTitle"].replace('"', '&quot;'),
        metaDescription=art["metaDescription"].replace('"', '&quot;'),
        catDisplay=cat_display(art["category"]),
        authorName=author["authorName"],
        authorRole=author["authorRole"],
        publishDate=pub_date,
        publishedAt=published_at,
        publishedAtTz=published_at_tz,
        readingTime=art["readingTime"],
        bodyHtml=body_html,
    )


def run():
    with open(f"{BASE}/data/blog.json") as f:
        blog_data = json.load(f)

    start_id = max(a["id"] for a in blog_data) + 1

    new_entries = []
    for i, art in enumerate(ARTICLES):
        author = AUTHORS[art["authorSlug"]]
        pub_date = art["publishDate"]
        published_at = f"{pub_date}T10:00:00.000Z"

        # Write HTML
        blog_dir = f"{BASE}/blog/{art['slug']}"
        os.makedirs(blog_dir, exist_ok=True)
        html = generate_html(art, author)
        with open(f"{blog_dir}/index.html", "w") as f:
            f.write(html)
        print(f"  Written: blog/{art['slug']}/index.html")

        # Build blog.json entry
        entry = {
            "id": start_id + i,
            "slug": art["slug"],
            "title": art["title"],
            "subtitle": art["subtitle"],
            "content": art["content"],
            "excerpt": art["excerpt"],
            "category": art["category"],
            **{k: author[k] for k in author},
            "imageUrl": "/trails/jl0WG48YTz7o.jpg",
            "images": ["/trails/jl0WG48YTz7o.jpg"],
            "readingTime": art["readingTime"],
            "metaTitle": art["metaTitle"],
            "metaDescription": art["metaDescription"],
            "featured": 0,
            "status": "published",
            "publishedAt": published_at,
            "createdAt": published_at,
            "updatedAt": published_at,
            "tags": art["tags"],
            "relatedTrailIds": [],
            "viewCount": 0,
        }
        new_entries.append(entry)

    blog_data.extend(new_entries)
    with open(f"{BASE}/data/blog.json", "w", encoding="utf-8") as f:
        json.dump(blog_data, f, ensure_ascii=False, indent=2)
    print(f"blog.json updated: {len(blog_data)} total articles")

    # Update editorial_calendar.json - mark these slugs as publicado
    slugs = {art["slug"] for art in ARTICLES}
    with open(f"{BASE}/data/editorial_calendar.json") as f:
        cal = json.load(f)
    updated = 0
    for entry in cal:
        if entry["slug"] in slugs:
            entry["status"] = "publicado"
            updated += 1
    with open(f"{BASE}/data/editorial_calendar.json", "w", encoding="utf-8") as f:
        json.dump(cal, f, ensure_ascii=False, indent=2)
    print(f"editorial_calendar.json: {updated} entries marked publicado")

if __name__ == "__main__":
    run()
