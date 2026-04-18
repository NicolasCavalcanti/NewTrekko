# US — Execução do Repasse via Chave Pix

## Title
**Como plataforma**, quero recuperar automaticamente a chave Pix válida do guia e executar o repasse via Mercado Pago após o encerramento do período de contestação, **para que** os guias recebam seus pagamentos de forma automática, rastreável e com tratamento de falhas sem intervenção manual.

---

## Description

O fluxo de repasse é composto por três estágios sequenciais:

**1. Agendamento** — ao marcar uma reserva como concluída (após contestação encerrada), o sistema cria um registro `payout` com `status = "scheduled"` e `scheduledDate = completedAt + 2 dias úteis`. A chave Pix é snapshottada nesse momento a partir de `guide_payment_methods` (DB-SEC-01: criptografada).

**2. Execução** — um job periódico (`payouts.processScheduled`) busca repasses com `status = "scheduled"` e `scheduledDate <= NOW()`. Para cada um:
- Verifica `guide_payment_methods.status === "payment_enabled"`
- Decripta a chave via `getPixKeyForPayout()` (único ponto autorizado, com audit)
- Chama a API de transferência Pix do Mercado Pago
- Persiste `pixTransactionId`, `pixEndToEndId` e muda status para `"sent"`

**3. Confirmação** — ao receber o webhook de confirmação do Mercado Pago, o payout muda para `"completed"` e `pixReceiptUrl` é armazenado.

Falhas são retentadas até 3 vezes com backoff exponencial (1h → 4h → 24h). Após a 3ª falha, o payout vai para `"failed"` e um alerta é disparado para o admin.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Repasse automático elimina operação manual — guias recebem sem intervenção da equipe Trekko. |
| 2 | Snapshot da chave no agendamento garante que troca de chave Pix pelo guia não quebra repasses em andamento. |
| 3 | Retry com backoff recupera falhas transientes (timeout, indisponibilidade do MP) sem perda de repasse. |
| 4 | Rastreabilidade completa (pixTransactionId, pixEndToEndId) permite conciliação financeira e resolução de disputas com o Mercado Pago. |

---

## Acceptance Criteria

