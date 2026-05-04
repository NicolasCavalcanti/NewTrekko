# Trekko — Guia de Configuração de Tracking

Referência técnica para configurar GTM, GA4 e Google Ads com base na estrutura implementada em `assets/trekko-analytics.js`.

---

## 1. Estado atual

| Componente | Status | Observação |
|---|---|---|
| GA4 `G-S816P190VN` | ✅ Ativo | gtag.js direto em todas as páginas |
| Google Tag Manager | ⚠️ Pendente | Script condicional adicionado — aguarda container ID |
| Google Ads Conversion | ⚠️ Pendente | ADS_ID vazio — aguarda conta Google Ads |
| `window.TrekkoAnalytics` | ✅ Ativo | `assets/trekko-analytics.js` em todas as páginas |
| SPA routing (page_view) | ✅ Ativo | Listener de history no `trekko-analytics.js` |
| Conversão formulário guia | ✅ Corrigido | Evento fires APÓS `res.ok`, não antes |
| Scroll depth 50%/90% | ✅ Ativo | Auto-iniciado pelo `trekko-analytics.js` |

---

## 2. Ativar o Google Tag Manager

### 2.1 Criar o container

1. Acesse [tagmanager.google.com](https://tagmanager.google.com)
2. Crie uma conta → Container → Tipo: **Web**
3. Anote o ID do container: `GTM-XXXXXXX`

### 2.2 Configurar o ID no código

Edite o `window.TREKKO_CONFIG` em **todos** os arquivos HTML abaixo, substituindo `GTM_ID: ''` por `GTM_ID: 'GTM-XXXXXXX'`:

```
index.html
404.html
guias/ativar-perfil/index.html
trilhas/sao-paulo/index.html
trilhas/rio-de-janeiro/index.html
trilhas/minas-gerais/index.html
trilhas/para-iniciantes/index.html
trilhas/com-cachoeira/index.html
trilhas/com-guia/index.html
```

Também atualize o `noscript` iframe em `index.html` e `404.html`:
```html
<iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX" ...>
```

Após preencher `GTM_ID`, o GA4 direto deixa de enviar `page_view` automaticamente
(flag `send_page_view: false` já configurada). O GTM assumirá o controle.

### 2.3 Tags essenciais no GTM

#### GA4 Configuration Tag
- Tipo: **Google Analytics: GA4 Configuration**
- Measurement ID: `G-S816P190VN`
- Trigger: **All Pages** (initialization)
- ⚠️ Marcar "Send a page view event when this configuration loads" = **OFF** (o `trekko-analytics.js` envia via dataLayer)

#### GA4 Event Tag — página_view SPA
- Tipo: GA4 Event
- Event Name: `page_view`
- Parâmetros do evento: todos vindos do dataLayer (ver seção 4)
- Trigger: **Custom Event** `page_view`

#### GA4 Event Tags — eventos principais
Para cada evento abaixo, criar uma tag GA4 Event com trigger Custom Event correspondente:

| Tag | Trigger (Custom Event) |
|---|---|
| GA4 - trail_view | `trail_view` |
| GA4 - guide_profile_view | `guide_profile_view` |
| GA4 - click_whatsapp_guide | `click_whatsapp_guide` |
| GA4 - lead_guide_request | `lead_guide_request` |
| GA4 - form_submit_guide_activation | `form_submit_guide_activation` |
| GA4 - guide_signup_complete | `guide_signup_complete` |
| GA4 - search_trail | `search_trail` |
| GA4 - filter_trails | `filter_trails` |
| GA4 - click_trail_card | `click_trail_card` |
| GA4 - click_guide_card | `click_guide_card` |
| GA4 - guide_signup_start | `guide_signup_start` |
| GA4 - form_start_guide_activation | `form_start_guide_activation` |
| GA4 - scroll_50 | `scroll_50` |
| GA4 - scroll_90 | `scroll_90` |
| GA4 - save_trail | `save_trail` |

---

## 3. Configurar GA4 — Conversões

Acesse **GA4 → Administrador → Eventos** e marque como conversão:

### Conversões principais (Primary)
| Evento | Justificativa |
|---|---|
| `click_whatsapp_guide` | Contato direto com guia — principal ação de trilheiro |
| `lead_guide_request` | Envio de formulário de solicitação de guia |
| `form_submit_guide_activation` | Guia concluiu envio de formulário de ativação |
| `guide_signup_complete` | Guia completou ativação de perfil |

### Microconversões (marcar como evento, não conversão)
`trail_view`, `guide_profile_view`, `search_trail`, `filter_trails`,
`click_trail_card`, `click_guide_card`, `guide_signup_start`,
`form_start_guide_activation`, `click_activate_profile`,
`click_register_new_guide`, `save_trail`, `scroll_50`, `scroll_90`

### Parâmetros customizados — registrar no GA4
Em **Configuração → Definições customizadas**, registre como **Event-scoped**:

```
page_type, trail_id, trail_slug, trail_name, guide_id, guide_name,
state, city, region, difficulty, distance_km, elevation_gain,
guide_required, has_cadastur, cadastur_status, profile_status,
source_page, cta_text, cta_location, form_name, search_term,
results_count, filter_type, filter_value, distance_range,
experience_type, request_type, content_group
```

---

## 4. Configurar Google Ads Conversion Tracking

### 4.1 Criar conta e obter o ADS_ID

1. Acesse [ads.google.com](https://ads.google.com)
2. **Ferramentas → Medições → Conversões → Nova ação de conversão**
3. Anote o ID da conta: `AW-XXXXXXXXX`
4. Preencha `ADS_ID: 'AW-XXXXXXXXX'` no `TREKKO_CONFIG` de todos os HTMLs

### 4.2 Criar ações de conversão

| Nome da conversão | Evento de origem | Categoria | Contagem | Janela |
|---|---|---|---|---|
| Lead guia/trilheiro | `lead_guide_request` | Lead | 1 por clique | 30 dias |
| Clique WhatsApp guia | `click_whatsapp_guide` | Contact | 1 por clique | 30 dias |
| Ativação perfil guia | `form_submit_guide_activation` | Sign-up | 1 por clique | 60 dias |
| Cadastro guia completo | `guide_signup_complete` | Sign-up | 1 por clique | 60 dias |

**Configurações recomendadas:**
- Modelo de atribuição: **Data-driven** (requer histórico) ou **Linear** inicialmente
- Contagem: **Uma conversão** por clique para todas as conversões acima
- Incluir conversões: **Sim** para todas

### 4.3 Tags Google Ads no GTM

Para cada conversão, criar uma tag no GTM:

```
Tag: Google Ads Conversion — click_whatsapp_guide
Tipo: Google Ads Conversion Tracking
Conversion ID: AW-XXXXXXXXX
Conversion Label: [label gerado na conversão]
Trigger: Custom Event — click_whatsapp_guide
```

Repetir para `lead_guide_request`, `form_submit_guide_activation`, `guide_signup_complete`.

### 4.4 Importar conversões GA4 para Google Ads (alternativa)

Se preferir não usar tags diretas no GTM:
1. Google Ads → **Ferramentas → Conversões → Importar → Google Analytics 4**
2. Importar: `click_whatsapp_guide`, `lead_guide_request`, `form_submit_guide_activation`, `guide_signup_complete`
3. Marcar como **Primária** para campanhas ativas
4. ⚠️ **Não usar importação GA4 E tag direta simultaneamente** — escolher um método para evitar duplicidade

---

## 5. Consent Mode v2 (recomendado)

Adicionar antes do GTM em todos os HTMLs:

```html
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
// Default: negado até consentimento
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'analytics_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'wait_for_update': 500
});
</script>
```

Após consentimento do usuário (banner de cookies):

```javascript
gtag('consent', 'update', {
  'ad_storage': 'granted',
  'analytics_storage': 'granted',
  'ad_user_data': 'granted',
  'ad_personalization': 'granted'
});
```

**Notas LGPD:**
- Política de Privacidade já está no rodapé de todas as páginas
- Formulários já têm aviso de coleta de dados
- Dados de e-mail e telefone NÃO são enviados ao analytics (apenas ao FormSubmit.co)
- Somente metadados categóricos (estado, cidade, has_cadastur) são rastreados

---

## 6. Eventos implementados por página

### `index.html` (SPA React — todas as rotas)
| Evento | Disparado por |
|---|---|
| `page_view` | Cada mudança de rota (pushState/replaceState/popstate) |
| `scroll_50` / `scroll_90` | Auto (trekko-analytics.js) |
| Todos os demais eventos | Componentes React via `window.TrekkoAnalytics.*` |

> Para rastrear eventos dentro do React SPA (trail_view, guide_profile_view, click_whatsapp_guide etc.),
> os componentes devem chamar `window.TrekkoAnalytics.trackTrailView(trail)` etc.
> Ver seção 7 para exemplos de integração.

### `/guias/ativar-perfil`
| Evento | Trigger |
|---|---|
| `page_view` + `page_view_guide_activation` | window.load |
| `form_start_guide_activation` + `guide_signup_start` | Primeiro input no formulário |
| `form_submit_guide_activation` + `guide_signup_complete` | Após `res.ok` da requisição |
| `click_activate_profile` | data-event no botão |
| `click_register_new_guide` | data-event no botão |
| `click_whatsapp_guide_support` | data-event no link WhatsApp |
| `scroll_50` / `scroll_90` | Auto (trekko-analytics.js) |

### Landing pages de trilhas (`/trilhas/[estado|intenção]`)
| Evento | Trigger |
|---|---|
| `page_view` + `page_view_trail_landing` | window.load |
| `filter_trails` | Mudança em qualquer filtro |
| `click_trail_card` etc. | data-event nos cards |
| `scroll_50` / `scroll_90` | Auto (trekko-analytics.js) |

---

## 7. Integração com o React SPA

O arquivo compilado `assets/index-DSKK19TW.js` não pode ser modificado diretamente.
Para integrar eventos de conversão nos componentes React, o código-fonte deve chamar:

```typescript
// Em qualquer componente React
declare global {
  interface Window { TrekkoAnalytics: any; }
}

// Trail detail page
window.TrekkoAnalytics?.trackTrailView({
  trail_id: trail.id,
  trail_slug: trail.slug,
  trail_name: trail.name,
  state: trail.uf,
  city: trail.city,
  difficulty: trail.difficulty,
  distance_km: trail.distanceKm,
  guide_required: trail.guideRequired
});

// WhatsApp click
window.TrekkoAnalytics?.trackWhatsappClick({
  guide_id: guide.id,
  guide_name: guide.name,
  state: guide.uf,
  city: guide.city,
  trail_id: currentTrail?.id,
  trail_name: currentTrail?.name,
  source_page: window.location.pathname
});

// Guide profile view
window.TrekkoAnalytics?.trackGuideView({
  guide_id: guide.id,
  guide_name: guide.name,
  state: guide.uf,
  city: guide.city,
  cadastur_status: guide.cadastur ? 'active' : 'none',
  profile_status: guide.status
});
```

---

## 8. Validação

### GTM Preview Mode
1. GTM → **Preview** → inserir URL do site
2. Verificar que os seguintes eventos chegam corretamente:
   - `page_view` ao navegar entre rotas
   - `form_start_guide_activation` ao digitar no formulário
   - `form_submit_guide_activation` **após** submit com sucesso
   - `filter_trails` ao aplicar filtro
   - `scroll_50` / `scroll_90` ao rolar

### GA4 DebugView
1. Instalar extensão Chrome: **Google Analytics Debugger**
2. GA4 → **Administrador → DebugView**
3. Navegar pelo site e verificar:
   - `page_view` com `page_type` correto em cada rota
   - Parâmetros sem dados pessoais (sem email, telefone)
   - Sem eventos duplicados
   - Conversões marcadas com ícone de funil

### Checklist antes de ir ao ar
- [ ] GTM_ID preenchido em todos os HTMLs
- [ ] ADS_ID preenchido em todos os HTMLs (quando disponível)
- [ ] Noscript iframe atualizado com GTM-XXXXXXX real
- [ ] Conversões criadas no GA4 e marcadas como Primary
- [ ] Conversões importadas ou tags Google Ads configuradas
- [ ] Teste do formulário de guia: evento só dispara após sucesso
- [ ] Teste de bloqueador de anúncios: site não quebra
- [ ] Nenhum dado pessoal visível no DebugView (e-mail, telefone, CPF)

---

## 9. Referência de eventos

### Nomenclatura padronizada
Todos os eventos usam **snake_case em inglês**.

| Parâmetro universal | Descrição |
|---|---|
| `page_type` | Tipo da página: `home`, `trail_listing`, `trail_detail`, `guide_listing`, `guide_detail`, `guide_activation_landing`, `trail_state_landing`, `trail_intent_landing`, `blog_detail`, `contact`, `institutional` |
| `page_path` | Caminho da URL sem domínio |
| `source_page` | Página de onde o evento foi disparado |
| `state` | Estado brasileiro (slug, ex: `sao-paulo`) |
| `city` | Cidade (nome) |
| `difficulty` | `facil`, `moderado`, `dificil`, `muito-dificil` |

### API pública — `window.TrekkoAnalytics`

```javascript
TrekkoAnalytics.trackEvent(name, params)
TrekkoAnalytics.trackPageView(params)
TrekkoAnalytics.trackTrailView(trail)
TrekkoAnalytics.trackGuideView(guide)
TrekkoAnalytics.trackWhatsappClick(data)
TrekkoAnalytics.trackFormStart(formName, extra)
TrekkoAnalytics.trackFormSubmit(formName, data)   // chamar APENAS após sucesso
TrekkoAnalytics.trackSearch(data)
TrekkoAnalytics.trackFilter(data)
TrekkoAnalytics.trackTrailCardClick(data)
TrekkoAnalytics.trackGuideCardClick(data)
TrekkoAnalytics.trackLeadGuideRequest(data)
TrekkoAnalytics.trackGuideSignupStart(data)
TrekkoAnalytics.trackGuideSignupComplete(data)    // CONVERSÃO PRINCIPAL
TrekkoAnalytics.trackSaveTrail(data)
TrekkoAnalytics.getPageType(path)
```
