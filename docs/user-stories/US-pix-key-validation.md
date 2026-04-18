# US — Validação da Chave Pix por Tipo

## Title
**Como guia**, quero que o sistema valide minha chave Pix de acordo com o tipo selecionado, **para que** eu seja avisado de erros de formato ou de negócio antes de salvar e evite falhas de repasse em produção.

---

## Description

Ao preencher o campo `pixKey` no formulário de configuração financeira, o sistema executa duas camadas de validação:

1. **Validação de formato** (client-side, em tempo real via `onChange`/`onBlur`): verifica máscara, comprimento e caracteres esperados para cada tipo.
2. **Validação de negócio** (client-side + server-side): regras específicas do Banco Central e do Trekko, como dígitos verificadores de CPF/CNPJ, consistência com o documento cadastrado, DDD válido, e limite de comprimento para e-mail (norma Pix BACEN).

A mutation `guides.savePixData` **rejeita** qualquer chave que não passe na camada server-side, independentemente do cliente, garantindo integridade dos dados em `guide_verification`.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Previne cadastro de chaves inválidas que causariam falha silenciosa no repasse via Mercado Pago. |
| 2 | Dígitos verificadores CPF/CNPJ bloqueiam chaves sintaticamente corretas mas inexistentes. |
| 3 | Validação server-side garante integridade mesmo se o cliente for bypassado (chamadas diretas à API). |
| 4 | Feedback imediato no formulário elimina ciclos de suporte pós-cadastro. |

---

## Acceptance Criteria

