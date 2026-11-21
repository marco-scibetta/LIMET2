# LIMET 2.0 — Subagents

I subagent sono **contesti isolati** per ruoli specifici. LIMET 2.0 ne usa **2** (non di più, per restare leggero).

## I 2 subagent

| Subagent | Ruolo | Tools | Quando |
|---|---|---|---|
| `limet-writer` | scrive i documenti (proposal/spec/plan/test) con contesto isolato | Read, Grep, Glob, Write | dentro `/limet-new` |
| `limet-gate` | **validatore**: verifica §1.5 + **fresh-eyes review** + **drift report** (doc ↔ codice) | Read, Grep, Glob | prima di `/limet-archive` e a fine task |

## Esempio `agents/limet-gate.md`

```markdown
---
name: limet-gate
description: Validatore LIMET. Verifica §1.5 (unit + e2e), fa fresh-eyes review della SPEC/PLAN e drift report doc↔codice. Rifiuta task senza verifica. Solo lettura.
tools: Read, Grep, Glob
---

# limet-gate — validatore

Controlla `limet/TASK_LIST.md` e i file di test. Per ogni task marcato "done":

1. Esiste un unit test dedicato? (o giustificazione esplicita "n/a")
2. Esiste una verifica e2e con passi eseguibili?
3. Il change log è compilato?

### Fresh-eyes review (principio "goldfish", da EGM)

Rivede la SPEC/PLAN con **contesto fresco** (subagent isolato, senza la conversazione precedente), per beccare assunzioni implicite e blind spot che chi ha scritto il doc non vede. Un reviewer che ha letto tutto non vede il vuoto.

### Drift report

Confronta SPEC/PLAN con il codice reale e segnala le divergenze ("la SPEC dice X ma il codice fa Y"). Proattivo, non retroattivo.

Output: lista di task `OK` / `FAIL` + eventuali blind spot e drift. Se `FAIL`, il task NON è chiuso.
```

## Esempio `agents/limet-writer.md`

```markdown
---
name: limet-writer
description: Scrive i documenti LIMET (proposal, spec, plan, task list, test plan, e2e) partendo da un'idea. Contesto isolato. Segue i template LIMET.
tools: Read, Grep, Glob, Write
---

# limet-writer — scrittore documenti

Dall'input ricevuto, genera i documenti LIMET in `limet/` seguendo i template.
Regole: spec-driven (§1.1), traceability (§1.2), test non-negoziabile (§1.5).
Mai assumere: scelte ambigue → riportale come domande aperte.
```

## Gate oggettivo: `/goal` (enforcement nativo di §1.5)

`/goal` (feature nativa Claude Code) imposta una **condizione di completamento** e un **fast evaluator** (modello leggero separato) verifica **oggettivamente** se è soddisfatta, ogni volta che l'agente prova a fermarsi. È l'enforcement di §1.5 che oggi è solo auto-dichiarato.

**Dove usarlo (1 punto, non di più):** a fine task (`/limet-task`):
```
/goal "tutti gli unit + e2e test del task passano, type checker zero errori"
```

**Rapporto con `limet-gate`:** complementari, non sovrapposti.

| | Verifica |
|---|---|
| `/goal` (fast evaluator) | **oggettiva**: i test passano davvero? |
| `limet-gate` (subagent) | **documentale**: fresh-eyes, drift, §1.5 documentato |

## Perché solo 2

- `limet-writer` = tutto il "produrre documenti" (un ruolo, non 18).
- `limet-gate` = il controllo qualità (il principio §1.5 come gate indipendente).

Le 2 estensioni di `limet-gate` (fresh-eyes review + drift report) vengono da **EGM (Elephant-Goldfish Model)**: rivedere con "occhi freschi" e confrontare doc↔codice. Sono piccole, **non aggiungono subagent** — estendono quello esistente.

Aggiungere altri subagent (es. `limet-analyzer` per la codebase analysis) **solo se** il flusso lo richiede davvero — non per completezza. (Vincolo "non overingegnerizzare".)
