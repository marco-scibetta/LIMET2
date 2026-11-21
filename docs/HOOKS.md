# LIMET 2.0 — Hooks

Gli hook sono **deterministici** (zero contesto se non ritornano output). In LIMET 2.0 fanno le **guardrail**: le regole non-negoziabili passano da testo a enforcement.

## I 4 hook

| Hook | Evento | Scopo |
|---|---|---|
| **intent** | `UserPromptSubmit` | **rileva l'intento** ("voglio una feature"/"c'è un bug") e avvia il flusso LIMET **senza che l'utente scriva comandi** |
| **guardrail** | `PreToolUse` (Bash) | blocca build/test autonomi + comandi a effetti persistenti senza autorizzazione |
| **changelog** | `PostToolUse` (Edit/Write) | appende automaticamente al change log di TASK_LIST.md |
| **reminder** | `Stop` | verifica test + archivio prima di chiudere |

**L'hook `intent` è ciò che rende LIMET conversazionale** (come LIMET 1.0): l'utente parla normalmente, Claude riconosce l'intento e parte col flusso. Nessun comando da digitare.

## Esempio `hooks/hooks.json`

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/intent.sh\""
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/guardrail.sh\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/changelog.sh\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PLUGIN_ROOT/hooks/reminder.sh\""
          }
        ]
      }
    ]
  }
}
```

## intent.sh (logica)

- Riceve il prompt dell'utente.
- Se contiene intento feature/bug (es. "aggiungi", "voglio una feature", "c'è un bug", "non funziona") e non c'è già un ciclo attivo → stampa: "LIMET: sembra una feature/bug. Avvia il flusso spec-driven (genera proposal/spec/plan)."
- Altrimenti: exit 0 (nessun output).

## guardrail.sh (logica)

- Se il comando Bash contiene `mvnw`, `./gradlew`, `npm test`, `pytest`, `cargo test`, ecc. → **blocca** (exit 2) con messaggio: "LIMET: build/test non in autonomia. Fornisci il comando all'utente."
- Se il comando contiene `git commit`, `git push`, `git rebase`, `migrate`, `deploy` → **blocca** senza autorizzazione esplicita.
- Altrimenti: exit 0 (nessun output, zero contesto).

## changelog.sh (logica)

- Riceve lo strumento + il file toccato.
- **Anti-rumore**: logga solo file **nello scope del task attivo**; **coalesce** modifiche multiple allo stesso file (una riga per file, non una per edit).
- Se `limet/TASK_LIST.md` esiste → appende/aggiorna la riga: `<timestamp> <file> — <tool>`.
- Se non c'è un task attivo → exit 0 (nessun output).

## reminder.sh (logica)

- Legge lo stato del task corrente.
- Se c'è un task senza sezione test o non archiviato → stampa un reminder: "LIMET: il task X non ha verifica/archivio. Usa /limet:test e /limet:archive."
- Se tutto a posto → nessun output.

## Fail-safe (tutti gli hook)

Ogni hook va in `try/catch`: **un hook che crasha NON deve mai bloccare Claude**. In caso di errore → exit 0 + eventuale log in un file di diagnosi. Un guardrail rotto che blocca il lavoro è peggio di nessun guardrail.

## Principio

> **Un'istruzione è una richiesta. Un hook è enforcement.**

Le regole §1.3 (no build/test autonomi) e §1.5 (test non-negoziabile) non sono più "scritte nel CLAUDE.md sperando che Claude le segua": sono **applicate** dagli hook.