```gherkin
Feature: Execução do repasse via chave Pix

  Background:
    Given uma reserva com status "awaiting_expedition" existe
    And o guia da expedição tem guide_payment_methods.status = "payment_enabled"

  # ─── Agendamento do payout ────────────────────────────────────────

  Scenario: Payout agendado ao concluir período de contestação
    Given a expedição foi concluída e contestationEndsAt = agora
    When o sistema processa o fim do período de contestação
    Then um registro é criado em "payouts" com:
      | guideId        | ID do guia da expedição                         |
      | reservationId  | ID da reserva                                   |
      | status         | "scheduled"                                     |
      | grossAmount    | totalAmount da reserva                          |
      | platformFee    | 4% de grossAmount                               |
      | gatewayFee     | taxa Mercado Pago (consultada no momento)       |
      | netAmount      | grossAmount - platformFee - gatewayFee          |
      | pixKey         | chave Pix criptografada (snapshot de guide_payment_methods) |
      | pixKeyType     | tipo da chave (snapshot)                        |
      | scheduledDate  | contestationEndsAt + 2 dias úteis               |
      | retryCount     | 0                                               |
    And reservation.status = "payout_sent" NÃO é atualizado ainda

  Scenario: Snapshot da chave Pix capturado no momento do agendamento
    Given o guia altera sua chave Pix após o agendamento do payout
    When o job processa o payout agendado
    Then o payout usa a chave snapshottada no agendamento (não a nova chave)
    And a nova chave será usada somente em payouts agendados APÓS a troca

  Scenario: Payout não agendado se guide_payment_methods.status != "payment_enabled"
    Given guide_payment_methods.status = "payment_blocked"
    When o sistema tenta agendar o payout
    Then o payout é criado com status = "blocked" e failureReason = "guide_payments_not_enabled"
    And um alerta é gerado para o admin
    And reservation.status permanece inalterado

  # ─── Execução pelo job ────────────────────────────────────────────

  Scenario: Job processa payout agendado com sucesso
    Given existe um payout com status = "scheduled" e scheduledDate <= NOW()
    When o job "payouts.processScheduled" executa
    Then o payout é atualizado para status = "processing"
    And getPixKeyForPayout() é chamado com (guideId, payoutId) — evento de auditoria gerado
    And a API de transferência Pix do Mercado Pago é chamada com:
      | pixKey         | chave Pix descriptografada (plaintext) |
      | pixKeyType     | tipo da chave                          |
      | amount         | netAmount do payout (em centavos)      |
      | description    | "Repasse Trekko - Reserva #{reservationId}" |
    And pixTransactionId e pixEndToEndId são salvos no payout
    And payout.status = "sent"
    And payout.processedAt = NOW()
    And reservation.status = "payout_sent"
    And um evento "payout_executed" é registrado em payment_audit_log

  Scenario: Job não processa payout com scheduledDate no futuro
    Given existe um payout com scheduledDate = amanhã
    When o job executa
    Then esse payout NÃO é processado
    And permanece com status = "scheduled"

  Scenario: Job processa múltiplos payouts em paralelo com limite de concorrência
    Given existem 50 payouts com scheduledDate <= NOW()
    When o job executa
    Then processa no máximo 10 payouts simultâneos (concurrency limit)
    And os demais permanecem "scheduled" para a próxima execução do job

  # ─── Confirmação via webhook ──────────────────────────────────────

  Scenario: Webhook do Mercado Pago confirma transferência Pix
    Given um payout com status = "sent" e pixTransactionId = "MP-TXN-123"
    When o Mercado Pago envia webhook com type = "transfer" e status = "approved"
    Then payout.status = "completed"
    And payout.completedAt = NOW()
    And pixReceiptUrl é salvo no payout
    And reservation.status = "completed_contestation" é mantido (reserva já estava concluída)
    And um evento "payout_completed" é registrado em payment_audit_log

  Scenario: Webhook recebido para payout já completed (idempotência)
    Given payout.status = "completed"
    When o mesmo webhook é recebido novamente
    Then nenhuma operação de escrita é executada
    And resposta HTTP 200 é retornada (não falha)

  # ─── Falha e retry ───────────────────────────────────────────────

  Scenario: Falha na transferência Pix — primeira tentativa
    Given o job tenta processar um payout
    When a API do Mercado Pago retorna erro (timeout, chave inválida, etc.)
    Then payout.status = "failed"
    And payout.retryCount = 1
    And payout.failureReason = mensagem de erro da API
    And payout.scheduledDate = NOW() + 1 hora (reagendado)
    And payout.status volta para "scheduled" para retry
    And um evento "payout_failed" é registrado com failureReason

  Scenario: Retry com backoff exponencial
    Given payout.retryCount = 1 e a segunda tentativa falha
    Then payout.scheduledDate = NOW() + 4 horas
    And payout.retryCount = 2

    Given payout.retryCount = 2 e a terceira tentativa falha
    Then payout.scheduledDate = NOW() + 24 horas
    And payout.retryCount = 3

  Scenario: Payout permanece failed após 3 tentativas fracassadas
    Given payout.retryCount = 3 e a tentativa falha novamente
    Then payout.status = "failed" (permanente — não reagendado)
    And payout.retryCount = 3 (não incrementado além do limite)
    And um alerta é disparado para admin: "Payout #{id} falhou após 3 tentativas"
    And reservation.status permanece "awaiting_expedition" ou estado anterior (não avança)
    And o guia vê no dashboard: "Houve um problema com seu repasse. Entre em contato com o suporte."

  Scenario: Falha por chave Pix inválida no Mercado Pago
    Given a chave Pix snapshottada no payout foi cadastrada incorretamente
    When o Mercado Pago rejeita com erro "invalid_pix_key"
    Then payout.failureReason = "invalid_pix_key"
    And payout.retryCount é incrementado mas o retry é inútil
    And após 3 tentativas, admin é alertado com contexto "invalid_pix_key"
    And o sistema sugere ao admin invalidar a chave via admin.invalidatePixKey()

  # ─── Cálculo de valores ───────────────────────────────────────────

  Scenario: Cálculo correto de taxas no agendamento
    Given grossAmount = R$ 500,00
    And platformFee = 4% = R$ 20,00
    And gatewayFee (Mercado Pago) = R$ 3,50
    Then netAmount = R$ 476,50
    And o guia recebe exatamente R$ 476,50 via Pix

  Scenario: Valor transferido ao Mercado Pago é netAmount em centavos
    Given netAmount = R$ 476,50
    When a API de transferência é chamada
    Then o campo amount = 47650 (centavos, sem arredondamento)

  # ─── Visibilidade para o guia ────────────────────────────────────

  Scenario: Guia vê status do repasse no painel financeiro
    When o guia acessa GuideFinancialPanel → aba "Repasses"
    Then cada payout exibe:
      | status           | label amigável                      |
      | scheduled        | Repasse Agendado                    |
      | processing       | Processando                         |
      | sent             | Enviado                             |
      | completed        | Concluído                           |
      | failed           | Falhou — Entre em contato           |
      | blocked          | Bloqueado — Conta sem Pix habilitado|
    And o guia vê netAmount (valor recebido), NÃO grossAmount
    And pixKey, pixKeyType e pixTransactionId NÃO são exibidos na UI do guia
```

