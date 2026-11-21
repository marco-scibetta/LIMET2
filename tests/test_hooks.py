"""Unit test — hooks (intent, guardrail) via bash + JSON stdin."""
import json
import os
import shutil
import subprocess

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _find_bash():
    for c in [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
    ]:
        if os.path.exists(c):
            return c
    return shutil.which("bash")


def _to_posix(path):
    p = path.replace("\\", "/")
    if len(p) >= 2 and p[1] == ":":
        p = "/" + p[0].lower() + p[2:]
    return p


BASH = _find_bash()
pytestmark = pytest.mark.skipif(BASH is None, reason="bash non disponibile")


def _run(name, payload):
    script = _to_posix(os.path.join(ROOT, "hooks", name))
    r = subprocess.run(
        [BASH, script],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=ROOT,
        timeout=30,
    )
    return r


def test_intent_feature():
    r = _run("intent.sh", {"prompt": "aggiungi una feature di login", "cwd": str(ROOT)})
    assert r.returncode == 0, r.stderr
    assert "/limet-new" in r.stdout


def test_intent_bug():
    r = _run("intent.sh", {"prompt": "c'è un bug nella login", "cwd": str(ROOT)})
    assert "/limet-bug" in r.stdout


def test_intent_no_false_positive_on_command_name():
    r = _run("intent.sh", {"prompt": "limet-bug e limet-new sono comandi", "cwd": str(ROOT)})
    assert "/limet-bug" not in r.stdout


def test_intent_related_projects():
    dummy = os.environ.get("LIMET_TEST_DUMMY")
    if not dummy:
        pytest.skip("LIMET_TEST_DUMMY non impostato (serve un progetto con link)")
    r = _run("intent.sh", {"prompt": "cosa fa questo progetto?", "cwd": dummy})
    assert "collegato" in r.stdout
    assert "cerebro_search" in r.stdout


def test_guardrail_blocks_git_commit():
    r = _run("guardrail.sh", {"tool_input": {"command": "git commit -m test"}})
    assert r.returncode == 2, r.stderr


def test_guardrail_blocks_pytest():
    r = _run("guardrail.sh", {"tool_input": {"command": "python -m pytest"}})
    assert r.returncode == 2, r.stderr


def test_guardrail_allows_ls():
    r = _run("guardrail.sh", {"tool_input": {"command": "ls"}})
    assert r.returncode == 0, r.stderr
