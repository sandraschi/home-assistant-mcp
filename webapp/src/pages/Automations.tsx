import React, { useState, useEffect, useCallback } from 'react'
import { ListTodo, RefreshCw, PlayCircle, Loader2, AlertCircle } from 'lucide-react'
import { api, type HaState } from '../lib/api'

export default function Automations() {
  const [automations, setAutomations] = useState<HaState[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [triggering, setTriggering] = useState<string | null>(null)

  const fetchAutomations = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await api.getAutomations()
      setAutomations(res.automations ?? [])
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load automations')
      setAutomations([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchAutomations()
  }, [fetchAutomations])

  const trigger = async (entity_id: string) => {
    setTriggering(entity_id)
    try {
      await api.triggerAutomation(entity_id)
    } catch {
      setError('Trigger failed')
    } finally {
      setTriggering(null)
    }
  }

  return (
    <div className="space-y-6 py-4 max-w-4xl">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <ListTodo className="text-emerald-400 w-8 h-8" />
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Automations</h1>
            <p className="text-slate-400 text-sm">List and trigger Home Assistant automations</p>
          </div>
        </div>
        <button
          type="button"
          onClick={fetchAutomations}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 rounded-xl border border-white/10 bg-white/5 text-slate-400 hover:text-slate-200 text-sm disabled:opacity-50"
        >
          <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          Refresh
        </button>
      </div>

      {error && (
        <div className="flex items-center gap-3 p-4 rounded-2xl border border-amber-500/20 bg-amber-500/10 text-amber-200">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <p className="text-sm">{error}</p>
        </div>
      )}

      {loading && !automations.length && (
        <div className="flex justify-center py-12">
          <RefreshCw className="w-8 h-8 animate-spin text-emerald-400" />
        </div>
      )}

      {!loading && (
        <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 overflow-hidden">
          <ul className="divide-y divide-white/5">
            {automations.map((a) => (
              <li key={a.entity_id} className="flex items-center justify-between px-4 py-3 hover:bg-white/5">
                <div>
                  <p className="font-mono text-sm text-slate-200">{a.entity_id}</p>
                  <p className="text-xs text-slate-500">State: {a.state}</p>
                </div>
                <button
                  type="button"
                  onClick={() => trigger(a.entity_id)}
                  disabled={triggering !== null}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 text-xs hover:bg-emerald-500/30 disabled:opacity-50"
                >
                  {triggering === a.entity_id ? <Loader2 size={12} className="animate-spin" /> : <PlayCircle size={12} />}
                  Trigger
                </button>
              </li>
            ))}
          </ul>
          {automations.length === 0 && !loading && (
            <p className="p-4 text-sm text-slate-500">No automation entities found.</p>
          )}
        </div>
      )}
    </div>
  )
}
