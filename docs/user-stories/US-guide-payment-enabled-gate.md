# US — Bloqueio de Pagamentos para Guias sem Chave Pix Válida

## Title
**Como plataforma**, quero marcar automaticamente um guia como "pagamentos não habilitados" quando ele não possui chave Pix válida registrada, **para que** nenhuma reserva paga seja criada sem garantia de repasse, protegendo trekkers e a integridade financeira do sistema.

---

## Description

O sistema deriva o estado `paymentsEnabled` de cada guia a partir de dois campos já existentes em `guide_verification`:

- `pixKeyVerified = 1` → chave registrada e validada
- `status IN ('pending', 'approved')` → verificação não rejeitada nem suspensa

Se qualquer uma dessas condições falhar — ou se o registro `guide_verification` não existir — o guia é considerado **"pagamentos não habilitados"**.

Esse estado é verificado em três pontos de enforcement:

1. **Checkout do trekker** — a mutation `expeditions.enrollUser` rejeita a reserva antes de qualquer criação de registro.
2. **Listagem de expedições** — cards exibem badge visual "Pagamentos não habilitados" para o trekker (sem expor detalhes internos).
3. **Dashboard do guia** — banner persistente com CTA para configurar/corrigir chave Pix.

Quando o guia registra uma chave válida, o estado se resolve automaticamente — nenhuma ação manual de admin é necessária para re-habilitar.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Elimina o risco de criar reservas pagas sem destino de repasse, evitando disputas e reembolsos forçados. |
| 2 | Trekkers não chegam ao checkout de expedições com pagamento irrepasse — reduz abandono e frustração. |
| 3 | Auto-resolução ao registrar Pix elimina intervenção manual de admin para re-habilitar guias. |
| 4 | Suspensão/rejeição da verificação desabilita pagamentos imediatamente, sem necessitar de nova entidade de controle. |

---

## Acceptance Criteria

