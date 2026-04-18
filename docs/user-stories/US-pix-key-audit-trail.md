# US — Rastreamento Completo de Alterações em Chaves Pix

## Title
**Como plataforma**, quero registrar e disponibilizar o histórico completo de todas as alterações em chaves Pix dos guias — com valor anterior, novo valor, timestamp e responsável — **para que** disputas financeiras, auditorias de compliance e investigações de suporte tenham rastreabilidade total e imutável.

---

## Description

Toda ação que cria, modifica, arquiva ou afeta o estado de um método de pagamento Pix gera obrigatoriamente um evento em `payment_audit_log`. O sistema cobre **seis tipos de evento** ao longo do ciclo de vida de uma chave Pix.

Os registros de auditoria são **imutáveis**: nenhum endpoint permite UPDATE ou DELETE sobre eles. Dados sensíveis são armazenados exclusivamente como `maskedPixKey` — nunca plaintext ou ciphertext.

Dois contextos de consulta são expostos:
- **Guia**: visualiza seu próprio histórico de chaves (campos limitados, sem IPs de atores externos).
- **Admin**: visualiza histórico de qualquer guia com campos completos, incluindo IP, userAgent e metadados de ator.

Retenção: registros são mantidos por **5 anos** (BACEN / Lei 9.613/98). Após esse período, `actorId` e `ipAddress` são anonimizados (nullificados); o evento em si é preservado.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Rastreabilidade completa para disputas: prova quem alterou qual chave e quando, com IP. |
| 2 | Conformidade com BACEN (Res. BCB nº 1) e Lei 9.613/98 (prevenção a lavagem de dinheiro) — registros financeiros por 5 anos. |
| 3 | Suporte consegue responder "por que o repasse falhou" consultando o audit log sem precisar de engenheiro. |
| 4 | Admin detecta padrões suspeitos (ex: guia alterando chave logo antes de um repasse) via queries no log. |

---

## Acceptance Criteria

