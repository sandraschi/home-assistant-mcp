import { Cable, Lightbulb, Lock, Power, Thermometer, Wifi } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const ENTITIES = [
  { domain: "light", id: "light.living_room_ceiling", state: "on", icon: Lightbulb, color: "text-yellow-400", bg: "bg-yellow-500/10" },
  { domain: "light", id: "light.kitchen_island", state: "off", icon: Lightbulb, color: "text-slate-400", bg: "bg-slate-500/10" },
  { domain: "light", id: "light.bedroom_lamp", state: "on", icon: Lightbulb, color: "text-yellow-400", bg: "bg-yellow-500/10" },
  { domain: "sensor", id: "sensor.living_room_temp", state: "21.5°C", icon: Thermometer, color: "text-blue-400", bg: "bg-blue-500/10" },
  { domain: "sensor", id: "sensor.outdoor_temp", state: "8.2°C", icon: Thermometer, color: "text-blue-400", bg: "bg-blue-500/10" },
  { domain: "sensor", id: "sensor.hallway_humidity", state: "45%", icon: Thermometer, color: "text-cyan-400", bg: "bg-cyan-500/10" },
  { domain: "switch", id: "switch.coffee_maker", state: "on", icon: Power, color: "text-emerald-400", bg: "bg-emerald-500/10" },
  { domain: "switch", id: "switch.water_heater", state: "off", icon: Power, color: "text-slate-400", bg: "bg-slate-500/10" },
  { domain: "lock", id: "lock.front_door", state: "locked", icon: Lock, color: "text-emerald-400", bg: "bg-emerald-500/10" },
  { domain: "lock", id: "lock.garage_door", state: "unlocked", icon: Lock, color: "text-orange-400", bg: "bg-orange-500/10" },
  { domain: "binary_sensor", id: "binary_sensor.main_door", state: "closed", icon: Wifi, color: "text-emerald-400", bg: "bg-emerald-500/10" },
  { domain: "binary_sensor", id: "binary_sensor.window_kitchen", state: "open", icon: Wifi, color: "text-red-400", bg: "bg-red-500/10" },
  { domain: "cover", id: "cover.living_room_blinds", state: "50%", icon: Cable, color: "text-purple-400", bg: "bg-purple-500/10" },
  { domain: "cover", id: "cover.bedroom_blinds", state: "closed", icon: Cable, color: "text-slate-400", bg: "bg-slate-500/10" },
];

export function Entities() {
  return (
    <div className="space-y-6 page-enter">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">Entities</h2>
          <p className="text-slate-400">{ENTITIES.length} registered devices and sensors</p>
        </div>
      </div>

      <div className="grid gap-4">
        {ENTITIES.map((entity) => (
          <Card key={entity.id} className="glass-card">
            <CardContent className="flex items-center justify-between p-4">
              <div className="flex items-center gap-4">
                <div className={`p-2 rounded-lg ${entity.bg}`}>
                  <entity.icon className={`h-5 w-5 ${entity.color}`} />
                </div>
                <div>
                  <p className="text-sm font-medium text-white">{entity.id}</p>
                  <p className="text-xs text-slate-500 capitalize">{entity.domain}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className={`text-sm font-mono ${
                  entity.state === "on" || entity.state === "locked" || entity.state === "closed"
                    ? "text-emerald-400"
                    : entity.state === "off" || entity.state === "unlocked" || entity.state === "open"
                    ? "text-slate-400"
                    : "text-blue-400"
                }`}>
                  {entity.state}
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
