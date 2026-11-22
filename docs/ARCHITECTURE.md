# LIMET 2.0 — Architettura

## Visione

LIMET 2.0 è **un unico repo/plugin** che contiene tutto: skill, hook, subagent, MCP, e i motori **CEREBRO** (RAG documentale) e **GRAPHIFY** (knowledge graph). Niente repo esterni da installare.

> **Self-contained**: `claude plugin install limet` + Qdrant/Ollama/Postgres (locali o Docker) = tutto pronto.

## Principio guida

> **"Le guardrail stanno nei hook, non nelle istruzioni."**
> - **Skill** = Claude interpreta (costa contesto) → per il *lavoro* (generare documenti).
> - **Hook** = deterministico (zero contesto) → per le *regole* (bloccare, tracciare, ricordare).
> - **Subagent** = contesto isolato → per i *ruoli* (scrivere, validare).
> - **MCP** = tool esterni → per i *dati* (CEREBRO RAG, GRAPHIFY KG, DB SQL).
> - **CLAUDE.md** = minimo (puntatore + regole binding) → sempre-on, in poche righe.

## Componenti

```
limet/                              ← UNICO plugin (self-contained)
├── .claude-plugin/plugin.json
├── skills/    → /limet-new, /limet-task, /limet-test, /limet-archive, /limet-bug
├── agents/    → limet-writer, limet-gate
├── hooks/     → intent (UserPromptSubmit), guardrail, changelog, reminder
├── commands/  → /limet-dashboard, /limet-dashboard-stop
├── .mcp.json  → cerebro + graphify (nativo graphify-mcp) + db
├── mcp/
│   ├── cerebro/                    (RAG: scripts + server MCP)
│   └── db/                         (DB: server MCP, legge config.yaml/config.local.yaml)
├── config/                         (config.yaml + config.local.yaml + loader.py)
├── dashboard/                      (backend FastAPI + frontend React, port 8787)
├── .gitignore                      (include config.local.yaml)
├── CLAUDE.md
└── docs/ (manual, onboarding)
```

Runtime esterno (infra, non codice): **Qdrant** + **Ollama** + **Postgres** — installabili **nativi o Docker** (nessuna dipendenza Docker obbligatoria). **Graphify** è un MCP nativo (`graphify-mcp`, package `graphifyy`), non vendorizzato nel repo.

## Mappatura 1.0 → 2.0

| LIMET 1.0 | LIMET 2.0 |
|---|---|
| CHANGE_PROPOSAL + SPEC + PLAN + TASK_LIST + TEST_PLAN + E2E_VERIFICATION | `/limet-new` (un flusso) |
| TASK (esecuzione) + change log | `/limet-task` + hook PostToolUse |
| TEST_PLAN + TEST_EXECUTION | `/limet-test` |
| ARCHIVE_ENTRY | `/limet-archive` |
| BUG_REPORT | `/limet-bug` |
| DECISIONS | `/limet-new` (ADR-lite, solo se hard-to-reverse) |
| scripts/limet.ps1/limet.sh (attivazione) | `claude plugin install limet` |
| CEREBRO (skill-guida + Python) | `cerebro` MCP |
| GRAPHIFY (CLI) | `graphify` MCP (nativo) |

> I 18 template 1.0 (glossary, conventions, codebase-analysis, module-map, non-technical-summary, cross-project…) **non esistono più**: il ciclo genera solo i documenti essenziali con tracciabilità, il resto è supporto eliminato per ridurre l'attrito.

## Flusso dati

```
/limet-new ──► [limet-writer] genera proposal+spec+plan+task+test
                  │
                  ▼
             /limet-task ──► [PostToolUse hook] appende change log
                  │
                  ▼
             /limet-test ──► verifica unit+e2e (§1.5)
                  │
                  ▼
             [limet-gate] valida ──► /limet-archive
```

Contesto a monte: **CEREBRO** (docs RAG) + **GRAPHIFY** (codice KG) + **DB** (SQL read-only) interrogati via MCP quando serve.

## Vincoli (filosofia mantenuta)

1. **Spec-driven, non vibe-driven** — il documento resta la fonte di verità.
2. **Traceability** — ogni scelta ambigua = domanda esplicita con data.
3. **Test non-negoziabile** — nessun task chiuso senza unit + e2e + lint/type (§1.5).
4. **Leggero** — 5 skill, 6 hook, 2 subagent, 3 MCP, 1 dashboard. Niente di più.
5. **Conversazionale** — l'utente parla, non digita comandi (hook `intent`).
6. **Claude-only** — via l'overhead tool-agnostic.
7. **Self-contained** — Cerebro dentro il repo, Graphify via MCP nativo, DB read-only. Un solo install.
