# LIMET 2.0 — MCP: cerebro + graphify + db

Three "context providers" exposed as **MCP servers**. Claude calls the tools natively; secrets live in the config, never in the context.

## CEREBRO — document RAG (`mcp/cerebro/`)

The RAG code (register/ingest/query) is **inside the repo**, wrapped in a stdio MCP server.

| MCP tool | Purpose |
|---|---|
| `cerebro_search(query, project, limit)` | search relevant fragments |
| `cerebro_count(project)` | chunk count |
| `cerebro_list(project)` | the project's Qdrant collections |
| `cerebro_ingest(project)` | re-index |
| `cerebro_register(project, path)` | register project |

External runtime: **Qdrant** + **Ollama** (native or Docker). Ingestion uses **batch embedding** (`/api/embed`, N chunks = 1 call), not one POST per chunk.

## GRAPHIFY — knowledge graph (native MCP)

Graphify is **not vendored**: it uses the native `graphify-mcp` entry point of the `graphifyy[mcp]==0.9.32` package (pinned in `pyproject.toml`, the `[mcp]` extra is mandatory for the MCP SDK).

| MCP tool | Purpose |
|---|---|
| `graphify_query(question)` | question about the graph |
| `graphify_path(a, b)` | relationship between symbols |
| `graphify_explain(symbol)` | symbol explanation |
| `graphify_update()` | regenerate graph |

Code indexing happens with `graphify extract <root> --code-only` (AST, no LLM).

## DB — relational database (Postgres, read-only)

Third context: the application database data. **Generic** (Postgres, then other drivers) and **safe**: credentials never pass through the LLM.

### Config: `config/config.yaml` + `config/config.local.yaml` (per-project)

```yaml
# config.yaml (committed, no secrets)
projects:
  my-app:
    db:
      host: localhost
      port: 5432
      database: mydb
      user: myuser
```

```yaml
# config.local.yaml (gitignored)
projects:
  my-app:
    db:
      password: "***"
```

The shared loader `config/loader.py` does the deep-merge. The password is never shown (masked in GET).

### Tools

| Tool | Purpose |
|---|---|
| `db_query(sql, project)` | runs read-only SELECT, row-limited |

### Security rules (binding)

1. **Read-only**: only SELECT (reject INSERT/UPDATE/DELETE/DDL via regex).
2. **Row limit** (default 100 rows).
3. **Secrets gitignored** (`config.local.yaml`), never in the repo nor in the prompt.
4. **No secrets in output**: the tools never return host/user/password.

## Plugin declaration — `.mcp.json`

```json
{
  "mcpServers": {
    "cerebro": { "command": "python", "args": ["mcp/cerebro/server.py"] },
    "graphify": { "command": "graphify-mcp", "args": [] },
    "db": { "command": "python", "args": ["mcp/db/server.py"] }
  }
}
```

## Principle

> **Cerebro (RAG) inside the repo, Graphify (KG) native, DB (data) read-only.** Secrets live in the config (gitignored) and are read only by the MCP server.

### Context = evidence, not certainty

The retrieved context is **evidence to verify**, not truth: it must be confirmed against the authoritative source (code, tests, contracts) before acting. Context providers **never contain secrets**.
