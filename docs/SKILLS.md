# LIMET 2.0 — Skills

The skills are LIMET's **lifecycle**. They are **NOT meant to be run by hand**: they activate **automatically** from CLAUDE.md (always-on policy) and from the `UserPromptSubmit` hook (intent detection). The user **talks normally** ("I want to add feature X" / "there is bug Y") and Claude starts the flow on its own — **like LIMET 1.0, no command to type**.

The `/limet-*` commands exist only as **optional shortcuts** for explicit control, not as the primary interaction.

Standard frontmatter (AgentSkills.io): `name`, `description`, `allowed-tools`, `user-invocable`. Progressive disclosure: metadata → SKILL.md body → file reference.

## The 6 skills

| Skill | What it does | Input | Output |
|---|---|---|---|
| `/limet-new` | full cycle: proposal + spec + plan + task + test + e2e | `$ARGUMENTS` = idea/feature | `limet/` with all docs |
| `/limet-task` | runs a task + change log | `$1` = task id (e.g. `task3`) | code + change log |
| `/limet-test` | generates/runs the test plan | — | TEST_PLAN + TEST_EXECUTION |
| `/limet-archive` | archives finished work | — | `limet/archive/<data-slug>/` |
| `/limet-bug` | structured bug report | `$ARGUMENTS` = description | BUG_REPORT.md |
| `/limet-analyze` | analyzes an undocumented project → onboarding docs in `docs/` | — | `docs/` (7 docs) |

The support templates (glossary, conventions, codebase-analysis, architecture, module-map, summary, **decisions**) are generated **ad hoc** inside `/limet-new`, not as separate skills.

**`decisions.md` = ADR-lite** (idea from ECC): **hard-to-reverse** decisions ("why do we use the point-in-time universe?") deserve a dedicated dated record with status (*accepted / superseded*), separate from spec/plan. Not the full ADR lifecycle — just a light log.

## SKILL.md example — `/limet-new`

```markdown
---
name: limet-new
description: Start a LIMET cycle for a new feature. Generates Change Proposal, SPEC, PLAN, TASK_LIST, TEST_PLAN and E2E_VERIFICATION. Use when the user asks for a new feature or says "/limet-new <idea>".
user-invocable: true
allowed-tools: Read, Grep, Glob, Write
---

# LIMET — new cycle ($ARGUMENTS)

Generate in `limet/` the following documents, in order, from the content of $ARGUMENTS:

1. `CHANGE_PROPOSAL.md` — what, why, impact (inline template below).
2. `SPEC.md` — what it must do (behavior, not implementation).
3. `PLAN.md` — how, at design level.
4. `TASK_LIST.md` — granular tasks, with an empty "Change log" section.
5. `TEST_PLAN.md` — unit + e2e + lint/type (if configured), with re-run command.
6. `E2E_VERIFICATION.md` — end-to-end steps.
7. `DECISIONS.md` — hard-to-reverse decisions (ADR-lite), only if they emerge.

Rules (binding):
- Any ambiguous choice → explicit question to the user (never assume).
- Every task must have a verification strategy (unit + e2e + lint/type if configured), even justified "n/a".
- Never run build/test: provide the commands, the user runs them.

## CHANGE_PROPOSAL template
(1.0 template content, inline)
## SPEC template
(...)
```

## Rules shared by all skills

1. **Never assume**: ambiguous choices → explicit question with a date.
2. **Never build/test autonomously**: provide the command, the user runs it and reports the outcome.
3. **Traceability**: every created/modified file ends up in the change log (via the PostToolUse hook).
4. **Language**: reply in the user's language.
5. **Brief before every task**: before implementing, give a 2-3 line brief (what, files touched, linked verification), then proceed without waiting for confirmation.

## Why 6 and not 18

The 18 1.0 templates were "documents to fill by hand". In 2.0, the **flow** generates them together (`/limet-new`), the **change log** is automatic (hook), the **archive** is a skill, the **bug** is a skill. The rest is support generated on demand. Less friction, same traceability.
