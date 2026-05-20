import { Activity, Cpu, HardDrive, Signal, Wifi } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const SERVICES = [
  { name: "HA Supervisor", status: "online", version: "2026.2.1", icon: Cpu },
  { name: "WebSocket Bridge", status: "online", version: "v3.2.0", icon: Wifi },
  { name: "MCP HTTP Transport", status: "online", version: "port 10835", icon: HardDrive },
  { name: "Zigbee Mesh", status: "online", version: "42 nodes · LQI 255/255", icon: Signal },
  { name: "Nabu Casa Cloud", status: "online", version: "latency 34ms", icon: Activity },
];

const METRICS = [
  { label: "Uptime", value: "14d 7h 32m" },
  { label: "Memory", value: "1.2 GB / 4 GB" },
  { label: "CPU Load", value: "23%" },
  { label: "Active Automations", value: "5" },
  { label: "Pending Updates", value: "2" },
  { label: "Error Rate", value: "0.03%" },
];

export function Status() {
  return (
    <div className="space-y-6 page-enter">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">System Status</h2>
          <p className="text-slate-400">Health overview for the Home Assistant MCP bridge</p>
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {SERVICES.map((svc) => (
          <Card key={svc.name} className="glass-card">
            <CardContent className="p-4">
              <div className="flex items-center gap-4">
                <div className="p-2 rounded-lg bg-emerald-500/10">
                  <svc.icon className="h-5 w-5 text-emerald-400" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-white">{svc.name}</span>
                    <span className="flex h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
                  </div>
                  <p className="text-xs text-slate-400 mt-0.5">{svc.version}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="glass-card">
        <CardHeader>
          <CardTitle className="text-xl font-bold uppercase tracking-widest text-orange-500/70">
            Runtime Metrics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {METRICS.map((m) => (
              <div key={m.label} className="p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06]">
                <p className="text-xs text-slate-500 mb-1">{m.label}</p>
                <p className="text-lg font-semibold text-white">{m.value}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