---

## Technical Notes

### 1 — Job `payouts.processScheduled`

```typescript
// server/jobs/processPayouts.ts
// Executar como cron: a cada 15 minutos

export async function processScheduledPayouts() {
  const due = await db.getScheduledPayouts(); // WHERE status='scheduled' AND scheduledDate <= NOW()

  // Processar em batches com concurrency limit
  await pLimit(10)(due.map(payout => () => processSinglePayout(payout)));
}

async function processSinglePayout(payout: Payout) {
  // 1. Idempotência: garantir que não há dois workers processando o mesmo payout
  const locked = await db.tryLockPayout(payout.id); // UPDATE ... WHERE status='scheduled' AND id=X
  if (!locked) return; // outro worker pegou esse payout

  await db.updatePayout(payout.id, { status: "processing" });

  try {
    // 2. Recuperar e descriptografar chave (com audit obrigatório)
    const pixKey = await getPixKeyForPayout(payout.guideId, payout.id, db);

    // 3. Chamar Mercado Pago
    const transfer = await mercadoPago.transfers.create({
      amount: toIntCents(payout.netAmount),
      receiver: {
        type: payout.pixKeyType,
        key: pixKey,
      },
      description: `Repasse Trekko - Reserva #${payout.reservationId}`,
      external_reference: `payout_${payout.id}`,
    });

    // 4. Persistir resultado
    await db.transaction(async (tx) => {
      await tx.updatePayout(payout.id, {
        status: "sent",
        pixTransactionId: transfer.id,
        pixEndToEndId: transfer.point_of_interaction?.transaction_data?.end_to_end_id,
        processedAt: new Date(),
      });
      await tx.updateReservation(payout.reservationId, { status: "payout_sent" });
      await writePaymentAuditEvent(tx, {
        action: "payout_executed",
        entityId: payout.id,
        actorType: "system",
        actorId: 0,
        previousValue: { status: "processing" },
        newValue: {
          status: "sent",
          pixTransactionId: transfer.id,
          netAmount: payout.netAmount,
        },
        ipAddress: "internal",
        userAgent: "payout-job",
      });
    });
  } catch (err) {
    await handlePayoutFailure(payout, err);
  }
}
```

### 2 — Snapshot da chave no agendamento

```typescript
// server/lib/schedulePayouts.ts

