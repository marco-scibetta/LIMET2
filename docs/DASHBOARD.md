# LIMET 2.0 — Dashboard (ops)

The dashboard is the **web interface for operations**, not for the work. The work is done by Claude; the ops are done by the human with a GUI.

## Separation principle

| | Claude (MCP + skills) | Dashboard |
|---|---|---|
| Role | **the work** | **the ops** |
| What | generate spec/tasks, implement, query context | init, re-index, status, setup/config, analyze |
| Interaction | conversational | GUI |

Rule: **if a function is more convenient in conversation, it lives in chat, not in the UI.** Each page = one real action.

## Architecture: single process

```
React (Vite) ──► REST API ◄── Claude MCP
                 ┌─────────────────┐
                 │ FastAPI backend │  (also serves the built frontend)
                 │ cerebro/db      │
                 └─────────────────┘
```

The FastAPI backend **also serves the built frontend** (`dist/`): one process, one command.

```bash
python dashboard/run.py     # builds if needed + starts on :8787
/limet-dashboard            # equivalent slash command
```

## Pages (6)

1. **Status** — Qdrant/Ollama status + registered projects.
2. **Init** — registers a project (name + docs path): in one go it does **register + graphify extract + Qdrant ingestion**. A combo proposes existing projects.
3. **Projects** — slug, root, docs paths of registered projects.
4. **Re-index** — incremental / force / clean (prune); project + docs path combo.
5. **Setup** — **per-project** configuration (Qdrant, Ollama, DB), saved in `config.local.yaml`. Password never shown. Includes "Test DB connection".
6. **Analyze** — marks a project for analysis (`analyze: true` in `config.local.yaml`). In Claude Code, `/limet-analyze` generates the onboarding docs in `docs/`.

## API

| Endpoint | Purpose |
|---|---|
| `GET /api/info` | name + version + status |
| `GET /api/status` | Qdrant/Ollama reachable + projects |
| `GET /api/projects` | registered projects (slug, root, docs) |
| `POST /api/init` | register + graphify + ingestion |
| `POST /api/reindex` | re-ingestion (incremental/force/prune) |
| `GET /api/config?project=` | a project's config (password masked) |
| `POST /api/config` | save per-project config to config.local.yaml |
| `POST /api/config/test` | test DB connection |
| `POST /api/analyze` | mark a project for analysis (analyze flag) |
| `GET /api/analyze?project=` | read a project's analyze flag |
| `GET /api/browse` | file browser (subfolders) |

## What the dashboard does NOT cover

- Generating spec/plan/tasks (→ Claude, via skills).
- Implementing code (→ Claude).
- Context queries during work (→ Claude, via MCP).

## Constraint (do not over-engineer)

The dashboard does **the ops a human would do by hand**. Each page maps a real action; if it only serves Claude, it does not belong in the UI.
