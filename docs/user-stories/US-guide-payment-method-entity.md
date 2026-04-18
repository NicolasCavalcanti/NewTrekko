# US — Estrutura de Dados Financeiros Separada do Perfil do Guia

## Title
**Como engenheiro de plataforma**, quero mover os dados financeiros do guia (chave Pix, dados bancários) para uma entidade `guide_payment_methods` separada da tabela `guide_verification`, **para que** o modelo suporte múltiplos métodos de pagamento futuros sem acumular colunas na tabela de verificação de identidade.

---

## Description

Atualmente, `guide_verification` acumula três responsabilidades distintas:

| Responsabilidade | Colunas atuais |
|---|---|
| Verificação de identidade | `documentType`, `documentNumber`, `status`, `reviewedBy`, `rejectionReason` |
| Dados financeiros Pix | `pixKey`, `pixKeyType`, `pixKeyHolderName`, `pixKeyVerified` |
| Dados bancários | `bankCode`, `bankName`, `agencyNumber`, `accountNumber`, `accountType` |

Essa mistura impede a evolução do modelo: adicionar TED/boleto/Stripe exigiria novas colunas nullable em `guide_verification`, o que degrada legibilidade, aumenta superfície de dados sensíveis e complica auditoria.

A solução é criar uma entidade `guide_payment_methods` com:
- Uma linha por método de pagamento por guia
- Coluna `type` (enum extensível: `"pix"` | `"bank_transfer"` | `"stripe"` | ...)
- Coluna `isDefault` para selecionar qual método o sistema usa nos repasses
- Campos sensíveis criptografados com AES-256-GCM (padrão DB-SEC-01 já em produção)
- Soft delete via `archivedAt` (padrão DB-ARCH-01)

`guide_verification` passa a ser exclusivamente uma tabela de verificação de identidade/compliance.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Adicionar um novo método de pagamento (ex: TED, Stripe) requer apenas novos campos JSON/colunas opcionais em `guide_payment_methods`, sem tocar em `guide_verification`. |
| 2 | Guias podem cadastrar múltiplos métodos e escolher o padrão, aumentando flexibilidade operacional. |
| 3 | Auditoria financeira fica isolada da auditoria de identidade — superfície menor por contexto. |
| 4 | Payout engine consulta uma única tabela com interface uniforme, independente do tipo de método. |

---

## Acceptance Criteria

```gherkin
Feature: Entidade separada para métodos de pagamento do guia

  # ─── Estrutura de dados ──────────────────────────────────────────

  Scenario: guide_verification não contém mais dados financeiros
    Given a migration foi aplicada
    Then a tabela "guide_verification" não possui as colunas:
      | pixKey            |
      | pixKeyType        |
      | pixKeyHolderName  |
      | pixKeyVerified    |
      | bankCode          |
      | bankName          |
      | agencyNumber      |
      | accountNumber     |
      | accountType       |
      | accountHolderName |
      | accountHolderDocument |

  Scenario: guide_payment_methods armazena método Pix do guia
    Given o guia salva uma chave Pix válida
    Then um registro é criado em "guide_payment_methods" com:
      | guideId           | ID do guia                          |
      | type              | "pix"                               |
      | pixKeyType        | tipo selecionado (ex: "cpf")        |
      | pixKey            | valor criptografado (AES-256-GCM)   |
      | pixKeyHolderName  | nome do titular                     |
      | status            | "active"                            |
      | isDefault         | true (primeiro método = padrão)     |
    And nenhum dado financeiro é gravado em "guide_verification"

  Scenario: Guia cadastra segundo método de pagamento
    Given o guia já possui um método "pix" com isDefault = true
    When cadastra um novo método "bank_transfer"
    Then um segundo registro é criado em "guide_payment_methods"
    And isDefault permanece true apenas no método Pix (anterior)
    And o guia pode promover o novo método como padrão

  Scenario: Guia define novo método padrão
    Given o guia possui dois métodos: "pix" (isDefault=true) e "bank_transfer" (isDefault=false)
    When chama "guides.setDefaultPaymentMethod" com id do método bank_transfer
    Then bank_transfer.isDefault = true
    And pix.isDefault = false
    And apenas um método pode ser isDefault = true por guia (constraint DB)

  Scenario: Método arquivado não é usado em repasses
    Given o guia arquiva o método Pix ativo
    When o sistema processa um payout para esse guia
    Then o payout usa o método com isDefault = true e archivedAt IS NULL
    And se nenhum método ativo existir, o payout.status = "blocked"

  # ─── Migração de dados existentes ────────────────────────────────

  Scenario: Dados Pix existentes são migrados automaticamente
    Given existem registros em "guide_verification" com pixKey preenchido
    When a migration de dados é executada
    Then para cada registro com pixKey não-nulo:
      | Um novo registro é criado em guide_payment_methods |
      | type = "pix"                                       |
      | pixKey = valor original (mantém criptografia)      |
      | isDefault = true                                   |
      | status = "active" se pixKeyVerified = 1            |
      | status = "pending" se pixKeyVerified = 0           |
    And as colunas financeiras em guide_verification são removidas

  Scenario: Guia sem pixKey em guide_verification não gera registro migrado
    Given um guia tem guide_verification sem pixKey (NULL)
    When a migration é executada
    Then nenhum registro é criado em guide_payment_methods para esse guia

  # ─── paymentsEnabled recalculado ─────────────────────────────────

  Scenario: paymentsEnabled usa novo modelo
    Given o guia não possui nenhum registro ativo em guide_payment_methods
    Then isGuidePaymentsEnabled() retorna false

  Scenario: paymentsEnabled = true quando método padrão ativo existe
    Given o guia possui um registro em guide_payment_methods com:
      | status     | "active"  |
      | isDefault  | true      |
      | archivedAt | NULL      |
    And guide_verification.status IN ("pending", "approved")
    Then isGuidePaymentsEnabled() retorna true

  # ─── API ─────────────────────────────────────────────────────────

  Scenario: guides.savePixData salva em guide_payment_methods
    When o guia chama a mutation "guides.savePaymentMethod" com type "pix"
    Then o registro é criado/atualizado em guide_payment_methods
    And guide_verification NÃO é modificado

  Scenario: guides.getMyPaymentMethods retorna lista de métodos (sem dados sensíveis)
    When o guia chama a query "guides.getMyPaymentMethods"
    Then recebe uma lista com:
      | id, type, status, isDefault, pixKeyType, pixKeyHolderName, createdAt |
    And pixKey (valor da chave) NÃO é retornado na resposta
    And documentNumber NÃO é retornado na resposta

  Scenario: payouts.processScheduled usa método padrão da nova tabela
    When o job de payout consulta o método de pagamento do guia
    Then consulta "guide_payment_methods" WHERE guideId = X AND isDefault = true AND archivedAt IS NULL
    And usa pixKey descriptografado desse registro para iniciar a transferência
```

