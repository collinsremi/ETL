import { useState } from 'react'
import { supabase } from './supabase'

export default function Auth({ onLogin }) {
  const [mode, setMode] = useState('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const handleSubmit = async () => {
    setError('')
    setMessage('')
    if (!email || !password) {
      setError('Please fill in all fields.')
      return
    }
    setLoading(true)
    if (mode === 'register') {
      const { error } = await supabase.auth.signUp({
        email,
        password,
        options: { data: { full_name: name } }
      })
      if (error) setError(error.message)
      else setMessage('Account created! Please check your email to confirm.')
    } else {
      const { data, error } = await supabase.auth.signInWithPassword({ email, password })
      if (error) setError(error.message)
      else onLogin(data.user)
    }
    setLoading(false)
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <div className="auth-logo">AIREME</div>
        <div className="auth-tagline">AI Real Estate Marketing Engine</div>
        <div className="auth-tabs">
          <button className={`auth-tab ${mode === 'login' ? 'active' : ''}`}
            onClick={() => { setMode('login'); setError(''); setMessage('') }}>
            Sign In
          </button>
          <button className={`auth-tab ${mode === 'register' ? 'active' : ''}`}
            onClick={() => { setMode('register'); setError(''); setMessage('') }}>
            Register
          </button>
        </div>
        {mode === 'register' && (
          <div className="auth-group">
            <label>Full Name</label>
            <input type="text" placeholder="e.g. John Adeyemi"
              value={name} onChange={e => setName(e.target.value)} />
          </div>
        )}
        <div className="auth-group">
          <label>Email Address</label>
          <input type="email" placeholder="you@example.com"
            value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div className="auth-group">
          <label>Password</label>
          <input type="password" placeholder="••••••••"
            value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        {error && <div className="auth-error">{error}</div>}
        {message && <div className="auth-message">{message}</div>}
        <button className="auth-btn" onClick={handleSubmit} disabled={loading}>
          {loading ? 'Please wait...' : mode === 'login' ? 'Sign In' : 'Create Account'}
        </button>
      </div>
    </div>
  )
}