# US 2.3 — Auditar e tratar páginas de expedição rasas

## Title
**Como motor de busca**, quero encontrar páginas de expedição com conteúdo editorial suficiente, **para que** o Trekko apareça em resultados relevantes de busca orgânica e evite penalidades por thin content.

---

## Contexto

A auditoria de SEO identificou que páginas `/expedicao/:id` funcionavam como páginas de produto rasas — exibindo apenas preço, data e disponibilidade — sem meta tags dinâmicas, structured data ou conteúdo editorial mínimo para justificar indexação.

---

## Critérios Mínimos de Indexação

Uma página de expedição é considerada **indexável** quando atende a **todos** os critérios abaixo:

| # | Critério | Campo no banco | Mínimo |
|---|---------|----------------|--------|
| 1 | Status público | `status` | `active` ou `full` |
| 2 | Descrição editorial | `description` | ≥ 80 caracteres |
| 3 | Ponto de encontro | `meetingPoint` | Preenchido |
| 4 | Notas do guia OU itens inclusos | `guideNotes` / `includedItems` | Pelo menos 1 |

Páginas com `status = draft` ou `cancelled` são **sempre** noindex.  
Páginas com `status = closed/completed` com data há mais de 90 dias também são noindex (conteúdo stale).

---

## Checklist de Elementos Obrigatórios

```
[ ] Título customizado OU nome da trilha vinculada
[ ] Descrição ≥ 80 caracteres com contexto da expedição
[ ] Ponto de encontro preenchido
[ ] Observações do guia OU lista de itens inclusos
[ ] Data de início (sempre obrigatório para criação)
[ ] Status = active ou full
```

---

## Regra Técnica de Indexação

A função `evaluateExpeditionQuality()` em `client/src/lib/expeditionQuality.ts`
retorna `{ shouldIndex: boolean, missingFields: string[], score: number }`.

O componente `ExpeditionDetail` injeta via `react-helmet-async`:

```html
<!-- Página forte (score ≥ 4, sem campos faltantes) -->
<meta name="robots" content="index, follow" />

<!-- Página fraca (score < 4 ou campos ausentes) -->
<meta name="robots" content="noindex, follow" />
```

O guia/admin vê um banner âmbar listando os campos em falta enquanto a
expedição ainda não atingiu o score mínimo.

---

## Template Ideal de Página Forte

```
Título:       Expedição Chapada Diamantina — Vale do Pati, BA | 15 de agosto de 2025 | Trekko
Description:  Expedição de 4 dias pelo Vale do Pati com guia certificado CADASTUR. 
              Inclusos: transporte de bagagem, refeições e seguro de vida.
              Ponto de encontro: Portão da Vale do Capão, Palmeiras-BA, às 07h.
              Saiba mais sobre datas, ponto de encontro e como se inscrever.

JSON-LD:      @type Event com startDate, location (PostalAddress), organizer (guide), 
              offers (price/availability)

OG tags:      og:type=event, og:image=(primeira foto da trilha), og:locale=pt_BR
```

### Página Forte vs Página Fraca

| Campo | Página Forte | Página Fraca |
|-------|-------------|--------------|
| `description` | "Expedição de 4 dias pelo Vale do Pati com guia certificado CADASTUR..." (≥80 chars) | `null` ou "Veja a expedição" (< 80 chars) |
| `meetingPoint` | "Portão da Vale do Capão, Palmeiras-BA, às 07h" | `null` |
| `guideNotes` | "Nível moderado. Traga 3L de água, botina impermeável e protetor solar." | `null` |
| `includedItems` | "Transporte de bagagem, refeições, seguro de vida" | `null` |
| **robots** | `index, follow` | `noindex, follow` |
| **score** | 4–5 | 0–3 |

---

## Impacto Técnico

| Arquivo | Mudança |
|---------|---------|
| `client/src/lib/expeditionQuality.ts` | Nova utilidade de scoring (criada) |
| `client/src/pages/ExpeditionDetail.tsx` | Helmet dinâmico + noindex + JSON-LD Event + banner para guia |

### Nenhuma alteração de schema ou migration necessária.

---

## Acceptance Criteria

```gherkin
Feature: Indexação condicional de páginas de expedição

  Scenario: Expedição com todos os campos preenchidos é indexada
    Given uma expedição com status "active"
    And description com 120 caracteres
    And meetingPoint preenchido
    And guideNotes preenchido
    When o Google acessa /expedicao/:id
    Then a meta tag robots é "index, follow"
    And há um JSON-LD @type Event na página

  Scenario: Expedição sem descrição recebe noindex
    Given uma expedição com status "active"
    And description null
    When o Google acessa /expedicao/:id
    Then a meta tag robots é "noindex, follow"

  Scenario: Expedição em rascunho recebe noindex
    Given uma expedição com status "draft"
    When qualquer usuário acessa /expedicao/:id
    Then a meta tag robots é "noindex, follow"

  Scenario: Guia vê aviso de campos faltantes
    Given o guia autenticado acessa sua expedição fraca
    And a expedição está sem meetingPoint
    Then um banner âmbar lista "Ponto de encontro" como campo em falta
    And o banner não é visível para visitantes anônimos

  Scenario: Expedição cancelada recebe noindex
    Given uma expedição com status "cancelled"
    When o Google acessa /expedicao/:id
    Then a meta tag robots é "noindex, follow"

  Scenario: Expedição encerrada há mais de 90 dias recebe noindex
    Given uma expedição com status "closed"
    And startDate há 95 dias
    When o Google acessa /expedicao/:id
    Then a meta tag robots é "noindex, follow"
```
