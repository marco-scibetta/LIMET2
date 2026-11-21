---
name: limet-test
description: Genera il piano di test e registra l'esito reale dei test.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit
---

# LIMET — test

Genera/aggiorna in `limet/changes/<data-slug>/`:

1. `TEST_PLAN.md` — unit + e2e, **prima** del codice, con autorevisione qualità (§5.1).
2. `TEST_EXECUTION.md` — **sempre generato**: se i test non sono ancora stati eseguiti, genera la
   struttura con i campi "da compilare a esecuzione avvenuta"; se sono stati eseguiti, incolla i
   log reali (non riassunti a memoria).

## Regole binding

- Non eseguire i test tu: fornisci i comandi, l'utente li esegue e riporta l'esito.
- Autorevisione qualità obbligatoria prima di dichiarare completo il piano.
- Ogni task prevede unit + e2e, anche con "n/a" giustificato.

---

## Template TEST_PLAN

```markdown
# Piano di test — [nome]

## Riferimenti
- Piano/proposta collegata: [...]
- Task collegato/i: [...]

## Ambito della verifica
[...]

## Unit test previsti
| # | Cosa verifica | File/classe di test | Caso (happy / edge / regressione) |
| - | -------------- | -------------------- | ---------------------------------- |

### Autorevisione della qualità (obbligatoria)
- Sabotaggio mentale: quale alterazione del codice NON farebbe fallire nessun test?
- [ ] Ogni assert può fallire per il motivo dichiarato
- [ ] Atteso non derivato dall'oggetto sotto test
- [ ] Contratto verificato (input assenti/vuoti/non validi), non solo happy path

## Test e2e previsti
| # | Scenario | Precondizioni | Passi principali | Esito atteso |
| - | -------- | -------------- | ------------------ | -------------- |

## Dati di test necessari
[...]

## Casi esclusi dal test (e perché)
- [...]

## Chi esegue
- Scrittura test: [...] / Esecuzione: [...]

## Comandi di test rieseguibili
- [comando esatto per rieseguire ogni test]
```

## Template TEST_EXECUTION

```markdown
# Esecuzione test — [nome]

## Riferimenti
- Piano collegato: [...]

## Metadati esecuzione
- Data/ora: [YYYY-MM-DD HH:MM] / Eseguito da: [...] / Ambiente: [...] / Comando eseguito: [...]

## Esito unit test
- Totale / Passati / Falliti / Saltati
- Log (incollare output reale del runner)

## Esito test e2e
| # | Scenario | Esito (OK / KO / non eseguito) | Note |
| - | -------- | ------------------------------ | ---- |

## Anomalie riscontrate
- [...]

## Conclusione
- Esito complessivo: `OK | KO | PARZIALE`
- Il task può passare a `done`? [sì/no + motivazione]
```