```gherkin
Feature: Bloqueio de pagamentos para guias sem Pix válido

  # ─── Definição do estado ─────────────────────────────────────────

  Scenario Outline: Estado paymentsEnabled derivado das condições
    Given o guia possui o seguinte estado em guide_verification:
      | pixKeyVerified | status      | paymentsEnabled esperado |
      | ausente (sem registro) | —      | false                    |
      | 0              | pending     | false                    |
      | 0              | approved    | false                    |
      | 1              | pending     | true                     |
      | 1              | approved    | true                     |
      | 1              | rejected    | false                    |
      | 1              | suspended   | false                    |
    Then guides.getById retorna paymentsEnabled = <esperado>

  # ─── Bloqueio no checkout ────────────────────────────────────────

  Scenario: Trekker tenta reservar expedição de guia sem Pix
    Given o guia da expedição tem paymentsEnabled = false
    When um trekker chama a mutation "expeditions.enrollUser"
    Then a mutation retorna erro PRECONDITION_FAILED com code "guide_payments_not_enabled"
    And nenhum registro é criado em "reservations"
    And o frontend exibe: "Este guia ainda não habilitou o recebimento de pagamentos. Tente novamente em breve."

  Scenario: Trekker reserva normalmente quando guia tem Pix válido
    Given o guia tem pixKeyVerified = 1 e status "pending" ou "approved"
    When um trekker chama "expeditions.enrollUser"
    Then a reserva é criada com status "created"
    And o fluxo de pagamento prossegue normalmente via Mercado Pago

  Scenario: Guia com status "rejected" bloqueia novas reservas
    Given o guia tinha pixKeyVerified = 1
    And um admin rejeita a verificação (status = "rejected")
    When um trekker tenta reservar qualquer expedição desse guia
    Then a mutation retorna PRECONDITION_FAILED: "guide_payments_not_enabled"

  Scenario: Guia com status "suspended" bloqueia novas reservas
    Given o guia tinha paymentsEnabled = true
    And um admin suspende a verificação (status = "suspended")
    When um trekker tenta reservar
    Then a mutation retorna PRECONDITION_FAILED: "guide_payments_not_enabled"

  # ─── Re-habilitação automática ───────────────────────────────────

  Scenario: Guia habilita pagamentos ao registrar chave Pix válida
    Given o guia não possuía guide_verification ou pixKeyVerified = 0
    When o guia salva uma chave Pix válida via "guides.savePixData"
    Then pixKeyVerified é atualizado para 1
    And paymentsEnabled passa a ser true automaticamente
    And na próxima tentativa de reserva, o trekker consegue prosseguir normalmente
    And o banner de aviso desaparece do dashboard do guia

  # ─── Dashboard do guia ───────────────────────────────────────────

  Scenario: Banner exibido quando paymentsEnabled = false
    Given o guia acessa "/guia"
    And paymentsEnabled = false
    Then o sistema exibe um CalloutBanner com severidade "warning"
    And o texto é: "Seus pagamentos estão desabilitados. Configure sua chave Pix para receber reservas."
    And o banner contém botão "Configurar Pix" que redireciona para "/guia/configuracoes/pix"
    And o banner é visível em todas as sub-rotas do dashboard (/guia/*)

  Scenario: Banner não exibido quando paymentsEnabled = true
    Given o guia tem pixKeyVerified = 1 e status "pending"
    When acessa o dashboard
    Then o CalloutBanner de Pix NÃO é renderizado

  Scenario: Banner com mensagem distinta para status "rejected"
    Given status da guide_verification é "rejected"
    When o guia acessa o dashboard
    Then o banner exibe: "Sua verificação foi rejeitada. Revise seus dados financeiros."
    And o botão direciona para "/guia/configuracoes/pix" com estado expandido no campo de rejeição

  Scenario: Banner com mensagem distinta para status "suspended"
    Given status da guide_verification é "suspended"
    When o guia acessa o dashboard
    Then o banner exibe: "Sua conta está suspensa. Entre em contato com o suporte."
    And o botão exibe "Falar com Suporte" (link externo para canal de suporte)

  # ─── Listagem de expedições (visão do trekker) ───────────────────

  Scenario: Badge exibido no card da expedição quando guia sem Pix
    Given o guia da expedição tem paymentsEnabled = false
    When o trekker visualiza o card da expedição na listagem
    Then o card exibe um badge: "Indisponível para reserva"
    And o botão de reserva fica desabilitado (disabled)
    And nenhum detalhe interno (Pix, verificação) é exposto ao trekker

  Scenario: Botão de reserva habilitado quando guia tem Pix válido
    Given paymentsEnabled = true
    When o trekker visualiza o card
    Then o botão "Reservar" está habilitado normalmente

  # ─── Audit log ───────────────────────────────────────────────────

  Scenario: Evento registrado ao bloquear tentativa de reserva
    Given paymentsEnabled = false para o guia
    When um trekker tenta reservar
    Then um registro é criado em "payment_audit_log":
      | entityType  | "reservation"               |
      | action      | "enrollment_blocked"        |
      | actorType   | "system"                    |
      | payload     | { guideId, expeditionId, reason: "guide_payments_not_enabled" } |
```

---

## Technical Notes

### 1 — Função utilitária `isGuidePaymentsEnabled`
Centralizar a lógica de derivação do estado em uma função reutilizável:

```typescript
// server/lib/paymentsGate.ts

type GuideVerificationRow = {
  pixKeyVerified: number | null;
  status: "pending" | "approved" | "rejected" | "suspended" | null;
} | null | undefined;

export function isGuidePaymentsEnabled(verification: GuideVerificationRow): boolean {
  if (!verification) return false;
  if (verification.pixKeyVerified !== 1) return false;
  if (!["pending", "approved"].includes(verification.status ?? "")) return false;
  return true;
}
```

### 2 — Guard em `expeditions.enrollUser`

```typescript
// server/routers.ts — expeditions.enrollUser
const verification = await db.getGuideVerification(expedition.guideId);
if (!isGuidePaymentsEnabled(verification)) {
  await db.createAuditLog({
    entityType: "reservation",
    action: "enrollment_blocked",
    actorId: String(ctx.user.id),
    actorType: "system",
    payload: JSON.stringify({
      guideId: expedition.guideId,
      expeditionId: input.expeditionId,
      reason: "guide_payments_not_enabled",
    }),
  });
  throw new TRPCError({
    code: "PRECONDITION_FAILED",
    message: "guide_payments_not_enabled",
  });
}
```

