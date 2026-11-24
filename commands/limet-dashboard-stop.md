---
description: Stop the LIMET dashboard (terminate the process listening on port :8787)
---

Stop the LIMET dashboard by closing the process listening on port 8787.

Run (PowerShell tool):

```
$pids = Get-NetTCPConnection -LocalPort 8787 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($pids) {
    $pids | ForEach-Object { Stop-Process -Id $_ -Force }
    "Dashboard stopped."
} else {
    "No dashboard active on http://127.0.0.1:8787"
}
```

If `Get-NetTCPConnection` is not available, fallback:
`netstat -ano | findstr :8787` → take the PID in the last column of the `LISTENING` row,
then `taskkill /PID <pid> /F`.

Reply to the user only with the outcome ("Dashboard stopped." or
"No dashboard active on http://127.0.0.1:8787").