export async function schedulePayoutForReservation(reservationId: number) {
  const reservation = await db.getReservationById(reservationId);
  const method = await db.getDefaultPaymentMethod(reservation.guideId);

  if (!method || method.status !== "payment_enabled") {
    await db.createPayout({
      guideId: reservation.guideId,
      reservationId,
      status: "blocked",
      failureReason: "guide_payments_not_enabled",
      grossAmount: reservation.totalAmount,
      platformFee: "0",
      gatewayFee: "0",
      netAmount: "0",
    });
    notifyAdmin(`Payout bloqueado — guia sem Pix habilitado. Reserva #${reservationId}`);
    return;
  }

  const { grossAmount, platformFee, gatewayFee, netAmount } = calculatePayoutFees(
    reservation.totalAmount
  );

  const scheduledDate = addBusinessDays(reservation.expeditionCompletedAt!, 2);

  await db.createPayout({
    guideId: reservation.guideId,
    reservationId,
    status: "scheduled",
    scheduledDate,
    grossAmount,
    platformFee,
    gatewayFee,
    netAmount,
    // Snapshot da chave — método pode ser trocado pelo guia depois
    pixKey: method.pixKey,        // ciphertext — já criptografado
    pixKeyType: method.pixKeyType,
    currency: "BRL",
    retryCount: 0,
  });
}
```

### 3 — Cálculo de taxas

```typescript
// server/lib/feeCalculator.ts

const PLATFORM_FEE_PERCENT = 0.04; // 4%

export function calculatePayoutFees(grossAmount: string) {
  const gross = new Decimal(grossAmount);
  const platformFee = gross.mul(PLATFORM_FEE_PERCENT).toDecimalPlaces(2);
  const gatewayFee = new Decimal(await mercadoPago.getTransferFee(gross.toNumber()));
  const netAmount = gross.minus(platformFee).minus(gatewayFee);

  return {
    grossAmount: gross.toString(),
    platformFee: platformFee.toString(),
    gatewayFee: gatewayFee.toString(),
    netAmount: netAmount.toString(),
  };
}

// Converter para centavos inteiros sem arredondamento
export function toIntCents(amount: string): number {
  return new Decimal(amount).mul(100).toInteger().toNumber();
}
```

Usar a biblioteca `decimal.js` (ou equivalente) para todas as operações financeiras — nunca `Number` ou `Math.round` para evitar erros de ponto flutuante.

### 4 — Tratamento de falha e retry

```typescript
// server/jobs/processPayouts.ts

const RETRY_BACKOFF_HOURS = [1, 4, 24]; // tentativa 1, 2, 3
const MAX_RETRIES = 3;

async function handlePayoutFailure(payout: Payout, error: unknown) {
  const failureReason = extractMpErrorCode(error);
  const newRetryCount = (payout.retryCount ?? 0) + 1;

  if (newRetryCount > MAX_RETRIES) {
    await db.transaction(async (tx) => {
      await tx.updatePayout(payout.id, {
        status: "failed",
        failureReason,
        retryCount: MAX_RETRIES,
      });
      await writePaymentAuditEvent(tx, {
        action: "payout_failed",
        entityId: payout.id,
        actorType: "system",
        actorId: 0,
        previousValue: { status: "processing", retryCount: payout.retryCount },
        newValue: { status: "failed", failureReason, finalFailure: true },
        ipAddress: "internal",
        userAgent: "payout-job",
      });
    });
    notifyAdmin(`Payout #${payout.id} falhou após ${MAX_RETRIES} tentativas. Motivo: ${failureReason}`);
    return;
  }

  const backoffHours = RETRY_BACKOFF_HOURS[newRetryCount - 1];
  const nextScheduledDate = addHours(new Date(), backoffHours);

  await db.updatePayout(payout.id, {
    status: "scheduled",          // volta para scheduled para retry
    retryCount: newRetryCount,
    scheduledDate: nextScheduledDate,
    failureReason,
  });
}
```

### 5 — Idempotência via lock otimista

Evitar duplo processamento em ambientes com múltiplos workers:

```sql
-- tryLockPayout: UPDATE atômico — só um worker ganha
UPDATE payouts
SET status = 'processing'
WHERE id = :payoutId AND status = 'scheduled'
-- affected_rows = 1 → worker obteve o lock
-- affected_rows = 0 → outro worker pegou primeiro
```

### 6 — Webhook de confirmação do Mercado Pago

```typescript
// server/webhooks/mercadopago.ts — adicionar handler de "transfer"

