# LIMET 2.0 — Architecture

## Vision

LIMET 2.0 is **one repo/plugin** containing everything: skills, hooks, subagents, MCP, and the **CEREBRO** (document RAG) and **GRAPHIFY** (knowledge graph) engines. No external repos to install.

> **Self-contained**: `claude plugin install limet` + Qdrant/Ollama/Postgres (local or Docker) = all set.

## Guiding principle

> **"Guardrails live in hooks, not in instructions."**
> - **Skill** = Claude interprets (costs context) → for the *work* (generating documents).
> - **Hook** = deterministic (zero context) → for the *rules* (block, track, remind).
> - **Subagent** = isolated context → for the *roles* (write, validate, analyze).
> - **MCP** = external tools → for the *data* (CEREBRO RAG, GRAPHIFY KG, DB SQL).
> - **CLAUDE.md** = minimal (pointer + binding rules) → always-on, in a few lines.

## Components

```
limet/                              ← SINGLE plugin (self-contained)
├── .claude-plugin/plugin.json
├── skills/    → /limet-new, /limet-task, /limet-test, /limet-archive, /limet-bug, /limet-analyze
├── agents/    → limet-writer, limet-gate, limet-analyzer
├── hooks/     → intent (UserPromptSubmit), guardrail, changelog, reminder
├── .mcp.json  → cerebro + graphify (native graphify-mcp) + db
├── mcp/
│   ├── cerebro/                    (RAG: scripts + MCP server)
│   └── db/                         (DB: MCP server, reads config.yaml/config.local.yaml)
├── config/                         (config.yaml + config.local.yaml + loader.py)
├── dashboard/                      (FastAPI backend + React frontend, port 8787)
├── .gitignore                      (includes config.local.yaml)
├── CLAUDE.md
└── docs/ (manual, onboarding)
```

Runtime external (infra, not code): **Qdrant** + **Ollama** + **Postgres** — installable **native or Docker** (no mandatory Docker dependency). **Graphify** is a native MCP (`graphify-mcp`, package `graphifyy`), not vendored in the repo.

## 1.0 → 2.0 mapping

| LIMET 1.0 | LIMET 2.0 |
|---|---|
| CHANGE_PROPOSAL + SPEC + PLAN + TASK_LIST + TEST_PLAN + E2E_VERIFICATION | `/limet-new` (one flow) |
| TASK (execution) + change log | `/limet-task` + PostToolUse hook |
| TEST_PLAN + TEST_EXECUTION | `/limet-test` |
| ARCHIVE_ENTRY | `/limet-archive` |
| BUG_REPORT | `/limet-bug` |
| DECISIONS | `/limet-new` (ADR-lite, only if hard-to-reverse) |
| scripts/limet.ps1/limet.sh (activation) | `claude plugin install limet` |
| CEREBRO (guide skill + Python) | `cerebro` MCP |
| GRAPHIFY (CLI) | `graphify` MCP (native) |

> The 18 1.0 templates (glossary, conventions, codebase-analysis, module-map, non-technical-summary, cross-project…) **no longer exist**: the cycle generates only the essential documents with traceability, the rest is support removed to reduce friction.

## Data flow

```
/limet-new ──► [limet-writer] generates proposal+spec+plan+task+test
                  │
                  ▼
             /limet-task ──► [PostToolUse hook] appends change log
                  │
                  ▼
             /limet-test ──► verifies unit+e2e (§1.5)
                  │
                  ▼
             [limet-gate] validates ──► /limet-archive
```

Upstream context: **CEREBRO** (docs RAG) + **GRAPHIFY** (code KG) + **DB** (SQL read-only) queried via MCP when needed.

## Constraints (philosophy kept)

1. **Spec-driven, not vibe-driven** — the document stays the source of truth.
2. **Traceability** — any ambiguous choice = explicit question with a date.
3. **Non-negotiable testing** — no task closed without unit + e2e + lint/type (§1.5).
4. **Lightweight** — 6 skills, 6 hooks, 3 subagents, 3 MCP, 1 dashboard. Nothing more.
5. **Conversational** — the user talks, doesn't type commands (`intent` hook).
6. **Claude-only** — no tool-agnostic overhead.
7. **Self-contained** — Cerebro inside the repo, Graphify via native MCP, DB read-only. One install.
