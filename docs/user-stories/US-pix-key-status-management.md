# US — Gerenciamento de Status da Chave Pix

## Title
**Como plataforma**, quero que cada chave Pix de guia tenha um status explícito com ciclo de vida definido — Pendente, Válida, Inválida, Pagamento Habilitado, Pagamento Bloqueado — **para que** o sistema saiba exatamente o que pode ser feito em cada estado e guias e admins tenham visibilidade clara da situação financeira da conta.

---

## Description

O campo `guide_payment_methods.status` é expandido de `"active" | "inactive" | "pending_verification"` para um enum de 5 estados que modela o ciclo de vida completo de uma chave Pix:

```
pending ──[validação passa]──► valid ──[guide_verification ativa]──► payment_enabled
   │                             │                                          │
   │[validação falha]            │[guide suspensa/rejeitada]     [guide suspensa/rejeitada]
   ▼                             ▼                                          │
invalid ◄──[guia resubmete]── payment_blocked ◄──────────────────────────►┘
                                    │
                         [guide_verification restaurada]
                                    │
                                    ▼
                            payment_enabled
```

**Separação de responsabilidades entre os dois eixos:**

- **Eixo da chave** (`pending` → `valid` | `invalid`): controlado exclusivamente por `validatePixKey()` no momento do save.
- **Eixo do pagamento** (`payment_enabled` ↔ `payment_blocked`): controlado pela combinação de `status = 'valid'` + `guide_verification.status`.

O estado `payment_enabled` / `payment_blocked` é atualizado de forma reativa sempre que `guide_verification.status` muda — sem intervenção manual para re-habilitar guias cuja verificação foi restaurada.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Estados explícitos eliminam lógica de derivação espalhada — uma consulta ao `status` resolve o que o sistema pode fazer. |
| 2 | Admins conseguem filtrar guias por estado financeiro sem joins complexos entre `guide_payment_methods` e `guide_verification`. |
| 3 | Transições reativas a `guide_verification` garantem que suspensão/reativação de guias propague imediatamente ao status Pix. |
| 4 | `invalid` como estado explícito distingue "guia nunca configurou" de "guia tentou configurar e falhou" — dado útil para suporte. |

---

## Acceptance Criteria

