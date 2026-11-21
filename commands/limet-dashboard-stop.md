---
description: Ferma la dashboard LIMET (termina il processo in ascolto sulla porta :8787)
---

Ferma la dashboard LIMET chiudendo il processo che ascolta sulla porta 8787.

Esegui (PowerShell tool):

```
$pids = Get-NetTCPConnection -LocalPort 8787 -State Listen -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($pids) {
    $pids | ForEach-Object { Stop-Process -Id $_ -Force }
    "Dashboard fermata."
} else {
    "Nessuna dashboard attiva su http://127.0.0.1:8787"
}
```

Se `Get-NetTCPConnection` non è disponibile, fallback:
`netstat -ano | findstr :8787` → prendi il PID nella colonna finale della riga `LISTENING`,
poi `taskkill /PID <pid> /F`.

Rispondi all'utente solo con l'esito ("Dashboard fermata." oppure
"Nessuna dashboard attiva su http://127.0.0.1:8787").
