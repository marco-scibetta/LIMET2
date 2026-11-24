---
name: limet-bug
description: Create a structured bug report.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit
---

# LIMET — bug ($ARGUMENTS)

Write `BUG_REPORT.md` from the content of `$ARGUMENTS`, following the template below.

**Where**: if an active `limet/changes/<data-slug>/` folder exists, write `BUG_REPORT.md` there.
Otherwise create `limet/changes/<data-slug>/` with `<data-slug>` = `YYYY-MM-DD-slug` derived from
`$ARGUMENTS` (e.g. `2026-11-20-save-button-does-not-work`).

## Binding rules

- Distinguish **observed behavior** (facts, evidence) from **hypotheses**.
- Write the root cause only after investigation, with a precise reference to code/log.
- Mandatory verification strategy: a regression test that **fails with the bug present** and passes after the fix.

---

## BUG_REPORT template

```markdown
# Bug report — [short defect title]

## Metadata
- Report date: [YYYY-MM-DD]
- Reported by: [...]
- Status: `OPEN | ANALYZING | IN FIX | RESOLVED | NOT REPRODUCIBLE | NOT A BUG`
- Severity: `blocking | high | medium | low`

## Observed behavior
[facts + evidence: logs, error messages, screenshots, steps that produced it.]

## Expected behavior
[what should happen according to the spec.]

## Steps to reproduce
1. [step 1]
2. [step 2]

## Environment
- Version/branch/commit: [...]
- Environment: [local/test/production]
- Required test data: [...]

## Root cause analysis
- Identified cause: [...]
- File/component involved: [path, lines]
- Why it happens: [...]

## Impact
- Who/what is affected: [...]
- Since when: [version/commit, if known]
- Workaround: [yes/no + description]

## Proposed fix
[minimal change to the root cause, not just the symptom.]

## Verification strategy (mandatory)
- Regression unit test: [must fail with the bug and pass after the fix]
- E2E test: [if necessary]

## Linked verification tasks
- [...]

## Outcome (at closure)
- Resolution date / Commit/PR / Notes
```
