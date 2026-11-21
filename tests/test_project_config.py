"""Unit test — mcp/cerebro/project_config.py (slug, collection, link)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "mcp", "cerebro"))

import project_config  # noqa: E402


def test_sanitize_project_name():
    assert project_config.sanitize_project_name("My App") == "my_app"
    assert project_config.sanitize_project_name("c:\\progetti\\x") == "c_progetti_x"


def test_collection_for():
    assert project_config.collection_for("My App") == "CRB_my_app"


def test_collections_for_primary_only_when_no_link():
    cols = project_config.collections_for("progetto-inesistente")
    assert cols == ["CRB_progetto_inesistente"]


def test_collections_for_includes_linked():
    # limet2_test_dummy è collegato a limet2_ws_test (registro)
    cols = project_config.collections_for("limet2_test_dummy")
    assert "CRB_limet2_test_dummy" in cols
    assert "CRB_limet2_ws_test" in cols  # collection collegata
