# US — Coleta da Chave Pix no Cadastro do Guia

## Title
**Como guia**, quero cadastrar minha chave Pix durante o onboarding, **para que** o Trekko possa me repassar os pagamentos das expedições sem fricção adicional após a conclusão de cada trilha.

---

## Description

Durante o fluxo de ativação da conta de guia — após a validação do CADASTUR e criação de credenciais — o sistema deve apresentar uma etapa obrigatória de configuração da chave Pix. Enquanto essa etapa não for concluída, o guia **não pode receber pagamentos**: tentativas de reserva em suas expedições são bloqueadas com mensagem informativa ao trekker.

O guia pode escolher entre cinco tipos de chave Pix (CPF, CNPJ, e-mail, telefone, chave aleatória). Para chaves do tipo CPF/CNPJ, o sistema valida que a chave pertence ao mesmo documento registrado. Todos os dados sensíveis são armazenados com criptografia AES-256-GCM.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Elimina atrasos de repasse causados por guias que não configuram o Pix pós-registro. |
| 2 | Reduz volume de tickets de suporte relacionados a "não recebi meu pagamento". |
| 3 | Garante conformidade com o fluxo de pagamentos intermediados (Mercado Pago → Pix). |
| 4 | Aumenta a taxa de ativação de guias (do cadastro à primeira expedição publicada). |

---

## Acceptance Criteria

```gherkin
Feature: Coleta da chave Pix no cadastro do guia

  Background:
    Given o guia já validou seu número CADASTUR
    And criou suas credenciais de acesso (e-mail + senha)
    And está autenticado na plataforma

  # ─── Onboarding ────────────────────────────────────────────────

  Scenario: Guia acessa dashboard sem chave Pix configurada
    Given o campo "pixKeyVerified" em "guide_verification" é 0 ou não existe
    When o guia acessa o dashboard "/guia"
    Then o sistema exibe um banner de aviso: "Configure sua chave Pix para começar a receber pagamentos"
    And o banner contém um CTA que redireciona para "/guia/configuracoes/pix"

  Scenario: Guia salva chave Pix do tipo CPF com sucesso
    Given o guia seleciona documentType "CPF"
    And informa documentNumber "272.987.694-88"
    And seleciona pixKeyType "cpf"
    And informa pixKey "272.987.694-88"
    And informa pixKeyHolderName "João da Silva"
    And aceita os três termos obrigatórios
    When submete o formulário
    Then "guide_verification.pixKeyVerified" é atualizado para 1
    And "guide_verification.pixKey" é armazenado criptografado (AES-256-GCM)
    And o sistema registra um evento em "payment_audit_log" com action "pix_key_saved"
    And o guia vê a mensagem: "Dados PIX salvos com sucesso"
    And o banner de aviso desaparece do dashboard

  Scenario: Guia salva chave Pix do tipo e-mail
    Given o guia seleciona pixKeyType "email"
    And informa pixKey "joao@email.com"
    When submete o formulário com documento e termos preenchidos
    Then o sistema salva a chave sem validação cruzada com documentNumber
    And "guide_verification.pixKeyVerified" é 1

  Scenario: Guia salva chave Pix do tipo telefone
    Given o guia seleciona pixKeyType "phone"
    And informa pixKey "(11) 99999-9999"
    When submete o formulário
    Then o sistema armazena apenas os 11 dígitos numéricos
    And "guide_verification.pixKeyVerified" é 1

  Scenario: Guia salva chave Pix do tipo chave aleatória
    Given o guia seleciona pixKeyType "random"
    And informa pixKey "123e4567-e89b-12d3-a456-426614174000"
    When submete o formulário
    Then nenhuma validação de formato é aplicada além de campo não-vazio
    And "guide_verification.pixKeyVerified" é 1

  # ─── Validações ────────────────────────────────────────────────

  Scenario: Chave Pix CPF não bate com o documento cadastrado
    Given o guia selecionou documentType "CPF" e documentNumber "272.987.694-88"
    And selecionou pixKeyType "cpf"
    When informa pixKey "111.111.111-11" (diferente do documentNumber)
    And tenta submeter
    Then o sistema exibe: "Chave PIX deve pertencer ao mesmo CPF/CNPJ cadastrado"
    And o formulário não é submetido

  Scenario: Chave Pix CNPJ não bate com o documento cadastrado
    Given o guia selecionou documentType "CNPJ" e documentNumber "12.345.678/0001-95"
    And selecionou pixKeyType "cnpj"
    When informa pixKey "99.999.999/0001-00"
    And tenta submeter
    Then o sistema exibe: "Chave PIX deve pertencer ao mesmo CPF/CNPJ cadastrado"

  Scenario: Submissão sem aceitar todos os termos
    Given o guia preencheu todos os campos corretamente
    And não marcou "acceptedContestationPolicy"
    When tenta submeter
    Then o botão "Salvar Dados PIX" permanece desabilitado

  # ─── Bloqueio de Pagamentos ─────────────────────────────────────

  Scenario: Trekker tenta pagar expedição de guia sem Pix configurado
    Given o guia da expedição tem "pixKeyVerified" = 0
    When um trekker inicia o checkout de uma reserva nessa expedição
    Then a mutation "expeditions.enrollUser" retorna erro PRECONDITION_FAILED
    And o frontend exibe: "Este guia ainda não configurou o recebimento de pagamentos. Tente novamente em breve."
    And nenhuma reserva é criada no banco

  Scenario: Trekker realiza reserva normalmente após guia configurar Pix
    Given o guia configurou sua chave Pix ("pixKeyVerified" = 1)
    When um trekker inicia o checkout
    Then a reserva é criada normalmente com status "created"
    And o fluxo de pagamento prossegue via Mercado Pago
```

