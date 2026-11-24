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


def _run(name, payload, cwd=None):
    script = _to_posix(os.path.join(ROOT, "hooks", name))
    r = subprocess.run(
        [BASH, script],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=cwd or ROOT,
        timeout=30,
    )
    return r


def _write_task_list(base, status="pending"):
    d = base / "limet"
    d.mkdir(parents=True, exist_ok=True)
    (d / "TASK_LIST.md").write_text(
        "## Registro modifiche\n\n"
        "| # | Titolo | Scopo | Stato | Dipende | Dettaglio | Note |\n"
        "| - | ------ | ----- | ----- | ------- | -------- | ---- |\n"
        "| 1 | Foo | bar | %s | — | | |\n"
        "| 2 | Baz | qux | done | — | | |\n" % status,
        encoding="utf-8",
    )
    return str(base)


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


def test_intent_analyze():
    r = _run("intent.sh", {"prompt": "analizza il progetto e documentalo", "cwd": str(ROOT)})
    assert r.returncode == 0, r.stderr
    assert "/limet-analyze" in r.stdout


def test_intent_no_false_positive_analyze():
    r = _run("intent.sh", {"prompt": "salva il file adesso", "cwd": str(ROOT)})
    assert "/limet-analyze" not in r.stdout


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


def test_guardrail_blocks_git_reset_hard():
    r = _run("guardrail.sh", {"tool_input": {"command": "git reset --hard HEAD~1"}})
    assert r.returncode == 2, r.stderr


def test_guardrail_blocks_git_clean():
    r = _run("guardrail.sh", {"tool_input": {"command": "git clean -fdx"}})
    assert r.returncode == 2, r.stderr


def test_guardrail_blocks_git_checkout_discard():
    r = _run("guardrail.sh", {"tool_input": {"command": "git checkout -- ."}})
    assert r.returncode == 2, r.stderr


def test_guardrail_blocks_rm_rf():
    r = _run("guardrail.sh", {"tool_input": {"command": "rm -rf build/"}})
    assert r.returncode == 2, r.stderr


def test_guardrail_allows_git_status():
    r = _run("guardrail.sh", {"tool_input": {"command": "git status"}})
    assert r.returncode == 0, r.stderr


def test_resume_active_cycle(tmp_path):
    base = _write_task_list(tmp_path, "in_progress")
    r = _run("resume.sh", {"cwd": base})
    assert r.returncode == 0, r.stderr
    assert "#1" in r.stdout


def test_resume_no_active(tmp_path):
    r = _run("resume.sh", {"cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr
    assert "LIMET" not in r.stdout


def test_precompact_active_cycle(tmp_path):
    base = _write_task_list(tmp_path, "pending")
    r = _run("precompact.sh", {"cwd": base})
    assert r.returncode == 0, r.stderr
    assert "LIMET" in r.stdout
    assert "#1" in r.stdout


def test_precompact_no_active(tmp_path):
    r = _run("precompact.sh", {"cwd": str(tmp_path)})
    assert r.returncode == 0, r.stderr
    assert "LIMET" not in r.stdout


def _run_script(name, args, cwd):
    script = _to_posix(os.path.join(ROOT, "scripts", name))
    return subprocess.run(
        [BASH, script] + args,
        capture_output=True,
        text=True,
        cwd=str(cwd),
        timeout=30,
    )


def _make_change(tmp_path):
    change = tmp_path / "limet" / "changes" / "2026-01-01-x"
    change.mkdir(parents=True)
    return change


def test_run_tests_ok_cleans_up(tmp_path):
    change = _make_change(tmp_path)
    r = _run_script("run-tests.sh", ["echo", "hello"], tmp_path)
    assert r.returncode == 0, r.stderr
    exec_file = change / "TEST_EXECUTION.md"
    assert exec_file.exists()
    assert "OK" in exec_file.read_text(encoding="utf-8")
    logdir = tmp_path / "limet" / ".test-logs"
    assert not (logdir / ".run-tests.tmp.log").exists()
    assert not (logdir / "raw.log").exists()


def test_run_tests_fail_keeps_log(tmp_path):
    change = _make_change(tmp_path)
    r = _run_script("run-tests.sh", ["sh", "-c", "echo boom; exit 3"], tmp_path)
    assert r.returncode == 0, r.stderr
    exec_file = change / "TEST_EXECUTION.md"
    assert "FAIL" in exec_file.read_text(encoding="utf-8")
    logdir = tmp_path / "limet" / ".test-logs"
    raw = logdir / "raw.log"
    assert raw.exists()
    assert "boom" in raw.read_text(encoding="utf-8")
    assert not (logdir / ".run-tests.tmp.log").exists()


def _run_reminder(cwd, env=None):
    script = _to_posix(os.path.join(ROOT, "hooks", "reminder.sh"))
    e = os.environ.copy()
    if env:
        e.update(env)
    return subprocess.run(
        [BASH, script],
        input="{}",
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env=e,
        timeout=30,
    )


def test_reminder_incomplete(tmp_path):
    base = _write_task_list(tmp_path, "in_progress")
    r = _run_reminder(tmp_path, {"CLAUDE_PLUGIN_ROOT": str(ROOT)})
    assert r.returncode == 0, r.stderr
    assert "#1" in r.stdout
    assert "run-tests.sh" in r.stdout


def test_reminder_all_done(tmp_path):
    _write_task_list(tmp_path, "done")
    r = _run_reminder(tmp_path)
    assert r.returncode == 0, r.stderr
    assert "LIMET" not in r.stdout


def test_reminder_no_task(tmp_path):
    r = _run_reminder(tmp_path)
    assert r.returncode == 0, r.stderr
    assert "LIMET" not in r.stdout
