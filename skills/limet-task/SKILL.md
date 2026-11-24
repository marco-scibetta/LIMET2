---
name: limet-task
description: 'Run a task from the TASK_LIST: brief, implementation and change log.'
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit
---

# LIMET — run task ($ARGUMENTS)

`$ARGUMENTS` = task id (e.g. `3` or `task3`).

## Flow

1. Read the active `TASK_LIST.md` in `limet/changes/<data-slug>/` and locate the requested task.
2. **Mandatory brief** (before touching any file): 2-3 lines with *what you will do*, *files you will touch*,
   *linked verification*. Then proceed **without waiting for confirmation**.
3. Implement the task, staying within the declared scope.
4. Record every created/modified file in the **"Change log"** section of `TASK_LIST.md`
   (one row per file: task, path, type, what changed, why, linked verification).
5. **Do not mark `done`** until verification is run: give the user the test/verification commands
   and stay on standby until the outcome arrives.

## Binding rules

- Any ambiguous choice → explicit question to the user with a date. **Never assume silently.**
- Never run build/test: provide the commands, the user runs them and reports the outcome.
- Never commit/push/migrate/deploy without explicit authorization.
- Stay within the task scope; any deviation → flag it and ask for approval.

## Brief format

```text
Brief #<id> — <title>
- What: <one line>
- Files touched: <list>
- Verification: <command or check>
```
