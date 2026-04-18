# US — Atualização da Chave Pix pelo Guia com Auditoria

## Title
**Como guia**, quero poder substituir minha chave Pix cadastrada a qualquer momento, **para que** eu possa corrigir dados incorretos ou migrar para uma chave diferente sem precisar de suporte, garantindo que meus repasses continuem funcionando.

---

## Description

O guia acessa `/guia/configuracoes/pix` e vê o estado atual da sua chave Pix (tipo e titular, nunca o valor bruto). Ao salvar uma nova chave:

1. O sistema valida o novo valor com as mesmas regras de formato e negócio do cadastro inicial (ver US-pix-key-validation).
2. O método de pagamento existente é **substituído** — o registro antigo recebe `archivedAt = NOW()` e um novo registro é criado como `isDefault = true`.
3. O status do novo método começa como `"active"` (validação automática por formato) — **não** exige nova revisão de admin para chave Pix.
4. Payouts já agendados (`status = "scheduled"`) retêm o snapshot da chave antiga e **não são afetados**.
5. Dois registros são criados em `payment_audit_log`: um para o arquivamento do método antigo e um para a criação do novo.
6. O guia recebe confirmação visual no formulário; nenhum e-mail transacional é disparado nessa versão.

---

## Business Value

| # | Valor |
|---|-------|
| 1 | Guias resolvem erros de cadastro de chave Pix sem abrir ticket de suporte, reduzindo volume de atendimento. |
| 2 | Audit trail completo garante rastreabilidade para disputas financeiras e conformidade com normas BACEN/PCI. |
| 3 | Snapshot de chave em payouts agendados evita falhas de repasse em transferências em andamento. |
| 4 | Arquivamento em vez de sobrescrita mantém histórico de métodos anteriores para auditoria retroativa. |

---

## Acceptance Criteria

