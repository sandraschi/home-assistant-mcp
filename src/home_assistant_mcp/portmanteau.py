"""Portmanteau tool ha(operation=...) for Home Assistant (FastMCP 3.1)."""
import logging
from fastmcp import Context

from . import client

logger = logging.getLogger("home-assistant-mcp.portmanteau")


async def ha_tool(
    ctx: Context | None = None,
    operation: str = "get_states",
    domain: str | None = None,
    service: str | None = None,
    entity_id: str | None = None,
    service_data: dict | None = None,
) -> dict:
    """Unified tool for Home Assistant.

    Operations:
    - get_states: all states, or pass entity_id for one. Optional domain filter (e.g. light, vacuum).
    - get_state: single entity (alias for get_states with entity_id).
    - call_service: domain + service required; optional entity_id and service_data dict.
    - get_config: HA server config.
    - get_automations: list automation entities.
    - trigger_automation: entity_id required (e.g. automation.my_automation).
    Returns dict with success (bool); on failure includes error (str).
    """
    correlation_id = ctx.correlation_id if ctx else "manual"
    logger.info("Executing ha operation: %s", operation, extra={"correlation_id": correlation_id})
    op_lower = operation.lower().strip()

    if not client.is_configured():
        return {"success": False, "error": "HA_TOKEN not set. Create a Long-Lived Access Token in HA profile."}

    try:
        if op_lower == "get_states":
            data = await client.get_states(entity_id if entity_id else None)
            if entity_id and isinstance(data, dict):
                if domain and not (data.get("entity_id") or "").startswith(f"{domain}."):
                    return {"success": True, "states": [], "message": "Entity not in domain"}
                return {"success": True, "state": data}
            if isinstance(data, list) and domain:
                data = [s for s in data if (s.get("entity_id") or "").startswith(f"{domain}.")]
            return {"success": True, "states": data if isinstance(data, list) else [data]}
        if op_lower == "get_state":
            if not entity_id:
                return {"success": False, "error": "entity_id required for get_state"}
            data = await client.get_states(entity_id)
            return {"success": True, "state": data}
        if op_lower == "call_service":
            if not domain or not service:
                return {"success": False, "error": "domain and service required for call_service"}
            body = service_data or {}
            if entity_id:
                body["entity_id"] = entity_id
            result = await client.call_service(domain, service, body)
            return {"success": True, "result": result, "message": f"Called {domain}.{service}"}
        if op_lower == "get_config":
            data = await client.get_config()
            return {"success": True, "config": data}
        if op_lower == "get_automations":
            data = await client.get_automations()
            return {"success": True, "automations": data}
        if op_lower == "trigger_automation":
            if not entity_id:
                return {"success": False, "error": "entity_id required for trigger_automation"}
            result = await client.trigger_automation(entity_id)
            return {"success": True, "result": result, "message": f"Triggered {entity_id}"}
        return {"success": False, "error": f"Unknown operation: {operation}. Use get_states, get_state, call_service, get_config, get_automations, trigger_automation."}
    except Exception as e:
        logger.exception("HA operation failed")
        return {"success": False, "error": str(e), "correlation_id": correlation_id}
