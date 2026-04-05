import React, { useEffect, useState } from 'react'
import { Home, Activity, AlertCircle } from 'lucide-react'
import { api, type Health } from '../lib/api'

export default function Dashboard() {
  const [health, setHealth] = useState<Health | null>(null)
  const [err, setErr] = useState<string | null>(null)

  useEffect(() => {
    api.getHealth().then(setHealth).catch((e) => setErr(e.message))
    const t = setInterval(() => api.getHealth().then(setHealth).catch(() => {}), 5000)
    return () => clearInterval(t)
  }, [])

  return (
    <div className="space-y-6 py-4 max-w-4xl">
      <div className="flex items-center gap-4">
        <Home className="text-emerald-400 w-8 h-8" />
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Dashboard</h1>
          <p className="text-slate-400 text-sm">Home Assistant at a glance</p>
        </div>
      </div>

      {err && (
        <div className="flex items-center gap-3 p-4 rounded-2xl border border-amber-500/20 bg-amber-500/10 text-amber-200">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <p className="text-sm">{err}. Run webapp\\start.ps1 and set HA_URL and HA_TOKEN.</p>
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 p-5">
          <div className="flex items-center gap-3 mb-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            <h2 className="text-sm font-bold text-slate-200">Backend</h2>
          </div>
          <p className="text-2xl font-bold text-white">{health?.status === 'ok' ? 'OK' : '—'}</p>
          <p className="text-xs text-slate-500 mt-1">Service: {health?.service ?? '—'}</p>
        </div>
        <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 p-5">
          <div className="flex items-center gap-3 mb-2">
            <Home className="w-5 h-5 text-emerald-400" />
            <h2 className="text-sm font-bold text-slate-200">Home Assistant</h2>
          </div>
          <p className="text-2xl font-bold text-white">{health?.connected ? 'Connected' : 'Not connected'}</p>
          <p className="text-xs text-slate-500 mt-1">HA_TOKEN and HA_URL required</p>
        </div>
      </div>

      <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 p-5">
        <h2 className="text-sm font-bold text-slate-200 mb-3">Quick links</h2>
        <div className="flex flex-wrap gap-3">
          <a href="/states" className="px-4 py-2 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-sm hover:bg-emerald-500/20">States</a>
          <a href="/services" className="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 text-sm hover:bg-white/10">Services</a>
          <a href="/automations" className="px-4 py-2 rounded-xl bg-white/5 border border-white/10 text-slate-300 text-sm hover:bg-white/10">Automations</a>
        </div>
      </div>
    </div>
  )
}
