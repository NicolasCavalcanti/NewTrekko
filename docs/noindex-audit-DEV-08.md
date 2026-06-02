# Auditoria de Meta Tags noindex — DEV-08

**Data:** 2026-06-02  
**Status:** ✅ Concluído

---

## Resultado da Auditoria

### Páginas com `noindex` intencional (mantidas)

| URL / Padrão | Motivo | Localização da regra |
|---|---|---|
| `/admin/*` | Área administrativa | `admin/index.html` meta robots |
| `/go/*` | Serviço de redirecionamento de links | `go/index.html` meta robots |
| `/component-showcase` | Página de desenvolvimento interno | Injeção dinâmica em `index.html` e `404.html` |
| `/trilhas/rj/itatiaia/circuito-5-lagos-pedra-do-altar/` | Redirect de URL legada (canonical → `/trilha/circuito-5-lagos-pedra-do-altar`) | meta robots na página de redirect |
| `/robots.txt` | Correto — bots não devem indexar o próprio robots.txt | `X-Robots-Tag: noindex` via `vercel.json` |

### Páginas sem `noindex` (indexáveis corretamente)

Todas as páginas de conteúdo público utilizam o header padrão `X-Robots-Tag: index, follow` configurado em `vercel.json` e **não possuem** meta robots noindex no HTML:

- Homepage (`/`)
- Trilhas individuais (`/trilha/*`)
- Listagem de trilhas (`/trilhas`)
- Blog e artigos (`/blog/*`)
- Equipamentos (`/equipamentos/*`)
- Páginas institucionais (`/sobre`, `/contato`, `/privacidade`, etc.)
- Perfis de guias credenciados (`/guia/*`) — **corrigido nesta tarefa**

---

## Correções Realizadas

### 1. `robots.txt` — bugs corrigidos

**Problema:** Havia um bloco duplicado `User-agent: Googlebot` (linhas 31-41) com regras inconsistentes em relação ao primeiro bloco (linhas 1-9). O bloco duplicado adicionava `Disallow: /guia/` e `Disallow: /expedicao/` que não existiam no bloco original, criando ambiguidade.

**Problema adicional:** `Disallow: /guia/` no bloco `User-agent: *` bloqueava o crawl de perfis de guias credenciados — páginas de conteúdo que devem ser indexadas.

**Correções:**
- Removido bloco duplicado `User-agent: Googlebot`
- Removido `Disallow: /guia/` de todos os blocos (guias devem ser indexados)
- Removido `Disallow: /expedicao/` (sem conteúdo publicado, regra desnecessária)
- Adicionado `Disallow: /dashboard/` ao bloco Googlebot (estava faltando)
- Reorganizado para melhor legibilidade

### 2. `sitemap.xml` — guias adicionados

Os 5 perfis de guias credenciados (`/guia/*`) foram adicionados ao sitemap com `priority: 0.5` e `changefreq: monthly`.

---

## Verificação Recomendada

1. **Search Console → Cobertura → Excluídas → "Excluídas por tag noindex"**  
   Confirmar que nenhuma página de conteúdo aparece nesta lista.

2. **Search Console → Cobertura → Válidas**  
   Confirmar que as páginas `/guia/*` aparecem como indexadas após recrawl.

3. **Testar headers** com `curl -I https://www.trekko.com.br/guia/[slug]`  
   Deve retornar `X-Robots-Tag: index, follow`.
