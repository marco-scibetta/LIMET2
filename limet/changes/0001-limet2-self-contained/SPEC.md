# Specifica — Capability: LIMET 2.0 (piattaforma self-contained)

> Descrive il *cosa* verificabile dell'intera piattaforma. I requisiti raggruppano le capability della
> proposta collegata; i dettagli per singola skill/agente vengono generati da `/limet:new` durante
> l'implementazione. I test (unit/e2e) si allineano a questi requisiti/scenari.

## Metadati

- **Proposta collegata**: `CHANGE_PROPOSAL.md`
- **Stato**: `APPROVATA`
- **Versione**: 1

## Descrizione della capability

LIMET 2.0 è un plugin Claude Code che sostituisce il flusso LIMET 1.0 manuale con: 5 skill per il
ciclo di vita, 4 hook deterministici per le guardrail, 2 subagent per scrittura/validazione, 3
server MCP (cerebro/graphify/db) e una dashboard React per le ops. Tutto in un unico repo
self-contained; esterni solo Qdrant e Ollama (infra).

## Requisiti

### Requisito 1: ciclo di vita conversazionale

L'utente esprime l'intento in linguaggio naturale; il sistema avvia il flusso spec-driven senza che
l'utente digiti comandi.

**Scenari**:
- **Dato** nessun ciclo attivo, **quando** l'utente scrive "voglio aggiungere la feature X", **allora**
  l'hook `intent` segnala feature e Claude avvia `/limet:new X`.
- **Dato** nessun ciclo attivo, **quando** l'utente scrive "c'è un bug Y" / "non funziona", **allora**
  viene avviato `/limet:bug Y`.
- **Dato** prompt senza intento feature/bug, **quando** l'hook `intent` lo riceve, **allora** nessun
  output (exit 0, zero contesto).

### Requisito 2: le 5 skill generano gli artefatti corretti

`/limet:new` produce proposal+spec+plan+task_list+test_plan+e2e (e decisions se emergono decisioni
hard-to-reverse); `/limet:task` esegue un task e aggiorna il change log; `/limet:test` genera/esegue
il piano test; `/limet:archive` archivia in `limet/archive/<data-slug>/`; `/limet:bug` genera un
BUG_REPORT strutturato.

**Scenari**:
- **Dato** `/limet:new "X"`, **quando** completato, **allora** in `limet/` esistono i documenti attesi,
  ognuno compilato dai template e non vuoto.
- **Dato** scelta ambigua durante `/limet:new`, **quando** manca un'informazione, **allora** viene
  registrata una domanda contestuale con data (mai assunta in silenzio).

### Requisito 3: hook = enforcement deterministico (con fail-safe)

Le regole non-negoziabili sono applicate dagli hook, non scritte come testo. Un hook che crasha non
blocca mai Claude.

**Scenari**:
- **Dato** comando Bash con `mvnw`/`./gradlew`/`npm test`/`pytest`/`cargo test`, **quando**
  `guardrail` (PreToolUse) lo intercetta, **allora** blocca (exit 2) con messaggio "build/test non in
  autonomia".
- **Dato** comando con `git commit`/`push`/`rebase`/`migrate`/`deploy`, **quando** senza
  autorizzazione esplicita, **allora** blocca.
- **Dato** Edit/Write su file nello scope del task attivo, **quando** `changelog` (PostToolUse) scatta,
  **allora** appende/coalesce una riga al change log di `TASK_LIST.md`.
- **Dato** un hook che lancia eccezione, **quando** eseguito, **allora** exit 0 + log di diagnosi
  (nessun blocco di Claude).

### Requisito 4: gate di validazione

`limet-gate` rifiuta un task senza verifica e segnala drift doc↔codice.

**Scenari**:
- **Dato** task marcato `done` senza unit test né giustificazione "n/a", **quando** `limet-gate` lo
  controlla, **allora** esito `FAIL` e il task non è chiuso.
- **Dato** SPEC/PLAN che divergono dal codice reale, **quando** `limet-gate` confronta, **allora**
  produce un drift report con le divergenze.

### Requisito 5: MCP cerebro (RAG)

Tool `cerebro_search/count/list/ingest/register` operano sulla collection Qdrant del progetto.

**Scenari**:
- **Dato** progetto registrato, **quando** `cerebro_search(project, query, limit)`, **allora** restituisce
  i frammenti rilevanti (limit rispettato).
- **Dato** ingestion con N chunk, **quando** `cerebro_ingest(project)`, **allora** embedding in batch
  (non 1 POST HTTP per chunk).

### Requisito 6: MCP graphify (KG)

Tool `graphify_query/path/explain/update` rispondono sul knowledge graph.

**Scenari**:
- **Dato** grafo generato, **quando** `graphify_explain(simbolo)`, **allora** restituisce la spiegazione
  del simbolo.
- **Dato** `graphifyy` dichiarato come dipendenza, **quando** si avvia `mcp/graphify`, **allora** riusa
  l'MCP nativo del pacchetto (no wrapper custom).

### Requisito 7: MCP db (read-only, segreti fuori dal contesto)

