# LIMET 2.0 — index

**L**ightweight **I**terative **M**ethod for **E**ngineering with **T**raceability — version 2.0, **native Claude Code**.

LIMET 2.0 is the rewrite of LIMET 1.0 to leverage Claude Code's native features: **skills, hooks, subagents, plugins, MCP, slash commands**. Same philosophy (lightweight, spec-driven, traceability, non-negotiable testing), but optimized: **Claude generates the documents, the human doesn't fill them**.

## Document index

| Doc | What it contains |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | overall architecture + 1.0→2.0 mapping |
| [SKILLS.md](SKILLS.md) | the 6 skills (lifecycle + analysis) with a SKILL.md example |
| [HOOKS.md](HOOKS.md) | the 6 hooks (resume, intent, guardrail, changelog, precompact, reminder) with hooks.json |
| [SUBAGENTS.md](SUBAGENTS.md) | the 3 subagents (writer, gate, analyzer) |
| [MCP.md](MCP.md) | cerebro + graphify + db as MCP |
| [PLUGIN.md](PLUGIN.md) | packaging/distribution of the `limet` plugin |
| [OPTIMIZATIONS.md](OPTIMIZATIONS.md) | the optimizations and their motivations |
| [MIGRATION.md](MIGRATION.md) | how to migrate from LIMET 1.0 to 2.0 |

## The lifecycle (in one line)

`/limet-new` (proposal→spec→plan) → `/limet-task` (implement, automatic change log) → `/limet-test` (verify) → `/limet-archive`. With `/limet-bug` for bugs and `/limet-analyze` for analyzing an undocumented project.

## Status

- Implementation **completed**: plugin, skills, hooks, subagents, MCP, dashboard.
- Language: English.

## How LIMET 2.0 was born (dogfooding)

LIMET 2.0 was developed **using LIMET itself**: the spec-driven method applied to its own construction. These documents were the first LIMET artifacts, and the project was built with its own method (`/limet-new` → task → test → archive).