```gherkin
Feature: Atualização da chave Pix pelo guia com auditoria

  Background:
    Given o guia está autenticado
    And possui um método Pix ativo em guide_payment_methods (isDefault=true, archivedAt=NULL)
    And está em "/guia/configuracoes/pix"

  # ─── Exibição do estado atual ────────────────────────────────────

  Scenario: Formulário exibe dados atuais sem expor o valor da chave
    When o guia abre a página de configuração Pix
    Then o formulário exibe:
      | Campo              | Valor exibido                          |
      | Tipo da chave      | Ex: "CPF"                              |
      | Titular da chave   | Nome do titular (pixKeyHolderName)     |
      | Chave atual        | Valor mascarado: "272.***.***-88"      |
      | Última atualização | Data de createdAt do método ativo      |
    And o valor bruto (pixKey descriptografado) NÃO é retornado pela API

  Scenario: Guia sem chave cadastrada vê formulário vazio
    Given o guia não possui nenhum registro em guide_payment_methods
    When abre a página
    Then o formulário exibe estado vazio (equivalente ao cadastro inicial)
    And não há seção "chave atual"

  # ─── Atualização bem-sucedida ─────────────────────────────────────

  Scenario: Guia substitui chave Pix por nova chave válida
    Given pixKeyType atual é "cpf" com titular "João Silva"
    When o guia seleciona pixKeyType "email"
    And informa pixKey "joao@novaempresa.com.br"
    And informa pixKeyHolderName "João Silva"
    And submete o formulário
    Then o registro antigo recebe archivedAt = NOW() e isDefault = 0
    And um novo registro é criado com:
      | type             | "pix"                       |
      | pixKeyType       | "email"                     |
      | pixKey           | criptografado (AES-256-GCM) |
      | pixKeyHolderName | "João Silva"                |
      | status           | "active"                    |
      | isDefault        | 1                           |
      | archivedAt       | NULL                        |
    And o formulário exibe: "Chave Pix atualizada com sucesso"
    And paymentsEnabled permanece true (novo método ativo imediatamente)

  Scenario: Guia salva chave Pix idêntica à atual
    Given a chave atual é "joao@empresa.com" (email)
    When o guia submete o mesmo valor sem alteração
    Then o sistema detecta que a chave sanitizada é idêntica ao registro ativo atual
    And exibe aviso: "Nenhuma alteração detectada. Dados não foram salvos."
    And nenhum registro é criado/arquivado
    And nenhum evento é gerado em payment_audit_log

  # ─── Impacto em payouts agendados ────────────────────────────────

  Scenario: Payout já agendado usa snapshot da chave anterior
    Given existe um payout com status "scheduled" referenciando paymentMethodId = ID_antigo
    When o guia atualiza sua chave Pix
    Then o payout agendado permanece com paymentMethodId = ID_antigo
    And ao processar, o sistema usa a chave do método arquivado (snapshot)
    And o novo payout gerado após a atualização usa o novo método

  # ─── Audit log ───────────────────────────────────────────────────

  Scenario: Dois eventos registrados em payment_audit_log ao atualizar
    When o guia atualiza a chave Pix com sucesso
    Then exatamente 2 registros são criados em payment_audit_log:

    Registro 1 — arquivamento do método antigo:
      | entityType    | "guide_payment_method"               |
      | entityId      | ID do método arquivado               |
      | action        | "payment_method_archived"            |
      | actorId       | ID do guia                           |
      | actorType     | "guide"                              |
      | previousValue | { type, pixKeyType, maskedPixKey }   |
      | newValue      | { archivedAt: <timestamp> }          |
      | ipAddress     | IP da requisição                     |

    Registro 2 — criação do novo método:
      | entityType    | "guide_payment_method"               |
      | entityId      | ID do novo método                    |
      | action        | "payment_method_created"             |
      | actorId       | ID do guia                           |
      | actorType     | "guide"                              |
      | previousValue | NULL                                 |
      | newValue      | { type, pixKeyType, maskedPixKey }   |
      | ipAddress     | IP da requisição                     |

  Scenario: Valor bruto da chave nunca aparece no audit log
    When o guia atualiza a chave Pix
    Then todos os registros de payment_audit_log com action contendo "payment_method"
    E o campo payload/previousValue/newValue NÃO contém pixKey descriptografado
    And contém apenas maskedPixKey (ex: "joao@***.com.br" para email, "272.***.***-88" para CPF)

  # ─── Validações (reutilizadas do cadastro inicial) ────────────────

  Scenario: Nova chave com formato inválido é rejeitada
    Given pixKeyType "phone"
    When pixKey "11 8888-7777" (telefone fixo — não celular)
    Then o sistema rejeita com erro "pix_key_phone_mobile"
    And nenhum registro é criado/arquivado
    And nenhum evento é gerado no audit log

  Scenario: Tentativa de bypass via chamada direta à API
    Given uma requisição direta à mutation "guides.updatePaymentMethod"
    With pixKeyType "cpf" e pixKey com dígitos verificadores inválidos
    Then a API retorna BAD_REQUEST: "pix_key_invalid_cpf"
    And nenhuma operação de banco é executada

  # ─── Rate limiting ───────────────────────────────────────────────

  Scenario: Guia tenta atualizar a chave mais de 5 vezes em 24h
    Given o guia já realizou 5 atualizações de método Pix nas últimas 24 horas
    When tenta uma 6ª atualização
    Then a mutation retorna TOO_MANY_REQUESTS: "pix_update_rate_limit_exceeded"
    And o formulário exibe: "Limite de atualizações atingido. Tente novamente em 24 horas."
    And nenhum registro é criado/arquivado
```

---

## Technical Notes

### 1 — Mutation `guides.updatePaymentMethod`

Operação atômica em transação de banco. Nenhuma etapa pode ser parcial:

