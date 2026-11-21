import { useEffect, useState } from 'react'
import { get, post } from '../api'
import PathInput from '../components/PathInput'
import { Dict } from '../i18n'

interface Project {
  slug: string
  root: string
  docs: string[]
}

export default function InitPage({ t }: { t: Dict }) {
  const [project, setProject] = useState('')
  const [path, setPath] = useState('')
  const [out, setOut] = useState('')
  const [err, setErr] = useState('')
  const [projects, setProjects] = useState<Project[]>([])
  const [open, setOpen] = useState(false)
  const [workspace, setWorkspace] = useState(false)

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

  async function submit() {
    setErr('')
    setOut('')
    try {
      const r = await post<{ log: string }>('/api/init', { project, path, workspace })
      setOut(r.log)
    } catch (e) {
      setErr(String(e))
    }
  }

  return (
    <div className="card card-narrow">
      <h3>{t.init}</h3>
      <div className="form">
        <div className="form-field" style={{ position: 'relative' }}>
          <span className="form-label">{t.projectName}</span>
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
          <span className="form-label">{t.docsPath}</span>
          <PathInput value={path} onChange={setPath} placeholder={t.docsPlaceholder} />
        </div>
        <label className="checkbox-row">
          <input type="checkbox" checked={workspace} onChange={(e) => setWorkspace(e.target.checked)} />
          <span>{t.workspace}</span>
        </label>
        <button className="button" onClick={submit}>{t.register}</button>
      </div>
      {err && <p className="muted">{t.err}: {err}</p>}
      {out && <pre className="log">{out}</pre>}
    </div>
  )
}
