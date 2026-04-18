# US — Segurança dos Dados da Chave Pix

## Title
**Como plataforma**, quero garantir que dados de chave Pix sejam criptografados em repouso, nunca expostos em texto claro fora do contexto de repasse, e mascarados em todas as interfaces de usuário, **para que** uma exposição acidental de banco de dados, log ou resposta de API não comprometa dados financeiros dos guias.

---

## Description

A segurança dos dados Pix é organizada em quatro camadas independentes, de modo que a falha em qualquer uma delas não comprometa as demais:

| Camada | Mecanismo |
|---|---|
| **Repouso** | AES-256-GCM application-layer encryption (`server/lib/crypto.ts`) em todos os campos sensíveis de `guide_payment_methods` |
| **Trânsito** | HTTPS obrigatório; `pixKey` plaintext nunca em query params, headers ou logs de request |
| **Acesso** | Decriptografia permitida exclusivamente no job de payout (`payouts.processScheduled`) — proibida em qualquer endpoint de API público ou de guia |
| **Apresentação** | Apenas `maskedPixKey` retornado em respostas de API; valor bruto e ciphertext nunca serializados para o cliente |

Um **evento de acesso** em `payment_audit_log` é registrado toda vez que `getDefaultPaymentMethodDecrypted()` é chamado — mesmo em contexto de sistema.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Vazamento do banco de dados não expõe chaves Pix — o atacante obtém apenas ciphertext sem a chave de criptografia. |
| 2 | Logs de aplicação e de request nunca contêm dados financeiros — reduz superfície de exposição em incidentes de log leakage. |
| 3 | Acesso à decriptografia limitado a um único ponto de código auditável — blast radius mínimo em caso de bug ou comprometimento. |
| 4 | Conformidade com LGPD (Art. 46 — segurança no tratamento) e PCI-DSS SAQ-A (proteção de dados de pagamento). |

---

## Acceptance Criteria

