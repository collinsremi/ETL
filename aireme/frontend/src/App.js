import { useState, useEffect } from 'react'
import { supabase } from './supabase'
import Auth from './Auth'
import Flyer from './Flyer'
import History from './History'
import './App.css'

const SECTIONS = [
  { key: 'listing', label: 'Listing Description', marker: 'LISTING DESCRIPTION' },
  { key: 'instagram', label: 'Instagram Caption', marker: 'INSTAGRAM CAPTION' },
  { key: 'video', label: 'Video Script', marker: 'VIDEO SCRIPT' },
]

function parseOutput(raw) {
  const result = {}
  SECTIONS.forEach((section, i) => {
    const start = raw.indexOf(`**${section.marker}**`)
    const nextMarker = SECTIONS[i + 1]
      ? raw.indexOf(`**${SECTIONS[i + 1].marker}**`)
      : raw.length
    if (start !== -1) {
      result[section.key] = raw.slice(start + section.marker.length + 4, nextMarker).trim()
    }
  })
  return result
}

export default function App() {
  const [user, setUser] = useState(null)
  const [checking, setChecking] = useState(true)
  const [form, setForm] = useState({
    property_type: '', location: '', price: '', features: '', target_buyer: ''
  })
  const [loading, setLoading] = useState(false)
  const [output, setOutput] = useState(null)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState('')

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setChecking(false)
    })
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })
    return () => subscription.unsubscribe()
  }, [])

  const handleLogout = async () => {
    await supabase.auth.signOut()
    setOutput(null)
  }

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleGenerate = async () => {
    if (!form.property_type || !form.location || !form.price) {
      setError('Please fill in at least Property Type, Location and Price.')
      return
    }
    setError('')
    setOutput(null)
    setLoading(true)
    try {
      const res = await fetch('http://127.0.0.1:8000/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, user_id: user.id }),
      })
      const data = await res.json()
      setOutput(parseOutput(data.output))
    } catch (err) {
      setError('Could not connect to backend. Make sure it is running.')
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = (text, key) => {
    navigator.clipboard.writeText(text)
    setCopied(key)
    setTimeout(() => setCopied(''), 2000)
  }

  if (checking) return (
    <div className="auth-wrapper">
      <div style={{ color: 'var(--gold)', letterSpacing: '4px', fontSize: '12px' }}>LOADING...</div>
    </div>
  )

  if (!user) return <Auth onLogin={setUser} />

  return (
    <div className="app">
      <header className="header">
        <div className="logo">AIREME</div>
        <div className="tagline">AI Real Estate Marketing Engine</div>
        <div className="user-bar">
          <span className="user-email">{user.email}</span>
          <button className="logout-btn" onClick={handleLogout}>Sign Out</button>
        </div>
      </header>

      <History
        userId={user.id}
        onRestore={(item) => {
          setForm({
            property_type: item.property_type,
            location: item.location,
            price: item.price,
            features: item.features,
            target_buyer: item.target_buyer,
          })
          setOutput(null)
          window.scrollTo({ top: 0, behavior: 'smooth' })
        }}
      />

      <div className="form-card">
        <div className="form-title">Property Details</div>
        <div className="form-grid">
          <div className="form-group">
            <label>Property Type</label>
            <input name="property_type" placeholder="e.g. 3 Bedroom Apartment"
              value={form.property_type} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label>Location</label>
            <input name="location" placeholder="e.g. Lekki Phase 1, Lagos"
              value={form.location} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label>Price</label>
            <input name="price" placeholder="e.g. ₦85,000,000"
              value={form.price} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label>Target Buyer</label>
            <input name="target_buyer" placeholder="e.g. Young professionals"
              value={form.target_buyer} onChange={handleChange} />
          </div>
          <div className="form-group full">
            <label>Key Features</label>
            <textarea name="features" rows={3}
              placeholder="e.g. Swimming pool, 24/7 power, fitted kitchen, boys quarters"
              value={form.features} onChange={handleChange} />
          </div>
        </div>
        {error && <div className="error">{error}</div>}
        <button className="generate-btn" onClick={handleGenerate} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Marketing Content'}
        </button>
      </div>

      {loading && (
        <div className="loading">
          <div>
            <span className="loading-dot" />
            <span className="loading-dot" />
            <span className="loading-dot" />
          </div>
          <p>AI is writing your content</p>
        </div>
      )}

      {output && (
        <div className="results">
          {SECTIONS.map((section) => (
            output[section.key] && (
              <div className="result-card" key={section.key}>
                <div className="result-header">
                  <span className="result-label">{section.label}</span>
                  <div className="result-actions">
                    <button className="copy-btn"
                      onClick={() => handleCopy(output[section.key], section.key)}>
                      {copied === section.key ? '✓ Copied' : 'Copy'}
                    </button>
                    {section.key === 'instagram' && (
                      <a className="whatsapp-btn"
                        href={`https://wa.me/?text=${encodeURIComponent(output[section.key])}`}
                        target="_blank" rel="noreferrer">
                        WhatsApp
                      </a>
                    )}
                  </div>
                </div>
                <div className="result-body">{output[section.key]}</div>
              </div>
            )
          ))}
        </div>
      )}

      {output && <Flyer data={form} output={output} />}
    </div>
  )
}