---

## Technical Notes

### 1 — Schema da nova tabela `guide_payment_methods`

```typescript
// drizzle/schema.ts

export const guidePaymentMethods = mysqlTable("guide_payment_methods", {
  id:               serial("id").primaryKey(),
  guideId:          int("guide_id").notNull()
                      .references(() => users.id, { onDelete: "cascade" }),

  // Tipo de método — extensível via enum
  type:             mysqlEnum("type", ["pix", "bank_transfer", "stripe"])
                      .notNull(),

  // Controle
  status:           mysqlEnum("status", ["active", "inactive", "pending_verification"])
                      .notNull().default("active"),
  isDefault:        int("is_default").notNull().default(0),

  // ── Pix (DB-SEC-01: criptografado AES-256-GCM) ──────────────────
  pixKeyType:       mysqlEnum("pix_key_type", ["cpf","cnpj","email","phone","random"]),
  pixKey:           varchar("pix_key", { length: 512 }),        // encrypted
  pixKeyHolderName: varchar("pix_key_holder_name", { length: 256 }),
  pixKeyDocument:   varchar("pix_key_document", { length: 512 }), // encrypted

  // ── Transferência bancária (futuro) ─────────────────────────────
  bankCode:         varchar("bank_code", { length: 10 }),
  bankName:         varchar("bank_name", { length: 128 }),
  agencyNumber:     varchar("agency_number", { length: 10 }),
  accountNumber:    varchar("account_number", { length: 20 }),
  accountType:      mysqlEnum("account_type", ["checking", "savings"]),
  accountHolderName:     varchar("account_holder_name", { length: 256 }),
  accountHolderDocument: varchar("account_holder_document", { length: 512 }), // encrypted

  // ── Gateway externo (Stripe, futuros) ───────────────────────────
  externalAccountId: varchar("external_account_id", { length: 256 }),
  externalMetadata:  json("external_metadata"),                 // campos arbitrários por gateway

  ...timestamps,
  archivedAt: timestamp("archived_at"),
}, (t) => ({
  // Somente um método padrão por guia
  uniqueDefault: uniqueIndex("uniq_guide_default")
    .on(t.guideId, t.isDefault)
    .where(sql`${t.isDefault} = 1 AND ${t.archivedAt} IS NULL`),
  idxGuide:  index("idx_guide_payment_methods_guide").on(t.guideId),
  idxStatus: index("idx_guide_payment_methods_status").on(t.status),
}));
```

### 2 — Colunas removidas de `guide_verification`

```sql
-- drizzle/XXXX_extract_payment_methods.sql

ALTER TABLE guide_verification
  DROP COLUMN pix_key,
  DROP COLUMN pix_key_type,
  DROP COLUMN pix_key_holder_name,
  DROP COLUMN pix_key_verified,
  DROP COLUMN pix_key_document,
  DROP COLUMN bank_code,
  DROP COLUMN bank_name,
  DROP COLUMN agency_number,
  DROP COLUMN account_number,
  DROP COLUMN account_type,
  DROP COLUMN account_holder_name,
  DROP COLUMN account_holder_document;
```

### 3 — Script de migração de dados (executar antes do DROP)

