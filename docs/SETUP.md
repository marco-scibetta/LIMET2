# LIMET 2.0 — Setup

Guida di installazione e configurazione per i membri del team.

## Cosa è

LIMET 2.0 è un plugin Claude Code per spec-driven engineering. Il repo stesso è il plugin e il marketplace: non serve pubblicarlo su alcun registry pubblico.

Il plugin spedisce:

| Componente | Cosa | Obbligatorio? |
|---|---|---|
| 5 skill | `limet-new`, `limet-task`, `limet-test`, `limet-archive`, `limet-bug` | Sì |
| 1 comando | `/limet-dashboard` | Sì |
| 2 agent | `limet-gate`, `limet-writer` | Sì |
| 4 hook | intento, guardrail, change log, reminder | No (vedi §4) |
| 3 MCP | `cerebro` (RAG), `db` (SQL read-only), `graphify` (code KG) | No (vedi §3) |

**Le skill funzionano anche senza MCP e senza hook.** MCP e hook sono componenti opzionali che arricchiscono il flusso.

---

## 1. Requisiti base

- Claude Code CLI (`claude`) 2.x
- Git + accesso al repo `marco-scibetta/LIMET2`
- (solo per MCP) Python ≥ 3.10 — vedi §3

---

## 2. Installazione

```bash
# 1. Clona il repo
git clone https://github.com/marco-scibetta/LIMET2
cd LIMET2

# 2. Passa al branch che contiene il plugin
git checkout dev

# 3. Registra il repo come marketplace locale
claude plugin marketplace add ./

# 4. Installa il plugin
claude plugin install limet@limet-marketplace
```

Alternativa one-liner (dentro Claude Code, Claude Code ≥ 2.1.275):

```
/plugin install limet --marketplace marco-scibetta/LIMET2
```

> Nota: la one-liner clona il **branch default** del repo (oggi `main`). Se il plugin vive su `dev`, usa il flusso clone + `git checkout dev` sopra.

### Verifica

1. **Riavvia Claude Code** (le skill si caricano a inizio sessione).
2. `claude plugin list` → deve comparire `limet@limet-marketplace` con stato `enabled`.
3. Nel menu `/` → deve esserci `/limet-dashboard`.
4. Chiedi in linguaggio naturale: *"voglio aggiungere una feature di login"* → parte il flusso LIMET (proposta → spec → plan → task → test → archive).

---

## 3. Prerequisiti MCP (opzionali)

I tre MCP sono **opzionali**. Se non li configuri, `claude` mostrerà errori di connessione per loro (come `graphify: Connection closed`) ma le skill restano pienamente funzionanti. Per disattivarli del tutto, vedi §6.

### 3.1 Dipendenze Python

```bash
pip install -e .
```

Installa tutte le dipendenze elencate in `pyproject.toml` (qdrant-client, psycopg2-binary, fastapi, ecc.). Se fallisce, installa le dipendenze una a una dallo stesso file.

### 3.2 `cerebro` — RAG su Qdrant

Richiede due servizi in esecuzione:

| Servizio | Default | Override env |
|---|---|---|
| Qdrant (vector DB) | `http://localhost:6333` | `QDRANT_URL` |
| Ollama (embedding) | `http://localhost:11434` | `OLLAMA_URL` |

Altri env opzionali: `EMBEDDING_MODEL` (default `nomic-embed-text`), `EMBEDDING_DIM` (default `768`).

Il modello di embedding deve essere caricato in Ollama (`ollama pull nomic-embed-text`). Un `.env` nella root del repo viene caricato automaticamente.

### 3.3 `db` — SQL read-only

Richiede PostgreSQL in esecuzione. **Non** legge env var: legge la sezione `db` da file di config nella root del plugin:

```yaml
# config/config.yaml         (committato, valori condivisi)
db:
  host: localhost
  port: 5432
  database: mydb
  user: myuser
  password: ""               # ← metti i secret in config.local.yaml, non qui

# config/config.local.yaml   (git-ignorato, secret personali)
db:
  password: "la-mia-password"
```

Campi: `host`, `port`, `database`, `user`, `password`, `row_limit` (default 100). Il server accetta **solo `SELECT`** (DDL/DML rifiutati).

### 3.4 `graphify` — knowledge graph del codice

Richiede il binario `graphify-mcp` sul `PATH` (fornito dal pacchetto `graphifyy`).

---

## 4. Hook su Windows

I 4 hook sono script `.sh` (`hooks/*.sh`). Su Windows servono **Git Bash** o **WSL** per essere eseguiti. Se non disponibili, gli hook falliscono in silenzio: le skill continuano a funzionare, ma perdi l'auto-attivazione e il change log automatico.

Da verificare sul primo uso: se il change log non si popola, controlla che Git Bash/WSL sia presente.

---

## 5. Aggiornamento (dopo nuove feature)

```bash
claude plugin update limet@limet-marketplace
```

Per un'installazione locale ("live", `Read from: <percorso repo>`), basta editare i file: il cambio è immediato, nessuna reinstall.

---

## 6. Disattivare gli MCP (se non ti servono)

Se non vuoi gli errori di connessione MCP, disabilita i server:

```bash
claude plugin disable limet@limet-marketplace   # disabilita tutto (anche skill)
```

Oppure, per togliere solo gli MCP, rimuovi la sezione `mcpServers` dal manifest del plugin prima di installare (per i membri che non usano cerebro/db/graphify).

---

## 7. Uninstall

```bash
claude plugin uninstall limet@limet-marketplace
claude plugin marketplace remove limet-marketplace
```

---

## 8. Troubleshooting

| Sintomo | Causa probabile | Fix |
|---|---|---|
| Skill non visibili dopo install | Claude Code non riavviato | Riavvia Claude Code |
| `graphify: Connection closed` | `graphify-mcp` non su PATH | Installa `graphifyy` (§3.4) o ignora |
| `cerebro` fallisce | Qdrant/Ollama spenti | Avvia i servizi (§3.2) |
| `db` fallisce | PostgreSQL spento o config mancante | Controlla `config/config.yaml` (§3.3) |
| Hook non partono (no change log) | Windows senza Git Bash/WSL | Installa Git Bash o WSL (§4) |
| `claude plugin install` non trova `limet` | Marketplace non registrato | Riesegui `claude plugin marketplace add ./` |
