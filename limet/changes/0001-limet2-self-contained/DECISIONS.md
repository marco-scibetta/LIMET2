# Decisioni (ADR-lite)

| # | Decisione | Stato | Data | Contesto | Conseguenze |
| - | --------- | ----- | ---- | -------- | ----------- |
| 1 | `claude plugin validate` non-strict (warning "CLAUDE.md root" by-design) | `accepted` | 2026-11-20 | repo root = plugin root; CLAUDE.md è policy progetto, non contesto plugin | e2e install usa `validate .` |
| 2 | Dashboard 5 pagine: Setup sostituisce Config DB, Artefatti rimossa | `accepted` | 2026-11-20 | ogni pagina = un'azione; Artefatti read-only ridondante | SPEC R8: 6→5 pagine |
| 3 | Monoprocesso: backend FastAPI serve anche frontend buildato | `accepted` | 2026-11-20 | niente BE+FE separati a mano | un solo `python dashboard/run.py` |
| 4 | Slug `YYYY-MM-DD-slug` per `changes/` e `archive/` | `accepted` | 2026-11-20 | sortabilità | devia da 1.0 `NNNN-slug` |
| 5 | Graphify nativo `graphify-mcp` (package `graphifyy`), non vendorizzato | `accepted` | 2026-11-20 | MCP nativo già esistente | niente `mcp/graphify/` nel repo |
| 6 | Config per-progetto (`projects.<slug>.{qdrant,ollama,db}`) + loader condiviso | `accepted` | 2026-11-20 | db diverso per progetto, qdrant/ollama condivisi | Setup per-progetto |
| 7 | Lingua IT/EN selezionabile da dashboard, documenti nella lingua scelta | `accepted` | 2026-11-20 | utente non deve capire "scegli lingua" visivamente | `language` in config + flag UI |

> Stato: `accepted` o `superseded`. Registrate solo decisioni hard-to-reverse.
