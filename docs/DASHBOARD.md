# LIMET 2.0 — Dashboard React (ops)

La dashboard è l'interfaccia **web per le operazioni**, non per il lavoro. Il lavoro lo fa Claude; le ops le fa l'umano con una GUI.

## Principio di separazione

| | Claude (MCP + skill) | Dashboard React |
|---|---|---|
| Ruolo | **il lavoro** | **le ops** |
| Cosa | generare spec/task, implementare, query contesto | init/setup, re-index, status, config, monitoraggio |
| Interazione | conversazionale | GUI |
| Perché | è il core spec-driven | una GUI batte una chat per ops ripetitive |

Regola: **se una funzione è più comoda in conversazione, sta in chat, non nella UI.** La dashboard non duplica il lavoro di Claude.

## Architettura: un backend, due frontend

```
React Dashboard ──► REST API (stessa logica) ◄── Claude MCP
                    ┌────────────────────┐
                    │  backend condiviso │
                    │  cerebro / graphify│
                    │  / db + ciclo limet│
                    └────────────────────┘
```

Il backend è lo stesso dei server MCP (`mcp/`). La dashboard parla con una **REST API** (o direttamente col backend), Claude parla con **MCP**. Stessa logica, due frontend.

## Stack

- **React** (Vite) + TypeScript.
- Nessun framework UI pesante: componenti semplici, tema scuro professionale.
- Stato locale (React state / localStorage), niente backend di stato separato: il backend è già nei server MCP/REST.

## Design / grafica (moderna professionale, non '90s)

"Super avanzata" = **grafica moderna professionale**, non più funzioni. Il launcher 1.0 (HTML vanilla) sembra anni '90: va ridisegnato, non solo portato in React.

Requisiti grafici:
- **Design system** con token (palette scura professionale, accent coerente, tipografia moderna, spaziature). Niente "sito anni '90".
- **Layout**: sidebar di navigazione + pannello contenuto; dashboard con card, badge di stato, tabelle, sparkline.
- **Dark mode** di default (coerente col contesto dev), con eventuale toggle.
- **Micro-interazioni** curate (hover, stato attivo, loading, streaming log), ma sobrie.
- **Responsive** (desktop first, ma leggibile su schermi stretti).
- Tipografia e palette scelte con criterio (si può usare il design system della skill `ui-ux-pro-max`: 67 stili, 96 palette, 57 coppie di font — da applicare, non inventare a caso).

La **qualità visiva** è un requisito, non un optional: la dashboard è la vetrina del prodotto.

## Pagine (le sezioni della dashboard)

1. **Init / Setup wizard** — crea progetto: percorso, lingua (it/en), modalità (progetto/workspace), progetti correlati, contesto (cerebro/graphify/db). Riusa il flusso del launcher.
2. **Progetti** — lista, aggiungi, rimuovi, collega/scollega (progetti correlati).
3. **Re-index** — modalità incrementale / forza / pulizia; log in streaming.
4. **Status / Monitoraggio** — collection Qdrant, chunk count, stato Qdrant/Ollama/MCP/db, progetti registrati.
5. **Config DB** — gestione `.env_db` (host, porta, db, utente read-only, sslmode). Mai mostrare la password in chiaro.
6. **Artefatti** — visualizzazione read-only dei documenti LIMET generati (spec, plan, task list, report, archive).

## API (riuso launcher.html)

Il launcher 1.0 espone già: `/api/info`, `/api/check`, `/api/run` (streaming), `/api/stop`, `/api/shutdown`. In 2.0:

| Endpoint 1.0 | 2.0 |
|---|---|
| `/api/info` | stato graphify/cerebro → esteso con db + MCP status |
| `/api/check` | auto-detect progetto (collisione slug, registrato, collection) → invariato |
| `/api/run` | azioni create/update/status/remove/adddocs/createrelated/unrelate (streaming) → invariato |
| `/api/stop` | ferma operazione → invariato |
| `/api/shutdown` | chiudi launcher → invariato |
| — | `/api/db/test` (verifica connessione read-only) |
| — | `/api/db/schema` (elenco tabelle) |

Il backend REST riusa la **stessa logica** dei server MCP: nessuna duplicazione.

## Cosa NON copre la dashboard

- Generare spec/plan/task (→ Claude, via skill).
- Implementare codice (→ Claude).
- Query di contesto durante il lavoro (→ Claude, via MCP cerebro/graphify/db).

## Riuso del launcher.html

Il `launcher.html` 1.0 (già una SPA vanilla con `/api/*` + streaming log) è la **base**:
- La logica (azioni, campi, auto-detect, streaming) si porta in React.
- Si estende con: **db config**, **monitoraggio MCP**, **artefatti read-only**.
- Si mantiene il tema scuro e l'UX (pill, log streaming, stop).

## Vincolo (non overingegnerizzare)

La dashboard fa **le ops che un umano farebbe a mano**. Niente funzioni superflue: ogni pagina mappa un'azione reale (init/reindex/status/config/artefatti). Se serve solo a Claude, non va nella UI. **"Super avanzata" = grafica moderna professionale, non più funzionalità.**
