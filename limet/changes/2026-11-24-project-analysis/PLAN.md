# PLAN — Analisi progetto / auto-onboarding

## Approccio

Flusso: **dashboard marca** il progetto (flag `analyze`) → **skill `/limet-analyze`** in Claude Code
legge il flag e **spawna `limet:analyzer`** → l'agent analizza il codice e **scrive i doc in `docs/`**.

La dashboard non esegue direttamente i subagent (impossibile: i subagent vivono in Claude Code);
scrive solo lo stato. L'esecuzione avviene in Claude Code sul progetto target.

## Componenti

1. `agents/analyzer.md` — subagent `limet:analyzer` (Read, Grep, Glob, Write).
2. `skills/limet-analyze/SKILL.md` — skill `/limet-analyze` (allowed-tools Read/Grep/Glob + Agent).
3. `config/loader.py` — helper `analyze_requested(slug)`.
4. `hooks/intent.sh` — rileva intento analisi/onboarding.
5. `dashboard/backend/server.py` — endpoint `POST /api/analyze` (setta flag) + `GET /api/analyze?project=` (legge flag).
6. `dashboard/frontend/src/pages/AnalyzePage.tsx` + nav + icon + i18n — pagina "Analizza".

## Alternative considerate

- **CLI headless (`claude -p`)**: scartata — pesante, fragile, dipende dalla CLI nel backend.
- **Riuso CE (`ce-repo-research-analyst`)**: scartata — dipendenza esterna.
- **Riuso solo built-in (Explore/general-purpose)**: scartata — vuole un agent dedicato self-contained.

## Rischi

- **Collisione `docs/`**: il progetto target potrebbe già avere `docs/`. Mitigazione: l'agent
  crea/aggiorna i 7 file ma non cancella nulla; segnala se `docs/` esiste già.
- **Progetti eterogenei** (linguaggi/stili diversi): l'agent rileva lo stack da file manifest
  (`package.json`, `pyproject.toml`, `go.mod`, `pom.xml`, `Cargo.toml`, …) e adatta i doc.
- **Progetti grandi**: l'agent campiona (entry point + moduli principali), non legge tutto.

## Ordine di implementazione

1. `agents/analyzer.md`
2. `skills/limet-analyze/SKILL.md`
3. `config/loader.py` (flag)
4. `hooks/intent.sh` (intento)
5. dashboard backend (`/api/analyze`)
6. dashboard frontend (pagina + nav + i18n + icon)
7. doc LIMET 2 (manuali, MASTER_INDEX, ONBOARDING, archive, docs/, guide HTML)
8. test (unit + e2e) ed esecuzione