```gherkin
Feature: Rastreamento completo de alterações em chaves Pix

  # ─── Cobertura de eventos ─────────────────────────────────────────

  Scenario Outline: Evento registrado para cada ação no ciclo de vida
    When a ação "<ação>" ocorre sobre um método de pagamento Pix
    Then exatamente 1 registro é criado em payment_audit_log com action = "<action_code>"
    And o registro contém previousValue e newValue em JSON conforme especificação
    And o registro NÃO pode ser modificado ou deletado por nenhum endpoint

    Exemplos:
      | ação                                    | action_code                    |
      | Guia registra chave Pix pela 1ª vez     | payment_method_created         |
      | Guia atualiza chave Pix                 | payment_method_archived        |
      | Guia atualiza chave Pix                 | payment_method_created         |
      | Guia define novo método padrão          | payment_method_default_changed |
      | Admin suspende método de pagamento      | payment_method_suspended       |
      | Admin reativa método suspenso           | payment_method_reactivated     |
      | Sistema arquiva método por inatividade  | payment_method_archived        |

  # ─── Estrutura dos eventos ────────────────────────────────────────

  Scenario: Estrutura do evento payment_method_created
    Given o guia registra uma chave Pix do tipo "email"
    Then o evento em payment_audit_log contém:
      | entityType    | "guide_payment_method"                            |
      | entityId      | ID do novo método                                 |
      | action        | "payment_method_created"                          |
      | previousValue | NULL                                              |
      | newValue      | { "pixKeyType": "email",                          |
      |               |   "maskedPixKey": "joao@***.com.br",              |
      |               |   "pixKeyHolderName": "João Silva",               |
      |               |   "status": "active",                             |
      |               |   "isDefault": true }                             |
      | actorId       | ID do guia                                        |
      | actorType     | "guide"                                           |
      | ipAddress     | IP da requisição                                  |
      | userAgent     | User-Agent da requisição                          |
      | createdAt     | Timestamp UTC preciso ao segundo                  |

  Scenario: Estrutura do evento payment_method_archived (via atualização)
    Given o guia substitui sua chave Pix atual
    Then o evento de arquivamento contém:
      | previousValue | { "pixKeyType": "cpf",                            |
      |               |   "maskedPixKey": "272.***.***-88",               |
      |               |   "status": "active",                             |
      |               |   "isDefault": true }                             |
      | newValue      | { "archivedAt": "<timestamp ISO 8601>",            |
      |               |   "archivedBy": "guide",                          |
      |               |   "reason": "replaced_by_update" }                |

  Scenario: Estrutura do evento payment_method_default_changed
    Given o guia muda o método padrão de "pix" para "bank_transfer"
    Then o evento contém:
      | previousValue | { "defaultMethodId": <id_antigo>,                 |
      |               |   "pixKeyType": "cpf",                            |
      |               |   "maskedPixKey": "272.***.***-88" }               |
      | newValue      | { "defaultMethodId": <id_novo>,                   |
      |               |   "type": "bank_transfer" }                       |

  Scenario: Estrutura do evento payment_method_suspended (admin)
    Given um admin suspende o método Pix de um guia
    Then o evento contém:
      | actorId       | ID do admin                                       |
      | actorType     | "admin"                                           |
      | newValue      | { "status": "suspended",                          |
      |               |   "suspendedBy": <adminId>,                       |
      |               |   "reason": "<motivo informado pelo admin>" }     |

  # ─── Imutabilidade ───────────────────────────────────────────────

  Scenario: Nenhum endpoint permite modificar um registro de auditoria
    When qualquer ator (guia, admin, sistema) tenta fazer UPDATE em payment_audit_log
    Then a operação é bloqueada (sem procedure UPDATE exposta)
    And o banco não possui trigger de UPDATE/DELETE na tabela

  Scenario: Registro criado dentro de transação atômica com a operação principal
    Given o guia atualiza sua chave Pix
    When a transação de banco falha após criar o método mas antes do audit log
    Then nem o método novo nem o evento de auditoria persistem (rollback total)
    And nenhum estado parcial é salvo

  # ─── Consulta pelo guia ───────────────────────────────────────────

  Scenario: Guia consulta seu histórico de chaves Pix
    When o guia chama "guides.getMyPixAuditHistory"
    Then recebe uma lista paginada de eventos, do mais recente ao mais antigo
    And cada item contém:
      | action           | código do evento                              |
      | maskedPixKey     | valor mascarado (anterior e novo, se aplicável) |
      | pixKeyType       | tipo da chave                                 |
      | actorType        | "guide" | "admin" | "system"                 |
      | createdAt        | timestamp                                     |
    And ipAddress e userAgent NÃO são retornados ao guia
    And actorId de admins NÃO é retornado ao guia (privacidade do admin)

  Scenario: Guia não pode consultar histórico de outro guia
    When o guia autenticado chama "guides.getMyPixAuditHistory" com guideId de outro guia
    Then a query ignora o parâmetro e retorna apenas os eventos do próprio guia

  # ─── Consulta pelo admin ──────────────────────────────────────────

  Scenario: Admin consulta histórico completo de um guia
    When um admin chama "admin.getPixAuditHistory" com guideId
    Then recebe a lista completa de eventos com todos os campos:
      | action, previousValue, newValue, actorId, actorType |
      | ipAddress, userAgent, createdAt                      |
    And eventos de diferentes guias não se misturam

  Scenario: Admin filtra eventos por intervalo de datas
    When admin chama "admin.getPixAuditHistory" com { guideId, from: "2025-01-01", to: "2025-03-31" }
    Then retorna apenas eventos cujo createdAt está no intervalo inclusivo

  Scenario: Admin filtra por action específica
    When admin chama com { guideId, action: "payment_method_archived" }
    Then retorna apenas eventos de arquivamento desse guia

  # ─── Retenção e anonimização ─────────────────────────────────────

  Scenario: Registros com mais de 5 anos são anonimizados, não deletados
    Given um registro em payment_audit_log com createdAt há mais de 5 anos
    When o job de retenção é executado
    Then o registro recebe actorId = NULL e ipAddress = NULL e userAgent = NULL
    And os campos action, previousValue, newValue, entityId e createdAt permanecem intactos
    And o registro NÃO é deletado

  Scenario: Job de retenção é idempotente
    Given o job já anonimizou um registro
    When é executado novamente sobre o mesmo registro
    Then nenhuma nova operação de escrita é feita (WHERE actorId IS NOT NULL)
```

---

## Technical Notes

### 1 — Catálogo completo de eventos (`action` enum)

Adicionar ao schema os novos valores de `action` para `payment_audit_log`:

