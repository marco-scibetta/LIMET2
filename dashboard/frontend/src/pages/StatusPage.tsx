import { useEffect, useState } from 'react'
import { get } from '../api'
import Icon from '../components/Icon'

interface Status {
  qdrant: boolean
  ollama: boolean
  projects: string[]
}

export default function StatusPage() {
  const [s, setS] = useState<Status | null>(null)
  const [err, setErr] = useState('')

  useEffect(() => {
    get<Status>('/api/status').then(setS).catch((e) => setErr(String(e)))
  }, [])

  if (err) return <p className="muted">Errore: {err}</p>
  if (!s) return <p className="muted">Caricamento…</p>

  return (
    <div>
      <div className="grid">
        <StatCard
          icon="db"
          tone="green"
          label="Qdrant"
          value={s.qdrant ? 'Attivo' : 'Offline'}
          ok={s.qdrant}
        />
        <StatCard
          icon="status"
          tone="blue"
          label="Ollama"
          value={s.ollama ? 'Attivo' : 'Offline'}
          ok={s.ollama}
        />
        <StatCard icon="projects" tone="amber" label="Progetti" value={String(s.projects.length)} />
      </div>

      <div className="card">
        <div className="card-head">
          <h3>Progetti registrati</h3>
          <span className="badge ok">{s.projects.length} totali</span>
        </div>
        {s.projects.length === 0 ? (
          <p className="muted">Nessuno</p>
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
  icon,
  tone,
  label,
  value,
  ok,
}: {
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
        <span className={ok ? 'badge ok' : 'badge ko'}>{ok ? 'online' : 'offline'}</span>
      )}
    </div>
  )
}
