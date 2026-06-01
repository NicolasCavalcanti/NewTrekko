#!/usr/bin/env python3
import json

with open('data/blog.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

expansions = {}

# A5 - seguranca-trilha-regras (id=20, 74w -> 1000w)
expansions[20] = """A maioria dos acidentes em trilhas brasileiras não é fruto de azar ou condições extremas imprevisíveis. É resultado de decisões evitáveis: trilhar sozinho sem avisar ninguém, continuar depois do ponto de retorno, ignorar sinais de cansaço excessivo, não verificar a previsão do tempo. Essas dez regras foram destiladas de anos de experiência conduzindo grupos em expedições e de análise dos casos de resgate mais recorrentes nos parques nacionais brasileiros.

Não são regras para trilheiros "paranóicos" — são regras para trilheiros que querem continuar fazendo trilhas por muitos anos.

## Regra 1: Avise Alguém Antes de Sair

Esta é a regra mais simples e a mais ignorada. Antes de qualquer saída, avise uma pessoa de confiança que não vai na trilha: nome da trilha, endereço do ponto de partida, horário de saída e horário previsto de retorno. Combine um horário de alerta: se você não entrar em contato até X horas, ela deve ligar para o Corpo de Bombeiros.

Em trilhas sem sinal de celular, isso não é paranóia — é o único sistema de segurança que funciona.

## Regra 2: Nunca Saia Sem Mapa Offline

Sinal de celular é imprevisível em áreas naturais. Mesmo trilhas próximas a centros urbanos podem ter trechos sem cobertura. Baixe o mapa da trilha no AllTrails, Wikiloc ou Maps.me antes de sair de casa, em modo offline. Confirme que o download foi feito — não confie em memória cache do aplicativo.

Se você usa GPS dedicado, mantenha as pilhas reserva em quantidade suficiente para o dobro do tempo estimado de trilha.

## Regra 3: Respeite o Ponto de Retorno

O ponto de retorno é o momento — geralmente a metade do tempo disponível, não a metade da distância — a partir do qual você deve começar a voltar, independente de estar no destino ou não. A maioria das pessoas que ficam presas na escuridão na trilha tomou a decisão errada de continuar "só mais um pouco" depois desse ponto.

Calcule assim: se você tem 8 horas de luz disponível e a trilha tem tempo estimado de 6 horas, seu ponto de retorno é ao completar 4 horas de caminhada — independente de ter chegado ao topo ou não.

## Regra 4: Verifique a Previsão do Tempo Com Antecedência

No Brasil, principalmente nas serras e chapadas, o tempo pode mudar em questão de horas. Verifique a previsão nos 3 dias anteriores à trilha e no dia da saída. Use o INMET ou o Climatempo.

Critérios para adiar:
- Previsão de chuva acima de 20mm em área serrana
- Qualquer alerta meteorológico em vigor para a região
- Vento acima de 40 km/h em trilhas de crista ou expostas
- Qualquer dúvida sobre condições em trilhas de dificuldade elevada

## Regra 5: Leve Mais Água do Que Você Acha Necessário

A maioria das pessoas leva água para o tempo estimado de trilha. O correto é levar para o dobro desse tempo. Se algo der errado — você se perde, alguém se machucar, o ritmo ficar mais lento que o esperado — a água é o recurso mais crítico.

Para trilhas de 1 dia, a recomendação mínima é 3 litros para adultos em condições normais. Em dias quentes ou trilhas com muita subida, 4–5 litros. Leve também pastilhas de purificação como reserva de emergência.

## Regra 6: Nunca Separe o Grupo Permanentemente

Em grupos, ocasionalmente os trilheiros mais rápidos chegam antes ao destino e esperam. Isso é aceitável. O que não é aceitável é dividir o grupo em subgrupos que tomam caminhos diferentes sem comunicação.

Se o grupo precisa se dividir por qualquer razão, ambas as partes devem ter: mapa, água, telefone carregado (ou rádio), o nome e localização do ponto de encontro e horário limite para o encontro.

## Regra 7: Reconheça os Sinais de Emergência no Corpo

Treinar saber reconhecer os sinais de que algo está errado com você ou com alguém do grupo pode fazer a diferença entre uma situação controlada e uma emergência:

**Hipotermia em início:** tremor incontrolável, confusão mental, dificuldade de coordenação motora. Pare imediatamente, abrigue a pessoa, adicione camadas secas e dê açúcar.

**Desidratação severa:** dor de cabeça intensa, tontura, urina escura ou ausente, confusão mental. Hidratação lenta e contínua. Se a pessoa estiver confusa, busque resgate.

**Exaustão por calor:** pele quente e seca (sem suor), pulso rápido, possível perda de consciência. Resfrie a pessoa na sombra, ventile, coloque panos úmidos.

## Regra 8: Carregue Seu Telefone Com Bateria Suficiente

Um telefone com 10% de bateria no começo da trilha pode não funcionar quando você precisar. Carregue a 100% na véspera. Leve um carregador portátil (power bank) em trilhas acima de 4 horas.

Ative o modo avião quando não houver sinal — evita que o telefone gaste bateria procurando rede. Salve os contatos de emergência (Bombeiros, SAMU, telefone do parque) no favoritos, fora do aplicativo de contatos normal, para acesso rápido.

## Regra 9: Vista-se Para a Pior Condição Esperada, Não Para a Melhor

O sistema de camadas resolve isso com elegância: use roupa que funciona tanto para o calor do início da trilha quanto para o frio do topo ou de uma chuva inesperada. Nunca saia sem uma camada impermeável em trilhas serranas, mesmo com sol.

## Regra 10: Saiba Quando Desistir

Esta é talvez a mais difícil das dez regras. A maioria das pessoas que precisa de resgate em trilhas estava com sinais claros de que algo não estava bem — e continuou mesmo assim.

Motivos válidos para interromper uma trilha:
- Qualquer membro do grupo com lesão que limita o movimento
- Deterioração repentina das condições climáticas
- Desorientação de qualquer membro do grupo
- Equipamento crítico com falha (bota rasgada, mochila quebrada com todo o equipamento)

Desistir de uma trilha não é fraqueza. É a decisão que garante que você vai poder fazer a próxima.

Para planejar sua saída com segurança desde o início, leia nosso guia sobre [como escolher uma trilha segura](/blog/como-escolher-trilha-segura-brasil) e aprenda sobre o [kit de primeiros socorros essencial para trilha](/blog/kit-primeiros-socorros-trilha)."""

# A6 - animais-perigosos-trilhas-brasil (id=13, 77w -> 1000w)
expansions[13] = """O Brasil é o país com a maior biodiversidade do planeta — e isso inclui alguns dos animais peçonhentos mais impressionantes do mundo. A boa notícia para trilheiros é que acidentes com animais representam uma fração mínima dos incidentes nas trilhas brasileiras, e a grande maioria é prevenível com conhecimento básico e comportamento adequado no campo.

O maior erro que os trilheiros cometem em relação a animais perigosos é deixar o medo irracional substituir o conhecimento prático. Conhecer os animais que você pode encontrar — e saber como se comportar — é muito mais útil do que o pânico.

## Serpentes Peçonhentas: Como Identificar e o Que Fazer

O Brasil tem as maiores populações de serpentes peçonhentas do mundo, com destaque para o gênero Bothrops (jararacas), responsável por mais de 90% dos acidentes ofídicos no país.

**Como evitar:**
- Nunca coloque mãos ou pés em locais que não pode ver: pedras, troncos, buracos, pilhas de folhas
- Ande sempre pela trilha marcada — serpentes ficam nas bordas, na vegetação densa
- Use bota de cano alto com sola grossa
- Em acampamentos, sacuda os sapatos e roupas antes de usar pela manhã
- Nunca tente pegar ou matar uma serpente — a maioria dos acidentes ocorre nessas tentativas

**O que fazer em caso de picada:**
1. Mantenha a calma e imobilize o membro afetado abaixo do nível do coração
2. Remova anéis, pulseiras e roupas apertadas no membro afetado
3. NÃO faça torniquete, não corte, não suce o veneno — essas técnicas aumentam o dano tecidual
4. Busque atendimento médico o mais rápido possível — o soro antiofídico é o único tratamento eficaz
5. Se possível, fotografe a serpente de distância segura para auxiliar na identificação do soro

## Escorpiões: O Risco Mais Subestimado

O Tityus serrulatus, escorpião-amarelo, é o animal mais perigoso do Brasil em termos de número de acidentes graves — especialmente para crianças. Presente em todo o Brasil, adaptou-se muito bem ao ambiente urbano e periurbano, mas é encontrado também em trilhas e acampamentos.

**Como evitar:**
- Antes de dormir, verifique o interior do saco de dormir e a roupa que vai usar amanhã
- Nunca deixe sapatos e botas sem proteção no chão à noite — coloque dentro da barraca ou em saco fechado
- Em acampamentos, não empilhe lenha ou pedras perto da área de dormir
- Evite caminhadas noturnas sem lanternas
- Use luvas ao mover pedras ou troncos

**Em caso de picada:** dor imediata e intensa no local. Crianças e idosos devem ser levados ao pronto-socorro imediatamente. Em adultos saudáveis, a picada geralmente causa apenas dor local, mas qualquer sintema sistêmico (vômito, tremores, sudorese intensa) é sinal para buscar atendimento de urgência.

## Abelhas e Marimbondos: Perigo Real em Grupos

Colmeias de abelhas africanizadas são um risco real em trilhas brasileiras — especialmente em trilhas com vegetação fechada. Uma colmeia perturbada pode mobilizar centenas de insetos em segundos.

**Como evitar:**
- Mantenha ritmo constante e silencioso em trechos de mata fechada
- Se ouvir zumbido intenso, recue imediatamente pelo mesmo caminho que veio
- Não use perfumes ou desodorantes muito fortes em trilhas — abelhas se atraem por odores
- Fique atento a buracos no chão, ocos em árvores e construções em forquilhas de galhos

**Em caso de ataque:** corra em linha reta para longe da colmeia, protegendo o rosto. Não pule em água — as abelhas esperam. Em pessoas com alergia conhecida, o uso de EpiPen (epinefrina autoinjetável) pode ser questão de vida ou morte.

## Carrapatos: Pequenos, Perigosos e Muito Comuns

Carrapatos do gênero Amblyomma são endêmicos em praticamente todo o Brasil e podem transmitir a febre maculosa brasileira, uma doença bacteriana com taxa de letalidade de até 20–40% em casos não tratados rapidamente.

**Como evitar:**
- Use calças compridas e camisas de manga longa em trilhas com vegetação rasteira
- Aplique repelente com DEET ou Icaridin nas roupas e pele exposta
- Ao final da trilha, faça uma inspeção completa do corpo: couro cabeludo, axilas, virilha, atrás dos joelhos
- Vista roupas claras — facilita a visualização dos carrapatos

**Como remover:** use pinça fina, segure próximo à pele e puxe em linha reta sem torcer. Nunca esmague nem aplique substâncias. Após remover, desinfete com álcool. Se desenvolver febre nos dias seguintes, informe o médico sobre possível contato com carrapatos.

## Onças e Outros Grandes Mamíferos

As chances de encontro com onça-pintada em trilhas convencionais são extremamente baixas. Onças são animais crepusculares e noturnos que evitam humanos. No entanto, em áreas do Pantanal e Amazônia, algumas orientações básicas são úteis:

- Nunca trilhe no crepúsculo ou à noite em áreas de onça
- Em grupos, mantenha conversas em voz normal — isso afasta predadores
- Se ver uma onça, mantenha contato visual, não corra e recue lentamente

Jacarés, presentes em rios e lagoas do Pantanal, Amazônia e Nordeste: nunca nade em águas não inspecionadas e mantenha distância de pelo menos 15 metros de animais visíveis na margem.

## Plantas Urticantes e Tóxicas

Nem só animais representam risco. A urtiga-gigante (Urera baccifera) causa queimação intensa e bolhas no contato. Diversas plantas da família Euphorbiaceae têm látex tóxico que causa irritação ocular grave.

Regra básica: nunca toque plantas desconhecidas com as mãos. Ao cruzar vegetação fechada, proteja braços e pernas.

Para saber mais sobre como se preparar antes de sair, confira nosso guia de [segurança em trilhas](/blog/seguranca-trilha-regras) e aprenda a montar um [kit de primeiros socorros adequado](/blog/kit-primeiros-socorros-trilha) para diferentes tipos de emergência no campo."""

# A7 - guia-cadastur-como-encontrar (id=25, 79w -> 900w)
expansions[25] = """Contratar um guia de trekking parece simples — uma busca rápida no Instagram ou no Google e você encontra dezenas de perfis com fotos bonitas de trilhas. Mas a aparência nas redes sociais não diz nada sobre a competência técnica, a formação em primeiros socorros, o conhecimento do terreno ou a responsabilidade legal do profissional. Saber distinguir um guia credenciado de um entusiasta improvisado é uma habilidade que pode fazer diferença real na segurança da sua saída.

Este guia explica como funciona o CADASTUR, por que ele importa e como encontrar um guia certificado para qualquer trilha no Brasil.

## O Que é o CADASTUR e Por Que Ele Existe

O CADASTUR é o sistema de cadastramento de prestadores de serviços turísticos do Ministério do Turismo. Para guias de turismo, o registro é obrigatório por lei federal (Lei 11.771/2008) e exige comprovação de formação técnica na área.

Para ser cadastrado como guia de turismo, o profissional precisa:
- Ter formação em curso de Guia de Turismo reconhecido pelo MEC
- Estar registrado no CADASTUR com situação regular
- Ter certidão negativa de antecedentes criminais
- Renovar o cadastro periodicamente

O cadastro não é uma formalidade burocrática — ele garante que o profissional passou por um processo de formação estruturado, tem responsabilidade legal pela segurança dos clientes e pode ser identificado e responsabilizado em caso de problemas.

## Como Verificar se um Guia é Realmente Cadastrado

O número do CADASTUR de um guia pode ser verificado em tempo real no site oficial: **cadastur.turismo.gov.br**. Na página inicial, clique em "Consultar Prestadores" e busque pelo nome ou CPF do profissional.

O que verificar:
- **Situação:** deve estar "Ativo". Cadastros "Em análise" ou "Vencido" indicam irregularidade
- **Categoria:** confirme que está registrado como "Guia de Turismo", não como agência ou transportador
- **Data de validade:** guias com cadastro vencido há mais de 90 dias estão irregulares

Qualquer guia profissional sério vai te fornecer o número do CADASTUR antes de fechar contrato — se ele hesitar ou não souber o número, desconfie.

## Onde Encontrar Guias Certificados por Região

**Parques Nacionais:** A sede administrativa de cada parque nacional tem uma lista de guias credenciados para aquele parque específico. Em alguns casos, como o Monte Roraima e a Travessia Petrópolis-Teresópolis, o guia credenciado pelo parque é obrigatório, não opcional. Consulte o site do ICMBio ou ligue diretamente para o parque.

**Associações de Guias:** várias regiões têm associações locais de guias credenciados:
- AGUIATUR (Bahia / Chapada Diamantina)
- Associação de Guias da Chapada dos Veadeiros (Goiás)
- AGUIA-RJ (Rio de Janeiro)
- Associações locais em Minas Gerais, Santa Catarina e Rio Grande do Sul

**Plataformas online:** o portal Turismo.gov.br e o próprio CADASTUR têm ferramentas de busca por localidade. Filtre por "Guia de Turismo" e pela cidade ou estado desejado.

## O Que Um Bom Guia de Trekking Deve Oferecer

Além da certificação, avalie:

**Formação em primeiros socorros:** guias que atuam em trilhas longas ou remotas devem ter, no mínimo, curso básico de primeiros socorros com validade vigente. Cursos da Cruz Vermelha, SAMU ou CBME (Corpo de Bombeiros) são referência.

**Conhecimento específico da rota:** um guia de trekking em Minas Gerais não necessariamente conhece a Chapada Diamantina. Pergunte quantas vezes ele já conduziu grupos naquela trilha específica.

**Relação grupo-guia adequada:** guias sérios limitam o tamanho dos grupos por questões de segurança. Para trilhas técnicas, a proporção recomendada é de 1 guia para cada 8 a 10 trilheiros. Desconfie de guias que aceitam grupos de 20 ou mais pessoas sem auxiliar.

**Equipamento coletivo de segurança:** o guia deve carregar kit de primeiros socorros completo, comunicador (rádio ou satélite) e equipamentos de segurança compatíveis com o nível da trilha.

## Valores Médios e O Que Está Incluído

Os valores cobrados por guias de trekking variam muito por região e tipo de trilha. Como referência:

- Trilhas de 1 dia em parques estaduais (SP, RJ, MG): R$ 150–300 por pessoa em grupos
- Travessias de 2–3 dias (Serra dos Órgãos, Diamantina): R$ 400–700 por pessoa
- Expedições longas (Roraima, Vale do Pati): R$ 1.200–2.500 por pessoa

Sempre confirme o que está incluído: o guia cobre apenas a condução, ou inclui transporte, alimentação e hospedagem? Há taxa de entrada no parque cobrada à parte?

Contratar um guia certificado não é um luxo — é uma decisão que aumenta sua segurança, enriquece a experiência com conhecimento local e garante que você está com um profissional responsável legalmente pela condução. Para entender mais sobre os benefícios concretos, leia nosso artigo sobre [por que contratar um guia CADASTUR](/blog/por-que-contratar-guia-cadastur)."""

# A8 - hidratacao-trilha-quantos-litros (id=22, 79w -> 800w)
expansions[22] = """A desidratação é um dos fatores de risco mais subestimados em trilhas brasileiras. Diferente de uma lesão de tornozelo ou uma picada de inseto — que têm sinais visíveis e imediatos — a desidratação se instala silenciosamente, comprometendo o raciocínio, o equilíbrio e a resistência muscular antes mesmo de você sentir muita sede. Entender como se hidratar corretamente em campo não é um detalhe — é parte fundamental da segurança em qualquer trilha.

Este guia cobre os três aspectos que mais importam para a hidratação em campo: quanto beber, como carregar e como tratar água de fontes naturais.

## Quanto Beber: Calculando Sua Necessidade Real

A resposta simples — "2 litros por dia" — não serve para trilhas. Ela foi formulada para adultos sedentários em temperatura ambiente. Em atividade física moderada a intensa, sob sol e com carga nas costas, a necessidade de hidratação é muito maior.

**Regra prática para trilhas:**
- Trilha leve (plana, temperatura amena): 500 ml por hora de caminhada
- Trilha moderada (subidas, temperatura até 25°C): 600–700 ml por hora
- Trilha intensa (subidas longas, temperatura acima de 28°C): 800–1.000 ml por hora

Para uma trilha de 6 horas com subidas em dia quente, isso significa entre 4,8 e 6 litros. Leve sempre mais do que o mínimo calculado.

**O erro mais comum:** beber apenas quando sente sede. A sede é um sinal tardio de desidratação — quando você sente sede, já perdeu entre 1% e 2% do peso corporal em fluidos. Uma perda de 2% já compromete o desempenho físico e cognitivo de forma mensurável. Beba proativamente, de 150 a 200 ml a cada 20–30 minutos, independente de estar com sede.

## Como Monitorar Sua Hidratação no Campo

O indicador mais confiável de hidratação no campo é a cor da urina. Memorize isso:

- **Amarelo-claro (quase transparente):** hidratado corretamente
- **Amarelo-médio:** levemente desidratado — beba agora
- **Amarelo-escuro ou alaranjado:** desidratação significativa — pare, beba e descanse
- **Urina muito escura ou ausente por mais de 4 horas:** emergência médica

Outros sinais de alerta: dor de cabeça intensa sem causa aparente, tontura ao levantar, cãibras musculares repentinas, irritabilidade desproporcional.

## Como Carregar Água: Garrafas vs. Hidratadores

**Garrafas rígidas de polipropileno (como Nalgene):** duráveis, fáceis de limpar, empilháveis, permitem ver quanto resta. Desvantagem: ocupam espaço específico na mochila.

**Hidratadores (reservatórios flexíveis com mangueira):** permitem beber sem parar ou tirar a mochila, incentivam hidratação contínua. Desvantagem: difíceis de limpar, não dá para ver quanto resta, podem vazar.

**Combinação recomendada:** um hidratador de 2L interno + uma garrafa de 1L acessível no bolso lateral da mochila como reserva. Isso dá 3L disponíveis e visíveis.

## Tratamento de Água de Fontes Naturais

Em trilhas de 1 dia em parques nacionais bem estruturados, geralmente não é necessário tratar água — você leva o suficiente de casa. Mas em travessias de múltiplos dias ou trilhas remotas, saber tratar água de fontes naturais é uma habilidade fundamental.

**Pastilhas de purificação (hipoclorito ou dióxido de cloro):**
- Vantagem: leves, baratas, fáceis de usar
- Tempo de espera: 30–60 minutos depois de adicionar
- Eficazes contra bactérias e vírus, menos eficazes contra protozoários como Giardia
- Custo: em torno de R$ 15–30 por embalagem com 50 pastilhas

**Filtros de membrana (tipo LifeStraw ou Sawyer Squeeze):**
- Vantagem: removem bactérias e protozoários, sem espera, sem gosto de cloro
- Limitação: não filtram vírus (menos relevante no Brasil continental, mais importante em áreas com muita presença humana)
- Custo: R$ 80–250

**Fervura:**
- Eficaz contra todos os patógenos
- Espere a água esfriar antes de beber — ninguém trilha melhor com queimadura na garganta
- Prático apenas em acampamentos com fogareiro

A combinação mais segura para travessias é filtro de membrana + pastilhas de cloro como backup.

## Eletrólitos: Por Que Só Água Não Basta em Trilhas Longas

Em atividades acima de 2 horas, especialmente com muito suor, repor apenas água pode diluir os eletrólitos do sangue — principalmente sódio. A hiponatremia (sódio baixo) causa sintomas parecidos com desidratação: dor de cabeça, náusea, confusão.

Adicione eletrólitos à sua estratégia de hidratação em trilhas longas:
- Sachês de sais de reidratação oral (baratos e eficazes)
- Bebidas isotônicas diluídas (1 parte de isotônico para 1 de água)
- Alimentos salgados durante as pausas: castanhas, queijo, barras de cereais com sal

Para trilhas em que a hidratação vai ser um desafio especial — como trilhas de longa duração no Nordeste — consulte também nosso guia sobre [como se preparar fisicamente para o trekking](/blog/preparo-fisico-trekking)."""

print("Batch 2 expansions defined.")

for post in data:
    if post['id'] in expansions:
        post['content'] = expansions[post['id']]

with open('data/blog.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Batch 2 written to blog.json")

for post in data:
    if post['id'] in expansions:
        words = len(post['content'].split())
        print(f"ID {post['id']} | {words}w | {post['slug']}")