```sql
-- Executar ANTES do ALTER TABLE acima
INSERT INTO guide_payment_methods (
  guide_id, type, status, is_default,
  pix_key_type, pix_key, pix_key_holder_name, pix_key_document,
  bank_code, bank_name, agency_number, account_number,
  account_type, account_holder_name, account_holder_document,
  created_at, updated_at
)
SELECT
  user_id,
  'pix',
  CASE WHEN pix_key_verified = 1 THEN 'active' ELSE 'pending_verification' END,
  1,                          -- primeiro método sempre é default
  pix_key_type,
  pix_key,                    -- já criptografado, mantém criptografia
  pix_key_holder_name,
  pix_key_document,
  bank_code, bank_name, agency_number, account_number,
  account_type, account_holder_name, account_holder_document,
  created_at, updated_at
FROM guide_verification
WHERE pix_key IS NOT NULL;
```

### 4 — Atualização de `isGuidePaymentsEnabled`

```typescript
// server/lib/paymentsGate.ts

export async function isGuidePaymentsEnabled(
  guideId: number,
  db: DbClient
): Promise<boolean> {
  const verification = await db.getGuideVerification(guideId);
  if (!["pending", "approved"].includes(verification?.status ?? "")) return false;

  const defaultMethod = await db.getDefaultPaymentMethod(guideId);
  return (
    defaultMethod !== null &&
    defaultMethod.status === "active" &&
    defaultMethod.archivedAt === null
  );
}
```

### 5 — Novos métodos em `server/db.ts`

```typescript
getDefaultPaymentMethod(guideId: number)
  → GuidePaymentMethod | null
  // WHERE guideId = X AND isDefault = 1 AND archivedAt IS NULL

listGuidePaymentMethods(guideId: number)
  → GuidePaymentMethod[]
  // WHERE guideId = X AND archivedAt IS NULL ORDER BY createdAt ASC

createPaymentMethod(data: NewGuidePaymentMethod)
  → insertId

updatePaymentMethod(id: number, data: Partial<GuidePaymentMethod>)
  → void

setDefaultPaymentMethod(guideId: number, methodId: number)
  → void
  // transaction: UPDATE SET isDefault=0 WHERE guideId; UPDATE SET isDefault=1 WHERE id

archivePaymentMethod(id: number)
  → void
  // UPDATE SET archivedAt = NOW()
```

### 6 — Novos endpoints tRPC

```typescript
// server/routers.ts

guides.savePaymentMethod       // substitui guides.savePixData
  [guideProcedure.mutation]
  Input: { type, pixKeyType?, pixKey?, pixKeyHolderName?, ...bankFields? }
  → { success: true, methodId: number }

guides.getMyPaymentMethods     // lista métodos sem dados sensíveis
  [guideProcedure.query]
  → { id, type, status, isDefault, pixKeyType, pixKeyHolderName, createdAt }[]
  // pixKey, pixKeyDocument, accountNumber NÃO retornados

guides.setDefaultPaymentMethod
  [guideProcedure.mutation]
  Input: { methodId: number }
  → { success: true }

guides.archivePaymentMethod
  [guideProcedure.mutation]
  Input: { methodId: number }
  → { success: true }
```

### 7 — Retrocompatibilidade
Manter `guides.savePixData` como alias depreciado que internamente chama `guides.savePaymentMethod` com `type: "pix"`. Remover após confirmar que nenhum cliente externo usa o endpoint antigo.

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|--------|---------|---------|
| **Nova tabela** | `guide_payment_methods` com suporte a multiplos tipos | `drizzle/schema.ts` |
| **Migration DDL** | `XXXX_extract_payment_methods.sql` — cria tabela + migra dados + remove colunas de `guide_verification` | `drizzle/` |
| **`guide_verification`** | Remove 11 colunas financeiras; mantém identidade/compliance | `drizzle/schema.ts` |
| **`paymentsGate.ts`** | `isGuidePaymentsEnabled` passa a consultar `guide_payment_methods` | `server/lib/paymentsGate.ts` |
| **`server/db.ts`** | Novos métodos: `getDefaultPaymentMethod`, `listGuidePaymentMethods`, `setDefaultPaymentMethod`, `archivePaymentMethod` | `server/db.ts` |
| **tRPC** | Novos: `savePaymentMethod`, `getMyPaymentMethods`, `setDefaultPaymentMethod`, `archivePaymentMethod` — `savePixData` vira alias depreciado | `server/routers.ts` |
| **Payout engine** | `payouts.processScheduled` consulta `getDefaultPaymentMethod` em vez de `getGuideVerificationDecrypted` | `server/` |
| **Frontend** | `GuidePixForm` → `GuidePaymentMethodForm` com campo `type` no topo | `GuidePixForm.tsx` |
| **Schema / Migrations** | **1 migration necessária** (create + data migration + alter) | `drizzle/` |

### Ordem de execução da migration

```
1. CREATE TABLE guide_payment_methods
2. INSERT INTO guide_payment_methods ... SELECT FROM guide_verification  ← migração de dados
3. ALTER TABLE guide_verification DROP COLUMN pix_key, ...              ← remove colunas
```

> **Rollback:** Manter backup das colunas como `_archived_pix_key` (prefixo) por 2 sprints antes do DROP definitivo, permitindo rollback sem perda de dados.
