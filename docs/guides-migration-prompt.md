# Trekko — Prompt de Migração de Guias (Atualização do Banco de Dados)

> **Destinatário:** Engenheiro sênior de dados / desenvolvedor full-stack responsável pela migração
> **Escopo:** Atualização segura do banco de guias do Trekko a partir de um novo arquivo de guias cadasturados
> **Stack:** MySQL 8 · Drizzle ORM · Node.js · Dados estáticos servidos via GitHub Pages (`data/guides.json`)

---

## 1. Contexto e arquitetura atual

### 1.1 Fontes de dados de guias no Trekko

O Trekko mantém **três camadas de dados** para guias:

| Camada | Tabela / Arquivo | Descrição |
|--------|-----------------|-----------|
| Registro oficial | `cadastur_registry` (MySQL) | Importado do CSV do CADASTUR (Ministério do Turismo). 50.242 registros. Chave única: `certificateNumber`. |
| Perfil Trekko | `guide_profiles` (MySQL) | Gerado quando o guia cria conta no Trekko. Vincula `userId` → `cadasturNumber`. |
| Verificação | `guide_verification` (MySQL) | CPF/CNPJ, chave Pix (criptografados), status de aprovação. |
| Dados públicos | `data/guides.json` | Exportação estática gerada por `scripts/export-guides-static.ts`. Servido via GitHub Pages. |

**Regra fundamental:** a tabela `cadastur_registry` é a fonte de verdade para dados brutos de guias. O arquivo `data/guides.json` é derivado dela e deve ser regerado após qualquer importação.

### 1.2 Estrutura da tabela `cadastur_registry`

```sql
CREATE TABLE cadastur_registry (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  certificateNumber VARCHAR(64) UNIQUE NOT NULL,  -- identificador único de deduplicação
  fullName         VARCHAR(256),
  uf               VARCHAR(2),
  city             VARCHAR(128),
  phone            VARCHAR(32),
  email            VARCHAR(320),
  website          TEXT,
  validUntil       TIMESTAMP NULL,
  languages        JSON,           -- ex: ["Português", "Inglês"]
  operatingCities  JSON,           -- ex: ["Petrópolis", "Teresópolis"]
  categories       JSON,           -- ex: ["Guia Regional", "Atrativo Natural"]
  segments         JSON,
  isDriverGuide    INT DEFAULT 0,  -- 0 ou 1
  phoneMasked      VARCHAR(20),    -- exibição pública
  emailMasked      VARCHAR(255),   -- exibição pública
  importedAt       TIMESTAMP,
  createdAt        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updatedAt        TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 1.3 Campos que NÃO devem ser sobrescritos

Os seguintes dados pertencem ao perfil Trekko do guia e nunca devem ser substituídos pela importação:

- `users`: `bio`, `photoUrl`, `passwordHash`, `cadasturValidated`, `role`
- `guide_profiles`: descrição, fotos, associações de trilhas
- `guide_verification`: `pixKey`, `pixKeyType`, `documentNumber`, `status`, `reviewedBy`
- `reviews`: avaliações e comentários de trekkers
- `reservations`: histórico de reservas
- `expeditions`: expedições criadas pelo guia

---

## 2. Pré-requisitos e checklist de segurança

### 2.1 Antes de qualquer modificação

```bash
# 1. Confirme o ambiente
echo $NODE_ENV           # deve ser "development" ou "staging", NUNCA "production" na primeira execução
echo $DATABASE_URL       # confirme o host antes de agir

# 2. Backup completo da tabela cadastur_registry
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME cadastur_registry \
  > backups/cadastur_registry_$(date +%Y%m%d_%H%M%S).sql

# 3. Backup do arquivo estático atual
cp data/guides.json backups/guides_$(date +%Y%m%d_%H%M%S).json

