---
name: limet-new
description: 'Start a LIMET cycle for a feature or change: generates proposal, spec, plan, task list, test plan and e2e.'
user-invocable: true
allowed-tools: Read, Grep, Glob, Write
---

# LIMET — new cycle ($ARGUMENTS)

Generate in `limet/changes/<data-slug>/` the documents below, **in order**, starting from the content of `$ARGUMENTS`.
`<data-slug>` = `YYYY-MM-DD-slug` derived from `$ARGUMENTS` (e.g. `2026-11-20-login-page`).
Write in the language configured in `config/config.yaml` + `config/config.local.yaml` (key `language`, values `it`/`en`); if absent, in the user's language. Each document is instantiated from the inline template below and must not stay empty.

## Documents to generate

1. `CHANGE_PROPOSAL.md` — the *why*: problem, what changes, impact.
2. `SPEC.md` — the *what*, verifiable: requirements + given/when/then scenarios.
3. `PLAN.md` — the *how* at design level: approach, alternatives, risks.
4. `TASK_LIST.md` — granular tasks with status, dependencies, test strategy, empty change log.
5. `TEST_PLAN.md` — unit + e2e + lint/type (if configured), with re-run commands.
6. `E2E_VERIFICATION.md` — step-by-step checklist for manual verification.
7. `DECISIONS.md` — only if hard-to-reverse decisions emerge (ADR-lite).

## Binding rules

