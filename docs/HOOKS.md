# LIMET 2.0 — Hooks

Hooks are **deterministic** (zero context unless they return output). In LIMET 2.0 they are the **guardrails**: the non-negotiable rules move from text to enforcement.

## The 6 hooks

| Hook | Event | Purpose |
|---|---|---|
| **resume** | `SessionStart` | **resumes the active cycle** at session start: injects the unfinished tasks |
| **intent** | `UserPromptSubmit` | **detects intent** (feature / bug / project analysis) and starts the LIMET flow **without the user typing commands** |
| **guardrail** | `PreToolUse` (Bash) | blocks autonomous build/test + commands with persistent effects + irreversible destructive ones without authorization |
| **changelog** | `PostToolUse` (Edit/Write) | appends automatically to the TASK_LIST.md change log |
| **precompact** | `PreCompact` | **injects the active cycle state** before compaction (tasks + touched files), so context is not lost |
| **reminder** | `Stop` | verifies test + archive before closing |

**The `intent` hook is what makes LIMET conversational** (like LIMET 1.0): the user talks normally, Claude recognizes the intent and starts the flow. No command to type.

## Example `hooks/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/resume.sh\"" }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/intent.sh\"" }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/guardrail.sh\"" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/changelog.sh\"" }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/precompact.sh\"" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/reminder.sh\"" }
        ]
      }
    ]
  }
}
```

## resume.sh (logic)

- Fires at `SessionStart`.
- If an active cycle exists (`limet/changes/*/TASK_LIST.md`, most recent) with `pending/in_progress/blocked` tasks → injects: "active cycle `slug` — unfinished tasks: #X. Resume from the first."
- Otherwise: exit 0 (no output).

## intent.sh (logic)

- Receives the user's prompt.
- If it contains feature/bug intent (e.g. "add", "I want a feature", "there is a bug", "doesn't work") → suggests `/limet-new` or `/limet-bug`.
- If it contains project analysis intent (e.g. "analyze the project", "onboarding", "document the project") → suggests `/limet-analyze`.
- Otherwise: exit 0 (no output).

## guardrail.sh (logic)

- If the Bash command contains `mvnw`, `./gradlew`, `npm test`, `pytest`, `cargo test`, etc. → **blocks** (exit 2) with the message: "LIMET: build/test must not run autonomously. Give the command to the user."
- If the command contains `git commit`, `git push`, `git rebase`, `migrate`, `deploy` → **blocks** without explicit authorization.
- If the command contains `git reset --hard`, `git clean`, `git checkout --`, `git branch -D`, `git stash drop`, `rm -rf` → **blocks** (irreversible destructive).
- Otherwise: exit 0 (no output, zero context).

## changelog.sh (logic)

- Receives the tool + the touched file.
- **Anti-noise**: logs only files **in the active task's scope**; **coalesces** multiple edits to the same file (one row per file, not one per edit).
- If `limet/TASK_LIST.md` exists → appends/updates the row: `<timestamp> <file> — <tool>`.
- If no active task → exit 0 (no output).

## precompact.sh (logic)

- Fires at `PreCompact`, before context compaction.
- If there is an active cycle → injects: cycle slug + unfinished tasks + last touched files (change log).
- Makes compaction "lossless" for the LIMET state: Claude does not forget where it is.
- If no active cycle → exit 0.

## reminder.sh (logic)

- Reads the current task's state.
- If there is a task without a test section or not archived → prints a reminder: "LIMET: unfinished/unverified tasks #X. Run the tests with `!bash <plugin>/scripts/run-tests.sh`, then /limet-test and /limet-archive."
- If all good → no output.

## Fail-safe (all hooks)

Every hook is in `try/catch`: **a crashing hook must NEVER block Claude**. On error → exit 0 + optional diagnostic log. A broken guardrail that blocks work is worse than no guardrail.

## Principle

> **An instruction is a request. A hook is enforcement.**

Rules §1.3 (no autonomous build/test) and §1.5 (non-negotiable testing) are no longer "written in CLAUDE.md hoping Claude follows them": they are **enforced** by the hooks.
