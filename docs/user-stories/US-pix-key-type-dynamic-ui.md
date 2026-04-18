# US — Seleção do Tipo de Chave Pix com Adaptação Dinâmica de UI

## Title
**Como guia**, quero selecionar o tipo da minha chave Pix antes de digitá-la, **para que** o campo de entrada se adapte automaticamente ao formato correto e eu não cometa erros de digitação ou validação.

---

## Description

No formulário de configuração Pix (`GuidePixForm`), o campo de seleção `pixKeyType` controla completamente o comportamento do campo `pixKey` imediatamente abaixo. Ao mudar o tipo, o sistema deve:

1. Limpar o valor atual do campo `pixKey`
2. Aplicar a máscara de formatação correspondente
3. Atualizar o `placeholder` e o texto de ajuda
4. Ativar as regras de validação específicas do tipo selecionado
5. Para tipos CPF/CNPJ: pré-preencher automaticamente com o valor já informado em `documentNumber`

O objetivo é **zero ambiguidade** — o guia sempre sabe exatamente o que digitar e recebe feedback em tempo real se o formato estiver incorreto.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Reduz erros de cadastro de chave Pix, prevenindo falhas de repasse em produção. |
| 2 | Elimina a necessidade de o guia tentar submeter o formulário para descobrir o formato esperado. |
| 3 | Auto-preenchimento CPF/CNPJ elimina digitação redundante e inconsistências de dado. |
| 4 | Feedback inline imediato reduz abandono do formulário de configuração financeira. |

---

## Acceptance Criteria

```gherkin
Feature: Seleção do tipo de chave Pix com adaptação dinâmica de UI

  Background:
    Given o guia está autenticado
    And está no formulário de configuração Pix ("/guia/configuracoes/pix")
    And já informou documentType "CPF" e documentNumber "272.987.694-88"

  # ─── Comportamento ao selecionar o tipo ─────────────────────────

  Scenario: Campo pixKey é limpo ao trocar o tipo
    Given o guia havia informado pixKey "joao@email.com" com pixKeyType "email"
    When altera pixKeyType para "phone"
    Then o campo pixKey é limpo (valor = "")
    And o cursor é posicionado automaticamente no campo pixKey

  Scenario: Seleção do tipo CPF — auto-preenchimento e máscara
    When o guia seleciona pixKeyType "cpf"
    Then o campo pixKey é preenchido automaticamente com "272.987.694-88" (valor de documentNumber)
    And a máscara aplicada é "000.000.000-00"
    And o placeholder exibe "000.000.000-00"
    And o texto de ajuda exibe "A chave PIX CPF deve ser o mesmo CPF do titular da conta"
    And o campo fica readonly (não editável diretamente)

  Scenario: Seleção do tipo CNPJ — auto-preenchimento e máscara
    Given documentType é "CNPJ" e documentNumber é "12.345.678/0001-95"
    When o guia seleciona pixKeyType "cnpj"
    Then o campo pixKey é preenchido automaticamente com "12.345.678/0001-95"
    And a máscara aplicada é "00.000.000/0000-00"
    And o campo fica readonly

  Scenario: Seleção do tipo e-mail — validação de formato
    When o guia seleciona pixKeyType "email"
    Then o campo pixKey é limpo e fica editável
    And o placeholder exibe "seuemail@exemplo.com"
    And o texto de ajuda exibe "Informe o e-mail cadastrado como chave Pix na sua instituição financeira"
    And ao sair do campo com valor "joao@invalido" (sem TLD)
    Then o campo exibe erro inline: "Formato de e-mail inválido"

  Scenario: Seleção do tipo telefone — máscara e validação de 11 dígitos
    When o guia seleciona pixKeyType "phone"
    Then o campo pixKey é limpo e fica editável
    And a máscara aplicada é "(00) 00000-0000"
    And o placeholder exibe "(11) 99999-9999"
    And o texto de ajuda exibe "Informe o celular com DDD cadastrado como chave Pix"
    And ao digitar "1199999" (incompleto)
    Then o campo exibe erro inline: "Telefone deve ter 11 dígitos"
    And ao digitar "11999999999" (completo)
    Then o erro desaparece e o valor é formatado como "(11) 99999-9999"

  Scenario: Seleção do tipo chave aleatória — sem máscara, validação UUID-like
    When o guia seleciona pixKeyType "random"
    Then o campo pixKey é limpo e fica editável
    And nenhuma máscara é aplicada
    And o placeholder exibe "Cole aqui a chave aleatória gerada pelo seu banco"
    And o texto de ajuda exibe "Chave aleatória (UUID) gerada pelo seu banco. Não possui formato fixo."
    And o campo aceita qualquer string não-vazia sem validação de formato

  # ─── Validação em tempo real ─────────────────────────────────────

  Scenario: Erro inline aparece ao sair do campo com valor inválido
    Given o guia selecionou pixKeyType "email"
    And digitou "nao-e-email"
    When remove o foco do campo pixKey (blur event)
    Then o campo exibe borda vermelha e mensagem de erro abaixo
    And o botão "Salvar Dados PIX" permanece desabilitado

  Scenario: Erro inline desaparece ao corrigir o valor
    Given o campo pixKey exibe erro de formato
    When o guia corrige o valor para um e-mail válido "joao@empresa.com.br"
    Then o erro desaparece imediatamente (onChange)
    And a borda volta ao estado normal

  Scenario: Indicador visual do tipo selecionado
    When o guia seleciona qualquer pixKeyType
    Then o label do campo pixKey atualiza para refletir o tipo:
      | pixKeyType | Label do campo          |
      | cpf        | Chave Pix (CPF)         |
      | cnpj       | Chave Pix (CNPJ)        |
      | email      | Chave Pix (E-mail)      |
      | phone      | Chave Pix (Telefone)    |
      | random     | Chave Pix (Aleatória)   |

  # ─── Integração com validação de submissão ───────────────────────

  Scenario: Submissão bloqueada com pixKey em formato inválido para o tipo
    Given pixKeyType é "phone" e pixKey é "(11) 9999-999" (incompleto)
    When o guia tenta submeter o formulário
    Then a mutation "guides.savePixData" NÃO é chamada
    And o foco é redirecionado ao campo pixKey com erro visível

  Scenario: Submissão bem-sucedida após correção do formato
    Given pixKeyType é "phone" e pixKey é "(11) 99999-9999" (válido)
    And todos os outros campos estão corretos
    And os três termos foram aceitos
    When o guia submete
    Then a mutation "guides.savePixData" é chamada com pixKey "11999999999" (somente dígitos)
    And "guide_verification.pixKeyVerified" é atualizado para 1
```

