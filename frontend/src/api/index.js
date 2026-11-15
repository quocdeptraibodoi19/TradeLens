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

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.status = status
  }
}

async function getJson(url, options) {
  const res = await fetch(url, options)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new ApiError(err.detail || `Request failed: ${res.status}`, res.status)
  }
  return res.json()
}

export function fetchAccountOverview() {
  return getJson(`${BASE}/dashboard/account_overview`)
}

export function fetchHoldings(limit = 5, offset = 0) {
  const params = new URLSearchParams({ limit, offset })
  return getJson(`${BASE}/dashboard/holdings?${params}`)
}

export function syncDashboard() {
  return getJson(`${BASE}/dashboard/sync`, { method: 'POST' })
}

export function logout() {
  return getJson(`${AUTH}/logout`, { method: 'POST' })
}

export function fetchMe() {
  return getJson(`${AUTH}/me`)
}
