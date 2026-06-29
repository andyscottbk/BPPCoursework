import React, { useState, useEffect } from 'react'

function App() {
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/status')
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(() => setError('Unable to reach API'))
  }, [])

  return (
    <main style={{ maxWidth: 640, margin: '60px auto', padding: '0 24px' }}>
      <h1 data-testid="app-title">BPM Application</h1>
      <p style={{ marginTop: 8, color: '#4a5568' }}>
        Business Process Management — Secure Internal Platform
      </p>

      <section style={{ marginTop: 32 }}>
        <h2>System Status</h2>
        {error && (
          <p data-testid="error-message" style={{ color: '#e53e3e', marginTop: 8 }}>
            {error}
          </p>
        )}
        {status && (
          <dl data-testid="status-panel" style={{ marginTop: 12 }}>
            <div style={{ display: 'flex', gap: 8, marginBottom: 4 }}>
              <dt style={{ fontWeight: 600 }}>Application:</dt>
              <dd data-testid="status-application">{status.application}</dd>
            </div>
            <div style={{ display: 'flex', gap: 8, marginBottom: 4 }}>
              <dt style={{ fontWeight: 600 }}>Status:</dt>
              <dd data-testid="status-value">{status.status}</dd>
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              <dt style={{ fontWeight: 600 }}>Environment:</dt>
              <dd data-testid="status-environment">{status.environment}</dd>
            </div>
          </dl>
        )}
        {!status && !error && (
          <p data-testid="loading-message" style={{ marginTop: 8, color: '#718096' }}>Loading...</p>
        )}
      </section>
    </main>
  )
}

export default App