# 4. Confirme contagem atual
mysql -e "SELECT COUNT(*) as total FROM cadastur_registry;" $DB_NAME
# Esperado: ~50.242 linhas
```

### 2.2 Verifique o arquivo de entrada

Antes de executar qualquer script, inspecione o arquivo recebido:

- Formatos aceitos: CSV (delimitado por `;` ou `,`), XLSX, JSON
- Se for XLSX: converta para CSV usando `xlsx2csv` ou `python -m xlsx2csv`
- Se tiver múltiplas abas: processe cada aba separadamente; verifique se representam guias distintos ou dados complementares

```bash
# Para CSV: verifique o cabeçalho e primeiras linhas
head -3 novo_arquivo.csv

# Para XLSX: liste abas
python3 -c "import openpyxl; wb=openpyxl.load_workbook('arquivo.xlsx'); print(wb.sheetnames)"
```

---

## 3. Etapa 1 — Análise e normalização do arquivo recebido

### 3.1 Mapeamento de colunas esperadas

O script de importação (`scripts/import-cadastur.mjs`) espera os seguintes campos no CSV de origem. Mapeie as colunas do arquivo recebido para estes nomes antes de processar:

| Campo esperado | Sinônimos comuns | Obrigatório |
|---------------|-----------------|-------------|
| `certificateNumber` | Número Cadastur, Certif., Nº Cadastur | **Sim** — chave de deduplicação |
| `fullName` | Nome, Nome completo, Razão Social | **Sim** |
| `uf` | UF, Estado, Sigla | **Sim** |
| `city` | Município, Cidade | **Sim** |
| `phone` | Telefone, Celular, Fone | Não |
| `email` | E-mail | Não |
| `website` | Site, URL | Não |
| `validUntil` | Validade, Data de Validade | Não |
| `categories` | Tipo de Atividade, Categoria | Não |
| `languages` | Idiomas | Não |
| `operatingCities` | Cidades de Atuação | Não |
| `segments` | Segmentos | Não |
| `isDriverGuide` | Guia Motorista, Driver | Não |

### 3.2 Regras de normalização obrigatórias

Aplique estas transformações **antes** de qualquer comparação ou inserção:

```javascript
// Número Cadastur — remover todos os não-dígitos (pontos, traços, barras)
function normalizeCadastur(raw) {
  return String(raw ?? '').replace(/\D/g, '');
}

// UF — uppercase, trim, valide contra lista de 27 estados
const VALID_UFS = new Set([
  'AC','AL','AP','AM','BA','CE','DF','ES','GO',
  'MA','MT','MS','MG','PA','PB','PR','PE','PI',
  'RJ','RN','RS','RO','RR','SC','SP','SE','TO'
]);
function normalizeUF(raw) {
  const uf = String(raw ?? '').trim().toUpperCase();
  return VALID_UFS.has(uf) ? uf : null; // null = inválido, sinalize para revisão
}

// Cidade — title case + trim + remover pontuação dupla
function normalizeCity(raw) {
  return String(raw ?? '')
    .trim()
    .replace(/\s+/g, ' ')
    .replace(/[.,]{2,}/g, '.')
    .replace(/\b(\w)/g, c => c.toUpperCase());
}

// Email — lowercase + trim
function normalizeEmail(raw) {
  return String(raw ?? '').trim().toLowerCase() || null;
}

// Telefone — formato brasileiro (XX)XXXXX-XXXX
function normalizePhone(raw) {
  const digits = String(raw ?? '').replace(/\D/g, '');
  if (digits.length === 11) return `(${digits.slice(0,2)})${digits.slice(2,7)}-${digits.slice(7)}`;
  if (digits.length === 10) return `(${digits.slice(0,2)})${digits.slice(2,6)}-${digits.slice(6)}`;
  return raw || null; // mantém original se formato não reconhecido
}

// Nome — uppercase + trim (padrão CADASTUR usa maiúsculas)
function normalizeName(raw) {
  return String(raw ?? '').trim().toUpperCase().replace(/\s+/g, ' ');
}

