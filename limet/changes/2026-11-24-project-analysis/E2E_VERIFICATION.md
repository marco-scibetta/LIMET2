# E2E_VERIFICATION — Analisi progetto / auto-onboarding

Checklist di verifica manuale.

## 1. Subagent `limet:analyzer`

- [ ] In un progetto fittizio (`/tmp/proj-test` o simile) con codice (es. un `pyproject.toml` + un modulo):
  - [ ] esegui l'agent `limet:analyzer` in quel cwd;
  - [ ] `docs/architecture.md`, `module-map.md`, `dependencies.md`, `conventions.md`, `glossary.md`, `NON_TECHNICAL_SUMMARY.md` esistono e non sono vuoti;
  - [ ] `decisions.md` esiste (o assente solo se nessuna decisione rilevata).

## 2. Skill `/limet-analyze`

- [ ] In un progetto con `analyze: true` nel config:
  - [ ] `/limet-analyze` spawna `limet:analyzer` e produce i doc;
  - [ ] al termine conferma i doc generati.

## 3. Dashboard

- [ ] Avvia la dashboard (`/limet-dashboard` → :8787);
- [ ] apri pagina "Analizza";
- [ ] seleziona un progetto registrato e clicca "Analizza";
- [ ] verifica in `config/config.local.yaml` → `projects.<slug>.analyze: true`.

## 4. Hook intent

- [ ] In Claude Code, prompt "analizza il progetto" → compare suggerimento `/limet-analyze`.
- [ ] Prompt neutro ("ciao") → nessun suggerimento.

## 5. Regressione

- [ ] `python -m pytest tests -v` → verde;
- [ ] `claude plugin validate .` → passa (solo warning CLAUDE.md by-design).