Il server MCP legge i segreti DB dal file di configurazione locale (`config.local.yaml`, sezione `db`);
l'LLM non vede mai host/user/password.

**Scenari**:
- **Dato** query `INSERT/UPDATE/DELETE/DDL`, **quando** `db_query`, **allora** reject (solo SELECT).
- **Dato** `config.local.yaml` con `db.password`, **quando** l'LLM chiama i tool db, **allora** l'output non
  contiene mai host/user/password/config.
- **Dato** SELECT che supera il row limit (default 100), **quando** eseguita, **allora** risultato
  troncato al limite.

### Requisito 8: dashboard ops

La dashboard espone le pagine init/progetti/re-index/status/config-db/artefatti e non duplica il
lavoro di Claude (nessuna generazione spec/plan/task).

**Scenari**:
- **Dato** stato Qdrant/Ollama/MCP/db, **quando** pagina Status, **allora** mostra stato + chunk count.
- **Dato** `config.local.yaml` con password, **quando** pagina Config DB, **allora** la password non è mai
  mostrata in chiaro.
- **Dato** artefatti LIMET generati, **quando** pagina Artefatti, **allora** visualizzazione read-only.

### Requisito 9: installazione self-contained

Un solo `claude plugin install limet` (+ infra Qdrant/Ollama) rende tutto operativo, senza repo
esterni CEREBRO/Graphify.

**Scenari**:
- **Dato** plugin installato, **quando** si esegue `claude plugin validate --strict ./limet`, **allora**
  validazione ok.
- **Dato** tool MCP dichiarati in `.mcp.json`, **quando** il plugin è attivo, **allora** i server
  cerebro/graphify/db sono raggiungibili (o errore diagnostico se l'infra è giù).

### Requisito 10: configurazione da file (zero hardcoded, zero env var)

Ogni variabile (path, host/porta, modello embedding, limiti, lingua, segreti) vive in file di
configurazione che LIMET legge da una posizione nota. Nessun valore hardcoded nel codice, nessuna
variabile d'ambiente richiesta all'utente.

**Scenari**:
- **Dato** `config/config.yaml` presente, **quando** un server MCP si avvia, **allora** legge i valori
  da lì (default committati).
- **Dato** `config/config.local.yaml` presente, **quando** si carica la config, **allora** i suoi valori
  sovrascrivono i default (merge default ← local).
- **Dato** `config.local.yaml` assente, **quando** si avvia LIMET, **allora** usa solo i default, senza
  errore, segnalando cosa è configurabile.
- **Dato** un valore non presente nel file, **quando** il codice lo usa, **allora** nessun path
  hardcoded: o c'è un default nel file o viene segnalato esplicitamente.

## Vincoli e casi limite

- Hook: fail-safe obbligatorio (un guardrail rotto non deve bloccare il lavoro).
- Segreti: `config.local.yaml` gitignored + permessi filesystem (chmod 600 / ACL Windows); commitare solo
  `config.local.example.yaml`.
- Row limit e timeout su db (niente query enormi nel contesto).
- `/goal` usato in un solo punto (fine `/limet:task`), non sovrapposto a `limet-gate`.
- Vincolo "non overingegnerizzare": 5 skill, 4 hook, 2 subagent, 3 MCP. Stop.
- Path interni del plugin con `${CLAUDE_PLUGIN_ROOT}/...`, mai assoluti.

## Fuori specifica (esplicitamente non coperto)

- Generazione spec/plan/task dalla dashboard (→ Claude, via skill).
- ADR completo: `decisions.md` è ADR-lite, non il lifecycle ADR pieno.
- Docker obbligatorio: resta opzionale (nativo di default).
- Marketplace pubblico/pubblicazione: solo dev locale nella v1 (`<org>` placeholder).

> **Nota lingua (Q4)**: la v1 è **bilingue IT+EN** (skill/agente/doc). Deroga esplicita a
> `docs/OPTIMIZATIONS.md` §2 ("EN rimandato"), decisa dall'utente il 2026-11-20.

## Tracciabilità verso i test

| Requisito | Unit test | Test e2e |
| --- | --- | --- |
| R1 intent | unit su `intent.sh` (frasi positive/negative) | prompt naturale → flusso avviato |
| R2 skill | unit sui template generati (non vuoti, schema) | `/limet:new X` → doc presenti |
| R3 hook | unit su guardrail/changelog (blocca/non-blocca, coalesce) | edit reale → riga in change log |
| R4 gate | unit su `limet-gate` (FAIL su task senza test) | task senza test → rifiutato |
| R5 cerebro | pytest su tool (limit, batch) | `cerebro_ingest` su Qdrant reale |
| R6 graphify | pytest su tool | `graphify_explain` su grafo reale |
| R7 db | pytest su reject DDL/row-limit/no-secret | connessione read-only reale |
| R8 dashboard | component test (no password in chiaro) | navigazione pagine su browser |
| R9 install | validazione manifest JSON | `claude plugin install` + tool MCP vivi |
| R10 config | unit sul loader (merge default↔local, default assenti) | avvio MCP con/senza `config.local.yaml` |
