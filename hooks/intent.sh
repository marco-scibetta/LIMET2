#!/usr/bin/env bash
# LIMET — intent hook (UserPromptSubmit)
# Rileva intento feature/bug nel prompt dell'utente e inietta un suggerimento per
# avviare il flusso spec-driven, senza che l'utente digiti comandi.
# Fail-safe: qualunque errore → exit 0 (mai bloccare Claude).

set -u

input="$(cat 2>/dev/null)" || exit 0

# Estrae il campo "prompt" dal JSON in stdin (richiede python nel PATH).
prompt="$(printf '%s' "$input" | python -c '
import sys, json
try:
    print(json.load(sys.stdin).get("prompt", "") or "")
except Exception:
    print("")
' 2>/dev/null)"

[ -z "$prompt" ] && exit 0

kind=""
if printf '%s' "$prompt" | grep -Eiq '(aggiung|nuova (feature|funzionalit|pagina|sezione)|implementa|crea una|sviluppa|feature)'; then
  kind="feature"
elif printf '%s' "$prompt" | grep -Eiq '(bug|non funziona|non va|errore|crash|difetto|correggi|fixa|sistemare)'; then
  kind="bug"
fi

[ -z "$kind" ] && exit 0

if [ "$kind" = "feature" ]; then
  hint="LIMET: rilevato intento feature. Avvia il flusso spec-driven: /limet-new"
else
  hint="LIMET: rilevato intento bug. Avvia il flusso spec-driven: /limet-bug"
fi

printf '{"hookSpecificOutput":{"hookEventName":"UserPromptSubmit","additionalContext":"%s"}}\n' "$hint"

exit 0