// Data — converta para ISO 8601 (YYYY-MM-DD)
function normalizeDate(raw) {
  if (!raw) return null;
  // Formatos comuns: DD/MM/YYYY, YYYY-MM-DD, MM/DD/YYYY
  const br = String(raw).match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  if (br) return `${br[3]}-${br[2]}-${br[1]}`;
  const iso = String(raw).match(/^\d{4}-\d{2}-\d{2}/);
  if (iso) return iso[0];
  return null;
}

// Arrays pipe-separated (padrão CADASTUR) → array JS
function normalizeArray(raw) {
  if (!raw) return [];
  if (Array.isArray(raw)) return raw.map(s => String(s).trim()).filter(Boolean);
  return String(raw).split('|').map(s => s.trim()).filter(Boolean);
}
```

### 3.3 Validação de chave Pix (se presente no arquivo)

```javascript
function validatePixKey(key) {
  if (!key) return { valid: false, type: null };
  const k = String(key).trim();
  const cpf  = /^\d{11}$/.test(k.replace(/\D/g,'')) && k.replace(/\D/g,'').length === 11;
  const cnpj = /^\d{14}$/.test(k.replace(/\D/g,''));
  const email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(k);
  const phone = /^\+55\d{10,11}$/.test(k);
  const uuid  = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(k);
  if (cpf)   return { valid: true, type: 'CPF' };
  if (cnpj)  return { valid: true, type: 'CNPJ' };
  if (email) return { valid: true, type: 'email' };
  if (phone) return { valid: true, type: 'phone' };
  if (uuid)  return { valid: true, type: 'random' };
  return { valid: false, type: null };
}
// Nota: Pix NÃO é armazenado em cadastur_registry. Se o arquivo contiver chave Pix,
// armazene-a em guide_verification (campo pixKey, criptografado com DB_ENCRYPTION_KEY).
```

---

## 4. Etapa 2 — Deduplicação: comparação com o banco atual

### 4.1 Critério primário (obrigatório)

O campo `certificateNumber` (número Cadastur normalizado, somente dígitos) é a **única chave confiável de deduplicação** para `cadastur_registry`. Não use nome + cidade como critério primário — nomes podem ter variações ortográficas.

```sql
-- Antes do import: carregue os números existentes em memória para comparação rápida
SELECT certificateNumber FROM cadastur_registry;
-- ~50.242 registros; carregue em um Set para lookup O(1)
```

### 4.2 Critérios secundários (usados apenas quando `certificateNumber` ausente)

Se o arquivo recebido não contiver número Cadastur para algum registro, aplique os critérios abaixo **em ordem de confiabilidade**:

1. Email exato (após normalização lowercase)
2. Telefone exato (após normalização de dígitos)
3. Nome completo normalizado + UF + Cidade

Se nenhum critério confirmar duplicata, trate como **novo registro** e sinalize o campo `certificateNumber` como ausente para revisão manual.

> **Atenção:** Nunca assuma duplicata apenas por nome similar. Guias com nomes parecidos podem ser pessoas distintas.

### 4.3 Lógica de decisão por registro

```
Para cada guia no arquivo recebido:
  ├─ certificateNumber existe e está no banco?
  │   ├─ SIM → Caso "Atualização" (Etapa 3B)
  │   └─ NÃO → Caso "Novo registro" (Etapa 3A)
  │
  └─ certificateNumber ausente?
      ├─ Match por email/telefone/nome+uf+cidade?
      │   ├─ SIM → Caso "Atualização" (Etapa 3B) — documente a correspondência usada
      │   └─ NÃO → Caso "Novo registro sem Cadastur" — flag: requer revisão manual
      └─ Múltiplos matches? → flag: ambíguo — NÃO importe, adicione à lista de revisão
```

---

## 5. Etapa 3A — Inserção de novos guias

### 5.1 Script de inserção (idempotente)

O script `scripts/import-cadastur.mjs` existente usa `ON DUPLICATE KEY UPDATE` — este é o padrão correto. Estenda-o ou crie um novo script seguindo este modelo:

```javascript
// scripts/import-guides-update.mjs
import mysql from 'mysql2/promise';
import { readFileSync } from 'fs';

