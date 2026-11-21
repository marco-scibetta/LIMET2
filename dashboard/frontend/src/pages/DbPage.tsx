import { useState } from 'react'
import { post } from '../api'

interface Table {
  schema: string
  table: string
}

export default function DbPage() {
  const [tables, setTables] = useState<Table[] | null>(null)
  const [test, setTest] = useState('')
  const [err, setErr] = useState('')

  async function runTest() {
    setTest('…')
    try {
      await post('/api/db/test')
      setTest('Connessione OK')
    } catch (e) {
      setTest(`Errore: ${e}`)
    }
  }

  async function loadSchema() {
    setErr('')
    try {
      const r = await post<{ tables: Table[] }>('/api/db/schema')
      setTables(r.tables)
    } catch (e) {
      setErr(String(e))
    }
  }

  return (
    <div>
      <div className="card">
        <h3>Connessione DB (read-only)</h3>
        <p className="muted">
          Host, porta, database e utente vivono in <code>config/config.local.yaml</code> (sez.{' '}
          <code>db</code>). La password non viene mai mostrata.
        </p>
        <div className="row">
          <button className="button" onClick={runTest}>Test connessione</button>
          <button className="button" onClick={loadSchema}>Carica schema</button>
        </div>
        {test && <p className="muted">{test}</p>}
      </div>
      {err && <p className="muted">Errore: {err}</p>}
      {tables && (
        <div className="card">
          <h3>Tabelle ({tables.length})</h3>
          <table className="table">
            <thead>
              <tr>
                <th>Schema</th>
                <th>Tabella</th>
              </tr>
            </thead>
            <tbody>
              {tables.map((t, i) => (
                <tr key={i}>
                  <td>{t.schema}</td>
                  <td>{t.table}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
