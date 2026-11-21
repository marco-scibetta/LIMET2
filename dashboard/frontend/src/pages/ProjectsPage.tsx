import { useEffect, useState } from 'react'
import { get, post } from '../api'
import { Dict } from '../i18n'

interface Project {
  slug: string
  docs: string[]
  root: string
  collections: string[]
}

export default function ProjectsPage({ t }: { t: Dict }) {
  const [p, setP] = useState<Project[] | null>(null)
  const [err, setErr] = useState('')
  const [a, setA] = useState('')
  const [b, setB] = useState('')
  const [msg, setMsg] = useState('')

  function load() {
    get<{ projects: Project[] }>('/api/projects')
      .then((r) => setP(r.projects))
      .catch((e) => setErr(String(e)))
  }

  useEffect(load, [])

  async function link() {
    setErr('')
    setMsg('')
    if (!a || !b || a === b) {
      setErr(t.pickTwo)
      return
    }
    try {
      const r = await post<{ linked: string[] }>('/api/link', { a, b })
      setMsg(`${t.linked} ${r.linked.join(' · ')}`)
      load()
    } catch (e) {
      setErr(String(e))
    }
  }

  async function unlink() {
    setErr('')
    setMsg('')
    if (!a || !b || a === b) {
      setErr(t.pickTwo)
      return
    }
    try {
      await post('/api/unlink', { a, b })
      setMsg(t.unlinked)
      load()
    } catch (e) {
      setErr(String(e))
    }
  }

  if (err) return <p className="muted">{t.err}: {err}</p>
  if (!p) return <p className="muted">{t.loading}</p>

  return (
    <div>
      <div className="card">
        <h3>{t.projectsCount} ({p.length})</h3>
        {p.length === 0 ? (
          <p className="muted">{t.noProjects}</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>{t.thSlug}</th>
                <th>{t.thRoot}</th>
                <th>{t.thDocs}</th>
                <th>{t.thCollections}</th>
              </tr>
            </thead>
            <tbody>
              {p.map((x) => (
                <tr key={x.slug}>
                  <td>{x.slug}</td>
                  <td>{x.root}</td>
                  <td>{x.docs.join(', ')}</td>
                  <td>{x.collections?.join(', ') || '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {p && p.length >= 2 && (
        <div className="card">
          <h3>{t.linkTitle}</h3>
          <p className="muted">{t.linkDesc}</p>
          <div className="form">
            <div className="form-field">
              <span className="form-label">{t.projectA}</span>
              <select value={a} onChange={(e) => setA(e.target.value)}>
                <option value="">{t.select}</option>
                {p.map((x) => (
                  <option key={x.slug} value={x.slug}>{x.slug}</option>
                ))}
              </select>
            </div>
            <div className="form-field">
              <span className="form-label">{t.projectB}</span>
              <select value={b} onChange={(e) => setB(e.target.value)}>
                <option value="">{t.select}</option>
                {p.map((x) => (
                  <option key={x.slug} value={x.slug}>{x.slug}</option>
                ))}
              </select>
            </div>
            <div className="row">
              <button className="button" onClick={link}>{t.link}</button>
              <button className="button ghost" onClick={unlink}>{t.unlink}</button>
            </div>
          </div>
          {msg && <p className="muted">{msg}</p>}
        </div>
      )}
    </div>
  )
}
