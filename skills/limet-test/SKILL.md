---
name: limet-test
description: Generate the test plan and record the actual test outcome.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit
---

# LIMET — test

Generate/update in `limet/changes/<data-slug>/`:

1. `TEST_PLAN.md` — unit + e2e, **before** the code, with quality self-review (§5.1).
2. `TEST_EXECUTION.md` — **always generated**: if tests have not been run yet, generate the
   structure with "to be filled once executed" fields; if they have been run, paste the real
   logs (not summaries from memory).

## Binding rules

- Do not run the tests yourself: provide the commands, the user runs them and reports the outcome. Suggest `!bash scripts/run-tests.sh <command>` (outcome in TEST_EXECUTION, log destroyed if OK).
- Quality self-review is mandatory before declaring the plan complete.
- Every task has unit + e2e + lint/type (if configured), even with justified "n/a".

---

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

## TEST_EXECUTION template

```markdown
# Test execution — [name]

## References
- Linked plan: [...]

## Execution metadata
- Date/time: [YYYY-MM-DD HH:MM] / Run by: [...] / Environment: [...] / Command run: [...]

## Unit test outcome
- Total / Passed / Failed / Skipped
- Log (paste the runner's real output)

## E2E test outcome
| # | Scenario | Outcome (OK / KO / not run) | Notes |
| - | -------- | -------------------------- | ----- |

## Anomalies found
- [...]

## Conclusion
- Overall outcome: `OK | KO | PARTIAL`
- Can the task move to `done`? [yes/no + reason]
```
