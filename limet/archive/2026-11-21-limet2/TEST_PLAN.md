# Piano di test — LIMET 2.0 (change 0001-limet2-self-contained)

## Riferimenti
- Proposta/SPEC: CHANGE_PROPOSAL.md, SPEC.md
- Task collegati: #1–#23 + feature extra (workspace, link, lingua, guide)

## Ambito della verifica
Componenti del plugin: config loader, hook (intent/guardrail), MCP db (read-only),
cerebro/project_config (slug, collection, link), dashboard (mask segreti, discover moduli).

## Unit test previsti (pytest, `tests/`)

| # | File | Cosa verifica |
| - | ---- | ------------- |
| U1 | `test_config_loader.py` | deep-merge, project_config defaults, shared qdrant/ollama, language |
| U2 | `test_db_server.py` | reject DDL/DML, reject multi-statement, reject non-select/empty, db_for fallback |
| U3 | `test_hooks.py` | intent feature/bug, no falso positivo, related projects, guardrail block/allow |
| U4 | `test_dashboard.py` | mask password, guide lang, discover moduli (solo con docs/) |
| U5 | `test_project_config.py` | sanitize slug, collection_for, collections_for con link |

### Autorevisione della qualità
- [x] Ogni assert può fallire per il motivo dichiarato
- [x] Atteso non derivato dall'oggetto sotto test
- [x] Contratto verificato (input assenti/vuoti/non validi), non solo happy path
- [x] Bug reali coperti da regressione: multi-statement (`SELECT 1; DROP`), falso positivo intent, discover moduli goloso

## Test e2e previsti

| # | Scenario | Esito |
| - | -------- | ----- |
| E1 | Ciclo completo su progetto fittizio (mini-todo): new→task→test→bug→archive | 15 pytest verdi |
| E2 | Workspace multi-modulo: init + auto-discovery + 1 collection | 2 moduli scoperti |
| E3 | Progetti correlati: link A↔B + ricerca cross-collection | search in A trova doc di B |

## Dati di test necessari
- `config/config.yaml` + `config.local.yaml` (limet2_test_dummy, limet2_ws_test).
- Qdrant (6333) + Ollama (11434) per l'e2e.

## Chi esegue
- Scrittura test: agente / Esecuzione: agente (autorizzato per la verifica).

## Comandi di test rieseguibili
- `python -m pytest tests -v`
- `claude plugin validate .`
- `npm run build` (in `dashboard/frontend`)