```gherkin
Feature: Ciclo de vida do status da chave Pix

  # ─── Estado inicial ──────────────────────────────────────────────

  Scenario: Novo registro criado com status pending
    Given o guia acaba de criar sua conta e ainda não submeteu uma chave Pix
    When um registro é criado em guide_payment_methods (ex: via onboarding step)
    Then status = "pending"
    And nenhum payout pode ser agendado para esse guia
    And enrollment de trekkers é bloqueado (paymentsEnabled = false)

  # ─── Transição pending → valid / invalid ─────────────────────────

  Scenario: Chave Pix salva com formato válido → status valid
    Given o guia está em status "pending"
    And guide_verification.status NÃO é "pending" ou "approved"
    When o guia salva uma chave Pix que passa em validatePixKey()
    Then guide_payment_methods.status = "valid"
    And um evento "pix_status_changed" é registrado: pending → valid

  Scenario: Chave Pix salva com formato válido + guide_verification ativa → payment_enabled
    Given o guia está em status "pending"
    And guide_verification.status É "pending" ou "approved"
    When o guia salva uma chave Pix que passa em validatePixKey()
    Then guide_payment_methods.status = "payment_enabled" (pula "valid")
    And paymentsEnabled = true imediatamente
    And enrollment de trekkers é liberado

  Scenario: Chave Pix salva com formato inválido → status invalid
    Given o guia está em qualquer estado (pending, valid, payment_enabled)
    When o guia tenta salvar uma chave que falha em validatePixKey()
    Then guide_payment_methods.status = "invalid"
    And o erro específico é retornado (ex: "pix_key_cpf_invalid")
    And paymentsEnabled = false
    And um evento "pix_status_changed" é registrado

  # ─── Transição valid ↔ payment_enabled / payment_blocked ─────────

  Scenario: guide_verification aprovada com chave valid → payment_enabled
    Given guide_payment_methods.status = "valid"
    When guide_verification.status é atualizado para "pending" ou "approved"
    Then guide_payment_methods.status = "payment_enabled" automaticamente
    And um evento "pix_status_changed" é registrado: valid → payment_enabled

  Scenario: Guide suspensa com payment_enabled → payment_blocked
    Given guide_payment_methods.status = "payment_enabled"
    When admin atualiza guide_verification.status para "suspended"
    Then guide_payment_methods.status = "payment_blocked" automaticamente
    And paymentsEnabled = false imediatamente
    And novos enrollments são bloqueados
    And payouts já agendados (status="scheduled") são marcados como "blocked"
    And um evento "pix_status_changed" é registrado: payment_enabled → payment_blocked

  Scenario: Guide rejeitada com payment_enabled → payment_blocked
    Given guide_payment_methods.status = "payment_enabled"
    When admin atualiza guide_verification.status para "rejected"
    Then guide_payment_methods.status = "payment_blocked" automaticamente

  Scenario: Guide reativada com payment_blocked → payment_enabled
    Given guide_payment_methods.status = "payment_blocked"
    And a chave Pix continua válida (pixKey e pixKeyType não foram alterados)
    When admin restaura guide_verification.status para "pending" ou "approved"
    Then guide_payment_methods.status = "payment_enabled" automaticamente
    And paymentsEnabled = true imediatamente
    And um evento "pix_status_changed" é registrado: payment_blocked → payment_enabled

  Scenario: Guide com valid + status mudado para rejected → payment_blocked
    Given guide_payment_methods.status = "valid"
    When guide_verification.status → "rejected"
    Then guide_payment_methods.status = "payment_blocked"
    And NÃO vai para "payment_enabled" (a chave é válida mas pagamento está bloqueado)

  # ─── Transição invalid → resubmissão ─────────────────────────────

  Scenario: Guia corrige e resubmete a chave após status invalid
    Given guide_payment_methods.status = "invalid"
    When o guia submete uma nova chave que passa em validatePixKey()
    Then o método inválido é arquivado (archivedAt = NOW())
    And um novo registro é criado com status = "valid" ou "payment_enabled"
    And eventos de auditoria registram o arquivamento + criação

  # ─── Transições proibidas ─────────────────────────────────────────

  Scenario Outline: Transições de estado não permitidas são rejeitadas
    Given guide_payment_methods.status = "<estado_origem>"
    When o sistema tenta transicionar para "<estado_destino>"
    Then a operação lança InvalidStateTransitionError
    And o status permanece "<estado_origem>"

    Exemplos:
      | estado_origem   | estado_destino    | motivo                                        |
      | invalid         | payment_enabled   | inválido não pode habilitar pagamento diretamente |
      | invalid         | payment_blocked   | inválido não percorre eixo de pagamento       |
      | pending         | payment_blocked   | pendente não percorre eixo de pagamento       |
      | payment_enabled | pending           | regressão de estado proibida                  |
      | valid           | pending           | regressão de estado proibida                  |

  # ─── Efeitos por estado ───────────────────────────────────────────

  Scenario Outline: Efeito operacional de cada status
    Given guide_payment_methods.status = "<status>"
    Then paymentsEnabled = <payments_enabled>
    And enrollment de trekkers = <enrollment>
    And agendamento de payout = <payout>

    Exemplos:
      | status           | payments_enabled | enrollment    | payout        |
      | pending          | false            | bloqueado     | bloqueado     |
      | valid            | false            | bloqueado     | bloqueado     |
      | invalid          | false            | bloqueado     | bloqueado     |
      | payment_enabled  | true             | permitido     | permitido     |
      | payment_blocked  | false            | bloqueado     | bloqueado     |

  # ─── Visibilidade no dashboard do guia ───────────────────────────

  Scenario Outline: Label e cor exibidos por status no dashboard
    Given guide_payment_methods.status = "<status>"
    When o guia acessa "/guia/configuracoes/pix"
    Then o badge exibe label "<label>" com variante "<variante>"
    And a descrição exibe "<descricao>"

    Exemplos:
      | status           | label                 | variante  | descricao                                              |
      | pending          | Pendente              | warning   | Configure sua chave Pix para receber pagamentos        |
      | valid            | Válida                | info      | Chave válida. Aguardando ativação da conta             |
      | invalid          | Inválida              | error     | Chave Pix inválida. Revise os dados e tente novamente  |
      | payment_enabled  | Pagamento Habilitado  | success   | Tudo pronto! Você pode receber pagamentos              |
      | payment_blocked  | Pagamento Bloqueado   | error     | Pagamentos suspensos. Entre em contato com o suporte   |

  # ─── Admin ────────────────────────────────────────────────────────

  Scenario: Admin filtra guias por status Pix
    When admin chama "admin.listGuidesByPixStatus" com status = "payment_blocked"
    Then retorna apenas guias com guide_payment_methods.status = "payment_blocked"

  Scenario: Admin força transição para inválido
    Given admin identifica uma chave Pix fraudulenta
    When chama "admin.invalidatePixKey" com guideId e motivo
    Then guide_payment_methods.status = "invalid"
    And evento registrado em payment_audit_log com actorType = "admin" e motivo
    And paymentsEnabled = false imediatamente

  # ─── Audit de transições ─────────────────────────────────────────

  Scenario: Toda transição de estado gera evento em payment_audit_log
    When qualquer transição de status ocorre
    Then um evento "pix_status_changed" é registrado com:
      | previousValue | { status: "<estado_anterior>" }    |
      | newValue      | { status: "<novo_estado>",         |
      |               |   trigger: "<gatilho>",            |
      |               |   triggeredBy: "<actorType>" }     |
    And o campo "trigger" descreve o que causou a transição:
      | Gatilho                          | Valor de trigger                |
      | validatePixKey() passou          | "validation_passed"             |
      | validatePixKey() falhou          | "validation_failed"             |
      | guide_verification ativa         | "guide_verification_activated"  |
      | guide_verification suspensa      | "guide_verification_suspended"  |
      | guide_verification rejeitada     | "guide_verification_rejected"   |
      | guide_verification restaurada    | "guide_verification_restored"   |
      | admin invalidou manualmente      | "admin_invalidation"            |
```

