import { useEffect, useState } from 'react'
import { get, post } from '../api'
import PathInput from '../components/PathInput'
import { Dict } from '../i18n'

interface Project {
  slug: string
  root: string
  docs: string[]
}

export default function ReindexPage({ t }: { t: Dict }) {
  const [project, setProject] = useState('')
  const [path, setPath] = useState('')
  const [log, setLog] = useState('')
  const [err, setErr] = useState('')
  const [projects, setProjects] = useState<Project[]>([])
  const [open, setOpen] = useState(false)

  useEffect(() => {
    get<{ projects: Project[] }>('/api/projects')
      .then((r) => setProjects(r.projects))
      .catch(() => {})
  }, [])

  const filtered = projects.filter((p) => p.slug.toLowerCase().includes(project.toLowerCase()))

  function pick(p: Project) {
    setProject(p.slug)
    setPath(p.docs[0] || p.root || '')
    setOpen(false)
  }

  async function run(mode: string) {
    setErr('')
    setLog(t.loading)
    try {
      const r = await post<{ log: string }>('/api/reindex', { project, path, mode })
      setLog(r.log)
    } catch (e) {
      setErr(String(e))
    }
  }

  return (
    <div className="card">
      <h3>{t.reindex}</h3>
      <p className="muted">{t.reindexDesc}</p>
      <div className="form form-wide">
        <div className="form-field" style={{ position: 'relative' }}>
          <span className="form-label">{t.projectAll}</span>
          <input
            value={project}
            onChange={(e) => {
              setProject(e.target.value)
              setOpen(true)
            }}
            onFocus={() => setOpen(true)}
            placeholder={t.projectPlaceholder}
          />
          {open && filtered.length > 0 && (
            <div className="combo">
              {filtered.map((p) => (
                <button
                  key={p.slug}
                  type="button"
                  className="combo-item"
                  onMouseDown={(e) => {
                    e.preventDefault()
                    pick(p)
                  }}
                >
                  {p.slug}
                </button>
              ))}
            </div>
          )}
        </div>
        <div className="form-field">
          <span className="form-label">{t.docsOptional}</span>
          <PathInput value={path} onChange={setPath} placeholder={t.docsPlaceholder} />
        </div>
        <div className="row">
          <button className="button" onClick={() => run('incremental')}>{t.incremental}</button>
          <button className="button" onClick={() => run('force')}>{t.force}</button>
          <button className="button" onClick={() => run('clean')}>{t.prune}</button>
        </div>
      </div>
      {err && <p className="muted">{t.err}: {err}</p>}
      {log && <pre className="log">{log}</pre>}
    </div>
  )
}
