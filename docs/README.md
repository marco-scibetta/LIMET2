# LIMET 2.0 — indice

**L**ightweight **I**terative **M**ethod for **E**ngineering with **T**raceability — versione 2.0, **nativa Claude Code**.

LIMET 2.0 è la riscrittura di LIMET 1.0 per sfruttare le feature native di Claude Code: **skill, hook, subagent, plugin, MCP, slash command**. Stessa filosofia (leggero, spec-driven, traceability, test non-negoziabile), ma ottimizzata: **Claude genera i documenti, non l'umano li riempie**.

## Differenza chiave 1.0 → 2.0

| | LIMET 1.0 | LIMET 2.0 |
|---|---|---|
| Template | 18 .md da riempire a mano | **5 skill** che Claude esegue |
| Regole (§1.3, §1.5) | testo in CLAUDE.md | **hook** (enforcement) |
| Attivazione | script PowerShell/bash | **plugin** + `/limet:init` |
| CEREBRO/Graphify | skill-guida + script Python/CLI | **MCP** (tool nativi) |
| Target | tool-agnostic (Copilot/Claude) | **Claude-only** |

## Indice dei documenti

| Doc | Cosa contiene |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | architettura complessiva + mappatura 1.0→2.0 |
| [SKILLS.md](SKILLS.md) | le 5 skill (ciclo di vita) con esempio SKILL.md |
| [HOOKS.md](HOOKS.md) | i 3 hook (guardrail, change log, reminder) con hooks.json |
| [SUBAGENTS.md](SUBAGENTS.md) | i 2 subagent (writer, gate) |
| [MCP.md](MCP.md) | CEREBRO + GRAPHIFY come MCP (thin wrapper) |
| [PLUGIN.md](PLUGIN.md) | packaging/distribuzione del plugin `limet` |
| [OPTIMIZATIONS.md](OPTIMIZATIONS.md) | le ottimizzazioni e le motivazioni |
| [MIGRATION.md](MIGRATION.md) | come migrare da LIMET 1.0 a 2.0 |

## Il ciclo di vita (in una riga)

`/limet:new` (proposta→spec→plan) → `/limet:task` (implementa, change log automatico) → `/limet:test` (verifica) → `/limet:archive`. Con `/limet:bug` per i bug.

## Stato

- Questo documento è il **design** di LIMET 2.0, non l'implementazione.
- L'implementazione (file `.claude/`, plugin, MCP reali) è il passo successivo.
- Linguaggio: italiano (EN aggiungibile dopo).

## Come nasce LIMET 2.0 (dogfooding)

LIMET 2.0 si sviluppa **usando LIMET stesso**: il metodo spec-driven si applica alla propria costruzione. Questi documenti (`README`, `ARCHITECTURE`, `SKILLS`, …) sono i primi artefatti LIMET e, quando si crea il nuovo repo, vivranno nella cartella **`docs/`** del progetto LIMET 2.0 (come già previsto nella struttura in [PLUGIN.md](PLUGIN.md)).

Ciclo previsto: `/limet:new` su "LIMET 2.0" → questi doc diventano SPEC/DESIGN → TASK_LIST → implementazione → test → archive. Il progetto si costruisce col proprio metodo.
