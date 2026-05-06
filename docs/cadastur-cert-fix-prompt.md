# Trekko — Prompt de Correção: `cert_norm` Truncation Bug

> **Escopo:** Correção do campo `cadasturNumber` em `data/guides.json` após migração `cadastur_cert_new_guides` (ID `fdfb2440-877d-418d-ac96-2f4ae1fefef9`)
> **Data do bug:** 2026-04-24
> **Registros afetados:** 669 do lote novo + potenciais updates no lote antigo
> **Arquivo fonte:** planilha de origem da migração (`Source = 2026_1_CADASTUR`)

---

## 1. Descrição do bug

Durante a importação da planilha `2026_1_CADASTUR`, o campo `cert_norm` foi gerado com **truncamento do último dígito** de cada número de certificado. O import usou `cert_norm` como valor de `cadasturNumber` em vez do campo original `Número do Certificado`.

### Padrão A — 10 dígitos (661 registros do lote novo)

O `cert_norm` foi armazenado diretamente, sem zero-padding:

```
Número do Certificado : 21670125700   (11 dígitos — correto)
cert_norm             : 2167012570    (10 dígitos — truncado)
cadasturNumber stored : "2167012570"  (ERRADO)
```

### Padrão B — 11 dígitos com zero à esquerda (confirmado: Gabriel, id=153)

O `cert_norm` foi zero-padded para 11 chars, gerando número inteiramente diferente:

```
Número do Certificado : 24403063280    (11 dígitos — correto)
cert_norm             : 2440306328     (10 dígitos — truncado)
cadasturNumber stored : "02440306328"  (ERRADO — zero-padded cert_norm)
```

### Padrão C — 13 dígitos (7 registros do lote novo, CNPJs)

CNPJ com zero à esquerda perdido por conversão numérica:

```
Número do Certificado : 01693868000187   (14 dígitos — correto)
cadasturNumber stored : "1693868000187"  (ERRADO — leading zero dropped)
```

### Padrão D — 12 dígitos (1 registro do lote novo)

```
id=54469 stored=251000418488  → provável correto: 25100041848?  (requer fonte)
```

---

## 2. Escopo completo dos registros afetados

```
Lote novo (IDs 53305–61566): 7.890 registros importados
  ├─ 661 com 10 dígitos  → Padrão A (cert_norm cru, sem padding)
  ├─ 7   com 13 dígitos  → Padrão C (CNPJ, leading zero perdido)
  ├─ 1   com 12 dígitos  → Padrão D (investigar individualmente)
  └─ 1   via ON DUPLICATE KEY UPDATE → Padrão B (id=153, já corrigido)

Lote antigo (IDs ≤ 53304): examinar registros atualizados pela migração
  └─ Qualquer registro cujo cadasturNumber foi sobrescrito pelo cert_norm
     durante o ON DUPLICATE KEY UPDATE deve ser revertido com dados da fonte
```

---

## 3. Pré-requisitos

```bash
# 1. Confirme que tem o arquivo fonte
ls -lh 2026_1_CADASTUR.*      # CSV, XLSX ou similar

# 2. Backup do estado atual
cp data/guides.json data/guides.json.bak_$(date +%Y%m%d_%H%M%S)

# 3. Confirme contagem atual
python3 -c "import json; d=json.load(open('data/guides.json')); print(len(d))"
# Esperado: 56191
```

---

## 4. Script de correção

### 4.1 Diagnóstico inicial (dry-run)

```python
# scripts/fix-cert-norm.mjs  (ou .py — exemplo em Python)
import json, re, sys
from collections import defaultdict

with open('data/guides.json', encoding='utf-8') as f:
    guides = json.load(f)

# Indexar por email e telefone para lookup rápido
by_email = {g['email'].strip().lower(): g for g in guides if g.get('email')}
by_phone = {''.join(filter(str.isdigit, g['phone'])): g
            for g in guides if g.get('phone')}

# Identificar candidatos a correção por comprimento anômalo
def is_anomalous(num):
    n = str(num)
    return len(n) not in (11, 14)   # CPF=11, CNPJ=14

anomalous = [g for g in guides if is_anomalous(g['cadasturNumber'])]
print(f"Registros com comprimento anômalo: {len(anomalous)}")
for g in anomalous[:20]:
    print(f"  id={g['id']:6d}  len={len(str(g['cadasturNumber']))}  "
          f"stored={g['cadasturNumber']:15s}  {g['name'][:40]}  {g['uf']}")
```

