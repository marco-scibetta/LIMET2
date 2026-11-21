# LIMET 2.0 — Install

Plugin spec-driven engineering per Claude Code. Un solo repo git, nessun marketplace pubblico: il repo stesso fa da marketplace.

## Requisiti

- Claude Code CLI (`claude`)
- Accesso git al repo `marco-scibetta/LIMET2`

## Install

```bash
claude plugin marketplace add marco-scibetta/LIMET2
claude plugin install limet@limet-marketplace
```

Il primo comando registra il repo come sorgente (marketplace). Il secondo installa il plugin `limet`.

## Verifica

Apri Claude Code in un progetto e chiedi in linguaggio naturale, es. *"voglio aggiungere una feature di login"*: il flusso LIMET parte (proposta → spec → plan → task → test → archive).

Skill disponibili dopo l'install:

- `limet-new` — nuovo ciclo
- `limet-task` — esegue un task
- `limet-test` — piano test
- `limet-archive` — archivia
- `limet-bug` — report bug

Comando slash: `/limet-dashboard` (avvia la dashboard su :8787).

## Update (dopo nuove feature)

Dentro Claude Code: `/plugin` → update, oppure riesegui i due comandi sopra.

## Uninstall

```bash
claude plugin uninstall limet@limet-marketplace
claude plugin marketplace remove limet-marketplace
```
