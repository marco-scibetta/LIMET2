import { useEffect, useState } from 'react'
import Icon from './components/Icon'
import { post } from './api'
import StatusPage from './pages/StatusPage'
import InitPage from './pages/InitPage'
import ProjectsPage from './pages/ProjectsPage'
import ReindexPage from './pages/ReindexPage'
import SetupPage from './pages/SetupPage'
import { T, Lang } from './i18n'

const NAV = [
  { id: 'status', label: 'status', desc: 'descStatus' },
  { id: 'init', label: 'init', desc: 'descInit' },
  { id: 'projects', label: 'projects', desc: 'descProjects' },
  { id: 'reindex', label: 'reindex', desc: 'descReindex' },
  { id: 'setup', label: 'setup', desc: 'descSetup' },
] as const

type PageId = (typeof NAV)[number]['id']

export default function App() {
  const [page, setPage] = useState<PageId>('status')
  const [lang, setLang] = useState<Lang>(() => {
    try {
      return (localStorage.getItem('limet-lang') as Lang) || 'it'
    } catch {
      return 'it'
    }
  })

  useEffect(() => {
    try {
      localStorage.setItem('limet-lang', lang)
    } catch {
      /* ignore */
    }
  }, [lang])

  function toggleLang() {
    const next: Lang = lang === 'it' ? 'en' : 'it'
    setLang(next)
    post('/api/language', { lang: next }).catch(() => {})
  }

  const t = T[lang]
  const current = NAV.find((n) => n.id === page)!

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark" />
          <span>LIMET</span>
        </div>
        <div className="nav-group">{lang === 'it' ? 'Operazioni' : 'Operations'}</div>
        <nav>
          {NAV.map((n) => (
            <button
              key={n.id}
              className={page === n.id ? 'nav active' : 'nav'}
              onClick={() => setPage(n.id)}
            >
              <Icon name={n.id} />
              <span>{t[n.label]}</span>
            </button>
          ))}
        </nav>
        <div className="nav-group">{t.docs}</div>
        <nav>
          <a className="nav" href={`/docs/setup?lang=${lang}`} target="_blank" rel="noopener noreferrer">
            <Icon name="book" />
            <span>{t.docsSetup}</span>
          </a>
          <a className="nav" href={`/docs/project-init?lang=${lang}`} target="_blank" rel="noopener noreferrer">
            <Icon name="book" />
            <span>{t.docsProjectInit}</span>
          </a>
          <a className="nav" href={`/docs/workflow?lang=${lang}`} target="_blank" rel="noopener noreferrer">
            <Icon name="book" />
            <span>{t.docsWorkflow}</span>
          </a>
        </nav>
        <div className="sidebar-foot">
          <span className="badge ok">v2.0.0</span>
        </div>
      </aside>

      <div className="main">
        <header className="topbar">
          <div className="title">
            <h1>{t[current.label]}</h1>
            <p>{t[current.desc]}</p>
          </div>
          <button
            className="lang-btn"
            onClick={toggleLang}
            title={lang === 'it' ? 'Switch to English' : 'Passa a italiano'}
          >
            {lang === 'it' ? '🇮🇹' : '🇬🇧'}
          </button>
        </header>
        <main className="content">
          {page === 'status' && <StatusPage t={t} />}
          {page === 'init' && <InitPage t={t} />}
          {page === 'projects' && <ProjectsPage t={t} />}
          {page === 'reindex' && <ReindexPage t={t} />}
          {page === 'setup' && <SetupPage t={t} />}
        </main>
      </div>
    </div>
  )
}
