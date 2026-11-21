"""Unit test — mcp/db/server.py guardrails (read-only, no secret)."""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "mcp", "db"))

import server as db  # noqa: E402


@pytest.mark.parametrize("sql", [
    "INSERT INTO x VALUES (1)",
    "UPDATE x SET a = 1",
    "DELETE FROM x",
    "DROP TABLE x",
    "CREATE TABLE x (a int)",
    "ALTER TABLE x ADD b int",
])
def test_reject_ddl_dml(sql):
    with pytest.raises(ValueError):
        db.query(sql)


def test_reject_multi_statement():
    # SELECT 1; DROP ... deve essere bloccato (multi-statement)
    with pytest.raises(ValueError):
        db.query("SELECT 1; DROP TABLE x")


def test_reject_non_select():
    with pytest.raises(ValueError):
        db.query("EXPLAIN SELECT 1")


def test_reject_empty():
    with pytest.raises(ValueError):
        db.query("")


def test_db_for_unknown_project_falls_back_to_first():
    # fallback: progetto sconosciuto → primo progetto con db configurato
    cfg = db._db_for("progetto-inesistente")
    assert "host" in cfg


def test_db_for_known_project_has_host():
    # limet2_ws_test ha db configurato in config.yaml
    cfg = db._db_for("limet2_ws_test")
    assert cfg.get("host") == "localhost"