```typescript
// server/routers.ts

guides.updatePaymentMethod = guideProcedure
  .input(z.object({
    pixKeyType: z.enum(["cpf","cnpj","email","phone","random"]),
    pixKey: z.string().min(1),
    pixKeyHolderName: z.string().min(3),
    documentNumber: z.string(),
  }))
  .mutation(async ({ ctx, input }) => {
    // 1. Validação de formato e negócio (shared/lib/pixKeyValidation.ts)
    const validation = validatePixKey(input.pixKeyType, input.pixKey, input.documentNumber);
    if (!validation.valid) {
      throw new TRPCError({ code: "BAD_REQUEST", message: validation.code });
    }

    // 2. Rate limit: máx 5 atualizações em 24h
    const recentUpdates = await db.countRecentPaymentMethodUpdates(ctx.user.id, 24);
    if (recentUpdates >= 5) {
      throw new TRPCError({ code: "TOO_MANY_REQUESTS", message: "pix_update_rate_limit_exceeded" });
    }

    // 3. Carregar método atual para comparação e audit
    const current = await db.getDefaultPaymentMethod(ctx.user.id);

    // 4. Detectar ausência de mudança real
    const sanitized = pixKeyConfig[input.pixKeyType].sanitize(input.pixKey);
    const currentDecrypted = current ? await decrypt(current.pixKey) : null;
    if (current && currentDecrypted === sanitized && current.pixKeyType === input.pixKeyType) {
      return { changed: false };
    }

    // 5. Transação: arquivar antigo + criar novo + audit
    await db.transaction(async (tx) => {
      const ip = ctx.req.ip ?? "unknown";
      const maskedNew = maskPixKey(input.pixKeyType, sanitized);

      if (current) {
        const maskedOld = maskPixKey(current.pixKeyType!, await decrypt(current.pixKey!));
        await tx.archivePaymentMethod(current.id);
        await tx.createAuditLog({
          entityType: "guide_payment_method",
          entityId: String(current.id),
          action: "payment_method_archived",
          actorId: String(ctx.user.id),
          actorType: "guide",
          previousValue: JSON.stringify({ type: current.type, pixKeyType: current.pixKeyType, maskedPixKey: maskedOld }),
          newValue: JSON.stringify({ archivedAt: new Date().toISOString() }),
          ipAddress: ip,
        });
      }

      const newId = await tx.createPaymentMethod({
        guideId: ctx.user.id,
        type: "pix",
        pixKeyType: input.pixKeyType,
        pixKey: await encrypt(sanitized),
        pixKeyHolderName: input.pixKeyHolderName,
        pixKeyDocument: await encrypt(input.documentNumber.replace(/\D/g, "")),
        status: "active",
        isDefault: 1,
      });

      await tx.createAuditLog({
        entityType: "guide_payment_method",
        entityId: String(newId),
        action: "payment_method_created",
        actorId: String(ctx.user.id),
        actorType: "guide",
        previousValue: null,
        newValue: JSON.stringify({ type: "pix", pixKeyType: input.pixKeyType, maskedPixKey: maskedNew }),
        ipAddress: ip,
      });
    });

    return { changed: true };
  });
```

### 2 — Função de mascaramento (`maskPixKey`)

O valor mascarado é o único que pode aparecer em logs, audit trail e respostas de API. Nunca o valor bruto:

```typescript
// server/lib/pixKeyMask.ts

export function maskPixKey(type: PixKeyType, value: string): string {
  switch (type) {
    case "cpf":
      // "27298769488" → "272.***.***-88"
      return `${value.slice(0,3)}.***.***-${value.slice(-2)}`;
    case "cnpj":
      // "11222333000181" → "11.***.***/0001-81"
      return `${value.slice(0,2)}.***.***/****-${value.slice(-2)}`;
    case "email": {
      const [local, domain] = value.split("@");
      const tld = domain.split(".").slice(-1)[0];
      return `${local.slice(0,4)}@***.${tld}`;
    }
    case "phone":
      // "+5511999999999" → "+55 (11) *****-9999"
      return `+55 (${value.slice(3,5)}) *****-${value.slice(-4)}`;
    case "random":
      // UUID: mostrar apenas primeiros e últimos 4 chars
      return `${value.slice(0,8)}-****-****-****-${value.slice(-4)}`;
  }
}
```

### 3 — Snapshot de chave em payouts agendados

`payouts` já referencia `pixKey` diretamente (campo varchar na tabela). A lógica atual em `payouts.processScheduled` deve continuar usando o `pixKey` snapshottado no momento do agendamento — **não** buscar o método atual do guia no momento do processamento:

```typescript
// Correto — usa snapshot
const payout = await db.getPayoutById(id);
const pixKey = await decrypt(payout.pixKey); // chave salva no momento do agendamento

// Incorreto — não fazer isso
const method = await db.getDefaultPaymentMethod(guideId); // buscaria a chave nova
```

Se `payouts` ainda não persiste `pixKey` como snapshot (usa referência via `guideId`), a migration deve adicionar o snapshot como parte desta US antes de habilitar atualizações de chave.

### 4 — Rate limiting via `payment_audit_log`

Usar a tabela existente para calcular o limite sem nova tabela:

```typescript
// server/db.ts

async function countRecentPaymentMethodUpdates(guideId: number, hours: number): Promise<number> {
  const since = new Date(Date.now() - hours * 60 * 60 * 1000);
  return db
    .select({ count: count() })
    .from(paymentAuditLog)
    .where(and(
      eq(paymentAuditLog.actorId, String(guideId)),
      eq(paymentAuditLog.action, "payment_method_created"),
      gte(paymentAuditLog.createdAt, since)
    ))
    .then(r => r[0].count);
}
```

### 5 — Resposta de API — `guides.getMyPaymentMethods` (campo `maskedPixKey`)

Adicionar `maskedPixKey` ao retorno da query existente. O campo é calculado server-side na camada de resposta, nunca na camada de banco:

```typescript
const methods = await db.listGuidePaymentMethods(ctx.user.id);
return methods.map(m => ({
  id: m.id,
  type: m.type,
  status: m.status,
  isDefault: m.isDefault === 1,
  pixKeyType: m.pixKeyType,
  pixKeyHolderName: m.pixKeyHolderName,
  maskedPixKey: m.pixKey
    ? maskPixKey(m.pixKeyType!, await decrypt(m.pixKey))
    : null,
  createdAt: m.createdAt,
}));
// pixKey (ciphertext) e pixKeyDocument NUNCA presentes na resposta
```

---

## API / Data Impact

| Camada | Mudança | Arquivo |
|--------|---------|---------|
| tRPC — nova mutation | `guides.updatePaymentMethod` (transação: archive + create + 2x audit) | `server/routers.ts` |
| tRPC — query atualizada | `guides.getMyPaymentMethods` adiciona campo `maskedPixKey` | `server/routers.ts` |
| Nova função utilitária | `maskPixKey(type, value)` | `server/lib/pixKeyMask.ts` |
| `server/db.ts` | `countRecentPaymentMethodUpdates(guideId, hours)` para rate limiting | `server/db.ts` |
| `payouts` (verificar) | Confirmar que `pixKey` é snapshottado no momento do agendamento (não por referência) | `drizzle/schema.ts` |
| Frontend — formulário | Exibir `maskedPixKey` + data da última atualização; botão "Atualizar chave" abre modo de edição | `GuidePaymentMethodForm.tsx` |
| Schema / Migrations | Nenhuma nova coluna — se `payouts.pixKey` já é snapshot, zero migrations | — |

### Novos error codes tRPC

| Code | Message | Cenário |
|------|---------|---------|
| `BAD_REQUEST` | `pix_key_*` | Validação de formato/negócio (reusa US-pix-key-validation) |
| `TOO_MANY_REQUESTS` | `pix_update_rate_limit_exceeded` | > 5 atualizações em 24h |

### Ações no `payment_audit_log` (novos valores de `action`)

| `action` | Disparado por | `entityType` |
|---|---|---|
| `payment_method_archived` | `guides.updatePaymentMethod` (método antigo) | `guide_payment_method` |
| `payment_method_created` | `guides.updatePaymentMethod` (método novo) | `guide_payment_method` |

> Os eventos `payment_method_archived` também servem para calcular o rate limit — evita tabela separada de controle.
