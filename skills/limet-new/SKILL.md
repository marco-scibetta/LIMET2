---
name: limet-new
description: Avvia un ciclo LIMET per una feature o modifica: genera proposta, spec, piano, task, test ed e2e.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write
---

# LIMET — nuovo ciclo ($ARGUMENTS)

Genera in `limet/changes/<data-slug>/` i documenti seguenti, **in ordine**, partendo dal contenuto di `$ARGUMENTS`.
`<data-slug>` = `YYYY-MM-DD-slug` derivato da `$ARGUMENTS` (es. `2026-11-20-login-page`).
Scrivi nella lingua dell'utente. Ogni documento è istanziato dal template inline sotto, e non deve
restare vuoto.

## Documenti da generare

1. `CHANGE_PROPOSAL.md` — il *perché*: problema, cosa cambia, impatto.
2. `SPEC.md` — il *cosa* verificabile: requisiti + scenari dato/quando/allora.
3. `PLAN.md` — il *come* a livello di disegno: approccio, alternative, rischi.
4. `TASK_LIST.md` — task granulari con stato, dipendenze, strategia di test, registro modifiche vuoto.
5. `TEST_PLAN.md` — unit + e2e, con comandi di riesecuzione.
6. `E2E_VERIFICATION.md` — checklist passo-passo per la verifica manuale.
7. `DECISIONS.md` — solo se emergono decisioni hard-to-reverse (ADR-lite).

## Regole binding

- Ogni scelta ambigua → domanda esplicita all'utente con data. **Mai assumere in silenzio.**
- Ogni task deve avere una strategia di verifica (unit + e2e), anche con "n/a" giustificato.
- Non eseguire build/test: fornisci i comandi, l'utente li esegue e riporta l'esito.
- Prima di implementare un task, dai un **brief di 2-3 righe** (cosa, file toccati, verifica) e procedi senza attendere conferma.
- Non eseguire commit/push/migrate/deploy senza autorizzazione esplicita.

---

## Template CHANGE_PROPOSAL

```markdown
# Proposta di modifica — [nome capability/change]

## Metadati
- Data creazione: [YYYY-MM-DD]
- Stato: `DRAFT | APPROVATA | IN CORSO | COMPLETATA | ABBANDONATA`
- Approvata da / data: [chi — YYYY-MM-DD]
- Specifiche collegate: [file SPEC]
- Disegno collegato: [file PLAN/DESIGN]

## Perché
[Problema/opportunità; perché ora; cosa succede se non si fa.]

## Cosa cambia (riepilogo)
- [cambiamento 1]
- [cambiamento 2]

## Capability
### Nuove capability
- `nome`: [descrizione]
### Capability modificate
- `nome`: [cosa cambia e perché]
### Capability rimosse/deprecate
- `nome`: [motivo + piano di migrazione]

## Impatto
- Codice/moduli interessati: [...]
- API/contratti interessati: [...] (compatibilità all'indietro)
- Dipendenze esterne: [...]
- Dati esistenti: [migrazione? retrocompatibile?]

## Domande contestuali aperte
| # | Domanda | Risposta | Data | Da chi |
| - | ------- | -------- | ---- | ------ |

## Strategia di verifica
- Unit test: [rif. TEST_PLAN.md]
- Test e2e: [rif. E2E_VERIFICATION.md]

## Esito (a chiusura, prima dell'archiviazione)
- Data: [...]
- Sintesi: [...]
- Scostamenti rispetto alla proposta originale: [...]
```

## Template SPEC

```markdown
# Specifica — Capability: [nome]

## Metadati
- Proposta collegata: [file CHANGE_PROPOSAL]
- Stato: `DRAFT | APPROVATA | IMPLEMENTATA`
- Versione: [N]

## Descrizione della capability
[Comportamento osservabile, non implementazione.]

## Requisiti
### Requisito N: [titolo breve]
[Descrizione.]

**Scenari** (dato/quando/allora):
- **Dato** [precondizione], **quando** [azione], **allora** [risultato atteso].
- **Dato** [edge case], **quando** [...], **allora** [...].

## Vincoli e casi limite
- [vincolo / caso limite]

## Fuori specifica (esplicitamente non coperto)
- [comportamento non garantito]

## Tracciabilità verso i test
| Requisito | Unit test | Test e2e |
| --- | --- | --- |
| Requisito 1 | [rif.] | [rif.] |
```

