---
name: limet-analyze
description: 'Analyze an undocumented project: generate onboarding docs in docs/ via the limet-analyzer subagent.'
user-invocable: true
allowed-tools: Read, Grep, Glob, Agent
---

# LIMET — analyze project ($ARGUMENTS)

Start the analysis of the current project to generate onboarding documents in `docs/`.

## Flow

1. Determine the project slug from the current directory name (as `hooks/intent.sh` does).
2. Check the `analyze` flag in `config/config.yaml` + `config/config.local.yaml`:
   - if `projects.<slug>.analyze` is `true`, proceed;
   - otherwise ask the user for confirmation before proceeding (never assume).
3. Spawn the `limet-analyzer` subagent (subagent_type `limet:limet-analyzer`) on the current project.
4. At the end, verify that the 7 expected documents exist in `docs/` and report the outcome.

## Binding rules

- Do not run build/test; do not modify the target project's code.
- Re-indexing the generated documents belongs to the user (never index autonomously).
- If the flag is inactive and the user does not confirm, stop without proceeding.
