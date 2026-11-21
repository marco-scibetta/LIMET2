import { useEffect, useState } from 'react'
import { get } from '../api'
import Icon from '../components/Icon'
import { Dict } from '../i18n'

interface Status {
  qdrant: boolean
  ollama: boolean
  projects: string[]
}

export default function StatusPage({ t }: { t: Dict }) {
  const [s, setS] = useState<Status | null>(null)
  const [err, setErr] = useState('')

  useEffect(() => {
    get<Status>('/api/status').then(setS).catch((e) => setErr(String(e)))
  }, [])

  if (err) return <p className="muted">{t.err}: {err}</p>
  if (!s) return <p className="muted">{t.loading}</p>

  return (
    <div>
      <div className="grid">
        <StatCard t={t} icon="db" tone="green" label="Qdrant" value={s.qdrant ? t.active : t.offline} ok={s.qdrant} />
        <StatCard t={t} icon="status" tone="blue" label="Ollama" value={s.ollama ? t.active : t.offline} ok={s.ollama} />
        <StatCard t={t} icon="projects" tone="amber" label={t.projects} value={String(s.projects.length)} />
      </div>

      <div className="card">
        <div className="card-head">
          <h3>{t.projectsTotal}</h3>
          <span className="badge ok">{s.projects.length} {t.totali}</span>
        </div>
        {s.projects.length === 0 ? (
          <p className="muted">{t.none}</p>
        ) : (
          <ul className="list">
            {s.projects.map((p) => (
              <li key={p}>{p}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

function StatCard({
  t,
  icon,
  tone,
  label,
  value,
  ok,
}: {
  t: Dict
  icon: string
  tone: 'green' | 'blue' | 'amber' | 'violet'
  label: string
  value: string
  ok?: boolean
}) {
  return (
    <div className="card stat">
      <div className={`stat-icon ${tone}`}>
        <Icon name={icon} />
      </div>
      <div className="stat-body">
        <div className="stat-label">{label}</div>
        <div className="stat-value">{value}</div>
      </div>
      {ok !== undefined && (
        <span className={ok ? 'badge ok' : 'badge ko'}>{ok ? t.online : t.offline}</span>
      )}
    </div>
  )
}
