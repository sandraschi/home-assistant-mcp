## Session Context (Home Assistant MCP)

You have access to a Home Assistant orchestration server with 30+ tools for entity control,
automation, scene activation, energy monitoring, and smart home orchestration.

**Before starting work:**
1. Check HA connection: health()
2. Query available entities: query_entities(domain="light") or query_entities(domain="sensor")

**At end of work:**
- Report any entities modified or automations triggered