```gherkin
Feature: Validação da chave Pix por tipo

  Background:
    Given o guia está autenticado
    And está no formulário de configuração Pix ("/guia/configuracoes/pix")
    And documentType é "CPF" e documentNumber é "272.987.694-88"

  # ─── CPF ──────────────────────────────────────────────────────

  Scenario: CPF válido — dígitos verificadores corretos e igual ao documento
    Given pixKeyType é "cpf"
    When pixKey é "272.987.694-88" (mesmo que documentNumber, dígitos válidos)
    Then nenhum erro é exibido
    And o botão "Salvar Dados PIX" fica habilitado (demais campos preenchidos)

  Scenario: CPF com dígitos verificadores inválidos
    Given pixKeyType é "cpf"
    When o guia digita pixKey "272.987.694-00" (dígitos verificadores incorretos)
    And remove o foco do campo
    Then o campo exibe erro inline: "CPF inválido"
    And a mutation "guides.savePixData" NÃO é chamada

  Scenario: CPF com todos os dígitos iguais
    Given pixKeyType é "cpf"
    When o guia digita pixKey "111.111.111-11"
    And remove o foco do campo
    Then o campo exibe erro inline: "CPF inválido"

  Scenario: CPF diferente do documentNumber cadastrado
    Given pixKeyType é "cpf"
    When pixKey é "111.444.777-35" (CPF válido, mas diferente do documentNumber)
    And tenta submeter
    Then o campo exibe erro: "Chave PIX deve pertencer ao mesmo CPF/CNPJ cadastrado"
    And a mutation NÃO é chamada

  Scenario: CPF com comprimento incorreto
    Given pixKeyType é "cpf"
    When pixKey tem menos ou mais de 11 dígitos
    Then o campo exibe erro inline: "CPF deve ter 11 dígitos"

  # ─── CNPJ ─────────────────────────────────────────────────────

  Scenario: CNPJ válido — dígitos verificadores corretos e igual ao documento
    Given documentType é "CNPJ" e documentNumber é "11.222.333/0001-81"
    And pixKeyType é "cnpj"
    When pixKey é "11.222.333/0001-81"
    Then nenhum erro é exibido

  Scenario: CNPJ com dígitos verificadores inválidos
    Given pixKeyType é "cnpj"
    When pixKey é "11.222.333/0001-00"
    And remove o foco
    Then o campo exibe erro inline: "CNPJ inválido"
    And a mutation NÃO é chamada

  Scenario: CNPJ com todos os dígitos iguais
    Given pixKeyType é "cnpj"
    When pixKey é "11.111.111/1111-11"
    Then o campo exibe erro inline: "CNPJ inválido"

  Scenario: CNPJ diferente do documentNumber cadastrado
    Given pixKeyType é "cnpj"
    When pixKey é um CNPJ válido mas diferente do documentNumber
    Then o campo exibe erro: "Chave PIX deve pertencer ao mesmo CPF/CNPJ cadastrado"

  # ─── E-mail ───────────────────────────────────────────────────

  Scenario: E-mail válido
    Given pixKeyType é "email"
    When pixKey é "guia@empresa.com.br"
    Then nenhum erro é exibido

  Scenario: E-mail sem domínio
    Given pixKeyType é "email"
    When pixKey é "guia@"
    And remove o foco
    Then o campo exibe erro inline: "Formato de e-mail inválido"

  Scenario: E-mail sem arroba
    Given pixKeyType é "email"
    When pixKey é "guiaempresa.com"
    And remove o foco
    Then o campo exibe erro inline: "Formato de e-mail inválido"

  Scenario: E-mail excede 77 caracteres (limite BACEN Pix)
    Given pixKeyType é "email"
    When pixKey tem 78 ou mais caracteres
    And remove o foco
    Then o campo exibe erro inline: "E-mail deve ter no máximo 77 caracteres (limite Pix)"

  # ─── Telefone ─────────────────────────────────────────────────

  Scenario: Telefone celular brasileiro válido
    Given pixKeyType é "phone"
    When pixKey é "(11) 99999-9999"
    Then nenhum erro é exibido
    And o valor sanitizado enviado à API é "+5511999999999"

  Scenario: Telefone com DDD inválido
    Given pixKeyType é "phone"
    When pixKey é "(00) 99999-9999" (DDD 00 não existe no Brasil)
    And remove o foco
    Then o campo exibe erro inline: "DDD inválido"

  Scenario: Telefone com menos de 11 dígitos
    Given pixKeyType é "phone"
    When pixKey é "(11) 9999-9999" (10 dígitos — formato fixo)
    And remove o foco
    Then o campo exibe erro inline: "Telefone celular deve ter 11 dígitos (DDD + 9 dígitos)"

  Scenario: Telefone fixo (não aceito como chave Pix celular)
    Given pixKeyType é "phone"
    When pixKey é "(11) 3333-3333" (começa com dígito 3, não é celular)
    And remove o foco
    Then o campo exibe erro inline: "A chave Pix telefone deve ser um número de celular (9º dígito obrigatório)"

  # ─── Chave Aleatória ──────────────────────────────────────────

  Scenario: Chave aleatória no formato UUID v4 válido
    Given pixKeyType é "random"
    When pixKey é "123e4567-e89b-42d3-a456-426614174000"
    Then nenhum erro é exibido

  Scenario: Chave aleatória com formato inválido
    Given pixKeyType é "random"
    When pixKey não segue o padrão UUID v4
      | valor inválido         | motivo                          |
      | "chave-invalida"       | não é UUID                      |
      | "123e4567e89b42d3"     | sem hífens                      |
      | ""                     | vazio                           |
    And remove o foco
    Then o campo exibe erro inline: "Chave aleatória deve estar no formato UUID (ex: xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx)"

  # ─── Validação server-side ────────────────────────────────────

  Scenario: Chamada direta à API com CPF inválido (bypass do cliente)
    Given uma requisição direta à mutation "guides.savePixData"
    With pixKeyType "cpf" e pixKey "11111111111" (dígitos verificadores inválidos)
    Then a API retorna erro BAD_REQUEST: "pix_key_invalid_cpf"
    And nenhum registro é criado ou atualizado em "guide_verification"

  Scenario: Chamada direta com e-mail acima de 77 caracteres
    Given uma requisição direta com pixKeyType "email" e pixKey com 78 chars
    Then a API retorna erro BAD_REQUEST: "pix_key_email_too_long"

  Scenario: Chamada direta com telefone sem prefixo "+55"
    Given a sanitização do cliente é bypassada
    And pixKey enviado é "11999999999" (sem "+55")
    Then o servidor adiciona o prefixo "+55" automaticamente antes de salvar
    And o valor armazenado é "+5511999999999"
```

---

## Technical Notes

### 1 — Biblioteca de validação compartilhada
Criar `shared/lib/pixKeyValidation.ts` (importável tanto no cliente quanto no servidor) para centralizar todas as regras e evitar duplicação:

```typescript
// shared/lib/pixKeyValidation.ts

export type PixKeyType = "cpf" | "cnpj" | "email" | "phone" | "random";

export type ValidationResult =
  | { valid: true }
  | { valid: false; code: string; message: string };

export function validatePixKey(
  type: PixKeyType,
  value: string,
  documentNumber?: string
): ValidationResult {
  const raw = value.replace(/\D/g, "");

  switch (type) {
    case "cpf":
      return validateCPF(raw, documentNumber?.replace(/\D/g, ""));
    case "cnpj":
      return validateCNPJ(raw, documentNumber?.replace(/\D/g, ""));
    case "email":
      return validateEmail(value.trim());
    case "phone":
      return validatePhone(raw);
    case "random":
      return validateRandomKey(value.trim());
  }
}
```