```typescript
// drizzle/schema.ts — expandir enum de action em payment_audit_log

type AuditAction =
  // Existentes
  | "pix_key_saved"              // legado — guides.savePixData anterior à refatoração
  | "enrollment_blocked"         // reserva bloqueada por paymentsEnabled=false

  // Novos — ciclo de vida de guide_payment_methods
  | "payment_method_created"       // primeiro cadastro ou criação via update
  | "payment_method_archived"      // arquivamento por update, admin ou sistema
  | "payment_method_default_changed" // troca de método padrão
  | "payment_method_suspended"     // admin suspende
  | "payment_method_reactivated"   // admin reativa método suspenso
```

### 2 — Contrato de `previousValue` / `newValue` por evento

Todos os campos JSON armazenados como `text` (padrão DB-SEC-04 do projeto — payload sanitizado, máx 4096 chars):

```typescript
// shared/lib/auditPayloads.ts

type PixMethodSnapshot = {
  pixKeyType: PixKeyType | null;
  maskedPixKey: string | null;   // via maskPixKey() — NUNCA valor bruto
  pixKeyHolderName: string | null;
  status: "active" | "inactive" | "pending_verification" | "suspended";
  isDefault: boolean;
};

const eventPayloads: Record<AuditAction, { previous: string; next: string }> = {
  payment_method_created:          { previous: "NULL",             next: "PixMethodSnapshot" },
  payment_method_archived:         { previous: "PixMethodSnapshot", next: "{ archivedAt, archivedBy, reason }" },
  payment_method_default_changed:  { previous: "{ defaultMethodId, type, maskedPixKey }", next: "{ defaultMethodId, type }" },
  payment_method_suspended:        { previous: "PixMethodSnapshot", next: "{ status, suspendedBy, reason }" },
  payment_method_reactivated:      { previous: "{ status: 'suspended' }", next: "PixMethodSnapshot" },
};
```

### 3 — Função centralizada `writePaymentAuditEvent`

Evitar chamadas diretas e inconsistentes a `createAuditLog` — encapsular em uma função tipada:

```typescript
// server/lib/auditWriter.ts

export async function writePaymentAuditEvent(
  tx: DbTransaction,
  params: {
    action: AuditAction;
    entityId: number;
    actorId: number;
    actorType: "guide" | "admin" | "system";
    previousValue: object | null;
    newValue: object;
    ipAddress: string;
    userAgent: string;
  }
) {
  const payload = JSON.stringify(params.newValue);
  if (payload.length > 4096) {
    throw new Error(`audit_payload_too_large: ${params.action}`); // fail-fast, não silencia
  }

  await tx.createAuditLog({
    entityType: "guide_payment_method",
    entityId: String(params.entityId),
    action: params.action,
    actorId: String(params.actorId),
    actorType: params.actorType,
    previousValue: params.previousValue ? JSON.stringify(params.previousValue) : null,
    newValue: payload,
    ipAddress: params.ipAddress,
    userAgent: params.userAgent ?? "unknown",
  });
}
```

Toda mutation que afeta `guide_payment_methods` deve chamar `writePaymentAuditEvent` **dentro da mesma transação**. Se o audit falhar, a operação principal faz rollback.

### 4 — Novos endpoints tRPC

```typescript
// server/routers.ts

// Guia: histórico próprio paginado (campos limitados)
guides.getMyPixAuditHistory = guideProcedure
  .input(z.object({ page: z.number().default(1), limit: z.number().max(50).default(20) }))
  .query(async ({ ctx, input }) => {
    const events = await db.getPixAuditHistory({
      guideId: ctx.user.id,
      page: input.page,
      limit: input.limit,
    });
    return events.map(e => ({
      action:      e.action,
      newValue:    JSON.parse(e.newValue),
      previousValue: e.previousValue ? JSON.parse(e.previousValue) : null,
      actorType:   e.actorType,
      // actorId e ipAddress OMITIDOS para guia
      createdAt:   e.createdAt,
    }));
  });

// Admin: histórico completo com filtros
admin.getPixAuditHistory = adminProcedure
  .input(z.object({
    guideId: z.number(),
    action:  z.string().optional(),
    from:    z.string().datetime().optional(),
    to:      z.string().datetime().optional(),
    page:    z.number().default(1),
    limit:   z.number().max(100).default(50),
  }))
  .query(async ({ input }) => {
    return db.getPixAuditHistory(input); // retorna todos os campos
  });
```

### 5 — Query `db.getPixAuditHistory`

