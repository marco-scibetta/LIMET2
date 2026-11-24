# LIMET 2.0 — Skills

Le skill sono il **ciclo di vita** di LIMET. **NON vanno lanciate a mano**: si attivano **automaticamente** dal CLAUDE.md (policy always-on) e dall'hook `UserPromptSubmit` (rilevamento intento). L'utente **parla normalmente** ("voglio aggiungere una feature X" / "c'è un bug Y") e Claude avvia il flusso da solo — **come LIMET 1.0, nessun comando da digitare**.

I comandi `/limet-*` esistono solo come **scorciatoie opzionali** per il controllo esplicito, non sono il modo primario di interazione.

Frontmatter standard (AgentSkills.io): `name`, `description`, `allowed-tools`, `user-invocable`. Progressive disclosure: metadata → SKILL.md body → file reference.

## Le 6 skill

| Skill | Cosa fa | Input | Output |
|---|---|---|---|
| `/limet-new` | ciclo completo: proposta + spec + plan + task + test + e2e | `$ARGUMENTS` = idea/feature | `limet/` con tutti i doc |
| `/limet-task` | esegue un task + change log | `$1` = id task (es. `task3`) | codice + change log |
| `/limet-test` | genera/esegue il piano test | — | TEST_PLAN + TEST_EXECUTION |
| `/limet-archive` | archivia il lavoro concluso | — | `limet/archive/<data-slug>/` |
| `/limet-bug` | report bug strutturato | `$ARGUMENTS` = descrizione | BUG_REPORT.md |
| `/limet-analyze` | analizza un progetto non documentato → doc onboarding in `docs/` | — | `docs/` (7 doc) |

I template di supporto (glossary, conventions, codebase-analysis, architecture, module-map, summary, **decisions**) si generano **ad hoc** dentro `/limet-new`, non come skill separate.

**`decisions.md` = ADR-lite** (idea da ECC): le decisioni **hard-to-reverse** ("perché usiamo l'universo point-in-time?") meritano un record dedicato datato con stato (*accepted / superseded*), separato da spec/plan. Non il lifecycle ADR completo — solo un log leggero.

## Esempio SKILL.md — `/limet-new`

```markdown
---
name: limet-new
description: Avvia un ciclo LIMET per una nuova feature. Genera Change Proposal, SPEC, PLAN, TASK_LIST, TEST_PLAN e E2E_VERIFICATION. Usa quando l'utente chiede una nuova feature o dice "/limet-new <idea>".
user-invocable: true
allowed-tools: Read, Grep, Glob, Write
---

# LIMET — nuovo ciclo ($ARGUMENTS)

Genera in `limet/` i seguenti documenti, in ordine, dal contenuto di $ARGUMENTS:

1. `CHANGE_PROPOSAL.md` — cosa, perché, impatto (template inline sotto).
2. `SPEC.md` — cosa deve fare (behaviour, non implementazione).
3. `PLAN.md` — come, a design level.
4. `TASK_LIST.md` — task granulari, con sezione "Change log" vuota.
5. `TEST_PLAN.md` — unit + e2e + lint/type (se configurati), con comando di riesecuzione.
6. `E2E_VERIFICATION.md` — passi end-to-end.
7. `DECISIONS.md` — decisioni hard-to-reverse (ADR-lite), solo se emergono.

Regole (binding):
- Ogni scelta ambigua → domanda esplicita all'utente (mai assumere).
- Ogni task deve avere una strategia di verifica (unit + e2e + lint/type se configurati), anche "n/a" giustificato.
- Non eseguire build/test: fornisci i comandi, l'utente li esegue.

## Template CHANGE_PROPOSAL
(contenuto del template 1.0, inline)
## Template SPEC
(...)
```

## Regole condivise da tutte le skill

1. **Mai assumere**: scelte ambigue → domanda esplicita con data.
2. **Mai build/test autonomi**: fornisci il comando, l'utente esegue e riporta l'esito.
3. **Traceability**: ogni file creato/modificato finisce nel change log (via hook PostToolUse).
4. **Lingua**: rispondi nella lingua dell'utente.
5. **Brief prima di ogni task**: prima di implementare, dai un brief di 2-3 righe (cosa farai, file toccati, verifica collegata), poi procedi senza attendere conferma.

## Perché 6 e non 18

I 18 template 1.0 erano "documenti da riempire a mano". In 2.0, il **flusso** li genera insieme (`/limet-new`), il **change log** è automatico (hook), l'**archivio** è una skill, il **bug** è una skill. Il resto è supporto generato a richiesta. Meno attrito, stessa tracciabilità.