### 2 — Algoritmo de dígitos verificadores CPF

```typescript
function validateCPF(raw: string, docNumber?: string): ValidationResult {
  if (raw.length !== 11)
    return { valid: false, code: "pix_key_cpf_length", message: "CPF deve ter 11 dígitos" };
  if (/^(\d)\1{10}$/.test(raw))
    return { valid: false, code: "pix_key_cpf_invalid", message: "CPF inválido" };

  // Dígito verificador 1
  let sum = 0;
  for (let i = 0; i < 9; i++) sum += parseInt(raw[i]) * (10 - i);
  let d1 = 11 - (sum % 11);
  if (d1 >= 10) d1 = 0;

  // Dígito verificador 2
  sum = 0;
  for (let i = 0; i < 10; i++) sum += parseInt(raw[i]) * (11 - i);
  let d2 = 11 - (sum % 11);
  if (d2 >= 10) d2 = 0;

  if (parseInt(raw[9]) !== d1 || parseInt(raw[10]) !== d2)
    return { valid: false, code: "pix_key_cpf_invalid", message: "CPF inválido" };

  if (docNumber && raw !== docNumber)
    return { valid: false, code: "pix_key_doc_mismatch", message: "Chave PIX deve pertencer ao mesmo CPF/CNPJ cadastrado" };

  return { valid: true };
}
```

### 3 — Algoritmo de dígitos verificadores CNPJ

```typescript
function validateCNPJ(raw: string, docNumber?: string): ValidationResult {
  if (raw.length !== 14)
    return { valid: false, code: "pix_key_cnpj_length", message: "CNPJ deve ter 14 dígitos" };
  if (/^(\d)\1{13}$/.test(raw))
    return { valid: false, code: "pix_key_cnpj_invalid", message: "CNPJ inválido" };

  const calcDigit = (slice: string, weights: number[]) => {
    const sum = slice.split("").reduce((acc, d, i) => acc + parseInt(d) * weights[i], 0);
    const rem = sum % 11;
    return rem < 2 ? 0 : 11 - rem;
  };

  const w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
  const w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];

  if (
    calcDigit(raw.slice(0, 12), w1) !== parseInt(raw[12]) ||
    calcDigit(raw.slice(0, 13), w2) !== parseInt(raw[13])
  )
    return { valid: false, code: "pix_key_cnpj_invalid", message: "CNPJ inválido" };

  if (docNumber && raw !== docNumber)
    return { valid: false, code: "pix_key_doc_mismatch", message: "Chave PIX deve pertencer ao mesmo CPF/CNPJ cadastrado" };

  return { valid: true };
}
```

### 4 — Validação de e-mail (norma BACEN)

```typescript
function validateEmail(value: string): ValidationResult {
  if (value.length > 77)
    return { valid: false, code: "pix_key_email_too_long", message: "E-mail deve ter no máximo 77 caracteres (limite Pix)" };
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value))
    return { valid: false, code: "pix_key_email_invalid", message: "Formato de e-mail inválido" };
  return { valid: true };
}
```

### 5 — Validação de telefone (DDD + celular brasileiro)

```typescript
// DDDs válidos no Brasil (ANATEL)
const VALID_DDDS = new Set([
  11,12,13,14,15,16,17,18,19, // SP
  21,22,24,                    // RJ/ES
  27,28,                       // ES
  31,32,33,34,35,37,38,        // MG
  41,42,43,44,45,46,           // PR
  47,48,49,                    // SC
  51,53,54,55,                 // RS
  61,62,63,64,65,66,67,68,69, // CO/N
  71,73,74,75,77,              // BA
  79,                          // SE
  81,82,83,84,85,86,87,88,89, // NE
  91,92,93,94,95,96,97,98,99, // N
]);

function validatePhone(raw: string): ValidationResult {
  if (raw.length !== 11)
    return { valid: false, code: "pix_key_phone_length", message: "Telefone celular deve ter 11 dígitos (DDD + 9 dígitos)" };

  const ddd = parseInt(raw.slice(0, 2));
  if (!VALID_DDDS.has(ddd))
    return { valid: false, code: "pix_key_phone_ddd", message: "DDD inválido" };

  if (raw[2] !== "9")
    return { valid: false, code: "pix_key_phone_mobile", message: "A chave Pix telefone deve ser um número de celular (9º dígito obrigatório)" };

  return { valid: true };
}
```

