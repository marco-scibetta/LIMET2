# LIMET 2

**L**ightweight **I**terative **M**ethod for **E**ngineering with **T**raceability.

A spec-driven method for building software with AI agents, built natively for **Claude Code**.

## What it does

- **Spec first.** Every change starts from a written proposal and spec — never from code.
- **Full lifecycle.** `proposal → spec → plan → task → test → archive`, each step tracked.
- **Quality enforced, not hoped for.** No task is marked *done* without a verification strategy. Every file change is logged automatically by a hook.
- **Three columns.** Qdrant for documents, Graphify for the code graph, spec-driven as the method that ties them together.
- **Native Claude Code.** Skills, hooks, subagents, MCP servers, a dashboard and slash commands.

## Install

```bash
pip install -e .          # dipendenze Python (qdrant-client, fastapi, graphifyy, …)
claude plugin marketplace add ./
claude plugin install limet
claude plugin validate .   # non-strict (the root CLAUDE.md warning is by design)
```

## Commands

| Command | Purpose |
|---|---|
| `/limet-new` | New change: proposal → spec → plan → task list → tests |
| `/limet-task` | Implement a task + automatic change log |
| `/limet-test` | Test plan and execution |
| `/limet-bug` | Structured bug report |
| `/limet-archive` | Archive the finished, verified change |
| `/limet-dashboard` | Launch the dashboard on http://127.0.0.1:8787 |

## Where to start

| You want to | Go to |
|---|---|
| Understand how LIMET works | `limet/FRAMEWORK_MANUAL.md` |
| Get going on a project | `limet/ONBOARDING_CHECKLIST.md` |
| Map every file | `limet/MASTER_INDEX.md` |
| Launch + set up Qdrant/Ollama/Postgres | `limet-setup.html` |
| Initialize a project from the dashboard | `limet-project-init.html` |

---

# LIMET 2

**L**ightweight **I**terative **M**ethod for **E**ngineering with **T**raceability.

Un metodo *spec-driven* per sviluppare software con agenti AI, costruito nativamente per **Claude Code**.

## Cosa fa

- **Prima la specifica.** Ogni modifica parte da una proposta e una spec scritte — mai dal codice.
- **Ciclo di vita completo.** `proposta → spec → piano → task → test → archivio`, ogni passo tracciato.
- **Qualità imposta, non sperata.** Nessun task è marcato *done* senza una strategia di verifica. Ogni modifica ai file è tracciata automaticamente da un hook.
- **Tre colonne.** Qdrant per i documenti, Graphify per il grafo del codice, spec-driven come metodo che li lega.
- **Claude Code nativo.** Skill, hook, subagent, server MCP, una dashboard e slash command.

## Installazione

```bash
pip install -e .          # dipendenze Python (qdrant-client, fastapi, graphifyy, …)
claude plugin marketplace add ./
claude plugin install limet
claude plugin validate .   # non-strict (il warning sul CLAUDE.md alla root è by-design)
```

## Comandi

| Comando | Scopo |
|---|---|
| `/limet-new` | Nuova modifica: proposta → spec → piano → task list → test |
| `/limet-task` | Implementa un task + change log automatico |
| `/limet-test` | Piano ed esecuzione dei test |
| `/limet-bug` | Report di bug strutturato |
| `/limet-archive` | Archivia la modifica conclusa e verificata |
| `/limet-dashboard` | Avvia la dashboard su http://127.0.0.1:8787 |

## Da dove partire

| Vuoi | Vai a |
|---|---|
| Capire come funziona LIMET | `limet/FRAMEWORK_MANUAL.md` |
| Partire su un progetto | `limet/ONBOARDING_CHECKLIST.md` |
| Mappa di tutti i file | `limet/MASTER_INDEX.md` |
| Avviare la dashboard + setup Qdrant/Ollama/Postgres | `limet-setup.html` |
| Inizializzare un progetto dalla dashboard | `limet-project-init.html` |
