import { useState } from 'react'
import { createPortal } from 'react-dom'
import { get } from '../api'
import Icon from './Icon'

interface Dir {
  name: string
  path: string
}

interface BrowseResp {
  path: string
  parent: string
  dirs: Dir[]
}

interface Props {
  value: string
  onChange: (v: string) => void
  placeholder?: string
}

export default function PathInput({ value, onChange, placeholder }: Props) {
  const [open, setOpen] = useState(false)
  const [resp, setResp] = useState<BrowseResp | null>(null)
  const [err, setErr] = useState('')

  async function browse(path: string) {
    setErr('')
    try {
      const r = await get<BrowseResp>(`/api/browse?path=${encodeURIComponent(path || '')}`)
      setResp(r)
    } catch (e) {
      setErr(String(e))
    }
  }

  function openBrowser() {
    setOpen(true)
    browse(value)
  }

  return (
    <>
      <button type="button" className="pathfield" onClick={openBrowser}>
        <Icon name="folder" size={16} />
        <span className={value ? 'pathfield-value' : 'pathfield-placeholder'}>
          {value || placeholder || 'Seleziona percorso…'}
        </span>
      </button>

      {open &&
        createPortal(
          <div className="modal-backdrop" onClick={() => setOpen(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <header className="modal-head">
                <h3>Seleziona percorso</h3>
                <button className="icon-btn" onClick={() => setOpen(false)} aria-label="Chiudi">
                  ×
                </button>
              </header>

              <div className="modal-path">{resp?.path || '…'}</div>

              {err && <p className="muted" style={{ padding: '0 18px' }}>{err}</p>}

              <div className="modal-body">
                {resp && (
                  <button className="row-item parent" onClick={() => browse(resp.parent)}>
                    .. (su)
                  </button>
                )}
                {resp?.dirs.map((d) => (
                  <button key={d.path} className="row-item" onClick={() => browse(d.path)}>
                    <Icon name="folder" size={15} />
                    <span>{d.name}</span>
                  </button>
                ))}
              </div>

              <footer className="modal-foot">
                <button className="button ghost" onClick={() => setOpen(false)}>
                  Annulla
                </button>
                <button
                  className="button"
                  onClick={() => {
                    if (resp) onChange(resp.path)
                    setOpen(false)
                  }}
                >
                  Seleziona
                </button>
              </footer>
            </div>
          </div>,
          document.body,
        )}
    </>
  )
}
