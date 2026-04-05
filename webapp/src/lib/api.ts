const API_BASE = ''

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const url = path.startsWith('http') ? path : `${API_BASE}${path}`
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(text || `HTTP ${res.status}`)
  }
  return res.json() as Promise<T>
}

export interface Health {
  status: string
  connected: boolean
  service?: string
  timestamp?: string
}

export interface HaState {
  entity_id: string
  state: string
  attributes?: Record<string, unknown>
  last_changed?: string
  last_updated?: string
}

export interface StatesResponse {
  states?: HaState[]
}

export const api = {
  getHealth: () => request<Health>('/api/v1/health'),
  getStates: (params?: { entity_id?: string; domain?: string }) => {
    const q = new URLSearchParams()
    if (params?.entity_id) q.set('entity_id', params.entity_id)
    if (params?.domain) q.set('domain', params.domain)
    const query = q.toString()
    return request<StatesResponse | HaState>(`/api/v1/states${query ? `?${query}` : ''}`)
  },
  getConfig: () => request<Record<string, unknown>>('/api/v1/config'),
  getAutomations: () => request<{ automations: HaState[] }>('/api/v1/automations'),
  triggerAutomation: (entity_id: string) =>
    request<{ success: boolean; result?: unknown }>('/api/v1/automations/trigger', {
      method: 'POST',
      body: JSON.stringify({ entity_id }),
    }),
  callService: (domain: string, service: string, body?: Record<string, unknown>) =>
    request<unknown[]>(`/api/v1/services/${domain}/${service}`, {
      method: 'POST',
      body: JSON.stringify(body || {}),
    }),
}
