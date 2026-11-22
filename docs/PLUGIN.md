# LIMET 2.0 — Plugin

LIMET 2.0 è un **plugin Claude Code** distribuibile: `skills/` + `agents/` + `hooks/` + `.mcp.json` + manifest.

## Struttura del plugin

```
limet/                          ← UNICO repo self-contained
├── .claude-plugin/
│   └── plugin.json            ← manifest (name=limet, version, description)
├── skills/
│   ├── limet-new/SKILL.md
│   ├── limet-task/SKILL.md
│   ├── limet-test/SKILL.md
│   ├── limet-archive/SKILL.md
│   └── limet-bug/SKILL.md
├── agents/
│   ├── limet-writer.md
│   └── limet-gate.md
├── hooks/
│   ├── hooks.json
│   ├── resume.sh
│   ├── intent.sh
│   ├── guardrail.sh
│   ├── changelog.sh
│   ├── precompact.sh
│   └── reminder.sh
├── .mcp.json                 ← cerebro + graphify (nativo) + db
├── mcp/                      ← cerebro e db DENTRO il repo
│   ├── cerebro/              (RAG: server.py + scripts register/ingest/query)
│   └── db/                   (DB: server.py, legge config.yaml/config.local.yaml)
├── config/                   ← config.yaml + config.local.yaml + loader.py
├── .gitignore                ← include config.local.yaml (mai nel repo)
├── CLAUDE.md                 ← policy always-on
└── docs/                     ← manual, onboarding

> Infra runtime (Qdrant + Ollama): **nativi di default** (binario Qdrant + installer Ollama), no Docker. `docker-compose.yml` solo come *opzione* per chi preferisce la riproducibilità.
```

## `plugin.json`

```json
{
  "name": "limet",
  "description": "Spec-driven engineering framework with traceability: proposal → spec → plan → task → test → archive.",
  "version": "2.0.0",
  "author": "LIMET",
  "homepage": "https://github.com/<org>/limet"
}
```

- `name` = namespace delle skill (`/limet-new`, ecc.).
- Le skill `user-invocable` diventano comandi `/limet-new`, `/limet-task`, …

## Distribuzione

1. **Marketplace proprio** (repo git): aggiungi `.claude-plugin/marketplace.json` con `source: "./"`. L'utente fa:
   `claude plugin marketplace add <repo>` → `claude plugin install limet@<marketplace>`.
2. **Directory Anthropic** (opzionale, più tardi): submission + scan automatico.

## Dev locale

- Sviluppo standalone in `.claude/` del progetto, poi migrazione a plugin quando stabile.
- `--plugin-dir ./limet` per test locale + `/reload-plugins` tra le modifiche.
- `claude plugin validate --strict ./limet` in CI.

## Nota path

Nel plugin, tutti i path interni usano `${CLAUDE_PLUGIN_ROOT}/...` (mai path assoluti).
