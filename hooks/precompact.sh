#!/usr/bin/env bash
# LIMET — precompact hook (PreCompact)
# Inietta lo stato del ciclo attivo prima della compattazione, così il contesto non si perde.
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

parts = ["LIMET: pre-compattazione — ciclo attivo `%s`." % slug]

incomplete = []
for m in re.finditer(r'^\|\s*(\d+)\s*\|[^|]*\|[^|]*\|\s*`?(pending|in_progress|blocked)`?', content, re.M):
    incomplete.append(m.group(1))
if incomplete:
    parts.append("Task non conclusi: #%s." % ", ".join(incomplete))
else:
    parts.append("Tutti i task conclusi.")

# File toccati di recente (registro modifiche), per ricordare cosa è stato cambiato.
reg = re.search(r'## Registro modifiche.*', content, re.S)
if reg:
    rows = re.findall(r'^\|\s*(?:—|\d+)\s*\|\s*`([^`]+)`', reg.group(0), re.M)
    if rows:
        parts.append("File toccati: " + ", ".join(rows[-10:]) + ".")

msg = " ".join(parts)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreCompact",
        "additionalContext": msg,
    }
}))
PYEOF

exit 0
