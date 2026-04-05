import React from 'react'
import { Settings as SettingsIcon } from 'lucide-react'

export default function Settings() {
  return (
    <div className="space-y-6 py-4 max-w-4xl">
      <div className="flex items-center gap-4">
        <SettingsIcon className="text-emerald-400 w-8 h-8" />
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Settings</h1>
          <p className="text-slate-400 text-sm">Backend configuration via environment variables</p>
        </div>
      </div>
      <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 p-5 space-y-3 text-sm text-slate-400">
        <p><strong className="text-slate-300">HA_URL</strong> — Home Assistant URL (e.g. http://homeassistant.local:8123 or http://192.168.1.50:8123)</p>
        <p><strong className="text-slate-300">HA_TOKEN</strong> — Long-Lived Access Token (Profile in HA → Long-Lived Access Tokens → Create)</p>
        <p><strong className="text-slate-300">HA_MCP_PORT</strong> — Backend port (default 10796)</p>
      </div>
    </div>
  )
}
