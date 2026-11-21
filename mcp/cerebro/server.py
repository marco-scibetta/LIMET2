#!/usr/bin/env python3
"""LIMET 2.0 — cerebro MCP server (RAG su Qdrant).

Espone 5 tool: cerebro_search, cerebro_count, cerebro_list, cerebro_ingest, cerebro_register.
Stdlib-only (JSON-RPC newline-delimited su stdio), coerente con la base CEREBRO.
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

ROOT = os.path.dirname(os.path.dirname(HERE))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import project_config  # noqa: E402
from config.loader import shared_qdrant_ollama  # noqa: E402

_sh = shared_qdrant_ollama()
QDRANT_URL = os.getenv("QDRANT_URL", _sh["qdrant"].get("url") or "http://localhost:6333")
OLLAMA_URL = os.getenv("OLLAMA_URL", _sh["ollama"].get("url") or "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBEDDING_MODEL", _sh["ollama"].get("model") or "nomic-embed-text")

SERVER_NAME = "cerebro"
SERVER_VERSION = "2.0.0"


def _post(url, payload, timeout=60):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _embed(text):
    return _post(f"{OLLAMA_URL}/api/embeddings",
                 {"model": EMBED_MODEL, "prompt": text})["embedding"]


def _default_project():
    cwd = os.getcwd().rstrip("\\/")
    name = os.path.basename(cwd)
    try:
        return project_config.sanitize_project_name(name)
    except ValueError:
        return name


def _project(args):
    return (args.get("project") or "").strip() or _default_project()


def search(project, query, limit):
    if not query:
        raise ValueError("query is required")
    vector = _embed(query)
    results = []
    for coll in project_config.collections_for(project):
        try:
            data = _post(f"{QDRANT_URL}/collections/{coll}/points/search",
                         {"vector": vector, "limit": limit, "with_payload": True})
            for pt in data.get("result", []):
                p = pt.get("payload", {}) or {}
                results.append({
                    "score": round(pt.get("score", 0.0), 4),
                    "collection": coll,
                    "source": p.get("source", ""),
                    "text": p.get("text", ""),
                })
        except urllib.error.HTTPError as e:
            results.append({"score": 0, "collection": coll, "source": "ERROR",
                            "text": f"collection '{coll}' unavailable: {e}"})
        except Exception as e:
            results.append({"score": 0, "collection": coll, "source": "ERROR",
                            "text": f"search error: {e}"})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def count(project):
    total = 0
    lines = []
    for coll in project_config.collections_for(project):
        try:
            data = _post(f"{QDRANT_URL}/collections/{coll}/points/count", {"exact": True})
            c = int(data.get("result", {}).get("count", 0))
        except Exception as e:
            lines.append(f"{coll}: error ({e})")
            continue
        total += c
        lines.append(f"{coll}: {c} chunks")
    return f"Project '{project}': {total} total chunks.\n" + "\n".join(lines)


def list_collections(project):
    return "Collections for project '%s': %s" % (
        project, ", ".join(project_config.collections_for(project)))


def ingest(project):
    script = os.path.join(HERE, "ingest_docs.py")
    try:
        out = subprocess.run([sys.executable, script, "--project", project],
                             capture_output=True, text=True, timeout=600, encoding="utf-8")
        return (out.stdout + out.stderr).strip() or "ingest completed (no output)"
    except subprocess.TimeoutExpired:
        return "ingest timed out after 600s"
    except Exception as e:
        return f"ingest error: {e}"


def register(project, path):
    script = os.path.join(HERE, "register_project.py")
    cmd = [sys.executable, script, project]
    if path:
        cmd.append(path)
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120, encoding="utf-8")
        return (out.stdout + out.stderr).strip() or "registered"
    except Exception as e:
        return f"register error: {e}"


TOOLS = [
    {
        "name": "cerebro_search",
        "description": "Semantic search over this project's documentation indexed in Qdrant (CEREBRO RAG). Returns the most relevant chunks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The question/topic."},
                "project": {"type": "string", "description": "Project slug (optional)."},
                "limit": {"type": "integer", "minimum": 1, "maximum": 20, "description": "Max results (default 5)."},
            },
            "required": ["query"],
        },
    },
    {
        "name": "cerebro_count",
        "description": "Count indexed chunks for a project.",
        "inputSchema": {"type": "object", "properties": {"project": {"type": "string"}}},
    },
    {
        "name": "cerebro_list",
        "description": "List the Qdrant collections of a project.",
        "inputSchema": {"type": "object", "properties": {"project": {"type": "string"}}},
    },
    {
        "name": "cerebro_ingest",
        "description": "Index/embed the project's documents into Qdrant (batch embedding).",
        "inputSchema": {"type": "object", "properties": {"project": {"type": "string"}}},
    },
    {
        "name": "cerebro_register",
        "description": "Register a project into CEREBRO (projects.json).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "path": {"type": "string", "description": "Optional docs path."},
            },
        },
    },
]


def _dispatch(name, args):
    if name == "cerebro_search":
        project = _project(args)
        chunks = search(project, (args.get("query") or "").strip(), int(args.get("limit") or 5))
        lines = [f"Top {len(chunks)} chunks (project '{project}'):\n"]
        for r in chunks:
            lines.append(f"[{r['score']}] {r['source']}  (collection {r['collection']})")
            lines.append(r["text"].strip())
            lines.append("---")
        return "\n".join(lines)
    if name == "cerebro_count":
        return count(_project(args))
    if name == "cerebro_list":
        return list_collections(_project(args))
    if name == "cerebro_ingest":
        return ingest(_project(args))
    if name == "cerebro_register":
        return register(_project(args), (args.get("path") or "").strip())
    raise ValueError(f"unknown tool: {name}")


def _handle(msg):
    method = msg.get("method")
    req_id = msg.get("id")
    params = msg.get("params") or {}

    def result(obj):
        return {"jsonrpc": "2.0", "id": req_id, "result": obj}

    def error(code, message):
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}

    if method == "initialize":
        proto = params.get("protocolVersion", "2024-11-05")
        return result({
            "protocolVersion": proto,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        })
    if method == "ping":
        return result({})
    if method == "tools/list":
        return result({"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            text = _dispatch(name, args)
            return result({"content": [{"type": "text", "text": text}], "isError": False})
        except Exception as e:
            return result({"content": [{"type": "text", "text": f"{name} error: {e}"}], "isError": True})
    return error(-32601, f"method not found: {method}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("id") is None:
            continue
        try:
            out = _handle(msg)
        except Exception as e:
            out = {"jsonrpc": "2.0", "id": msg.get("id"),
                   "error": {"code": -32603, "message": str(e)}}
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
