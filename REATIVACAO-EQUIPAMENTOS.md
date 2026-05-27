# Rota de Reativação — Páginas de Equipamentos com Prateleira Vazia

**Contexto:** Implementado em DEV-04 (2026-05-27). Páginas com `noindex,nofollow` e removidas do sitemap enquanto não possuem produtos reais. Aguardando conclusão de **RED-01**.

---

## Páginas afetadas

| Página | URL | Status |
|--------|-----|--------|
| Lanternas | `/equipamentos/lanternas/` | ⏸ noindex — prateleira vazia |
| Hidratação | `/equipamentos/hidratacao/` | ⏸ noindex — prateleira vazia |
| Camping | `/equipamentos/camping/` | ⏸ noindex — prateleira vazia |
| Segurança | `/equipamentos/seguranca/` | ⏸ noindex — prateleira vazia |
| Pets Outdoor | `/equipamentos/pets-outdoor/` | ⏸ noindex — prateleira vazia |
| Ofertas | `/equipamentos/ofertas/` | ⏸ noindex — prateleira vazia |
| Primeiros Socorros | `/equipamentos/primeiros-socorros/` | ⏸ noindex — prateleira vazia |

---

## Para reativar uma página (após RED-01)

Faça as seguintes alterações **para cada página** que tiver produtos reais preenchidos:

### 1. Remover `noindex` do `<head>` da página HTML

Abrir o arquivo `equipamentos/<categoria>/index.html` e trocar:

```html
<meta name="robots" content="noindex,nofollow"><!-- DEV-04: prateleira vazia — remover quando produtos forem adicionados (RED-01) -->
```

Por:

```html
<meta name="robots" content="index,follow">
```

### 2. Readicionar a URL ao `sitemap.xml`

Abrir `sitemap.xml` e, dentro da seção `<!-- Trekko Store / Equipamentos -->`, adicionar o bloco correspondente. Exemplos:

```xml
<!-- Lanternas -->
<url>
  <loc>https://trekko.com.br/equipamentos/lanternas</loc>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>

<!-- Hidratação -->
<url>
  <loc>https://trekko.com.br/equipamentos/hidratacao</loc>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>

<!-- Camping -->
<url>
  <loc>https://trekko.com.br/equipamentos/camping</loc>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>

<!-- Segurança -->
<url>
  <loc>https://trekko.com.br/equipamentos/seguranca</loc>
  <changefreq>weekly</changefreq>
  <priority>0.8</priority>
</url>

<!-- Pets Outdoor -->
<url>
  <loc>https://trekko.com.br/equipamentos/pets-outdoor</loc>
  <changefreq>weekly</changefreq>
  <priority>0.75</priority>
</url>

<!-- Ofertas -->
<url>
  <loc>https://trekko.com.br/equipamentos/ofertas</loc>
  <changefreq>daily</changefreq>
  <priority>0.85</priority>
</url>

<!-- Primeiros Socorros -->
<url>
  <loc>https://trekko.com.br/equipamentos/primeiros-socorros</loc>
  <lastmod>YYYY-MM-DD</lastmod>
  <changefreq>monthly</changefreq>
  <priority>0.90</priority>
</url>
```

> ⚠️ Substituir `YYYY-MM-DD` pela data real de publicação dos produtos.

### 3. Remover os comentários `<!-- DEV-04: ... -->` do `sitemap.xml`

Após readicionar as URLs, apagar os comentários de placeholder que foram deixados em DEV-04.

### 4. Validar antes de publicar

- [ ] Verificar via `curl -I https://trekko.com.br/equipamentos/<categoria>` que o `robots` não aparece mais no response header
- [ ] Abrir o HTML e confirmar que a tag `<meta name="robots">` diz `index,follow`
- [ ] Validar o sitemap em [Google Search Console > Sitemaps](https://search.google.com/search-console)
- [ ] Enviar a URL para re-rastreamento via **Inspeção de URL** no Search Console

---

## Critérios para reativar

Uma página só deve ser reindexada quando **todos** os itens abaixo estiverem satisfeitos:

- [ ] A seção de produtos tem ao menos **3 produtos reais** com links afiliados ativos
- [ ] Os links de afiliado estão verificados e funcionando
- [ ] O conteúdo editorial está alinhado com os produtos listados
- [ ] A mensagem `"Em breve"` / `empty-sub` foi removida da página

---

*Documento criado em DEV-04 · 2026-05-27*
