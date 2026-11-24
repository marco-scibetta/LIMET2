# SPEC — Analisi progetto / auto-onboarding

## Obiettivo

Dato un progetto non documentato, produrre a richiesta un set di documenti onboarding in
`/docs/` (root del progetto) tramite un subagent dedicato, attivato da una sezione della
dashboard e lanciato da una skill in Claude Code.

## Requisiti

### R1 — Subagent `limet:analyzer`
Subagent self-contained che, dato un progetto, ne analizza struttura e contenuto e genera i
documenti onboarding.

- Scenario dato/quando/allora:
  - **Dato** un progetto in `cwd` con codice sorgente e nessuna doc onboarding,
  - **quando** `limet:analyzer` viene eseguito,
  - **allora** genera in `docs/` i documenti R6, non vuoti, con riferimenti `file:line`.
- Lingua dei doc: lingua configurata in `config/config.yaml`+`local` (`it`/`en`), altrimenti lingua dell'utente.

### R2 — Skill `/limet-analyze`
Skill che avvia l'analisi in Claude Code.

- **Dato** un progetto con flag `analyze: true` nel config,
- **quando** l'utente esegue `/limet-analyze`,
- **allora** la skill spawna `limet:analyzer` sul progetto corrente e verifica che i doc R6 siano prodotti.
- Se il flag non è attivo, la skill chiede conferma prima di procedere (o procede comunque su conferma esplicita).

### R3 — Dashboard: sezione "Analizza"
- **Dato** un progetto registrato in CEREBRO,
- **quando** l'utente, in dashboard, seleziona il progetto e clicca "Analizza",
- **allora** il backend imposta `projects.<slug>.analyze: true` in `config/config.local.yaml` e conferma.

### R4 — Config: flag `analyze`
- Il loader espone `analyze_requested(slug)` che restituisce `True` se `projects.<slug>.analyze` è `true`.
- Il flag vive solo in `config.local.yaml` (per-progetto, non committato).

### R5 — Intent hook
- **Dato** un prompt utente contenente "analizza il progetto" / "onboarding" / "documenta il progetto",
- **quando** scatta UserPromptSubmit,
- **allora** viene iniettato il suggerimento `/limet-analyze` (fail-safe: exit 0 su errore).

### R6 — Documenti generati (in `docs/`)
1. `architecture.md` — struttura, componenti, flusso dati (Mermaid).
2. `module-map.md` — mappa moduli → `file:line`.
3. `dependencies.md` — dipendenze esterne e interne.
4. `conventions.md` — convenzioni di codice.
5. `decisions.md` — decisioni architetturali rilevate (solo se presenti).
6. `glossary.md` — termini di dominio.
7. `NON_TECHNICAL_SUMMARY.md` — sintesi onboarding non tecnica.

### R7 — Fail-safe
- Ogni componente (hook, skill, agent, endpoint) non deve mai bloccare Claude Code su errore:
  hook exit 0, skill/agent errori riportati ma non fatali.

## Vincoli
- Nessuna breaking change ai componenti LIMET 2 esistenti.
- `limet:analyzer` non dipende da plugin esterni (CE).
- I doc generati non vengono automaticamente indicizzati (re-index resta dell'utente).
