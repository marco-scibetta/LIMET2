# LIMET 2.0 — MCP: cerebro + graphify + db

Tre "context provider" esposti come **server MCP**. Claude chiama i tool nativamente; i segreti stanno nel config, mai nel contesto.

## CEREBRO — RAG documentale (`mcp/cerebro/`)

Il codice RAG (register/ingest/query) è **dentro il repo**, avvolto in un server MCP stdio.

| Tool MCP | Scopo |
|---|---|
| `cerebro_search(query, project, limit)` | cerca frammenti rilevanti |
| `cerebro_count(project)` | numero chunk |
| `cerebro_list(project)` | collezioni Qdrant del progetto |
| `cerebro_ingest(project)` | re-indicizza |
| `cerebro_register(project, path)` | registra progetto |

Runtime esterno: **Qdrant** + **Ollama** (nativi o Docker). L'ingestion usa **batch embedding** (`/api/embed`, N chunk = 1 chiamata), non un POST per chunk.

## GRAPHIFY — knowledge graph (MCP nativo)

Graphify **non è vendorizzato**: si usa l'entry point nativo `graphify-mcp` del package `graphifyy==0.9.32` (pinnato in `pyproject.toml`).

| Tool MCP | Scopo |
|---|---|
| `graphify_query(domanda)` | domanda sul grafo |
| `graphify_path(a, b)` | relazione tra simboli |
| `graphify_explain(simbolo)` | spiegazione simbolo |
| `graphify_update()` | rigenera grafo |

L'indicizzazione del codice avviene con `graphify extract <root> --code-only` (AST, senza LLM).

## DB — database relazionale (Postgres, read-only)

Terzo contesto: i dati del database applicativo. **Generico** (Postgres, poi altri driver) e **sicuro**: le credenziali non passano mai dall'LLM.

### Config: `config/config.yaml` + `config/config.local.yaml` (per-progetto)

```yaml
# config.yaml (committed, senza segreti)
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

Il loader condiviso `config/loader.py` fa il deep-merge. La password non è mai mostrata (mascherata in GET).

### Tool

| Tool | Scopo |
|---|---|
| `db_query(sql, project)` | esegue SELECT read-only, row-limited |

### Regole di sicurezza (binding)

1. **Read-only**: solo SELECT (reject INSERT/UPDATE/DELETE/DDL via regex).
2. **Row limit** (default 100 righe).
3. **Segreti gitignored** (`config.local.yaml`), mai nel repo né nel prompt.
4. **Nessun segreto in output**: i tool non restituiscono mai host/user/password.

## Dichiarazione nel plugin — `.mcp.json`

```json
{
  "mcpServers": {
    "cerebro": { "command": "python", "args": ["mcp/cerebro/server.py"] },
    "graphify": { "command": "graphify-mcp", "args": [] },
    "db": { "command": "python", "args": ["mcp/db/server.py"] }
  }
}
```

## Principio

> **Cerebro (RAG) dentro il repo, Graphify (KG) nativo, DB (dati) read-only.** I segreti stanno nel config (gitignored) e li legge solo il server MCP.

### Contesto = evidenza, non certezza

Il contesto recuperato è **evidenza da verificare**, non verità: va confermato contro la fonte autorevole (codice, test, contratti) prima di agire. I context provider **non contengono mai segreti**.