---

## Technical Notes

### 1 — Enum expandido em `guide_payment_methods`

```typescript
// drizzle/schema.ts

export const guidePaymentMethods = mysqlTable("guide_payment_methods", {
  // ...
  status: mysqlEnum("status", [
    "pending",          // submetida, aguardando ou nunca validada
    "valid",            // passou validatePixKey(), guide_verification inativa
    "invalid",          // falhou validatePixKey() ou invalidada por admin
    "payment_enabled",  // válida + guide_verification ativa
    "payment_blocked",  // válida + guide_verification suspensa/rejeitada
  ]).notNull().default("pending"),
  // ...
});
```

Migration: renomear `"active"` → `"payment_enabled"`, `"pending_verification"` → `"pending"`, `"inactive"` → depende do contexto (avaliar caso a caso).

### 2 — Máquina de estados (`server/lib/pixKeyStateMachine.ts`)

Centralizar todas as transições permitidas e a lógica de próximo estado:

```typescript
export type PixKeyStatus =
  | "pending"
  | "valid"
  | "invalid"
  | "payment_enabled"
  | "payment_blocked";

type VerificationStatus = "pending" | "approved" | "rejected" | "suspended";

// Grafo de transições permitidas
const ALLOWED_TRANSITIONS: Record<PixKeyStatus, PixKeyStatus[]> = {
  pending:          ["valid", "payment_enabled", "invalid"],
  valid:            ["payment_enabled", "payment_blocked", "invalid"],
  invalid:          ["pending"],  // somente via resubmissão (arquiva + cria novo)
  payment_enabled:  ["payment_blocked", "invalid"],
  payment_blocked:  ["payment_enabled", "invalid"],
};

export function assertTransitionAllowed(from: PixKeyStatus, to: PixKeyStatus): void {
  if (!ALLOWED_TRANSITIONS[from].includes(to)) {
    throw new InvalidStateTransitionError(
      `Transition ${from} → ${to} is not allowed`
    );
  }
}

// Determina o próximo status após salvar uma chave validada
export function resolveStatusAfterValidation(
  validationPassed: boolean,
  verificationStatus: VerificationStatus | null
): PixKeyStatus {
  if (!validationPassed) return "invalid";
  const verificationActive = ["pending", "approved"].includes(verificationStatus ?? "");
  return verificationActive ? "payment_enabled" : "valid";
}

// Determina o próximo status quando guide_verification muda
export function resolveStatusAfterVerificationChange(
  currentPixStatus: PixKeyStatus,
  newVerificationStatus: VerificationStatus
): PixKeyStatus | null {  // null = sem mudança necessária
  const verificationActive = ["pending", "approved"].includes(newVerificationStatus);
  const pixIsValid = ["valid", "payment_enabled", "payment_blocked"].includes(currentPixStatus);

  if (!pixIsValid) return null; // pending/invalid não percorrem eixo de pagamento

  if (verificationActive && currentPixStatus !== "payment_enabled") return "payment_enabled";
  if (!verificationActive && currentPixStatus === "payment_enabled") return "payment_blocked";
  if (!verificationActive && currentPixStatus === "valid") return "payment_blocked";
  return null;
}
```

