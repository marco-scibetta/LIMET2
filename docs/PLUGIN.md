# LIMET 2.0 — Plugin

LIMET 2.0 is a distributable **Claude Code plugin**: `skills/` + `agents/` + `hooks/` + `.mcp.json` + manifest.

## Plugin structure

```
limet/                          ← SINGLE self-contained repo
├── .claude-plugin/
│   └── plugin.json            ← manifest (name=limet, version, description)
├── skills/
│   ├── limet-new/SKILL.md
│   ├── limet-task/SKILL.md
│   ├── limet-test/SKILL.md
│   ├── limet-archive/SKILL.md
│   ├── limet-bug/SKILL.md
│   └── limet-analyze/SKILL.md
├── agents/
│   ├── limet-writer.md
│   ├── limet-gate.md
│   └── limet-analyzer.md
├── hooks/
│   ├── hooks.json
│   ├── resume.sh
│   ├── intent.sh
│   ├── guardrail.sh
│   ├── changelog.sh
│   ├── precompact.sh
│   └── reminder.sh
├── .mcp.json                 ← cerebro + graphify (native) + db
├── mcp/                      ← cerebro and db INSIDE the repo
│   ├── cerebro/              (RAG: server.py + register/ingest/query scripts)
│   └── db/                   (DB: server.py, reads config.yaml/config.local.yaml)
├── config/                   ← config.yaml + config.local.yaml + loader.py
├── .gitignore                ← includes config.local.yaml (never in the repo)
├── CLAUDE.md                 ← always-on policy
└── docs/                     ← manual, onboarding

> Runtime infra (Qdrant + Ollama): **native by default** (Qdrant binary + Ollama installer), no Docker. `docker-compose.yml` only as an *option* for those who prefer reproducibility.
```

## `plugin.json`

```json
{
  "name": "limet",
  "description": "Spec-driven engineering plugin for Claude Code: proposal → spec → plan → task → test → archive.",
  "version": "2.0.0",
  "author": "LIMET",
  "homepage": "https://github.com/<org>/limet"
}
```

- `name` = skills namespace (`/limet-new`, etc.).
- `user-invocable` skills become the `/limet-new`, `/limet-task`, … commands.

## Distribution

1. **Own marketplace** (git repo): add `.claude-plugin/marketplace.json` with `source: "./"`. The user runs:
   `claude plugin marketplace add <repo>` → `claude plugin install limet@<marketplace>`.
2. **Anthropic directory** (optional, later): submission + automatic scan.

## Local dev

- Standalone development in the project's `.claude/`, then migration to a plugin once stable.
- `--plugin-dir ./limet` for local testing + `/reload-plugins` between changes.
- `claude plugin validate --strict ./limet` in CI.

## Path note

In the plugin, all internal paths use `${CLAUDE_PLUGIN_ROOT}/...` (never absolute paths).
