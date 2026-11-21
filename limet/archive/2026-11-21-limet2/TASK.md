# Scheda task singolo — Skill `/limet:new`

## 0. Sintesi

### Scopo (non tecnico)

Quando l'utente vuole una nuova feature, `/limet:new` fa nascere da solo tutti i documenti di piano
(proposta, specifica, piano, lista task, piano test, verifica e2e) invece di farli compilare a mano.
È il cuore del "spec-driven": l'umano approva, Claude genera.

### Modifiche (tecnico)

| Progetto | File (path) | Creato/Modificato | Cosa cambia e perché | Test collegato |
| -------- | ----------- | ----------------- | -------------------- | -------------- |
| limet2 | `skills/limet-new/SKILL.md` | creato | skill che genera i 7 doc dal contenuto di `$ARGUMENTS` | unit template + e2e `/limet:new` |

## Metadati

- **Riferimento**: task #3 di `TASK_LIST.md`
- **Stato**: `pending`
- **Data ultimo aggiornamento**: 2026-11-20

## 1. Descrizione del task

Creare `skills/limet-new/SKILL.md` con frontmatter (`name: limet-new`, `description`,
`user-invocable: true`, `allowed-tools`) e corpo che, dato `$ARGUMENTS`, genera in `limet/`:
1. `CHANGE_PROPOSAL.md` 2. `SPEC.md` 3. `PLAN.md` 4. `TASK_LIST.md` 5. `TEST_PLAN.md`
6. `E2E_VERIFICATION.md` 7. `DECISIONS.md` (solo se emergono decisioni hard-to-reverse).
Regole binding: mai assumere (domanda esplicita con data), ogni task con strategia di verifica,
mai build/test autonomi. I template 1.0 sono inclusi inline come riferimento (`docs/SKILLS.md`).

## 2. Contesto raccolto

- **docs/SKILLS.md** (documentazione): definisce le 5 skill, l'esempio SKILL.md di `/limet:new` con
  i 7 artefatti e le 4 regole condivise. **Fatto**.
- **limet/templates/** (codice): i 18 template 1.0 da cui si estraggono gli schemi inline.
  **Fatto**.
- **CLAUDE.md** (documentazione): regole binding (approvazione umana, traceability, test). **Fatto**.

## 3. Domanda contestuale (se presente)

- **Domanda**: `/limet:new` genera i documenti direttamente (inline) o li delega al subagent
  `limet-writer` (contesto isolato, task #13)?
- **Perché è rilevante**: cambia l'architettura della skill — inline = self-contained ma costa
  contesto; delegato = isolamento ma dipende dal task #13.
- **Risposta ricevuta**: — **Data**: — **Da**: —

> Assunzione motivata (se si procede senza risposta): usare `limet-writer` come indicato in
> `docs/SUBAGENTS.md` ("dentro `/limet:new`"), con la skill che orchestra e il writer che scrive.

## 4. Soluzione proposta/applicata

Skill `limet-new` che orchestra: rileva `$ARGUMENTS`, invoca il subagent `limet-writer` per
generare i documenti, poi mostra all'utente la proposta per l'approvazione (mai implementare prima
dell'ok). Template 1.0 inclusi inline come blocco di riferimento per lo schema di ogni artefatto.

- **skills/limet-new/SKILL.md** — frontmatter + flusso di generazione + regole binding.

### Alternative scartate

- Skill che genera tutto inline senza writer — scartata perché viola la separazione scrittura
  isolata di `docs/SUBAGENTS.md`.
- 18 skill separate (una per artefatto) — scartata perché `docs/SKILLS.md` consolida in 5.

## 5. Strategia di test (obbligatoria)

### 5.1 Unit test

- **Esistono già test che coprono quest'area?** no (repo vuoto, nessun codice 2.0).
- **Nuovi unit test previsti**: (a) frontmatter valido e campi obbligatori presenti; (b) lo SKILL.md
  elenca i 7 artefatti nell'ordine richiesto; (c) il testo contiene le 4 regole binding.
- **Dove sono descritti in dettaglio**: `TEST_PLAN.md`.
- **Autorevisione della qualità eseguita** (manuale §5.1): sì, a implementazione — criterio:
  *quale alterazione dello SKILL.md (es. rimuovere l'ordine degli artefatti) non farebbe fallire
  nessun test?* → aggiungere assert sull'ordine e sulla presenza di ogni regola.

### 5.2 Test e2e

- **Necessari?** sì — la skill è il flusso centrale, va provata in un ciclo reale.
- **Riferimento**: `E2E_VERIFICATION.md` (§ "ciclo /limet:new su progetto fittizio").

## 6. Rischi/impatti su altre parti del sistema

- `limet-writer` (task #13) dipende da questa skill → ordinare bene.
- Hooks `changelog` (task #10) intercettano gli Edit/Write generati → verificare che non logghino
  rumore durante la generazione bulk dei documenti.

## 7. Esito (da compilare a lavoro concluso)

- **Data**:
- **Stato finale**:
- **Esito test**:
- **Note per chi leggerà questo documento in futuro**:
