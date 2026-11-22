# Graph Report - .  (2026-11-22)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 414 nodes · 646 edges · 39 communities (26 shown, 13 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `416d020c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- backend/server.py
- ingest_docs.py
- App.tsx
- test_hooks.py
- project_config.py
- package.json
- cerebro/server.py
- compilerOptions
- Feature: Assegnatario task (multi-utente)
- query_qdrant.py
- LIMET 2
- LIMET — nuovo ciclo ($ARGUMENTS)
- test_db_server.py
- marketplace.json
- db/server.py
- test_dashboard.py
- LIMET 2.0 — Install
- test_config_loader.py
- .mcp.json
- test_project_config.py
- limet-gate — validatore
- LIMET — esegui task ($ARGUMENTS)
- LIMET — test
- LIMET 2.0
- LIMET — archive
- LIMET — bug ($ARGUMENTS)
- limet-writer — scrittore documenti
- run.py
- changelog.sh
- guardrail.sh
- intent.sh
- precompact.sh
- reminder.sh
- resume.sh
- run-tests.sh
- limet

## God Nodes (most connected - your core abstractions)
1. `_run()` - 19 edges
2. `compilerOptions` - 16 edges
3. `get()` - 12 edges
4. `sanitize_project_name()` - 12 edges
5. `ingest_file()` - 10 edges
6. `load_registry()` - 10 edges
7. `Feature: Assegnatario task (multi-utente)` - 10 edges
8. `LIMET — nuovo ciclo ($ARGUMENTS)` - 10 edges
9. `_load_config()` - 8 edges
10. `collections_for()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `init()` --calls--> `_run()`  [INFERRED]
  dashboard/backend/server.py → tests/test_hooks.py
- `ingest_file()` --calls--> `assets_dir_for()`  [EXTRACTED]
  mcp/cerebro/ingest_docs.py → mcp/cerebro/project_config.py
- `main()` --calls--> `_default_project()`  [INFERRED]
  mcp/cerebro/limet_rag.py → mcp/cerebro/server.py
- `main()` --calls--> `collections_for()`  [EXTRACTED]
  mcp/cerebro/query_qdrant.py → mcp/cerebro/project_config.py
- `InitPage()` --calls--> `get()`  [EXTRACTED]
  dashboard/frontend/src/pages/InitPage.tsx → dashboard/frontend/src/api.ts

## Import Cycles
- None detected.

## Communities (39 total, 13 thin omitted)

### Community 0 - "backend/server.py"
Cohesion: 0.11
Nodes (42): BaseModel, browse(), ConfigBody, _db_conn_from(), _deep_merge(), _discover_modules(), get_config(), _guide_lang() (+34 more)

### Community 1 - "ingest_docs.py"
Cohesion: 0.09
Nodes (39): epub_to_markdown(), extract_image_names(), _next_image(), pdf_to_markdown(), Path, PDF / EPUB -> Markdown conversion with image extraction. Each function writes…, Resolve a src relative to the EPUB document into a normalized href., Extract the image names referenced in the markdown (order of appearance). (+31 more)

### Community 2 - "App.tsx"
Cohesion: 0.12
Nodes (26): get(), post(), req(), App(), NAV, PageId, Icon(), ICONS (+18 more)

### Community 3 - "test_hooks.py"
Cohesion: 0.14
Nodes (28): _make_change(), Unit test — hooks (intent, guardrail) via bash + JSON stdin., _run(), _run_reminder(), _run_script(), test_guardrail_allows_git_status(), test_guardrail_allows_ls(), test_guardrail_blocks_git_checkout_discard() (+20 more)

### Community 4 - "project_config.py"
Cohesion: 0.17
Nodes (27): assets_dir_for(), collection_for(), collections_for(), docs_paths_for(), extra_collections_for(), load_registry(), Path, Shared CEREBRO helper: project resolution -> Qdrant collection. Naming: project… (+19 more)

### Community 5 - "package.json"
Cohesion: 0.08
Nodes (24): dependencies, react, react-dom, devDependencies, @types/react, @types/react-dom, typescript, vite (+16 more)

### Community 6 - "cerebro/server.py"
Cohesion: 0.17
Nodes (20): deep_merge(), load_config(), _load_yaml(), project_config(), Loader condiviso per config.yaml + config.local.yaml (per-progetto)., Infrastruttura condivisa: qdrant/ollama dal primo progetto (o default)., shared_qdrant_ollama(), main() (+12 more)

### Community 7 - "compilerOptions"
Cohesion: 0.09
Nodes (21): compilerOptions, allowImportingTsExtensions, isolatedModules, jsx, lib, module, moduleResolution, noEmit (+13 more)

### Community 8 - "Feature: Assegnatario task (multi-utente)"
Cohesion: 0.12
Nodes (16): 1. Obiettivo, 2. Requisiti (scenari), 3.1 Assegnatario nella colonna esistente `Note` (nessun cambio di template), 3.2 Filtro `--mine` in `/limet-task` (opzionale, R4), 3.3 Impatto su hook esistenti, 3.4 Dove vive il template (per non dimenticare file), 3. Design dettagliato, 4. File da toccare (lista esaustiva) (+8 more)

### Community 9 - "query_qdrant.py"
Cohesion: 0.25
Nodes (11): load_env(), Load variables from .env in the repo root (if present)., resolve_project(), count(), get_embedding(), main(), qdrant_post(), scroll() (+3 more)

### Community 10 - "LIMET 2"
Cohesion: 0.18
Nodes (10): Comandi, Commands, Cosa fa, Da dove partire, Install, Installazione, LIMET 2, LIMET 2 (+2 more)

### Community 11 - "LIMET — nuovo ciclo ($ARGUMENTS)"
Cohesion: 0.18
Nodes (10): Documenti da generare, LIMET — nuovo ciclo ($ARGUMENTS), Regole binding, Template CHANGE_PROPOSAL, Template DECISIONS (ADR-lite — solo se emergono decisioni hard-to-reverse), Template E2E_VERIFICATION, Template PLAN, Template SPEC (+2 more)

### Community 12 - "test_db_server.py"
Cohesion: 0.22
Nodes (3): parametrize, Unit test — mcp/db/server.py guardrails (read-only, no secret)., test_reject_ddl_dml()

### Community 13 - "marketplace.json"
Cohesion: 0.25
Nodes (7): description, name, owner, name, url, plugins, $schema

### Community 14 - "db/server.py"
Cohesion: 0.46
Nodes (7): _connect(), _db_for(), _deep_merge(), _handle(), _load_config(), main(), query()

### Community 16 - "LIMET 2.0 — Install"
Cohesion: 0.29
Nodes (6): Install, LIMET 2.0 — Install, Requisiti, Uninstall, Update (dopo nuove feature), Verifica

### Community 18 - ".mcp.json"
Cohesion: 0.40
Nodes (5): graphify-mcp, python, cerebro, db, graphify

### Community 20 - "limet-gate — validatore"
Cohesion: 0.40
Nodes (4): Drift report, Fresh-eyes review, limet-gate — validatore, Output

### Community 21 - "LIMET — esegui task ($ARGUMENTS)"
Cohesion: 0.40
Nodes (4): Flusso, Formato del brief, LIMET — esegui task ($ARGUMENTS), Regole binding

### Community 22 - "LIMET — test"
Cohesion: 0.40
Nodes (4): LIMET — test, Regole binding, Template TEST_EXECUTION, Template TEST_PLAN

### Community 23 - "LIMET 2.0"
Cohesion: 0.50
Nodes (3): Binding rules, Context tools (MCP), LIMET 2.0

### Community 24 - "LIMET — archive"
Cohesion: 0.50
Nodes (3): LIMET — archive, Regole binding, Template ARCHIVE_ENTRY

### Community 25 - "LIMET — bug ($ARGUMENTS)"
Cohesion: 0.50
Nodes (3): LIMET — bug ($ARGUMENTS), Regole binding, Template BUG_REPORT

## Knowledge Gaps
- **109 isolated node(s):** `$schema`, `name`, `description`, `name`, `url` (+104 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_run()` connect `test_hooks.py` to `backend/server.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `init()` connect `backend/server.py` to `test_hooks.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `sanitize_project_name()` connect `project_config.py` to `ingest_docs.py`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **What connects `$schema`, `name`, `description` to the rest of the system?**
  _109 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `backend/server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11074197120708748 - nodes in this community are weakly interconnected._
- **Should `ingest_docs.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09268292682926829 - nodes in this community are weakly interconnected._
- **Should `App.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.12375533428165007 - nodes in this community are weakly interconnected._