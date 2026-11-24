import { useEffect, useState } from 'react'
import { get, post } from '../api'
import { Dict } from '../i18n'

interface Project {
  slug: string
  root: string
  docs: string[]
}

export default function AnalyzePage({ t }: { t: Dict }) {
  const [projects, setProjects] = useState<Project[]>([])
  const [slug, setSlug] = useState('')
  const [analyze, setAnalyze] = useState(false)
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')

  useEffect(() => {
    get<{ projects: Project[] }>('/api/projects')
      .then((r) => setProjects(r.projects))
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (!slug) {
      setAnalyze(false)
      return
    }
    get<{ analyze: boolean }>(`/api/analyze?project=${encodeURIComponent(slug)}`)
      .then((r) => setAnalyze(r.analyze))
      .catch(() => setAnalyze(false))
  }, [slug])

  async function request() {
    setErr('')
    setMsg('')
    try {
      await post('/api/analyze', { project: slug })
      setAnalyze(true)
      setMsg(t.analyzeRequested)
    } catch (e) {
      setErr(String(e))
    }
  }

  return (
    <div className="card">
      <h3>{t.analyze}</h3>
      <p className="muted">{t.analyzeDesc}</p>
      <div className="form form-wide">
        <div className="form-field">
          <span className="form-label">{t.project}</span>
          <select value={slug} onChange={(e) => setSlug(e.target.value)}>
            <option value="">{t.selectProject}</option>
            {projects.map((p) => (
              <option key={p.slug} value={p.slug}>{p.slug}</option>
            ))}
          </select>
        </div>

        {!slug && <p className="muted">{t.selectPrompt}</p>}

        {slug && (
          <>
            <p className="muted">{t.analyzeHint} <code>/limet-analyze</code></p>
            <div className="row">
              <button className="button" onClick={request}>{t.analyzeRequest}</button>
            </div>
            {analyze && <span className="badge ok">{t.analyzeOn}</span>}
          </>
        )}
      </div>
      {err && <p className="muted">{t.err}: {err}</p>}
      {msg && <p className="muted">{msg}</p>}
    </div>
  )
}
