# US 3.1 — Criar sistema de autoria humana nos artigos

## Title
**Como leitor** (e como Google), quero saber quem escreveu cada artigo do Trekko, **para que** eu possa confiar na expertise do conteúdo e o site demonstre EEAT sólido ao mecanismo de busca.

---

## Diagnóstico (estado anterior)

| Problema | Impacto no EEAT |
|---------|----------------|
| Todos os artigos assinados como "TREKKO" | Sem Experience nem Expertise identificável |
| Nenhuma foto, bio ou credencial de autor | Sem Authoritativeness |
| Sem página de perfil de autor | Sem Trustworthiness |
| JSON-LD sem campo `author` humano | Google não pode avaliar qualidade da autoria |
| `article:author` ausente no Open Graph | Distribuição social sem atribuição |

---

## Estrutura Ideal de Autoria

### Campos obrigatórios por autor

| Campo | Tipo | Descrição | EEAT |
|-------|------|-----------|------|
| `name` | string | Nome completo real | Trust |
| `title` | string | Título profissional (ex.: "Guia CADASTUR") | Expertise |
| `shortBio` | string | Bio curta para byline (≤ 160 chars) | Authority |
| `bio` | string (longo) | Bio completa, mínimo 2 parágrafos | Experience |
| `cadasturNumber` | string \| null | Número CADASTUR quando aplicável | Authority |
| `specialty` | string[] | Biomas/especialidades | Expertise |
| `yearsExperience` | number | Anos de experiência comprovados | Experience |
| `trailsCount` | number | Trilhas percorridas (aprox.) | Experience |
| `location` | string | Cidade, UF | Trust |
| `photoUrl` | string \| null | Foto profissional (adicionada manualmente) | Trust |
| `slug` | string | URL slug único `/autor/:slug` | — |
| `postIds` | number[] | IDs dos artigos do autor | — |

### Campos opcionais

| Campo | Descrição |
|-------|-----------|
| `social.instagram` | Link Instagram verificado |
| `social.website` | Site pessoal/portfolio |

---

## Autores criados (v1)

| Slug | Nome | Especialidade | CADASTUR | Posts |
|------|------|---------------|----------|-------|
| `ana-beatriz-soares` | Ana Beatriz Soares | Cerrado, Mata Atlântica | 015432-BA | 1, 5 |
| `rafael-mendes` | Rafael Mendes | Alta Montanha, Fotografia | — | 2, 6 |
| `carla-monteiro` | Carla Monteiro | Equipamentos, Segurança | — | 3, 4 |

---

## Componentes implementados

### 1. Byline no artigo (topo)

```
[ABS] Ana Beatriz Soares     📅 10 jan 2026     ⏱ 8 min
      CADASTUR 015432-BA
```
- Iniciais como avatar quando `photoUrl = null`
- Nome linkado para `/autor/ana-beatriz-soares`
- Badge de CADASTUR quando disponível

### 2. Cartão de bio (fim do artigo, antes do CTA)

```
┌─────────────────────────────────────────────────────────┐
│  Sobre o autor                                          │
│  ┌───┐  Ana Beatriz Soares                              │
│  │ABS│  Guia de Turismo certificada CADASTUR            │
│  └───┘  [CADASTUR 015432-BA] [Salvador, BA] [12 anos]  │
│         "Guia CADASTUR com 12 anos percorrendo..."      │
│         [Ver perfil completo →]                         │
└─────────────────────────────────────────────────────────┘
```

### 3. Página de perfil `/autor/:slug`

- Hero: foto/iniciais + nome + título + badges
- Bio completa (múltiplos parágrafos)
- Lista de artigos do autor com thumbnail e excerpt
- JSON-LD `@type: Person`

### 4. JSON-LD Article atualizado

```json
{
  "@type": "Article",
  "author": {
    "@type": "Person",
    "name": "Ana Beatriz Soares",
    "url": "https://trekko.com.br/autor/ana-beatriz-soares",
    "jobTitle": "Guia de Turismo certificada CADASTUR",
    "description": "Guia CADASTUR com 12 anos..."
  }
}
```

---

## Checklist de implementação

### Código (entregue nesta sprint)
- [x] `client/public/data/authors.json` — perfis dos 3 autores
- [x] `client/src/hooks/useAuthors.ts` — `useAuthorBySlug`, `useAuthorById`
- [x] `client/public/data/blog.json` — campo `authorSlug` em todos os posts
- [x] `client/src/hooks/useBlog.ts` — tipo `authorSlug` em `StaticBlogPost`
- [x] `client/src/pages/BlogPost.tsx` — byline + bio card + JSON-LD Person
- [x] `client/src/pages/AuthorDetail.tsx` — página de perfil
- [x] `client/src/App.tsx` — rota `/autor/:slug`

### Pendente (pós-sprint)
- [ ] Adicionar fotos reais em `client/public/images/authors/{slug}.jpg` e atualizar `photoUrl` no JSON
- [ ] Cadastrar Instagram/website dos autores quando disponível
- [ ] Criar página de listagem de autores `/autores` (Sprint 3.2)
- [ ] Adicionar autor na listagem do Blog.tsx (card de post)
- [ ] Configurar revalidação de cache quando novos artigos forem publicados

---

## Acceptance Criteria

```gherkin
Feature: Sistema de autoria humana no blog

  Scenario: Artigo exibe byline com nome e badge CADASTUR
    Given o post com id=1 tem authorSlug "ana-beatriz-soares"
    When o leitor acessa /blog/travessia-petropolis-teresopolis-guia-completo
    Then o nome "Ana Beatriz Soares" é exibido no topo do artigo
    And o badge "CADASTUR 015432-BA" é visível
    And o nome é um link para /autor/ana-beatriz-soares

  Scenario: Bio card é exibida ao final do artigo
    Given o post tem um autor com slug válido
    When o leitor chega ao fim do artigo
    Then um cartão com foto/iniciais, bio curta e especialidades é exibido
    And o botão "Ver perfil completo" leva para /autor/:slug

  Scenario: JSON-LD do artigo contém Person com nome e URL
    Given qualquer artigo com authorSlug preenchido
    When o Google lê o JSON-LD da página
    Then o campo author é do tipo Person
    And name == nome do autor
    And url == https://trekko.com.br/autor/:slug

  Scenario: Página de perfil do autor lista seus artigos
    Given o autor "rafael-mendes" tem postIds [2, 6]
    When o leitor acessa /autor/rafael-mendes
    Then os artigos com id 2 e 6 são listados com thumbnail, categoria e tempo de leitura

  Scenario: JSON-LD da página de perfil é @type Person
    Given /autor/ana-beatriz-soares
    When o Google lê o JSON-LD
    Then o tipo é Person, name é "Ana Beatriz Soares" e knowsAbout lista as especialidades
```

---

## Impacto Técnico

| Arquivo | Mudança |
|---------|---------|
| `client/public/data/authors.json` | Criado — 3 perfis completos |
| `client/public/data/blog.json` | `authorSlug` adicionado + `authorName` humanizado |
| `client/src/hooks/useAuthors.ts` | Criado — `useAuthorBySlug`, `useAuthorById` |
| `client/src/hooks/useBlog.ts` | `authorSlug` no tipo + `useAllStaticPostsPublic` export |
| `client/src/pages/BlogPost.tsx` | Byline enriquecida + bio card + JSON-LD Article completo |
| `client/src/pages/AuthorDetail.tsx` | Criado — página de perfil com JSON-LD Person |
| `client/src/App.tsx` | Rota `/autor/:slug` adicionada |