### 3 — Expor `paymentsEnabled` em `guides.getById`
Adicionar ao retorno da query pública para que o frontend desabilite o botão de reserva **antes** do trekker chegar ao checkout:

```typescript
// server/routers.ts — guides.getById
const verification = await db.getGuideVerification(guide.userId);
return {
  ...guide,
  paymentsEnabled: isGuidePaymentsEnabled(verification),
  // NÃO expor pixKey, pixKeyType, documentNumber, status — dados internos
};
```

### 4 — Banner no dashboard do guia
Lógica de mensagem baseada em `status` + `pixKeyVerified`:

```typescript
// client/src/components/GuidePaymentBanner.tsx

function getBannerConfig(verification: GuideVerification | null) {
  if (!verification || verification.pixKeyVerified !== 1) {
    return {
      message: "Seus pagamentos estão desabilitados. Configure sua chave Pix para receber reservas.",
      cta: { label: "Configurar Pix", href: "/guia/configuracoes/pix" },
    };
  }
  if (verification.status === "rejected") {
    return {
      message: "Sua verificação foi rejeitada. Revise seus dados financeiros.",
      cta: { label: "Revisar dados", href: "/guia/configuracoes/pix" },
    };
  }
  if (verification.status === "suspended") {
    return {
      message: "Sua conta está suspensa. Entre em contato com o suporte.",
      cta: { label: "Falar com Suporte", href: SUPPORT_URL, external: true },
    };
  }
  return null; // paymentsEnabled = true, sem banner
}
```

Renderizar em todos os layouts do dashboard via `GuideLayout.tsx`:

```tsx
const banner = getBannerConfig(verification);
{banner && <CalloutBanner severity="warning" message={banner.message} cta={banner.cta} />}
```

### 5 — Card de expedição (visão do trekker)
Em `ExpeditionCard.tsx`, usar `paymentsEnabled` retornado por `guides.getById`:

```tsx
<Button
  disabled={!expedition.guide.paymentsEnabled}
  title={!expedition.guide.paymentsEnabled ? "Indisponível para reserva" : undefined}
>
  {expedition.guide.paymentsEnabled ? "Reservar" : "Indisponível"}
</Button>
{!expedition.guide.paymentsEnabled && (
  <Badge variant="warning">Indisponível para reserva</Badge>
)}
```

### 6 — Sem nova coluna de banco de dados
`paymentsEnabled` é **sempre derivado** em tempo de execução. Não adicionar coluna `paymentEnabled` em `users` ou `guide_verification` — isso criaria estado redundante sujeito a inconsistências. A fonte de verdade permanece sendo `pixKeyVerified` + `status` em `guide_verification`.

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|--------|---------|---------|
| Nova função utilitária | `isGuidePaymentsEnabled(verification)` | `server/lib/paymentsGate.ts` |
| tRPC `expeditions.enrollUser` | Guard com `isGuidePaymentsEnabled` + audit log | `server/routers.ts` |
| tRPC `guides.getById` | Adicionar campo `paymentsEnabled: boolean` na resposta | `server/routers.ts` |
| Frontend — layout do guia | `GuidePaymentBanner` com 3 variações de mensagem | `GuideLayout.tsx` |
| Frontend — card de expedição | Botão desabilitado + badge quando `paymentsEnabled = false` | `ExpeditionCard.tsx` |
| Schema / Migrations | **Nenhuma alteração necessária** | — |

### Contrato de resposta atualizado — `guides.getById`

```typescript
// Campos adicionados — nenhum removido
{
  // ... campos existentes do guia
  paymentsEnabled: boolean; // derivado: pixKeyVerified=1 AND status IN ('pending','approved')
}
```

### Erro tRPC

| Code | Message | Disparado por |
|------|---------|---------------|
| `PRECONDITION_FAILED` | `guide_payments_not_enabled` | `expeditions.enrollUser` quando `paymentsEnabled = false` |

### Regras de derivação (tabela de verdade)

| `guide_verification` existe | `pixKeyVerified` | `status` | `paymentsEnabled` |
|---|---|---|---|
| Não | — | — | `false` |
| Sim | `0` | qualquer | `false` |
| Sim | `1` | `pending` | `true` |
| Sim | `1` | `approved` | `true` |
| Sim | `1` | `rejected` | `false` |
| Sim | `1` | `suspended` | `false` |
