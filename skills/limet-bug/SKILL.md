---
name: limet-bug
description: Crea un bug report strutturato.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit
---

# LIMET — bug ($ARGUMENTS)

Scrivi `BUG_REPORT.md` dal contenuto di `$ARGUMENTS`, seguendo il template sotto.

**Dove**: se esiste una cartella attiva `limet/changes/<data-slug>/`, scrivi `BUG_REPORT.md` lì dentro.
Altrimenti crea `limet/changes/<data-slug>/` con `<data-slug>` = `YYYY-MM-DD-slug` derivato da
`$ARGUMENTS` (es. `2026-11-20-pulsante-salva-non-funziona`).

## Regole binding

- Distingui **comportamento osservato** (fatti, evidenze) da **ipotesi**.
- La causa radice va scritta solo dopo l'investigazione, con riferimento puntuale a codice/log.
- Strategia di verifica obbligatoria: test di regressione che **fallisce col bug presente** e passa dopo il fix.

---

## Template BUG_REPORT

```markdown
# Bug report — [titolo breve del difetto]

## Metadati
- Data segnalazione: [YYYY-MM-DD]
- Segnalato da: [...]
- Stato: `APERTO | IN ANALISI | IN FIX | RISOLTO | NON RIPRODUCIBILE | NON UN BUG`
- Severità: `bloccante | alta | media | bassa`

## Comportamento osservato
[fatti + evidenze: log, messaggi di errore, screenshot, passi che lo hanno prodotto.]

## Comportamento atteso
[cosa dovrebbe succedere secondo la specifica.]

## Passi per riprodurre
1. [passo 1]
2. [passo 2]

## Ambiente
- Versione/branch/commit: [...]
- Ambiente: [locale/test/produzione]
- Dati di test necessari: [...]

## Analisi della causa radice
- Causa identificata: [...]
- File/componente coinvolto: [percorso, righe]
- Perché accade: [...]

## Impatto
- Chi/cosa è affetto: [...]
- Da quando: [versione/commit, se noto]
- Workaround: [sì/no + descrizione]

## Fix proposto
[modifica minimale sulla causa radice, non solo sul sintomo.]

## Strategia di verifica (obbligatoria)
- Unit test di regressione: [deve fallire col bug e passare dopo il fix]
- Test e2e: [se necessario]

## Task di verifica collegati
- [...]

## Esito (a chiusura)
- Data risoluzione / Commit/PR / Note
```