---

## Technical Notes

### 1 — Gate de Pagamento (`expeditions.enrollUser`)
Adicionar verificação no início da mutation, **antes** de criar o registro de reserva:

```typescript
// server/routers.ts — expeditions.enrollUser
const verification = await db.getGuideVerification(expedition.guideId);
if (!verification || verification.pixKeyVerified !== 1) {
  throw new TRPCError({
    code: "PRECONDITION_FAILED",
    message: "guide_pix_not_configured",
  });
}
```

O cliente deve mapear o código `"guide_pix_not_configured"` para a mensagem localizada em pt-BR.

### 2 — Banner no Dashboard do Guia
Em `client/src/pages/GuiaDashboard.tsx` (ou equivalente), buscar o status via `guides.getMyVerification`:

```typescript
const { data: verification } = trpc.guides.getMyVerification.useQuery();
const pixPending = !verification?.pixKeyVerified;
```

Renderizar `<CalloutBanner>` condicionalmente com CTA para `/guia/configuracoes/pix`.

### 3 — Rota de Configuração
- **Rota:** `/guia/configuracoes/pix`
- **Componente:** Reusar `GuidePixForm.tsx` (já implementado) — nenhuma alteração necessária no componente.
- Caso `pixKeyVerified = 1`, exibir estado de "Chave Pix já configurada" com opção de editar.

### 4 — Audit Log
Em `db.saveGuidePixData`, após salvar, registrar em `payment_audit_log`:

```typescript
await db.createAuditLog({
  entityType: "guide_verification",
  entityId: String(userId),
  action: "pix_key_saved",
  actorId: String(userId),
  actorType: "guide",
  newValue: pixKeyType, // não logar a chave em si
});
```

### 5 — Sem Alterações de Schema
Todos os campos necessários já existem em `guide_verification`:
`pixKeyType`, `pixKey` (encrypted), `pixKeyDocument` (encrypted), `pixKeyHolderName`, `pixKeyVerified`.
**Nenhuma migration é necessária.**

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|--------|---------|---------|
| tRPC mutation | Adicionar guard `pixKeyVerified` em `expeditions.enrollUser` | `server/routers.ts` |
| tRPC query | `guides.getMyVerification` já existe — nenhuma alteração | `server/routers.ts` |
| Audit log | Registrar evento `pix_key_saved` em `db.saveGuidePixData` | `server/db.ts` |
| Frontend route | Nova rota `/guia/configuracoes/pix` com `GuidePixForm` | `client/src/pages/` |
| Frontend dashboard | Banner condicional quando `pixKeyVerified = 0` | `client/src/pages/GuiaDashboard.tsx` |
| Schema / Migrations | **Nenhuma alteração necessária** | — |

### Error Codes (tRPC)

| Code | Message key | Descrição |
|------|-------------|-----------|
| `PRECONDITION_FAILED` | `guide_pix_not_configured` | Guia sem Pix — bloqueia reserva |

### Encryption
Todos os campos sensíveis (`pixKey`, `documentNumber`, `pixKeyDocument`) continuam criptografados via AES-256-GCM (`server/lib/crypto.ts`) conforme padrão DB-SEC-01 já em produção.
