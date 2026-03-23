# Home Assistant MCP Server

FastMCP 3.1 MCP server and webapp for **Home Assistant**. Portmanteau tool, sampling, agentic workflow, prompts, and skills. Webapp follows SOTA standards (React, Tailwind, dark theme, ports 10796/10797).

## Features

- **MCP tools**: `ha(operation=...)` — get_states, get_state, call_service, get_config, get_automations, trigger_automation. `ha_help(category)`. `ha_agentic_workflow(goal)` with SEP-1577 sampling.
- **Prompts**: `ha_quick_start`, `ha_diagnostics`.
- **Skills**: `skills/ha-operator.md`.
- **REST API**: GET /api/v1/health, /api/v1/states, /api/v1/config, /api/v1/automations; POST /api/v1/services/{domain}/{service}, /api/v1/automations/trigger.
- **Webapp**: Dashboard, States (filter by domain), Services (call service form), Automations (list + trigger), Settings, Help, MCP Tools.

## Ports

- Backend: **10796** (REST + MCP SSE)
- Dashboard: **10797** (Vite)

## Setup

Clone the repo and install dependencies from the **repository root** (not `webapp/`):

```powershell
git clone https://github.com/sandraschi/home-assistant-mcp.git
Set-Location home-assistant-mcp
uv sync
```

Start the webapp from the **same** clone:

```powershell
cd webapp
.\start.ps1
```

Set **HA_URL** (e.g. http://homeassistant.local:8123) and **HA_TOKEN** (Long-Lived Access Token from HA Profile → Long-Lived Access Tokens).

## MCP client

```json
{
  "mcpServers": {
    "home-assistant": {
      "url": "http://localhost:10796/sse",
      "transport": "sse"
    }
  }
}
```

## Fleet

Documented in mcp-central-docs (integrations + projects/home-assistant-mcp).
