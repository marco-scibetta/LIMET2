# LIMET 2.0 — Setup

Installation and configuration guide for team members.

## What it is

LIMET 2.0 is a Claude Code plugin for spec-driven engineering. The repo itself is the plugin and the marketplace: no need to publish it on any public registry.

The plugin ships:

| Component | What | Required? |
|---|---|---|
| 6 skills | `limet-new`, `limet-task`, `limet-test`, `limet-archive`, `limet-bug`, `limet-analyze` | Yes |
| 1 command | `/limet-dashboard` | Yes |
| 3 agents | `limet-gate`, `limet-writer`, `limet-analyzer` | Yes |
| 6 hooks | resume, intent, guardrail, change log, pre-compact, reminder | No (see §4) |
| 1 script | `run-tests.sh` (runs tests, log destroyed if OK) | No (see §4) |
| 3 MCP | `cerebro` (RAG), `db` (read-only SQL), `graphify` (code KG) | No (see §3) |

**The skills work even without MCP and without hooks.** MCP and hooks are optional components that enrich the flow.

---

## 1. Base requirements

- Claude Code CLI (`claude`) 2.x
- Git + access to the `marco-scibetta/LIMET2` repo
- (only for MCP) Python ≥ 3.10 — see §3

---

## 2. Installation

```bash
# 1. Clone the repo
git clone https://github.com/marco-scibetta/LIMET2
cd LIMET2

# 2. Check out the branch that contains the plugin
git checkout dev

# 3. Register the repo as a local marketplace
claude plugin marketplace add ./

# 4. Install the plugin
claude plugin install limet@limet-marketplace
```

One-liner alternative (inside Claude Code, Claude Code ≥ 2.1.275):

```
/plugin install limet --marketplace marco-scibetta/LIMET2
```

> Note: the one-liner clones the repo's **default branch** (today `main`). If the plugin lives on `dev`, use the clone + `git checkout dev` flow above.

### Verify

1. **Restart Claude Code** (skills load at session start).
2. `claude plugin list` → `limet@limet-marketplace` must appear with `enabled` status.
3. In the `/` menu → `/limet-dashboard` must be there.
4. Ask in natural language: *"I want to add a login feature"* → the LIMET flow starts (proposal → spec → plan → task → test → archive).

---

## 3. MCP prerequisites (optional)

The three MCP are **optional**. If you don't configure them, `claude` will show connection errors for them (like `graphify: Connection closed`) but the skills remain fully functional. To disable them entirely, see §6.

### 3.1 Python dependencies

```bash
pip install -e .
```

Installs all the dependencies listed in `pyproject.toml` (qdrant-client, psycopg2-binary, fastapi, etc.). If it fails, install the dependencies one by one from the same file.

### 3.2 `cerebro` — RAG on Qdrant

Requires two running services:

| Service | Default | Env override |
|---|---|---|
| Qdrant (vector DB) | `http://localhost:6333` | `QDRANT_URL` |
| Ollama (embedding) | `http://localhost:11434` | `OLLAMA_URL` |

Other optional envs: `EMBEDDING_MODEL` (default `nomic-embed-text`), `EMBEDDING_DIM` (default `768`).

The embedding model must be loaded in Ollama (`ollama pull nomic-embed-text`). A `.env` in the repo root is loaded automatically.

### 3.3 `db` — read-only SQL

Requires PostgreSQL running. Does **not** read env vars: it reads the `db` section from config files in the plugin root:

```yaml
# config/config.yaml         (committed, shared values)
db:
  host: localhost
  port: 5432
  database: mydb
  user: myuser
  password: ""               # ← put secrets in config.local.yaml, not here

# config/config.local.yaml   (git-ignored, personal secrets)
db:
  password: "my-password"
```

Fields: `host`, `port`, `database`, `user`, `password`, `row_limit` (default 100). The server accepts **only `SELECT`** (DDL/DML rejected).

### 3.4 `graphify` — code knowledge graph

Requires the `graphify-mcp` binary on the `PATH` (provided by the `graphifyy` package).

---

## 4. Hooks on Windows

The 6 hooks are `.sh` scripts (`hooks/*.sh`). On Windows they need **Git Bash** or **WSL** to run. If unavailable, the hooks fail silently: the skills keep working, but you lose auto-activation and the automatic change log.

The helper script `scripts/run-tests.sh` (test execution) is also `.sh` and requires Git Bash/WSL.

Transient test logs go to `limet/.test-logs/` (per-project): make sure the project's `.gitignore` contains `limet/.test-logs/` (`/limet-new` adds it at bootstrap).

To verify on first use: if the change log doesn't populate, check that Git Bash/WSL is present.

---

## 5. Update (after new features)

```bash
claude plugin update limet@limet-marketplace
```

For a local ("live", `Read from: <repo path>`) installation, just edit the files: the change is immediate, no reinstall.

---

## 6. Disabling the MCP (if you don't need them)

If you don't want the MCP connection errors, disable the servers:

```bash
claude plugin disable limet@limet-marketplace   # disables everything (including skills)
```

Or, to remove only the MCP, remove the `mcpServers` section from the plugin manifest before installing (for members who don't use cerebro/db/graphify).

---

## 7. Uninstall

```bash
claude plugin uninstall limet@limet-marketplace
claude plugin marketplace remove limet-marketplace
```

---

## 8. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Skills not visible after install | Claude Code not restarted | Restart Claude Code |
| `graphify: Connection closed` | `graphify-mcp` not on PATH | Install `graphifyy` (§3.4) or ignore |
| `cerebro` fails | Qdrant/Ollama off | Start the services (§3.2) |
| `db` fails | PostgreSQL off or config missing | Check `config/config.yaml` (§3.3) |
| Hooks don't fire (no change log) | Windows without Git Bash/WSL | Install Git Bash or WSL (§4) |
| `claude plugin install` doesn't find `limet` | Marketplace not registered | Re-run `claude plugin marketplace add ./` |