### 4.2 Carga do arquivo fonte

O arquivo fonte (`2026_1_CADASTUR`) possui estas colunas relevantes:

| Coluna fonte | Papel |
|---|---|
| `Número do Certificado` | **Valor correto** — use este |
| `cert_norm` | Valor truncado — NÃO use para corrigir |
| `E-mail do usuário administrador` | Chave de match primária |
| `Telefone Comercial` | Chave de match secundária |
| `Nome Completo` + `UF` + `Município` | Chave de match terciária |

```python
import csv

def load_source(filepath):
    """Retorna dict: email_normalizado → {cert_number, name, uf, city, phone, ...}"""
    records = {}
    with open(filepath, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')   # ajuste delimiter se necessário
        for row in reader:
            cert = ''.join(filter(str.isdigit, row.get('Número do Certificado', '')))
            email = row.get('E-mail do usuário administrador', '').strip().lower()
            phone = ''.join(filter(str.isdigit, row.get('Telefone Comercial', '')))
            name  = row.get('Nome Completo', '').strip().upper()
            uf    = row.get('UF', '').strip().upper()
            city  = row.get('Município', '').strip()
            if cert:
                records[email] = records[phone] = {
                    'cert': cert, 'name': name, 'uf': uf, 'city': city,
                    'email': email, 'phone': phone
                }
    return records

source = load_source('2026_1_CADASTUR.csv')   # ajuste caminho/extensão
```

### 4.3 Lógica de matching e correção

```python
def normalize_email(e):
    return str(e or '').strip().lower()

def normalize_phone(p):
    return ''.join(filter(str.isdigit, str(p or '')))

def normalize_name_uf(name, uf):
    return f"{str(name).strip().upper()}|{str(uf).strip().upper()}"

fixes   = []   # (guide_id, old_cert, new_cert, match_method)
manual  = []   # registros que precisam de revisão humana

for g in anomalous:
    stored = str(g['cadasturNumber'])
    correct = None
    method  = None

    # --- Tentativa 1: match por email ---
    email_key = normalize_email(g.get('email'))
    if email_key and email_key in source:
        correct = source[email_key]['cert']
        method  = 'email'

    # --- Tentativa 2: match por telefone ---
    if not correct:
        phone_key = normalize_phone(g.get('phone'))
        if len(phone_key) >= 8 and phone_key in source:
            correct = source[phone_key]['cert']
            method  = 'phone'

    # --- Tentativa 3: match por nome+UF ---
    if not correct:
        nk = normalize_name_uf(g.get('name'), g.get('uf'))
        for src in source.values():
            if normalize_name_uf(src['name'], src['uf']) == nk:
                correct = src['cert']
                method  = 'name+uf'
                break

    # --- Padrão C: CNPJ de 13 dígitos (leading zero perdido) ---
    if not correct and len(stored) == 13:
        candidate = '0' + stored
        correct = candidate
        method  = 'cnpj-prepend-0'

    if correct and correct != stored:
        fixes.append({
            'id': g['id'], 'old': stored, 'new': correct,
            'method': method, 'name': g['name'], 'uf': g['uf']
        })
    else:
        manual.append(g)

print(f"\nFixes prontos:  {len(fixes)}")
print(f"Requer revisão: {len(manual)}")

# Preview dos fixes
for f in fixes[:10]:
    print(f"  id={f['id']:6d}  {f['old']:15s} → {f['new']:15s}  ({f['method']})  {f['name'][:35]}")

# Preview dos registros sem match
print("\nSem match automático:")
for g in manual[:10]:
    print(f"  id={g['id']:6d}  stored={g['cadasturNumber']:15s}  {g['name'][:35]}  {g['uf']}")
```

