import { useState } from 'react'

export default function History({ userId, onRestore }) {
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)

  const fetchHistory = async () => {
    setLoading(true)
    try {
      const res = await fetch(`http://127.0.0.1:8000/history/${userId}`)
      const data = await res.json()
      setHistory(data.history || [])
    } catch (err) {
      console.error(err)
    }
    setLoading(false)
  }

  const handleOpen = () => {
    setOpen(!open)
    if (!open) fetchHistory()
  }

  const formatDate = (dateStr) => {
    const d = new Date(dateStr)
    return d.toLocaleDateString('en-NG', {
      day: 'numeric', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit'
    })
  }

  return (
    <div className="history-wrapper">
      <button className="history-toggle-btn" onClick={handleOpen}>
        {open ? '✕ Close History' : '🕒 My Past Generations'}
      </button>
      {open && (
        <div className="history-panel">
          {loading && (
            <div className="history-loading">
              <span className="loading-dot" />
              <span className="loading-dot" />
              <span className="loading-dot" />
            </div>
          )}
          {!loading && history.length === 0 && (
            <div className="history-empty">No generations yet. Generate your first listing above!</div>
          )}
          {!loading && history.map((item, i) => (
            <div key={i} className="history-item">
              <div className="history-item-header">
                <div className="history-item-info">
                  <div className="history-item-title">{item.property_type} — {item.location}</div>
                  <div className="history-item-meta">{item.price} · {formatDate(item.created_at)}</div>
                </div>
                <button className="history-restore-btn" onClick={() => onRestore(item)}>
                  Restore
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}