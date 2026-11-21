# LIMET 2.0 — Migrazione da 1.0

Come passare da un progetto che usa LIMET 1.0 a LIMET 2.0.

## Cosa cambia per l'utente

| Azione | LIMET 1.0 | LIMET 2.0 |
|---|---|---|
| Attivare LIMET | `limet.ps1` / `limet.sh` | `claude plugin install limet` + `/limet-new` |
| Nuova feature | riempire CHANGE_PROPOSAL + SPEC + PLAN + TASK_LIST a mano | `/limet-new <idea>` |
| Implementare | riempire TASK + change log a mano | `/limet-task <n>` (change log automatico) |
| Verificare | riempire TEST_PLAN + TEST_EXECUTION a mano | `/limet-test` |
| Archiviare | spostare i file a mano | `/limet-archive` |
| Contestualizzare | leggere il CLAUDE.md con blocchi CEREBRO/GRAPHIFY | MCP `cerebro` + `graphify` (tool nativi) |

## Passi di migrazione

1. **Installa il plugin**: `claude plugin install limet`.
2. **Sostituisci il vecchio CLAUDE.md**: togli i blocchi `<!-- CEREBRO:START/END -->` e `<!-- GRAPHIFY:START/END -->` (ora sono MCP), tieni le policy build/test/task/test.
3. **I documenti 1.0 esistenti restano validi**: sono gli stessi artefatti (SPEC, PLAN, TASK_LIST…). LIMET 2.0 li legge e li aggiorna. Nessuna conversione necessaria.
4. **Re-indicizza con CEREBRO**: se usavi il RAG, `cerebro_ingest(project)` per allineare.
5. **Verifica Graphify**: se usavi il KG, assicurati che il server `graphify` MCP sia raggiungibile.

## Compatibilità

- **I file** (`limet/`, i template già riempiti) → **compatibili al 100%**: LIMET 2.0 non cambia il formato dei documenti, cambia *chi li genera e chi li compila*.
- **Le regole** (§1.1–§1.5) → invariare; cambia solo il meccanismo (testo → hook).

## Cosa NON serve migrare

- Gli script `limet.ps1`/`limet.sh` → sostituiti dal plugin.
- La skill-guida CEREBRO → sostituita dal MCP `cerebro` (stessi script, **spostati dentro** `mcp/cerebro/`).
- Il CLI Graphify → sostituito dal MCP `graphify` (nativo `graphify-mcp`, package `graphifyy`).

## Self-contained

LIMET 2.0 è **un solo repo**: niente `<repo-cerebro>` esterno. Cerebro e DB vivono in `mcp/`, Graphify è un MCP nativo (`graphify-mcp`). Restano esterni solo Qdrant + Ollama + Postgres (infra).

## Rollback

Se qualcosa non va: disinstalla il plugin (`claude plugin uninstall limet`) e torni a LIMET 1.0 (i documenti non sono toccati).
