# Home Assistant Operator Skill

## Scope
Operate Home Assistant via the HA MCP server (FastMCP 3.1). Use the portmanteau tool `ha(operation=...)` and the agentic workflow for high-level goals.

## Tools
- **ha(operation, domain, service, entity_id, service_data)** — get_states, get_state, call_service, get_config, get_automations, trigger_automation.
- **ha_help(category, topic)** — Drill-down help: get_states, call_service, get_config, automations, connection.
- **ha_agentic_workflow(goal)** — High-level goal; LLM plans and runs get_states, get_state, call_service, trigger_automation via sampling.

## Prompts
- **ha_quick_start()** — Setup (HA token, HA_URL, dashboard, MCP usage).
- **ha_diagnostics()** — Diagnostic checklist.

## Rules
1. Always use HA_TOKEN (Long-Lived Access Token from HA profile). HA_URL defaults to http://homeassistant.local:8123.
2. For call_service provide domain and service (e.g. light.turn_on, vacuum.start); entity_id and extra service_data as needed.
3. Prefer ha_agentic_workflow for multi-step goals (e.g. "turn off all lights in the living room then set thermostat to 20").
