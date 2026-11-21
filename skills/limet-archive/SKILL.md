---
name: limet-archive
description: Archivia il lavoro concluso e verificato.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# LIMET — archive

1. Verifica che il lavoro sia **concluso e verificato** (task `done`, test eseguiti e registrati).
   Se manca la verifica, non archiviare: segnalalo e chiedi l'esito.
2. Sposta `limet/changes/<data-slug>/` in `limet/archive/<data-slug>/`.
3. Genera la voce di archivio come riassunto finale (template sotto) — non riscrivere la storia:
   i documenti di dettaglio restano collegati per riferimento.
4. Ricorda all'utente il re-index (mai eseguito dall'agente).

## Regole binding

- Archivia solo lavoro verificato; senza verifica → fermati e segnala.
- Non eseguire commit/push senza autorizzazione esplicita.

---

## Template ARCHIVE_ENTRY

```markdown
# Voce di archivio — [nome modifica]

## Metadati
- Nome modifica: [...]
- Tipo: `feature | bug fix | refactor | altro`
- Data conclusione: [YYYY-MM-DD HH:MM]
- Autore/i: [...]

## Riepilogo
[3-5 righe, comprensibili a distanza di mesi senza contesto.]

## Documenti collegati (riferimento, non copia)
- Piano/proposta: [link]
- Elenco task: [link]
- Test plan/execution: [link]
- Sintesi non tecnica: [link, se presente]
- Bug report: [link, se applicabile]

## Decisioni chiave prese durante il lavoro
[domande contestuali più rilevanti + risposte, per non perdere il "perché".]

## Esito finale della verifica
- Unit test: [OK/KO, riferimento]
- Test e2e: [OK/KO, riferimento]
- Problemi noti residui: [...]

## Lezioni apprese (opzionale)
[...]

## Re-indicizzazione del contesto
- [ ] Ricorda all'utente: Launcher → Re-index → Incrementale → clic Re-index.
      Il re-index spetta all'utente, mai all'agente.
```
