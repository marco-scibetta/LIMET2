"""Loader condiviso per config.yaml + config.local.yaml (per-progetto)."""
import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "config.yaml")
LOCAL_CONFIG_PATH = os.path.join(HERE, "config.local.yaml")

_DEFAULTS = {
    "qdrant": {"url": "http://localhost:6333"},
    "ollama": {"url": "http://localhost:11434", "model": "nomic-embed-text"},
    "db": {"host": "localhost", "port": 5432, "database": "", "user": ""},
}


def deep_merge(base, override):
    out = dict(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _load_yaml(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def load_config():
    return deep_merge(_load_yaml(CONFIG_PATH), _load_yaml(LOCAL_CONFIG_PATH))


def project_config(slug):
    proj = (load_config().get("projects") or {}).get(slug) or {}
    return deep_merge(_DEFAULTS, proj)


def shared_qdrant_ollama():
    """Infrastruttura condivisa: qdrant/ollama dal primo progetto (o default)."""
    projects = load_config().get("projects") or {}
    for _slug, section in projects.items():
        merged = deep_merge(_DEFAULTS, section)
        return {"qdrant": merged["qdrant"], "ollama": merged["ollama"]}
    return {"qdrant": _DEFAULTS["qdrant"], "ollama": _DEFAULTS["ollama"]}
