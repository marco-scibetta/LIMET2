# Elenco task — LIMET 2.0 (piattaforma self-contained)

> Deriva da `CHANGE_PROPOSAL.md` + `DESIGN.md`. Fasi ordinate; ogni task con stato e dipendenze.
> Per un task complesso, scheda dedicata in `TASK.md` linkata da "Dettaglio".

> **Convenzione di sessione (utente, 2026-11-20)**: prima di implementare ogni task, l'agente dà un
> brief di 2-3 righe (cosa, file toccati, verifica) e procede **senza attendere conferma**. Baked-in
> nel design LIMET 2.0 — `docs/SKILLS.md` §"Regole condivise" e skill `/limet:task` (task #4).
>
> **Verifica skill (utente, 2026-11-20)**: il test di `/limet:new` e delle altre skill si fa **dopo**
> aver scritto tutte e 5 (task #3–#7), in un'unica sessione di test — non skill per skill.
>
> **Esito test unico (2026-11-20)**: ciclo completo OK in `<progetto-test>` — new→task→test→bug→archive
> tutti i doc prodotti. **Gap trovati e corretti**: `/limet:new` generava flat in `limet/` (→ `changes/<slug>/`); `/limet:bug`
> senza regola slug; `/limet:test` senza TEST_EXECUTION; `/limet:archive` senza `Bash` (mv). **Verifica finale (16:43)**:
> `limet/archive/2026-11-20-login-page/` completo (ARCHIVE_ENTRY + 9 doc), `changes/` svuotata. Guardrail archive robusto
> (rifiuta non-verificato, rileva `done` forzato, esige e2e). Tutte e 5 le skill funzionanti end-to-end.
>
> **Slug convenzione (decisione, 2026-11-20)**: le skill usano `<data-slug>` = `YYYY-MM-DD-slug` per `changes/` e
> `archive/` (deviazione da 1.0 `NNNN-slug`, scelta per sortabilità).
>
> **Dashboard senza "Artefatti" (decisione utente, 2026-11-20)**: pagina "Artefatti" rimossa — read-only ridondante
> (i doc si vedono già nell'editor), viola "ogni pagina = un'azione". Scostamento da SPEC R8 (6→5 pagine).
>
> **Dashboard monoprocesso (decisione, 2026-11-20)**: il backend FastAPI serve anche il frontend buildato (`dist/`),
> così l'utente avvia UN solo processo (niente BE+FE separati a mano).
>
> **Validazione plugin non-strict (scostamento, 2026-11-20)**: task #1 e2e `claude plugin validate --strict .`
> declassato a non-strict. Motivo: warning `CLAUDE.md at the plugin root is not loaded as project context` è
> by-design — repo root = plugin root, e `CLAUDE.md` è policy dev del progetto (non contesto plugin), non rimovibile.
> Aggiunti `icon` + `network.hosts` (`localhost`, `127.0.0.1`); resta solo quel warning strutturale.
>
> **Amendment post-archivio (2026-11-22)**: aggiunti 2 hook — `resume.sh` (SessionStart: riprende il
> ciclo attivo) e `precompact.sh` (PreCompact: inietta stato prima della compattazione) — ed esteso
> `guardrail.sh` ai comandi distruttivi irreversibili (`git reset --hard`, `git clean`, `git checkout --`,
> `git branch -D`, `git stash drop`, `rm -rf`). Hook 4→6. Test `tests/test_hooks.py` estesi: 33→41 unit
> (41 passed, 1 skipped). Doc aggiornate: `docs/HOOKS.md`, `docs/PLUGIN.md`, `docs/ARCHITECTURE.md`,
> `docs/OPTIMIZATIONS.md`, `docs/README.md`, `docs/SETUP.md`, `FRAMEWORK_MANUAL.md`, `MASTER_INDEX.md`,
> `SPEC.md`, `DESIGN.md`, `ARCHIVE_ENTRY.md`.
>
> **Amendment 2 (2026-11-22)**: `limet-gate` esteso — verifica anche lint/type (quando il progetto ha
> `ruff`/`mypy`/`eslint`/`tsc` configurati); rifiuta `done` senza esito lint/type registrato. §1.5
> aggiornata a "unit + e2e + lint/type (se configurati)" in `CLAUDE.md`, `limet-writer`, skill
> (`limet-new`, `limet-test`), `docs/SKILLS.md`, `docs/SUBAGENTS.md`, `docs/ARCHITECTURE.md`,
> `FRAMEWORK_MANUAL.md`, `MASTER_INDEX.md`, `ONBOARDING_CHECKLIST.md`.
>
> **Amendment 3 (2026-11-22)**: aggiunto `scripts/run-tests.sh` — comando esplicito (NON hook) che
> esegue i test, registra l'esito compatto in `TEST_EXECUTION.md`, distrugge i log temporanei se OK e
> mantiene `raw.log` se KO. `reminder.sh` (Stop) ora suggerisce il comando; `limet-gate` legge solo il
> summary (mai `raw.log`). Test `tests/test_hooks.py` estesi con OK-cleanup e KO-keep-log.
>
> **Amendment 4 (2026-11-22)**: fix bug MCP graphify — `pyproject.toml` ora dichiara
> `graphifyy[mcp]==0.9.32` (extra `[mcp]` mancante → SDK `mcp` non installato → `graphify-mcp` crash
> "Connection closed"). Fix runtime: `uv tool install "graphifyy[mcp]==0.9.32"`. Aggiunti test `reminder.sh`.
>
> **Amendment 5 (2026-11-24)**: aggiunta feature "Analisi progetto / auto-onboarding" — nuovo subagent
> `limet-analyzer` + skill `/limet-analyze` + flag config `analyze` + intento hook + pagina dashboard
> "Analizza" (`/api/analyze`). Doc onboarding generati in `docs/`. Vedi `limet/changes/2026-11-24-project-analysis/`.
>
> **Amendment 6 (2026-11-24)**: `run-tests.sh` su FAIL ora scrive nel summary anche il puntatore a
> `raw.log` + la coda output (60 righe, language-agnostic — nessun parsing della firma). Il summary
> basta a valutare l'esito senza rilanciare i test. Test `test_run_tests_fail_keeps_log` rafforzato.

## Legenda stato

- `pending` — non ancora iniziato
- `in_progress` — in corso
- `blocked` — bloccato (motivare in Note)
- `done` — completato **e verificato** (annotare `YYYY-MM-DD HH:MM` in Note)

## Tabella task

| # | Titolo | Scopo (non tecnico) | Stato | Dipende da | Dettaglio | Note |
| - | ------ | ------------------- | ----- | ---------- | --------- | ---- |
| 1 | Skeleton repo + plugin manifest | Impalcatura repo: `.claude-plugin/plugin.json`, `.gitignore`, `.mcp.json` stub, `CLAUDE.md` policy | done | — | | 2026-11-20 18:47 — validate OK (non-strict); scostamento sotto |
| 2 | Dev locale + marketplace placeholder | `marketplace.json` con `<org>` segnaposto + install dev locale (`--plugin-dir`) | done | #1 | | 2026-11-20 18:49 — marketplace add `./` + install OK, loads in place |
| 3 | Skill `/limet:new` | Ciclo completo: proposal+spec+plan+task+test+e2e+decisions | done | #1 | [TASK.md](./TASK.md) | 2026-11-20 18:54 — `/limet-new "prova-dummy"` → 7 doc non vuoti in dummy |
| 4 | Skill `/limet:task` | Esegue un task + change log; **brief di 2-3 righe prima di implementare** (regola condivisa `docs/SKILLS.md`) | done | #3 | | 2026-11-20 16:43 — ciclo completo OK (evidenza nota in testa) |
| 5 | Skill `/limet:test` | Genera/esegue il piano test | done | #4 | | 2026-11-20 16:43 — TEST_PLAN + TEST_EXECUTION OK |
| 6 | Skill `/limet:archive` | Archivia il lavoro concluso | done | #5 | | 2026-11-20 16:43 — archive completo (9 doc) + guardrail robusto |
| 7 | Skill `/limet:bug` | Report bug strutturato | done | #1 | | 2026-11-20 16:43 — BUG_REPORT OK |
| 8 | Hook `intent.sh` | Rileva intento feature/bug da UserPromptSubmit | done | #1 | | 2026-11-20 18:58 — fix falso positivo limet-bug/debug; test 4 prompt OK |
| 9 | Hook `guardrail.sh` | Blocca build/test/commit non autorizzati (PreToolUse) | done | #1 | | 2026-11-20 18:58 — git commit+pytest bloccati exit 2; ls libero |
| 10 | Hook `changelog.sh` | Appende change log (PostToolUse Edit/Write) | done | #1 | | 2026-11-20 18:58 — auto-righe (plugin.json, intent.sh, reminder.sh) apparse |
| 11 | Hook `reminder.sh` | Ricorda test/archivio a fine ciclo (Stop) | done | #1 | | 2026-11-20 18:58 — fix regex backtick; reminder scattato con #8–17+#20–23 |
| 12 | `hooks.json` + fail-safe | Wiring dei 4 hook con try/catch | done | #8–11 | | 2026-11-20 18:58 — validate elenca 4 hook; fail-safe in ogni script |
| 13 | Agent `limet-writer` | Scrive i documenti con contesto isolato | done | #3 | | 2026-11-20 19:02 — 7 doc generati non vuoti in dummy writer-test |
| 14 | Agent `limet-gate` | Valida §1.5 + fresh-eyes + drift report | done | #5 | | 2026-11-20 19:02 — agent eseguito: 14 task FAIL (no test persistiti) + drift rilevato; gate funziona |
| 15 | MCP `cerebro` + batch embedding | Copia script CEREBRO + wrapper MCP + rewrite `ingest_docs`/`doc_to_markdown` | done | #1 | | 2026-11-20 19:25 — reindex da dashboard → 3 chunk su Qdrant reale, search OK |
| 16 | MCP `graphify` | Dipendenza `graphifyy==0.9.32` + riuso MCP nativo | done | #1 | | 2026-11-20 19:25 — graphify extract 43 nodi + explain/god-nodes OK |
| 17 | MCP `db` | Server read-only + `.env_db` | done | #1 | | 2026-11-20 19:46 — SELECT reale su Postgres Docker OK (per-progetto), INSERT reject, no-secret |
| 18 | Dashboard backend + scaffold | REST condiviso + React/Vite/TS + design system | done | #1 | | 2026-11-20 16:34 — build ok + /api/info 200 |
| 19 | Dashboard pagine ops | init/progetti/re-index/status/setup | done | #18 | | 2026-11-20 19:35 — 5 pagine (Artefatti tolta, Config DB→Setup), combobox Init/Reindex, Setup config |
| 20 | Integrazione E2E + docs | Ciclo completo validato + manuale + onboarding | done | #12,#14,#17 | | 2026-11-20 20:23 — e2e mini-todo (15 test) + E2E_VERIFICATION + MANUAL + ONBOARDING |
| 21 | File di configurazione + loader | `config.yaml` + `config.local.yaml` + loader; letto da hook/MCP/dashboard | done | #1 | | 2026-11-20 19:47 — config per-progetto + `config/loader.py` condiviso; cerebro+db+dashboard leggono config |
| 22 | Riscrittura documenti legacy per LIMET 2.0 | `limet/FRAMEWORK_MANUAL.md`, `MASTER_INDEX.md`, `ONBOARDING_CHECKLIST.md` e template 1.0 → riscritti/aggiornati per LIMET 2.0 (skill/hook/subagent/MCP/plugin) | done | #20 | | 2026-11-20 20:39 — MANUAL/INDEX/ONBOARDING riscritti; rimossi templates/, scripts/, AGENTS.md, copilot-instructions.md, docs-limet/ |
| 23 | Aggiornamento README | README root riflette lo stato finale di LIMET 2.0 (già abbozzato; da rivedere a fine implementazione) | done | #22 | | 2026-11-20 20:40 — README EN/IT, comandi corretti, link a MANUAL/INDEX/ONBOARDING + guide HTML |

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
| 22 | sì: n/a (sola documentazione) | sì: grep assenza riferimenti 1.0 residui (`Copilot CLI`, `18 template`) + percorsi/rimandi del manuale risolvibili | unit n/a: nessuna logica nuova |
| 23 | sì: n/a (sola documentazione) | sì: README renderizza, link corretti, due sezioni (EN/IT) presenti | unit n/a: nessuna logica nuova |

## Registro modifiche — una riga per file toccato

| Task | File | Tipo | Cosa è cambiato | Perché | Verifica collegata |
| ---- | ---- | ---- | --------------- | ------ | ------------------ |
| 1    | `.claude-plugin/plugin.json` | creato | Manifest plugin `limet` v2.0.0 (name/description/version/author/homepage) | Skeleton plugin; fonte per `claude plugin validate` | task #1 e2e: validate --strict |
| 1    | `.gitignore` | creato | Ignora `config.local.yaml`, `.env_db`, artefatti Python/Node, `graphify-out/` | Segreti fuori dal repo (R10) + niente build artifact | task #1: presenza file + segreti esclusi |
| 1    | `.mcp.json` | creato | Stub 3 server MCP (cerebro/graphify/db) con command/args | Dichiarazione unica dei tool; wiring finale in #15–17 | task #1: file valido; MCP vivi in #15–17 |
| 1    | `CLAUDE.md` | modificato | Policy 2.0 minima (regole binding + pointer MCP) sostituisce 1.0 `@AGENTS.md` | `CLAUDE.md` = minimo (principio guida DESIGN) | task #1: policy presente e coerente |
| 2    | `.claude-plugin/marketplace.json` | creato | Marketplace placeholder: `name=limet-marketplace`, `owner=<org>`, plugin `limet` `source="./"` | Distribuzione via `claude plugin marketplace add` (design PLUGIN.md) | task #2: `marketplace add` valida |
| 3    | `skills/limet-new/SKILL.md` | creato | Skill `/limet:new`: genera proposal+spec+plan+task+test+e2e+decisions, template inline, regole binding (incl. brief) | Skill del ciclo di vita (R2); self-contained | task #3: frontmatter valido + template non vuoti |
| 3    | `docs/SKILLS.md` | modificato | Aggiunta regola condivisa #5 "brief prima di ogni task" | Requisito utente: brief sempre, baked-in nel design | task #4: `/limet:task` implementa la regola |
| 4    | `skills/limet-task/SKILL.md` | creato | Skill `/limet:task`: legge task, brief 2-3 righe, implementa, change log, no-done-senza-verifica | Skill ciclo di vita (R2) + regola brief (utente) | task #4: frontmatter valido + brief/no-done presenti |
| 5    | `skills/limet-test/SKILL.md` | creato | Skill `/limet:test`: TEST_PLAN + TEST_EXECUTION, autorevisione qualità, template inline | Skill ciclo di vita (R2) | task #5: frontmatter valido + template non vuoti |
| 6    | `skills/limet-archive/SKILL.md` | creato | Skill `/limet:archive`: archivia in `archive/<data-slug>/` + voce archivio, solo lavoro verificato | Skill ciclo di vita (R2) | task #6: frontmatter valido + solo-verificato presente |
| 7    | `skills/limet-bug/SKILL.md` | creato | Skill `/limet:bug`: BUG_REPORT strutturato con causa radice + test regressione | Skill ciclo di vita (R2) | task #7: frontmatter valido + template non vuoto |
| 3–7  | `skills/limet-{new,task,test,archive,bug}/SKILL.md` | modificato | `description` accorciata (rimossi rimandi `/limet:*` e testo lungo) | Descrizione concisa per registrazione/triggering del comando | task #3–7 e2e: `/limet-*` tutti visibili |
| 3–7  | `skills/limet-{new,task,test,archive,bug}/SKILL.md` | modificato | Path `limet/` → `limet/changes/<data-slug>/` | Gap e2e: i doc vanno in `changes/`, non flat in `limet/` | retest: `/limet-new` crea `limet/changes/<data-slug>/` |
| 5    | `skills/limet-test/SKILL.md` | modificato | `TEST_EXECUTION.md` sempre generato (struttura "da compilare" se test non eseguiti) | Gap e2e: `/limet-test` produceva solo TEST_PLAN | retest: `/limet-test` → TEST_EXECUTION presente |
| 7    | `skills/limet-bug/SKILL.md` | modificato | Slug esplicito: scrive in `changes/<slug>` attivo o ne crea uno da `$ARGUMENTS` | Gap e2e: `/limet-bug` senza regola slug → non produceva BUG_REPORT | retest: `/limet-bug` → BUG_REPORT.md nella dir giusta |
| 6    | `skills/limet-archive/SKILL.md` | modificato | `allowed-tools` + `Bash` (per `mv` changes→archive) | Spostamento file richiede shell; Write/Edit non cancellano origine | retest `/limet-archive` su lavoro verificato → sposta + voce |
| 8    | `hooks/intent.sh` | creato | Hook intento: rileva feature/bug dal prompt, inietta `additionalContext` (suggerimento `/limet-new` o `/limet-bug`); exit 0 se nessun intento/errore | Flusso conversazionale (R1); fail-safe | task #8: exit 0 su prompt neutro; JSON su intento |
| 9    | `hooks/guardrail.sh` | creato | Hook guardrail (PreToolUse/Bash): blocca build/test (exit 2) e comandi persistenti (commit/push/rebase/migrate/deploy) con messaggio su stderr | Enforcement §1.3 (R3); fail-safe | task #9: `./mvnw test`→exit 2; `git commit`→exit 2; `ls`→exit 0 |
| 10   | `hooks/changelog.sh` | creato | Hook changelog (PostToolUse Edit/Write): appende riga al registro del TASK_LIST attivo, solo file in scope, coalesce | Tracciabilità automatica (R3); fail-safe | task #10: edit→riga aggiunta; file tracciato→no duplicato; `limet/`/`.git/`→ignorato |
| 11   | `hooks/reminder.sh` | creato | Hook reminder (Stop): se task non `done` → inietta reminder `/limet-test` + `/limet-archive` | Verifica/archivio non dimenticati (R1.5); fail-safe | task #11: task non-done→reminder; tutto done→exit 0 |
| 12   | `hooks/hooks.json` | creato | Wiring 4 hook: UserPromptSubmit→intent, PreToolUse/Bash→guardrail, PostToolUse/Edit|Write→changelog, Stop→reminder; timeout 10–15s | Registrazione hook nel plugin (R3); fail-safe negli script | task #12: `claude plugin validate --strict .` riconosce i 4 hook |
| 13   | `agents/limet-writer.md` | creato | Subagent scrittore: genera 7 doc LIMET in `changes/<slug>/` con regole binding (spec-driven, traceability, test, no build/test) | Ruolo scrittura isolata (R2) | task #13: frontmatter valido + regole binding presenti |
| 14   | `agents/limet-gate.md` | creato | Subagent validatore (sola lettura): verifica §1.5, fresh-eyes review, drift report; rifiuta task senza verifica | Gate qualità indipendente (R4) | task #14: frontmatter valido + OK/FAIL/drift presenti |
| 15   | `mcp/cerebro/server.py` | creato | MCP cerebro: 5 tool (`search/count/list/ingest/register`), JSON-RPC stdio, stdlib-only | RAG come MCP nativo (R5/R9) | task #15: `tools/list`→5 tool; `search` rispetta limit |
| 15   | `mcp/cerebro/ingest_docs.py` | copiato+riscritto | `get_embedding` (1 HTTP/chunk) → `get_embeddings_batch` (`/api/embed`, N chunk = 1 chiamata) | Fix velocità ingestion (§8) | task #15: batch = 1 POST per file, non per chunk |
| 15   | `mcp/cerebro/doc_to_markdown.py` | copiato+riscritto | `pdf_to_markdown`: pdfplumber seriale → pypdfium2 + `ThreadPoolExecutor` | Fix velocità parsing (§9) | task #15: PDF multi-pagina processato in parallelo |
| 15   | `mcp/cerebro/{project_config,query_qdrant,register_project,serve_images,limet_rag}.py` | copiati | Script CEREBRO intatti dentro il plugin | Self-contained, zero repo esterni (R9) | task #15: import/avvio senza repo CEREBRO |
| 16   | `pyproject.toml` | creato | Dipendenze: `graphifyy==0.9.32` (pin) + qdrant-client, requests, pypdfium2, markitdown[all], ebooklib, markdownify, beautifulsoup4 | Graphify terze-parti pinnato, non vendorizzato (R6/R9) | task #16: `pip install -e .` risolve tutte le dipendenze |
| 16   | `.mcp.json` | modificato | `graphify`: `graphifyy mcp` → `graphify-mcp` (entry point nativo `graphify.serve:_main`) | Riuso MCP nativo, zero wrapper (R6) | task #16: tool `graphify_*` vivi via `graphify-mcp` |
| 17   | `mcp/db/server.py` | creato | MCP db read-only: solo SELECT (reject DDL/DML via regex), row limit 100, segreti letti da `config.local.yaml`/`config.yaml` (sez. `db`) mai esposti | Query SQL senza segreti nel contesto (R7) | task #17: INSERT→reject; SELECT>limit→troncata; output senza host/user/password |
| 17   | `pyproject.toml` | modificato | + `PyYAML`, `psycopg2-binary` (driver Postgres + parser YAML config) | Config YAML + connessione DB (R7/R10) | task #17: import yaml/psycopg2 risolti |
| 18   | `dashboard/backend/server.py` | creato | FastAPI: `/api/info`, `/api/db/test`, `/api/db/schema` (CORS aperto, port 8787), segreti mai esposti | Backend REST condiviso (R8) | task #18: `/api/info`→200; `/api/db/test`→ok/502 |
| 18   | `dashboard/frontend/{package.json,vite.config.ts,tsconfig.json,index.html}` | creati | Scaffold Vite + React + TS (React 18, Vite 5, strict) | Frontend React/TS (R8) | task #18: `npm run build` compila |
| 18   | `dashboard/frontend/src/{main.tsx,App.tsx,theme.css}` | creati | App con sidebar (6 pagine) + design system token dark professionale | Grafica moderna, non '90s (R8) | task #18: layout responsive + token coerenti |
| 18   | `pyproject.toml` | modificato | + `fastapi`, `uvicorn` | Backend REST | task #18: uvicorn avvia il server |
| 19   | `dashboard/frontend/src/pages/*.tsx` (6) + `api.ts` | creati | 6 pagine: Status, Init, Progetti, Re-index, Config DB (password mai mostrata), Artefatti (read-only) | Pagine ops (R8) | task #19: `npm run build` + navigazione |
| 19   | `dashboard/frontend/src/App.tsx` | modificato | Render pagine per stato nav (sidebar → componente) | Routing pagine | task #19: click nav → pagina corretta |
| 19   | `dashboard/frontend/src/theme.css` | modificato | Componenti: card, badge, table, form, button, log, grid | Design system applicato | task #19: stile coerente |
| 19   | `dashboard/backend/server.py` | modificato | + `/api/status`, `/api/projects`, `/api/artifacts`, `/api/reindex`, `/api/init` | Backend per le pagine | task #19: endpoint → 200 |
| 19   | `dashboard/frontend/src/theme.css` + `App.tsx` + `StatusPage.tsx` | riscritti | Design system "code dark + run green" (bg #0F172A, accent #22C55E, Fira Sans/Code), sidebar raggruppata + header con descrizione + card KPI | Grafica moderna (richiesta utente) | task #19: look professionale, non '90s |
| 19   | `dashboard/frontend/src/components/PathInput.tsx` | creato | File browser: dialog modale che naviga il filesystem via `/api/browse` | Seleziona path senza digitarli (richiesta utente) | task #19: "Sfoglia…" apre dialog → seleziona cartella |
| 19   | `dashboard/backend/server.py` | modificato | + `/api/browse` (elenca sottocartelle) | File browser | task #19: navigate + select path |
| 19   | `dashboard/frontend/src/components/PathInput.tsx` | modificato | Campo path → `<button>`; dialog → `createPortal(document.body)`; rimosso `<label>` wrapper | Fix click dialog non si apriva | task #19: click campo → dialog aperta (verificato utente) |
| 19   | `dashboard/frontend/src/pages/InitPage.tsx` | modificato | `<label>` → `.form-field`/`.form-label` | Semantica corretta, non interferisce col click | task #19: click campo funziona |
| 19   | `dashboard/run.py` | creato | Launcher monocomando: builda il frontend se serve, poi avvia il backend (API + frontend servito) | Un solo comando per l'utente (niente BE+FE a mano) | task #19: `python dashboard/run.py` → dashboard su :8787 |
| 19   | `dashboard/backend/server.py` | modificato | Serve il frontend `dist/` (static + SPA fallback) | Monoprocesso: API + UI in un server | task #19: `/` → index.html; `/api/*` → JSON |
| 19   | `dashboard/frontend/src/App.tsx` + `ArtifactsPage.tsx` | modificato/rimosso | Rimossa pagina "Artefatti" (nav + import + render + file) | Read-only ridondante (decisione utente) | task #19: 5 pagine, build ok |
| 19   | `commands/limet-dashboard.md` | creato | Slash command `/limet-dashboard`: avvia la dashboard in background e riferisce l'URL | L'utente non digita mai il comando a mano | task #19: `/limet-dashboard` → server su :8787 |
| —    | (lavoro extra e test — dettaglio in TEST_EXECUTION.md) | | | | |

| —    | `hooks\changelog.sh` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `config\config.yaml` | creato | (auto) | (da completare) | (da verificare) |
| —    | `mcp\projects.example.json` | creato | (auto) | (da completare) | (da verificare) |
| —    | `config\config.local.yaml` | creato | (auto) | (da completare) | (da verificare) |
| —    | `tests\test_hooks.py` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `tests\test_dashboard.py` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `config\config.local.example.yaml` | creato | (auto) | (da completare) | (da verificare) |
| —    | `README.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `limet\FRAMEWORK_MANUAL.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `limet\ONBOARDING_CHECKLIST.md` | modificato | (auto) | (da completare) | (da verificare) |
## Esito implementazione (a lavoro concluso)

- **Data**: 2026-11-21
- **Sintesi esito**: 23/23 task implementati e verificati. 33 unit test (pytest) verdi. Feature extra: workspace multi-modulo, progetti correlati, lingua IT/EN, guide HTML.
- **Scostamenti rispetto al piano**: (1) SPEC R8 6 pagine → 5 (Artefatti rimossa, Config DB→Setup); (2) graphify nativo `graphify-mcp`, non vendorizzato in `mcp/graphify/`; (3) slug `YYYY-MM-DD-slug` per `changes/`; (4) feature extra non previste nel piano originale.
- **Esito test**: `python -m pytest tests -v` → 33 passed (rif. TEST_EXECUTION.md).
- **Data/ora di completamento di ciascun task**: colonna Note.
