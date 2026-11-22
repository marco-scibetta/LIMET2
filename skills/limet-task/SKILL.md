---
name: limet-task
description: 'Esegue un task del TASK_LIST: brief, implementazione e change log.'
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit
---

# LIMET — esegui task ($ARGUMENTS)

`$ARGUMENTS` = id del task (es. `3` o `task3`).

## Flusso

1. Leggi il `TASK_LIST.md` attivo in `limet/changes/<data-slug>/` e individua il task richiesto.
2. **Brief obbligatorio** (prima di toccare qualsiasi file): 2-3 righe con *cosa farai*, *file che
   toccherai*, *verifica collegata*. Poi procedi **senza attendere conferma**.
3. Implementa il task, restando dentro il perimetro dichiarato.
4. Registra ogni file creato/modificato nella sezione **"Registro modifiche"** di `TASK_LIST.md`
   (una riga per file: task, percorso, tipo, cosa è cambiato, perché, verifica collegata).
5. **Non marcare `done`** finché la verifica non è eseguita: dai all'utente i comandi di test/verifica
   e resta in standby finché non arriva l'esito.

## Regole binding

- Ogni scelta ambigua → domanda esplicita all'utente con data. **Mai assumere in silenzio.**
- Non eseguire build/test: fornisci i comandi, l'utente li esegue e riporta l'esito.
- Non eseguire commit/push/migrate/deploy senza autorizzazione esplicita.
- Resta nel perimetro del task; ogni scostamento → segnala e chiedi approvazione.

## Formato del brief

```text
Brief #<id> — <titolo>
- Cosa: <una riga>
- File toccati: <elenco>
- Verifica: <comando o controllo>
```
