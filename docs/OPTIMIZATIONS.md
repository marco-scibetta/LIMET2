# LIMET 2.0 — Ottimizzazioni (filosofia mantenuta)

LIMET 1.0 era corretto nella **filosofia** (spec-driven, traceability, test non-negoziabile) ma **pesante nell'esecuzione**. LIMET 2.0 mantiene la filosofia e ottimizza l'esecuzione. Non gonfiare: ogni ottimizzazione elimina attrito, non aggiunge complessità.

## 1. Doc-heavy → skill-automated

- **1.0**: 18 template .md che l'umano riempie a mano. Attrito = si salta la tracciabilità.
- **2.0**: 5 skill. Claude genera i documenti, l'umano approva. Il documento resta la fonte di verità (§1.1) ma non è più un modulo da compilare.

## 2. Tool-agnostic → Claude-only

- **1.0**: due edizioni (IT/EN) + compatibilità Copilot/Claude = overhead di manutenzione.
- **2.0**: solo Claude Code. Via il doppio albero documentale e l'astrazione "tool-agnostic". (L'EN si può aggiungere dopo, se serve.)

## 3. Python/CLI → MCP thin wrapper

- **1.0**: CEREBRO = skill-guida che orchestra script Python; GRAPHIFY = CLI.
- **2.0**: stessi motori, avvolti in MCP. Claude chiama `cerebro_search(...)` invece di lanciare `python query_qdrant.py`. **Nessuna riscrittura della logica.**

## 4. Template manuali → hook-driven

- **1.0**: il change log (§1.4) e l'archivio si compilavano a mano.
- **2.0**: `PostToolUse` appende al change log automaticamente; `Stop` ricorda l'archivio. Il lavoro noioso sparisce.

## 5. Regole da testo → enforcement

- **1.0**: §1.3 (no build/test autonomi) e §1.5 (test non-negoziabile) erano *scritte* nel CLAUDE.md.
- **2.0**: `PreToolUse` *blocca* i build/test; `limet-gate` *rifiuta* i task senza verifica. "Un'istruzione è una richiesta; un hook è enforcement."

## 6. Consolidamento: 18 → 5 skill

- **1.0**: un template per ogni artefatto = 18 documenti separati.
- **2.0**: `/limet:new` genera tutto il ciclo insieme (proposal+spec+plan+task+test+e2e). I doc di supporto (glossary, conventions, analysis…) si generano a richiesta. Meno attrito, stessa tracciabilità.

## 7. Self-contained: un solo repo

- **1.0**: LIMET + CEREBRO + GRAPHIFY = tre cose separate da installare.
- **2.0**: tutto in un unico repo. Cerebro e Graphify sono dentro `mcp/`. Un solo `claude plugin install` + un `docker-compose` per Qdrant/Ollama. Meno dipendenze, distribuzione pulita.

## 8. Embedding a batch, non 1-alla-volta (fix lentezza ingestion)

- **1.0**: `ingest_docs.py` fa **un POST HTTP a Ollama per chunk** (`/api/embeddings`). Un PDF con 300 chunk = 300 round-trip → lentezza. **Non serve GPU**: `nomic-embed-text` è piccolo (~137M), gira su CPU.
- **2.0**: **batch `/api/embed`** (lista di chunk in una sola chiamata) oppure **`fastembed`/ONNX in-process** (niente server Ollama). 10-50× più veloce, su CPU. Eventuale parsing PDF parallelizzato con `pypdfium2`.

## 9. Parsing PDF/EPUB: pypdfium2 diretto + parallel (secondo collo di bottiglia)

- **1.0**: `doc_to_markdown.py` usa **pdfplumber** pagina per pagina (lento), e per ogni immagine renderizza a 150 DPI e salva PNG **in seriale**. È il secondo collo di bottiglia, dopo l'embedding 1-alla-volta.
- **2.0**:
  - **`pypdfium2` diretto** per il testo (già dipendenza presente, molto più veloce di pdfplumber).
  - **Parallelizzare le pagine** (`concurrent.futures`).
  - Rendering immagini a risoluzione ridotta / solo se serve (non 150 DPI fisso per tutte).

## Riepilogo per script (audit Cerebro completo)

| Script | Collo di bottiglia | Fix in 2.0 |
|---|---|---|
| `ingest_docs.py` | embedding 1 chunk = 1 POST HTTP | batch `/api/embed` o fastembed/ONNX |
| `doc_to_markdown.py` | pdfplumber lento + rendering immagini seriale | pypdfium2 diretto + parallel |
| `query_qdrant.py` | ok (query singola + search Qdrant) | — |
| `register_project.py` | ok (JSON leggero) | — |
| `serve_images.py` | ok (server statico) | — |

## Cosa NON cambia (la filosofia)

- Spec-driven, non vibe-driven (§1.1).
- Traceability delle decisioni (§1.2).
- Separazione scrittura/esecuzione (§1.3).
- Test non-negoziabile (§1.5).
- Leggero: 5 skill, 4 hook, 2 subagent, 3 MCP. Stop.
- **Conversazionale** (come 1.0): l'utente parla, non digita comandi — l'hook `intent` rileva e avvia.
