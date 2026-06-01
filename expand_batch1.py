#!/usr/bin/env python3
import json

with open('data/blog.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

expansions = {}

# A1 - trekking-com-cachorro-guia-completo (id=8, 33w -> 1000w)
expansions[8] = """Levar seu cão para trilhas é possível e recompensador, mas exige preparação progressiva, equipamentos adequados, conhecimento dos riscos de saúde e respeito pelas regras das áreas naturais. Um guia honesto para tutores responsáveis.

## Por Que Trilhar Com Cachorro é Diferente de Uma Caminhada no Parque

A diferença entre passear com seu cão no parque da cidade e trilhar com ele em uma área natural é enorme — e muitos tutores descobrem isso da pior forma, no meio do percurso. Na natureza, seu cão vai encontrar terreno irregular, calor intenso, distâncias muito maiores do que está acostumado, outros animais silvestres, plantas tóxicas e ausência de veterinários por perto.

Isso não significa que trilhar com cachorro é perigoso por natureza. Significa que exige uma preparação que vai além de "o meu cachorro adora passear". Um cão de 5 kg com problemas articulares não tem o mesmo perfil de trilheiro que um border collie de 18 kg acostumado a correr. Raça, idade, condicionamento físico e temperamento importam muito.

## Condicionamento Físico Progressivo: Comece Antes da Trilha

Assim como você não sai do sedentarismo direto para uma trilha de 20 km, seu cão também precisa de condicionamento progressivo. Se ele está acostumado com passeios de 30 minutos por dia, não espere que ele faça 12 km sem sofrimento.

Um plano básico de 8 semanas funciona assim:
- Semanas 1–2: aumentar passeios diários para 45–60 minutos em terreno variado
- Semanas 3–4: incluir subidas e descidas em parques ou morros acessíveis
- Semanas 5–6: fazer trilhas curtas de 5–7 km para testar resistência e patas
- Semanas 7–8: trilhas de 8–10 km com simulação das condições esperadas

Preste atenção em sinais de esforço excessivo: ofegamento muito intenso, língua branca ou azulada, relutância em continuar, claudicação ou lambidas excessivas nas patas após a trilha.

## Equipamentos Essenciais Para Cães em Trilha

A lista de equipamentos para seu cão é quase tão importante quanto a sua:

**Coleira, peitoral e guia:** Em trilhas onde cães devem ficar presos, use uma guia extensível de no máximo 2 metros ou uma guia curta de 1 metro. Peitoral é mais seguro do que coleira para evitar pressão no pescoço em subidas.

**Água e vasilha:** Leve água exclusiva para o cão. Cães de médio porte precisam de cerca de 60 ml de água por kg de peso por hora de atividade moderada em dia quente. Ou seja, um cão de 15 kg pode precisar de 900 ml por hora. Uma vasilha dobrável de silicone pesa poucos gramas e resolve.

**Protetor de patas:** Paralelepípedos quentes, pedras afiadas e asfalto podem machucar as almofadas plantares. Bota de silicone ou cera protetora de patas (como a da marca Musher's Secret) ajudam bastante.

**Coleira com identificação:** Em área aberta, um segundo de distração pode resultar em um cão perdido. Identificação com nome e telefone é obrigatória.

**Kit de primeiros socorros canino:** Inclua pinça para carrapatos, soro fisiológico, curativo, esparadrapo e o número de um veterinário de plantão da cidade mais próxima.

## Regras das Áreas Naturais: Onde Cães São Permitidos

Este é o ponto onde mais tutores se frustram: a maioria dos parques nacionais brasileiros não permite a entrada de cães. O IBAMA proíbe animais domésticos em unidades de conservação de proteção integral — o que inclui a maioria dos parques nacionais — exatamente para proteger a fauna silvestre do impacto dos animais domésticos.

Parques onde cães geralmente **não** são permitidos:
- Parque Nacional da Serra dos Órgãos (RJ)
- Parque Nacional do Itatiaia (RJ/MG)
- Parque Nacional da Chapada Diamantina (BA)
- Parque Nacional da Serra da Canastra (MG)

Áreas onde cães geralmente **são** aceitos (verifique sempre antes):
- Parques estaduais com regulamentação própria
- Propriedades privadas com trilhas abertas ao público
- Trilhas municipais em cidades como Florianópolis e Curitiba
- Algumas áreas de proteção ambiental (APAs) com regras mais flexíveis

Antes de qualquer saída, consulte o site ou telefone da unidade de gestão da área. Não confie apenas em relatos de outros trilheiros nas redes sociais — as regras mudam.

## Riscos de Saúde Específicos Para Cães em Trilha

**Carrapatos:** O risco maior em trilhas brasileiras. Carrapatos do gênero Amblyomma podem transmitir febre maculosa, uma doença grave e potencialmente fatal. Use repelente específico para cães (consulte seu veterinário) e faça uma inspeção completa do animal ao fim de cada trilha.

**Leptospirose:** Presente em rios e poças d'água contaminados por urina de animais silvestres. A vacina anual é obrigatória e protege bem. Evite que seu cão beba de fontes naturais sem filtração.

**Hipotermia e superaquecimento:** Cães regulam temperatura pela respiração e pelas patas. Em dias quentes acima de 28°C, o risco de superaquecimento é alto. Evite trilhar entre 10h e 16h. Em dias frios e úmidos, especialmente para raças de pelo curto, uma capa leve pode ser necessária.

**Plantas tóxicas:** Diversas plantas da flora brasileira são tóxicas para cães. Se seu cão ingerir alguma planta desconhecida e apresentar vômito, salivação excessiva ou letargia, procure veterinário o mais rápido possível.

## A Etiqueta do Trilheiro com Cachorro

Além das regras formais, há uma etiqueta informal que todo tutor responsável deve conhecer:

Mantenha seu cão na guia sempre que outros trilheiros estiverem por perto. Nem todo mundo é fã de cachorros, e crianças podem se assustar. Nem todo cão fica feliz com a aproximação de um estranho, mesmo que seu cão seja dócil.

Recolha sempre as fezes do seu cão. Sim, na natureza também. Use sacos biodegradáveis e leve para um lixo. As fezes de cães domésticos contêm patógenos que não pertencem àquele ecossistema.

Não deixe seu cão perseguir animais silvestres. Mesmo que não os alcance, o estresse causado à fauna local é real e prejudicial.

## Quando Deixar o Cachorro em Casa

Nem toda trilha é adequada para cães. Seja honesto na avaliação:

- Trilhas com mais de 15 km em dias quentes: alto risco de superaquecimento
- Trilhas com terreno técnico (escalada, rappel): risco de lesão grave
- Cão idoso, com artrite ou problemas cardíacos: consulte o veterinário antes
- Trilhas que cruzam unidades de conservação fechadas para animais: não arrisque a multa nem o impacto ambiental

Para saber mais sobre como planejar sua saída com segurança, leia nosso guia [como escolher uma trilha segura no Brasil](/blog/como-escolher-trilha-segura-brasil) e conheça as [regras de segurança em trilhas](/blog/seguranca-trilha-regras) que todo trilheiro deve seguir.

Trilhar com seu cão pode ser uma das experiências mais especiais da sua vida como tutor. Com preparação adequada, respeito às regras e atenção à saúde do animal, você e seu companheiro podem explorar trilhas incríveis juntos — de forma segura e responsável."""

# A2 - como-escolher-trilha-segura-brasil (id=7, 45w -> 1000w)
expansions[7] = """A escolha errada da trilha é um dos principais fatores de risco em atividades outdoor no Brasil. Aprenda a avaliar seu nível de preparo, pesquisar rotas com fontes confiáveis, entender os sistemas de classificação de dificuldade e tomar decisões mais conscientes antes de cada saída.

## Por Que a Escolha da Trilha é Uma Decisão de Segurança

A maioria das pessoas que precisam de resgate em trilhas brasileiras não cometeu um erro durante o percurso. Cometeu um erro antes de sair de casa: escolheu uma trilha acima da sua capacidade atual, ou escolheu uma trilha sem informações suficientes sobre as condições reais do terreno.

O Brasil tem mais de 2.000 trilhas cadastradas em sistemas como Wikiloc, AllTrails e Trilhas Brasil — e um número ainda maior de rotas não oficiais que circulam em grupos de WhatsApp e fóruns. Saber filtrar essa informação é uma habilidade fundamental.

## Os Sistemas de Classificação de Dificuldade Usados no Brasil

Não existe um sistema nacional único padronizado para classificação de trilhas no Brasil. Os parques nacionais geralmente usam uma escala própria (fácil, moderado, difícil, muito difícil), enquanto plataformas digitais usam algoritmos que consideram distância e desnível. Isso cria inconsistências.

**O que avaliar além da classificação:**

- **Distância total:** considere sempre o percurso de ida E volta, não apenas um sentido
- **Desnível acumulado:** mais relevante que a distância para determinar o esforço real. Uma trilha de 8 km com 800m de desnível é muito mais exigente que uma de 12 km plana
- **Tipo de terreno:** pedra, barro, raízes, areia — cada um exige habilidade e equipamento diferente
- **Exposição:** trilhas abertas em cristas ou chapadas expõem a vento, chuva e raios de forma bem diferente de trilhas fechadas em mata

**Regra prática para iniciantes:** se você nunca fez trilha, comece com percursos de até 8 km, desnível acumulado abaixo de 400m e classificação "fácil" segundo o parque ou área. Faça isso por pelo menos 3 a 5 saídas antes de avançar para trilhas moderadas.

## Fontes Confiáveis Para Pesquisar Trilhas no Brasil

**Sites e aplicativos:**
- **AllTrails:** a maior base de dados de trilhas do mundo, com resenhas e fotos recentes de outros trilheiros. Tem boa cobertura das principais trilhas brasileiras
- **Wikiloc:** forte em trilhas mapeadas por GPS, com arquivos GPX para download
- **Trilhas Brasil:** foco em trilhas nacionais, com informações sobre parques e unidades de conservação
- **Meu Parque:** sistema oficial do ICMBio com informações sobre parques nacionais

**O que verificar nas resenhas:**
Priorize resenhas recentes (dos últimos 90 dias). Uma trilha pode estar excelente em junho e intransitável em fevereiro depois das chuvas. Leia especificamente sobre condições do terreno, sinalização e tempo de percurso real.

**Contato direto com o parque:**
Para trilhas em parques nacionais ou estaduais, ligue ou mande e-mail para a sede administrativa. Pergunte sobre condições atuais, necessidade de reserva e se há restrições em vigor. Essa informação raramente está atualizada nos aplicativos.

## Como Avaliar Seu Nível de Preparo

Autopercepção é o maior risco. A maioria das pessoas superestima sua capacidade física quando está motivada a fazer uma trilha específica. Use esses critérios objetivos:

**Nível iniciante:**
- Consegue caminhar 5 km sem pausas longas em terreno urbano
- Nunca fez trilha em área natural ou fez poucas vezes
- Não tem equipamento específico (bota, mochila, bastões)

**Nível intermediário:**
- Faz trilhas regularmente (ao menos 1 por mês)
- Consegue completar 10–12 km com mochila de 6–8 kg sem problemas
- Já enfrentou chuva, frio ou terreno técnico em campo

**Nível avançado:**
- Treina regularmente para trekking (caminhadas longas, subidas com peso)
- Já fez travessias de múltiplos dias
- Sabe navegação básica sem depender exclusivamente de GPS

Seja honesto. Escolha trilhas no seu nível atual, não no nível que você aspira ter.

## Verificação da Previsão do Tempo: Um Passo Que Muitos Pulam

No Brasil, a variação climática entre regiões é enorme e as mudanças rápidas de tempo são comuns, especialmente na Serra da Mantiqueira, Serra dos Órgãos e Chapada Diamantina. Uma manhã ensolarada pode virar uma tarde de tempestade.

Use o [INMET](https://www.inmet.gov.br) ou o Climatempo para verificar a previsão dos 3 dias anteriores à trilha e do dia da saída. Em parques serranos, chuva significa trilha escorregadia, risco de hipotermia e, em casos extremos, risco de queda de barreira.

Critérios para adiar ou cancelar:
- Chuva prevista acima de 20mm no dia da trilha em área serrana
- Vento acima de 40 km/h em trilhas de crista ou expostas
- Qualquer alerta meteorológico do INMET em vigor para a região

## O Protocolo Antes de Sair: Comunicação de Emergência

Independente do nível da trilha, sempre:

1. **Informe alguém:** deixe o nome da trilha, horário de saída previsto e horário de retorno previsto com uma pessoa de confiança fora do grupo
2. **Defina um horário de alerta:** se não entrar em contato até X horas, essa pessoa deve ligar para o Corpo de Bombeiros
3. **Salve o número de resgate:** Corpo de Bombeiros (193), SAMU (192) e o telefone do parque

Para trilhas mais longas, considere alugar ou comprar um dispositivo de comunicação via satélite como o Garmin inReach — que funciona mesmo sem cobertura de celular.

Consulte também nosso guia completo sobre [segurança em trilhas e regras essenciais](/blog/seguranca-trilha-regras) e, se for a primeira vez, considere contratar um [guia certificado pelo CADASTUR](/blog/guia-cadastur-como-encontrar) para ter apoio profissional no campo.

## Checklist Final Antes de Confirmar Sua Trilha

- [ ] Pesquisei a trilha em pelo menos 2 fontes diferentes
- [ ] Li resenhas recentes (últimos 90 dias)
- [ ] Verifiquei se precisa de reserva ou autorização prévia
- [ ] A classificação de dificuldade é compatível com meu nível atual
- [ ] Verifiquei a previsão do tempo para os próximos 3 dias
- [ ] Sei a distância, desnível e tempo estimado de percurso
- [ ] Tenho todo o equipamento necessário para esse tipo de trilha
- [ ] Informei alguém sobre minha saída, rota e horário de retorno

Escolher bem é a primeira e mais importante decisão de qualquer saída. Faça esse trabalho antes de calçar as botas."""

# A3 - trilha-com-cachorro-regras (id=21, 73w -> 900w)
expansions[21] = """Levar seu cachorro para trilhas é uma das experiências mais gratificantes que um tutor pode ter com seu pet. Ver um cão descobrindo cheiros, texturas e sons completamente novos com entusiasmo genuíno tem uma qualidade especial que qualquer pessoa com cão entende imediatamente. Mas trilhar com cachorro também exige preparação específica, respeito rigoroso pelas regras das áreas naturais e consciência sobre o impacto que animais domésticos podem ter nos ecossistemas.

O ponto mais importante — e mais ignorado — é verificar antecipadamente se cães são permitidos na área que você vai visitar. Muitos tutores chegam à portaria de um parque nacional com o cachorro no banco de trás e descobrem na hora que animais domésticos são proibidos por lei.

## A Regra Mais Importante: Verificar Antes de Ir

A legislação brasileira proíbe animais domésticos em unidades de conservação de proteção integral, categoria que inclui a maioria dos parques nacionais. Essa regra existe para proteger a fauna silvestre: mesmo cães dóceis e bem adestrados podem causar estresse em animais silvestres, transmitir doenças para a fauna local e perturbar ninhos, tocas e territórios de reprodução.

Isso significa que trilhas em parques como Itatiaia, Serra dos Órgãos, Chapada Diamantina e Caparaó estão, em princípio, fechadas para cães. A infração pode gerar multa e apreensão do animal.

Onde cães costumam ser aceitos:
- Parques municipais e estaduais com regulamentação própria
- Trilhas em Áreas de Proteção Ambiental (APAs) com regras específicas
- Propriedades privadas que abrem trilhas ao público
- Trilhas municipais de cidades como Florianópolis, Curitiba e São Paulo

Sempre confirme com antecedência telefonando ou consultando o site da unidade gestora.

## Guia na Mão o Tempo Todo

Mesmo em áreas onde cães são permitidos, manter o animal na guia não é apenas etiqueta — é uma regra formal na maioria dos locais e uma questão de segurança. Cães soltos em trilhas podem:

- Perseguir animais silvestres e se perder
- Atacar outros cães ou trilheiros com medo de animais
- Cair em barrancos, pedras ou rios em terreno desconhecido
- Contaminar fontes de água com fezes

Use guia de no máximo 2 metros. Em trechos de subida técnica, opte por guia curta para ter mais controle sobre o animal.

## Hidratação e Alimentação no Campo

Cães se desidratam mais rápido do que humanos em atividade física intensa. O sinal mais claro é o ofegamento excessivo, mas não espere chegar nesse ponto. Ofereça água a cada 30–40 minutos durante a trilha, especialmente em dias quentes.

Leve o dobro do que você acha que vai precisar. Para um cão de 15 kg, calcule pelo menos 500 ml por hora de trilha em dias amenos e até 900 ml em dias quentes.

Nunca deixe seu cão beber de rios, poças ou córregos sem filtração. O risco de leptospirose é real e a doença pode ser fatal para cães não vacinados.

## Inspeção Pós-Trilha: Carrapatos e Lesões

Assim que chegar ao carro ou acampamento, faça uma varredura completa no cão: foque em orelhas, pescoço, axilas, virilhas e entre os dedos. Carrapatos se instalam nessas regiões e podem transmitir febre maculosa.

Use uma pinça própria para remoção de carrapatos — nunca torça nem esmague. Após remover, desinfete a área com antisséptico.

Verifique também as almofadas das patas. Pedras afiadas, areia quente e asfalto podem causar cortes ou queimaduras que o cão só vai demonstrar dias depois.

## A Questão das Fezes: Sem Exceção

Recolher as fezes do seu cão é obrigação em qualquer área natural, não apenas nas calçadas da cidade. As fezes de cães domésticos introduzem patógenos, hormônios e bactérias que não pertencem ao ecossistema local e podem afetar a fauna e a flora.

Leve sacos biodegradáveis em quantidade suficiente. Se não houver lixo disponível no percurso, carregue os sacos fechados até encontrar um.

## Temperamento e Sociabilização

Nem todo cão está preparado para trilha do ponto de vista comportamental. Um cão reativo com outros cães ou com pessoas vai transformar a experiência em estresse constante. Um cão que late compulsivamente vai perturbar outros trilheiros e assustar a fauna local.

Avalie honestamente o temperamento do seu cão antes de levá-lo para uma trilha movimentada. Trilhas mais desertas e curtas são um bom começo para testar como o animal reage ao ambiente.

Para saber mais sobre equipamentos e preparação, veja nosso [guia completo de trekking com cachorro](/blog/trekking-com-cachorro-guia-completo) e confira as [trilhas mais acessíveis do estado de São Paulo](/blog/trilhas-faceis-sao-paulo) como opções para primeiras saídas com pets."""

# A4 - como-planejar-trilha-grupo (id=24, 73w -> 900w)
expansions[24] = """Trilhar com amigos ou família tem uma qualidade especial que a trilha solo não consegue replicar — a experiência compartilhada de superar um desafio juntos, as conversas que o ritmo da caminhada facilita, a celebração coletiva no topo. Mas trilhas em grupo têm uma característica que pode transformar a experiência em frustração: o atrito entre expectativas, capacidades físicas e preferências de diferentes pessoas.

Grupos mal planejados geram os problemas mais clássicos do trekking coletivo: o grupo se fragmenta pelo ritmo, alguém não estava preparado para a dificuldade, a logística de transporte virou um caos no dia anterior, ou metade do grupo queria acampar e a outra metade queria voltar no mesmo dia.

## O Primeiro Passo: Nivelar as Expectativas do Grupo

Antes de escolher qualquer trilha, tenha uma conversa franca com todos os participantes sobre três pontos:

**Capacidade física atual:** não o que cada um acha que consegue, mas o que efetivamente treinou nos últimos meses. Uma pessoa que não caminha regularmente vai sofrer em qualquer trilha acima de 10 km, independente de boa vontade.

**Disponibilidade de equipamento:** tênis de corrida urbano não é calçado para trilha. Se alguém do grupo não tem equipamento mínimo, a trilha precisa ser simples o suficiente para esse perfil, ou o equipamento precisa ser providenciado antes.

**Expectativa de experiência:** alguns querem desafio e suor, outros querem paisagem e descanso. Grupos mistos se dão melhor em trilhas de dificuldade moderada com pontos de interesse ao longo do percurso.

## Como Escolher a Trilha Certa Para o Grupo

A regra de ouro de planejamento de trilha em grupo é simples: **adapte a trilha ao participante menos preparado, não ao mais experiente**.

Isso pode ser frustrante para trilheiros experientes, mas é o que mantém o grupo coeso e garante que ninguém se machuque ou fique para trás com exaustão. Um grupo que termina a trilha junto, mesmo que numa rota mais curta, tem uma experiência muito melhor do que um grupo que se fragmenta numa rota ambiciosa.

Critérios para escolha:
- Distância compatível com o participante com menos condicionamento
- Desnível acumulado abaixo de 400m para grupos com iniciantes
- Trilha com boa sinalização ou familiaridade prévia do líder com a rota
- Possibilidade de retorno antecipado se alguém não conseguir continuar

## Logística de Transporte e Encontro

A logística de grupos é onde mais planos desmoronam na véspera. Defina com antecedência:

**Ponto de encontro:** escolha um local de fácil acesso e que todos conheçam. Evite pontos de encontro "na trilha" — se alguém se atrasar, o grupo inteiro espera ou parte sem ele.

**Divisão de carros:** planeje a distribuição de vagas com antecedência. Quem tem carro maior leva mais gente. Defina também o sistema de divisão de combustível antes.

**Horário de saída real:** se o grupo combina 7h, parte das pessoas vai chegar às 7h30. Decida com honestidade qual é o horário real de partida e mantenha-o.

**Trilhas de acesso:** se o ponto de partida exige estrada de terra ou GPS específico, certifique-se de que o motorista de cada carro tem as coordenadas salvas offline antes de sair de casa.

## Divisão de Responsabilidades no Grupo

Em grupos sem guia profissional, distribua papéis antes da saída:

**Líder de rota:** a pessoa com mais experiência na trilha específica ou com melhor conhecimento de navegação. Vai na frente, mantém o ritmo e monitora a sinalização.

**Varredor:** fica na retaguarda, garante que ninguém fique para trás e faz a contagem do grupo em pontos de descanso.

**Responsável pela comunicação de emergência:** tem os contatos de resgate salvos, sabe a localização do grupo e é o ponto de contato para a pessoa avisada fora do grupo.

**Porta-kit de primeiros socorros:** carrega o kit e sabe usar os itens básicos.

## Ritmo e Pausas: O Maior Desafio de Grupos

O ritmo é a principal fonte de tensão em trilhas em grupo. Trilheiros mais rápidos se frustram esperando, trilheiros mais lentos se estressam tentando acompanhar o grupo.

Estratégias que funcionam:
- **Defina pontos de encontro:** em vez de todos caminharem juntos, os mais rápidos vão na frente e esperam no próximo ponto de referência (bifurcação, mirador, início de subida)
- **Regra das pausas:** pausa coletiva a cada 60–90 minutos de caminhada, com duração de 10–15 minutos. Todos param juntos, todos comem e bebem
- **Ritmo do mais lento na subida:** em subidas técnicas, o grupo inteiro adota o ritmo do participante mais lento. Esse não é um ponto de negociação

## Comunicação Durante a Trilha

Em trilhas com cobertura de celular, crie um grupo de WhatsApp com todos os participantes antes de sair. Se alguém se perder ou precisar de ajuda, a comunicação é imediata.

Em trilhas sem cobertura, combine sinais visuais e sonoros simples: dois apitos = "parar e esperar", três apitos = "emergência, venham todos".

Para trilhas mais longas com grupos maiores, um rádio comunicador portátil entre o líder de frente e o varredor de retaguarda pode ser muito útil.

Consulte nosso guia de [segurança em trilhas](/blog/seguranca-trilha-regras) e nosso guia sobre [como começar no trekking para iniciantes](/blog/como-comecar-trekking-iniciante) para complementar o planejamento da sua saída em grupo."""

print("Batch 1 expansions defined.")

for post in data:
    if post['id'] in expansions:
        post['content'] = expansions[post['id']]

with open('data/blog.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Batch 1 written to blog.json")

# Verify word counts
for post in data:
    if post['id'] in expansions:
        words = len(post['content'].split())
        print(f"ID {post['id']} | {words}w | {post['slug']}")
