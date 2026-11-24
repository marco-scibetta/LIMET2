#!/usr/bin/env bash
# LIMET — resume hook (SessionStart)
# Se esiste un ciclo attivo, inietta lo stato (task non conclusi) all'avvio sessione.
# Fail-safe: qualunque errore → exit 0 (mai bloccare Claude).

set -u

input="$(cat 2>/dev/null)" || exit 0

python - "$input" <<'PYEOF'
import sys, json, os, glob, re

try:
    d = json.loads(sys.argv[1])
except Exception:
    d = {}

cwd = d.get("cwd") or os.getcwd()

# Ciclo attivo: il più recente tra limet/changes/*/TASK_LIST.md.
cands = glob.glob(os.path.join(cwd, "limet", "changes", "*", "TASK_LIST.md"))
if cands:
    task_list = max(cands, key=os.path.getmtime)
    slug = os.path.basename(os.path.dirname(task_list))
else:
    p = os.path.join(cwd, "limet", "TASK_LIST.md")
    if not os.path.exists(p):
        sys.exit(0)
    task_list = p
    slug = "limet"

with open(task_list, "r", encoding="utf-8") as f:
    content = f.read()

incomplete = []
for m in re.finditer(r'^\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*`?(pending|in_progress|blocked)`?', content, re.M):
    incomplete.append(m.group(1))

if not incomplete:
    sys.exit(0)

ids = ", ".join(incomplete)
msg = "LIMET: active cycle `%s` — unfinished tasks: #%s. Resume from the first." % (slug, ids)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": msg,
    }
}))
PYEOF

exit 0