case "transfer": {
  const transfer = await mercadoPago.transfers.get(data.id);
  const payout = await db.getPayoutByMpTransactionId(transfer.id);
  if (!payout || payout.status === "completed") return; // idempotência

  if (transfer.status === "approved") {
    await db.transaction(async (tx) => {
      await tx.updatePayout(payout.id, {
        status: "completed",
        completedAt: new Date(),
        pixReceiptUrl: transfer.point_of_interaction?.transaction_data?.ticket_url,
      });
      await writePaymentAuditEvent(tx, {
        action: "payout_completed",
        entityId: payout.id,
        actorType: "system",
        actorId: 0,
        previousValue: { status: "sent" },
        newValue: { status: "completed", pixReceiptUrl: transfer.point_of_interaction?.transaction_data?.ticket_url },
        ipAddress: "internal",
        userAgent: "mp-webhook",
      });
    });
  }
  break;
}
```

### 7 — `addBusinessDays` (dias úteis brasileiros)

```typescript
// server/lib/dateUtils.ts

// Considerar feriados nacionais — versão mínima:
export function addBusinessDays(date: Date, days: number): Date {
  let count = 0;
  let current = new Date(date);
  while (count < days) {
    current.setDate(current.getDate() + 1);
    const day = current.getDay();
    if (day !== 0 && day !== 6) count++; // pula sábado e domingo
    // TODO: integrar calendário de feriados nacionais (fase 2)
  }
  return current;
}
```

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|---|---|---|
| Novo job | `processPayouts.ts` — cron 15min, concurrency=10, lock otimista | `server/jobs/processPayouts.ts` |
| Agendador | `schedulePayoutForReservation()` — chamado ao fechar contestação | `server/lib/schedulePayouts.ts` |
| Cálculo de taxas | `calculatePayoutFees()` e `toIntCents()` com `decimal.js` | `server/lib/feeCalculator.ts` |
| Retry handler | `handlePayoutFailure()` com backoff [1h, 4h, 24h], max 3 tentativas | `server/jobs/processPayouts.ts` |
| Webhook MP | Adicionar handler de evento `"transfer"` com idempotência | `server/webhooks/mercadopago.ts` |
| `db.getScheduledPayouts` | WHERE status='scheduled' AND scheduledDate <= NOW() | `server/db.ts` |
| `db.tryLockPayout` | UPDATE atômico para lock otimista | `server/db.ts` |
| `db.getPayoutByMpTransactionId` | Lookup por pixTransactionId para webhook | `server/db.ts` |
| `payment_audit_log` | Novos actions: `payout_executed`, `payout_failed`, `payout_completed` | `drizzle/schema.ts` |
| Schema / Migrations | Nenhuma nova coluna — `payouts` já possui todos os campos necessários | — |

### Ciclo de vida de status do payout (referência)

| Status | Significado | Próximo(s) |
|---|---|---|
| `scheduled` | Aguardando scheduledDate | `processing`, `blocked` |
| `processing` | Job em execução | `sent`, `failed` |
| `sent` | Transferência submetida ao MP | `completed`, `failed` |
| `completed` | Confirmado pelo webhook | — (terminal) |
| `failed` | Após 3 tentativas ou falha permanente | — (terminal) |
| `blocked` | Guide sem `payment_enabled` no agendamento | — (requer intervenção admin) |

### Campos de `payouts` preenchidos por etapa

| Campo | Agendamento | Execução | Confirmação webhook |
|---|---|---|---|
| `pixKey` (snapshot) | ✅ | — | — |
| `pixKeyType` (snapshot) | ✅ | — | — |
| `grossAmount`, `platformFee`, `gatewayFee`, `netAmount` | ✅ | — | — |
| `scheduledDate` | ✅ | — | — |
| `pixTransactionId` | — | ✅ | — |
| `pixEndToEndId` | — | ✅ | — |
| `processedAt` | — | ✅ | — |
| `pixReceiptUrl` | — | — | ✅ |
| `completedAt` | — | — | ✅ |
| `failureReason`, `retryCount` | — | ✅ (se falha) | — |
