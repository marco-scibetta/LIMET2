import { useState } from 'react'
import { post } from '../api'

export default function ReindexPage() {
  const [project, setProject] = useState('')
  const [log, setLog] = useState('')
  const [err, setErr] = useState('')

  async function run(mode: string) {
    setErr('')
    setLog('Avvio…')
    try {
      const r = await post<{ log: string }>('/api/reindex', { project, mode })
      setLog(r.log)
    } catch (e) {
      setErr(String(e))
    }
  }

  return (
    <div className="card">
      <h3>Re-index</h3>
      <div className="form">
        <label>
          Progetto (vuoto = tutti)
          <input value={project} onChange={(e) => setProject(e.target.value)} />
        </label>
        <div className="row">
          <button className="button" onClick={() => run('incremental')}>Incrementale</button>
          <button className="button" onClick={() => run('force')}>Forza</button>
          <button className="button" onClick={() => run('clean')}>Pulizia (prune)</button>
        </div>
      </div>
      {err && <p className="muted">Errore: {err}</p>}
      {log && <pre className="log">{log}</pre>}
    </div>
  )
}
