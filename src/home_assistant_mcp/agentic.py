"""Agentic workflow and sampling for Home Assistant (FastMCP 3.1 / SEP-1577)."""
import logging

from fastmcp import Context

from .portmanteau import ha_tool

logger = logging.getLogger("home-assistant-mcp.agentic")


async def ha_agentic_workflow(goal: str, ctx: Context) -> str:
    """Achieve a high-level Home Assistant goal via planning and sampling (SEP-1577)."""

    async def get_states(entity_id: str | None = None, domain: str | None = None) -> str:
        out = await ha_tool(ctx=None, operation="get_states", entity_id=entity_id or "")
        if not out.get("success"):
            return str(out.get("error", out))
        states = out.get("states") or ([] if not out.get("state") else [out["state"]])
        if not states:
            return "No states returned."
        if len(states) > 10:
            return f"Found {len(states)} entities. First 10: " + str([s.get("entity_id") for s in states[:10]])
        return str([{"entity_id": s.get("entity_id"), "state": s.get("state")} for s in states])

    async def get_state(entity_id: str) -> str:
        out = await ha_tool(ctx=None, operation="get_state", entity_id=entity_id)
        if not out.get("success"):
            return str(out.get("error", out))
        return str(out.get("state", out))

    async def call_service(domain: str, service: str, entity_id: str | None = None, service_data: dict | None = None) -> str:
        out = await ha_tool(ctx=None, operation="call_service", domain=domain, service=service, entity_id=entity_id, service_data=service_data)
        if not out.get("success"):
            return str(out.get("error", out))
        return out.get("message", str(out.get("result", "")))

    async def trigger_automation(entity_id: str) -> str:
        out = await ha_tool(ctx=None, operation="trigger_automation", entity_id=entity_id)
        if not out.get("success"):
            return str(out.get("error", out))
        return out.get("message", "Triggered.")

    system_prompt = (
        "You are a Home Assistant operator. Tools: get_states(entity_id optional, domain optional), "
        "get_state(entity_id), call_service(domain, service, entity_id optional, service_data optional), "
        "trigger_automation(entity_id). Plan steps to achieve the user goal; execute and summarize."
    )
    try:
        result = await ctx.sample(
            messages=goal,
            system_prompt=system_prompt,
            tools=[get_states, get_state, call_service, trigger_automation],
            temperature=0.2,
            max_tokens=1024,
        )
        return result.text or "No response from planner."
    except Exception as e:
        logger.exception("Agentic workflow failed")
        return f"Workflow failed: {e}"
