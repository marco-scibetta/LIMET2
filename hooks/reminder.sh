#!/usr/bin/env bash
# LIMET — reminder hook (Stop)
# Se ci sono task non conclusi/verificati, inietta un reminder. Fail-safe: exit 0.

set -u

input="$(cat 2>/dev/null)" || exit 0

python - "$input" <<'PYEOF'
import sys, json, os, glob, re

cwd = os.getcwd()
cands = glob.glob(os.path.join(cwd, "limet", "changes", "*", "TASK_LIST.md"))
if cands:
    task_list = max(cands, key=os.path.getmtime)
else:
    p = os.path.join(cwd, "limet", "TASK_LIST.md")
    if not os.path.exists(p):
        sys.exit(0)
    task_list = p

with open(task_list, "r", encoding="utf-8") as f:
    content = f.read()

# Task non conclusi: righe della tabella con stato pending/in_progress/blocked.
incomplete = []
for m in re.finditer(r'^\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*`?(pending|in_progress|blocked)`?', content, re.M):
    incomplete.append(m.group(1))

if not incomplete:
    sys.exit(0)

ids = ", ".join(incomplete)
root = os.environ.get("CLAUDE_PLUGIN_ROOT") or ""
run = ""
if root:
    run = ' Run the tests: !bash "%s/scripts/run-tests.sh" (or add the exact command).' % root
msg = "LIMET: unfinished/unverified tasks: #%s.%s Then /limet-test and /limet-archive." % (ids, run)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "Stop",
        "additionalContext": msg,
    }
}))
PYEOF

exit 0
