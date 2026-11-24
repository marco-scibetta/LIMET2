# LIMET 2.0 — Migration from 1.0

How to move from a project using LIMET 1.0 to LIMET 2.0.

## What changes for the user

| Action | LIMET 1.0 | LIMET 2.0 |
|---|---|---|
| Activate LIMET | `limet.ps1` / `limet.sh` | `claude plugin install limet` + `/limet-new` |
| New feature | fill CHANGE_PROPOSAL + SPEC + PLAN + TASK_LIST by hand | `/limet-new <idea>` |
| Implement | fill TASK + change log by hand | `/limet-task <n>` (automatic change log) |
| Verify | fill TEST_PLAN + TEST_EXECUTION by hand | `/limet-test` |
| Archive | move files by hand | `/limet-archive` |
| Contextualize | read CLAUDE.md with CEREBRO/GRAPHIFY blocks | MCP `cerebro` + `graphify` (native tools) |

## Migration steps

1. **Install the plugin**: `claude plugin install limet`.
2. **Replace the old CLAUDE.md**: remove the `<!-- CEREBRO:START/END -->` and `<!-- GRAPHIFY:START/END -->` blocks (now MCP), keep the build/test/task/test policies.
3. **Existing 1.0 documents remain valid**: they are the same artifacts (SPEC, PLAN, TASK_LIST…). LIMET 2.0 reads and updates them. No conversion needed.
4. **Re-index with CEREBRO**: if you used the RAG, `cerebro_ingest(project)` to align.
5. **Verify Graphify**: if you used the KG, make sure the `graphify` MCP server is reachable.

## Compatibility

- **The files** (`limet/`, the already-filled templates) → **100% compatible**: LIMET 2.0 does not change the document format, it changes *who generates them and who fills them*.
- **The rules** (§1.1–§1.5) → unchanged; only the mechanism changes (text → hook).

## What does NOT need migrating

- The `limet.ps1`/`limet.sh` scripts → replaced by the plugin.
- The CEREBRO guide skill → replaced by the MCP `cerebro` (same scripts, **moved inside** `mcp/cerebro/`).
- The Graphify CLI → replaced by the MCP `graphify` (native `graphify-mcp`, package `graphifyy`).

## Self-contained

LIMET 2.0 is **one repo**: no external `<cerebro-repo>`. Cerebro and DB live in `mcp/`, Graphify is a native MCP (`graphify-mcp`). Only Qdrant + Ollama + Postgres stay external (infra).

## Rollback

If something goes wrong: uninstall the plugin (`claude plugin uninstall limet`) and you are back to LIMET 1.0 (the documents are untouched).