```gherkin
Feature: Segurança dos dados da chave Pix

  # ─── Criptografia em repouso ──────────────────────────────────────

  Scenario: Campos sensíveis armazenados como ciphertext no banco
    Given o guia salva uma chave Pix do tipo "cpf" com valor "27298769488"
    When o valor é consultado diretamente no banco (SELECT pix_key FROM guide_payment_methods)
    Then o valor retornado é ciphertext AES-256-GCM, não "27298769488"
    And o ciphertext inclui o nonce (IV) concatenado ao valor cifrado
    And documentNumber e pixKeyDocument também estão criptografados

  Scenario: Colunas sensíveis identificadas por convenção de nomenclatura
    Then as seguintes colunas em guide_payment_methods são sempre criptografadas:
      | pix_key                   |
      | pix_key_document          |
      | account_holder_document   |
      | account_number            |
    And as seguintes colunas são armazenadas em texto claro (não-sensíveis):
      | pix_key_type              |
      | pix_key_holder_name       |
      | type                      |
      | status                    |

  Scenario: Chave de criptografia não está hardcoded no código-fonte
    When qualquer arquivo do repositório é inspecionado por strings de chave AES
    Then nenhuma chave de criptografia é encontrada no código-fonte
    And a chave é carregada exclusivamente de variável de ambiente ENCRYPTION_KEY
    And a aplicação falha ao iniciar (startup check) se ENCRYPTION_KEY não estiver definida

  Scenario: Rotação de chave de criptografia — re-encryption sem downtime
    Given a ENCRYPTION_KEY precisa ser rotacionada
    When o job de rotação é executado com ENCRYPTION_KEY_OLD e ENCRYPTION_KEY_NEW
    Then para cada registro em guide_payment_methods com campo criptografado:
      | O campo é descriptografado com ENCRYPTION_KEY_OLD |
      | Re-criptografado com ENCRYPTION_KEY_NEW            |
      | Atualizado atomicamente no banco                   |
    And um evento "encryption_key_rotated" é registrado em payment_audit_log por registro
    And ENCRYPTION_KEY_OLD é removida das variáveis de ambiente após validação

  # ─── Controle de acesso à decriptografia ─────────────────────────

  Scenario: Decriptografia permitida somente no job de payout
    Given qualquer código fora de payouts.processScheduled
    When tenta chamar getDefaultPaymentMethodDecrypted()
    Then uma exceção de compilação ou runtime impede o uso não autorizado
    And a função só é exportada para o módulo de payout

  Scenario: API de guia nunca retorna pixKey em texto claro
    When o guia chama qualquer endpoint tRPC (guides.*, expeditions.*)
    Then nenhuma resposta contém pixKey em plaintext
    And nenhuma resposta contém o ciphertext de pixKey
    And apenas maskedPixKey (ex: "272.***.***-88") está presente nas respostas

  Scenario: API pública nunca expõe dados financeiros do guia
    When um usuário não autenticado chama guides.getById
    Then a resposta contém apenas: paymentsEnabled (boolean)
    And não contém: pixKey, pixKeyType, maskedPixKey, documentNumber, bankCode

  Scenario: Admin pode ver maskedPixKey mas não o valor bruto via API
    When um admin chama admin.getGuidePaymentMethod
    Then recebe maskedPixKey, pixKeyType, pixKeyHolderName, status
    And NÃO recebe pixKey em plaintext
    And para obter o valor bruto, o admin acessa o painel interno com 2FA obrigatório

  Scenario: Evento de acesso registrado a cada decriptografia
    Given o job de payout chama getDefaultPaymentMethodDecrypted(guideId)
    Then um evento é criado em payment_audit_log:
      | entityType | "guide_payment_method"       |
      | action     | "pix_key_decrypted"          |
      | actorType  | "system"                     |
      | actorId    | NULL (sistema, não usuário)  |
      | newValue   | { "context": "payout_processing", "payoutId": <id> } |
    And pixKey decriptografado NÃO aparece no payload do evento

  # ─── Mascaramento na UI ───────────────────────────────────────────

  Scenario: Formulário de configuração Pix exibe valor mascarado
    When o guia acessa "/guia/configuracoes/pix" com chave já cadastrada
    Then o campo exibe o valor mascarado conforme tipo:
      | Tipo    | Exemplo de exibição         |
      | cpf     | 272.***.***-88              |
      | cnpj    | 11.***.***/0001-81          |
      | email   | joao@***.com.br             |
      | phone   | +55 (11) *****-9999         |
      | random  | 123e4567-****-****-****-0000|
    And o campo está em modo readonly (não editável sem clicar em "Alterar chave")

  Scenario: Campo mascarado não pode ser inspecionado via DevTools para revelar o valor real
    Given o campo de chave Pix mascarada está visível na UI
    When o usuário inspeciona o elemento no navegador (DevTools)
    Then o valor no DOM é apenas o texto mascarado
    And nenhum atributo data-* ou hidden input contém o valor bruto ou ciphertext
    And a resposta da API que populou o campo contém apenas maskedPixKey

  Scenario: Logs de request nunca contêm pixKey
    Given qualquer request POST/PUT para endpoints de salvar ou atualizar Pix
    When o middleware de logging registra a requisição
    Then o campo pixKey é redacted no log: "[REDACTED]"
    And documentNumber também é redacted: "[REDACTED]"
    And os demais campos (pixKeyType, pixKeyHolderName) são logados normalmente

  Scenario: Mensagens de erro nunca ecoam o valor da chave Pix
    Given uma validação falha com pixKey inválido
    When o servidor retorna o erro ao cliente
    Then a mensagem de erro contém apenas o código (ex: "pix_key_cpf_invalid")
    And NÃO contém o valor submetido da chave Pix no corpo do erro

  # ─── Transporte ──────────────────────────────────────────────────

  Scenario: pixKey nunca trafega em query string ou header
    When qualquer mutation que recebe pixKey é chamada
    Then o valor é transmitido exclusivamente no body da requisição (POST/PUT)
    And nenhum endpoint aceita pixKey como query param ou header customizado

  Scenario: Resposta de API não inclui headers com dados sensíveis
    When qualquer endpoint retorna dados de guide_payment_methods
    Then os headers da resposta não contêm pixKey, documentNumber ou qualquer dado financeiro
    And o header Content-Security-Policy está presente para endpoints de UI

  # ─── Startup check ───────────────────────────────────────────────

  Scenario: Aplicação recusa inicialização sem variáveis de segurança
    Given ENCRYPTION_KEY não está definida no ambiente
    When a aplicação tenta inicializar
    Then o processo termina com exit code 1
    And a mensagem de erro é: "FATAL: ENCRYPTION_KEY environment variable is required"
    And nenhuma requisição é aceita

  Scenario: Chave de criptografia com comprimento inválido causa falha no startup
    Given ENCRYPTION_KEY está definida mas tem menos de 32 bytes
    When a aplicação tenta inicializar
    Then o processo termina com exit code 1 e mensagem descritiva
```

---

## Technical Notes

### 1 — Campos criptografados por convenção

Adotar sufixo `_encrypted` **internamente no código** (não no schema) para distinguir variáveis que contêm ciphertext de variáveis que contêm plaintext — evita passagem acidental de ciphertext onde plaintext é esperado:

