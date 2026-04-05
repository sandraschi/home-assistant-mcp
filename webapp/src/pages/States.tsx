import React, { useState, useEffect, useCallback } from 'react'
import { Layers, RefreshCw, AlertCircle } from 'lucide-react'
import { api, type HaState } from '../lib/api'

const DOMAINS = ['', 'light', 'switch', 'vacuum', 'climate', 'sensor', 'binary_sensor', 'automation', 'script', 'cover', 'media_player']

export default function States() {
  const [states, setStates] = useState<HaState[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [domain, setDomain] = useState('')

  const fetchStates = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.getStates(domain ? { domain } : undefined)
      const list = Array.isArray(res)
        ? res
        : (res as { states?: HaState[] }).states ?? ((res as HaState).entity_id ? [res as HaState] : [])
      setStates(list)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load states')
      setStates([])
    } finally {
      setLoading(false)
    }
  }, [domain])

  useEffect(() => {
    fetchStates()
  }, [fetchStates])

  return (
    <div className="space-y-6 py-4 max-w-5xl mx-auto">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-4">
          <Layers className="text-emerald-400 w-8 h-8" />
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">States</h1>
            <p className="text-slate-400 text-sm">Entity states from Home Assistant</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            className="bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-sm text-slate-200"
          >
            {DOMAINS.map((d) => (
              <option key={d} value={d}>{d || 'All domains'}</option>
            ))}
          </select>
          <button
            type="button"
            onClick={fetchStates}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 rounded-xl border border-white/10 bg-white/5 text-slate-400 hover:text-slate-200 text-sm disabled:opacity-50"
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            Refresh
          </button>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-3 p-4 rounded-2xl border border-amber-500/20 bg-amber-500/10 text-amber-200">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <p className="text-sm">{error}</p>
        </div>
      )}

      {loading && (
        <div className="flex justify-center py-12">
          <RefreshCw className="w-8 h-8 animate-spin text-emerald-400" />
        </div>
      )}

      {!loading && !error && (
        <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 overflow-hidden">
          <div className="overflow-x-auto max-h-[70vh]">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-[#0f0f12] border-b border-white/10">
                <tr className="text-left text-slate-500">
                  <th className="px-4 py-3 font-medium">Entity</th>
                  <th className="px-4 py-3 font-medium">State</th>
                </tr>
              </thead>
              <tbody>
                {states.map((s) => (
                  <tr key={s.entity_id} className="border-b border-white/5 hover:bg-white/5">
                    <td className="px-4 py-2 font-mono text-slate-300">{s.entity_id}</td>
                    <td className="px-4 py-2 text-slate-400">{s.state}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="p-2 text-xs text-slate-500 border-t border-white/5">{states.length} entities</p>
        </div>
      )}
    </div>
  )
}