### 3 — Hook reativo em `guides.updateVerificationStatus` (admin)

Toda vez que `guide_verification.status` muda, propagar para `guide_payment_methods`:

```typescript
// server/routers.ts — admin.updateVerificationStatus

const activeMethod = await db.getDefaultPaymentMethod(input.guideId);
if (activeMethod) {
  const nextStatus = resolveStatusAfterVerificationChange(
    activeMethod.status,
    input.newStatus
  );
  if (nextStatus) {
    assertTransitionAllowed(activeMethod.status, nextStatus);
    await db.transaction(async (tx) => {
      await tx.updatePaymentMethod(activeMethod.id, { status: nextStatus });

      // Bloquear payouts agendados se payment_blocked
      if (nextStatus === "payment_blocked") {
        await tx.blockScheduledPayouts(input.guideId, "guide_verification_suspended");
      }

      await writePaymentAuditEvent(tx, {
        action: "pix_status_changed",
        entityId: activeMethod.id,
        actorId: ctx.user.id,
        actorType: "admin",
        previousValue: { status: activeMethod.status },
        newValue: {
          status: nextStatus,
          trigger: nextStatus === "payment_blocked"
            ? "guide_verification_suspended"
            : "guide_verification_restored",
          triggeredBy: "admin",
        },
        ipAddress: ctx.req.ip,
        userAgent: ctx.req.headers["user-agent"] ?? "unknown",
      });
    });
  }
}
```

### 4 — `isGuidePaymentsEnabled` simplificado

Com o estado explícito, a função de `paymentsGate.ts` (US-guide-payment-enabled-gate) torna-se trivial — sem joins:

```typescript
// Antes (derivava de 2 tabelas)
export async function isGuidePaymentsEnabled(guideId, db): Promise<boolean> {
  const verification = await db.getGuideVerification(guideId);
  const method = await db.getDefaultPaymentMethod(guideId);
  return method?.status === "active" && ["pending","approved"].includes(verification?.status);
}

// Depois (consulta única)
export async function isGuidePaymentsEnabled(guideId, db): Promise<boolean> {
  const method = await db.getDefaultPaymentMethod(guideId);
  return method?.status === "payment_enabled";
}
```

### 5 — Índice para query de admin por status

```sql
-- Para admin.listGuidesByPixStatus e dashboards
CREATE INDEX idx_payment_methods_status
  ON guide_payment_methods (status, is_default, archived_at);
```

### 6 — Mapeamento de apresentação (`shared/lib/pixStatusDisplay.ts`)

