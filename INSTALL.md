# LIMET 2.0 — Install

Spec-driven engineering plugin for Claude Code. One git repo, no public marketplace: the repo itself is the marketplace.

## Requirements

- Claude Code CLI (`claude`)
- Git access to the `marco-scibetta/LIMET2` repo

## Install

```bash
claude plugin marketplace add marco-scibetta/LIMET2
claude plugin install limet@limet-marketplace
```

The first command registers the repo as a source (marketplace). The second installs the `limet` plugin.

## Verify

Open Claude Code in a project and ask in natural language, e.g. *"I want to add a login feature"*: the LIMET flow starts (proposal → spec → plan → task → test → archive).

Skills available after install:

- `limet-new` — new cycle
- `limet-task` — run a task
- `limet-test` — test plan
- `limet-archive` — archive
- `limet-bug` — bug report
- `limet-analyze` — analyze an undocumented project

Dashboard (ops UI): launch with `python dashboard/run.py` — builds the frontend if needed, serves API + UI on :8787, and opens the browser.

## Update (after new features)

Inside Claude Code: `/plugin` → update, or re-run the two commands above.

## Uninstall

```bash
claude plugin uninstall limet@limet-marketplace
claude plugin marketplace remove limet-marketplace
```
