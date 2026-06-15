const BASE = '/api'

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
