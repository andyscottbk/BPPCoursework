import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import { vi } from 'vitest'
import App from './App'

describe('App component', () => {

  beforeEach(() => {
    global.fetch = vi.fn()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  test('renders the application title', () => {
    global.fetch = vi.fn(() => new Promise(() => {}))
    render(<App />)
    expect(screen.getByTestId('app-title')).toBeInTheDocument()
    expect(screen.getByTestId('app-title').textContent).toBe('BPM Application')
  })

  test('shows loading state initially', () => {
    global.fetch = vi.fn(() => new Promise(() => {}))
    render(<App />)
    expect(screen.getByTestId('loading-message')).toBeInTheDocument()
  })

  test('displays status data when API responds successfully', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({
          application: 'bpm-frontend',
          status: 'operational',
          environment: 'production'
        })
      })
    )
    render(<App />)
    await waitFor(() => {
      expect(screen.getByTestId('status-panel')).toBeInTheDocument()
    })
    expect(screen.getByTestId('status-application').textContent).toBe('bpm-frontend')
    expect(screen.getByTestId('status-value').textContent).toBe('operational')
    expect(screen.getByTestId('status-environment').textContent).toBe('production')
  })

  test('displays error message when API call fails', async () => {
    global.fetch = vi.fn(() => Promise.reject(new Error('Network error')))
    render(<App />)
    await waitFor(() => {
      expect(screen.getByTestId('error-message')).toBeInTheDocument()
    })
    expect(screen.getByTestId('error-message').textContent).toBe('Unable to reach API')
  })

  test('does not render status panel when loading', () => {
    global.fetch = vi.fn(() => new Promise(() => {}))
    render(<App />)
    expect(screen.queryByTestId('status-panel')).not.toBeInTheDocument()
  })

})
