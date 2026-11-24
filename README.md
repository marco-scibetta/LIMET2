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
pip install -e .          # Python dependencies (qdrant-client, fastapi, graphifyy, …)
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
| `/limet-analyze` | Analyze an undocumented project → onboarding docs in `docs/` |
| `/limet-dashboard` | Launch the dashboard on http://127.0.0.1:8787 |

## Where to start

| You want to | Go to |
|---|---|
| Understand how LIMET works | `limet/FRAMEWORK_MANUAL.md` |
| Get going on a project | `limet/ONBOARDING_CHECKLIST.md` |
| Map every file | `limet/MASTER_INDEX.md` |
| Launch + set up Qdrant/Ollama/Postgres | `limet-setup.html` |
| Initialize a project from the dashboard | `limet-project-init.html` |
