#!/usr/bin/env bash
# LIMET — changelog hook (PostToolUse, matcher Edit|Write)
# Appende automaticamente una riga al "Registro modifiche" del TASK_LIST attivo.
# Anti-rumore: solo file in scope, coalesce (una riga per file). Fail-safe: exit 0.

set -u

input="$(cat 2>/dev/null)" || exit 0

python - "$input" <<'PYEOF'
import sys, json, os, re, glob

try:
    d = json.loads(sys.argv[1])
except Exception:
    sys.exit(0)

tool = d.get("tool_name", "")
if tool not in ("Edit", "Write"):
    sys.exit(0)

fp = d.get("tool_input", {}).get("file_path", "") or ""
if not fp:
    sys.exit(0)

cwd = d.get("cwd", os.getcwd())

# TASK_LIST attivo: il più recente tra limet/changes/*/TASK_LIST.md
cands = glob.glob(os.path.join(cwd, "limet", "changes", "*", "TASK_LIST.md"))
if cands:
    task_list = max(cands, key=os.path.getmtime)
else:
    p = os.path.join(cwd, "limet", "TASK_LIST.md")
    if not os.path.exists(p):
        sys.exit(0)
    task_list = p

# scope: escludi framework LIMET e rumore
rel = os.path.relpath(fp, cwd)
if rel.startswith("limet/changes") or rel.startswith("limet/archive") or rel.startswith("..") or re.search(r'(^|/)(\.git|node_modules|__pycache__|dist|build|\.vite|graphify-out|\.claude)(/|$)', rel):
    sys.exit(0)

tipo = "creato" if tool == "Write" else "modificato"

with open(task_list, "r", encoding="utf-8") as f:
    content = f.read()

# coalesce: file già tracciato → non duplicare
if rel in content:
    sys.exit(0)

row = "| —    | `%s` | %s | (auto) | (da completare) | (da verificare) |" % (rel, tipo)

lines = content.splitlines()
idx = None
in_reg = False
for i, ln in enumerate(lines):
    if ln.startswith("## Registro modifiche"):
        in_reg = True
        continue
    if in_reg and ln.startswith("## "):
        idx = i
        break
if not in_reg:
    sys.exit(0)
if idx is None:
    idx = len(lines)

lines.insert(idx, row)
with open(task_list, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
PYEOF

exit 0