```typescript
// server/db.ts

async function getPixAuditHistory(params: {
  guideId: number;
  action?: string;
  from?: string;
  to?: string;
  page: number;
  limit: number;
}) {
  const offset = (params.page - 1) * params.limit;

  return db
    .select()
    .from(paymentAuditLog)
    .where(and(
      eq(paymentAuditLog.actorId, String(params.guideId)),       // eventos do guia como ator
      params.action ? eq(paymentAuditLog.action, params.action) : undefined,
      params.from   ? gte(paymentAuditLog.createdAt, new Date(params.from)) : undefined,
      params.to     ? lte(paymentAuditLog.createdAt, new Date(params.to)) : undefined,
      inArray(paymentAuditLog.action, PIX_AUDIT_ACTIONS),         // somente ações Pix
    ))
    .orderBy(desc(paymentAuditLog.createdAt))
    .limit(params.limit)
    .offset(offset);
}

const PIX_AUDIT_ACTIONS: AuditAction[] = [
  "payment_method_created",
  "payment_method_archived",
  "payment_method_default_changed",
  "payment_method_suspended",
  "payment_method_reactivated",
  "pix_key_saved",
];
```

### 6 — Job de anonimização (retenção 5 anos)

```typescript
// server/jobs/auditRetention.ts
// Executar como cron mensal

export async function anonymizeExpiredAuditRecords() {
  const cutoff = new Date();
  cutoff.setFullYear(cutoff.getFullYear() - 5);

  await db
    .update(paymentAuditLog)
    .set({ actorId: null, ipAddress: null, userAgent: null })
    .where(and(
      lte(paymentAuditLog.createdAt, cutoff),
      isNotNull(paymentAuditLog.actorId),       // idempotente: só processa não-anonimizados
      inArray(paymentAuditLog.entityType, ["guide_payment_method"]),
    ));
}
```

### 7 — Índices necessários em `payment_audit_log`

Os índices de `createdAt` e `entityType+entityId` já existem (DB-SEC-04). Adicionar:

```sql
-- Para queries do admin por guia + action + data
CREATE INDEX idx_audit_actor_action_date
  ON payment_audit_log (actor_id, action, created_at DESC);

-- Para job de retenção (WHERE created_at <= cutoff AND actor_id IS NOT NULL)
-- O índice existente em created_at já cobre — nenhum índice adicional necessário
```

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|--------|---------|---------|
| `payment_audit_log` | Expandir enum `action` com 5 novos valores | `drizzle/schema.ts` |
| Nova função tipada | `writePaymentAuditEvent()` — ponto único de escrita, fail-fast em payload > 4096 chars | `server/lib/auditWriter.ts` |
| Payloads tipados | `shared/lib/auditPayloads.ts` — contrato de `previousValue`/`newValue` por evento | `shared/lib/auditPayloads.ts` |
| `server/db.ts` | `getPixAuditHistory(params)` com filtros e paginação | `server/db.ts` |
| tRPC — guia | `guides.getMyPixAuditHistory` — paginado, sem IP/actorId | `server/routers.ts` |
| tRPC — admin | `admin.getPixAuditHistory` — campos completos + filtros | `server/routers.ts` |
| Job de retenção | `auditRetention.ts` — anonimiza actorId/IP após 5 anos, idempotente | `server/jobs/auditRetention.ts` |
| Novo índice | `idx_audit_actor_action_date` em `payment_audit_log` | `drizzle/` migration |
| Schema / Migrations | 1 migration: enum expansion + novo índice | `drizzle/` |

### Campos retornados por contexto

| Campo | Guia (próprio) | Admin |
|---|---|---|
| `action` | ✅ | ✅ |
| `previousValue` | ✅ (mascarado) | ✅ (mascarado) |
| `newValue` | ✅ (mascarado) | ✅ (mascarado) |
| `actorType` | ✅ | ✅ |
| `actorId` | ❌ (omitido) | ✅ |
| `ipAddress` | ❌ | ✅ |
| `userAgent` | ❌ | ✅ |
| `createdAt` | ✅ | ✅ |

### Normas aplicadas
- **BACEN Res. BCB nº 1** — rastreabilidade de chaves Pix
- **Lei 9.613/98 (COAF)** — retenção de registros financeiros por 5 anos
- **LGPD Art. 16** — anonimização de dados pessoais após prazo de retenção (actorId, IP)
