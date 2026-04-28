# Trekko — Prompt de Criação de Nova Trilha

> **Objetivo:** Adicionar uma nova trilha completa ao arquivo `data/trails.json`, incluindo todos os campos obrigatórios, textos editoriais otimizados e metadados corretos.
> **Arquivo-alvo:** `data/trails.json`
> **Imagens:** `/trails/<id-imagem>.<ext>` (copiar para a raiz do repo)

---

## 1. Schema completo de uma trilha

Cada objeto do array `data/trails.json` deve conter os campos abaixo. Os campos marcados com ⚠️ são obrigatórios; os demais são fortemente recomendados.

```json
{
  "id": 10,                           // ⚠️ inteiro sequencial (max(id) + 1)
  "name": "",                         // ⚠️ nome oficial da trilha em português
  "slug": "",                         // ⚠️ kebab-case único, sem acentos (usado na URL)
  "uf": "",                           // ⚠️ sigla do estado (ex: "SP", "MG")
  "city": "",                         // ⚠️ município(s) onde a trilha está localizada
  "region": "",                       // ⚠️ nome da região/serra/chapada/litoral
  "park": "",                         // ⚠️ unidade de conservação (parque, APA, RPPN, etc.)
  "distanceKm": "",                   // ⚠️ distância total em km (string, ex: "30" ou "9.91")
  "elevationGain": 0,                 // ⚠️ ganho de elevação acumulado em metros (inteiro)
  "maxAltitude": 0,                   // ⚠️ altitude máxima atingida em metros (inteiro)
  "difficulty": "",                   // ⚠️ "easy" | "moderate" | "hard" | "expert"
  "guideRequired": 0,                 // ⚠️ 1 = guia obrigatório, 0 = opcional/não obrigatório
  "entranceFee": "",                  // ⚠️ valor da taxa de entrada (ex: "R$ 36,00" ou "Gratuito")
  "estimatedTime": "",                // ⚠️ duração estimada (ex: "1 dia", "4-6 horas", "3-5 dias")
  "trailType": "",                    // ⚠️ "circular" | "linear" | "traverse"
  "bestSeason": "",                   // ⚠️ meses ou estações ideais (ex: "Abril a Outubro")
  "waterPoints": [],                  // ⚠️ lista de pontos de captação de água ao longo da rota
  "campingPoints": [],                // lista de áreas de acampamento (array vazio se não houver)
  "highlights": [],                   // ⚠️ 4–6 atrativos principais (strings curtas)
  "shortDescription": "",             // ⚠️ 1–2 frases impactantes (máx. 160 chars) — usado em cards
  "hookText": "",                     // ⚠️ 2–3 frases poéticas para engajar o leitor — abre a página
  "ctaText": "",                      // ⚠️ chamada para ação direta (1–2 frases com verbo imperativo)
  "description": "",                  // ⚠️ descrição completa (3–5 parágrafos, mín. 200 palavras)
  "imageUrl": "",                     // ⚠️ caminho da imagem principal (ex: "/trails/ABCD1234.jpg")
  "images": [],                       // ⚠️ array com 6–8 caminhos de imagens da galeria
  "heroImage": { ... },               // objeto de imagem hero (ver seção 4) — obrigatório se usar Wikimedia
  "gallery": [],                      // array de objetos de imagem (ver seção 4) — obrigatório se usar Wikimedia
  "wiklocUrl": "",                    // URL do tracklog público no Wikiloc (pt.wikiloc.com)
  "wiklocGpxUrl": "",                 // URL de download do GPX no Wikiloc
  "status": "published"               // ⚠️ "published" | "draft"
}
```

---

## 2. Regras de negócio por campo

### `id`
Sempre o maior `id` atual + 1. Nunca reutilize IDs de trilhas removidas.

### `slug`
- Apenas letras minúsculas, números e hífens.
- Sem acentos: `ã→a`, `ç→c`, `é→e`, etc.
- Deve ser único em todo o array.
- Exemplos corretos: `"vale-da-lua-e-cachoeiras"`, `"pico-da-bandeira"`.

### `difficulty`
| Valor | Critérios |
|---|---|
| `easy` | Terreno regular, elevação < 300 m, distância < 8 km, sem técnica |
| `moderate` | Elevação 300–700 m, até 15 km, pode haver trechos irregulares |
| `hard` | Elevação 700–1500 m, +15 km ou terreno técnico, boa forma exigida |
| `expert` | Elevação > 1500 m acumulado, múltiplos dias, trechos de escalada ou extrema exposição |

### `trailType`
| Valor | Significado |
|---|---|
| `circular` | Início e fim no mesmo ponto |
| `linear` | Início e fim em pontos diferentes, mesma direção |
| `traverse` | Travessia — ponto de partida e chegada em locais distintos (requer logística) |

### `guideRequired`
Use `1` apenas quando a exigência de guia é **regulamentar** (decreto do parque, ICMBio, etc.). Use `0` quando o guia é recomendado mas não obrigatório.

