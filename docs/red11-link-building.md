# RED-11 — Estratégia de Link Building Editorial

**Objetivo:** 10 backlinks de domínios com DA > 30 em 90 dias  
**Período:** 05/06/2026 – 03/09/2026  
**Nicho:** ecoturismo, aventura, turismo, trilhas

---

## Visão geral

| Componente | Detalhe |
|---|---|
| Portais-alvo | 10 ativos + 2 reservas |
| DA mínimo | 30 (validar com Moz ou Ahrefs antes do envio) |
| Artigos prontos | 7 (GP-01 a GP-07) |
| Templates de pitch | 2 (inicial + follow-up) |
| Tracking | `data/link_building_red11.json` |

---

## Arquivos da campanha

```
docs/
  red11-link-building.md          ← este arquivo
  guest-posts/
    GP-01-trilha-multiplos-dias.md
    GP-02-equipamentos-mata-atlantica.md
    GP-03-ecoturismo-responsavel.md
    GP-04-trilhas-desafiadoras.md
    GP-05-turismo-aventura-destinos.md
    GP-06-trilhas-cachoeira.md
    GP-07-guia-operadores.md
    pitch-template-inicial.md
    pitch-template-followup.md

data/
  link_building_red11.json        ← source of truth do status da campanha
```

---

## Portais-alvo e artigos recomendados

| ID | Portal | DA est. | Nicho | Artigo |
|---|---|---|---|---|
| T01 | mochileiros.com | 42 | aventura | GP-01 |
| T02 | aventureiro.com.br | 38 | aventura | GP-02 |
| T03 | ecoviagem.com.br | 45 | ecoturismo | GP-03 |
| T04 | trilhasebosques.com.br | 33 | trilhas | GP-04 |
| T05 | guiatravel.com.br | 41 | turismo | GP-05 |
| T06 | viajali.com.br | 36 | turismo | GP-01 |
| T07 | caminhosdaterra.com.br | 34 | ecoturismo | GP-06 |
| T08 | brasilaventura.com | 39 | aventura | GP-02 |
| T09 | turismoconsultoria.com.br | 35 | turismo B2B | GP-07 |
| T10 | conexaonatureza.com.br | 31 | sustentabilidade | GP-03 |
| T11 | explorebrasil.tur.br | 37 | **reserva** | GP-05 |
| T12 | naturezaviva.com.br | 32 | **reserva** | GP-06 |

---

## Cronograma de execução

### Semanas 1–2 (05–19/jun)
- [ ] Validar DA real de cada domínio (Moz Free / Ahrefs Trial)
- [ ] Revisar todos os 7 artigos com leitura final
- [ ] Enviar pitch lote 1: T01, T02, T03

### Semanas 3–4 (20/jun–03/jul)
- [ ] Follow-up lote 1 (se sem resposta após 7 dias)
- [ ] Enviar pitch lote 2: T04, T05, T06

### Semanas 5–6 (04–17/jul)
- [ ] Enviar pitch lote 3: T07, T08, T09, T10
- [ ] Acompanhar publicações confirmadas do lote 1
- [ ] Validar primeiros backlinks no GSC

### Semanas 7–8 (18–31/jul)
- [ ] Follow-up geral em pendentes
- [ ] Acionar T11/T12 se necessário

### Semanas 9–13 (01/ago–03/set)
- [ ] Monitorar publicações restantes
- [ ] Validar todos os backlinks via GSC
- [ ] Relatório final da campanha

---

## KPIs

| Métrica | Meta |
|---|---|
| Backlinks publicados | ≥ 10 |
| DA mínimo por domínio | ≥ 30 |
| Taxa de resposta de pitch | > 30% |
| Taxa de conversão pitch→publicação | > 60% |
| Prazo | 90 dias |

---

## Fluxo de atualização do JSON

Após cada ação, atualizar o campo `status` do portal em `data/link_building_red11.json`:

- `para_contato` → pitch ainda não enviado
- `pitch_enviado` → preencher campo `pitch_sent` com a data
- `em_negociacao` → respondeu positivamente, artigo enviado
- `publicado` → preencher campo `backlink_url`
- `recusado` → portal recusou, acionar próxima reserva
- `sem_retorno` → sem resposta após follow-up, acionar reserva
- `reserva` → não acionar ainda
