# LIMET 2.0 — Architettura

## Visione

LIMET 2.0 è **un unico repo/cartella** che contiene tutto: skill, hook, subagent, plugin, MCP, e i motori **CEREBRO** (RAG documentale) e **GRAPHIFY** (knowledge graph) **incorporati dentro**, non esterni. Niente dipendenze da repo separati da installare.

> **Self-contained**: `claude plugin install limet` + un `docker-compose` per Qdrant/Ollama (infra runtime) = tutto pronto. Nessun `C:\Progetti\CEREBRO` esterno, nessun Graphify da installare a parte.

## Principio guida

> **"Le guardrail stanno nei hook, non nelle istruzioni."**
> - **Skill** = Claude interpreta (costa contesto) → per il *lavoro* (generare documenti).
> - **Hook** = deterministico (zero contesto) → per le *regole* (bloccare, tracciare, ricordare).
> - **Subagent** = contesto isolato → per i *ruoli* (scrivere, validare).
> - **MCP** = tool esterni → per i *dati* (CEREBRO RAG, GRAPHIFY KG).
> - **CLAUDE.md** = minimo (puntatore + regole binding) → sempre-on, in poche righe.

> **CLAUDE.md minimo**: se gonfio, Claude diluisce l'attenzione e ignora parti. Regole binding in CLAUDE.md, dettaglio nelle skill (on-demand), enforcement negli hook (zero contesto). Progressive disclosure, non "tutto in CLAUDE.md".

## Componenti

```
limet/                              ← UNICO repo (self-contained)
├── .claude-plugin/plugin.json
├── skills/    → /limet:new, /limet:task, /limet:test, /limet:archive, /limet:bug
├── agents/    → limet-writer, limet-gate
├── hooks/     → intent (UserPromptSubmit), guardrail, changelog, reminder
├── .mcp.json  → cerebro + graphify + db
├── mcp/                            ← i motori SONO dentro
│   ├── cerebro/                    (RAG: scripts + server MCP)
│   ├── graphify/                   (KG: server MCP)
│   └── db/                         (DB: server MCP, legge .env_db)
├── .gitignore                      (include .env_db)
├── CLAUDE.md
└── docs/ (manual, onboarding)
```

Runtime esterno (solo infra, non codice): **Qdrant** (binario singolo Rust, free) + **Ollama** (installer nativo). **Nativi di default, Docker opzionale** (niente dipendenza Docker obbligatoria).

## Mappatura 1.0 → 2.0 (ogni template trova casa)

| LIMET 1.0 (template) | LIMET 2.0 |
|---|---|
| CHANGE_PROPOSAL + SPEC + PLAN + TASK_LIST + TEST_PLAN + E2E_VERIFICATION | `/limet:new` (un flusso) |
| TASK (esecuzione) + change log | `/limet:task` + hook PostToolUse |
| TEST_PLAN + TEST_EXECUTION | `/limet:test` |
| ARCHIVE_ENTRY | `/limet:archive` |
| BUG_REPORT | `/limet:bug` |
| GLOSSARY, CONVENTIONS, CODEBASE_ANALYSIS, ARCHITECTURE, MODULE_MAP, NON_TECHNICAL_SUMMARY | generati **ad hoc** dentro `/limet:new` (supporto, non skill separate) |
| CROSS_PROJECT_CHANGE | dentro `/limet:new` (opzione workspace) |
| scripts/limet.ps1 (attivazione) | `/limet:init` + plugin install |
| CEREBRO (skill-guida + Python) | `cerebro` MCP |
| GRAPHIFY (CLI) | `graphify` MCP |

## Flusso dati

```
/limet:new ──► [limet-writer] genera proposal+spec+plan+task+test
                  │
                  ▼
             /limet:task ──► [PostToolUse hook] appende change log
                  │
                  ▼
             /limet:test ──► verifica unit+e2e (§1.5)
                  │
                  ▼
             [limet-gate] valida ──► /limet:archive
```

Contesto a monte: **CEREBRO** (docs RAG) + **GRAPHIFY** (codice KG) interrogati via MCP quando serve.

## Vincoli (filosofia mantenuta)

1. **Spec-driven, non vibe-driven** — il documento resta la fonte di verità.
2. **Traceability** — ogni scelta ambigua = domanda esplicita con data.
3. **Test non-negoziabile** — nessun task chiuso senza unit + e2e (§1.5).
4. **Leggero** — 5 skill, 4 hook, 2 subagent, 3 MCP. Niente di più.
5. **Conversazionale** — l'utente parla, non digita comandi (hook `intent` + policy CLAUDE.md).
5. **Claude-only** — via l'overhead tool-agnostic.
6. **Self-contained** — Cerebro e Graphify sono dentro il repo LIMET, non esterni. Un solo install.