### 6 — Validação de chave aleatória (UUID v4)

```typescript
const UUID_V4_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

function validateRandomKey(value: string): ValidationResult {
  if (!value)
    return { valid: false, code: "pix_key_random_empty", message: "Informe a chave aleatória" };
  if (!UUID_V4_REGEX.test(value))
    return { valid: false, code: "pix_key_random_invalid", message: "Chave aleatória deve estar no formato UUID (ex: xxxxxxxx-xxxx-4xxx-xxxx-xxxxxxxxxxxx)" };
  return { valid: true };
}
```

### 7 — Sanitização de telefone para padrão BACEN (+55)
Telefone deve ser armazenado com prefixo `+55` conforme norma Pix do BACEN. Aplicar no servidor em `db.saveGuidePixData`:

```typescript
// server/db.ts — saveGuidePixData
if (data.pixKeyType === "phone") {
  const digits = data.pixKey.replace(/\D/g, "");
  data.pixKey = digits.startsWith("55") ? `+${digits}` : `+55${digits}`;
}
```

### 8 — Integração no servidor (`guides.savePixData`)
Adicionar chamada a `validatePixKey` no início da mutation, antes de qualquer operação de banco:

```typescript
// server/routers.ts — guides.savePixData
const result = validatePixKey(input.pixKeyType, input.pixKey, input.documentNumber);
if (!result.valid) {
  throw new TRPCError({ code: "BAD_REQUEST", message: result.code });
}
```

### 9 — Integração no cliente (`GuidePixForm.tsx`)
Usar o mesmo `validatePixKey` no Zod `superRefine` (conforme US-pix-key-type-dynamic-ui):

```typescript
.superRefine((data, ctx) => {
  const result = validatePixKey(data.pixKeyType, data.pixKey, data.documentNumber);
  if (!result.valid) {
    ctx.addIssue({ code: z.ZodIssueCode.custom, message: result.message, path: ["pixKey"] });
  }
})
```

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|--------|---------|---------|
| Novo módulo compartilhado | `validatePixKey()` com todas as regras por tipo | `shared/lib/pixKeyValidation.ts` |
| tRPC `guides.savePixData` | Chamar `validatePixKey` antes de persistir; lançar `BAD_REQUEST` se inválido | `server/routers.ts` |
| DB `saveGuidePixData` | Normalizar telefone para `+55XXXXXXXXXXX` antes de criptografar | `server/db.ts` |
| Frontend `GuidePixForm` | Integrar `validatePixKey` no `superRefine` do schema Zod | `GuidePixForm.tsx` |
| Schema / Migrations | **Nenhuma alteração necessária** | — |

### Mapa de códigos de erro (tRPC `BAD_REQUEST`)

| `message` (code) | Tipo | Descrição |
|---|---|---|
| `pix_key_cpf_length` | CPF | Não tem 11 dígitos |
| `pix_key_cpf_invalid` | CPF | Dígitos verificadores incorretos ou todos iguais |
| `pix_key_cnpj_length` | CNPJ | Não tem 14 dígitos |
| `pix_key_cnpj_invalid` | CNPJ | Dígitos verificadores incorretos ou todos iguais |
| `pix_key_doc_mismatch` | CPF/CNPJ | Chave não bate com `documentNumber` |
| `pix_key_email_invalid` | Email | Formato inválido |
| `pix_key_email_too_long` | Email | Excede 77 chars (norma BACEN) |
| `pix_key_phone_length` | Telefone | Não tem 11 dígitos |
| `pix_key_phone_ddd` | Telefone | DDD inexistente no Brasil |
| `pix_key_phone_mobile` | Telefone | Não é celular (9º dígito ausente) |
| `pix_key_random_empty` | Aleatória | Campo vazio |
| `pix_key_random_invalid` | Aleatória | Não segue formato UUID v4 |

### Normas aplicadas
- **BACEN Resolução BCB nº 1** — formatos de chaves Pix (CPF, CNPJ, e-mail ≤ 77 chars, telefone `+55XXXXXXXXXXX`, UUID v4 para aleatória)
- **Receita Federal** — algoritmo de dígitos verificadores CPF e CNPJ
- **ANATEL** — lista de DDDs válidos no Brasil
