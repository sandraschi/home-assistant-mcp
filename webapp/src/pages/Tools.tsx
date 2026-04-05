import React, { useState } from 'react'
import { Wrench, Copy, Check } from 'lucide-react'

const Code = ({ children }: { children: string }) => {
  const [copied, setCopied] = useState(false)
  const copy = () => {
    navigator.clipboard.writeText(children)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }
  return (
    <div className="relative group mt-2">
      <pre className="bg-black/60 border border-white/10 rounded-xl px-4 py-3 text-xs text-slate-300 font-mono overflow-x-auto whitespace-pre-wrap break-all">
        {children}
      </pre>
      <button
        type="button"
        onClick={copy}
        className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity p-1.5 rounded-lg bg-white/10 hover:bg-white/20"
      >
        {copied ? <Check size={12} className="text-green-400" /> : <Copy size={12} className="text-slate-400" />}
      </button>
    </div>
  )
}

export default function Tools() {
  return (
    <div className="space-y-6 py-4 max-w-4xl">
      <div className="flex items-center gap-4">
        <Wrench className="text-emerald-400 w-8 h-8" />
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">MCP Tools</h1>
          <p className="text-slate-400 text-sm">Home Assistant tools for AI clients (Cursor, Claude Desktop)</p>
        </div>
      </div>
      <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 p-5 space-y-4">
        <p className="text-sm text-slate-400">
          Connect your MCP client to <code className="text-emerald-400">http://localhost:10796/sse</code> (SSE transport).
        </p>
        <div>
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Portmanteau</p>
          <p className="text-sm text-slate-400">
            ha(operation=&quot;get_states&quot;), ha(operation=&quot;get_state&quot;, entity_id=&quot;...&quot;), ha(operation=&quot;call_service&quot;, domain=&quot;light&quot;, service=&quot;turn_on&quot;, entity_id=&quot;...&quot;), ha(operation=&quot;get_config&quot;), ha(operation=&quot;get_automations&quot;), ha(operation=&quot;trigger_automation&quot;, entity_id=&quot;automation.xxx&quot;)
          </p>
        </div>
        <div>
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Help</p>
          <p className="text-sm text-slate-400">ha_help(category=...) — categories: get_states, call_service, get_config, automations, connection</p>
        </div>
        <div>
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">Agentic workflow (SEP-1577)</p>
          <p className="text-sm text-slate-400">ha_agentic_workflow(goal=&quot;...&quot;) — LLM plans and runs get_states, get_state, call_service, trigger_automation</p>
        </div>
        <div>
          <p className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-1">mcp_config.json</p>
          <Code>{`{
  "mcpServers": {
    "home-assistant": {
      "url": "http://localhost:10796/sse",
      "transport": "sse"
    }
  }
}`}</Code>
        </div>
      </div>
    </div>
  )
}
