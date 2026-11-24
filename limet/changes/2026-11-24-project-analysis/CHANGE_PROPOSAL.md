# CHANGE_PROPOSAL — Analisi progetto / auto-onboarding

## Problema

Come sviluppatore capita spesso di iniziare a lavorare su feature o bug in progetti
**non documentati**, senza onboarding. Si perde tempo a ricostruire struttura, dipendenze,
convenzioni e decisioni passate prima di poter scrivere codice sensato.

LIMET 2.0 già **documenta** il flusso di lavoro, ma non aiuta a **capire un progetto esistente**
di cui non si sa nulla.

## Cosa cambia

Nuova feature "Analisi progetto": a richiesta, un subagent dedicato analizza il codice di un
progetto non documentato e genera una serie di documenti onboarding in `/docs/` nella root
del progetto analizzato.

Trigger: dalla dashboard LIMET si marca un progetto "da analizzare" (flag nel config);
poi, in Claude Code su quel progetto, una skill `/limet-analyze` fa partire l'analisi
spawnando i subagent.

## Decisioni chiave (approvate con l'utente, 2026-11-24)

1. **Trigger** = skill + flag dashboard (niente `claude -p` headless: la dashboard non può
   spawnare subagent; i subagent li spawna solo Claude Code).
2. **Output** = `/docs/` nella root del progetto analizzato.
3. **Subagent** = nuovo `limet:analyzer` self-contained (nessuna dipendenza da plugin CE).

## Impatto

Nuovi componenti (nessuna breaking change ai componenti esistenti):

- `agents/analyzer.md` — nuovo subagent `limet:analyzer` (sola lettura).
- `skills/limet-analyze/SKILL.md` — nuova skill `/limet-analyze`.
- Dashboard: nuova pagina "Analizza" + endpoint `/api/analyze` (scrive flag config).
- `config/loader.py` — supporto flag `analyze` per progetto.
- `hooks/intent.sh` — rileva intento "analizza/onboarding" → suggerisce `/limet-analyze`.
- Documenti generati in `/docs/` (template riusato da `CODEBASE_ANALYSIS_TEMPLATE`).

## Non in scope

- Analisi automatica/continua (CI, watch).
- Generazione di test o refactor.
- Multi-lingua documenti (per ora lingua config o dell'utente).
