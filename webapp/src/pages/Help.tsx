import React, { useState } from 'react'
import { HelpCircle, Package, Play, Wifi, AlertTriangle, ExternalLink } from 'lucide-react'

const tabs = [
  { id: 'overview', label: 'Overview', icon: Package },
  { id: 'quickstart', label: 'Quick Start', icon: Play },
  { id: 'connection', label: 'Connection', icon: Wifi },
  { id: 'trouble', label: 'Troubleshooting', icon: AlertTriangle },
]

export default function Help() {
  const [tab, setTab] = useState('overview')

  return (
    <div className="space-y-6 py-4 max-w-4xl">
      <div className="flex items-center gap-4">
        <HelpCircle className="text-emerald-400 w-8 h-8" />
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Help</h1>
          <p className="text-slate-400 text-sm">Home Assistant MCP server and dashboard</p>
        </div>
      </div>

      <div className="flex gap-1 p-1 bg-white/5 border border-white/5 rounded-2xl w-fit">
        {tabs.map((t) => (
          <button
            key={t.id}
            type="button"
            onClick={() => setTab(t.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-widest transition-all ${
              tab === t.id ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/30' : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            <t.icon size={13} />
            <span className="hidden sm:inline">{t.label}</span>
          </button>
        ))}
      </div>

      <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 p-5 space-y-4 text-sm text-slate-400">
        {tab === 'overview' && (
          <>
            <h3 className="text-slate-200 font-bold">Home Assistant MCP</h3>
            <p>Control and query Home Assistant from AI clients and this dashboard. Tools: ha(operation=&quot;get_states&quot;), ha(operation=&quot;call_service&quot;, domain=..., service=...), ha(operation=&quot;trigger_automation&quot;, entity_id=...). Use ha_agentic_workflow(goal=&quot;...&quot;) for multi-step goals.</p>
          </>
        )}
        {tab === 'quickstart' && (
          <>
            <h3 className="text-slate-200 font-bold">Quick Start</h3>
            <ol className="list-decimal list-inside space-y-2">
              <li>In HA: Profile → Long-Lived Access Tokens → Create token. Copy it.</li>
              <li>Set HA_URL (e.g. http://192.168.1.50:8123) and HA_TOKEN. Run webapp\\start.ps1.</li>
              <li>Open dashboard at <a href="http://localhost:10797" className="text-emerald-400 hover:underline">http://localhost:10797</a>.</li>
              <li>Use States, Services, and Automations pages. MCP clients: ha(operation=&quot;get_states&quot;) or ha_agentic_workflow(goal=&quot;...&quot;).</li>
            </ol>
          </>
        )}
        {tab === 'connection' && (
          <>
            <h3 className="text-slate-200 font-bold">Connection</h3>
            <p>Backend: port 10796. Dashboard: port 10797. MCP clients use SSE: <code className="text-emerald-400">http://localhost:10796/sse</code>.</p>
            <p>HA must be reachable (same network or exposed). Token from Profile → Long-Lived Access Tokens.</p>
            <a href="http://localhost:10796/docs" target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 text-emerald-400 hover:underline">
              Swagger UI <ExternalLink size={12} />
            </a>
          </>
        )}
        {tab === 'trouble' && (
          <>
            <h3 className="text-slate-200 font-bold">Troubleshooting</h3>
            <ul className="space-y-2 list-disc list-inside">
              <li><strong className="text-slate-300">Not connected</strong> — Check HA_URL and HA_TOKEN; ensure HA is reachable (ping, browser).</li>
              <li><strong className="text-slate-300">401 Unauthorized</strong> — Token invalid or expired; create a new Long-Lived Access Token.</li>
              <li><strong className="text-slate-300">Backend not reachable</strong> — Run webapp\\start.ps1; check port 10796.</li>
            </ul>
          </>
        )}
      </div>
    </div>
  )
}
