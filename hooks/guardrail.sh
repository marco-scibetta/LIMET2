#!/usr/bin/env bash
# LIMET — guardrail hook (PreToolUse, matcher Bash)
# Blocca build/test autonomi e comandi a effetti persistenti senza autorizzazione.
# Fail-safe: qualunque errore → exit 0 (mai bloccare Claude).

set -u

input="$(cat 2>/dev/null)" || exit 0

# Estrae il comando Bash dal campo tool_input.command del JSON in stdin.
cmd="$(printf '%s' "$input" | python -c '
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get("tool_input", {}).get("command", "") or "")
except Exception:
    print("")
' 2>/dev/null)"

[ -z "$cmd" ] && exit 0

# Build/test autonomi → blocca sempre.
if printf '%s' "$cmd" | grep -Eq '(mvnw|gradlew|mvn[[:space:]]|npm[[:space:]]+(test|run[[:space:]]+(test|build))|yarn[[:space:]]+(test|build)|pnpm[[:space:]]+(test|build)|pytest|python[[:space:]]+-m[[:space:]]+(pytest|unittest)|cargo[[:space:]]+(test|build)|go[[:space:]]+(test|build)|make[[:space:]]+(test|build))'; then
  echo "LIMET: build/test non in autonomia. Fornisci il comando all'utente e attendi l'esito." >&2
  exit 2
fi

# Effetti persistenti → blocca senza autorizzazione esplicita.
if printf '%s' "$cmd" | grep -Eq '(git[[:space:]]+(commit|push|rebase|merge)|migrate|deploy|kubectl[[:space:]]+apply|terraform[[:space:]]+apply)'; then
  echo "LIMET: comando a effetti persistenti (commit/push/migrate/deploy). Richiede autorizzazione esplicita dell'utente." >&2
  exit 2
fi

# Distruttivo irreversibile → blocca sempre.
if printf '%s' "$cmd" | grep -Eq '(git[[:space:]]+(reset[[:space:]]+--hard|clean|checkout[[:space:]]+--|branch[[:space:]]+-D|stash[[:space:]]+drop)|rm[[:space:]]+-[rRfF])'; then
  echo "LIMET: comando distruttivo irreversibile. Richiede autorizzazione esplicita dell'utente." >&2
  exit 2
fi

exit 0
