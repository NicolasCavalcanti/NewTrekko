#!/usr/bin/env python3
import json

with open('data/blog.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

expansions = {}

# A9 - trilhas-faceis-sao-paulo (id=10, 79w -> 1000w)
expansions[10] = """São Paulo pode parecer uma metrópole sufocante de concreto, mas quem conhece o estado sabe que ele esconde uma rede de trilhas surpreendentemente rica — muitas a menos de 2 horas da capital, acessíveis de carro ou transporte público, sem exigir experiência prévia. Neste guia, selecionei 8 trilhas fáceis em São Paulo que valem cada quilômetro percorrido.

Todas as opções desta lista atendem aos critérios de trilha fácil: distância de até 10 km, desnível menor que 400 metros, terreno acessível para iniciantes e boa sinalização.

## 1. Pedra Grande — Atibaia (SP)

**Distância:** 4 km ida e volta | **Desnível:** 200m | **Dificuldade:** fácil

A Pedra Grande é a trilha de iniciação clássica do interior paulista. O topo do afloramento granítico oferece uma das vistas mais amplas do estado, com a cidade de Atibaia, a represa e a Serra da Cantareira ao fundo. O percurso é bem sinalizado, com placas em todo o caminho, e pode ser feito em 2 horas no total.

**Como chegar:** a 68 km da capital pela Rodovia Dom Pedro I (SP-065). Há estacionamento pago na portaria do Parque Municipal da Pedra Grande.

## 2. Trilha da Cachoeira Véu de Noiva — Brotas (SP)

**Distância:** 6 km circular | **Desnível:** 180m | **Dificuldade:** fácil a moderado

Brotas é um polo de ecoturismo a 240 km de São Paulo, mas a trilha da Véu de Noiva pode ser feita em visita de 1 dia sem aventura radical. A trilha circular passa por mata ciliar densa, pontes de madeira sobre o Rio Jacaré-Pepira e termina na queda d'água com 18 metros de altura.

**Observação:** é necessário contratar um guia local para a trilha. A prefeitura de Brotas tem parceria com guias credenciados acessíveis pelo site oficial do município.

## 3. Parque Estadual da Cantareira — Zona Norte de São Paulo

**Distância:** 4 a 8 km (diversas rotas) | **Desnível:** 150–250m | **Dificuldade:** fácil

A Cantareira é a maior floresta urbana do mundo dentro de uma área metropolitana e está literalmente dentro da cidade de São Paulo. Os trilheiros da capital têm acesso a mais de 30 km de trilhas sem precisar pegar a rodovia.

Os núcleos Engordador, Cabuçu e Pedra Grande têm trilhas bem sinalizadas com diferentes graus de dificuldade. O Mirante do Cipó oferece vista panorâmica acessível em menos de 2 km de caminhada.

**Dica prática:** é necessário reserva prévia pelo site do Instituto Florestal.

## 4. Pedra do Baú — São Bento do Sapucaí (SP)

**Distância:** 7 km circular | **Desnível:** 380m | **Dificuldade:** fácil a moderado

A [Pedra do Baú](/trilha/pedra-do-bau) é um dos afloramentos rochosos mais icônicos do estado, com 1.950 metros de altitude. A trilha principal sobe pelo flanco norte em caminho de mata fechada e termina na base do monolito, de onde é possível subir pelos cabos de aço fixados na pedra até o topo.

**Como chegar:** a 170 km da capital pela Rodovia dos Tamoios (SP-099). Há pousadas e camping na área para quem quer transformar em viagem de fim de semana.

## 5. Parque Estadual Intervales — Ribeirão Grande (SP)

**Distância:** múltiplas opções de 3 a 10 km | **Dificuldade:** fácil a moderado

Para quem quer mata atlântica densa, fauna exuberante e cachoeiras, o Intervales é um dos melhores parques de São Paulo. As trilhas curtas como a Trilha da Figueira (3 km) e a Trilha da Cachoeira do Mirante (5 km) são acessíveis para iniciantes.

O parque tem uma das maiores densidades de morcegos cavernícolas do Brasil e avifauna impressionante — perfeito para observação de aves.

## 6. Cachoeiras de Paranapiacaba — Santo André (SP)

**Distância:** 6 km circular | **Desnível:** 200m | **Dificuldade:** fácil

Paranapiacaba é uma vila histórica de arquitetura inglesa na borda do planalto paulistano, a 50 km de Santo André. A trilha das cachoeiras desce a escarpa da Serra do Mar até uma série de quedas d'água na Mata Atlântica. O retorno é pela mesma trilha ou pelo trem histórico nos fins de semana.

**Diferencial:** você pode ir de trem de Santo André até Paranapiacaba nos fins de semana — uma saída de trilha incomum e encantadora saindo de casa sem carro.

## 7. Circuito das Hortências — Campos do Jordão (SP)

**Distância:** 5 km circular | **Desnível:** 200m | **Dificuldade:** fácil

Campos do Jordão é o destino de montanha mais estruturado do estado, com infraestrutura turística completa e diversas trilhas sinalizadas dentro e no entorno do Parque Estadual. O Circuito das Hortências atravessa campos de altitude floridos entre junho e setembro e tem vista para o Vale do Paraíba.

**Melhor época:** junho a agosto, quando as hortências estão em flor e o frio paulista está no pico.

## 8. Trilha da Represa do Juqueri — Franco da Rocha (SP)

**Distância:** 8 km circular | **Desnível:** 120m | **Dificuldade:** fácil

A trilha da Represa do Juqueri, no Parque Estadual do Juquery, é uma das poucas opções de trilha em campos de cerrado acessíveis a partir da região metropolitana de São Paulo. O terreno plano e a vista para a represa tornam o percurso indicado para famílias com crianças e para quem está começando.

## Dicas Gerais para Trilhas em São Paulo

**Reserva antecipada:** vários parques estaduais de São Paulo exigem reserva pelo sistema do Instituto Florestal (iflorestal.sp.gov.br). Faça isso com pelo menos uma semana de antecedência nos fins de semana.

**Transporte público:** Cantareira (metrô Tucuruvi + ônibus), Paranapiacaba (trem a partir de Santo André) e Cantareira são acessíveis sem carro. As demais trilhas são mais práticas de carro.

**Melhor época:** de abril a setembro, quando as chuvas são menos intensas. Evite trilhas em dias de chuva — o terreno argiloso de São Paulo se torna escorregadio rapidamente.

Para equipamentos básicos antes de sua primeira saída, leia nosso guia dos [10 itens essenciais para qualquer trilha](/blog/10-itens-essenciais-mochila-trekking) e, se for iniciante, não deixe de conferir [como começar no trekking](/blog/como-comecar-trekking-iniciante)."""

# A10 - como-comecar-trekking-iniciante (id=9, 81w -> 1200w)
expansions[9] = """O trekking é uma das atividades outdoor que mais cresce no Brasil — e por razões óbvias. Não exige habilidades técnicas especiais para começar, pode ser feito em praticamente todos os estados do país, e oferece uma experiência de imersão na natureza que caminhadas urbanas simplesmente não conseguem proporcionar. Se você chegou até aqui porque está pensando em fazer sua primeira trilha, está no lugar certo.

A boa notícia: começar no trekking é mais simples do que parece. A má notícia: a falta de planejamento básico arruína a experiência de muita gente logo na primeira saída — tornozelo torcido em tênis inadequado, desidratação, exaustão por escolher trilha acima do nível. Este guia vai te ajudar a evitar esses erros.

## O Que é Trekking, Afinal?

Trekking é qualquer caminhada em terreno natural não pavimentado com o objetivo de percorrer uma rota ou chegar a um destino específico. Isso abrange desde uma trilha de 3 km em parque municipal até uma travessia de 10 dias em altitude.

A diferença prática em relação a uma caminhada urbana é que o terreno exige mais atenção, o esforço físico é maior e, dependendo da localização, você vai estar distante de ajuda. Isso não significa perigo — significa que uma preparação mínima é necessária.

## Passo 1: Defina Que Tipo de Trilheiro Você Quer Ser

Antes de comprar qualquer equipamento, responda estas perguntas:

- **Você prefere trilhas de 1 dia ou quer acampar?** Trilhas de 1 dia são mais simples logisticamente. Camping abre um universo de possibilidades mas exige mais equipamento e planejamento.
- **Você gosta mais de paisagens abertas ou mata fechada?** Isso vai definir as regiões mais interessantes para você.
- **Você quer aventura intensa ou relaxamento ativo?** Trilhas de alta dificuldade com muito desnível são diferentes de trilhas panorâmicas tranquilas.

Não existe resposta certa. Mas saber o que você quer evita que você compre equipamento errado ou escolha trilhas incompatíveis com suas preferências reais.

## Passo 2: O Equipamento Mínimo Para a Primeira Trilha

Você não precisa gastar muito para começar. Para trilhas fáceis de 1 dia, o mínimo é:

**Calçado:** este é o único item onde não vale economizar. Um tênis de corrida urbano é inadequado para terreno irregular — amortecimento demais e sola lisa desliza em pedra molhada ou barro. Para começar sem investimento alto, um tênis de trilha básico (marcas como Merrell, Columbia ou Asics Trail) entre R$ 200–350 já resolve para trilhas fáceis. Bota só é necessária para trilhas longas ou com muito desnível.

**Mochila:** para trilhas de 1 dia, uma mochila de 20–25 litros é suficiente. Qualquer mochila de hiking básica funciona — só evite usar mochilas escolares ou de viagem que não têm suporte adequado para as costas.

**Roupas:** camisa de manga longa ou curta de material sintético (que seca rápido), calça ou bermuda leve, meia de trilha (evita bolhas melhor que meia comum), bom chapéu ou boné com proteção para o pescoço.

**Proteção solar:** protetor fator 70+, óculos de sol com proteção UV400.

**Água:** leve pelo menos 2 litros para uma trilha de até 4 horas. Mais detalhes em nosso guia de [hidratação em trilhas](/blog/hidratacao-trilha-quantos-litros).

**Lanterna ou celular carregado:** para segurança mínima, mesmo em trilhas curtas.

## Passo 3: Escolha a Trilha Certa Para o Seu Nível Atual

O erro mais comum de iniciantes é escolher uma trilha "ambiciosa" para a primeira saída — e sair com a memória de um sofrimento desnecessário. A primeira trilha deve ser aquela que deixa você querendo voltar.

Critérios para iniciantes absolutos:
- Distância total (ida e volta) de no máximo 6–8 km
- Desnível acumulado abaixo de 300 metros
- Trilha classificada como "fácil" pelo parque ou pela plataforma AllTrails
- Boa sinalização — nada de trilha que exige GPS ou mapa especializado
- Próxima a área urbana — para saídas próximas ao início da prática

Em São Paulo, trilhas como o Parque Estadual da Cantareira e a Pedra Grande em Atibaia são excelentes pontos de partida. No Rio de Janeiro, as trilhas do Parque Nacional da Tijuca têm opções fáceis acessíveis de metrô. Em Minas Gerais, o Parque Estadual do Itacolomi em Ouro Preto tem trilhas para todos os níveis.

## Passo 4: Condicione o Corpo Antes, Não Apenas Depois

Muita gente acha que vai "se condicionar fazendo trilhas". Isso funciona para trilhas fáceis curtas. Mas se você tem uma trilha específica em mente com alguma dificuldade, prepare o corpo antes.

Um programa simples de 4 semanas:
- Semanas 1–2: caminhadas de 45–60 minutos em terreno urbano, 3 vezes por semana
- Semanas 3–4: aumentar para 90 minutos e incluir escadas ou subidas no percurso

Isso não vai te deixar atleta, mas vai adaptar os joelhos, tornozelos e a musculatura das panturrilhas ao esforço de subida e descida — que é bem diferente de caminhar em terreno plano.

## Passo 5: Aprenda a Usar o AllTrails Antes de Sair

O AllTrails é o aplicativo de trilhas mais completo disponível no Brasil. Baixe o app, procure pela trilha que vai fazer e:
- Leia as resenhas mais recentes (dos últimos 60 dias) para saber as condições reais
- Baixe o mapa offline antes de sair — o app funciona sem internet com o mapa baixado
- Anote o tempo médio que outros trilheiros levaram no percurso

Aprenda também a usar o recurso de localização em tempo real. Em caso de desorientação, você consegue ver sua posição exata no mapa offline.

## Passo 6: Os Erros Mais Comuns de Iniciantes

**Sair tarde demais:** comece trilhas antes das 8h, especialmente no verão. Isso evita o pior calor do dia e dá margem de segurança para imprevistos.

**Não avisar ninguém:** antes de sair, mande mensagem para alguém informando a trilha, o horário de saída e o horário previsto de retorno.

**Subestimar o retorno:** subir é mais lento, mas descer é onde as lesões acontecem. As pernas trêmulas na descida após horas de caminhada são a causa número 1 de quedas.

**Não levar comida:** trilhas consomem muito mais calorias do que uma caminhada normal. Leve barras de cereais, frutas secas ou sanduíches para manter a energia.

**Trilhar só na primeira vez:** para a primeira experiência, prefira grupos de amigos ou grupos organizados de trilheiros. Muitas cidades têm grupos no Meetup.com ou no Facebook dedicados a trilhas para iniciantes.

## O Que Esperar da Primeira Trilha

Provavelmente você vai ter músculo dolorido nos 2 dias seguintes — especialmente coxa e panturrilha. Isso é normal e passa. Se você sentir dor nos joelhos durante a descida, diminua o passo e use bastões de trekking (pode improvisar com um galho grosso e resistente) para redistribuir o impacto.

E provavelmente você vai querer voltar. A sensação de chegar a um ponto de vista depois de uma hora de caminhada em mata fechada é difícil de descrever — e muito difícil de parar de buscar.

Para continuar aprendendo, confira nosso guia sobre [a diferença entre trekking e caminhada](/blog/o-que-e-trekking-diferenca-caminhada) e, quando estiver pronto para avançar, leia sobre [como planejar uma trilha de longo curso](/blog/planejamento-trilha-longo-curso-passo-a-passo)."""

# A11 - melhor-epoca-trilhas-brasil (id=16, 81w -> 1000w)
expansions[16] = """O Brasil é um país continental com 5 regiões climáticas distintas e uma variação de biomas que vai da floresta tropical úmida amazônica ao deserto de dunas do Maranhão. Isso significa que não existe uma única "melhor época" para trilhas no Brasil — existe a melhor época para cada região. Um erro de planejamento climático pode transformar a trilha dos sonhos em uma experiência de lama, chuva e frustração.

Este guia cobre as janelas ideais de visitação para as principais regiões e destinos de trekking do Brasil.

## Sudeste: Serra do Mar, Mantiqueira e Itatiaia

A região Sudeste concentra a maior parte dos trilheiros brasileiros e tem um clima de duas estações bem definidas: chuvosa (outubro a março) e seca (abril a setembro).

**Melhor época:** abril a setembro

Nesse período, as trilhas estão mais secas, o céu mais aberto e o risco de tempestades é mínimo. Os meses de junho e julho têm os dias mais curtos do ano, o que exige planejamento de horários, mas o clima é estável e previsível.

**Evitar:** dezembro a fevereiro, quando as chuvas de verão são intensas — especialmente na Serra dos Órgãos (RJ) e na Serra da Mantiqueira (MG/SP). Nesse período, deslizamentos, queda de barreiras e cheias de rios são riscos reais.

**Exceção:** o Pico da Bandeira e o Parque Nacional do Caparaó ficam bonitos com a névoa do verão, mas as trilhas ficam muito escorregadias. Apenas para trilheiros experientes.

## Nordeste: Chapada Diamantina, Lençóis Maranhenses e Litoral

O Nordeste tem uma lógica inversa ao Sudeste. As chuvas estão concentradas no primeiro semestre, com variações importantes por sub-região.

**Chapada Diamantina (BA):**
- Melhor época: junho a novembro (seco, cachoeiras ainda cheias de junho a setembro)
- Evitar: março a maio (chuvas intensas, trilhas fechadas)
- Nota: as cachoeiras ficam cheias até setembro, depois das chuvas de abril/maio. A combinação ideal é julho a agosto.

**Lençóis Maranhenses (MA):**
- Melhor época: julho e agosto, quando as lagoas entre as dunas estão cheias das chuvas de março a junho
- A travessia dos Lençóis Maranhenses precisa das lagoas — sem elas, é apenas areia quente

**Litoral nordestino (RN, CE, PI):**
- Melhor época: agosto a dezembro (ventos alísios garantem temperatura agradável e praias exuberantes)
- Trilhas costeiras como os Lençóis de Paracuru são mais agradáveis nessa janela

## Centro-Oeste: Chapada dos Veadeiros e Pantanal

**Chapada dos Veadeiros (GO):**
- Melhor época: maio a setembro (seco, cachoeiras acessíveis)
- Evitar: outubro a março (chuvas de verão intensas, trilhas fechadas pelo parque frequentemente)
- Diferencial: a Chapada dos Veadeiros tem uma concentração extraordinária de raios durante as chuvas de verão — a região registra um dos maiores índices de descargas elétricas do planeta

**Pantanal (MT/MS):**
- Melhor época para fauna: julho e agosto (seco, animais concentrados nas poucas fontes d'água)
- Melhor época para flora e paisagem: fevereiro e março (cheia, Pantanal alagado, paisagem extraordinária)
- Para trilhas de longo curso, prefira o período seco (junho a outubro)

## Sul: Serra Gaúcha, Cânions e Litoral Catarinense

**Cânions do Sul (RS/SC) — Itaimbezinho e Fortaleza:**
- Melhor época: setembro a março (verão e início do outono, temperaturas agradáveis)
- Evitar: junho e julho (inverno intenso, chuvas, neblina que fecha os cânions)
- Nota: as geadas de inverno criam paisagens belíssimas no cânion, mas tornam as trilhas perigosas

**Serra Gaúcha (Gramado, Canela, São Francisco de Paula):**
- Melhor época para quem quer frio e inverno: junho a agosto
- Melhor época para trilhas confortáveis: setembro a novembro (outono/primavera)

**Litoral de Santa Catarina:**
- Trilhas costeiras como a [Trilha das Praias Rosa Norte–Sul](/trilha/trilha-das-praias-rosa-norte-sul) são melhores em março e abril — após o verão lotado, com mar ainda quente e fluxo menor de turistas

## Norte: Amazônia e Monte Roraima

A Amazônia e Roraima têm as condições mais extremas do Brasil para planejamento climático.

**Monte Roraima (RR):**
- Melhor época: dezembro a março (menos chuvas no planalto, apesar de ser verão)
- Evitar: junho a setembro (período de maior precipitação, trilhas podem ficar intransitáveis)
- Importante: o topo do Roraima tem chuva e neblina durante boa parte do ano independente da estação

**Amazônia Central (AM):**
- Melhor época para trilhas de selva: agosto a novembro (seco, nível dos rios baixo, acesso facilitado)
- Cheia (fevereiro a junho): impossibilita trilhas de terra, mas cria o fenômeno do "igapó" — a floresta inundada navegável de canoa

## Ferramenta Prática: Como Checar o Clima Antes de Ir

Para qualquer destino de trekking no Brasil:
1. Consulte o site do INMET (inmet.gov.br) para previsão de até 5 dias
2. Use o Climatempo para previsão de 15 dias por cidade próxima à trilha
3. Leia resenhas recentes no AllTrails — trilheiros deixam registros das condições reais
4. Ligue para a sede do parque 2 a 3 dias antes — eles sabem o estado atual das trilhas

Para planejamento de viagem mais detalhado, consulte nosso guia de [planejamento de trilha de longo curso](/blog/planejamento-trilha-longo-curso-passo-a-passo) e, se for a primeira vez em alguma dessas regiões, considere contratar um [guia CADASTUR local](/blog/guia-cadastur-como-encontrar)."""

# A12 - trilhas-santa-catarina (id=19, 81w -> 1000w)
expansions[19] = """Santa Catarina é um estado que surpreende quem olha além de Florianópolis e Balneário Camboriú. No extremo norte, na divisa com o Paraná, o Parque Nacional de Aparados da Serra guarda um dos espetáculos geológicos mais impressionantes da América do Sul — cânions de basalto com mais de 700 metros de profundidade. No centro-oeste, a Serra Catarinense tem paisagens de campos de altitude que lembram os Andes. No litoral sul, praias selvagens acessíveis apenas a pé guardam alguns dos trechos mais bonitos da costa brasileira.

Este guia apresenta os melhores destinos de trekking de Santa Catarina, com informações práticas para planejar sua visita.

## Cânion Itaimbezinho — O Mais Impressionante do Brasil

Localizado no Parque Nacional de Aparados da Serra, o [Cânion Itaimbezinho](/trilha/canion-itaimbezinho) é o destino mais emblemático de Santa Catarina para trilheiros. Com 5,8 km de extensão, paredes de basalto que chegam a 720 metros de altura e a fenda mais estreita de qualquer cânion da América do Sul, o Itaimbezinho é uma experiência geológica única.

**Trilha do Cotovelo (fácil):** 2,4 km ida e volta ao primeiro mirante. Desnível mínimo, adequada para todas as idades. Oferece a primeira visão da fenda do cânion — já impactante o suficiente para justificar a viagem.

**Trilha do Vértice (moderado):** 6 km circular pelo paredão superior do cânion. Desnível de 200m, com mirantes sucessivos ao longo do percurso. Recomenda-se guia para grupos iniciantes.

**Trilha Cotovelo–Vértice completa:** nossos dados incluem a [Trilha do Cotovelo e Vértice](/trilha/trilha-cotovelo-vertice-itaimbezinho-cambara-do-sul-rs) como uma das rotas mais completas da região.

**Como chegar:** o parque fica em Cambará do Sul (RS), mas a gestão se estende ao lado catarinense. A partir de Florianópolis são cerca de 5 horas de carro pela BR-116.

**Reserva:** obrigatória pelo site do ICMBio. Capacidade limitada a 800 visitantes por dia.

## Cânion Fortaleza — A Alternativa Menos Conhecida

A menos de 30 km do Itaimbezinho, o [Cânion Fortaleza](/trilha/canion-fortaleza) é, por muitos critérios técnicos, ainda mais impressionante. Com 1.800 metros de comprimento e paredões que chegam a 900 metros de altura, é o maior cânion em profundidade do Brasil.

A trilha principal tem 8 km ida e volta com desnível de 300 metros. O ponto de destaque é a Cachoeira do Tigre Preto, que despenca do planalto para o cânion em queda livre de quase 800 metros.

**Quando ir:** setembro a março, quando o clima é mais estável. Evite o inverno (junho a agosto) — neblina intensa pode fechar os mirantes por dias.

## Serra Catarinense: Trekking em Altitude

A Serra Catarinense, com cidades como Urubici, Bom Retiro e São Joaquim, tem alguns dos campos de altitude mais belos do Sul do Brasil. Em altitude entre 900 e 1.800 metros, a paisagem muda completamente em relação ao litoral — araucárias, campos com grama baixa e, no inverno, a única neve natural do Brasil.

**Morro da Igreja — Urubici:** 1.822 metros de altitude, o ponto mais alto de Santa Catarina. A trilha tem 6 km ida e volta com desnível de 400 metros. No inverno, as geadas criam paisagens de gelo e neblina únicas.

**Cascata do Avencal:** cascata de 100 metros a 7 km de Urubici. Trilha de 4 km fácil, adequada para famílias. Uma das mais fotografadas do Sul.

**Pico da Boa Vista — São Joaquim:** o segundo ponto mais alto de SC (1.793m). Trilha técnica de 10 km para trilheiros experientes, com vista para os municípios vizinhos em dias claros.

## Litoral Sul: Trilhas Costeiras Entre Praias Selvagens

O litoral sul de Santa Catarina, entre Imbituba e Laguna, guarda uma das costas menos desenvolvidas do estado. Praias como Rosa, Silveira e Gamboa são acessíveis apenas a pé pela [Trilha das Praias Rosa Norte–Sul](/trilha/trilha-das-praias-rosa-norte-sul) — um percurso de 12 km em ambiente de restinga e mata atlântica costeira.

A trilha não tem dificuldade técnica, mas exige boa hidratação (não há fonte d'água no percurso) e respeito com os horários — a última praia é acessível apenas com maré baixa.

## Parque Nacional da Serra do Itajaí

Menos conhecido que o Aparados da Serra, o Parque Nacional da Serra do Itajaí fica na região de Indaial e Blumenau, a apenas 1 hora de Florianópolis. O parque protege um remanescente contínuo de Mata Atlântica com mais de 57.000 hectares.

As trilhas internas têm dificuldade fácil a moderada, com destaque para a Trilha da Cachoeira do Saltão (6 km) e a Trilha da Pedra do Macaco (4 km). A fauna é diversificada, com avistamentos frequentes de tucanos, tamanduás e até onça-parda.

## Dicas de Infraestrutura

**Hospedagem:** Urubici e Cambará do Sul (para o Aparados) têm boa rede de pousadas e camping. Em alta temporada (dezembro a fevereiro no litoral, julho nos cânions para ver geada), reserve com 2 a 3 meses de antecedência.

**Equipamento:** para cânions no inverno, leve camadas de lã e impermeável — a neblina molha mais do que qualquer chuva. Para Serra Catarinense no inverno, gear de temperatura negativa pode ser necessário.

**Guias:** a Associação de Guias da Serra Catarinense atua em Urubici e arredores. Para o Aparados, guias locais de Cambará do Sul conhecem as condições dos cânions como ninguém.

Para mais destinos no Sul do Brasil, confira nossas [trilhas e cânions do Rio Grande do Sul](/blog/melhores-trilhas-rs-canyons) e o guia sobre [como escolher a melhor época para trilhas no Brasil](/blog/melhor-epoca-trilhas-brasil)."""

print("Batch 3 expansions defined.")

for post in data:
    if post['id'] in expansions:
        post['content'] = expansions[post['id']]

with open('data/blog.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Batch 3 written to blog.json")

for post in data:
    if post['id'] in expansions:
        words = len(post['content'].split())
        print(f"ID {post['id']} | {words}w | {post['slug']}")
