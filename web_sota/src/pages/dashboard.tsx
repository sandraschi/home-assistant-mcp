import { Activity, HardDrive, Home, ShieldCheck, Zap } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function Dashboard() {
  // Mock state for SOTA demonstration
  const activeEntities = 152;
  const automations = 28;
  const securityStatus = "Armed (Stay)";
  const bridgePort = 10835;

  return (
    <div className="space-y-8 page-enter">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold tracking-tight gradient-text">Home Intelligence Hub</h2>
          <p className="text-slate-400">Smart home telemetry and state overview</p>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card className="glass-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
            <CardTitle className="text-sm font-medium text-slate-300">Active Entities</CardTitle>
            <div className="p-2 rounded-lg bg-emerald-500/10">
              <Home className="h-4 w-4 text-emerald-400" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{activeEntities}</div>
            <p className="text-xs text-slate-500 mt-1">45 Lights | 12 Sensors</p>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
            <CardTitle className="text-sm font-medium text-slate-300">Automations</CardTitle>
            <div className="p-2 rounded-lg bg-blue-500/10">
              <Zap className="h-4 w-4 text-blue-400" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{automations}</div>
            <div className="flex items-center gap-1.5 mt-1.5">
              <span className="flex h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]"></span>
              <p className="text-xs text-slate-500">All sequences nominal</p>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
            <CardTitle className="text-sm font-medium text-slate-300">Security Status</CardTitle>
            <div className="p-2 rounded-lg bg-purple-500/10">
              <ShieldCheck className="h-4 w-4 text-purple-400" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{securityStatus}</div>
            <p className="text-xs text-slate-500 mt-1">Stay mode active</p>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-3">
            <CardTitle className="text-sm font-medium text-slate-300">Bridge Port</CardTitle>
            <div className="p-2 rounded-lg bg-orange-500/10">
              <HardDrive className="h-4 w-4 text-orange-400" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">{bridgePort}</div>
            <p className="text-xs text-slate-500 mt-1">Websocket bridge active</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4 glass-card">
          <CardHeader>
            <CardTitle className="text-xl font-bold uppercase tracking-widest text-orange-500/70">
              State Changes
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[250px] font-mono text-sm p-5 overflow-y-auto border border-white/[0.06] rounded-xl bg-black/40 text-slate-400 space-y-1.5 scrollbar-thin scrollbar-thumb-white/10">
              <p className="text-blue-400">[08:45:01] light.living_room_ceiling: turned_off</p>
              <p>[08:45:10] binary_sensor.main_door: closed</p>
              <p>[08:45:15] climate.hallway: target_temp changed to 21°C</p>
              <p className="text-emerald-400">[success] Nabu Casa cloud connection restored</p>
              <p className="text-orange-400">[notify] Automation 'Welcome Home' triggered</p>
              <div className="animate-pulse inline-block h-2 w-1 bg-slate-500 ml-1 mt-2" />
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-3 glass-card">
          <CardHeader>
            <CardTitle className="text-xl font-bold uppercase tracking-widest text-orange-500/70">
              System Health
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              <div className="flex items-center p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.05] transition-all">
                <Activity className="h-5 w-5 text-emerald-400 mr-4" />
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">Supervisor Online</p>
                  <p className="text-xs text-slate-400 mt-1.5">Version 2026.2.1 • Stable</p>
                </div>
              </div>
              <div className="flex items-center p-4 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:bg-white/[0.05] transition-all">
                <Activity className="h-5 w-5 text-slate-400 mr-4" />
                <div className="space-y-1">
                  <p className="text-sm font-medium leading-none">Zigbee Mesh</p>
                  <p className="text-xs text-slate-400 mt-1.5">42 nodes • LQI 255/255 Avg</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
