#!/usr/bin/env python3
"""LIMET 2.0 — db MCP server (read-only SQL).

Segreti letti da config (config.local.yaml → config.yaml, sezione `db`), mai da env var,
mai esposti nell'output. Solo SELECT (reject DDL/DML). Row limit (default 100).
"""

import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN_ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(HERE))

SERVER_NAME = "db"
SERVER_VERSION = "2.0.0"

_DDL_DML_RE = re.compile(
    r"^\s*(insert|update|delete|drop|create|alter|truncate|grant|revoke|merge|call|"
    r"copy|vacuum|analyze|begin|commit|rollback|set|lock|replace)\b",
    re.IGNORECASE,
)


def _deep_merge(base, override):
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _load_config():
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
                merged = _deep_merge(merged, data.get("projects") or {})
            except Exception:
                pass
    return merged


ROW_LIMIT = 100


def _db_for(project):
    cfg = _load_config()
    if project and project in cfg:
        return (cfg[project].get("db") or {})
    for _p, s in cfg.items():
        if isinstance(s, dict) and s.get("db"):
            return s["db"]
    return {}


def _connect(db):
    import psycopg2
    return psycopg2.connect(
        host=db.get("host", "localhost"),
        port=int(db.get("port", 5432) or 5432),
        dbname=db.get("database") or db.get("dbname") or "",
        user=db.get("user") or "",
        password=db.get("password") or "",
    )


def query(sql, project=""):
    sql = (sql or "").strip()
    if not sql:
        raise ValueError("sql is required")
    if ";" in sql.rstrip(";"):
        raise ValueError("multiple statements are not allowed (read-only)")
    if not sql.lstrip().lower().startswith("select"):
        raise ValueError("only SELECT queries are allowed (read-only)")
    if _DDL_DML_RE.match(sql):
        raise ValueError("only SELECT queries are allowed (read-only)")

    conn = _connect(_db_for(project))
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchmany(ROW_LIMIT + 1)
        truncated = len(rows) > ROW_LIMIT
        rows = rows[:ROW_LIMIT]
        cols = [d[0] for d in cur.description] if cur.description else []
        safe_rows = [
            [str(v) if not isinstance(v, (int, float, str, type(None))) else v for v in r]
            for r in rows
        ]
        return {"columns": cols, "rows": safe_rows, "truncated": truncated}
    finally:
        conn.close()


TOOLS = [
    {
        "name": "db_query",
        "description": "Run a READ-ONLY SQL query (SELECT only) against a project's configured database. Row-limited.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "The SELECT query."},
                "project": {"type": "string", "description": "Project slug (optional)."},
            },
            "required": ["sql"],
        },
    },
]


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
        if name != "db_query":
            return error(-32601, f"unknown tool: {name}")
        try:
            out = query(args.get("sql") or "", args.get("project") or "")
            return result({
                "content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}],
                "isError": False,
            })
        except Exception as e:
            return result({
                "content": [{"type": "text", "text": f"db_query error: {e}"}],
                "isError": True,
            })
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
