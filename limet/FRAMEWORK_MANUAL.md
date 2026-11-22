# LIMET 2.0 — Manuale

Spec-driven engineering per Claude Code, come plugin self-contained.

## Cos'è

LIMET sostituisce il flusso manuale 1.0 con un plugin Claude Code che guida
lo sviluppo spec-driven con tracciabilità completa: proposal → spec → plan → task → test → archive.

## Installazione

```bash
pip install -e .            # dipendenze Python (qdrant-client, fastapi, graphifyy, …)
claude plugin marketplace add ./
claude plugin install limet
claude plugin validate .    # non-strict: il warning CLAUDE.md alla root è by-design
```

## Architettura

| Componente | Cosa fa |
| ---------- | ------- |
| **Skill** (5) | `/limet-new`, `/limet-task`, `/limet-test`, `/limet-bug`, `/limet-archive` |
| **Hook** (6) | `resume.sh` (riprende ciclo attivo), `intent.sh` (rileva intento), `guardrail.sh` (blocca build/commit/distruttivi), `changelog.sh` (registro auto), `precompact.sh` (stato pre-compattazione), `reminder.sh` (ricorda test/archive) |
| **Subagent** (2) | `limet-writer` (scrive doc), `limet-gate` (valida §1.5 + drift) |
| **MCP** (3) | `cerebro` (RAG Qdrant), `graphify` (knowledge graph codice), `db` (SQL read-only) |
| **Dashboard** | init / progetti / re-index / setup (config per-progetto) su :8787 |
| **Comandi** | `/limet-dashboard` (avvia), `/limet-dashboard-stop` (ferma) |

## Ciclo di vita

```
limet-new → limet-task → limet-test → (limet-bug) → limet-archive
```

1. **new** — genera i documenti in `limet/changes/<data-slug>/`.
2. **task** — esegue un task con brief di 2-3 righe e aggiorna il change log.
3. **test** — genera TEST_PLAN + TEST_EXECUTION con comandi rieseguibili. L'esecuzione spetta all'utente: `!bash scripts/run-tests.sh` (o `!bash scripts/run-tests.sh <comando>`) registra l'esito in TEST_EXECUTION senza sporcare il contesto e distrugge i log temporanei se OK.
4. **bug** — report bug strutturato (se serve).
5. **archive** — sposta il lavoro verificato in `limet/archive/<slug>/`.

## Configurazione (per-progetto)

`config/config.yaml` (default committed) + `config/config.local.yaml` (override + segreti, gitignored).

```yaml
# config.yaml
projects:
  <slug>:
    qdrant: { url: http://localhost:6333 }
    ollama: { url: http://localhost:11434, model: nomic-embed-text }
    db: { host: localhost, port: 5432, database: mydb, user: myuser }
```

```yaml
# config.local.yaml (password mai in config.yaml)
projects:
  <slug>:
    db: { password: "..." }
```

Loader condiviso: `config/loader.py` (deep-merge config.yaml ← config.local.yaml).

## Dashboard

- `python dashboard/run.py` (builda se serve + serve API/UI su :8787).
- **Init**: nome progetto (combobox progetti esistenti) + percorso docs → fa register + graphify extract + ingestion Qdrant.
- **Re-index**: combobox progetto + percorso docs, modalità incrementale/forza/pulizia.
- **Setup**: combobox progetto → sezioni Qdrant/Ollama/DB → salva in config.local.yaml.

## Lingua (IT/EN)

- Flag 🇮🇹/🇬🇧 in alto a destra nella dashboard → cambia l'interfaccia e imposta `language` in `config.local.yaml`.
- Skill e agent leggono `language` da `config/config.yaml` → i documenti prodotti sono nella lingua scelta.

## Progetti multi-modulo (workspace)

- Cartella `X/` con più moduli (`X/module-a`, `X/module-b`), ognuno con la sua `docs/`.
- **Init** + spunta **"Workspace"** → registra `X` con tutti i docs (root + moduli) in **una** collection Qdrant, **un** grafo Graphify, **un** db.
- Ogni modulo ha la sua `limet/` (via cwd), ma Qdrant/Graphify/DB sono condivisi.
- Feature cross-modulo: sessione in `X`; feature locale: sessione nel modulo.

## Progetti correlati (link)

- Due progetti indipendenti A e B che interagiscono.
- **Progetti** → "Collega progetti": seleziona A e B → **Collega**.
- La ricerca Qdrant in A interroga A **e** B (collection extra).
- Un hook (UserPromptSubmit) ricorda a ogni prompt: "sei in X, collegato a Y — usa `cerebro_search` con `project=X`".

## Regole binding

- Spec first: proposal/plan prima di codice non banale.
- Ambiguità → domanda esplicita con data, mai assumere.
- Nessun task `done` senza strategia di verifica (unit + e2e + lint/type se configurati).
- Mai build/test in autonomia: dai il comando, l'utente lo esegue.
- Mai commit/push/migrate/deploy senza autorizzazione.
