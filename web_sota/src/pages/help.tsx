import { Book, Command, FileText, MessageSquare } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const HELP_SECTIONS = [
  {
    title: "Getting Started",
    description: "Connect the MCP server to your Home Assistant instance via the Settings page. Configure the WebSocket URL and test the connection.",
    icon: Book,
  },
  {
    title: "Natural Language Commands",
    description: "Use the HA Command interface to query and control your smart home in plain English. The LLM agent translates requests into service calls.",
    icon: MessageSquare,
  },
  {
    title: "MCP Tool Reference",
    description: "The server exposes tools like get_entity_state, list_entities, call_service, and more. Browse them in the Tools section.",
    icon: Command,
  },
  {
    title: "Troubleshooting",
    description: "Ensure Home Assistant is reachable, WebSocket port 8123 is open, and the long-lived access token is valid. Check the Status page for service health.",
    icon: FileText,
  },
];

export function Help() {
  return (
    <div className="space-y-6 page-enter">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">Help & Documentation</h2>
          <p className="text-slate-400">Reference guide for the Home Assistant MCP server</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {HELP_SECTIONS.map((section) => (
          <Card key={section.title} className="glass-card">
            <CardContent className="p-4">
              <div className="flex items-start gap-4">
                <div className="p-2 rounded-lg bg-white/[0.06]">
                  <section.icon className="h-5 w-5 text-orange-400" />
                </div>
                <div className="space-y-2">
                  <h3 className="text-sm font-medium text-white">{section.title}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{section.description}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="glass-card">
        <CardHeader>
          <CardTitle className="text-xl font-bold uppercase tracking-widest text-orange-500/70">
            Quick Reference
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 font-mono text-sm">
            <div className="flex items-center gap-4 p-3 rounded-xl bg-white/[0.03] border border-white/[0.06]">
              <code className="text-emerald-400 text-xs">/api/states</code>
              <span className="text-slate-500 text-xs">REST endpoint for entity state snapshots</span>
            </div>
            <div className="flex items-center gap-4 p-3 rounded-xl bg-white/[0.03] border border-white/[0.06]">
              <code className="text-emerald-400 text-xs">/api/services</code>
              <span className="text-slate-500 text-xs">REST endpoint for available service domains</span>
            </div>
            <div className="flex items-center gap-4 p-3 rounded-xl bg-white/[0.03] border border-white/[0.06]">
              <code className="text-emerald-400 text-xs">ws://ha:8123/api/websocket</code>
              <span className="text-slate-500 text-xs">WebSocket connection URL (configure in Settings)</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
