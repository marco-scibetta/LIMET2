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
    printf '\n## Esito test\n'
    printf -- '- Data: %s\n' "$TS"
    printf -- '- Comando: `%s`\n' "$CMD"
    printf -- '- Esito: OK (exit 0)\n'
  } >> "$CHANGE/TEST_EXECUTION.md"
  rm -f "$TMP" "$LOGDIR/raw.log"
  echo "OK — test passati. Log temporaneo distrutto."
else
  mv "$TMP" "$LOGDIR/raw.log"
  {
    printf '\n## Esito test\n'
    printf -- '- Data: %s\n' "$TS"
    printf -- '- Comando: `%s`\n' "$CMD"
    printf -- '- Esito: FAIL (exit %s)\n\n' "$RC"
    printf '## Fallimenti (ultime 30 righe)\n```\n'
    tail -n 30 "$LOGDIR/raw.log"
    printf '```\n'
  } >> "$CHANGE/TEST_EXECUTION.md"
  echo "FAIL (exit $RC) — log completo in $LOGDIR/raw.log"
fi

exit 0