---

## Technical Notes

### 1 — Configuração de tipos (`pixKeyConfig`)
Centralizar toda a lógica em um objeto de configuração, evitando condicionais espalhados:

```typescript
// client/src/components/GuidePixForm.tsx

type PixKeyType = "cpf" | "cnpj" | "email" | "phone" | "random";

const pixKeyConfig: Record<PixKeyType, {
  label: string;
  placeholder: string;
  helpText: string;
  mask?: string;         // máscara para react-input-mask ou similar
  readonly?: boolean;    // auto-preenchido a partir de documentNumber
  validate: (value: string) => string | undefined; // retorna mensagem de erro ou undefined
  sanitize: (value: string) => string; // remove formatação antes de salvar
}> = {
  cpf: {
    label: "Chave Pix (CPF)",
    placeholder: "000.000.000-00",
    helpText: "A chave PIX CPF deve ser o mesmo CPF do titular da conta",
    mask: "999.999.999-99",
    readonly: true,
    validate: (v) => v.replace(/\D/g, "").length === 11 ? undefined : "CPF inválido",
    sanitize: (v) => v.replace(/\D/g, ""),
  },
  cnpj: {
    label: "Chave Pix (CNPJ)",
    placeholder: "00.000.000/0000-00",
    helpText: "A chave PIX CNPJ deve pertencer ao CNPJ do titular da conta",
    mask: "99.999.999/9999-99",
    readonly: true,
    validate: (v) => v.replace(/\D/g, "").length === 14 ? undefined : "CNPJ inválido",
    sanitize: (v) => v.replace(/\D/g, ""),
  },
  email: {
    label: "Chave Pix (E-mail)",
    placeholder: "seuemail@exemplo.com",
    helpText: "Informe o e-mail cadastrado como chave Pix na sua instituição financeira",
    validate: (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? undefined : "Formato de e-mail inválido",
    sanitize: (v) => v.trim().toLowerCase(),
  },
  phone: {
    label: "Chave Pix (Telefone)",
    placeholder: "(11) 99999-9999",
    helpText: "Informe o celular com DDD cadastrado como chave Pix",
    mask: "(99) 99999-9999",
    validate: (v) => v.replace(/\D/g, "").length === 11 ? undefined : "Telefone deve ter 11 dígitos",
    sanitize: (v) => v.replace(/\D/g, ""),
  },
  random: {
    label: "Chave Pix (Aleatória)",
    placeholder: "Cole aqui a chave aleatória gerada pelo seu banco",
    helpText: "Chave aleatória (UUID) gerada pelo seu banco. Não possui formato fixo.",
    validate: (v) => v.trim().length > 0 ? undefined : "Informe a chave aleatória",
    sanitize: (v) => v.trim(),
  },
};
```

