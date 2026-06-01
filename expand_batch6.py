#!/usr/bin/env python3
import json

with open('data/blog.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

expansions = {}

# B5 - travessia-petropolis-teresopolis-guia-completo (id=1, 318w -> 900w)
expansions[1] = """A Travessia Petrópolis x Teresópolis é, sem dúvida, a trilha de longo curso mais famosa do Brasil. São 30 km de pura Mata Atlântica, com picos rochosos, abrigos históricos e paisagens que tiram o fôlego. Se você está planejando fazer essa travessia, este guia vai te preparar para cada passo.

## Onde Fica e Como Chegar

A trilha está localizada no Parque Nacional da Serra dos Órgãos, no estado do Rio de Janeiro. O ponto de partida clássico é a sede de Petrópolis do parque, acessível de carro ou ônibus a partir do Rio de Janeiro. O ponto de chegada é a sede de Teresópolis, de onde você pode pegar transporte de volta.

A maioria das pessoas opta por fazer a travessia no sentido Petrópolis → Teresópolis, pois o ganho de altitude é mais gradual nesse sentido. De carro, a sede de Petrópolis fica a cerca de 70 km do centro do Rio de Janeiro, pela BR-040. De ônibus, a Viação 1001 opera linhas regulares de Novo Rio para Petrópolis.

## O Que Esperar no Percurso

O percurso é dividido em três dias recomendados:

- **Dia 1:** Sede de Petrópolis → Abrigo 2 (aprox. 12 km, desnível positivo de 1.100m)
- **Dia 2:** Abrigo 2 → Abrigo 4 (aprox. 10 km), com ascensão ao Pico do Sino (2.263m)
- **Dia 3:** Abrigo 4 → Sede de Teresópolis (aprox. 8 km, desnível negativo de 1.200m)

Trilheiros com bom condicionamento completam em 2 dias, mas 3 dias permitem aproveitar melhor a paisagem e chegar com energia ao Pico do Sino.

O desnível acumulado total é de aproximadamente 2.100 metros de positivo e 2.100 metros de negativo. Esse dado é mais relevante para avaliar a dificuldade do que a distância bruta.

## Infraestrutura dos Abrigos

O parque mantém 4 abrigos numerados ao longo do percurso. Cada abrigo tem:
- Dormitório com beliches e colchonetes (leve saco de dormir)
- Cozinha simples com fogão e gás
- Banheiros com chuveiro frio
- Fonte de água potável

**Reserva obrigatória:** os abrigos têm capacidade limitada e precisam ser reservados antecipadamente pelo site do ICMBio. Em fins de semana e feriados, a demanda é alta — reserve com 30 a 60 dias de antecedência.

Além dos abrigos, é possível montar barraca nas áreas designadas próximas a cada abrigo — boa alternativa para quem prefere mais privacidade.

## As Principais Dificuldades da Travessia

**Pico do Sino no Dia 2:** a ascensão ao Pico do Sino (2.263m) pelo lado norte tem trechos de granito vertical onde são necessárias as mãos. Não chega a ser escalada técnica, mas exige confiança em terreno exposto. Em dia de nevoeiro ou chuva, esse trecho é especialmente desafiador.

**Descida para Teresópolis no Dia 3:** o trecho de descida após o Abrigo 4 é longo, com muito desnível e pedras irregulares que castigam os joelhos. Bastões de trekking são altamente recomendados nesse dia.

**Chuva e visibilidade:** a Serra dos Órgãos tem microclima instável. Névoa e chuva podem aparecer sem aviso em qualquer época do ano. Leve sempre capa impermeável, mesmo com sol na saída.

## Equipamento Específico Para Esta Travessia

Além do kit básico de trekking, leve especificamente para a Petrópolis-Teresópolis:

- Saco de dormir com conforto até 5°C (a altitude faz o frio ser mais intenso do que parece)
- Bastões de trekking (imprescindíveis nas descidas do Dia 3)
- Gamacha ou perneira (o primeiro dia tem muita lama após chuva)
- Capacete ou acolchoamento para a mochila (trechos com pedras acima da cabeça)
- Lanterna de cabeça com pilhas reserva (necessária para saída muito cedo no Dia 2)

## A Melhor Época Para a Travessia

Entre abril e outubro o tempo é mais seco e as condições são mais favoráveis. Evite os meses de dezembro a março, quando as chuvas intensas tornam o percurso perigoso — deslizamentos no trecho do Pico do Sino e cheias no Rio Paquequer são riscos reais no verão.

O inverno (junho a agosto) traz os dias mais claros e o frio mais intenso. Noites no Abrigo 2 (a 1.800m de altitude) podem registrar temperatura próxima de 0°C nesse período.

## Variações e Trilhas Conectadas

**Subida ao Dedo de Deus:** a formação rochosa mais icônica da Serra dos Órgãos pode ser visitada a partir da sede de Teresópolis, sem necessidade de fazer a travessia completa. Uma alternativa para quem quer provar da Serra dos Órgãos sem o compromisso de 3 dias.

**Travessia reversa (Teresópolis → Petrópolis):** menos popular mas mais interessante para fotografia, pois você vai de frente para as formações rochosas mais icônicas ao longo de todo o Dia 1.

## Protocolo de Segurança

Informe sempre alguém de confiança fora do grupo sobre o seu itinerário completo. Em caso de emergência, o número do Parque Nacional da Serra dos Órgãos (0800 024 7654) deve estar salvo no celular.

O sinal de celular é inexistente em boa parte do percurso, especialmente entre os Abrigos 2 e 4. Considere alugar um comunicador via satélite para grupos grandes ou condições incertas.

Para a [Travessia Petrópolis x Teresópolis](/trilha/travessia-petropolis-teresopolis) completa, confira também nosso guia de [preparo físico para trekking](/blog/preparo-fisico-trekking) e saiba como montar um [kit de primeiros socorros para trilha](/blog/kit-primeiros-socorros-trilha) adequado para 3 dias em campo."""

# B6 - monte-roraima-guia-completo (id=2, 347w -> 800w)
expansions[2] = """O Monte Roraima é uma das experiências mais únicas que a natureza brasileira tem a oferecer. Um tepui com 2 bilhões de anos de história geológica, erguendo-se a 2.810 metros na tríplice fronteira entre Brasil, Venezuela e Guiana. Se você sonha em pisar num dos lugares mais remotos e fascinantes do planeta, este guia é para você.

## O Que é um Tepui?

Tepuis são formações tabulares de arenito encontradas na região da Guiana. O Monte Roraima é o mais famoso deles — seu topo plano e isolado abriga uma fauna e flora únicas, com espécies que não existem em nenhum outro lugar do mundo. A paisagem inspirou Arthur Conan Doyle a escrever O Mundo Perdido e a Pixar a criar o filme UP.

## A Trilha: 48 km em 6 a 8 Dias

O acesso pelo lado brasileiro parte da aldeia indígena Parumatá, em Uiramutã (RR). A trilha de 48 km ida e volta atravessa campos de lavrado, florestas de galeria e termina na famosa escalada pelo flanco sul do tepui.

A ascensão ao topo é feita por um corredor natural de pedras — sem necessidade de equipamento de escalada, mas exige bom equilíbrio e preparo físico. No topo, cristais de quartzo, piscinas naturais e formações rochosas surreais esperam por você.

## Como Chegar Até Uiramutã

Uiramutã fica a cerca de 320 km de Boa Vista (RR), a capital do estado. O trecho é feito de carro, com parte do percurso em estrada de terra que pode ficar intransitável na época das chuvas (maio a setembro). De Boa Vista, você pode alugar carro com tração 4x4 ou contratar transporte com as próprias agências de trekking locais.

Voos para Boa Vista operam a partir de Manaus (AM) e Belém (PA) com conexão. Não há voo direto de São Paulo ou Rio para Boa Vista sem escala.

## Guia é Obrigatório

A legislação brasileira exige guia credenciado para subir o Roraima pelo lado do Brasil. Os guias indígenas locais não apenas garantem sua segurança — são eles que negociam as permissões com a comunidade Ingarikó, que tem a tutela da área.

Contratar uma agência especializada em Boa Vista ou diretamente em Uiramutã é a forma mais comum de organizar a expedição. Os pacotes geralmente incluem guia, alimentação e transporte de bagagem por muares (animais de carga) até a base do tepui.

## O Topo do Roraima

O topo do Roraima tem aproximadamente 31 km² de área plana — suficiente para caminhar por horas sem repetir o mesmo percurso. Os principais pontos de interesse no planalto:

**Piscina do Roraima:** formações de rocha que criam piscinas naturais de água cristalina alimentadas pelas chuvas frequentes no topo. A temperatura da água fica entre 15°C e 20°C.

**El Foso:** um buraco circular na rocha com mais de 30 metros de profundidade, que parece um cratêra vulcânica mas é formação natural de erosão.

**Ventana:** ponto no limite do tepui com vista para a Venezuela e a Grande Sabana — uma das panorâmicas mais impressionantes da América do Sul.

## Fauna e Flora Exclusivas

O isolamento do topo por milhões de anos criou um laboratório evolutivo único:
- Heliamphora (plantas carnívoras endêmicas do tepui)
- Beija-flores de espécies endêmicas
- Rã transparente (Oreophrynella)
- Cristais de quartzo e formações de diamante bruto

## A Melhor Época para o Roraima

Ao contrário da maioria dos destinos de trekking no Brasil, o Roraima tem uma lógica climática específica: dezembro a março é o período relativamente mais seco, e portanto mais indicado para a expedição. De junho a setembro as chuvas são mais intensas e a trilha de acesso pode ficar intransitável.

Prepare-se: o topo do Roraima tem nevoeiro e chuva frequentes em qualquer época do ano. Impermeável e saco de dormir para baixas temperaturas são obrigatórios independente da estação.

## Checklist Essencial

Leve para essa expedição:
- Saco de dormir com conforto mínimo até 5°C (no topo pode gelar à noite)
- Capa de chuva e roupas impermeáveis
- Bastões de trekking para a escalada
- Filtro ou purificador de água
- Protetor solar fator 70+ (a altitude intensifica a radiação UV)
- Botas impermeáveis de cano alto
- Pilhas reserva para lanternas

Para começar a planejar, leia nosso guia de [preparo físico para trekking](/blog/preparo-fisico-trekking) — o Roraima exige um condicionamento sólido — e confira como [contratar um guia CADASTUR](/blog/guia-cadastur-como-encontrar) para expedições remotas como esta."""

# B2 - 10-itens-essenciais-mochila-trekking (id=3, 305w -> 800w)
expansions[3] = """Independente de ser sua primeira trilha ou a décima travessia de longo curso, há um conjunto de itens que nunca deve faltar na sua mochila. Esses itens foram definidos pelos maiores órgãos de segurança em montanhismo do mundo e adaptados para a realidade brasileira.

## Os 10 Essenciais do Trekking

A lista original foi criada nos anos 1930 pelo The Mountaineers e evoluiu ao longo das décadas. Aqui está a versão adaptada para trilhas brasileiras:

- **Navegação:** mapa offline (download no Maps.me ou AllTrails), bússola ou GPS
- **Proteção solar:** protetor fator 70+, óculos UV400, chapéu de abas largas
- **Isolamento térmico:** casaco impermeável + camada leve de lã ou fleece
- **Iluminação:** lanterna de cabeça com pilhas reserva
- **Kit de primeiros socorros:** curativo, antisséptico, fita crepe, esparadrapo, analgésico
- **Fogo/calor:** isqueiro e velas de emergência (mesmo em trilhas de 1 dia)
- **Ferramentas de reparo:** canivete ou multitool, fita silver tape
- **Alimentação extra:** barras energéticas ou mix de castanhas para emergência
- **Hidratação:** garrafa de 2L + filtro ou pastilhas de purificação
- **Abrigo de emergência:** manta aluminizada (pesa 80g e pode salvar vidas)

## Por Que Cada Item Importa

**Navegação offline:** o sinal de celular falha com mais frequência do que qualquer trilheiro gosta de admitir. Um mapa baixado offline no AllTrails ou Maps.me funciona sem internet e pode ser consultado com o GPS do celular ativo mesmo em área sem cobertura de rede. Se o celular morrer, uma bússola básica de R$ 30 e saber ler um mapa impresso são habilidades que podem ser a diferença entre achar o caminho de volta e precisar de resgate.

**Proteção solar:** no Brasil, a radiação UV é muito mais intensa do que a maioria das pessoas percebe — especialmente em altitude. Pele queimada em trilha é dolorosa, gera calor extra no corpo e pode causar desidratação secundária.

**Isolamento térmico:** a hipotermia não acontece apenas em montanhas nevadas. Uma chuva intensa em trilha de mata atlântica, seguida de uma parada longa para descanso, pode reduzir a temperatura corporal perigosamente mesmo em dias de verão. Uma camada seca na mochila pode mudar esse cenário completamente.

**Iluminação:** calcule mal o tempo de trilha — algo que acontece com frequência — e você vai querer uma lanterna. Caminhada noturna sem iluminação adequada em terreno irregular é uma receita para lesão de tornozelo.

**Kit de primeiros socorros:** veja nosso guia completo de [kit de primeiros socorros para trilha](/blog/kit-primeiros-socorros-trilha) para detalhes de montagem. Um kit de R$ 80 com os itens certos pode evitar que um corte simples vire uma emergência.

**Fogo/calor:** um isqueiro à prova d'água custa R$ 15 e pesa 20g. Em situação de emergência com hipotermia iminente, conseguir fazer fogo pode ser literalmente questão de sobrevivência.

**Ferramentas de reparo:** a fita silver tape merece menção especial. Serve para consertar bota rasgada, mochila furada, improvizar curativo oclusivo, fixar bandagem, reparar vara de barraca. É o canivete suíço dos materiais de reparo.

**Alimentação extra:** levar barras energéticas para emergência não é paranóia — é planejamento. Se a trilha levar 2 horas a mais do esperado, essa reserva calórica pode evitar que seu grupo tome decisões ruins por hipoglicemia.

**Hidratação:** leve mais água do que você acha necessário. Pastilhas de purificação pesam gramas e podem transformar qualquer fonte natural em água segura para beber em emergência.

**Manta aluminizada:** o item mais subestimado da lista. Uma manta de resgate de uso único custa R$ 10, pesa 80g e ocupa o espaço de um baralho. Em situação de hipotermia ou trauma, reflete até 90% do calor corporal de volta. É o seguro de vida da sua mochila.

## O Que a Maioria das Pessoas Esquece

De todos esses itens, os mais frequentemente negligenciados são a navegação offline e o abrigo de emergência. Celular sem sinal não serve de mapa. E a hipotermia pode acontecer mesmo em dias quentes quando você para de se movimentar molhado.

## Adapte o Peso ao Percurso

Não existe lista única para todas as trilhas. Para um dia de trilha de 5 km você não precisa do mesmo kit de uma travessia de 5 dias. A regra geral é que a mochila não deve ultrapassar 20–25% do seu peso corporal.

Invista tempo planejando o que levar. Uma mochila bem planejada é a diferença entre uma aventura segura e uma emergência evitável. Para trilhas de múltiplos dias, consulte nosso guia de [planejamento de trilha de longo curso](/blog/planejamento-trilha-longo-curso-passo-a-passo) e [como escolher o calçado certo](/blog/bota-ou-tenis-trilha) antes de comprar qualquer equipamento."""

# B1 - por-que-contratar-guia-cadastur (id=4, 289w -> 800w)
expansions[4] = """Muitos trilheiros experientes torcem o nariz quando ouvem falar em guia. "Eu conheço o caminho", "é só seguir a trilha marcada", "vai encarecer a viagem". Mas há razões muito sólidas para reconsiderar essa posição — especialmente quando falamos de guias certificados pelo CADASTUR.

## O Que é o CADASTUR?

O CADASTUR é o sistema de cadastramento de prestadores de serviços turísticos do Ministério do Turismo. Para guias de turismo, o cadastro é obrigatório e exige formação técnica, conhecimento sobre primeiros socorros e capacitação específica para conduzir grupos em trilhas e montanhas.

Um guia CADASTUR não é apenas alguém que conhece o caminho — é um profissional formado que pode ser responsabilizado legalmente por sua conduta. Isso muda completamente a equação de risco quando algo dá errado.

## Cinco Razões Concretas Para Contratar um Guia

**1. Conhecimento local que nenhum aplicativo tem**

Guias locais conhecem as condições reais da trilha: onde a água secou nos últimos meses, qual trecho tem mais carrapatos nessa época do ano, quais cachoeiras secam em agosto, qual bifurcação não está sinalizada. Esse conhecimento operacional é invisível no AllTrails e no Wikiloc.

**2. Primeiros socorros e gestão de emergências**

Guias certificados pelo CADASTUR têm formação básica em primeiros socorros. Em caso de acidente, a diferença entre um grupo com e sem guia pode ser a diferença entre uma situação controlada e um resgate de helicóptero.

**3. Interpretação ambiental**

Uma trilha com guia e uma trilha sem guia no mesmo local são duas experiências completamente diferentes. O guia transforma um percurso em uma narrativa: a história geológica daquele afloramento, o nome da planta medicinal que você está tocando, o canto da espécie de ave que acabou de cruzar a trilha. Isso é impossível de replicar com um podcast no ouvido.

**4. Responsabilidade legal**

Em caso de acidente em trilha conduzida por guia CADASTUR, o profissional tem responsabilidade civil pela segurança do grupo. Ele geralmente tem seguro de responsabilidade profissional. Isso não elimina o risco, mas cria uma rede de proteção que não existe quando você vai sozinho.

**5. Impacto econômico local**

Contratar guias locais gera renda direta nas comunidades próximas às áreas protegidas. É uma forma concreta de fazer o turismo funcionar como ferramenta de conservação — quando a floresta em pé gera renda, as comunidades têm interesse direto em protegê-la.

## Quando o Guia é Obrigatório

Em vários parques nacionais brasileiros, o guia credenciado não é opcional — é exigência legal:

- **Monte Roraima (RR):** guia indígena obrigatório por regulamentação do parque
- **Travessia do Vale do Pati — Chapada Diamantina (BA):** obrigatório para a travessia completa
- **Parque Nacional da Serra dos Órgãos (RJ):** guia exigido em algumas rotas específicas
- **Parques com acesso controlado:** capacidade limitada gerida por concessionárias que operam com guias

Trilhar sem guia em áreas que exigem pode resultar em multa e expulsão do parque.

## Como Verificar se o Guia é Realmente CADASTUR

Acesse o site do CADASTUR em **cadastur.turismo.gov.br**, clique em "Consultar Prestadores" e busque pelo nome ou CPF do profissional. A situação deve estar "Ativo" e a categoria deve ser "Guia de Turismo".

Qualquer guia profissional sério fornece o número do CADASTUR antes de fechar contrato. Se ele hesitar ou não souber o número, isso é um sinal de alerta.

## O Que Custa um Guia de Trekking

Os valores variam muito por região, duração e tipo de trilha. Como referência:

- Trilha de 1 dia em parque estadual: R$ 150–300 por pessoa em grupos de 5 a 8
- Travessia de 2–3 dias: R$ 400–700 por pessoa
- Expedição de 5+ dias (Roraima, Pati): R$ 1.200–2.500 por pessoa com logística

Sempre confirme o que está incluído — transporte, alimentação e taxa de entrada podem ou não fazer parte do pacote.

Para saber como encontrar um guia CADASTUR na região da sua trilha, leia nosso guia completo de [como encontrar e contratar um guia CADASTUR](/blog/guia-cadastur-como-encontrar). E para entender a importância do planejamento completo antes de qualquer expedição, confira [como planejar uma trilha de longo curso](/blog/planejamento-trilha-longo-curso-passo-a-passo)."""

print("Batch 6 expansions defined.")

for post in data:
    if post['id'] in expansions:
        post['content'] = expansions[post['id']]

with open('data/blog.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Batch 6 written to blog.json")

for post in data:
    if post['id'] in expansions:
        words = len(post['content'].split())
        print(f"ID {post['id']} | {words}w | {post['slug']}")
