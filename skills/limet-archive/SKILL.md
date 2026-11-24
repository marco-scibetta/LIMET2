---
name: limet-archive
description: Archive finished and verified work.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# LIMET — archive

1. Verify the work is **finished and verified** (tasks `done`, tests run and recorded).
   If verification is missing, do not archive: flag it and ask for the outcome.
2. Move `limet/changes/<data-slug>/` to `limet/archive/<data-slug>/`.
3. Generate the archive entry as a final summary (template below) — do not rewrite history:
   the detailed documents remain linked by reference.
4. Remind the user to re-index (never run by the agent).

## Binding rules

- Archive only verified work; without verification → stop and flag it.
- Never commit/push without explicit authorization.

---

## ARCHIVE_ENTRY template

```markdown
# Archive entry — [change name]

## Metadata
- Change name: [...]
- Type: `feature | bug fix | refactor | other`
- Completion date: [YYYY-MM-DD HH:MM]
- Author(s): [...]

## Summary
[3-5 lines, understandable months later without context.]

## Linked documents (reference, not copy)
- Plan/proposal: [link]
- Task list: [link]
- Test plan/execution: [link]
- Non-technical summary: [link, if present]
- Bug report: [link, if applicable]

## Key decisions made during the work
[most relevant contextual questions + answers, so the "why" is not lost.]

## Final verification outcome
- Unit tests: [OK/KO, reference]
- E2E tests: [OK/KO, reference]
- Known residual issues: [...]

## Lessons learned (optional)
[...]

## Context re-indexing
- [ ] Remind the user: Launcher → Re-index → Incremental → click Re-index.
      Re-indexing belongs to the user, never the agent.
```
