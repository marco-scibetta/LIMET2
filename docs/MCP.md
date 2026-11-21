# LIMET 2.0 — MCP: CEREBRO + GRAPHIFY (incorporati)

I due "context provider" diventano **server MCP dentro il repo LIMET** (`mcp/`), non esterni. **Thin wrapper + bundling: il codice dei motori viene portato DENTRO LIMET, non riscritto.** Claude chiama i tool nativamente, e l'utente installa un solo repo.

## CEREBRO — RAG documentale (bundled in `mcp/cerebro/`)

Stato attuale: repo separato `C:\Progetti\CEREBRO` + skill-guida che orchestra script Python.

In 2.0: il codice RAG (register/ingest/query) **viene copiato dentro** `mcp/cerebro/` e avvolto in un server MCP. **Zero riscrittura della logica, solo riposizionamento.**

| Tool MCP | Scopo |
|---|---|
| `cerebro_search(project, query, limit)` | cerca frammenti rilevanti |
| `cerebro_count(project)` | numero chunk |
| `cerebro_list()` | elenco progetti |
| `cerebro_ingest(project)` | re-indicizza |
| `cerebro_register(name, docs, root)` | registra progetto |

Runtime esterno (infra): Qdrant + Ollama — **nativi** (binario Qdrant + installer Ollama), Docker opzionale. Non codice, solo servizi locali.

**Ottimizzazione ingestion (importante, trovata nell'audit):** oggi `ingest_docs.py` fa **un POST HTTP a Ollama per ogni chunk** (`/api/embeddings`), quindi un PDF con 300 chunk = 300 round-trip → è il vero collo di bottiglia della lentezza (non serve GPU). In 2.0: **batch `/api/embed`** (lista di chunk in una sola chiamata) oppure **`fastembed`/ONNX in-process** (niente Ollama). 10-50× più veloce su CPU. Vedi OPTIMIZATIONS §8.

## GRAPHIFY — knowledge graph (bundled in `mcp/graphify/`)

Stato attuale: CLI esterno (`graphify query/path/explain/update`), sorgente non localizzato.

In 2.0: il sorgente di Graphify **viene portato dentro** `mcp/graphify/` ed esposto come MCP. (Prima dell'implementazione: localizzare il sorgente.)

| Tool MCP | Scopo |
|---|---|
| `graphify_query(domanda)` | domanda sul grafo |
| `graphify_path(a, b)` | relazione tra simboli |
| `graphify_explain(simbolo)` | spiegazione simbolo |
| `graphify_update()` | rigenera grafo |

## DB — database relazionale (Postgres, generico)

Terzo contesto per l'inferenza: i dati del database applicativo. **Generico** (Postgres prima, poi altri driver cambiando solo il driver) e **sicuro**: le credenziali **non passano mai dall'LLM e non stanno nel repo**.

### Config: `.env_db` (gitignored, MAI nel repo né nel prompt)

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=limet_readonly
DB_PASSWORD=***
DB_SSLMODE=require
```

Commitare **`.env_db.example`** (stesso schema, valori placeholder) come template; il `.env_db` vero è gitignored. In più, proteggere il file a filesystem: solo l'utente lo legge (`chmod 600` su Linux, ACL su Windows) — il segreto va protetto anche fuori da git, non solo dal versionamento.

### Il server MCP legge `.env_db`, l'LLM NO

Il tool MCP assembla la connection string **dentro il server**. L'LLM chiama `db_query(...)` e vede **solo i risultati**, mai host/user/password.

### Tool

| Tool | Scopo |
|---|---|
| `db_schema()` | elenco tabelle/colonne (per capire lo schema) |
| `db_query(sql)` | esegue SELECT read-only |
| `db_describe(tabella)` | struttura di una tabella |

### Regole di sicurezza (binding)

1. **Read-only**: solo SELECT (reject INSERT/UPDATE/DELETE/DDL/COMMENT). In più, **utente DB dedicato** (`limet_readonly`) con grant SELECT-only — doppia protezione.
2. **Row limit** (default 100 righe) + **timeout** → niente query enormi che riempiono il contesto.
3. **`.env_db` gitignored** → mai nel repo, mai nel prompt.
4. **Nessun segreto in output**: i tool non restituiscono mai host/user/password/config.

## Dichiarazione nel plugin — `.mcp.json`

```json
{
  "mcpServers": {
    "cerebro": { "command": "python", "args": ["${CLAUDE_PLUGIN_ROOT}/mcp/cerebro/server.py"] },
    "graphify": { "command": "python", "args": ["${CLAUDE_PLUGIN_ROOT}/mcp/graphify/server.py"] },
    "db": { "command": "python", "args": ["${CLAUDE_PLUGIN_ROOT}/mcp/db/server.py"] }
  }
}
```

## Principio

> **Stesso motore, un solo repo, interfaccia nativa.** Cerebro (RAG), Graphify (KG) e DB (dati) vivono dentro `mcp/`. I segreti (`.env_db`) stanno fuori dal repo e fuori dal contesto: li legge solo il server MCP.

### Contesto = evidenza, non certezza (idea da ECC)

Il contesto recuperato (Cerebro/db) è **evidenza da verificare**, non verità: va confermato contro la fonte autorevole (codice, test, contratti) prima di agire. E i context provider **non contengono mai segreti** (mai credenziali/token nei dati indicizzati).
