import { useEffect, useState } from 'react'
import { get } from '../api'

interface Project {
  slug: string
  docs: string[]
  root: string
}

export default function ProjectsPage() {
  const [p, setP] = useState<Project[] | null>(null)
  const [err, setErr] = useState('')

  useEffect(() => {
    get<{ projects: Project[] }>('/api/projects')
      .then((r) => setP(r.projects))
      .catch((e) => setErr(String(e)))
  }, [])

  if (err) return <p className="muted">Errore: {err}</p>
  if (!p) return <p className="muted">Caricamento…</p>

  return (
    <div className="card">
      <h3>Progetti ({p.length})</h3>
      {p.length === 0 ? (
        <p className="muted">Nessun progetto registrato.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Slug</th>
              <th>Root</th>
              <th>Docs</th>
            </tr>
          </thead>
          <tbody>
            {p.map((x) => (
              <tr key={x.slug}>
                <td>{x.slug}</td>
                <td>{x.root}</td>
                <td>{x.docs.join(', ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
