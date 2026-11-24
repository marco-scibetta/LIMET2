# LIMET 2.0 — Subagents

Subagents are **isolated contexts** for specific roles. LIMET 2.0 uses **3** (no more, to stay lightweight).

## The 3 subagents

| Subagent | Role | Tools | When |
|---|---|---|---|
| `limet-writer` | writes the documents (proposal/spec/plan/test) with isolated context | Read, Grep, Glob, Write | inside `/limet-new` |
| `limet-gate` | **validator**: verifies §1.5 (unit + e2e + lint/type) + **fresh-eyes review** + **drift report** (docs ↔ code) | Read, Grep, Glob | before `/limet-archive` and at task end |
| `limet-analyzer` | analyzes an undocumented project and generates onboarding docs in `docs/` | Read, Grep, Glob, Write | inside `/limet-analyze` |

## Example `agents/limet-gate.md`

```markdown
---
name: limet-gate
description: LIMET validator. Verifies §1.5 (unit + e2e + lint/type if configured), does a fresh-eyes review of SPEC/PLAN and a doc↔code drift report. Rejects tasks without verification. Read-only.
tools: Read, Grep, Glob
---

# limet-gate — validator

Checks `limet/TASK_LIST.md` and the test files. For every task marked "done":

1. Is there a dedicated unit test? (or an explicit "n/a" justification)
2. Is there an e2e verification with runnable steps?
3. Is the change log filled in?
4. Lint/typecheck run (if configured)?

### Fresh-eyes review ("goldfish" principle, from EGM)

Reviews the SPEC/PLAN with **fresh context** (isolated subagent, without the previous conversation), to catch implicit assumptions and blind spots the author does not see. A reviewer who has read everything does not see the void.

### Drift report

Compares SPEC/PLAN with the real code and reports the divergences ("the SPEC says X but the code does Y"). Proactive, not retroactive.

Output: list of `OK` / `FAIL` tasks + any blind spots and drift. If `FAIL`, the task is NOT closed.
```

## Example `agents/limet-writer.md`

```markdown
---
name: limet-writer
description: Writes the LIMET documents (proposal, spec, plan, task list, test plan, e2e) from an idea. Isolated context. Follows the LIMET templates.
tools: Read, Grep, Glob, Write
---

# limet-writer — document writer

From the received input, generates the LIMET documents in `limet/` following the templates.
Rules: spec-driven (§1.1), traceability (§1.2), non-negotiable testing (§1.5).
Never assume: ambiguous choices → report them as open questions.
```

## Objective gate: `/goal` (native enforcement of §1.5)

`/goal` (a native Claude Code feature) sets a **completion condition** and a **fast evaluator** (a separate lightweight model) verifies **objectively** whether it is satisfied, every time the agent tries to stop. It is the enforcement of §1.5 that today is only self-declared.

**Where to use it (1 point, no more):** at task end (`/limet-task`):
```
/goal "all unit + e2e tests for the task pass, type checker has zero errors"
```

**Relationship with `limet-gate`:** complementary, not overlapping.

| | Verification |
|---|---|
| `/goal` (fast evaluator) | **objective**: do the tests really pass? |
| `limet-gate` (subagent) | **documental**: fresh-eyes, drift, documented §1.5 |

## Why only 3

- `limet-writer` = all the "producing documents" (one role, not 18).
- `limet-gate` = quality control (the §1.5 principle as an independent gate).
- `limet-analyzer` = understanding an undocumented project (analysis → onboarding docs).

The two `limet-gate` extensions (fresh-eyes review + drift report) come from **EGM (Elephant-Goldfish Model)**: reviewing with "fresh eyes" and comparing docs↔code. They are small, **they don't add subagents** — they extend the existing one.

`limet-analyzer` was added when the flow required it (analysis of an undocumented project, dashboard trigger + `/limet-analyze`). Add others **only if** the flow really requires them — not for completeness. ("Do not over-engineer" constraint.)
