import { Play, Pause, Clock, Zap, Bell, Home } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const AUTOMATIONS = [
  { id: 1, name: "Welcome Home", trigger: "binary_sensor.main_door opens", action: "Turn on lights, disarm alarm", status: "active", icon: Home },
  { id: 2, name: "Morning Coffee", trigger: "Time 06:30 + weekday", action: "Switch on coffee maker, open blinds", status: "active", icon: Zap },
  { id: 3, name: "Leave for Work", trigger: "binary_sensor.main_door closes (out)", action: "Arm alarm, turn off all lights", status: "active", icon: Bell },
  { id: 4, name: "Evening Wind Down", trigger: "Time 22:00", action: "Dim lights, close blinds, lock doors", status: "active", icon: Clock },
  { id: 5, name: "High Temp Alert", trigger: "sensor.living_room_temp > 30°C", action: "Notify phone, turn on AC", status: "paused", icon: Play },
  { id: 6, name: "Garage Open Reminder", trigger: "cover.garage_door open > 10min", action: "Push notification to all devices", status: "active", icon: Bell },
];

export function Automations() {
  return (
    <div className="space-y-6 page-enter">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">Automations</h2>
          <p className="text-slate-400">{AUTOMATIONS.filter(a => a.status === "active").length} active sequences</p>
        </div>
      </div>

      <div className="grid gap-4">
        {AUTOMATIONS.map((auto) => (
          <Card key={auto.id} className="glass-card">
            <CardContent className="p-4">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  <div className={`p-2 rounded-lg mt-1 ${
                    auto.status === "active" ? "bg-emerald-500/10" : "bg-slate-500/10"
                  }`}>
                    <auto.icon className={`h-5 w-5 ${
                      auto.status === "active" ? "text-emerald-400" : "text-slate-400"
                    }`} />
                  </div>
                  <div className="space-y-2">
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-medium text-white">{auto.name}</span>
                      <Badge variant={auto.status === "active" ? "default" : "secondary"} className="text-xs">
                        {auto.status === "active" ? "Active" : "Paused"}
                      </Badge>
                    </div>
                    <div className="space-y-1">
                      <p className="text-xs text-slate-500">
                        <span className="text-slate-400">Trigger:</span> {auto.trigger}
                      </p>
                      <p className="text-xs text-slate-500">
                        <span className="text-slate-400">Action:</span> {auto.action}
                      </p>
                    </div>
                  </div>
                </div>
                <button className={`p-2 rounded-lg transition-colors ${
                  auto.status === "active"
                    ? "text-emerald-400 hover:bg-emerald-500/10"
                    : "text-slate-400 hover:bg-slate-500/10"
                }`}>
                  {auto.status === "active" ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                </button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
