import { useState } from 'react'
import { post } from '../api'
import PathInput from '../components/PathInput'

export default function InitPage() {
  const [project, setProject] = useState('')
  const [path, setPath] = useState('')
  const [out, setOut] = useState('')
  const [err, setErr] = useState('')

  async function submit() {
    setErr('')
    setOut('')
    try {
      const r = await post<{ log: string }>('/api/init', { project, path })
      setOut(r.log)
    } catch (e) {
      setErr(String(e))
    }
  }

  return (
    <div className="card">
      <h3>Init / Setup</h3>
      <p className="muted">Registra un progetto in CEREBRO (projects.json).</p>
      <div className="form">
        <div className="form-field">
          <span className="form-label">Nome progetto</span>
          <input value={project} onChange={(e) => setProject(e.target.value)} />
        </div>
        <div className="form-field">
          <span className="form-label">Percorso docs</span>
          <PathInput value={path} onChange={setPath} placeholder="C:\Progetti\mio-progetto\docs" />
        </div>
        <button className="button" onClick={submit}>Registra</button>
      </div>
      {err && <p className="muted">Errore: {err}</p>}
      {out && <pre className="log">{out}</pre>}
    </div>
  )
}
