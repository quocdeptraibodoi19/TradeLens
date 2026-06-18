const BASE = '/api'
const AUTH = '/auth'

export async function register(firstName, lastName, email, password) {
  const res = await fetch(`${AUTH}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ first_name: firstName, last_name: lastName, email, password }),
  })
  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.detail || 'Registration failed')
  }
  return res.json()
}

export async function login(email, password) {
  const res = await fetch(`${AUTH}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email, password }),
  })
  if (!res.ok) {
    const err = await res.json()
    throw new Error(err.detail || 'Login failed')
  }
  return res.json()
}

export async function fetchOrders() {
  const res = await fetch(`${BASE}/orders`)
  if (!res.ok) throw new Error(`Failed to fetch orders: ${res.status}`)
  return res.json()
}

export async function fetchAlerts() {
  const res = await fetch(`${BASE}/alerts`)
  if (!res.ok) throw new Error(`Failed to fetch alerts: ${res.status}`)
  return res.json()
}

export async function fetchSymbols() {
  const res = await fetch(`${BASE}/symbols`)
  if (!res.ok) throw new Error(`Failed to fetch symbols: ${res.status}`)
  return res.json()
}
