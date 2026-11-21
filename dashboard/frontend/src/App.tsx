import { useState } from 'react'
import Icon from './components/Icon'
import StatusPage from './pages/StatusPage'
import InitPage from './pages/InitPage'
import ProjectsPage from './pages/ProjectsPage'
import ReindexPage from './pages/ReindexPage'
import DbPage from './pages/DbPage'

const NAV = [
  { id: 'status', label: 'Status', desc: 'Stato di Qdrant, Ollama e progetti registrati.' },
  { id: 'init', label: 'Init', desc: 'Registra un nuovo progetto in CEREBRO.' },
  { id: 'projects', label: 'Progetti', desc: 'Progetti registrati e percorsi docs.' },
  { id: 'reindex', label: 'Re-index', desc: 'Re-indicizzazione incrementale, forzata o pulizia.' },
  { id: 'db', label: 'Config DB', desc: 'Connessione read-only e schema del database.' },
] as const

type PageId = (typeof NAV)[number]['id']

export default function App() {
  const [page, setPage] = useState<PageId>('status')
  const current = NAV.find((n) => n.id === page)!

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark" />
          <span>LIMET</span>
        </div>
        <div className="nav-group">Operazioni</div>
        <nav>
          {NAV.map((n) => (
            <button
              key={n.id}
              className={page === n.id ? 'nav active' : 'nav'}
              onClick={() => setPage(n.id)}
            >
              <Icon name={n.id} />
              <span>{n.label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-foot">
          <span className="badge ok">v2.0.0</span>
        </div>
      </aside>

      <div className="main">
        <header className="topbar">
          <h1>{current.label}</h1>
          <p>{current.desc}</p>
        </header>
        <main className="content">
          {page === 'status' && <StatusPage />}
          {page === 'init' && <InitPage />}
          {page === 'projects' && <ProjectsPage />}
          {page === 'reindex' && <ReindexPage />}
          {page === 'db' && <DbPage />}
        </main>
      </div>
    </div>
  )
}
