# Feature: Assegnatario task (multi-utente)

> Piano dettagliato per implementare la divisione dei task tra più sviluppatori in LIMET 2.0.
> **Stato**: PIANIFICATA (non implementata). Da attivare quando servirà un progetto a 6 persone.

## 1. Obiettivo

Permettere a un team (es. 6 persone) di dividersi i task di un change LIMET:
- Il **master** crea/inizializza il progetto, genera il `TASK_LIST` e assegna ogni task a una persona.
- Il **dev** clona il progetto, vede **i suoi** task, lavora su quelli (`/limet-task N`), committa.

**Principio**: minimo intervento, nessun Agile/XLS/board. Solo "chi fa cosa" = una colonna `Assegnatario` nel TASK_LIST.

## 2. Requisiti (scenari)

- **R1**: `/limet-new` genera un TASK_LIST con una colonna `Assegnatario` (vuota di default).
- **R2**: il master compila la colonna `Assegnatario` (nome utente) per ogni task, poi committa.
- **R3**: il dev, clonato il repo, individua i propri task leggendo la colonna `Assegnatario`.
- **R4** (opzionale): `/limet-task --mine <nome>` filtra/elenca i task assegnati a `<nome>`.
- **R5**: il campo `Assegnatario` non rompe il parsing esistente (hook `reminder.sh`, `changelog.sh`).

## 3. Design dettagliato

### 3.1 Assegnatario nella colonna esistente `Note` (nessun cambio di template)

**Nessuna colonna nuova — il TASK_LIST resta com'è.** Si usa la colonna libera **`Note`** per l'assegnatario.

Convenzione: il master scrive in `Note` il nome della persona (es. `→ mario`, oppure `mario + luca`).

Esempio riga (colonna `Note` in fondo):
```
| 3 | Collector Binance | Scaricare OHLCV | pending | — | | → mario |
```

Regole:
- `Note` vuota = non assegnato.
- Formato libero (`→ mario`, `mario`, `mario + luca`), nessuna validazione.
- Il **codice del task è il `#`** (numero reale in TASK_LIST): il branch usa `feat/<persona>-<#>` (es. `feat/mario-3`).

### 3.2 Filtro `--mine` in `/limet-task` (opzionale, R4)

File: `skills/limet-task/SKILL.md`.

Aggiungere al flusso della skill:
- `$ARGUMENTS` può contenere `--mine <nome>`.
- Se presente, prima di implementare: elenca i task della tabella la cui colonna `Note` contiene `<nome>` e stato non `done` (es. "I tuoi task: #1, #4"). Poi l'utente sceglie `N`.
- Se `--mine` senza nome: usa il nome dall'utente (chiedere, o da `$USER`/git config).

Nota: è un **filtro di lettura** (mostra i task), non cambia il ciclo `/limet-task N` che resta identico.

### 3.3 Impatto su hook esistenti

- `hooks/reminder.sh`: **nessuna modifica** (nessun cambio di template; lo stato resta la 4ª colonna).
- `hooks/changelog.sh`: **nessuna modifica** (appende al registro, non alla tabella task).
- `skills/limet-new/SKILL.md` e `agents/limet-writer.md`: **nessuna modifica** (il template resta identico).

### 3.4 Dove vive il template (per non dimenticare file)

Il template TASK_LIST è **inline** in `skills/limet-new/SKILL.md`. NON ci sono file template separati (rimossi in 2.0). Quindi la modifica è **una riga** in `limet-new/SKILL.md`.

`limet-writer` (agent) genera i doc seguendo gli stessi template; va verificato che usi lo stesso header tabella (o aggiornato di conseguenza).

## 4. File da toccare (lista esaustiva)

| # | File | Cosa | Perché |
| - | ---- | ---- | ------ |
| 1 | `skills/limet-task/SKILL.md` | aggiungere filtro `--mine <nome>` (parsa la colonna `Note`) | R4: il dev vede i suoi task |
| 2 | `docs/SKILLS.md` | documentare la convenzione `Note` + il filtro | doc |
| 3 | `limet/FRAMEWORK_MANUAL.md` | sezione "progetti multi-utente" (assignee via Note + branch) | doc |
| 4 | `limet/ONBOARDING_CHECKLIST.md` | passo "master assegna i task" | doc |
| 5 | `guides/it/multiuser.html` + `guides/en/multiuser.html` | guida SPA multi-utente (IT + EN) | doc dashboard |
| 6 | `dashboard/backend/server.py` | route `/docs/multiuser` (serve la guida via `_guide_lang`) | doc dashboard |
| 7 | `dashboard/frontend/src/App.tsx` + `i18n.ts` | link sidebar "Multi-utente" + chiave `docsMultiuser` | doc dashboard |

