import { Code, Globe, List, MessageSquare, Settings, Terminal } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const TOOLS = [
  {
    name: "get_entity_state",
    description: "Retrieve the current state and attributes of any Home Assistant entity",
    icon: List,
    category: "Read",
    params: "entity_id: string",
  },
  {
    name: "list_entities",
    description: "List all registered entities, optionally filtered by domain (light, sensor, switch, etc.)",
    icon: Globe,
    category: "Read",
    params: "domain?: string",
  },
  {
    name: "call_service",
    description: "Execute a Home Assistant service call (turn_on, turn_off, set_temperature, etc.)",
    icon: Terminal,
    category: "Write",
    params: "domain: string, service: string, data?: object",
  },
  {
    name: "list_automations",
    description: "List all configured automations with their triggers and actions",
    icon: Code,
    category: "Read",
    params: "",
  },
  {
    name: "trigger_automation",
    description: "Manually trigger a specific automation by id",
    icon: Settings,
    category: "Write",
    params: "automation_id: string",
  },
  {
    name: "converse",
    description: "Process a natural language command through Home Assistant's conversation agent",
    icon: MessageSquare,
    category: "AI",
    params: "text: string",
  },
];

export function Tools() {
  return (
    <div className="space-y-6 page-enter">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">MCP Tools</h2>
          <p className="text-slate-400">{TOOLS.length} tools exposed by the Home Assistant MCP server</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {TOOLS.map((tool) => (
          <Card key={tool.name} className="glass-card">
            <CardContent className="p-4">
              <div className="flex items-start gap-4">
                <div className={`p-2 rounded-lg ${
                  tool.category === "Read" ? "bg-blue-500/10" :
                  tool.category === "Write" ? "bg-orange-500/10" : "bg-purple-500/10"
                }`}>
                  <tool.icon className={`h-5 w-5 ${
                    tool.category === "Read" ? "text-blue-400" :
                    tool.category === "Write" ? "text-orange-400" : "text-purple-400"
                  }`} />
                </div>
                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-3">
                    <code className="text-sm font-mono text-white">{tool.name}</code>
                    <span className={`text-xs px-2 py-0.5 rounded-full border ${
                      tool.category === "Read" ? "border-blue-500/30 text-blue-400" :
                      tool.category === "Write" ? "border-orange-500/30 text-orange-400" : "border-purple-500/30 text-purple-400"
                    }`}>
                      {tool.category}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{tool.description}</p>
                  {tool.params && (
                    <p className="text-xs text-slate-500 font-mono">Params: {tool.params}</p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
