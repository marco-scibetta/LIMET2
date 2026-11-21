# Disegno tecnico — LIMET 2.0 (piattaforma self-contained)

> Il *come* non è ovvio dalla sola spec: la scelta plugin/MCP/subagent e il riuso dei motori meritano
> di essere registrati prima di scrivere codice.

## Metadati

- **Proposta/specifica collegata**: `CHANGE_PROPOSAL.md` / `SPEC.md`
- **Stato**: `APPROVATO`

## Contesto tecnico (verificato, non assunto)

- LIMET 1.0 esiste come file di framework in `C:\Progetti\LIMET2\limet\` (template 18, manuale,
  checklist, script `limet-index.ps1/sh`, `limet_related.py`).
- CEREBRO è un repo separato `C:\Progetti\CEREBRO` con script Python (`ingest_docs.py`,
  `doc_to_markdown.py`, `query_qdrant.py`, `register_project.py`, `serve_images.py`) e `projects.json`.
- Il design 2.0 è interamente in `docs/` (ARCHITECTURE, SKILLS, HOOKS, SUBAGENTS, MCP, PLUGIN,
  OPTIMIZATIONS, MIGRATION). Non esiste ancora codice 2.0.
- Graphify: **terze parti** — `graphifyy` v0.9.32 (Graphify-Labs, Apache-2.0); sorgente in
  `C:\Users\admin\AppData\Roaming\uv\tools\graphifyy\Lib\site-packages\graphify`, con MCP nativo già
  incluso (`serve.py`, `mcp_ingest.py`).

## Decisione di disegno

**Struttura repo** (unico repo self-contained, da `docs/PLUGIN.md`):

```
limet/
├── .claude-plugin/plugin.json, marketplace.json
├── skills/limet-{new,task,test,archive,bug}/SKILL.md
├── agents/limet-writer.md, limet-gate.md
├── hooks/hooks.json, intent.sh, guardrail.sh, changelog.sh, reminder.sh
├── .mcp.json              (cerebro + graphify + db)
├── mcp/cerebro/  mcp/graphify/  mcp/db/
├── dashboard/             (React + Vite + TS, backend REST condiviso)
├── config/
│   ├── config.yaml              (default committati, no segreti)
│   ├── config.local.yaml        (gitignored: override + segreti)
│   ├── config.local.example.yaml
│   └── config.py / config.ts    (loader)
├── .gitignore             (include config.local.yaml)
├── CLAUDE.md              (policy minimale)
└── docs/                  (manuale + onboarding)
```

**Principio guida** (`docs/ARCHITECTURE.md`): skill = lavoro (Claude interpreta), hook = regole
(zero contesto), subagent = ruoli (contesto isolato), MCP = dati (tool esterni), CLAUDE.md = minimo.

**MCP — Cerebro (codice nostro): copia + wrap + rewrite mirato.** Gli script RAG di CEREBRO si
*copiano* dentro `mcp/cerebro/` e si avvolgono in un server MCP. Tre script restano intatti
(`query_qdrant.py`, `register_project.py`, `serve_images.py`); **due si riscrivono** per il fix di
velocità (`docs/OPTIMIZATIONS.md` §8/§9): `ingest_docs.py` (embedding batch `/api/embed`) e
`doc_to_markdown.py` (`pypdfium2` + parallel). CEREBRO ha già `limet_mcp.py`/`limet_rag.py` come
base MCP.

**MCP — Graphify (terze parti): dipendenza pinnata, non vendorizzato.** `graphifyy` (Graphify-Labs,
Apache-2.0) si dichiara come dipendenza `graphifyy==0.9.32` nel `pyproject.toml` — **non** si copia il
sorgente nel repo. Il pacchetto espone già un MCP nativo (`serve.py` + `mcp_ingest.py`): il task #16
riusa quello invece di scrivere un wrapper.

**MCP — db**: nuovo, generico (Postgres read-only; segreti in `config.local.yaml`).

**Configurazione = file, non env var** (richiesta esplicita). Tutte le variabili — path, host/porta,
modello embedding, limiti, lingua, segreti — stanno in file che LIMET legge da una posizione nota.
Niente hardcoded, niente variabili d'ambiente richieste all'utente.

- `config/config.yaml` → default sicuri, committati (no segreti).
- `config/config.local.yaml` → override + segreti, **gitignored**; `config.local.example.yaml` committato.
- **Lookup** (ordine): 1) `${CLAUDE_PLUGIN_ROOT}/config/config.local.yaml` se esiste, 2)
  `${CLAUDE_PLUGIN_ROOT}/config/config.yaml`. Merge: default ← local (local vince).
- **Loader unico**: `config.py` (Python) per i server MCP e gli hook; `config.ts` per la dashboard —
  una sola fonte di verità, nessuna duplicazione.
- Sezioni: `paths`, `qdrant`, `ollama`, `db`, `cerebro`, `graphify`, `limits`, `lang`.
- Nota: `${CLAUDE_PLUGIN_ROOT}` è fornito dalla piattaforma Claude Code, non è un env var impostato
  dall'utente → non viola il vincolo "niente env var". Sostituisce `.env_db` di `docs/MCP.md`.

**Dashboard = un backend, due frontend** (`docs/DASHBOARD.md`): il backend REST riusa la *stessa
logica* dei server MCP; Claude parla via MCP, la dashboard via REST. Niente duplicazione logica.

**Hook deterministici con fail-safe** (`docs/HOOKS.md`): ogni hook in try/catch; su errore exit 0 +
log di diagnosi. `guardrail` blocca build/test/commit senza autorizzazione; `changelog` logga solo
file nello scope del task attivo e coalesce più edit allo stesso file.

## Alternative considerate

### Alternativa A: MCP come riscrittura dei motori

- **Descrizione**: riscrivere cerebro/graphify come server MCP nativi da zero.
- **Pro**: codice più pulito, niente codice legacy.
- **Contro**: rischio regressione, costo alto, viola il principio "zero riscrittura".
- **Motivo di scarto**: il valore è nel *riposizionamento*, non nel rewrite (`docs/MCP.md`).

### Alternativa B: dashboard vanilla (portare launcher.html così com'è)

- **Descrizione**: mantenere la SPA vanilla 1.0.
- **Pro**: meno lavoro.
- **Contro**: look "anni '90", requisito grafico esplicito violato (`docs/DASHBOARD.md`).
- **Motivo di scarto**: la qualità visiva è un requisito, non un optional; React + design system.

### Alternativa C: batch `/api/embed` vs `fastembed`/ONNX in-process (embedding)

- **Descrizione**: due strade per eliminare l'embedding 1-alla-volta.
- **Pro**: batch = niente nuova dipendenza; fastembed = niente server Ollama.
- **Contro**: batch dipende ancora da Ollama; fastembed aggiunge dipendenza ONNX.
- **Motivo di scarto**: **nessuna scartata** — batch è il primo passo (minimo cambiamento), fastembed
  è l'ottimizzazione successiva opzionale. Decisione finale al task #15.

### Alternativa D: Docker obbligatorio vs nativo

- **Descrizione**: Qdrant/Ollama via docker-compose vs binari/installer nativi.
- **Pro**: Docker = riproducibile.
- **Contro**: dipendenza Docker obbligatoria.
- **Motivo di scarto**: nativo di default, Docker solo come opzione (`docs/ARCHITECTURE.md`).

## Compromessi (trade-off) accettati

- **Self-contained vs peso repo**: si guadagna un solo install a fronte di un repo più grande
  (motori dentro). Accettato.
- **Claude-only vs tool-agnostic**: si perde Copilot/compatibilità, si elimina il doppio albero IT/EN.
- **Nativo vs Docker**: si perde riproducibilità by-default, si evita la dipendenza Docker.
- **5 skill vs 18 template**: si perde granularità per-artefatto, si guadagna generazione congiunta.

## Domande contestuali aperte

| # | Domanda | Risposta | Data | Da chi |
| - | ------- | -------- | ---- | ------ |
| 1 | Sorgente Graphify: dove si trova (per `mcp/graphify/`)? | `C:\Users\admin\AppData\Roaming\uv\tools\graphifyy\Lib\site-packages\graphify` (v0.9.32; contiene già `serve.py` + `mcp_ingest.py`) | 2026-11-20 | utente |
| 2 | Embedding: batch `/api/embed` oppure `fastembed`/ONNX come scelta v1? | *aperta — si decide al task #15* (batch = passo 1, fastembed = step successivo opzionale) | | |
| 3 | Dashboard: quale design system (skill `ui-ux-pro-max` indicata in `docs/DASHBOARD.md`)? | *aperta — si decide al task #18* | | |

## Impatto su test e verifica

- Hook bash: testabili con harness in-process (spy su stdin/stdout, exit code), senza lanciare Claude.
- MCP server: testabili con pytest (tool = funzioni pure sul layer logico; mock su Qdrant/Ollama/DB).
- Dashboard: component test per "no password in chiaro"; e2e browser per le pagine.
- Loader config: unit su merge default↔local, default mancante, file assente (fallback senza errore).
- Punti di iniezione per testabilità: separare la logica (embedding/parsing/query) dal trasporto
  (MCP/hook/REST) così la logica è unit-testabile senza infra.
