# LIMET 2.0

Spec-driven engineering for Claude Code. Lifecycle: `/limet:new` → `/limet:task` → `/limet:test` → `/limet:archive`; `/limet:bug` for bugs.

## Binding rules

- Spec first: proposal/plan before non-trivial code changes.
- Ambiguity → explicit question with date; never assume.
- No task marked `done` without a verification strategy (unit + e2e), or explicit justification.
- Human approval recorded before implementation.
- Never run build/test autonomously — give the command, the user runs it.
- No commit/push/migrate/deploy without explicit authorization.

## Context tools (MCP)

`cerebro` (docs RAG) · `graphify` (code KG) · `db` (read-only SQL).
