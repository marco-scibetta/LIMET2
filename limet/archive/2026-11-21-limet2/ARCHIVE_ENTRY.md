# Archivio — 2026-11-21-limet2

## Metadati
- Slug: `2026-11-21-limet2`
- Data archiviazione: 2026-11-21
- Stato: `COMPLETATA` (verificata)

## Sintesi
LIMET 2.0 — plugin Claude Code self-contained. Riscrittura di LIMET 1.0:
5 skill ciclo di vita, 4 hook deterministici, 2 subagent, 3 MCP (cerebro/graphify/db),
dashboard React/FastAPI monoprocesso, config per-progetto.

Feature: workspace multi-modulo, progetti correlati (link), lingua IT/EN, guide HTML (IT+EN).

## Esito test
- `python -m pytest tests -v` → **33 passed** (config loader, db guardrail, hook, dashboard, project config).
- e2e: ciclo completo mini-todo (15 test), workspace multi-modulo, link progetti.

## Documenti inclusi
CHANGE_PROPOSAL, SPEC, DESIGN, TASK, TASK_LIST, E2E_VERIFICATION, TEST_PLAN, TEST_EXECUTION, DECISIONS.

## Scostamenti rispetto alla proposta
- SPEC R8: 6→5 pagine (Artefatti rimossa, Config DB→Setup).
- Graphify nativo `graphify-mcp` (non vendorizzato in `mcp/graphify/`).
- Slug `YYYY-MM-DD-slug` per changes/archive/.
- Feature extra non previste nel piano: workspace, link, lingua, guide.
