# LIMET 2.0 — Indice master

> Ordine di lettura dei file del plugin e mappa rapida "voglio fare X → vai a Y".
> Da aprire per primo quando ci si avvicina a LIMET 2.0.

## 1. Prima di tutto: orientamento

| # | Documento | Percorso | Perché leggerlo |
| - | --------- | -------- | --------------- |
| 1 | README del repository (bilingue) | `../README.md` | Panoramica IT/EN e comando di install |
| 2 | Manuale completo del framework | `FRAMEWORK_MANUAL.md` | Architettura, ciclo di vita, regole binding |
| 3 | Checklist di onboarding | `ONBOARDING_CHECKLIST.md` | Passi per partire su un progetto |
| 4 | Guida Setup (SPA, IT/EN) | `../guides/it/limet-setup.html` · `../guides/en/limet-setup.html` | Avvio dashboard + Qdrant/Ollama/Postgres (Docker e locale) + config |
| 5 | Guida Project Init (SPA, IT/EN) | `../guides/it/limet-project-init.html` · `../guides/en/limet-project-init.html` | Tre colonne, documenti, pagine dashboard, multi-modulo, link progetti |
| 6 | Guida Workflow (SPA, IT/EN) | `../guides/it/workflow.html` · `../guides/en/workflow.html` | Come creare un progetto, una feature, gestire un bug |

## 2. Componenti del plugin

| Componente | Percorso | Ruolo |
| ---------- | -------- | ----- |
| Skill (6) | `skills/limet-{new,task,test,bug,archive,analyze}/SKILL.md` | Ciclo di vita + analisi progetto (`analyze`) |
| Hook (6) | `hooks/{resume,intent,guardrail,changelog,precompact,reminder}.sh` + `hooks/hooks.json` | resume ciclo, intento, blocco build/commit/distruttivi, change log, stato pre-compattazione, reminder |
| Subagent (3) | `agents/{limet-writer,limet-gate,limet-analyzer}.md` | scrittura documenti, validazione §1.5 + drift, analisi progetto |
| MCP (3) | `mcp/{cerebro,graphify,db}/` | RAG documentale (Qdrant), knowledge graph codice, SQL read-only |
| Dashboard | `dashboard/` | init / progetti / re-index / setup / analizza su :8787 |
| Comandi | `commands/{limet-dashboard,limet-dashboard-stop}.md` | `/limet-dashboard`, `/limet-dashboard-stop` |
| Script (1) | `scripts/run-tests.sh` | esegue i test, esito compatto in TEST_EXECUTION, log distrutto se OK |

## 3. Configurazione (per-progetto)

| File | Percorso | Ruolo |
| ---- | -------- | ----- |
| Default | `config/config.yaml` | qdrant/ollama/db per progetto, senza segreti |
| Override + segreti | `config/config.local.yaml` | gitignored (password) |
| Loader condiviso | `config/loader.py` | deep-merge config.yaml ← config.local.yaml |
| Lingua | `config/config.yaml` → `language` | `it`/`en` per i documenti prodotti |

## 4. Documenti generati dal ciclo

In `limet/changes/<data-slug>/` (poi `limet/archive/<slug>/`):
`CHANGE_PROPOSAL` · `SPEC` · `PLAN` · `TASK_LIST` · `TEST_PLAN` · `E2E_VERIFICATION` ·
`DECISIONS` · `TEST_EXECUTION` · `BUG_REPORT` · `ARCHIVE_ENTRY`.

## 5. Documentazione tecnica del progetto LIMET

`docs/ARCHITECTURE.md` · `docs/SKILLS.md` · `docs/HOOKS.md` · `docs/MCP.md` ·
`docs/SUBAGENTS.md` · `docs/PLUGIN.md` · `docs/DASHBOARD.md` · `docs/SETUP.md` ·
`docs/MIGRATION.md` · `docs/OPTIMIZATIONS.md`.

## 6. Riferimento rapido

- **Nuova feature** → `/limet-new "feature"` (genera i documenti)
- **Implementare un task** → `/limet-task N` (brief + implementazione + change log)
- **Testare** → `/limet-test` (piano) + `!bash scripts/run-tests.sh <comando>` (esecuzione, esito in TEST_EXECUTION)
- **Segnalare un bug** → `/limet-bug "descrizione"`
- **Archiviare** → `/limet-archive` (solo lavoro verificato)
- **Analizzare un progetto** → dashboard Analizza → `/limet-analyze`
- **Dashboard** → `/limet-dashboard` → http://127.0.0.1:8787

## 7. Template

I template dei documenti sono **inline nelle skill** (`skills/limet-*/SKILL.md`).
I vecchi template 1.0 in file separati (`limet/templates/`) sono stati rimossi.
