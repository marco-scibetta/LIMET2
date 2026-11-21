# Verifica e2e manuale — LIMET 2.0 (ciclo completo)

## Riferimenti
- Piano/task collegato: TASK_LIST.md #20
- Ambiente di verifica: locale (Windows 10), progetto fittizio `<progetto-test>`

## Precondizioni
- Plugin `limet` installato (`claude plugin marketplace add ./` + `claude plugin install limet`)
- Python 3.11, pytest 8.3.5, Docker (Qdrant + Postgres), Ollama (nomic-embed-text)

## Stato pre-verifica
- `claude plugin validate .` → OK (1 warning CLAUDE.md by-design, non-strict)
- Qdrant (6333) UP, Ollama (11434) UP, Postgres (5432) UP via Docker

## Passi di verifica

### 1. new
`/limet-new "mini-todo"` → genera 7 doc in `limet/changes/<slug>/`.
- **Esito**: OK — CHANGE_PROPOSAL, SPEC (5 requisiti), PLAN, TASK_LIST (5 task), TEST_PLAN, E2E_VERIFICATION, DECISIONS.

### 2. task
Implementazione dei 5 task (`mini_todo/model.py`, `store.py`, `todo.py`).
- **Esito**: OK — codice scritto, registro modifiche compilato, nessun `done` senza verifica.

### 3. test
`python -m pytest tests -v`
- **Esito**: OK — **15 passed** (13 unit/e2e + 2 regressione).

### 4. bug
Bug reale trovato (JSON valido non-list → `TypeError` non gestito).
- **Esito**: OK — BUG_REPORT, fix (validazione list + utf-8-sig), 2 test regressione verdi.

### 5. archive
`/limet-archive` → change spostata in `limet/archive/<slug>/`.
- **Esito**: OK — ARCHIVE_ENTRY + 9 doc, `changes/` svuotata.

## Stato post-verifica
- `limet/archive/2026-11-20-mini-todo/` completo (ARCHIVE_ENTRY + 9 doc).
- `limet/changes/` vuoto.

## Casi limite verificati
- Titolo vuoto → ValueError (CLI exit 2).
- File JSON corrotto/BOM → errore chiaro (dopo fix).
- id inesistente su done/delete → KeyError (exit 2).

## Esito esecuzione
- Data/ora: 2026-11-20 19:09 · Eseguito da: agente (autorizzato) · Esito: **OK**
