#!/usr/bin/env bash
# LIMET — run-tests (comando esplicito, NON hook)
# Esegue i test forniti, registra esito COMPATTO in TEST_EXECUTION.md.
# Output grezzo in temp: se OK viene DISTRUTTO, se KO resta in raw.log.
# Fail-safe: nessun ciclo attivo → fallback a limet/.

set -u

PROJ="$(pwd)"

# Comando di test = argomenti, o default pytest.
CMD="$*"
if [ -z "$CMD" ]; then
  set -- python -m pytest
  CMD="python -m pytest"
fi

# Ciclo attivo: il più recente tra limet/changes/*/.
CHANGE="$(ls -dt "$PROJ"/limet/changes/*/ 2>/dev/null | head -n1 | tr -d '\r')"
if [ -z "$CHANGE" ]; then
  CHANGE="$PROJ/limet"
fi
mkdir -p "$CHANGE"

LOGDIR="$PROJ/limet/.test-logs"
mkdir -p "$LOGDIR"
TMP="$LOGDIR/.run-tests.tmp.log"
TS="$(date '+%Y-%m-%d %H:%M')"

( cd "$PROJ" && "$@" ) > "$TMP" 2>&1
RC=$?

if [ "$RC" -eq 0 ]; then
  {
    printf '\n## Test outcome\n'
    printf -- '- Date: %s\n' "$TS"
    printf -- '- Command: `%s`\n' "$CMD"
    printf -- '- Outcome: OK (exit 0)\n'
  } >> "$CHANGE/TEST_EXECUTION.md"
  rm -f "$TMP" "$LOGDIR/raw.log"
  echo "OK — tests passed. Temporary log destroyed."
else
  mv "$TMP" "$LOGDIR/raw.log"
  {
    printf '\n## Test outcome\n'
    printf -- '- Date: %s\n' "$TS"
    printf -- '- Command: `%s`\n' "$CMD"
    printf -- '- Outcome: FAIL (exit %s)\n' "$RC"
    printf -- '- Full log: `%s`\n\n' "$LOGDIR/raw.log"
    printf '## Output tail (last 60 lines)\n```\n'
    tail -n 60 "$LOGDIR/raw.log"
    printf '```\n'
  } >> "$CHANGE/TEST_EXECUTION.md"
  echo "FAIL (exit $RC) — full log in $LOGDIR/raw.log"
fi

exit 0