const INSERT_SQL = `
  INSERT INTO cadastur_registry
    (certificateNumber, fullName, uf, city, phone, email, website,
     validUntil, languages, operatingCities, categories, segments,
     isDriverGuide, phoneMasked, emailMasked, importedAt)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
  ON DUPLICATE KEY UPDATE
    -- Atualiza apenas campos que estavam vazios ou são mais recentes
    fullName         = IF(fullName IS NULL OR fullName = '', VALUES(fullName), fullName),
    phone            = IF(phone IS NULL OR phone = '', VALUES(phone), phone),
    email            = IF(email IS NULL OR email = '', VALUES(email), email),
    website          = IF(website IS NULL OR website = '', VALUES(website), website),
    validUntil       = IF(VALUES(validUntil) > validUntil, VALUES(validUntil), validUntil),
    languages        = IF(JSON_LENGTH(languages) = 0, VALUES(languages), languages),
    operatingCities  = IF(JSON_LENGTH(operatingCities) = 0, VALUES(operatingCities), operatingCities),
    categories       = IF(JSON_LENGTH(categories) = 0, VALUES(categories), categories),
    phoneMasked      = IF(phoneMasked IS NULL, VALUES(phoneMasked), phoneMasked),
    emailMasked      = IF(emailMasked IS NULL, VALUES(emailMasked), emailMasked),
    importedAt       = NOW(),
    updatedAt        = NOW()
`;

function maskPhone(phone) {
  if (!phone) return null;
  return phone.replace(/(\(\d{2}\))(\d+)(\d{4})/, '$1****$3');
}

function maskEmail(email) {
  if (!email) return null;
  const [user, domain] = email.split('@');
  return user.slice(0, 2) + '***@' + domain;
}
```

### 5.2 Status inicial para novos guias

Novos registros importados do CADASTUR entram como dados do registro oficial. O "status ativo" no Trekko é controlado pela tabela `users` (campo `cadasturValidated`), que só existe quando o guia **cria uma conta**. Portanto:

- Guias importados para `cadastur_registry` ficam disponíveis para busca pública imediatamente via `guides.json`
- Eles **não** têm conta Trekko até se cadastrarem — não crie registros em `users` automaticamente
- Se `validUntil < NOW()`: marque o guia como **expirado** — não bloqueie a importação, mas registre no relatório
- Se `validUntil IS NULL`: importe normalmente — validade desconhecida não é motivo para bloquear

---

## 6. Etapa 3B — Atualização de guias existentes

### 6.1 Regra de não-sobrescrita

A cláusula `ON DUPLICATE KEY UPDATE` acima já implementa a regra correta:

| Campo | Política |
|-------|---------|
| `fullName` | Atualiza se estava vazio; preserva se já preenchido |
| `phone`, `email`, `website` | Atualiza se estava vazio; preserva se já preenchido |
| `validUntil` | Atualiza apenas se a nova data é **mais recente** |
| `languages`, `categories`, `operatingCities`, `segments` | Atualiza se array estava vazio |
| `city`, `uf` | **Nunca sobrescreve** — UF e cidade são dados geográficos sensíveis ao perfil |
| Qualquer campo de `users`, `guide_profiles`, `guide_verification` | **Jamais toque nessas tabelas durante o import** |

### 6.2 Dados de usuário que nunca devem ser alterados

```sql
-- Estes campos estão fora do escopo do import e NÃO devem ser modificados:
-- users.bio, users.photoUrl, users.passwordHash, users.cadasturValidated
-- guide_profiles.* (todo o perfil Trekko do guia)
-- guide_verification.pixKey, guide_verification.status
-- reviews.*, reservations.*, expeditions.*
```

---

## 7. Etapa 4 — Associação de guias com trilhas

### 7.1 Trilhas disponíveis no Trekko (referência)

```
ID  UF  Cidade          Nome da Trilha
 1  RR  (Roraima)       Monte Roraima
 2  RJ  Petrópolis/Teresópolis  Travessia Petrópolis x Teresópolis
 3  GO  (Goiás)         Vale da Lua e Cachoeiras
 4  SP  São Bento do Sapucaí    Pedra do Baú
 5  MG  Caparaó        Pico da Bandeira
 6  RS  Cambará do Sul  Cânion Itaimbezinho
 7  SC  (Santa Catarina) Trilha das Praias
 8  MG  (Minas Gerais)  Travessia Serra Fina
 9  MA  (Maranhão)      Travessia Lençóis Maranhenses
