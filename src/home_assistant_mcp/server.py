#!/usr/bin/env python3
"""Home Assistant MCP Server — FastMCP 3.1, sampling, agentic workflow."""
import logging
import sys
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP

from . import client
from .agentic import ha_agentic_workflow
from .portmanteau import ha_tool

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", stream=sys.stderr)
logger = logging.getLogger("home-assistant-mcp")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Home Assistant MCP starting")
    yield
    logger.info("Home Assistant MCP shutting down")


app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

mcp = FastMCP.from_fastapi(app, name="Home Assistant")

# --- Help ---
_HELP_CATEGORIES = {
    "get_states": "List all entity states or filter by entity_id/domain. ha(operation='get_states', entity_id='...', domain='light').",
    "call_service": "Call a HA service. ha(operation='call_service', domain='light', service='turn_on', entity_id='light.living').",
    "get_config": "HA server config. ha(operation='get_config').",
    "automations": "get_automations lists automation entities; trigger_automation(entity_id) runs one.",
    "connection": "HA_URL (default http://homeassistant.local:8123), HA_TOKEN (Long-Lived Access Token from profile).",
}


async def ha_help(category: str | None = None, topic: str | None = None) -> dict:
    """Multi-level help for Home Assistant MCP."""
    if not category:
        return {"help": "Home Assistant MCP", "categories": _HELP_CATEGORIES}
    if category not in _HELP_CATEGORIES:
        return {"error": f"Unknown category: {category}", "available": list(_HELP_CATEGORIES.keys())}
    return {"category": category, "detail": _HELP_CATEGORIES[category]}


# --- Register tools ---
mcp.tool()(ha_tool)
mcp.tool()(ha_help)
mcp.tool()(ha_agentic_workflow)

# --- FastMCP Parity ---
try:
    from .prompts import register_prompts
    register_prompts(mcp)
except Exception as e:
    logger.debug("Prompt registration skipped: %s", e)

try:
    from pathlib import Path

    from fastmcp.server.providers.skills import SkillsDirectoryProvider

    roots = []
    repo_root = Path(__file__).resolve().parents[2]
    for rel in (".cursor/skills", "skills"):
        rp = repo_root / rel
        if rp.is_dir():
            roots.append(rp)

    if roots:
        mcp.add_provider(SkillsDirectoryProvider(roots=roots))
except Exception as e:
    logger.debug("Skills provider registration skipped: %s", e)


# --- REST ---
@app.get("/api/v1/health")
async def health():
    connected = False
    if client.is_configured():
        try:
            await client.get_config()
            connected = True
        except Exception:
            pass
    return {
        "status": "ok",
        "service": "home-assistant-mcp",
        "connected": connected,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/api/v1/states")
async def api_states(entity_id: str | None = None, domain: str | None = None):
    """GET all states or one entity. Query: entity_id, domain (filter)."""
    out = await ha_tool(ctx=None, operation="get_states", entity_id=entity_id or "", domain=domain)
    if not out.get("success"):
        raise HTTPException(status_code=502, detail=out.get("error", "HA unavailable"))
    states = out.get("states")
    state = out.get("state")
    if state is not None:
        return state
    if domain and states:
        states = [s for s in states if (s.get("entity_id") or "").startswith(f"{domain}.")]
    return {"states": states or []}


@app.get("/api/v1/config")
async def api_config():
    """GET HA config."""
    if not client.is_configured():
        raise HTTPException(status_code=503, detail="HA_TOKEN not set")
    try:
        return await client.get_config()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/api/v1/services/{domain}/{service}")
async def api_call_service(domain: str, service: str, body: dict | None = None):
    """POST call HA service. Body: entity_id, or other service_data."""
    out = await ha_tool(ctx=None, operation="call_service", domain=domain, service=service, entity_id=(body or {}).get("entity_id"), service_data=body)
    if not out.get("success"):
        raise HTTPException(status_code=502, detail=out.get("error", "Call failed"))
    return out.get("result", [])


@app.get("/api/v1/automations")
async def api_automations():
    """GET list of automation entities."""
    out = await ha_tool(ctx=None, operation="get_automations")
    if not out.get("success"):
        raise HTTPException(status_code=502, detail=out.get("error", "HA unavailable"))
    return {"automations": out.get("automations", [])}


@app.post("/api/v1/automations/trigger")
async def api_trigger_automation(body: dict):
    """POST trigger automation. Body: { entity_id: "automation.xxx" }."""
    entity_id = (body or {}).get("entity_id")
    if not entity_id:
        raise HTTPException(status_code=400, detail="entity_id required")
    out = await ha_tool(ctx=None, operation="trigger_automation", entity_id=entity_id)
    if not out.get("success"):
        raise HTTPException(status_code=502, detail=out.get("error", "Trigger failed"))
    return out


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--mode", default="dual", choices=("stdio", "http", "dual"))
    p.add_argument("--port", type=int, default=10782)
    args = p.parse_args()
    if args.mode == "stdio":
        from fastmcp.cli import run_stdio
        run_stdio(mcp)
        return
    uvicorn.run(app, host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