```typescript
// server/lib/crypto.ts — tipos opacos para separação em compile-time

type Ciphertext = string & { readonly __brand: "Ciphertext" };
type Plaintext  = string & { readonly __brand: "Plaintext" };

export function encrypt(value: Plaintext): Promise<Ciphertext>;
export function decrypt(value: Ciphertext): Promise<Plaintext>;
```

O schema Drizzle usa `Ciphertext` nos campos sensíveis:

```typescript
// drizzle/schema.ts
pixKey: varchar("pix_key", { length: 512 }).$type<Ciphertext>(),
```

Qualquer tentativa de passar `Ciphertext` onde `Plaintext` é esperado (ou vice-versa) gera erro de TypeScript — sem custo de runtime.

### 2 — Startup check e validação da chave

```typescript
// server/_core/index.ts — executar antes de qualquer listener

function assertEncryptionKeyValid() {
  const key = process.env.ENCRYPTION_KEY;
  if (!key) {
    console.error("FATAL: ENCRYPTION_KEY environment variable is required");
    process.exit(1);
  }
  const keyBytes = Buffer.from(key, "hex");
  if (keyBytes.length !== 32) {
    console.error(`FATAL: ENCRYPTION_KEY must be 32 bytes (256 bits). Got: ${keyBytes.length} bytes`);
    process.exit(1);
  }
}

assertEncryptionKeyValid(); // antes de app.listen()
```

### 3 — Algoritmo AES-256-GCM (padrão DB-SEC-01 já existente)

Confirmar que a implementação em `server/lib/crypto.ts` segue:
- **Algoritmo:** AES-256-GCM
- **Nonce:** 12 bytes aleatórios gerados por `crypto.randomBytes(12)` — único por operação de encrypt
- **Formato armazenado:** `nonce(12 bytes) + authTag(16 bytes) + ciphertext` — concatenados em hex ou base64
- **AAD (Additional Authenticated Data):** incluir `guideId` como AAD para vincular o ciphertext ao registro correto (previne transplante de ciphertext entre registros)

```typescript
// Exemplo de AAD para vincular ciphertext ao guia
const aad = Buffer.from(`guide:${guideId}:pixKey`);
cipher.setAAD(aad);
// ... durante decrypt, verificar com o mesmo AAD
```

### 4 — Acesso à decriptografia restrito ao módulo de payout

Usar módulo com export seletivo para impedir uso fora do contexto autorizado:

```typescript
// server/lib/payoutDecrypt.ts
// ÚNICO arquivo autorizado a chamar decrypt() para pixKey

import { decrypt } from "./crypto";
import { db } from "../db";

// Não exportar decrypt() diretamente — encapsular com audit obrigatório
export async function getPixKeyForPayout(
  guideId: number,
  payoutId: number,
  tx: DbTransaction
): Promise<string> {
  const method = await db.getDefaultPaymentMethod(guideId);
  if (!method?.pixKey) throw new Error("no_active_pix_method");

  const plaintext = await decrypt(method.pixKey);

  await writePaymentAuditEvent(tx, {
    action: "pix_key_decrypted",
    entityId: method.id,
    actorId: 0,             // sistema
    actorType: "system",
    previousValue: null,
    newValue: { context: "payout_processing", payoutId },
    ipAddress: "internal",
    userAgent: "payout-job",
  });

  return plaintext;
}
```

No `tsconfig.json` ou via ESLint rule (`no-restricted-imports`), bloquear imports de `decrypt` fora de `payoutDecrypt.ts`:

```json
// .eslintrc — regra de import restrito
{
  "rules": {
    "no-restricted-imports": ["error", {
      "paths": [{
        "name": "../lib/crypto",
        "importNames": ["decrypt"],
        "message": "Use getPixKeyForPayout() from payoutDecrypt.ts instead of calling decrypt() directly."
      }]
    }]
  }
}
```

### 5 — Redaction de campos sensíveis nos logs

Adicionar middleware de sanitização de request body antes do logger:

```typescript
// server/_core/middleware/logSanitizer.ts

const SENSITIVE_FIELDS = ["pixKey", "documentNumber", "pixKeyDocument", "accountNumber", "accountHolderDocument"];

export function sanitizeLogBody(body: Record<string, unknown>): Record<string, unknown> {
  return Object.fromEntries(
    Object.entries(body).map(([k, v]) => [
      k,
      SENSITIVE_FIELDS.includes(k) ? "[REDACTED]" : v,
    ])
  );
}
```

Aplicar no middleware de logging do Express antes de serializar o body.

### 6 — `maskedPixKey` como único dado de apresentação

`maskPixKey()` (definida em `server/lib/pixKeyMask.ts`, ver US-guide-pix-key-update) é chamada exclusivamente na camada de resposta tRPC — nunca armazenada no banco ou em cache:

