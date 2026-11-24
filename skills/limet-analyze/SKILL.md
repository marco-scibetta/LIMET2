---
name: limet-analyze
description: 'Analizza un progetto non documentato: genera i documenti onboarding in docs/ tramite il subagent limet-analyzer.'
user-invocable: true
allowed-tools: Read, Grep, Glob, Agent
---

# LIMET — analisi progetto ($ARGUMENTS)

Avvia l'analisi del progetto corrente per generare documenti onboarding in `docs/`.

## Flusso

1. Determina lo slug del progetto dal nome della directory corrente (come fa `hooks/intent.sh`).
2. Verifica il flag `analyze` in `config/config.yaml` + `config/config.local.yaml`:
   - se `projects.<slug>.analyze` è `true`, procedi;
   - altrimenti chiedi conferma all'utente prima di procedere (mai assumere).
3. Spawna il subagent `limet-analyzer` (subagent_type `limet:limet-analyzer`) sul progetto corrente.
4. Al termine, verifica che in `docs/` esistano i 7 documenti attesi e riporta l'esito.

## Regole binding

- Non eseguire build/test; non modificare il codice del progetto target.
- Il re-index dei documenti generati resta all'utente (mai indicizzare in autonomia).
- Se il flag non è attivo e l'utente non conferma, fermati senza procedere.
