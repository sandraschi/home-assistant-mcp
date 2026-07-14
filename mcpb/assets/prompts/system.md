# home-assistant-mcp — MCP Server Capabilities

**Instructions for LLM:** This file must contain 3,000+ words describing the server's complete capabilities.
Include: all tools with parameters, all prompts, all resources, configuration options, environment variables,
data sources, and integration points. Every tool must have its purpose, parameters, and return format documented.

## Server Overview

[Write 2-3 paragraphs describing what this MCP server does, its domain, and key features.]

## Tools

- **ha_tool**: ha_tool - **ha_help**: ha_help - **ha_agentic_workflow**: ha_agentic_workflow - **health**: health - **api_states**: GET all states or one entity. Query: entity_id, domain (filter). - **api_config**: GET HA config. - **api_call_service**: POST call HA service. Body: entity_id, or other service_data. - **api_automations**: GET list of automation entities. - **api_trigger_automation**: api_trigger_automation - **main_stdio**: main(stdio) - **main_http**: main(http) - **main_sse**: main(sse) - **control_light_advanced**: control_light_advanced - **control_climate_advanced**: control_climate_advanced - **execute_automation_advanced**: execute_automation_advanced - **activate_scene**: activate_scene - **query_entities**: query_entities - **control_entity**: control_entity - **control_light**: control_light - **control_climate**: control_climate - **execute_automation**: execute_automation - **execute_script**: execute_script - **get_home_status**: get_home_status - **render_template**: render_template - **get_available_events**: get_available_events - **smart_home_orchestration**: smart_home_orchestration - **analyze_home_patterns**: analyze_home_patterns - **get_home_status_detailed**: get_home_status_detailed - **monitor_energy_usage**: monitor_energy_usage - **security_monitoring**: security_monitoring - **emergency_response**: emergency_response - **energy_optimization**: energy_optimization - **create_smart_schedule**: create_smart_schedule - **natural_language_control**: natural_language_control - **predictive_automation**: predictive_automation - **multi_zone_orchestration**: multi_zone_orchestration - **debug_automation**: debug_automation - **system_maintenance_check**: system_maintenance_check

## Configuration

[Document all environment variables, their defaults, and purposes.]

## Data Sources

[Document any databases, APIs, or files the server reads.]
