#!/usr/bin/env python3
"""LIMET — avvia la dashboard con un solo comando.

Se il frontend non è buildato, lo builda (npm install + npm run build).
Poi avvia il backend FastAPI che serve API + frontend su http://127.0.0.1:8787.

Uso:  python dashboard/run.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

FRONTEND = os.path.join(ROOT, "dashboard", "frontend")
DIST = os.path.join(FRONTEND, "dist")


def build_frontend():
    if os.path.isfile(os.path.join(DIST, "index.html")):
        return
    print("Frontend non buildato. Build in corso (npm install + npm run build)…")
    subprocess.run(["npm", "install"], cwd=FRONTEND, check=True)
    subprocess.run(["npm", "run", "build"], cwd=FRONTEND, check=True)
    print("Build completata.")


def main():
    build_frontend()
    import uvicorn

    print("LIMET dashboard → http://127.0.0.1:8787")
    uvicorn.run("dashboard.backend.server:app", host="127.0.0.1", port=8787)


if __name__ == "__main__":
    main()