```typescript
export const PIX_STATUS_DISPLAY: Record<PixKeyStatus, {
  label: string;
  variant: "warning" | "info" | "error" | "success";
  description: string;
  canEdit: boolean;  // se o guia pode alterar a chave nesse estado
}> = {
  pending:         { label: "Pendente",             variant: "warning", description: "Configure sua chave Pix para receber pagamentos",       canEdit: true  },
  valid:           { label: "Válida",               variant: "info",    description: "Chave válida. Aguardando ativação da conta",            canEdit: true  },
  invalid:         { label: "Inválida",             variant: "error",   description: "Chave Pix inválida. Revise os dados e tente novamente", canEdit: true  },
  payment_enabled: { label: "Pagamento Habilitado", variant: "success", description: "Tudo pronto! Você pode receber pagamentos",            canEdit: true  },
  payment_blocked: { label: "Pagamento Bloqueado",  variant: "error",   description: "Pagamentos suspensos. Entre em contato com o suporte", canEdit: false },
};
```

`canEdit: false` para `payment_blocked` — impede que o guia altere a chave enquanto a conta está suspensa (alterar não resolveria o bloqueio).

### 7 — `InvalidStateTransitionError`

```typescript
// server/lib/pixKeyStateMachine.ts

export class InvalidStateTransitionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "InvalidStateTransitionError";
  }
}

// Mapeado em tRPC error handler:
// InvalidStateTransitionError → TRPCError code: "BAD_REQUEST", message: "invalid_state_transition"
```

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|---|---|---|
| Schema | `guide_payment_methods.status` enum expandido para 5 estados | `drizzle/schema.ts` |
| Migration | Renomear valores existentes: `active` → `payment_enabled`, `pending_verification` → `pending` | `drizzle/XXXX_expand_pix_status.sql` |
| State machine | `pixKeyStateMachine.ts`: grafo de transições, `resolveStatusAfterValidation`, `resolveStatusAfterVerificationChange`, `assertTransitionAllowed` | `server/lib/pixKeyStateMachine.ts` |
| `paymentsGate.ts` | Simplificar para consulta única: `method.status === "payment_enabled"` | `server/lib/paymentsGate.ts` |
| `admin.updateVerificationStatus` | Hook reativo: propagação de status Pix ao alterar `guide_verification` | `server/routers.ts` |
| `admin.invalidatePixKey` | Nova mutation: força transição para `invalid` com motivo | `server/routers.ts` |
| `admin.listGuidesByPixStatus` | Nova query: filtra guias por `guide_payment_methods.status` | `server/routers.ts` |
| Display map | `pixStatusDisplay.ts`: label, variante e descrição por estado | `shared/lib/pixStatusDisplay.ts` |
| Novo índice | `idx_payment_methods_status` em `guide_payment_methods` | `drizzle/` migration |
| `payment_audit_log` | Novo action: `"pix_status_changed"` com campo `trigger` | `drizzle/schema.ts` |

### Tabela de transições permitidas (referência rápida)

| De \ Para | pending | valid | invalid | payment_enabled | payment_blocked |
|---|---|---|---|---|---|
| **pending** | — | ✅ | ✅ | ✅ | ❌ |
| **valid** | ❌ | — | ✅ | ✅ | ✅ |
| **invalid** | ✅ | ❌ | — | ❌ | ❌ |
| **payment_enabled** | ❌ | ❌ | ✅ | — | ✅ |
| **payment_blocked** | ❌ | ❌ | ✅ | ✅ | — |

### Efeitos operacionais por estado (referência rápida)

| Status | `paymentsEnabled` | Enrollment | Payout agendável | Guia pode editar chave |
|---|---|---|---|---|
| `pending` | ❌ | Bloqueado | ❌ | ✅ |
| `valid` | ❌ | Bloqueado | ❌ | ✅ |
| `invalid` | ❌ | Bloqueado | ❌ | ✅ |
| `payment_enabled` | ✅ | Permitido | ✅ | ✅ |
| `payment_blocked` | ❌ | Bloqueado | ❌ | ❌ |
