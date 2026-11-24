---
description: Launch the LIMET dashboard (build if needed + API/UI server on :8787)
---

Launch the LIMET dashboard by running `python dashboard/run.py` **in the background** (Bash tool with
`run_in_background: true`), then report to the user:

> Dashboard started → http://127.0.0.1:8787

If port 8787 is already in use (dashboard already active), do not restart it: just answer
"Dashboard already active on http://127.0.0.1:8787".
