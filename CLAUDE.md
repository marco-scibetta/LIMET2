# LIMET 2.0

Spec-driven engineering for Claude Code. Lifecycle: `limet-new` → `limet-task` → `limet-test` → `limet-archive`; `limet-bug` for bugs. (Skills, non slash command: `/limet-dashboard` è l'unico comando slash.)

## Binding rules

- Spec first: proposal/plan before non-trivial code changes.
- Ambiguity → explicit question with date; never assume.
- No task marked `done` without a verification strategy (unit + e2e + lint/type when configured), or explicit justification.
- Human approval recorded before implementation.
- Never run build/test autonomously — give the command, the user runs it.
- No commit/push/migrate/deploy without explicit authorization.

## Context tools (MCP)

`cerebro` (docs RAG) · `graphify` (code KG) · `db` (read-only SQL).

<!-- LIMET-CONTEXT:START -->
## Project context tools (CEREBRO RAG + Graphify) · Strumenti di contesto del progetto

**EN** — This project's documentation is indexed in Qdrant collection `CRB_limet2`.
Its code is indexed in the Graphify knowledge graph.

Query the documentation (semantic RAG):
  python "C:\Progetti\CEREBRO\scripts\query_qdrant.py" --project limet2 search "<query>" --limit 5

Query the code (knowledge graph):
  graphify query "<question>"   /   graphify explain <symbol>   /   graphify path <A> <B>

Rules:
- **RAG**: BEFORE answering any question about the project, call the `limet_search` MCP tool and ground your answer in its results. If the tool is unavailable, fall back to the `query_qdrant.py` command below.
- Search CEREBRO/Qdrant FIRST. If the document is not indexed (0 results or missing), read it
  LOCALLY from `docs-limet/` or `limet/`.
- Re-indexing and Graphify updates belong to the user, never the agent. Use local docs until indexed.
- **Code questions** (where is X implemented, who uses Y, how does flow Z work): FIRST use
  `graphify query` / `graphify explain` / `graphify path`; THEN confirm exact lines and usages
  with a targeted text search (grep). Do not start directly from grep.
- After code/document changes, periodically remind the user (at task completion or archiving):
  Launcher -> project path -> Re-index -> Incrementale -> click Re-index.
- If Qdrant, Ollama or Graphify are unreachable, say so and proceed with the local docs.

---

**IT** — La documentazione di questo progetto è indicizzata nella collection Qdrant `CRB_limet2`.
Il codice è indicizzato nel knowledge graph Graphify.

Interroga la documentazione (RAG semantico):
  python "C:\Progetti\CEREBRO\scripts\query_qdrant.py" --project limet2 search "<query>" --limit 5

Interroga il codice (knowledge graph):
  graphify query "<domanda>"   /   graphify explain <simbolo>   /   graphify path <A> <B>

Regole:
- **RAG**: PRIMA di rispondere a qualsiasi domanda sul progetto, chiama lo strumento MCP `limet_search` e fonda la risposta sui suoi risultati. Se lo strumento non è disponibile, usa il comando `query_qdrant.py` qui sotto.
- Cerca PRIMA in CEREBRO/Qdrant. Se il documento non è indicizzato (0 risultati o assente), leggilo
  LOCALMENTE da `docs-limet/` o `limet/`.
- Il re-index e gli aggiornamenti Graphify spettano all'utente, mai all'agente. Usa i doc locali
  finché non sono indicizzati.
- **Domande sul codice** (dov'è implementato X, chi usa Y, come funziona il flusso Z): PRIMA usa
  `graphify query` / `graphify explain` / `graphify path`; POI conferma righe e usi esatti con
  una ricerca testuale mirata (grep). Non partire direttamente da grep.
- Dopo modifiche a codice/documenti, ricordare periodicamente all'utente (al termine di un task
  o dell'archiviazione): Launcher -> Percorso progetto -> Re-index -> Incrementale -> clic Re-index.
- Se Qdrant, Ollama o Graphify non sono raggiungibili, segnalalo e procedi con i doc locali.
<!-- LIMET-CONTEXT:END -->

<!-- PROJECT:START -->
## Project overview · Panoramica del progetto

**EN** — Project `limet2` — CEREBRO collection `CRB_limet2`.

Complete local Markdown inventory under docs-limet/ (excluding _templates; not proof of indexing):
  - `docs-limet\architecture\GRAPH_REPORT.md`

For indexed sources, consult CEREBRO's projects.json and query the collection above.

Code graph (Graphify): `graphify-out/` (report: `graphify-out/GRAPH_REPORT.md`).

---

**IT** — Progetto `limet2` — collection CEREBRO `CRB_limet2`.

Inventario locale completo dei Markdown in docs-limet/ (esclusi _templates; non attesta l'indicizzazione):
  - `docs-limet\architecture\GRAPH_REPORT.md`

Per le fonti indicizzate, consulta projects.json di CEREBRO e interroga la collection indicata sopra.

Grafo del codice (Graphify): `graphify-out/` (report: `graphify-out/GRAPH_REPORT.md`).

## Documentation to maintain · Documentazione da mantenere

**EN** — Follow limet/templates/CODEBASE_ANALYSIS_TEMPLATE.md to maintain docs-limet/module-map.md, architecture.md, decisions.md, dependencies.md, conventions.md and glossary.md with file:line citations and Mermaid diagrams. UPDATE existing documents. Maintain docs-limet/NON_TECHNICAL_SUMMARY.md after relevant changes. Re-indexing belongs to the user, never the agent. After code/document changes, periodically remind the user (at task completion or archiving): Launcher -> project path -> Re-index -> Incrementale -> click Re-index.

**IT** — Segui limet/templates/CODEBASE_ANALYSIS_TEMPLATE.md per mantenere docs-limet/module-map.md, architecture.md, decisions.md, dependencies.md, conventions.md e glossary.md con citazioni file:line e diagrammi Mermaid. AGGIORNA i documenti esistenti. Mantieni docs-limet/NON_TECHNICAL_SUMMARY.md dopo modifiche rilevanti. Il re-index spetta all'utente, mai all'agente. Dopo modifiche a codice/documenti, ricordarlo periodicamente (al termine di un task o dell'archiviazione): Launcher -> Percorso progetto -> Re-index -> Incrementale -> clic Re-index.
<!-- PROJECT:END -->