### 2 — Lógica de auto-preenchimento (CPF/CNPJ)
No handler `onPixKeyTypeChange`, verificar se o tipo selecionado é `cpf` ou `cnpj` e propagar o valor de `documentNumber`:

```typescript
const onPixKeyTypeChange = (type: PixKeyType) => {
  setValue("pixKeyType", type);
  if (type === "cpf" || type === "cnpj") {
    setValue("pixKey", getValues("documentNumber")); // auto-fill
  } else {
    setValue("pixKey", "");  // limpar para outros tipos
  }
  trigger("pixKey"); // revalidar imediatamente
};
```

### 3 — Validação com react-hook-form + Zod
O schema Zod deve usar `superRefine` para validação cruzada dinâmica:

```typescript
// Exemplo com zod .superRefine
const schema = z.object({
  pixKeyType: z.enum(["cpf", "cnpj", "email", "phone", "random"]),
  pixKey: z.string().min(1),
  documentNumber: z.string(),
  // ... demais campos
}).superRefine((data, ctx) => {
  const config = pixKeyConfig[data.pixKeyType];
  const error = config.validate(data.pixKey);
  if (error) {
    ctx.addIssue({ code: z.ZodIssueCode.custom, message: error, path: ["pixKey"] });
  }
  if ((data.pixKeyType === "cpf" || data.pixKeyType === "cnpj") &&
      config.sanitize(data.pixKey) !== data.documentNumber.replace(/\D/g, "")) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Chave PIX deve pertencer ao mesmo CPF/CNPJ cadastrado",
      path: ["pixKey"],
    });
  }
});
```

### 4 — Sanitização antes de enviar à API
Sempre chamar `pixKeyConfig[type].sanitize(pixKey)` antes da mutation para garantir que somente dados limpos (sem máscara) trafeguem pela rede e sejam armazenados:

```typescript
onSubmit: (data) => {
  const sanitizedPixKey = pixKeyConfig[data.pixKeyType].sanitize(data.pixKey);
  mutate({ ...data, pixKey: sanitizedPixKey });
}
```

### 5 — Máscara de input
Usar `react-input-mask` (já utilizado no projeto para CPF/CNPJ em `RegisterModal.tsx`) ou o padrão nativo `onInput` + `onChange` existente. Remover a máscara quando `pixKeyType = "email"` ou `"random"` (sem máscara).

### 6 — Acessibilidade
- `aria-describedby` ligando o campo `pixKey` ao parágrafo de `helpText`
- `aria-invalid="true"` quando houver erro
- `aria-label` atualizado dinamicamente com o label do tipo selecionado

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|--------|---------|---------|
| Frontend — form config | Novo objeto `pixKeyConfig` centralizando máscaras, validações e textos | `GuidePixForm.tsx` |
| Frontend — schema Zod | Substituir validações inline por `superRefine` com despacho via `pixKeyConfig` | `GuidePixForm.tsx` |
| Frontend — handler | `onPixKeyTypeChange` com auto-fill e limpeza | `GuidePixForm.tsx` |
| Frontend — submissão | Sanitização com `pixKeyConfig[type].sanitize()` antes da mutation | `GuidePixForm.tsx` |
| tRPC `guides.savePixData` | **Sem alterações** — já recebe `pixKey` limpo (sem máscara) | `server/routers.ts` |
| Schema / Migrations | **Nenhuma alteração necessária** | — |

### Contrato da mutation (inalterado)

```typescript
// Input — guides.savePixData
{
  documentType: "cpf" | "cnpj";
  documentNumber: string;          // somente dígitos, ex: "27298769488"
  pixKeyType: "cpf" | "cnpj" | "email" | "phone" | "random";
  pixKey: string;                  // sanitizado (sem máscara), ex: "11999999999"
  pixKeyHolderName: string;
  acceptedIntermediationTerms: boolean;
  acceptedPayoutTerms: boolean;
  acceptedContestationPolicy: boolean;
}

// Output
{ success: true }
```

### Regras de validação por tipo (resumo)

| pixKeyType | Validação de formato | Sanitização antes de salvar |
|------------|---------------------|-----------------------------|
| `cpf`      | Exatamente 11 dígitos; deve == `documentNumber` | `replace(/\D/g, "")` |
| `cnpj`     | Exatamente 14 dígitos; deve == `documentNumber` | `replace(/\D/g, "")` |
| `email`    | Regex `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` | `trim().toLowerCase()` |
| `phone`    | Exatamente 11 dígitos após remover não-numéricos | `replace(/\D/g, "")` |
| `random`   | Não-vazio (qualquer string) | `trim()` |