10  PR  Tibagi          Cânion do Guartelá
11  BA  Andaraí         Travessia Vale do Pati
12  MT  (Mato Grosso)   Morro de São Jerônimo
```

### 7.2 Lógica de associação permitida

A associação guia ↔ trilha é feita na tabela `guide_profiles.operatingCities` ou via expedições. **Não crie associações inventadas.**

Critério permitido:
```
guia.uf === trilha.uf
  E (guia.city === trilha.city OU guia.operatingCities.includes(trilha.city))
```

Se o critério acima for atendido, você pode **sugerir** a associação no relatório final — mas **não a insira automaticamente** em `guide_profiles` sem aprovação humana.

---

## 8. Execução do script de migração

### 8.1 Ordem de execução

```bash
# PASSO 1: Backup (obrigatório)
mysqldump -u $DB_USER -p $DB_NAME cadastur_registry \
  > backups/cadastur_registry_pre_import_$(date +%Y%m%d_%H%M%S).sql

cp data/guides.json backups/guides_pre_import_$(date +%Y%m%d_%H%M%S).json

# PASSO 2: Converter arquivo se necessário (XLSX → CSV)
# python3 -m xlsx2csv -a arquivo.xlsx output_dir/

# PASSO 3: Executar o script de análise (dry-run)
node scripts/import-guides-update.mjs --file novo_arquivo.csv --dry-run

# PASSO 4: Revisar o relatório de dry-run antes de prosseguir
# Verifique: novos, atualizados, duplicatas, erros de validação

# PASSO 5: Executar a importação real
node scripts/import-guides-update.mjs --file novo_arquivo.csv

# PASSO 6: Verificar contagem pós-import
mysql -e "SELECT COUNT(*) FROM cadastur_registry;" $DB_NAME

# PASSO 7: Regenerar o arquivo estático
pnpm tsx scripts/export-guides-static.ts
# Verifica: wc -l data/guides.json

# PASSO 8: Commit e deploy (somente após validação)
git add data/guides.json
git commit -m "data: atualiza guides.json com novos guias CADASTUR — [data]"
git push -u origin claude/trekko-migration-guide-QrNMC
```

### 8.2 Rollback em caso de erro

```bash
# Se algo der errado, restaure o backup:
mysql -u $DB_USER -p $DB_NAME < backups/cadastur_registry_pre_import_YYYYMMDD_HHMMSS.sql
cp backups/guides_pre_import_YYYYMMDD_HHMMSS.json data/guides.json
```

### 8.3 Transação MySQL para segurança adicional

Envolva o insert em uma transação:

```sql
START TRANSACTION;

-- Execute todos os INSERTs/UPDATEs aqui

-- Verifique se a contagem faz sentido antes de confirmar:
SELECT COUNT(*) FROM cadastur_registry;
-- Se OK:
COMMIT;
-- Se não:
ROLLBACK;
```

---

## 9. Qualidade de dados — regras adicionais

### 9.1 Registros que devem ir para a lista de revisão manual

Um registro é marcado como `REQUER_REVISÃO` e **não** importado automaticamente se:

- `certificateNumber` ausente E nenhum critério secundário identifica o guia com certeza
- `uf` inválido (não está nos 27 estados brasileiros)
- `fullName` vazio ou com menos de 3 caracteres
- `email` com formato inválido (ex: sem `@`, sem domínio)
- Múltiplos registros no arquivo com o mesmo `certificateNumber` — sinalize como duplicata interna no arquivo

### 9.2 Registros aceitos com flag `INCOMPLETO`

Aceite mas sinalize os seguintes casos:

- `phone` ausente ou com menos de 8 dígitos
- `email` ausente
- `validUntil` no passado (guia com cadastro expirado)
- `categories` vazio

Guias com flag `INCOMPLETO` são importados para `cadastur_registry` mas aparecem no relatório final para acompanhamento.

### 9.3 LGPD — mascaramento de dados sensíveis

No relatório final e em logs de console, mascare sempre:

```javascript
// CPF/CNPJ: mostre apenas últimos 2 dígitos
function maskDoc(doc) { return '***' + String(doc).slice(-2); }