### `entranceFee`
- Formato: `"R$ XX,00"` ou `"Gratuito"` ou `"Não confirmado"`.
- Use o valor vigente na data de publicação; inclua nota de revisão periódica na `description` se necessário.

### `waterPoints` e `campingPoints`
Arrays de strings com nomes dos locais. Array vazio `[]` quando não houver nenhum.

---

## 3. Guia editorial de texto

### `shortDescription` — Card da trilha
- Máximo 160 caracteres.
- Deve comunicar o diferencial da trilha em uma ou duas frases.
- Evite começar com "A trilha de…". Use o atributo mais único da trilha.
- **Exemplo (Monte Roraima):** `"A montanha mais antiga do planeta, um tepui de 2 bilhões de anos que inspirou o filme 'UP' da Pixar."`

### `hookText` — Abertura da página de detalhe
- 2–3 frases poéticas e evocativas.
- Coloque o leitor na cena — use verbos de ação na 2ª pessoa ("Imagine", "Atravesse", "Assista").
- Não inclua dados técnicos (distância, altitude) aqui.
- **Exemplo (Pico da Bandeira):** `"Assista ao nascer do sol do terceiro ponto mais alto do Brasil, quando o mar de nuvens se tinge de dourado aos seus pés."`

### `ctaText` — Chamada para ação
- 1–2 frases com verbo imperativo.
- Deve motivar o leitor a dar o próximo passo (reservar, planejar, explorar).
- **Exemplo:** `"Conquiste o topo do mundo perdido. Reserve sua expedição ao Monte Roraima."`

### `description` — Descrição completa
- Mínimo 200 palavras, máximo 400.
- Estrutura sugerida:
  1. **Parágrafo 1:** Localização e por que a trilha é especial (contexto geográfico/cultural).
  2. **Parágrafo 2:** O percurso — como é caminhar ali, o que você encontra.
  3. **Parágrafo 3:** Infraestrutura, logística, acesso.
  4. **Parágrafo 4 (opcional):** Dificuldades, recomendações de preparo, avisos de segurança.
- Tom: informativo mas inspirador. Evite linguagem de manual de instruções.
- Não repita dados que já estão em campos estruturados (distância, elevação, etc.).

### `highlights` — Destaques
- 4 a 6 itens.
- Strings curtas (2–5 palavras), sem ponto final.
- Cada item deve ser um atrativo distinto e vendável.
- **Exemplo:** `["Tepui milenar", "Formações rochosas únicas", "Piscinas naturais", "Vista da tríplice fronteira"]`

---

## 4. Imagens

### Imagens locais (padrão preferencial)
- Armazene em `/trails/<nome-aleatorio>.<ext>`.
- O nome do arquivo deve ter 12 caracteres alfanuméricos (ex: `x3cCqIWOMgkN.jpg`).
- Formatos aceitos: `.jpg`, `.jpeg`, `.webp`.
- `imageUrl` = caminho da foto principal (melhor ângulo, boa luz, horizontal).
- `images[]` = array com 6–8 fotos para galeria; inclua o `imageUrl` como primeiro item.
- Não é necessário preencher `heroImage` nem `gallery` para imagens locais.

### Imagens externas (Wikimedia Commons — uso licenciado)
Quando a trilha não tem fotos locais, use imagens do Wikimedia Commons com licença CC. Neste caso, preencha `heroImage` e `gallery` com o objeto completo:

```json
"heroImage": {
  "src": "https://upload.wikimedia.org/...",
  "mobileSrc": "https://upload.wikimedia.org/...",
  "fallbackSrc": "https://upload.wikimedia.org/...",
  "alt": "Descrição acessível da imagem com nome da trilha e localização",
  "title": "Nome da Trilha",
  "caption": "Legenda curta descritiva.",
  "credit": "Autor / Wikimedia Commons (CC BY-SA 3.0)",
  "sourceUrl": "https://commons.wikimedia.org/wiki/File:...",
  "licenseStatus": "licensed",
  "width": 0,
  "height": 0,
  "aspectRatio": "W:H",
  "focalPoint": { "x": 50, "y": 50 }
},
"gallery": [
  {
    "src": "https://upload.wikimedia.org/...",
    "thumbnailSrc": "https://upload.wikimedia.org/...",
    "alt": "...",
    "title": "...",
    "caption": "...",
    "credit": "...",
    "sourceUrl": "...",
    "licenseStatus": "licensed",
    "width": 0,
    "height": 0,
    "aspectRatio": "W:H"
  }
]
```

**Regras para imagens Wikimedia:**
- Sempre confirme a licença (CC BY, CC BY-SA, ou domínio público).
- Preencha `credit` com `"Autor / Wikimedia Commons (CC BY-SA X.X)"`.
- O campo `licenseStatus` deve ser `"licensed"`.
- Para imagens locais sem atribuição necessária, omita `heroImage` e `gallery`.

---

## 5. Dados GPX / Wikiloc

