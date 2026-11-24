"""Unit test — config/loader.py (merge, defaults, shared infra)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import loader


def test_deep_merge_nested_keeps_base():
    base = {"db": {"host": "localhost", "port": 5432}}
    override = {"db": {"password": "x"}}
    merged = loader.deep_merge(base, override)
    assert merged["db"]["host"] == "localhost"
    assert merged["db"]["password"] == "x"


def test_project_config_has_defaults_when_missing():
    cfg = loader.project_config("progetto-inesistente")
    assert cfg["qdrant"]["url"] == "http://localhost:6333"
    assert cfg["db"]["host"] == "localhost"
    assert cfg["db"]["port"] == 5432


def test_project_config_merges_overrides():
    # limet2_ws_test è registrato con db.database=limet in config.yaml
    cfg = loader.project_config("limet2_ws_test")
    assert cfg["db"]["host"] == "localhost"


def test_shared_qdrant_ollama_returns_http_urls():
    sh = loader.shared_qdrant_ollama()
    assert "qdrant" in sh and "ollama" in sh
    assert sh["qdrant"]["url"].startswith("http")
    assert sh["ollama"]["url"].startswith("http")
    assert sh["ollama"]["model"]


def test_load_config_has_language():
    cfg = loader.load_config()
    assert "language" in cfg
    assert cfg["language"] in ("it", "en")


def test_analyze_requested_true(monkeypatch):
    monkeypatch.setattr(loader, "load_config", lambda: {"projects": {"x": {"analyze": True}}})
    assert loader.analyze_requested("x") is True


def test_analyze_requested_false_when_missing(monkeypatch):
    monkeypatch.setattr(loader, "load_config", lambda: {"projects": {"x": {}}})
    assert loader.analyze_requested("x") is False
    assert loader.analyze_requested("missing") is False
