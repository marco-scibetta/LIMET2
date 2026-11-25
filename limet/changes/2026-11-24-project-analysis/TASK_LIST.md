# Elenco task — Analisi progetto / auto-onboarding

> Deriva da `CHANGE_PROPOSAL.md` + `SPEC.md` + `PLAN.md`.

## Legenda stato

- `pending` / `in_progress` / `blocked` / `done` (con `YYYY-MM-DD HH:MM` se verificato)

## Tabella task

| # | Titolo | Scopo | Stato | Dipende | Note |
| - | ------ | ----- | ----- | ------- | ---- |
| 1 | Agent `limet:analyzer` | Analizza progetto e genera i 7 doc in `docs/` | done | — | frontmatter valido, doc template inline |
| 2 | Skill `/limet-analyze` | Legge flag, spawna analyzer, verifica doc | done | #1 | allowed-tools + regole binding |
| 3 | Config flag `analyze` | `analyze_requested(slug)` nel loader | done | — | default `false`, solo config.local |
| 4 | Intent hook | Rileva "analizza/onboarding" → `/limet-analyze` | done | — | fail-safe exit 0 |
| 5 | Backend `/api/analyze` | POST setta flag, GET legge flag | done | #3 | in `dashboard/backend/server.py` |
| 6 | Pagina "Analizza" | Seleziona progetto + "Analizza" → flag | done | #5 | nav + icon + i18n it/en |
| 7 | Doc LIMET 2 | Manuali, MASTER_INDEX, ONBOARDING, archive, docs/, guide HTML | done | #2,#4,#6 | Amendment 5 in archive |
| 8 | Test + esecuzione | Unit + e2e, pytest verde | done | #1–7 | test_hooks/config_loader/dashboard estesi |

## Strategia di test (obbligatoria per ogni task)

| # | Unit | E2E |
| - | ---- | --- |
| 1 | frontmatter valido + template non vuoti | `limet:analyzer` su progetto fittizio → 7 doc non vuoti |
| 2 | skill frontmatter + regole presenti | `/limet-analyze` → doc generati |
| 3 | `analyze_requested` true/false/assente | loader con `analyze: true` |
| 4 | prompt analisi → hint `/limet-analyze`; prompt neutro → exit 0 | intent hook su prompt reale |
| 5 | POST setta flag, GET legge flag | `/api/analyze` 200 + config aggiornato |
| 6 | component test pagina | navigazione + click "Analizza" |
| 7 | n/a (solo doc) | grep riferimenti coerenti nei manuali |
| 8 | pytest su tutto | `python -m pytest tests -v` verde |

## Registro modifiche

| Task | File | Tipo | Cosa | Perché | Verifica |
| ---- | ---- | ---- | ---- | ------ | -------- |
| 1 | `agents/analyzer.md` | creato | subagent analisi → doc in `docs/` | R1 | #1 |
| 2 | `skills/limet-analyze/SKILL.md` | creato | skill che spawna analyzer | R2 | #2 |
| 3 | `config/loader.py` | modificato | + `analyze_requested(slug)` | R4 | #3 |
| 4 | `hooks/intent.sh` | modificato | + intento analisi/onboarding | R5 | #4 |
| 5 | `dashboard/backend/server.py` | modificato | + `POST/GET /api/analyze` | R3 | #5 |
| 6 | `dashboard/frontend/src/pages/AnalyzePage.tsx`, `App.tsx`, `i18n.ts`, `Icon.tsx` | creati/modificati | pagina Analizza + nav + i18n | R3 | #6 |
| 7 | `limet/FRAMEWORK_MANUAL.md`, `MASTER_INDEX.md`, `ONBOARDING_CHECKLIST.md`, `limet/archive/.../TASK_LIST.md`, `docs/*`, `guides/*/limet-*.html` | modificati | doc aggiornate alla feature | coerenza doc | #7 |
| 8 | `tests/test_hooks.py`, `test_config_loader.py`, `test_dashboard.py` | modificati | test flag/intento/endpoint | R4/R5/R3 | #8 |
| —    | `limet\changes\2026-11-24-project-analysis\TASK_LIST.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `limet\changes\2026-11-24-project-analysis\TEST_PLAN.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `limet\changes\2026-11-24-project-analysis\E2E_VERIFICATION.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `agents\limet-analyzer.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `skills\limet-analyze\SKILL.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `config\loader.py` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `hooks\intent.sh` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `dashboard\backend\server.py` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `dashboard\frontend\src\pages\AnalyzePage.tsx` | creato | (auto) | (da completare) | (da verificare) |
| —    | `dashboard\frontend\src\App.tsx` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `dashboard\frontend\src\components\Icon.tsx` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `dashboard\frontend\src\i18n.ts` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `tests\test_config_loader.py` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `tests\test_hooks.py` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `tests\test_dashboard.py` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `docs\SKILLS.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `docs\SUBAGENTS.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `docs\ARCHITECTURE.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `limet\FRAMEWORK_MANUAL.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `limet\MASTER_INDEX.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `limet\ONBOARDING_CHECKLIST.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `limet\archive\2026-11-21-limet2\TASK_LIST.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `guides\it\workflow.html` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `guides\en\workflow.html` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `guides\it\limet-project-init.html` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `guides\en\limet-project-init.html` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `docs\README.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `docs\SETUP.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `docs\OPTIMIZATIONS.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `docs\DASHBOARD.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `docs\HOOKS.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `scripts\run-tests.sh` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `agents\limet-gate.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `.gitignore` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `.claude-plugin\plugin.json` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `.claude-plugin\marketplace.json` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `pyproject.toml` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `docs\PLUGIN.md` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `skills\limet-task\SKILL.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `skills\limet-test\SKILL.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `skills\limet-bug\SKILL.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `skills\limet-archive\SKILL.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `agents\limet-writer.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `commands\limet-dashboard.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `commands\limet-dashboard-stop.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `INSTALL.md` | creato | (auto) | (da completare) | (da verificare) |
| —    | `hooks\guardrail.sh` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `hooks\resume.sh` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `hooks\precompact.sh` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `hooks\reminder.sh` | modificato | (auto) | (da completare) | (da verificare) |
| —    | `hooks\changelog.sh` | modified | (auto) | (da completare) | (da verificare) |
| —    | `docs\MCP.md` | created | (auto) | (to complete) | (to verify) |
| —    | `docs\MIGRATION.md` | created | (auto) | (to complete) | (to verify) |
| —    | `dashboard\run.py` | modified | (auto) | (to complete) | (to verify) |
| —    | `CLAUDE.md` | modified | (auto) | (to complete) | (to verify) |
| —    | `guides\en\limet-setup.html` | modified | (auto) | (to complete) | (to verify) |
| —    | `guides\it\limet-setup.html` | modified | (auto) | (to complete) | (to verify) |
