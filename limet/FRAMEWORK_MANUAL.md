# LIMET 2.0 — Manual

Spec-driven engineering for Claude Code, as a self-contained plugin.

## What it is

LIMET replaces the manual 1.0 flow with a Claude Code plugin that guides
spec-driven development with full traceability: proposal → spec → plan → task → test → archive.

## Installation

```bash
pip install -e .            # Python dependencies (qdrant-client, fastapi, graphifyy, …)
claude plugin marketplace add ./
claude plugin install limet
claude plugin validate .    # non-strict: the root CLAUDE.md warning is by design
```

## Architecture

| Component | What it does |
| --------- | ------------ |
| **Skills** (6) | `/limet-new`, `/limet-task`, `/limet-test`, `/limet-bug`, `/limet-archive`, `/limet-analyze` |
| **Hooks** (6) | `resume.sh` (resumes active cycle), `intent.sh` (detects intent), `guardrail.sh` (blocks build/commit/destructive), `changelog.sh` (auto log), `precompact.sh` (pre-compact state), `reminder.sh` (reminds test/archive) |
| **Subagents** (3) | `limet-writer` (writes docs), `limet-gate` (validates §1.5 + drift), `limet-analyzer` (analyzes project → `docs/` docs) |
| **MCP** (3) | `cerebro` (Qdrant RAG), `graphify` (code knowledge graph), `db` (read-only SQL) |
| **Dashboard** | init / projects / re-index / setup / analyze (per-project config) on :8787 |

## Lifecycle

```
limet-new → limet-task → limet-test → (limet-bug) → limet-archive
```

1. **new** — generates the documents in `limet/changes/<data-slug>/`.
2. **task** — runs a task with a 2-3 line brief and updates the change log.
3. **test** — generates TEST_PLAN + TEST_EXECUTION with re-runnable commands. Execution belongs to the user: `!bash scripts/run-tests.sh` (or `!bash scripts/run-tests.sh <command>`) records the outcome in TEST_EXECUTION without polluting the context and destroys temporary logs if OK. On FAIL it keeps `raw.log` and writes into the summary exit code + a pointer to the log + a 60-line tail (enough to assess without re-running the tests).
4. **bug** — structured bug report (if needed).
5. **archive** — moves the verified work to `limet/archive/<slug>/`.

## Configuration (per-project)

`config/config.yaml` (committed defaults) + `config/config.local.yaml` (overrides + secrets, gitignored).

```yaml
# config.yaml
projects:
  <slug>:
    qdrant: { url: http://localhost:6333 }
    ollama: { url: http://localhost:11434, model: nomic-embed-text }
    db: { host: localhost, port: 5432, database: mydb, user: myuser }
```

```yaml
# config.local.yaml (password never in config.yaml)
projects:
  <slug>:
    db: { password: "..." }
```

Shared loader: `config/loader.py` (deep-merge config.yaml ← config.local.yaml).

## Dashboard

- `python dashboard/run.py` (builds if needed + serves API/UI on :8787).
- **Init**: project name (existing-projects combo) + docs path → does register + graphify extract + Qdrant ingestion.
- **Re-index**: project combo + docs path, incremental/force/clean modes.
- **Setup**: project combo → Qdrant/Ollama/DB sections → saves to config.local.yaml.
- **Analyze**: project combo → marks the project for analysis.

## Language (IT/EN)

- The 🇮🇹/🇬🇧 flag at the top right of the dashboard → changes the interface and sets `language` in `config.local.yaml`.
- Skills and agents read `language` from `config/config.yaml` → the produced documents are in the chosen language.

## Multi-module projects (workspace)

- A folder `X/` with multiple modules (`X/module-a`, `X/module-b`), each with its own `docs/`.
- **Init** + check **"Workspace"** → registers `X` with all docs (root + modules) in **one** Qdrant collection, **one** Graphify graph, **one** db.
- Each module has its own `limet/` (via cwd), but Qdrant/Graphify/DB are shared.
- Cross-module feature: session in `X`; local feature: session in the module.

## Linked projects

- Two independent projects A and B that interact.
- **Projects** → "Link projects": select A and B → **Link**.
- Qdrant search in A queries A **and** B (extra collection).
- A hook (UserPromptSubmit) reminds at every prompt: "you are in X, linked to Y — use `cerebro_search` with `project=X`".

## Project analysis (auto-onboarding)

- For **undocumented** projects, without onboarding.
- Dashboard → **Analyze**: select the project and click "Request analysis" → sets `projects.<slug>.analyze: true` in `config.local.yaml`.
- In Claude Code on that project: `/limet-analyze` → spawns `limet-analyzer`, which generates in `docs/`: `architecture.md`, `module-map.md`, `dependencies.md`, `conventions.md`, `decisions.md`, `glossary.md`, `NON_TECHNICAL_SUMMARY.md`.
- Re-indexing the generated docs belongs to the user.

## Binding rules

- Spec first: proposal/plan before non-trivial code.
- Ambiguity → explicit question with a date, never assume.
- No task `done` without a verification strategy (unit + e2e + lint/type if configured).
- Never build/test autonomously: give the command, the user runs it.
- Never commit/push/migrate/deploy without authorization.