- Any ambiguous choice → explicit question to the user with a date. **Never assume silently.**
- Every task must have a verification strategy (unit + e2e + lint/type if configured), even with justified "n/a".
- Never run build/test: provide the commands, the user runs them and reports the outcome.
- Ensure the project `.gitignore` contains `limet/.test-logs/` (add the line if missing, so transient test logs don't end up in the repo).
- Before implementing a task, give a **2-3 line brief** (what, files touched, linked verification) and proceed without waiting for confirmation.
- Never commit/push/migrate/deploy without explicit authorization.

---

## CHANGE_PROPOSAL template

```markdown
# Change proposal — [capability/change name]

## Metadata
- Creation date: [YYYY-MM-DD]
- Status: `DRAFT | APPROVED | IN PROGRESS | COMPLETED | ABANDONED`
- Approved by / date: [who — YYYY-MM-DD]
- Linked spec: [SPEC file]
- Linked design: [PLAN/DESIGN file]

## Why
[Problem/opportunity; why now; what happens if not done.]

## What changes (summary)
- [change 1]
- [change 2]

## Capability
### New capabilities
- `name`: [description]
### Modified capabilities
- `name`: [what changes and why]
### Removed/deprecated capabilities
- `name`: [reason + migration plan]

## Impact
- Code/modules affected: [...]
- API/contracts affected: [...] (backward compatibility)
- External dependencies: [...]
- Existing data: [migration? backward-compatible?]

## Open contextual questions
| # | Question | Answer | Date | By |
| - | -------- | ------ | ---- | -- |

## Verification strategy
- Unit tests: [ref. TEST_PLAN.md]
- E2E tests: [ref. E2E_VERIFICATION.md]

## Outcome (at closure, before archiving)
- Date: [...]
- Summary: [...]
- Deviations from the original proposal: [...]
```

## SPEC template

```markdown
# Spec — Capability: [name]

## Metadata
- Linked proposal: [CHANGE_PROPOSAL file]
- Status: `DRAFT | APPROVED | IMPLEMENTED`
- Version: [N]

## Capability description
[Observable behavior, not implementation.]

## Requirements
### Requirement N: [short title]
[Description.]

**Scenarios** (given/when/then):
- **Given** [precondition], **when** [action], **then** [expected result].
- **Given** [edge case], **when** [...], **then** [...].

## Constraints and edge cases
- [constraint / edge case]

## Out of scope (explicitly not covered)
- [behavior not guaranteed]

## Traceability to tests
| Requirement | Unit test | E2E test |
| --- | --- | --- |
| Requirement 1 | [ref.] | [ref.] |
```

## PLAN template

```markdown
# Plan — [feature / bug fix name]

## Metadata
- Creation date: [YYYY-MM-DD]
- Status: `DRAFT | APPROVED | IN PROGRESS | COMPLETED | ABANDONED`
- Approved by / date: [who — YYYY-MM-DD]

## 1. Goal
[2-4 sentences: what and why, not yet how.]

## 2. Scope
### In scope
- [...]
### Out of scope
- [...] (reason)

## 3. Current state
[Verified by facts, not assumption.]
- [component]: [what it does today]

## 4. Open contextual questions
| # | Question | Answer | Date | By |

## 5. Proposed approach
[Design: components touched, logic introduced/modified.]

### Alternatives considered and rejected
- **Alternative A**: [description] — rejected because [reason].

## 6. Activity list
[The granular detail goes in TASK_LIST.md — always generate TASK_LIST.md.]

## 7. Verification strategy (mandatory)
- Unit tests: [yes/no + ref. TEST_PLAN.md]
- E2E tests: [yes/no + ref. E2E_VERIFICATION.md]

## 8. Risks and impacts
- [risk] — mitigation: [...]
- Backward compatibility: [...]

## 9. Operational notes
- Commit/push: [who performs them]
```

## TASK_LIST template

```markdown
# Task list — [name]

## Status legend
- `pending` / `in_progress` / `blocked` / `done` (completed **and verified**; annotate `YYYY-MM-DD HH:MM`)

## Task table
| # | Title | Purpose (non-technical) | Status | Depends on | Detail | Notes |
| - | ----- | ----------------------- | ------ | ---------- | ------ | ----- |

## Test strategy — mandatory for every task
| # task | Planned unit tests | Planned e2e tests | If omitted, justification |
| ------ | ------------------ | ----------------- | ------------------------ |

## Change log — one row per touched file
| Task | File | Type | What changed | Why | Linked verification |
| ---- | ---- | ---- | ------------ | --- | ------------------- |

## Implementation outcome (at closure)
- Date / Summary / Deviations / Test outcome
```

## TEST_PLAN template

```markdown
# Test plan — [name]

## References
- Linked plan/proposal: [...]
- Linked task(s): [...]

## Verification scope
[...]

## Planned unit tests
| # | What it verifies | Test file/class | Case (happy / edge / regression) |
| - | ---------------- | --------------- | -------------------------------- |

### Quality self-review (mandatory)
- Mental sabotage: which code change would NOT make any test fail?
- [ ] Every assert can fail for the stated reason
- [ ] Expected not derived from the object under test
- [ ] Contract verified (missing/empty/invalid inputs), not only happy path

## Planned e2e tests
| # | Scenario | Preconditions | Main steps | Expected outcome |
| - | -------- | ------------- | ---------- | ---------------- |

## Required test data
[...]

## Cases excluded from testing (and why)
- [...]

## Who runs
- Test authoring: [...] / Execution: [...]

## Re-runnable test commands
- [exact command to re-run each test]
```

## E2E_VERIFICATION template

```markdown
# Manual e2e verification — [name]

## References
- Linked plan/task: [...]
- Verification environment: [local/test/staging/production]

## Preconditions
- [...]

## Pre-verification state (check BEFORE the steps)
- Check: [...] (e.g. SELECT/SQL, file, config)

## Verification steps
1. [Step 1 — precise action]
   - **Expected outcome**: [...]
2. [...]

## Post-verification state (check AFTER the steps)
- Check: [...]

## Edge cases to verify
- [...]

## Execution outcome (to be filled by who runs it)
- Date/time / Run by / Outcome (`OK | KO`) / Notes
```

## DECISIONS template (ADR-lite — only if hard-to-reverse decisions emerge)

```markdown
# Decisions (ADR-lite)

| # | Decision | Status | Date | Context | Consequences |
| - | -------- | ------ | ---- | ------- | ------------ |
| 1 | [...]    | `accepted` | [YYYY-MM-DD] | [why] | [...] |
```

> Status: `accepted` or `superseded` (with reference to the decision that replaces it).
> Record only hard-to-reverse decisions; not the full ADR lifecycle.
