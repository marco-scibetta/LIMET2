# LIMET 2.0 — indice

**L**ightweight **I**terative **M**ethod for **E**ngineering with **T**raceability — versione 2.0, **nativa Claude Code**.

LIMET 2.0 è la riscrittura di LIMET 1.0 per sfruttare le feature native di Claude Code: **skill, hook, subagent, plugin, MCP, slash command**. Stessa filosofia (leggero, spec-driven, traceability, test non-negoziabile), ma ottimizzata: **Claude genera i documenti, non l'umano li riempie**.

## Differenza chiave 1.0 → 2.0

| | LIMET 1.0 | LIMET 2.0 |
|---|---|---|
| Template | 18 .md da riempire a mano | **6 skill** che Claude esegue |
| Regole (§1.3, §1.5) | testo in CLAUDE.md | **hook** (enforcement) |
| Attivazione | script PowerShell/bash | **plugin** install |
| CEREBRO/Graphify | skill-guida + script Python/CLI | **MCP** (tool nativi) |
| Target | tool-agnostic (Copilot/Claude) | **Claude-only** |

## Indice dei documenti

| Doc | Cosa contiene |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | architettura complessiva + mappatura 1.0→2.0 |
| [SKILLS.md](SKILLS.md) | le 6 skill (ciclo di vita + analisi) con esempio SKILL.md |
| [HOOKS.md](HOOKS.md) | i 6 hook (resume, intent, guardrail, changelog, precompact, reminder) con hooks.json |
| [SUBAGENTS.md](SUBAGENTS.md) | i 3 subagent (writer, gate, analyzer) |
| [MCP.md](MCP.md) | cerebro + graphify + db come MCP |
| [PLUGIN.md](PLUGIN.md) | packaging/distribuzione del plugin `limet` |
| [OPTIMIZATIONS.md](OPTIMIZATIONS.md) | le ottimizzazioni e le motivazioni |
| [MIGRATION.md](MIGRATION.md) | come migrare da LIMET 1.0 a 2.0 |

## Il ciclo di vita (in una riga)

`/limet-new` (proposta→spec→plan) → `/limet-task` (implementa, change log automatico) → `/limet-test` (verifica) → `/limet-archive`. Con `/limet-bug` per i bug e `/limet-analyze` per l'analisi di un progetto non documentato.

## Stato

- Implementazione **completata**: plugin, skill, hook, subagent, MCP, dashboard.
- Linguaggio: italiano (README root bilingue IT/EN).

## Come nasce LIMET 2.0 (dogfooding)

LIMET 2.0 si è sviluppato **usando LIMET stesso**: il metodo spec-driven applicato alla propria costruzione. Questi documenti sono stati i primi artefatti LIMET, e il progetto si è costruito col proprio metodo (`/limet-new` → task → test → archive).
