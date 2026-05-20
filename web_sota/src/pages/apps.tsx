import { ExternalLink } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { APPS_CATALOG } from "@/common/apps-catalog";

export function Apps() {
  return (
    <div className="space-y-6 page-enter">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">App Hub</h2>
          <p className="text-slate-400">Fleet-wide application launcher ({APPS_CATALOG.length} available)</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {APPS_CATALOG.map((app) => (
          <a key={app.id} href={app.url} target="_blank" rel="noopener noreferrer">
            <Card className="glass-card h-full cursor-pointer">
              <CardContent className="p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="p-2 rounded-lg bg-white/[0.06]">
                    <app.icon className="h-5 w-5 text-orange-400" />
                  </div>
                  <ExternalLink className="h-4 w-4 text-slate-500" />
                </div>
                <h3 className="text-sm font-medium text-white mb-1">{app.label}</h3>
                <p className="text-xs text-slate-400 mb-2">{app.description}</p>
                <div className="flex flex-wrap gap-1.5">
                  {app.tags.map((tag) => (
                    <span key={tag} className="text-[10px] px-1.5 py-0.5 rounded-full bg-white/[0.05] text-slate-500 border border-white/[0.06]">
                      {tag}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          </a>
        ))}
      </div>
    </div>
  );
}