```typescript
// Regra: maskedPixKey é computado on-the-fly, nunca persistido
// Motivo: se a lógica de mascaramento mudar, não há dados históricos "errados" no banco
```

A função de mascaramento é **determinística e reversível apenas para o sistema** — o mascaramento não é um hash, não é criptografia, é apresentação. A única fonte de verdade é o ciphertext no banco.

### 7 — Rotação de chave de criptografia

```typescript
// server/jobs/encryptionKeyRotation.ts

export async function rotateEncryptionKey(oldKey: string, newKey: string) {
  const records = await db.getAllPaymentMethodsWithEncryptedFields();

  for (const record of records) {
    await db.transaction(async (tx) => {
      const updates: Partial<GuidePaymentMethod> = {};

      if (record.pixKey) {
        const plain = await decryptWithKey(record.pixKey, oldKey);
        updates.pixKey = await encryptWithKey(plain, newKey);
      }
      if (record.pixKeyDocument) {
        const plain = await decryptWithKey(record.pixKeyDocument, oldKey);
        updates.pixKeyDocument = await encryptWithKey(plain, newKey);
      }

      await tx.updatePaymentMethod(record.id, updates);
      await writePaymentAuditEvent(tx, {
        action: "encryption_key_rotated",
        entityId: record.id,
        actorType: "system",
        actorId: 0,
        previousValue: null,
        newValue: { rotatedAt: new Date().toISOString() },
        ipAddress: "internal",
        userAgent: "key-rotation-job",
      });
    });
  }
}
```

### 8 — Matriz de acesso por contexto

| Contexto | pixKey plaintext | pixKey ciphertext | maskedPixKey | documentNumber |
|---|---|---|---|---|
| `publicProcedure` (guides.getById) | ❌ | ❌ | ❌ | ❌ |
| `guideProcedure` (getMyPaymentMethods) | ❌ | ❌ | ✅ | ❌ |
| `adminProcedure` (getGuidePaymentMethod) | ❌ | ❌ | ✅ | ❌ |
| Payout job (`getPixKeyForPayout`) | ✅ (com audit) | ❌ | ❌ | ✅ (com audit) |
| DB direto (DBA/admin) | — | ✅ (ciphertext) | ❌ | ✅ (ciphertext) |
| Logs de request | ❌ ([REDACTED]) | ❌ | ❌ | ❌ ([REDACTED]) |
| `payment_audit_log` | ❌ | ❌ | ✅ (maskedPixKey) | ❌ |

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|--------|---------|---------|
| Tipos opacos | `Ciphertext` e `Plaintext` branded types para segurança em compile-time | `server/lib/crypto.ts` |
| Startup check | `assertEncryptionKeyValid()` — falha fast se `ENCRYPTION_KEY` ausente ou inválida | `server/_core/index.ts` |
| AAD no AES-GCM | Adicionar `guideId` como Additional Authenticated Data no encrypt/decrypt | `server/lib/crypto.ts` |
| Acesso restrito | `getPixKeyForPayout()` como único ponto de decriptografia — com audit obrigatório | `server/lib/payoutDecrypt.ts` |
| ESLint rule | `no-restricted-imports` bloqueando `decrypt` fora de `payoutDecrypt.ts` | `.eslintrc` |
| Log sanitizer | Middleware que redacta campos sensíveis antes de serializar logs de request | `server/_core/middleware/logSanitizer.ts` |
| Rotação de chave | Job `rotateEncryptionKey(oldKey, newKey)` com re-encrypt atômico por registro | `server/jobs/encryptionKeyRotation.ts` |
| `payment_audit_log` | Novo action: `"pix_key_decrypted"`, `"encryption_key_rotated"` | `drizzle/schema.ts` |
| Schema / Migrations | Nenhuma nova coluna — apenas adição de branded types e AAD ao fluxo existente | — |

### Variáveis de ambiente obrigatórias

| Variável | Descrição | Formato |
|---|---|---|
| `ENCRYPTION_KEY` | Chave AES-256 ativa | 64 chars hex (32 bytes) |
| `ENCRYPTION_KEY_OLD` | Somente durante rotação | 64 chars hex (32 bytes) |

### Normas aplicadas
- **LGPD Art. 46** — medidas técnicas de segurança no tratamento de dados pessoais
- **PCI-DSS SAQ-A / Req. 3.4** — proteção de dados de pagamento armazenados
- **OWASP Top 10 A02:2021** — Cryptographic Failures — algoritmo forte, nonce único, AAD
- **OWASP Top 10 A01:2021** — Broken Access Control — decriptografia restrita a contexto mínimo necessário