## Template PLAN

```markdown
# Piano — [nome feature / bug fix]

## Metadati
- Data creazione: [YYYY-MM-DD]
- Stato: `DRAFT | APPROVATO | IN CORSO | COMPLETATO | ABBANDONATO`
- Approvato da / data: [chi — YYYY-MM-DD]

## 1. Obiettivo
[2-4 frasi: cosa e perché, non ancora come.]

## 2. Perimetro (scope)
### Dentro perimetro
- [...]
### Fuori perimetro
- [...] (motivo)

## 3. Stato attuale
[Verificato per fatti, non per assunzione.]
- [componente]: [cosa fa oggi]

## 4. Domande contestuali aperte
| # | Domanda | Risposta | Data | Da chi |

## 5. Approccio proposto
[Disegno: componenti toccati, logica introdotta/modificata.]

### Alternative considerate e scartate
- **Alternativa A**: [descrizione] — scartata perché [motivo].

## 6. Elenco attività
[Il dettaglio granulare va in TASK_LIST.md — genera sempre TASK_LIST.md.]

## 7. Strategia di verifica (obbligatoria)
- Unit test: [sì/no + rif. TEST_PLAN.md]
- Test e2e: [sì/no + rif. E2E_VERIFICATION.md]

## 8. Rischi e impatti
- [rischio] — mitigazione: [...]
- Compatibilità all'indietro: [...]

## 9. Note operative
- Commit/push: [chi li esegue]
```

## Template TASK_LIST

```markdown
# Elenco task — [nome]

## Legenda stato
- `pending` / `in_progress` / `blocked` / `done` (completato **e verificato**; annotare `YYYY-MM-DD HH:MM`)

## Tabella task
| # | Titolo | Scopo (non tecnico) | Stato | Dipende da | Dettaglio | Note |
| - | ------ | ------------------- | ----- | ---------- | --------- | ---- |

## Strategia di test — obbligatoria per ogni task
| # task | Unit test previsti | Test e2e previsti | Se omesso, motivazione |
| ------ | ------------------ | ----------------- | ---------------------- |

## Registro modifiche — una riga per file toccato
| Task | File | Tipo | Cosa è cambiato | Perché | Verifica collegata |
| ---- | ---- | ---- | --------------- | ------ | ------------------ |

## Esito implementazione (a lavoro concluso)
- Data / Sintesi esito / Scostamenti / Esito test
```

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

## Template E2E_VERIFICATION

```markdown
# Verifica e2e manuale — [nome]

## Riferimenti
- Piano/task collegato: [...]
- Ambiente di verifica: [locale/test/staging/produzione]

## Precondizioni
- [...]

## Stato pre-verifica (controllo PRIMA dei passi)
- Controllo: [...] (es. SELECT/SQL, file, config)

## Passi di verifica
1. [Passo 1 — azione precisa]
   - **Esito atteso**: [...]
2. [...]

## Stato post-verifica (controllo DOPO i passi)
- Controllo: [...]

## Casi limite da verificare
- [...]

## Esito esecuzione (da compilare da chi esegue)
- Data/ora / Eseguito da / Esito (`OK | KO`) / Note
```

## Template DECISIONS (ADR-lite — solo se emergono decisioni hard-to-reverse)

```markdown
# Decisioni (ADR-lite)

| # | Decisione | Stato | Data | Contesto | Conseguenze |
| - | --------- | ----- | ---- | -------- | ----------- |
| 1 | [...]     | `accepted` | [YYYY-MM-DD] | [perché] | [...] |
```

> Stato: `accepted` o `superseded` (con riferimento alla decisione che la sostituisce).
> Registra solo decisioni hard-to-reverse; non il lifecycle ADR completo.
