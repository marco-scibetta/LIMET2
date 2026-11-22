# LIMET 2.0 — Onboarding Checklist

Passi per partire con LIMET su un progetto.

## 1. Installa il plugin
```bash
pip install -e .                    # dipendenze Python
claude plugin marketplace add ./
claude plugin install limet
claude plugin validate .            # non-strict
```

## 2. Prepara l'infrastruttura (se serve)
- Qdrant: `docker run -d -p 6333:6333 qdrant/qdrant`
- Ollama: `ollama pull nomic-embed-text`
- Postgres: `docker run -d --name limet-postgres -e POSTGRES_USER=... -e POSTGRES_PASSWORD=... -e POSTGRES_DB=... -p 5432:5432 postgres:18-alpine3.23`

## 3. Avvia la dashboard
```
/limet-dashboard
```
→ http://127.0.0.1:8787

Scegli la **lingua** col flag 🇮🇹/🇬🇧 in alto a destra (interfaccia + documenti prodotti).

## 4. Inizializza il progetto (Init)
- nome progetto (combobox se esistente)
- percorso docs
→ register + graphify + ingestion Qdrant in un colpo.
- Spunta **Workspace** se il progetto è multi-modulo (root + moduli in una collection).

## 5. Configura il progetto (Setup)
- seleziona progetto dalla combo
- Qdrant / Ollama / DB
- Salva → config.local.yaml
- Test connessione DB.

## 5bis. Collega progetti (se interagiscono)
- **Progetti** → "Collega progetti" → A e B → **Collega**.
- La ricerca Qdrant in A copre anche B (e viceversa).

## 6. Ciclo di lavoro
```
/limet-new "feature X"    → genera i documenti
/limet-task 1             → implementa (brief 2-3 righe)
/limet-test               → piano + esecuzione test
!bash scripts/run-tests.sh <comando>   → esegue test, esito in TEST_EXECUTION (log distrutto se OK)
/limet-bug "errore Y"     → se serve
/limet-archive            → archivia il lavoro verificato
```

## 7. Verifica finale
- `python -m pytest tests -v` → tutti verdi
- `limet-gate` → OK su ogni task `done`

## Regole da ricordare
- Mai build/test in autonomia.
- Mai commit/push senza autorizzazione esplicita.
- Ogni task `done` ha una strategia di verifica (unit + e2e + lint/type se configurati).
