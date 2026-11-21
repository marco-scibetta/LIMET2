#!/usr/bin/env python3
"""LIMET 2.0 — dashboard REST backend (FastAPI).

Stessa logica dei server MCP (cerebro/db), esposta come REST per la dashboard React.
Le pagine (#19) consumano questi endpoint. CORS aperto per dev locale.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(ROOT, "mcp", "cerebro"), os.path.join(ROOT, "mcp", "db")):
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel  # noqa: E402

app = FastAPI(title="LIMET dashboard", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or ROOT


def _load_db_config():
    try:
        import yaml
    except ImportError:
        return {}
    merged = {}
    for name in ("config.yaml", "config.local.yaml"):
        p = os.path.join(PLUGIN_ROOT, "config", name)
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                for k, v in (data.get("db") or {}).items():
                    if v is not None:
                        merged[k] = v
            except Exception:
                pass
    return merged


@app.get("/api/info")
def info():
    return {"name": "LIMET dashboard", "version": "2.0.0", "status": "ok"}


class SqlBody(BaseModel):
    sql: str


@app.post("/api/db/test")
def db_test():
    """Verifica la connessione read-only (senza esporre i segreti)."""
    import psycopg2

    db = _load_db_config()
    try:
        conn = psycopg2.connect(
            host=db.get("host", "localhost"),
            port=int(db.get("port", 5432) or 5432),
            dbname=db.get("database") or db.get("dbname") or "",
            user=db.get("user") or "",
            password=db.get("password") or "",
        )
        conn.close()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"connection failed: {e}")


@app.post("/api/db/schema")
def db_schema():
    """Elenco tabelle (read-only)."""
    import psycopg2

    db = _load_db_config()
    try:
        conn = psycopg2.connect(
            host=db.get("host", "localhost"),
            port=int(db.get("port", 5432) or 5432),
            dbname=db.get("database") or db.get("dbname") or "",
            user=db.get("user") or "",
            password=db.get("password") or "",
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT table_schema, table_name FROM information_schema.tables "
            "WHERE table_schema NOT IN ('pg_catalog', 'information_schema') "
            "ORDER BY table_schema, table_name"
        )
        rows = [{"schema": r[0], "table": r[1]} for r in cur.fetchall()]
        conn.close()
        return {"tables": rows}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"schema error: {e}")


def _registry():
    try:
        import project_config

        return project_config.load_registry()
    except Exception:
        return {}


@app.get("/api/status")
def status():
    import urllib.request

    def reachable(url):
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=2) as r:
                r.read()
            return True
        except Exception:
            return False

    return {
        "qdrant": reachable("http://localhost:6333/collections"),
        "ollama": reachable("http://localhost:11434/api/tags"),
        "projects": sorted(_registry().keys()),
    }


@app.get("/api/projects")
def projects():
    reg = _registry()
    return {
        "projects": [
            {"slug": s, "docs": e.get("docs", []), "root": e.get("root", "")}
            for s, e in reg.items()
        ]
    }


class ReindexBody(BaseModel):
    project: str = ""
    mode: str = "incremental"


@app.post("/api/reindex")
def reindex(body: ReindexBody):
    import subprocess

    script = os.path.join(ROOT, "mcp", "cerebro", "ingest_docs.py")
    cmd = [sys.executable, script]
    if body.project:
        cmd += ["--project", body.project]
    if body.mode == "force":
        cmd += ["--force"]
    elif body.mode == "clean":
        cmd += ["--prune"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=600, encoding="utf-8")
        return {"log": (out.stdout + out.stderr).strip() or "reindex completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class InitBody(BaseModel):
    project: str
    path: str = ""


@app.post("/api/init")
def init(body: InitBody):
    import subprocess

    if not body.path:
        raise HTTPException(status_code=400, detail="path (docs) is required")
    script = os.path.join(ROOT, "mcp", "cerebro", "register_project.py")
    cmd = [sys.executable, script, "add", body.project, "--docs", body.path]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120, encoding="utf-8")
        return {"log": (out.stdout + out.stderr).strip() or "registered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/browse")
def browse(path: str = ""):
    """Elenca le sottocartelle di un percorso (per il file browser della dashboard)."""
    import os

    target = path.strip() or os.path.expanduser("~")
    if not os.path.isdir(target):
        target = os.path.dirname(target) or os.path.abspath(os.sep)
    dirs = []
    try:
        for name in sorted(os.listdir(target)):
            full = os.path.join(target, name)
            if os.path.isdir(full):
                dirs.append({"name": name, "path": full})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"path": target, "parent": os.path.dirname(target), "dirs": dirs}


# Serve il frontend buildato (dist/) così la dashboard parte con UN SOLO processo.
from fastapi.staticfiles import StaticFiles  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402

DIST = os.path.join(ROOT, "dashboard", "frontend", "dist")
ASSETS = os.path.join(DIST, "assets")

if os.path.isdir(ASSETS):
    app.mount("/assets", StaticFiles(directory=ASSETS), name="assets")


@app.get("/", include_in_schema=False)
def serve_root():
    index = os.path.join(DIST, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    raise HTTPException(status_code=503, detail="frontend not built (run: npm run build)")


@app.get("/{path:path}", include_in_schema=False)
def serve_spa(path: str):
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="not found")
    index = os.path.join(DIST, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    raise HTTPException(status_code=503, detail="frontend not built (run: npm run build)")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8787)
