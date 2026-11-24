# LIMET 2.0 — Optimizations (philosophy kept)

LIMET 1.0 was right in **philosophy** (spec-driven, traceability, non-negotiable testing) but **heavy in execution**. LIMET 2.0 keeps the philosophy and optimizes the execution. Do not bloat: each optimization removes friction, not adds complexity.

## 1. Doc-heavy → skill-automated

- **1.0**: 18 .md templates the human fills by hand. Friction = traceability gets skipped.
- **2.0**: 6 skills. Claude generates the documents, the human approves. The document stays the source of truth (§1.1) but is no longer a module to compile.

## 2. Tool-agnostic → Claude-only

- **1.0**: two editions (IT/EN) + Copilot/Claude compatibility = maintenance overhead.
- **2.0**: Claude Code only. Gone the double document tree and the "tool-agnostic" abstraction. (EN can be added later, if needed.)

## 3. Python/CLI → MCP

- **1.0**: CEREBRO = guide skill that orchestrates Python scripts; GRAPHIFY = CLI.
- **2.0**: CEREBRO wrapped in MCP (same scripts), Graphify via native MCP (`graphify-mcp`). Claude calls `cerebro_search(...)` instead of running `python query_qdrant.py`.

## 4. Manual templates → hook-driven

- **1.0**: the change log (§1.4) and the archive were filled by hand.
- **2.0**: `PostToolUse` appends to the change log automatically; `Stop` reminds about the archive. The boring work disappears.

## 5. Rules from text → enforcement

- **1.0**: §1.3 (no autonomous build/test) and §1.5 (non-negotiable testing) were *written* in CLAUDE.md.
- **2.0**: `PreToolUse` *blocks* build/test; `limet-gate` *rejects* tasks without verification. "An instruction is a request; a hook is enforcement."

## 6. Consolidation: 18 → 6 skills

- **1.0**: one template per artifact = 18 separate documents.
- **2.0**: `/limet-new` generates the whole cycle together (proposal+spec+plan+task+test+e2e). Support docs (glossary, conventions, analysis…) are generated on demand. Less friction, same traceability.

## 7. Self-contained: one repo

- **1.0**: LIMET + CEREBRO + GRAPHIFY = three separate things to install.
- **2.0**: everything in one repo. Cerebro and Graphify are inside `mcp/`. One `claude plugin install` + a `docker-compose` for Qdrant/Ollama. Fewer dependencies, clean distribution.

## 8. Batch embedding, not one-at-a-time (ingestion speed fix)

- **1.0**: `ingest_docs.py` does **one HTTP POST to Ollama per chunk** (`/api/embeddings`). A PDF with 300 chunks = 300 round-trips → slowness. **No GPU needed**: `nomic-embed-text` is small (~137M), runs on CPU.
- **2.0**: **batch `/api/embed`** (list of chunks in one call) or **`fastembed`/ONNX in-process** (no Ollama server). 10-50× faster, on CPU. Optional parallel PDF parsing with `pypdfium2`.

## 9. PDF/EPUB parsing: direct pypdfium2 + parallel (second bottleneck)

- **1.0**: `doc_to_markdown.py` uses **pdfplumber** page by page (slow), and for each image renders at 150 DPI and saves PNG **serially**. It is the second bottleneck, after the one-at-a-time embedding.
- **2.0**:
  - **Direct `pypdfium2`** for the text (dependency already present, much faster than pdfplumber).
  - **Parallelize pages** (`concurrent.futures`).
  - Image rendering at reduced resolution / only if needed (not a fixed 150 DPI for all).

## Per-script summary (full Cerebro audit)

| Script | Bottleneck | 2.0 fix |
|---|---|---|
| `ingest_docs.py` | embedding 1 chunk = 1 HTTP POST | batch `/api/embed` or fastembed/ONNX |
| `doc_to_markdown.py` | slow pdfplumber + serial image rendering | direct pypdfium2 + parallel |
| `query_qdrant.py` | ok (single query + Qdrant search) | — |
| `register_project.py` | ok (light JSON) | — |
| `serve_images.py` | ok (static server) | — |

## What does NOT change (the philosophy)

- Spec-driven, not vibe-driven (§1.1).
- Traceability of decisions (§1.2).
- Separation of writing/execution (§1.3).
- Non-negotiable testing (§1.5).
- Lightweight: 6 skills, 6 hooks, 3 subagents, 3 MCP. Stop.
- **Conversational** (like 1.0): the user talks, doesn't type commands — the `intent` hook detects and starts.
