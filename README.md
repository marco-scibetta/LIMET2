# LIMET 2

**L**ightweight **I**terative **M**ethod for **E**ngineering with **T**raceability.

A spec-driven method for building software with AI agents, built natively for **Claude Code**.

## What it does

- **Spec first.** Every change starts from a written proposal and spec — never from code.
- **Full lifecycle.** `proposal → spec → plan → task → test → archive`, each step tracked.
- **Quality enforced, not hoped for.** No task is marked *done* without a verification strategy. Human approval is recorded. Every file change is logged automatically.
- **Project context on tap.** Document search (CEREBRO + Qdrant) and a code knowledge graph (Graphify) exposed as native MCP tools.
- **Native Claude Code.** Built from skills, hooks, subagents, a plugin and slash commands.

## How it works

You speak normally — *"add feature X"*, *"there's a bug Y"* — and Claude starts the right flow by itself.

| Command | Purpose |
|---|---|
| `/limet:init` | Install LIMET in a project |
| `/limet:new` | New change: proposal → spec → plan |
| `/limet:bug` | Structured bug report |
| `/limet:task` | Implement a task + automatic change log |
| `/limet:test` | Test plan and execution |
| `/limet:archive` | Archive the finished change |

### Where to start

| You want to | Go to |
|---|---|
| Add a feature | `limet/FRAMEWORK_MANUAL.md` Appendix B.4 |
| Fix a bug | `limet/FRAMEWORK_MANUAL.md` Appendix B.3 |
| Set up LIMET in a project | `limet/FRAMEWORK_MANUAL.md` §9 |
| Multi-project workspace | `limet/FRAMEWORK_MANUAL.md` Appendix C.1 |

---

# LIMET 2

**L**ightweight **I**terative **M**ethod for **E**ngineering with **T**raceability.

Un metodo *spec-driven* per sviluppare software con agenti AI, costruito nativamente per **Claude Code**.

## Cosa fa

- **Prima la specifica.** Ogni modifica parte da una proposta e una spec scritte — mai dal codice.
- **Ciclo di vita completo.** `proposta → spec → piano → task → test → archivio`, ogni passo tracciato.
- **Qualità imposta, non sperata.** Nessun task è marcato *done* senza una strategia di verifica. L'approvazione umana è registrata. Ogni modifica ai file è tracciata automaticamente.
- **Contesto del progetto a portata di mano.** Ricerca documentale (CEREBRO + Qdrant) e grafo del codice (Graphify) esposti come strumenti MCP nativi.
- **Claude Code nativo.** Fatto di skill, hook, subagent, plugin e slash command.

## Come funziona

Parli normalmente — *"aggiungi la feature X"*, *"c'è un bug Y"* — e Claude avvia da solo il flusso giusto.

| Comando | Scopo |
|---|---|
| `/limet:init` | Installa LIMET in un progetto |
| `/limet:new` | Nuova modifica: proposta → spec → piano |
| `/limet:bug` | Report di bug strutturato |
| `/limet:task` | Implementa un task + change log automatico |
| `/limet:test` | Piano ed esecuzione dei test |
| `/limet:archive` | Archivia la modifica conclusa |

### Da dove partire

| Vuoi | Vai a |
|---|---|
| Aggiungere una feature | `limet/FRAMEWORK_MANUAL.md` Appendice B.4 |
| Correggere un bug | `limet/FRAMEWORK_MANUAL.md` Appendice B.3 |
| Installare LIMET in un progetto | `limet/FRAMEWORK_MANUAL.md` §9 |
| Workspace multi-progetto | `limet/FRAMEWORK_MANUAL.md` Appendice C.1 |
