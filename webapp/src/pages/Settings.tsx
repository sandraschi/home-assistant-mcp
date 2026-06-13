import React, { useState, useEffect } from 'react'
import { Settings as SettingsIcon } from 'lucide-react'

function LLMSettings() {
  const [providers, setProviders] = useState<Record<string, {name:string}[]>>({});
  const [selectedProvider, setSelectedProvider] = useState("ollama");
  const [selectedModel, setSelectedModel] = useState("");
  const [status, setStatus] = useState<"loading"|"ready"|"error">("loading");
  useEffect(() => {
    fetch("/api/llm/providers").then(r => r.json()).then(d => {
      setProviders(d);
      const savedP = localStorage.getItem("llm_provider") || "ollama";
      const savedM = localStorage.getItem("llm_model") || "";
      setSelectedProvider(savedP);
      const models = d[savedP === "ollama" ? "ollama" : "lm_studio"] || [];
      setSelectedModel(savedM && models.some((m:{name:string}) => m.name === savedM) ? savedM : (models[0]?.name || ""));
      setStatus(models.length > 0 ? "ready" : "error");
    }).catch(() => {
      setProviders({ ollama: [{name:"llama3.2:3b"}] });
      setSelectedModel(localStorage.getItem("llm_model") || "llama3.2:3b");
      setStatus("ready");
    });
  }, []);
  const save = (p:string, m:string) => { localStorage.setItem("llm_provider", p); localStorage.setItem("llm_model", m); };
  const models = providers[selectedProvider === "ollama" ? "ollama" : "lm_studio"] || [];
  return (
    <div className="rounded-2xl border border-white/10 bg-[#0f0f12]/80 p-5 space-y-3">
      <h3 className="text-sm font-semibold text-slate-300">Local LLM</h3>
      <select className="w-full rounded-xl border border-white/10 bg-black/40 px-3 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500/40"
        value={selectedProvider} onChange={(e) => { setSelectedProvider(e.target.value); save(e.target.value, ""); }}>
        <option value="ollama">Ollama</option>
        <option value="lm_studio">LM Studio</option>
      </select>
      <select className="w-full rounded-xl border border-white/10 bg-black/40 px-3 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-emerald-500/40"
        value={selectedModel} onChange={(e) => { setSelectedModel(e.target.value); save(selectedProvider, e.target.value); }}>
        {models.map((m) => <option key={m.name} value={m.name}>{m.name}</option>)}
      </select>
    </div>
  );
}

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
      <LLMSettings />
    </div>
  )
}
