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


CONFIG_DIR = os.path.join(PLUGIN_ROOT, "config")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.yaml")
LOCAL_CONFIG_PATH = os.path.join(CONFIG_DIR, "config.local.yaml")

_SECRET_KEYS = {"password"}


def _deep_merge(base, override):
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _load_yaml(path):
    try:
        import yaml
    except ImportError:
        return {}
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def _load_config():
    base = _load_yaml(CONFIG_PATH)
    local = _load_yaml(LOCAL_CONFIG_PATH)
    return _deep_merge(base, local)


def _save_local_config(data):
    import yaml

    existing = _load_yaml(LOCAL_CONFIG_PATH)
    merged = _deep_merge(existing, data)
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(LOCAL_CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(merged, f, sort_keys=False, allow_unicode=True)


def _mask(data):
    out = {}
    for k, v in data.items():
        if isinstance(v, dict):
            out[k] = _mask(v)
        elif k in _SECRET_KEYS and v:
            out[k] = "****"
        else:
            out[k] = v
    return out


def _db_conn_from(cfg):
    import psycopg2

    db = (cfg or {}).get("db", {}) or {}
    return psycopg2.connect(
        host=db.get("host", "localhost"),
        port=int(db.get("port", 5432) or 5432),
        dbname=db.get("database") or db.get("dbname") or "",
        user=db.get("user") or "",
        password=db.get("password") or "",
    )


_DEFAULT_PROJECT = {
    "qdrant": {"url": "http://localhost:6333"},
    "ollama": {"url": "http://localhost:11434", "model": "nomic-embed-text"},
    "db": {"host": "localhost", "port": 5432, "database": "", "user": ""},
}


def _project_config(slug):
    cfg = _load_config()
    proj = (cfg.get("projects") or {}).get(slug) or {}
    return _deep_merge(_DEFAULT_PROJECT, proj)


def _save_project_config(slug, qdrant, ollama, db):
    section = {}
    if qdrant:
        section["qdrant"] = qdrant
    if ollama:
        section["ollama"] = ollama
    if db:
        section["db"] = db
    _save_local_config({"projects": {slug: section}})


@app.get("/api/info")
def info():
    return {"name": "LIMET dashboard", "version": "2.0.0", "status": "ok"}


class ConfigBody(BaseModel):
    project: str = ""
    qdrant: dict = {}
    ollama: dict = {}
    db: dict = {}


@app.get("/api/config")
def get_config(project: str = ""):
    """Configurazione (password mascherata) — globale o di un progetto."""
    if project:
        return _mask(_project_config(project))
    return _mask(_load_config())


@app.post("/api/config")
def save_config(body: ConfigBody):
    """Salva la configurazione di un progetto in config.local.yaml."""
    if not body.project:
        raise HTTPException(status_code=400, detail="project is required")
    _save_project_config(body.project, body.qdrant, body.ollama, body.db)
    return {"ok": True, "config": _mask(_project_config(body.project))}


class TestBody(BaseModel):
    project: str = ""


@app.post("/api/config/test")
def test_db(body: TestBody):
    """Verifica la connessione DB di un progetto (senza esporre i segreti)."""
    cfg = _project_config(body.project) if body.project else _load_config()
    try:
        conn = _db_conn_from(cfg)
        conn.close()
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


class LanguageBody(BaseModel):
    lang: str


@app.post("/api/language")
def set_language(body: LanguageBody):
    """Imposta la lingua globale (it/en) in config.local.yaml."""
    if body.lang not in ("it", "en"):
        raise HTTPException(status_code=400, detail="lang must be 'it' or 'en'")
    _save_local_config({"language": body.lang})
    return {"ok": True, "language": body.lang}


class AnalyzeBody(BaseModel):
    project: str


@app.post("/api/analyze")
def request_analyze(body: AnalyzeBody):
    """Marca un progetto per l'analisi (flag `projects.<slug>.analyze: true`)."""
    if not body.project:
        raise HTTPException(status_code=400, detail="project is required")
    _save_local_config({"projects": {body.project: {"analyze": True}}})
    return {"ok": True, "project": body.project, "analyze": True}


@app.get("/api/analyze")
def analyze_status(project: str = ""):
    """Legge il flag `analyze` di un progetto."""
    if not project:
        raise HTTPException(status_code=400, detail="project is required")
    proj = (_load_config().get("projects") or {}).get(project) or {}
    return {"project": project, "analyze": bool(proj.get("analyze"))}


def _registry():
    try:
        import project_config

        return project_config.load_registry()
    except Exception:
        return {}


def _reachable(url: str, timeout: float = 2.0) -> bool:
    import urllib.request

    # Windows: `localhost` risolve prima `::1` (IPv6) e si blocca ~2s se il servizio
    # ascolta solo su IPv4. Forza 127.0.0.1 per il loopback.
    url = url.replace("localhost", "127.0.0.1")
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            r.read()
        return True
    except Exception:
        return False


@app.get("/api/status")
def status():
    from concurrent.futures import ThreadPoolExecutor

    qdrant_url = (_DEFAULT_PROJECT.get("qdrant") or {}).get("url", "http://localhost:6333").rstrip("/")
    ollama_url = (_DEFAULT_PROJECT.get("ollama") or {}).get("url", "http://localhost:11434").rstrip("/")

    with ThreadPoolExecutor(max_workers=2) as ex:
        f_q = ex.submit(_reachable, qdrant_url + "/collections")
        f_o = ex.submit(_reachable, ollama_url + "/api/tags")
        qdrant_ok = f_q.result()
        ollama_ok = f_o.result()

    return {
        "qdrant": qdrant_ok,
        "ollama": ollama_ok,
        "projects": sorted(_registry().keys()),
    }


@app.get("/api/projects")
def projects():
    reg = _registry()
    return {
        "projects": [
            {"slug": s, "docs": e.get("docs", []), "root": e.get("root", ""),
             "collections": e.get("collections", [])}
            for s, e in reg.items()
        ]
    }


class LinkBody(BaseModel):
    a: str
    b: str


@app.post("/api/link")
def link(body: LinkBody):
    import project_config

    reg = project_config.load_registry()
    sa = project_config.sanitize_project_name(body.a)
    sb = project_config.sanitize_project_name(body.b)
    ca = project_config.collection_for(body.a)
    cb = project_config.collection_for(body.b)
    linked = []
    for slug, extra in ((sa, cb), (sb, ca)):
        entry = reg.setdefault(slug, {})
        cols = list(entry.get("collections") or [])
        if extra not in cols:
            cols.append(extra)
        entry["collections"] = cols
        linked.append(f"{slug} -> {extra}")
    project_config.save_registry(reg)
    return {"ok": True, "linked": linked}


@app.post("/api/unlink")
def unlink(body: LinkBody):
    import project_config

    reg = project_config.load_registry()
    sa = project_config.sanitize_project_name(body.a)
    sb = project_config.sanitize_project_name(body.b)
    ca = project_config.collection_for(body.a)
    cb = project_config.collection_for(body.b)
    for slug, extra in ((sa, cb), (sb, ca)):
        entry = reg.get(slug, {})
        cols = [c for c in (entry.get("collections") or []) if c != extra]
        if cols:
            entry["collections"] = cols
        else:
            entry.pop("collections", None)
    project_config.save_registry(reg)
    return {"ok": True, "unlinked": [sa, sb]}


class ReindexBody(BaseModel):
    project: str = ""
    path: str = ""
    mode: str = "incremental"


@app.post("/api/reindex")
def reindex(body: ReindexBody):
    import subprocess

    script = os.path.join(ROOT, "mcp", "cerebro", "ingest_docs.py")
    cmd = [sys.executable, script]
    if body.project:
        cmd += ["--project", body.project]
    if body.path:
        cmd += [body.path]
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
    workspace: bool = False


_EXCLUDE_DIRS = {
    ".git", "node_modules", "__pycache__", "dist", "build", "graphify-out",
    "limet", "docs", "venv", ".venv", "env",
}


def _discover_modules(root):
    modules = []
    try:
        for name in sorted(os.listdir(root)):
            full = os.path.join(root, name)
            if not os.path.isdir(full) or name in _EXCLUDE_DIRS or name.startswith("."):
                continue
            docs = os.path.join(full, "docs")
            if os.path.isdir(docs):
                modules.append({"name": name, "docs": docs})
    except Exception:
        pass
    return modules


@app.post("/api/init")
def init(body: InitBody):
    import shutil
    import subprocess

    if not body.path:
        raise HTTPException(status_code=400, detail="path (docs) is required")

    norm = os.path.normpath(body.path.rstrip("\\/"))
    if os.path.basename(norm).lower() == "docs":
        root = os.path.dirname(norm)
        docs_path = norm
    else:
        root = norm
        candidate = os.path.join(root, "docs")
        docs_path = candidate if os.path.isdir(candidate) else norm

    def _run(cmd, timeout):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, encoding="utf-8")
        return (r.stdout + r.stderr).strip()

    log = []

    # docs: docs_path + (se workspace) i docs dei moduli
    docs_paths = [docs_path]
    modules = []
    if body.workspace:
        modules = _discover_modules(root)
        docs_paths += [m["docs"] for m in modules]

    # 1) registra UN progetto con TUTTI i docs (root + moduli) → Qdrant/Graphify/DB unici
    reg = os.path.join(ROOT, "mcp", "cerebro", "register_project.py")
    reg_cmd = [sys.executable, reg, "add", body.project, "--docs"] + docs_paths + ["--root", root]
    log.append("=== register ===\n" + _run(reg_cmd, 120))

    # 2) graphify: unico grafo su root (copre tutti i moduli)
    graphify = shutil.which("graphify")
    if graphify:
        log.append("=== graphify ===\n" + _run(
            [graphify, "extract", root, "--code-only"], 600))
    else:
        log.append("=== graphify ===\n(comando `graphify` non trovato nel PATH)")

    # 3) ingestion Qdrant: unica collection con tutti i docs
    ing = os.path.join(ROOT, "mcp", "cerebro", "ingest_docs.py")
    log.append("=== qdrant ingest ===\n" + _run(
        [sys.executable, ing, "--project", body.project], 600))

    if body.workspace:
        if modules:
            log.append(f"=== workspace: {len(modules)} moduli, docs indicizzati nella collection '{body.project}' ===")
        else:
            log.append("=== workspace: nessun modulo trovato ===")

    return {"log": "\n\n".join(log)}


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


# Documentazione (HTML servita dal backend, prima del fallback SPA)
def _guide_lang(lang: str) -> str:
    if lang in ("it", "en"):
        return lang
    return (_load_config().get("language") or "it")


@app.get("/docs/setup", include_in_schema=False)
def serve_setup_doc(lang: str = ""):
    l = _guide_lang(lang)
    return FileResponse(os.path.join(ROOT, "guides", l, "limet-setup.html"))


@app.get("/docs/project-init", include_in_schema=False)
def serve_project_init_doc(lang: str = ""):
    l = _guide_lang(lang)
    return FileResponse(os.path.join(ROOT, "guides", l, "limet-project-init.html"))


@app.get("/docs/workflow", include_in_schema=False)
def serve_workflow_doc(lang: str = ""):
    l = _guide_lang(lang)
    return FileResponse(os.path.join(ROOT, "guides", l, "workflow.html"))


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
