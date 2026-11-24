# LIMET 2.0 — Onboarding Checklist

Steps to start with LIMET on a project.

## 1. Install the plugin
```bash
pip install -e .                    # Python dependencies
claude plugin marketplace add ./
claude plugin install limet
claude plugin validate .            # non-strict
```

## 2. Prepare the infrastructure (if needed)
- Qdrant: `docker run -d -p 6333:6333 qdrant/qdrant`
- Ollama: `ollama pull nomic-embed-text`
- Postgres: `docker run -d --name limet-postgres -e POSTGRES_USER=... -e POSTGRES_PASSWORD=... -e POSTGRES_DB=... -p 5432:5432 postgres:18-alpine3.23`

## 3. Launch the dashboard
```
/limet-dashboard
```
→ http://127.0.0.1:8787

Choose the **language** with the 🇮🇹/🇬🇧 flag at the top right (interface + produced documents).

## 4. Initialize the project (Init)
- project name (combo if existing)
- docs path
→ register + graphify + Qdrant ingestion in one go.
- Check **Workspace** if the project is multi-module (root + modules in one collection).

## 5. Configure the project (Setup)
- select the project from the combo
- Qdrant / Ollama / DB
- Save → config.local.yaml
- Test DB connection.

## 5bis. Link projects (if they interact)
- **Projects** → "Link projects" → A and B → **Link**.
- Qdrant search in A covers B too (and vice versa).

## 5ter. Analyze an undocumented project (optional)
- Dashboard → **Analyze** → select project → "Request analysis".
- In Claude Code on that project: `/limet-analyze` → generates onboarding docs in `docs/`.
- Re-index the docs when you want.

## 6. Work cycle
```
/limet-new "feature X"    → generates the documents
/limet-task 1             → implement (2-3 line brief)
/limet-test               → plan + test execution
!bash scripts/run-tests.sh <command>   → runs tests, outcome in TEST_EXECUTION (log destroyed if OK)
/limet-bug "error Y"     → if needed
/limet-archive            → archives the verified work
```

## 7. Final verification
- `python -m pytest tests -v` → all green
- `limet-gate` → OK on every `done` task

## Rules to remember
- Never build/test autonomously.
- Never commit/push without explicit authorization.
- Every `done` task has a verification strategy (unit + e2e + lint/type if configured).