**NON toccare**: `hooks/reminder.sh`, `hooks/changelog.sh` (nessun impatto se la colonna è dopo `Stato`).

## 5. Test

### 5.1 Unit
- `reminder.sh` su un TASK_LIST con `Note` compilata → rileva ancora i task `pending`/`in_progress` (nessun impatto: il template non cambia).
- Filtro `--mine`: su un TASK_LIST di prova, `--mine mario` → elenca i task con `→ mario` in `Note`.

### 5.2 e2e
1. Master: `/limet-new "feature X"` → TASK_LIST con `Assegnatario`.
2. Master: compila `Assegnatario` (mario, luca), commit.
3. Dev (clone): `/limet-task --mine luca` → vede i task di luca.
4. Dev: `/limet-task N` sul suo task → implementa → commit.
5. Merge → TASK_LIST con i task `done` dei rispettivi assegnatari.

## 6. Rischi e edge case

1. **Concorrenza su TASK_LIST** (due dev editano lo stesso file) → merge conflict git. **Non risolto da questa feature** (resta disciplina git: branch per persona + merge). Fuori scope.
   - **Convenzione branch**: `feat/<persona>-<#>` (es. `feat/mario-3`, dove `3` = il `#` del task in TASK_LIST). Ogni dev lavora sul branch del suo task, poi merge.
2. **Colonna spostata** → se qualcuno mette `Assegnatario` PRIMA di `Stato`, `reminder.sh` si rompe. Mitigazione: metterla DOPO `Stato` (come da §3.1) + test di regressione §5.1.
3. **Assegnatario multi-valore** (`mario + luca`) → convenzione testuale, nessuna logica di parsing sul valore (solo visualizzazione/filtro per nome).
4. **`--mine` senza nome** → fallback: `$USER`/`git config user.name`; se assente, elenca tutti (senza filtrare).

## 7. Ordine di implementazione

1. Modificare `skills/limet-new/SKILL.md` (colonna `Assegnatario`).
2. (Opzionale) Modificare `skills/limet-task/SKILL.md` (filtro `--mine`).
3. Allineare `agents/limet-writer.md` se duplica il template.
4. Aggiornare doc (`docs/SKILLS.md`, `FRAMEWORK_MANUAL.md`, `ONBOARDING_CHECKLIST.md`).
5. Test unit (template + reminder.sh) + e2e (master→dev).

## 8. Fuori scope (esplicitamente)

- Agile/wave/sprint/story — duplicherebbero il TASK_LIST.
- XLS o board kanban — se servirà, tool esterno (GitHub Projects/Linear), non dentro LIMET.
- Lock dinamico / assegnazione automatica — per 6 persone basta l'assegnazione manuale del master.
- Coordinamento merge su TASK_LIST — compito di git (branch + merge), non di LIMET.

## 9. Documentazione SPA (guida multi-utente)

Nuova guida HTML in `guides/it/multiuser.html` + `guides/en/multiuser.html`, servita dalla dashboard
(come Setup / Project Init / Workflow, tramite `_guide_lang` + route `/docs/multiuser`), che spiega
chiaro e dettagliato come usare LIMET 2.0 multi-utente:

1. **Ruoli** — master (crea/inizializza/assegna) vs dev (prende i suoi task).
2. **Init + assegnazione** — master fa Init, `/limet-new`, compila la colonna `Assegnatario`, commit.
3. **Flusso dev** — clone → `pip install -e .` + plugin → Init locale → `--mine <nome>` → `/limet-task N` → commit.
4. **Branch per persona + merge** — branch nominato `feat/<persona>-<#>` (es. `feat/mario-3`, dove `3` = il `#` del task): sempre identificabile chi fa cosa su quale task, merge puliti.
5. **Condiviso vs locale** — git (codice/docs/changes/archive) vs Qdrant/graphify/config per-macchina.

Struttura: riusa il CSS delle altre guide (masthead, step numerati, note). Contenuto: stesso livello di
dettaglio di `project-init` (card + step + note). Link in sidebar "Documentazione" con chiave `docsMultiuser`.
