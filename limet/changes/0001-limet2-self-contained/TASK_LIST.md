# Elenco task — LIMET 2.0 (piattaforma self-contained)

> Deriva da `CHANGE_PROPOSAL.md` + `DESIGN.md`. Fasi ordinate; ogni task con stato e dipendenze.
> Per un task complesso, scheda dedicata in `TASK.md` linkata da "Dettaglio".

## Legenda stato

- `pending` — non ancora iniziato
- `in_progress` — in corso
- `blocked` — bloccato (motivare in Note)
- `done` — completato **e verificato** (annotare `YYYY-MM-DD HH:MM` in Note)

## Tabella task

| # | Titolo | Scopo (non tecnico) | Stato | Dipende da | Dettaglio | Note |
| - | ------ | ------------------- | ----- | ---------- | --------- | ---- |
| 1 | Skeleton repo + plugin manifest | Impalcatura repo: `.claude-plugin/plugin.json`, `.gitignore`, `.mcp.json` stub, `CLAUDE.md` policy | pending | — | | |
| 2 | Dev locale + marketplace placeholder | `marketplace.json` con `<org>` segnaposto + install dev locale (`--plugin-dir`) | pending | #1 | | |
| 3 | Skill `/limet:new` | Ciclo completo: proposal+spec+plan+task+test+e2e+decisions | pending | #1 | [TASK.md](./TASK.md) | |
| 4 | Skill `/limet:task` | Esegue un task + change log | pending | #3 | | |
| 5 | Skill `/limet:test` | Genera/esegue il piano test | pending | #4 | | |
| 6 | Skill `/limet:archive` | Archivia il lavoro concluso | pending | #5 | | |
| 7 | Skill `/limet:bug` | Report bug strutturato | pending | #1 | | |
| 8 | Hook `intent.sh` | Rileva intento feature/bug da UserPromptSubmit | pending | #1 | | |
| 9 | Hook `guardrail.sh` | Blocca build/test/commit non autorizzati (PreToolUse) | pending | #1 | | |
| 10 | Hook `changelog.sh` | Appende change log (PostToolUse Edit/Write) | pending | #1 | | |
| 11 | Hook `reminder.sh` | Ricorda test/archivio a fine ciclo (Stop) | pending | #1 | | |
| 12 | `hooks.json` + fail-safe | Wiring dei 4 hook con try/catch | pending | #8–11 | | |
| 13 | Agent `limet-writer` | Scrive i documenti con contesto isolato | pending | #3 | | |
| 14 | Agent `limet-gate` | Valida §1.5 + fresh-eyes + drift report | pending | #5 | | |
| 15 | MCP `cerebro` + batch embedding | Copia script CEREBRO + wrapper MCP + rewrite `ingest_docs`/`doc_to_markdown` | pending | #1 | | |
| 16 | MCP `graphify` | Dipendenza `graphifyy==0.9.32` + riuso MCP nativo | pending | #1 | | niente porting; solo pin + launch MCP nativo |
| 17 | MCP `db` | Server read-only + `.env_db` | pending | #1 | | |
| 18 | Dashboard backend + scaffold | REST condiviso + React/Vite/TS + design system | pending | #1 | | |
| 19 | Dashboard pagine ops | init/progetti/re-index/status/config-db/artefatti | pending | #18 | | |
| 20 | Integrazione E2E + docs | Ciclo completo validato + manuale + onboarding | pending | #12,#14,#17 | | |
| 21 | File di configurazione + loader | `config.yaml` + `config.local.yaml` + loader; letto da hook/MCP/dashboard | pending | #1 | | trasversale: da fare subito dopo #1 |

---

## Strategia di test — obbligatoria per ogni task

> Comandi di test eseguiti dall'**utente** (mai dall'agente — vedi CLAUDE.md "MAI build/test").

| # task | Unit test previsti/esistenti | Test e2e previsti (rif. `E2E_VERIFICATION.md`) | Se omesso, motivazione esplicita |
| ------ | ----------------------------- | --------------------------------------------------------- | --------------------------------- |
| 1 | sì: validazione schema `plugin.json` + presenza file attesi | sì: `claude plugin validate --strict ./limet` | |
| 2 | sì: validazione `marketplace.json` | sì: `claude plugin install` da path locale / `--plugin-dir` | |
| 3 | sì: template generati non vuoti + schema per artefatto | sì: `/limet:new "X"` → doc attesi presenti | |
| 4 | sì: riga change log aggiunta per file toccato | sì: `/limet:task 1` su task fittizio | |
| 5 | sì: TEST_PLAN/TEST_EXECUTION generati con comandi esatti | sì: `/limet:test` → piano eseguibile | |
| 6 | sì: path `limet/archive/<data-slug>/` corretto | sì: `/limet:archive` → file spostati | |
| 7 | sì: BUG_REPORT con sezioni obbligatorie | sì: `/limet:bug "Y"` → report strutturato | |
| 8 | sì: frasi positive/negative → exit/output attesi | sì: prompt naturale → flusso avviato (R1) | |
| 9 | sì: blocco `mvnw`/`pytest`/`git commit` + non-blocco altro | sì: comando bloccato → exit 2 con messaggio | |
| 10 | sì: coalesce edit multipli, ignora fuori-scope | sì: edit reale → riga in change log | |
| 11 | sì: reminder solo se task senza test/archivio | sì: Stop con task incompleto → reminder | |
| 12 | sì: hook che crasha → exit 0 (fail-safe) | sì: hook rotto non blocca Claude | |
| 13 | sì: output documenti conforme ai template | sì: `limet-writer` produce spec+plan validi | |
| 14 | sì: `FAIL` su task senza test; drift rilevato | sì: task senza test → rifiutato (R4) | |
| 15 | sì: pytest su tool + batch embedding (N chunk = 1 chiamata) | sì: `cerebro_ingest` su Qdrant reale | |
| 16 | sì: pytest su tool graphify | sì: `graphify_explain` su grafo reale | |
| 17 | sì: pytest su reject DDL/row-limit/no-secret | sì: connessione read-only reale (R7) | |
| 18 | sì: component test (no password in chiaro) | sì: dashboard si avvia + REST `/api/info` | |
| 19 | sì: component test per pagina | sì: navigazione pagine su browser | |
| 20 | sì: n/a (integrazione) | sì: ciclo completo su progetto fittizio | unit n/a perché integrazione, non nuova logica |
| 21 | sì: pytest su loader (merge default↔local, default assenti, file assente) | sì: avvio MCP con/senza `config.local.yaml` | |

## Registro modifiche — una riga per file toccato

| Task | File | Tipo | Cosa è cambiato | Perché | Verifica collegata |
| ---- | ---- | ---- | --------------- | ------ | ------------------ |
| —    | (vuoto, popolato in fase di implementazione) | | | | |

## Esito implementazione (da compilare a lavoro concluso)

- **Data**:
- **Sintesi esito**:
- **Scostamenti rispetto al piano**:
- **Esito test** (riferimento a `TEST_EXECUTION.md` se presente):
- **Data/ora di completamento di ciascun task** (`YYYY-MM-DD HH:MM`): colonna Note.