- Procure o tracklog da trilha em `pt.wikiloc.com` buscando pelo nome da trilha.
- Prefira tracks com alta qualidade (muitos pontos de passagem, fotos, descrição detalhada).
- `wiklocUrl` = URL da página do track no Wikiloc.
- `wiklocGpxUrl` = URL de download do GPX (`https://www.wikiloc.com/wikiloc/download.do?id=XXXXXXX`).
- Se não houver track confiável no Wikiloc, deixe ambos os campos como strings vazias `""`.

---

## 6. Checklist antes de publicar

- [ ] `id` é o maior ID existente + 1
- [ ] `slug` é único, sem acentos, sem espaços
- [ ] Todos os campos ⚠️ estão preenchidos
- [ ] `shortDescription` tem no máximo 160 caracteres
- [ ] `description` tem no mínimo 200 palavras
- [ ] `highlights` tem entre 4 e 6 itens
- [ ] `images[]` tem entre 6 e 8 itens (ou ao menos 1 via Wikimedia)
- [ ] `imageUrl` é o primeiro item de `images[]` (ou mesmo URL)
- [ ] `difficulty` segue a tabela da seção 2
- [ ] `guideRequired` é 0 ou 1 (não booleano, não string)
- [ ] `status` está como `"published"` (ou `"draft"` se ainda incompleto)
- [ ] JSON é válido — sem vírgulas faltando/sobrando
- [ ] O novo objeto foi inserido **ao final** do array, antes do `]` final

---

## 7. Workflow completo

```bash
# 1. Crie o branch de trabalho (se não existir)
git checkout -b claude/add-trail-<nome-slug>

# 2. Edite data/trails.json — adicione o novo objeto ao final do array

# 3. Valide o JSON
python3 -c "import json; json.load(open('data/trails.json')); print('JSON válido')"

# 4. (Opcional) Copie as fotos locais para /trails/
cp <fotos> /home/user/NewTrekko/trails/

# 5. Commit e push
git add data/trails.json trails/
git commit -m "feat: add trail <nome da trilha> (<UF>)"
git push -u origin claude/add-trail-<nome-slug>
```

---

## 8. Exemplo de objeto mínimo válido

```json
{
  "id": 10,
  "name": "Chapada Diamantina — Trilha do Morro do Pai Inácio",
  "slug": "morro-do-pai-inacio",
  "uf": "BA",
  "city": "Palmeiras",
  "region": "Chapada Diamantina",
  "park": "Parque Nacional da Chapada Diamantina",
  "distanceKm": "6",
  "elevationGain": 350,
  "maxAltitude": 1120,
  "difficulty": "moderate",
  "guideRequired": 0,
  "entranceFee": "Gratuito",
  "estimatedTime": "3-4 horas",
  "trailType": "circular",
  "bestSeason": "Maio a Setembro",
  "waterPoints": [],
  "campingPoints": [],
  "highlights": [
    "Vista do Mar de Morros",
    "Pôr do sol mais famoso da Chapada",
    "Formações de quartzito",
    "Vale do Capão ao fundo"
  ],
  "shortDescription": "O mirante mais fotografado da Chapada Diamantina, com vista de 360° sobre um oceano de morros.",
  "hookText": "Suba por uma trilha de quartzito e chegue a um mirante onde o horizonte inteiro se abre em um mar de morros — um dos pores do sol mais espetaculares do Brasil.",
  "ctaText": "Descubra o Morro do Pai Inácio. Escolha o seu pôr do sol na Chapada.",
  "description": "O Morro do Pai Inácio é o ponto mais visitado do Parque Nacional da Chapada Diamantina e oferece um dos panoramas mais icônicos do interior da Bahia. A trilha de 6 km, em percurso circular, sobe pelas formações de quartzito até o mirante a 1.120 m de altitude, de onde se avista o Vale do Capão e um vasto mar de morros cobertos de vegetação de caatinga e cerrado. O trajeto é acessível para a maioria dos caminhantes, com trechos de rocha escorregadia que exigem atenção redobrada após chuvas. O pôr do sol no topo é um fenômeno à parte: quando a luz dourada incide sobre as chapadas ao redor, a paisagem se transforma em uma das cenas naturais mais belas do Brasil. Chegue com pelo menos uma hora de antecedência para garantir bom posicionamento.",
  "imageUrl": "/trails/ABCDE12345XY.jpg",
  "images": [
    "/trails/ABCDE12345XY.jpg",
    "/trails/FGHIJ67890KL.jpg"
  ],
  "wiklocUrl": "https://pt.wikiloc.com/trilhas-trekking/morro-do-pai-inacio-chapada-diamantina-ba-XXXXXXX",
  "wiklocGpxUrl": "https://www.wikiloc.com/wikiloc/download.do?id=XXXXXXX",
  "status": "published"
}
```

---

*Prompt criado para o projeto Trekko (www.trekko.com.br) · `docs/create-trail-prompt.md` · 2026-04-28*