### 4.4 Aplicar correções

Execute **somente após validar o dry-run acima**:

```python
if '--apply' not in sys.argv:
    print("\n[DRY-RUN] Passe --apply para aplicar as correções.")
    sys.exit(0)

# Indexar guides por id para update O(1)
by_id = {g['id']: g for g in guides}

applied = 0
for fix in fixes:
    guide = by_id.get(fix['id'])
    if guide:
        guide['cadasturNumber'] = fix['new']
        applied += 1

print(f"Aplicados: {applied}/{len(fixes)}")

# Salvar
with open('data/guides.json', 'w', encoding='utf-8') as f:
    json.dump(guides, f, ensure_ascii=False, separators=(',', ':'))

print("data/guides.json salvo.")
```

### 4.5 Verificação pós-fix

```python
with open('data/guides.json', encoding='utf-8') as f:
    guides = json.load(f)

# Nenhum registro deve ter comprimento anômalo (exceto os da lista manual)
still_bad = [g for g in guides if len(str(g['cadasturNumber'])) not in (11, 14)]
manual_ids = {g['id'] for g in manual}
unresolved = [g for g in still_bad if g['id'] not in manual_ids]

print(f"Total guias: {len(guides)}")
print(f"Ainda com comprimento anômalo (exceto manual): {len(unresolved)}")
# Esperado: 0

# Teste de lookup para o caso reportado pelo usuário
match = next((g for g in guides if g['cadasturNumber'] == '24403063280'), None)
print(f"Lookup 24403063280: {'OK — ' + match['name'] if match else 'AINDA NÃO ENCONTRADO'}")
```

---

## 5. Registros que requerem revisão manual

Os registros sem match automático devem ser corrigidos individualmente consultando:

1. O arquivo fonte `2026_1_CADASTUR` — procure pelo nome completo + UF
2. O portal oficial CADASTUR em `cadastur.turismo.gov.br` — busca por nome do guia
3. Contato direto com o guia via e-mail/telefone para confirmar o número

Registre cada correção manual no relatório de saída (seção 6).

---

## 6. Relatório de saída

Salve em `reports/cert-norm-fix-YYYYMMDD.json`:

```json
{
  "executedAt": "2026-...",
  "triggerBug": "cert_norm trailing-digit truncation during 2026_1_CADASTUR import",
  "summary": {
    "totalAnomalousFound": 669,
    "fixedByEmail": 0,
    "fixedByPhone": 0,
    "fixedByNameUf": 0,
    "fixedByCnpjPrepend0": 7,
    "fixedManually": 0,
    "stillUnresolved": 0
  },
  "unresolvedRecords": [],
  "dataIntegrityConfirmation": {
    "noGuideRemoved": true,
    "noOtherFieldModified": true,
    "guidesJsonRegenerated": true
  }
}
```

---

## 7. Commit e push

```bash
git add data/guides.json reports/cert-norm-fix-*.json
git commit -m "fix: correct cert_norm truncation in cadasturNumber for 669 new-batch records"
git push -u origin claude/verify-supabase-migration-LkhX8
```

---

## 8. Checklist final

- [ ] Arquivo fonte `2026_1_CADASTUR` disponível e legível
- [ ] Backup de `data/guides.json` criado antes do fix
- [ ] Dry-run executado e revisado — fixes fazem sentido
- [ ] Nenhum campo além de `cadasturNumber` foi modificado
- [ ] Nenhum guia foi removido (`len(guides) >= 56191`)
- [ ] Lookup de `24403063280` retorna GABRIEL MENDONCA DOS SANTOS
- [ ] Registros sem match automático documentados no relatório
- [ ] Relatório salvo em `reports/`
- [ ] Push feito para `claude/verify-supabase-migration-LkhX8`

---

*Bug documentado em `docs/cadastur-cert-fix-prompt.md` · Migração `fdfb2440` · 2026-04-24*
