#!/usr/bin/env bash
# LIMET — intent + related projects hook (UserPromptSubmit)
# Rileva intento feature/bug E progetti collegati; inietta i reminder.
# Fail-safe: qualunque errore → exit 0 (mai bloccare Claude).

set -u

input="$(cat 2>/dev/null)" || exit 0

python - "$input" <<'PYEOF'
import sys, json, os, re

try:
    d = json.loads(sys.argv[1])
except Exception:
    sys.exit(0)

prompt = d.get("prompt") or ""
cwd = d.get("cwd") or os.getcwd()
root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.getcwd()

hints = []

# 1) intento feature/bug
if prompt:
    p = prompt
    if re.search(r'(aggiung|nuova (feature|funzionalit|pagina|sezione)|implementa|crea una|sviluppa|feature)', p, re.I):
        hints.append("rilevato intento feature. Avvia il flusso spec-driven: /limet-new")
    elif re.search(r'onboarding|\b(analizza|documenta|mappa)\b.{0,30}\b(progetto|codebase|repo|architettura)\b', p, re.I):
        hints.append("rilevato intento analisi progetto. Avvia: /limet-analyze")
    elif re.search(r'limet[-:]?bug', p, re.I):
        pass  # falso positivo: nome comando, non un report bug
    elif re.search(r'\b(bug|non funziona|non va|errore|crash|difetto|correggi|fixa|sistemare)\b', p, re.I):
        hints.append("rilevato intento bug. Avvia il flusso spec-driven: /limet-bug")

# 2) progetti collegati (dal cwd della sessione)
name = os.path.basename(cwd.rstrip("\\/"))
slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
reg_path = os.path.join(root, "mcp", "projects.json")
if os.path.exists(reg_path):
    try:
        with open(reg_path, encoding="utf-8-sig") as f:
            reg = json.load(f)
        linked = (reg.get(slug) or {}).get("collections") or []
        if linked:
            hints.append(
                "progetto collegato: %s è collegato alle collection %s. "
                "Per il contesto documentale usa cerebro_search con project=%s "
                "(interroga sia %s sia i collegati)."
                % (slug, ", ".join(linked), slug, slug)
            )
    except Exception:
        pass

if not hints:
    sys.exit(0)

msg = "LIMET: " + " | ".join(hints)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": msg,
    }
}))
PYEOF

exit 0
