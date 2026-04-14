"""
Home Assistant MCP Prompt Registry
SOTA v14.1.0-compliant prompt definitions for HA orchestration.
"""

from fastmcp.prompts import Message


def ha_quick_start() -> Message:
    """Setup and connect to Home Assistant."""
    return Message(
        "You are helping set up the Home Assistant MCP server.\n\n"
        "1. In Home Assistant: Profile (bottom sidebar) -> Long-Lived Access Tokens -> Create token. Copy it.\n"
        "2. Set HA_URL (e.g. http://192.168.1.50:8123) and HA_TOKEN. Start server: uv run python -m home_assistant_mcp.server --mode dual --port 10782.\n"
        "3. Open dashboard at http://localhost:10783. Use States to browse entities, Services to call services, Automations to list/trigger.\n"
        "4. From an MCP client use ha(operation='get_states') or ha(operation='call_service') or ha_agentic_workflow(goal='...')."
    )

def ha_diagnostics() -> Message:
    """Diagnostic checklist for Home Assistant connection."""
    return Message(
        "Run a quick diagnostic:\n\n"
        "1. Call ha(operation='get_config') to verify HA connection.\n"
        "2. Call ha(operation='get_states') to list entities.\n"
        "3. Ensure HA_URL is reachable and HA_TOKEN is a valid Long-Lived Access Token."
    )

def register_prompts(mcp) -> None:
    """Register all SOTA prompts with the FastMCP instance."""
    mcp.add_prompt(ha_quick_start)
    mcp.add_prompt(ha_diagnostics)
