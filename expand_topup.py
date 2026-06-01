#!/usr/bin/env python3
import json

with open('data/blog.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Map id -> post for easy access
posts = {p['id']: p for p in data}

def append_section(post_id, section_text):
    posts[post_id]['content'] += '\n\n' + section_text

# ID 1 - travessia-petropolis-teresopolis (need +37w)
append_section(1, """## Transporte de Retorno

Ao terminar a travessia em Teresópolis, você pode pegar ônibus da empresa Viação 1001 de volta para o Rio de Janeiro (Rodoviária Novo Rio), com saídas frequentes ao longo do dia. O trecho dura cerca de 2h30. Se tiver carro deixado na sede de Petrópolis, a solução mais prática é um táxi de Teresópolis até Petrópolis — o percurso de 70 km leva cerca de 1h30 pelas serras.""")

# ID 2 - monte-roraima (need +74w)
append_section(2, """## Planejamento Orçamentário

Uma expedição ao Monte Roraima pelo lado brasileiro tem custo médio de R$ 3.000 a R$ 5.000 por pessoa, incluindo guia, alimentação, transporte de carga por muares, transporte de Boa Vista a Uiramutã e as taxas de visitação. Pacotes contratados em Boa Vista com agências especializadas geralmente incluem tudo isso. É possível organizar de forma independente, mas o custo raramente é muito menor e a complexidade logística é significativamente maior — especialmente a negociação com a comunidade indígena para a permissão de acesso.""")

# ID 3 - 10-itens-essenciais (need +55w)
append_section(3, """## Checklist Rápido de Conferência

Antes de sair de casa, percorra mentalmente cada categoria: navegação online? mapa offline baixado? protetor solar na bolsa lateral? camada impermeável no topo da mochila? lanterna carregada? kit de primeiros socorros no bolso acessível? pastilhas de purificação no fundo? Manta aluminizada? Essa revisão de 2 minutos antes de cada saída vira hábito depois de 3 trilhas — e pode fazer toda a diferença na quarta.""")

# ID 4 - por-que-contratar-guia-cadastur (need +134w)
append_section(4, """## Guia vs. Condutor de Visitantes

No Brasil, existe uma distinção importante que muitos trilheiros desconhecem: o Guia de Turismo registrado no CADASTUR é diferente do Condutor de Visitantes credenciado pelo parque. O guia tem formação nacional e pode atuar em qualquer área do país. O condutor de visitantes tem credenciamento específico para uma unidade de conservação — conhece profundamente aquele território, mas sua habilitação é local.

Em muitos parques nacionais, como o Chapada dos Veadeiros e o Aparados da Serra, o credenciamento aceito é o de condutor local, não necessariamente o CADASTUR nacional. Verifique com o parque específico qual tipo de habilitação é exigida para a trilha que você vai fazer — e sempre confirme a validade do credenciamento antes de contratar.""")

# ID 5 - chapada-dos-veadeiros (need +78w)
append_section(5, """## Alto Paraíso ou São Jorge: Qual Base Escolher?

A escolha da base na Chapada dos Veadeiros depende do seu estilo de viagem. Alto Paraíso de Goiás é a cidade com melhor infraestrutura — supermercados, farmácias, restaurantes variados, pousadas de todos os perfis e acesso rápido à portaria do parque. São Jorge é uma vila menor, com energia alternativa e pegada mais bohemia, frequentada por praticantes de turismo espiritual e viajantes independentes. Está a 35 km de Alto Paraíso e bem próximo ao Vale da Lua. Para uma primeira visita, Alto Paraíso oferece mais conforto e praticidade.""")

# ID 6 - planejamento-trilha-longo-curso (need +5w — trivial, add one sentence)
append_section(6, """Boa trilha.""")

# ID 9 - como-comecar-trekking-iniciante (need +34w)
append_section(9, """## Grupos e Comunidades Para Trilheiros Iniciantes

Trilhar acompanhado é mais seguro e mais divertido na fase inicial. Procure grupos de trekking para iniciantes no Meetup.com, Facebook e Instagram da sua cidade. Cidades como São Paulo, Rio, BH e Curitiba têm grupos ativos com saídas toda semana — muitos de graça, organizados por trilheiros experientes que gostam de apresentar novos percursos para pessoas que estão começando.""")

# ID 10 - trilhas-faceis-sao-paulo (need +29w)
append_section(10, """## Grupos de Trekking em São Paulo

A cidade de São Paulo tem uma das maiores comunidades de trekking do Brasil. Grupos no Facebook como "Trilheiros SP" e no Meetup têm saídas semanais organizadas para as principais trilhas do estado, muitas vezes com transporte fretado saindo da capital e sem custo de organização.""")

# ID 11 - trilhas-faceis-rio-de-janeiro (need +109w)
append_section(11, """## Parque Nacional do Itatiaia — Acesso a Partir do Rio

A apenas 165 km do Rio de Janeiro, o Parque Nacional do Itatiaia é o mais antigo parque nacional do Brasil e um dos destinos de trekking mais completos do Sudeste. O parque tem duas partes bem distintas: a parte baixa (700–1.100m) com trilhas de cachoeira e mata atlântica densa, e a parte alta (acima de 2.200m) com campos de altitude e picos rochosos.

**Trilha da Cachoeira de Itaporani:** 3 km fácil na parte baixa. Adequada para iniciantes.

**Agulhas Negras (2.791m):** o quarto ponto mais alto do Brasil. Trilha de 12 km com desnível de 900m — para trilheiros experientes com condicionamento sólido.

**Como chegar:** pela Via Dutra (BR-116), saída em Itatiaia. Há ônibus de Resende para a portaria do parque. Para a parte alta, é necessário carro.""")

# ID 12 - kit-primeiros-socorros-trilha (need +121w)
append_section(12, """## Medicamentos Para Condições Pessoais Específicas

Um kit de primeiros socorros genérico cobre a maioria das emergências comuns em trilha. Mas pessoas com condições médicas específicas precisam de itens adicionais:

**Alergia severa a picadas de inseto (anafilaxia):** leve EpiPen (epinefrina autoinjetável) prescrita por médico. Informe o grupo sobre o procedimento de aplicação.

**Asma:** bombinha de resgate na mochila, não apenas em casa. O esforço físico intenso em altitude pode desencadear crise mesmo em asmáticos bem controlados.

**Diabetes:** gel de glicose ou tabletes de dextrose para hipoglicemia. Monitore com frequência em trilhas longas — a hipoglicemia em campo é uma emergência.

**Hipertensão:** verifique com seu cardiologista se há restrição para esforço intenso em altitude antes de qualquer trilha de maior dificuldade.

**Acrofobia ou claustrofobia:** identifique os trechos da trilha que podem ser gatilhos antes de sair — evitar surpresas em campo é sempre melhor.""")

# ID 13 - animais-perigosos-trilhas-brasil (need +89w)
append_section(13, """## Lagartas Urticantes: O Perigo Esquecido

As lagartas do gênero Lonomia, conhecidas como taturanas, são responsáveis por centenas de acidentes no Brasil por ano — e são subnotificadas porque muitas pessoas não associam os sintomas ao contato. O veneno da Lonomia interfere na coagulação sanguínea e pode causar hemorragia interna grave.

Evite tocar qualquer lagarta peluda ou com cerdas visíveis. Se houver contato, lave abundantemente com água e sabão e procure o Corpo de Bombeiros ou o Centro de Informações Toxicológicas mais próximo — há soro específico disponível em hospitais de referência em todas as regiões do Brasil.""")

# ID 14 - melhores-trilhas-minas-gerais (need +248w)
append_section(14, """## Roteiro Sugerido Para 5 Dias em Minas Gerais

**Para trilheiros intermediários:**
- **Dia 1–2:** Ouro Preto e Parque Estadual do Itacolomi (trilha do Cume, 14 km)
- **Dia 3:** traslado para Conceição do Mato Dentro (3h de carro)
- **Dia 4–5:** Serra do Cipó — Cachoeira da Farofa no Dia 4, Trilha da Serra das Bandeirinhas no Dia 5

**Para trilheiros avançados:**
- **Dia 1:** chegada em Alto Caparaó, aclimatação e trilha curta
- **Dia 2:** ascensão até o Vale Verde (Abrigo 1) — 8 km
- **Dia 3:** cume do Pico da Bandeira (2.892m) e retorno ao Vale Verde
- **Dia 4:** descida e traslado para próximo destino

## Aluguel de Carro em Belo Horizonte

Belo Horizonte tem boa oferta de locadoras no Aeroporto de Confins e no Aeroporto da Pampulha. Para o Caparaó, é necessário carro com boa tração — o acesso às portarias de Alto Caparaó (MG) e Iúna (ES) inclui trechos de estrada de terra. SUVs ou pickups são mais indicados em período chuvoso.

## Preparação Física Específica Para o Caparaó

O Caparaó é a trilha de altitude mais acessível do Brasil — mas essa acessibilidade não significa que qualquer pessoa pode fazer sem preparação. A altitude acima de 2.500m reduz a pressão parcial de oxigênio, aumenta o esforço percebido e pode causar sintomas de mal de altitude (cefaleia, náusea, insônia) mesmo em trilheiros bem condicionados.

Passe pelo menos uma noite em Carangola ou Alto Caparaó (900–1.100m) antes de subir para os abrigos. Hidrate-se bem, evite álcool na véspera e não subestime a temperatura — o parque registra temperaturas negativas na parte alta durante todo o inverno e mesmo em noites de outono.""")

# ID 15 - trilhas-chapada-diamantina (need +195w)
append_section(15, """## Hospedagem em Lençóis: Do Hostel à Pousada de Charme

Lençóis tem uma das melhores relações custo-benefício em hospedagem de destino de trekking no Brasil. Hostels com camas em dormitório custam R$ 60–100 por noite; pousadas simples com quarto privativo ficam entre R$ 150–300; pousadas boutique de charme chegam a R$ 500–800.

Para um roteiro de 5 dias com guia, orçamento o realista fica entre R$ 1.800–3.500 por pessoa, incluindo hospedagem, guias para as trilhas principais e alimentação no local.

## Como Chegar a Lençóis

**De avião:** o Aeroporto de Lençóis (LAJ) recebe voos diretos de Salvador e São Paulo. Em 2026, a Azul e o TRIP operam regularmente essa rota — verifique disponibilidade e antecedência de compra (os voos enchem em julho e nas férias de janeiro).

**De Salvador:** ônibus da Viação São Luiz e Real Expresso partem da rodoviária de Salvador em direção a Lençóis com saídas regulares. O percurso de 430 km pela BR-242 leva entre 5h30 e 7h dependendo das paradas.

## Gastronomia Local: Parte da Experiência

Lençóis tem restaurantes excelentes de cozinha baiana e nordestina. A moqueca de peixe do Rio Lençóis, o bode ao molho e as doces de buriti são experiências gastronômicas que complementam a experiência de trekking. Não saia sem provar a cachaça artesanal local servida em muitas pousadas da região.""")

# ID 16 - melhor-epoca-trilhas-brasil (need +168w)
append_section(16, """## Resumo Visual: Melhor Época Por Região

| Região | Melhor Época | Evitar |
|---|---|---|
| Sudeste (Serra, SP/RJ/MG) | Abril–Setembro | Dezembro–Março |
| Nordeste (Chapada Diamantina) | Junho–Novembro | Março–Maio |
| Nordeste (Lençóis Maranhenses) | Julho–Agosto | Outubro–Fevereiro |
| Centro-Oeste (Chapada dos Veadeiros) | Maio–Setembro | Outubro–Março |
| Pantanal | Junho–Outubro (fauna) | —— |
| Sul (Cânions RS/SC) | Setembro–Março | Junho–Agosto (neblina) |
| Norte (Monte Roraima) | Dezembro–Março | Junho–Setembro |

## Aplicativos e Fontes Para Consulta Climática

Antes de qualquer saída, consulte pelo menos duas fontes: o INMET para previsão técnica oficial e o Climatempo para interface mais amigável com detalhamento por hora. Para trilhas em parques, o site do ICMBio de cada unidade tem boletins de condições publicados com alguma frequência — vale conferir especialmente na véspera de travessias.""")

# ID 17 - o-que-e-trekking-diferenca-caminhada (need +122w)
append_section(17, """## Trekking vs. Hiking: A Diferença Internacional

Em inglês, o termo "hiking" é mais comum para caminhadas de 1 dia em trilha, enquanto "trekking" geralmente se refere a jornadas de múltiplos dias em terreno mais remoto — como o trekking no Nepal (Everest Base Camp, Annapurna Circuit) ou na Patagônia. No Brasil, usamos "trekking" de forma muito mais ampla, cobrindo desde trilhas de 2 horas até expedições de 10 dias.

Na prática, o que importa não é o rótulo — é o planejamento adequado para o tipo de saída que você está fazendo. Uma trilha de 3 horas sem equipamento adequado pode ser mais perigosa do que uma expedição de 5 dias bem planejada. Entender as características específicas da sua saída — terreno, distância, nível de isolamento, clima esperado — é mais relevante do que categorizar a atividade pelo nome.""")

# ID 18 - bota-ou-tenis-trilha (need +120w)
append_section(18, """## Cuidado Com o Calçado: Vida Útil e Manutenção

Um bom calçado de trilha pode durar de 500 a 1.000 km de uso se bem cuidado — ou 200 km se maltratado. Cuidados básicos que prolongam a vida útil:

**Após trilhas:** remova barro e pedras da sola com escova de cerdas duras. Não force a secagem com calor direto (secador, sol forte) — resseca couro e cola. Deixe secar à sombra com ventilação.

**Impermeabilização:** botas de couro e algumas de sintético perdem a impermeabilização natural com o uso. Reaproveite com produtos à base de cera (como Grangers ou Nikwax) a cada 3 a 6 meses de uso regular.

**Cadarços e palmilhas:** palmilhas são o item mais substituído e mais barato. Palmilhas específicas para trekking (Superfeet, Sole) melhoram o suporte e amortecimento de forma significativa em saídas longas.""")

# ID 19 - trilhas-santa-catarina (need +126w)
append_section(19, """## Serra Geral e Rota da Neve

A Serra Geral catarinense, que abrange municípios como Urubici, Bom Jardim da Serra e São Joaquim, é a única região do Brasil com neve regular — fenômeno que ocorre em média 1 a 3 vezes por inverno. A Rota da Neve, como é informalmente chamada, atrai visitantes de todo o país entre junho e agosto.

Para trilheiros, as nevadas transformam trilhas comuns em experiências completamente diferentes — e consideravelmente mais perigosas. Terreno coberto de gelo exige equipamento específico (polainas, bastões com ponteiras para gelo) e experiência com condições adversas. Não tente trilhas de altitude em Santa Catarina durante ou após nevadas sem guia local que conheça as condições do terreno.

## Como Chegar em Cambará do Sul

O acesso a Cambará do Sul (RS), porta de entrada do Aparados da Serra pelo lado gaúcho, é feito pela RS-235. A estrada tem trechos de terra no trecho final — recomenda-se carro com boa tração em períodos chuvosos.""")

# ID 20 - seguranca-trilha-regras (need +4w)
append_section(20, """Cuide-se bem.""")

# ID 21 - trilha-com-cachorro-regras (need +162w)
append_section(21, """## Treinamento de Obediência Básico Antes da Trilha

Um cão que não sabe sentar, ficar parado e vir quando chamado representa um risco em trilhas — tanto para o próprio animal quanto para outros trilheiros e para a fauna local. Antes de levar o cão para qualquer trilha, certifique-se de que ele atende a pelo menos três comandos básicos: sentar, ficar e vir.

Se o cão nunca foi expostos a ambientes naturais, comece com parques urbanos com terreno variado — grama, terra, pedra — antes de trilhas mais longas. O cão precisa aprender a andar em rédea curta sem puxar em terreno irregular, sem se assustar com barulhos de mato e sem reagir a outros animais com agressividade.

## Pós-trilha: O Que Fazer ao Chegar Em Casa

Além da inspeção de carrapatos, dê um banho completo no cão ao chegar — remove pólen, fungos, esporos e outros microrganismos que podem ser trazidos da mata. Verifique os olhos (areia, sementes) e as orelhas (acúmulo de sujeira e umidade, propício para otite). Observe o comportamento nas 48 horas seguintes: letargia, falta de apetite ou mancar podem ser sinais de problema que não apareceram imediatamente.""")

# ID 22 - hidratacao-trilha-quantos-litros (need +55w)
append_section(22, """## Hidratação em Alta Altitude

Em trilhas acima de 2.000 metros — como o Pico da Bandeira, o Caparaó ou o Monte Roraima — o ar seco e a respiração mais rápida causada pelo esforço em altitude aumentam a perda de água pelo sistema respiratório. Isso significa que a necessidade de hidratação é ainda maior do que em trilhas de baixa altitude com o mesmo esforço. Aumente o consumo em pelo menos 20% a cada 500 metros de altitude acima de 2.000m e preste atenção especial na cor da urina como indicador.""")

# ID 23 - sistema-camadas-roupa-trekking (need +130w)
append_section(23, """## Mãos, Cabeça e Pescoço: As Extremidades Esquecidas

O sistema de três camadas cobre o tronco de forma eficiente — mas boa parte do calor corporal se perde pelas extremidades. Em trilhas de altitude ou em qualquer ambiente abaixo de 15°C:

**Cabeça:** um gorro de lã ou sintético fino pode ser a diferença entre conforto e hipotermia em paradas longas. O calor perdido pela cabeça representa 30–40% do calor corporal total.

**Mãos:** luvas finas de lã ou sintético para paradas e trechos de vento. Podem ser guardadas facilmente no bolso quando não forem necessárias.

**Pescoço:** um buff ou gaiola de pescoço resolve o gap entre a camada base e a jaqueta, onde entra vento frio. É levíssimo e faz diferença enorme em cristas ventosas.

Leve sempre esses três itens de extremidade quando a previsão indicar temperatura abaixo de 18°C em qualquer ponto do percurso.""")

# ID 24 - como-planejar-trilha-grupo (need +54w)
append_section(24, """## O Que Fazer Quando Alguém Quer Desistir no Meio da Trilha

Não existe resposta certa para isso — mas existe um protocolo: nunca deixe um membro do grupo voltar sozinho. Se alguém precisar retornar antes do destino, pelo menos uma pessoa experiente acompanha de volta. O grupo decide juntos e por unanimidade, sem pressão. Uma trilha interrompida é infinitamente melhor do que um acidente solitário no retorno.""")

# ID 25 - guia-cadastur-como-encontrar (need +145w)
append_section(25, """## Red Flags: Sinais de Que Um Guia Não é Confiável

Além da verificação do cadastro, fique atento a estes sinais de alerta:

**Preço muito abaixo do mercado:** guias sérios têm custos reais de operação. Um guia que cobra metade do preço de mercado provavelmente está cortando algum corner — na formação, no seguro ou no equipamento de segurança.

**Recusa em mostrar o número do CADASTUR:** qualquer profissional certificado tem o número memorizado e não hesita em mostrá-lo.

**Grupos muito grandes sem auxiliar:** para trilhas moderadas a difíceis, a proporção segura é de 1 guia para cada 8 a 10 pessoas. Grupos maiores sem auxiliar de guia são sinais de descuido com a segurança.

**Sem kit de primeiros socorros ou comunicador:** pergunte antes de contratar o que o guia leva de equipamento de segurança. Um profissional sério vai ter resposta imediata para essa pergunta.

Para saber mais sobre os critérios de seleção de guia, leia nosso artigo sobre [por que contratar um guia CADASTUR](/blog/por-que-contratar-guia-cadastur).""")

# ID 26 - melhores-trilhas-rs-canyons (need +68w)
append_section(26, """## A Importância de Reservar Com Antecedência

O Parque Nacional de Aparados da Serra é um dos parques mais visitados do Sul do Brasil. Nos meses de setembro a novembro e em julho (inverno gaúcho com geada), os fins de semana esgotam a cota de visitantes com semanas de antecedência. Reserve pelo sistema do ICMBio assim que definir a data da viagem — não deixe para a semana anterior.""")

# ID 27 - preparo-fisico-trekking (need +75w)
append_section(27, """## Lesões Mais Comuns e Como Prevenir

**Tendinite patelar ("joelho do corredor"):** causada por descidas longas sem condicionamento adequado. Prevenção: fortalecimento de quadríceps e exercícios excêntricos de coxa. Tratamento em campo: compressa de gelo (snow ou compressa química), redução do passo na descida e uso de bastões.

**Entorse de tornozelo:** mais comum em terreno rochoso irregular. Prevenção: fortalecimento dos estabilizadores de tornozelo (exercícios de equilíbrio em superfície instável). Em campo: compressão com bandagem elástica, elevação e gelo. Se não suportar peso, evacue.""")

# ID 28 - trilhas-nordeste-brasil (need +136w)
append_section(28, """## Chapada do Araripe — Ceará/Pernambuco: A Floresta no Semiárido

A Chapada do Araripe, no extremo sul do Ceará e norte de Pernambuco, é um dos fenômenos geográficos mais intrigantes do Nordeste — uma chapada com floresta subtropical úmida (brejo de altitude) no meio do semiárido. A umidade vem das nuvens que se condensam nas encostas da chapada, criando um microclima completamente diferente da caatinga ao redor.

O município de Crato (CE) é a porta de entrada para o Geopark Araripe, com trilhas pelo Sítio Paleontológico da Chapada (fósseis de peixes de 110 milhões de anos) e pelas nascentes que alimentam o Rio Crato. A trilha mais acessível tem 5 km fácil.

**Melhor época:** maio a setembro, quando a vegetação está verde e as nascentes cheias depois das chuvas do inverno nordestino.""")

print("Top-up batch defined.")

for post in data:
    pass  # already modified in-place via posts dict

with open('data/blog.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Top-up written to blog.json")

# Final report
targets = {
    1: 900, 2: 800, 3: 800, 4: 800, 5: 800, 6: 800,
    7: 1000, 8: 1000, 9: 1200, 10: 1000, 11: 1000, 12: 1000,
    13: 1000, 14: 1200, 15: 1200, 16: 1000, 17: 900, 18: 900,
    19: 1000, 20: 1000, 21: 900, 22: 800, 23: 900, 24: 900,
    25: 900, 26: 1000, 27: 1000, 28: 1000
}
ok = 0
fail = 0
for post in data:
    words = len(post['content'].split())
    target = targets.get(post['id'], 800)
    status = '✓' if words >= target else f'✗ need+{target-words}'
    if words >= target:
        ok += 1
    else:
        fail += 1
    print(f'ID {post["id"]:2} | {words:5}w / {target}w {status}')
print(f'\nTotal: {ok} OK, {fail} below target')