// Email: mostre apenas domínio
function maskEmail(email) {
  const [u, d] = String(email).split('@');
  return u.slice(0,2) + '***@' + d;
}

// Telefone: mascare os 5 dígitos centrais
function maskPhone(phone) {
  return String(phone).replace(/(\(\d{2}\))(\d+)(\d{4})/, '$1****$3');
}
```

---

## 10. Relatório de saída obrigatório

Após a execução, gere e salve um relatório no formato abaixo em `reports/migration_YYYYMMDD.json`:

```json
{
  "executedAt": "2025-01-01T12:00:00Z",
  "executedBy": "nome-do-responsavel",
  "sourceFile": "nome_do_arquivo_recebido.csv",
  "summary": {
    "totalInFile": 0,
    "newGuidesAdded": 0,
    "existingGuidesUpdated": 0,
    "duplicatesSkipped": 0,
    "incompleteRecordsFlagged": 0,
    "errorsFailed": 0,
    "previousTotalInDB": 50242,
    "newTotalInDB": 0
  },
  "validationIssues": [
    {
      "record": "linha 42 — MARIA DA SILVA (Cadastur: ***91)",
      "issue": "UF inválida: 'XX'",
      "action": "Ignorado — requer revisão"
    }
  ],
  "expiredGuides": [
    {
      "name": "JOÃO SANTOS",
      "cadasturMasked": "***123",
      "uf": "RJ",
      "expiredAt": "2024-06-30",
      "action": "Importado como expirado"
    }
  ],
  "assumptions": [
    "Guias sem número Cadastur foram identificados por email quando possível",
    "Guias com validade expirada foram importados sem bloqueio",
    "Chave Pix não presente no arquivo — campo guide_verification não alterado"
  ],
  "dataPreservationConfirmation": {
    "usersTableModified": false,
    "guideProfilesModified": false,
    "guideVerificationModified": false,
    "reviewsModified": false,
    "reservationsModified": false,
    "expeditionsModified": false
  }
}
```

---

## 11. Checklist final antes de fazer push

- [ ] Backup da tabela `cadastur_registry` salvo em `backups/`
- [ ] Backup de `data/guides.json` salvo em `backups/`
- [ ] Dry-run executado e revisado
- [ ] Nenhum registro em `users`, `guide_profiles` ou `guide_verification` foi alterado
- [ ] Nenhum guia existente foi removido da base
- [ ] `data/guides.json` regenerado com `pnpm tsx scripts/export-guides-static.ts`
- [ ] Contagem de `guides.json` >= 50.242 (nunca menor)
- [ ] Relatório `reports/migration_YYYYMMDD.json` salvo
- [ ] Dados sensíveis mascarados no relatório
- [ ] Push feito para branch `claude/trekko-migration-guide-QrNMC`
- [ ] Pull Request criado para revisão antes de merge em `master`

---

## 12. Contatos e responsabilidades

| Papel | Responsabilidade |
|-------|-----------------|
| Engenheiro de dados | Executar o script, validar relatório |
| Revisor técnico | Aprovar PR antes do merge |
| Administrador do sistema | Aprovar merge em `master` e deploy |
| DPO (LGPD) | Validar mascaramento de dados no relatório |

---

*Documento gerado para o projeto Trekko · Branch `claude/trekko-migration-guide-QrNMC` · Stack: MySQL 8 · Drizzle ORM · Node.js · GitHub Pages*
