# LIMET 2.0 — Dashboard (ops)

La dashboard è l'interfaccia **web per le operazioni**, non per il lavoro. Il lavoro lo fa Claude; le ops le fa l'umano con una GUI.

## Principio di separazione

| | Claude (MCP + skill) | Dashboard |
|---|---|---|
| Ruolo | **il lavoro** | **le ops** |
| Cosa | generare spec/task, implementare, query contesto | init, re-index, status, setup/config |
| Interazione | conversazionale | GUI |

Regola: **se una funzione è più comoda in conversazione, sta in chat, non nella UI.** Ogni pagina = un'azione reale.

## Architettura: monoprocesso

```
React (Vite) ──► REST API ◄── Claude MCP
                 ┌─────────────────┐
                 │ backend FastAPI │  (serve anche il frontend buildato)
                 │ cerebro/db      │
                 └─────────────────┘
```

Il backend FastAPI **serve anche il frontend buildato** (`dist/`): un solo processo, un solo comando.

```bash
python dashboard/run.py     # builda se serve + avvia su :8787
/limet-dashboard            # comando slash equivalente
```

## Pagine (5)

1. **Status** — stato di Qdrant/Ollama + progetti registrati.
2. **Init** — registra un progetto (nome + percorso docs): in un colpo fa **register + graphify extract + ingestion Qdrant**. Una combo propone i progetti già esistenti.
3. **Progetti** — slug, root, percorsi docs dei progetti registrati.
4. **Re-index** — incrementale / forza / pulizia (prune); combo progetto + percorso docs.
5. **Setup** — configurazione **per progetto** (Qdrant, Ollama, DB), salvata in `config.local.yaml`. Password mai mostrata. Include "Test connessione DB".

## API

| Endpoint | Scopo |
|---|---|
| `GET /api/info` | nome + versione + stato |
| `GET /api/status` | Qdrant/Ollama reachable + progetti |
| `GET /api/projects` | progetti registrati (slug, root, docs) |
| `POST /api/init` | register + graphify + ingestion |
| `POST /api/reindex` | re-ingestion (incremental/force/prune) |
| `GET /api/config?project=` | config di un progetto (password mascherata) |
| `POST /api/config` | salva config per-progetto in config.local.yaml |
| `POST /api/config/test` | test connessione DB |
| `GET /api/browse` | file browser (sottocartelle) |

## Cosa NON copre la dashboard

- Generare spec/plan/task (→ Claude, via skill).
- Implementare codice (→ Claude).
- Query di contesto durante il lavoro (→ Claude, via MCP).

## Vincolo (non overingegnerizzare)

La dashboard fa **le ops che un umano farebbe a mano**. Ogni pagina mappa un'azione reale; se serve solo a Claude, non va nella UI.
