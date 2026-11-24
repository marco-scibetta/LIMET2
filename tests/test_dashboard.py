"""Unit test — dashboard/backend/server.py (mask segreti, guide lang, info)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dashboard.backend import server as dash  # noqa: E402


def test_mask_hides_password_only():
    cfg = {"db": {"password": "segretissimo", "host": "localhost", "user": "limet"}}
    masked = dash._mask(cfg)
    assert masked["db"]["password"] == "****"
    assert masked["db"]["host"] == "localhost"
    assert masked["db"]["user"] == "limet"


def test_mask_recursive():
    cfg = {"projects": {"a": {"db": {"password": "x"}}}}
    masked = dash._mask(cfg)
    assert masked["projects"]["a"]["db"]["password"] == "****"


def test_info_ok():
    assert dash.info()["status"] == "ok"
    assert dash.info()["name"] == "LIMET dashboard"


def test_guide_lang_valid():
    assert dash._guide_lang("it") == "it"
    assert dash._guide_lang("en") == "en"


def test_guide_lang_invalid_falls_back():
    assert dash._guide_lang("xx") in ("it", "en")


def test_discover_modules_only_with_docs(tmp_path):
    (tmp_path / "module-a" / "docs").mkdir(parents=True)
    (tmp_path / "module-b" / "docs").mkdir(parents=True)
    (tmp_path / "mini_todo").mkdir()   # senza docs/ → NON è un modulo
    (tmp_path / "tests").mkdir()       # senza docs/ → NON è un modulo

    mods = dash._discover_modules(str(tmp_path))
    names = {m["name"] for m in mods}
    assert names == {"module-a", "module-b"}


def test_analyze_endpoint_sets_flag(monkeypatch):
    calls = {}

    def fake_save(data):
        calls.update(data)

    monkeypatch.setattr(dash, "_save_local_config", fake_save)
    body = dash.AnalyzeBody(project="x")
    r = dash.request_analyze(body)
    assert r["ok"] is True
    assert r["analyze"] is True
    assert calls == {"projects": {"x": {"analyze": True}}}


def test_analyze_status_reads_flag(monkeypatch):
    monkeypatch.setattr(dash, "_load_config", lambda: {"projects": {"x": {"analyze": True}}})
    assert dash.analyze_status("x")["analyze"] is True
    monkeypatch.setattr(dash, "_load_config", lambda: {"projects": {"x": {}}})
    assert dash.analyze_status("x")["analyze"] is False
