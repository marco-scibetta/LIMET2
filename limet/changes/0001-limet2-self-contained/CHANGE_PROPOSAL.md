# Proposta di modifica — LIMET 2.0 (piattaforma self-contained, Claude Code native)

> Modifica ampia: nuova piattaforma, più moduli, cambio di interfaccia. Il *cosa* verificabile è in
> `SPEC.md`; il *come* in `DESIGN.md`. Sorgente di verità del "perché": `docs/` (design LIMET 2.0).

## Metadati

- **Data creazione**: 2026-11-20
- **Stato**: `APPROVATA`
- **Approvata da / data**: utente — 2026-11-20
- **Specifiche collegate**: `SPEC.md`
- **Disegno collegato**: `DESIGN.md`

## Perché

LIMET 1.0 ha la filosofia giusta (spec-driven, traceability, test non-negoziabile) ma l'esecuzione
pesante: **18 template da riempire a mano**, CEREBRO come skill-guida che orchestra script Python,
GRAPHIFY come CLI esterno, doppio albero IT/EN tool-agnostic. Il cambio si fa **ora** perché:

1. Le feature native di Claude Code (skill, hook, subagent, plugin, MCP, `/goal`) coprono ogni
   componente di LIMET 1.0 senza più attrito manuale.
2. L'audit di CEREBRO ha trovato i due colli di bottiglia reali dell'ingestion (embedding
   1-alla-volta e parsing pdfplumber seriale) — risolvibili in 2.0.
3. Dogfooding: LIMET 2.0 si costruisce **usando LIMET stesso** (`docs/README.md` §"Come nasce").
   Questi stessi `docs/` sono i primi artefatti SPEC/DESIGN.

Se non si fa: LIMET resta tool-agnostic e doc-heavy → la tracciabilità (§1.4) viene saltata dagli
utenti, e i 3 pezzi (LIMET + CEREBRO + GRAPHIFY) restano tre installazioni separate.

## Cosa cambia (riepilogo)

- **Plugin unico self-contained** `limet/`: `.claude-plugin/` + `skills/` + `agents/` + `hooks/` +
  `.mcp.json` + `mcp/` (cerebro, graphify, db dentro il repo, non esterni).
- **18 template manuali → 5 skill**: `/limet:new`, `/limet:task`, `/limet:test`, `/limet:archive`,
  `/limet:bug`. Claude genera i documenti, l'umano approva.
- **Regole da testo → enforcement**: 4 hook (`intent`, `guardrail`, `changelog`, `reminder`)
  applicano §1.3/§1.5 in modo deterministico, con fail-safe che non blocca mai Claude.
- **2 subagent**: `limet-writer` (scrive i doc) e `limet-gate` (valida §1.5 + fresh-eyes + drift).
- **3 server MCP** (thin wrapper, zero riscrittura dei motori): `cerebro`, `graphify`, `db`.
- **Dashboard React** per le ops (init/re-index/status/config-db/artefatti), backend condiviso con MCP.
- **Ingestion 10-50× più veloce**: batch `/api/embed` o `fastembed`/ONNX; parsing `pypdfium2` + parallel.
- **Mappatura 1.0→2.0** completa in `docs/ARCHITECTURE.md`.
- **Configurazione da file**: `config/config.yaml` + `config.local.yaml` (segreti) — niente path hardcoded, niente env var.

## Capability

### Nuove capability
- `plugin-limet`: packaging + manifest + distribuzione marketplace.
- `skill-lifecycle`: le 5 skill del ciclo (new/task/test/archive/bug).
- `hook-enforcement`: intent/guardrail/changelog/reminder deterministici.
- `agents-writer-gate`: scrittura isolata + validazione/quality-gate.
- `mcp-cerebro`: RAG documentale (search/count/list/ingest/register).
- `mcp-graphify`: knowledge graph (query/path/explain/update).
- `mcp-db`: query read-only su DB relazionale, segreti fuori dal contesto.
- `dashboard-ops`: GUI React per operazioni (non lavoro).
- `config-file`: configurazione centralizzata da file (path/host/limiti/segreti), zero hardcoded, zero env var.

### Capability modificate
- `cerebro-ingestion`: da embedding 1-chunk-1-HTTP a batch/in-process; parsing pdfplumber→pypdfium2.
- `limet-cli` (scripts `limet.ps1`/`limet.sh`): sostituiti dal plugin (l'install resta).

### Capability rimosse/deprecate
- `cerebro-skill-guida` e `graphify-cli` esterni: deprecati in favore degli MCP bundlati.
  Migrazione: script **spostati dentro** `mcp/`, non riscritti (`docs/MCP.md`, `docs/MIGRATION.md`).
- Doppio albero IT/EN e astrazione tool-agnostic: rimossi (Claude-only).

## Impatto

- **Codice/moduli interessati**: nuovo repo `limet/` (plugin, skills, agents, hooks, mcp/*, dashboard).
  `<repo-cerebro>` resta sorgente da copiare per `mcp/cerebro/`; Graphify = dipendenza `graphifyy==0.9.32`.
- **API/contratti interessati**: contratti dei tool MCP (nuovi); compatibilità all'indietro sui
  **documenti** LIMET 1.0 garantita al 100% (`docs/MIGRATION.md`: stesso formato, cambia chi genera).
- **Dipendenze esterne**: Qdrant + Ollama (infra runtime, nativi di default, Docker opzionale).
- **Dati esistenti**: `projects.json` di CEREBRO non cambia formato; nessuna migrazione dati.

## Domande contestuali aperte

| # | Domanda | Risposta | Data | Da chi |
| - | ------- | -------- | ---- | ------ |
| 1 | Sorgente Graphify non localizzato: da dove si copia `mcp/graphify/`? | `C:\Users\admin\AppData\Roaming\uv\tools\graphifyy\Lib\site-packages\graphify` (pacchetto Python v0.9.32) | 2026-11-20 | utente |
| 2 | Dashboard: dentro questa proposta (fase 5) o separata? | Dentro (task #18–19) | 2026-11-20 | utente |
| 3 | Marketplace: org/homepage placeholder `<org>` — valore reale? | Solo dev locale (placeholder `<org>` resta) | 2026-11-20 | utente |
| 4 | Lingua: solo italiano nella v1 o bilingue? | Bilingue IT+EN subito (deroga a `docs/OPTIMIZATIONS.md` §2) | 2026-11-20 | utente |
| 5 | Infra target: nativo o Docker? | Nativo di default, Docker solo opzionale | 2026-11-20 | utente |

## Strategia di verifica (obbligatoria, vedi `FRAMEWORK_MANUAL.md` §5)

- **Unit test**: per hook (script bash) harness di test con casi negativi/positivi; per MCP pytest;
  per dashboard component test. Dettaglio per task in `TASK_LIST.md`; piano in `TEST_PLAN.md`.
- **Test e2e**: `claude plugin validate --strict ./limet`, ciclo completo `/limet:new → task → test
  → archive` su un progetto fittizio, connessione reale Qdrant/Ollama/DB. Riferimento
  `E2E_VERIFICATION.md`.

## Esito (da compilare a chiusura, prima dell'archiviazione)

- **Data**:
- **Sintesi**:
- **Scostamenti rispetto alla proposta originale**:
