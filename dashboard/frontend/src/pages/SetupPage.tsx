import { useEffect, useState } from 'react'
import { get, post } from '../api'
import { Dict } from '../i18n'

interface Project {
  slug: string
  root: string
  docs: string[]
}

interface Config {
  qdrant?: { url?: string }
  ollama?: { url?: string; model?: string }
  db?: { host?: string; port?: number | string; database?: string; user?: string; password?: string }
}

export default function SetupPage({ t }: { t: Dict }) {
  const [projects, setProjects] = useState<Project[]>([])
  const [slug, setSlug] = useState('')
  const [cfg, setCfg] = useState<Config>({})
  const [loaded, setLoaded] = useState(false)
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')

  useEffect(() => {
    get<{ projects: Project[] }>('/api/projects')
      .then((r) => setProjects(r.projects))
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (!slug) {
      setLoaded(false)
      setCfg({})
      return
    }
    setLoaded(false)
    get<Config>(`/api/config?project=${encodeURIComponent(slug)}`)
      .then((c) => {
        setCfg(c)
        setLoaded(true)
      })
      .catch((e) => setErr(String(e)))
  }, [slug])

  function setSection(section: 'qdrant' | 'ollama' | 'db', key: string, value: string) {
    setCfg((c) => ({ ...c, [section]: { ...(c[section] || {}), [key]: value } }))
  }

  async function save() {
    setErr('')
    setMsg('')
    try {
      await post('/api/config', { project: slug, ...cfg })
      setMsg(t.saved)
    } catch (e) {
      setErr(String(e))
    }
  }

  async function testDb() {
    setErr('')
    setMsg('')
    try {
      const r = await post<{ ok: boolean; error?: string }>('/api/config/test', { project: slug })
      setMsg(r.ok ? t.dbOk : `${t.dbKo} ${r.error || ''}`)
    } catch (e) {
      setErr(String(e))
    }
  }

  const q = cfg.qdrant || {}
  const o = cfg.ollama || {}
  const d = cfg.db || {}

  return (
    <div className="card">
      <h3>{t.setup}</h3>
      <p className="muted">{t.setupDesc}</p>
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

        {slug && loaded && (
          <>
            <section className="section">
              <h4>{t.qdrant}</h4>
              <div className="form-field">
                <span className="form-label">{t.url}</span>
                <input value={q.url || ''} onChange={(e) => setSection('qdrant', 'url', e.target.value)} />
              </div>
            </section>

            <section className="section">
              <h4>{t.ollama}</h4>
              <div className="form-field">
                <span className="form-label">{t.url}</span>
                <input value={o.url || ''} onChange={(e) => setSection('ollama', 'url', e.target.value)} />
              </div>
              <div className="form-field">
                <span className="form-label">{t.embeddingModel}</span>
                <input value={o.model || ''} onChange={(e) => setSection('ollama', 'model', e.target.value)} />
              </div>
            </section>

            <section className="section">
              <h4>{t.dbSection}</h4>
              <div className="grid">
                <div className="form-field">
                  <span className="form-label">{t.host}</span>
                  <input value={d.host || ''} onChange={(e) => setSection('db', 'host', e.target.value)} />
                </div>
                <div className="form-field">
                  <span className="form-label">{t.port}</span>
                  <input value={d.port ?? ''} onChange={(e) => setSection('db', 'port', e.target.value)} />
                </div>
              </div>
              <div className="form-field">
                <span className="form-label">{t.database}</span>
                <input value={d.database || ''} onChange={(e) => setSection('db', 'database', e.target.value)} />
              </div>
              <div className="form-field">
                <span className="form-label">{t.user}</span>
                <input value={d.user || ''} onChange={(e) => setSection('db', 'user', e.target.value)} />
              </div>
              <div className="form-field">
                <span className="form-label">{t.password}</span>
                <input type="password" value={d.password || ''} onChange={(e) => setSection('db', 'password', e.target.value)} />
              </div>
            </section>

            <div className="row">
              <button className="button" onClick={save}>{t.save}</button>
              <button className="button ghost" onClick={testDb}>{t.testDb}</button>
            </div>
          </>
        )}
      </div>
      {err && <p className="muted">{t.err}: {err}</p>}
      {msg && <p className="muted">{msg}</p>}
    </div>
  )
}
