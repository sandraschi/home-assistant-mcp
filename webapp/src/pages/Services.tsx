import React, { useState } from 'react'
import { PlayCircle, Loader2, AlertCircle, Check } from 'lucide-react'
import { api } from '../lib/api'

const COMMON_SERVICES: { domain: string; service: string; label: string; entity_id?: string }[] = [
  { domain: 'light', service: 'turn_on', label: 'Light on', entity_id: '' },
  { domain: 'light', service: 'turn_off', label: 'Light off', entity_id: '' },
  { domain: 'vacuum', service: 'start', label: 'Vacuum start', entity_id: '' },
  { domain: 'vacuum', service: 'return_to_base', label: 'Vacuum dock', entity_id: '' },
  { domain: 'climate', service: 'set_temperature', label: 'Set temp', entity_id: '' },
]

export default function Services() {
  const [domain, setDomain] = useState('light')
  const [service, setService] = useState('turn_on')
  const [entityId, setEntityId] = useState('')
  const [loading, setLoading] = useState(false)
  const [msg, setMsg] = useState<{ type: 'ok' | 'err'; text: string } | null>(null)

  const call = async (dom?: string, svc?: string, eid?: string) => {
    const d = dom ?? domain
    const s = svc ?? service
    const e = eid ?? entityId
    setLoading(true)
    setMsg(null)
    try {
      await api.callService(d, s, e ? { entity_id: e } : undefined)
      setMsg({ type: 'ok', text: `Called ${d}.${s}` })
    } catch (err) {
      setMsg({ type: 'err', text: err instanceof Error ? err.message : 'Failed' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6 py-4 max-w-4xl">
      <div className="flex items-center gap-4">
        <PlayCircle className="text-emerald-400 w-8 h-8" />
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Services</h1>
          <p className="text-slate-400 text-sm">Call Home Assistant services</p>
        </div>
      </div>

      {msg && (
        <div className={`flex items-center gap-3 p-4 rounded-2xl border ${msg.type === 'ok' ? 'border-green-500/20 bg-green-500/10 text-green-200' : 'border-amber-500/20 bg-amber-500/10 text-amber-200'}`}>
          {msg.type === 'err' && <AlertCircle className="w-5 h-5 flex-shrink-0" />}
          {msg.type === 'ok' && <Check className="w-5 h-5 flex-shrink-0" />}
          <p className="text-sm">{msg.text}</p>
        </div>
      )}

      <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 p-5 space-y-4">
        <h2 className="text-sm font-bold text-slate-200">Custom call</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs text-slate-500 mb-1">Domain</label>
            <input
              type="text"
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-slate-200 text-sm"
              placeholder="light"
            />
          </div>
          <div>
            <label className="block text-xs text-slate-500 mb-1">Service</label>
            <input
              type="text"
              value={service}
              onChange={(e) => setService(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-slate-200 text-sm"
              placeholder="turn_on"
            />
          </div>
          <div className="sm:col-span-2">
            <label className="block text-xs text-slate-500 mb-1">Entity ID (optional)</label>
            <input
              type="text"
              value={entityId}
              onChange={(e) => setEntityId(e.target.value)}
              className="w-full bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-slate-200 text-sm font-mono"
              placeholder="light.living_room"
            />
          </div>
        </div>
        <button
          type="button"
          onClick={() => call()}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 text-sm hover:bg-emerald-500/30 disabled:opacity-50"
        >
          {loading ? <Loader2 size={14} className="animate-spin" /> : <PlayCircle size={14} />}
          Call service
        </button>
      </div>

      <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 p-5">
        <h2 className="text-sm font-bold text-slate-200 mb-3">Quick actions</h2>
        <p className="text-xs text-slate-500 mb-3">Set entity_id in States, then use these or add entity_id when calling.</p>
        <div className="flex flex-wrap gap-2">
          {COMMON_SERVICES.map((s) => (
            <button
              key={`${s.domain}.${s.service}`}
              type="button"
              onClick={() => call(s.domain, s.service, entityId || undefined)}
              disabled={loading}
              className="px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-slate-300 text-xs hover:bg-white/10 disabled:opacity-50"
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
