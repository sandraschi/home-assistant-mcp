"""
Mock Home Assistant API for comprehensive testing

Provides realistic HA API responses for testing MCP tools without
requiring a live HA instance.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Union
from unittest.mock import AsyncMock, Mock
import random


class MockHomeAssistantAPI:
    """
    Comprehensive mock implementation of Home Assistant API.

    Supports all operations needed for testing the MCP server including:
    - Entity state management
    - Service calls
    - Event handling
    - Configuration access
    - Template rendering
    """

    def __init__(self):
        self.states = {}
        self.config = {}
        self.events = []
        self.services = {}
        self.templates = {}
        self._setup_mock_data()

    def _setup_mock_data(self):
        """Initialize mock HA data."""
        # Mock configuration
        self.config = {
            "version": "2024.12.0",
            "location_name": "Test Home",
            "time_zone": "America/New_York",
            "unit_system": {
                "length": "mi",
                "mass": "lb",
                "temperature": "°F",
                "volume": "gal"
            }
        }

        # Mock entities
        self.states = {
            "light.living_room": {
                "entity_id": "light.living_room",
                "state": "on",
                "attributes": {
                    "friendly_name": "Living Room Light",
                    "brightness": 255,
                    "rgb_color": [255, 255, 255],
                    "supported_features": 63
                },
                "last_updated": "2026-01-16T10:00:00Z",
                "last_changed": "2026-01-16T10:00:00Z"
            },
            "light.bedroom": {
                "entity_id": "light.bedroom",
                "state": "off",
                "attributes": {
                    "friendly_name": "Bedroom Light",
                    "brightness": 0,
                    "supported_features": 63
                },
                "last_updated": "2026-01-16T09:30:00Z",
                "last_changed": "2026-01-16T09:30:00Z"
            },
            "climate.living_room": {
                "entity_id": "climate.living_room",
                "state": "heat",
                "attributes": {
                    "friendly_name": "Living Room Climate",
                    "temperature": 72.0,
                    "current_temperature": 70.0,
                    "hvac_modes": ["off", "heat", "cool", "auto"],
                    "preset_modes": ["home", "away", "boost"],
                    "supported_features": 7
                },
                "last_updated": "2026-01-16T10:15:00Z",
                "last_changed": "2026-01-16T10:15:00Z"
            },
            "sensor.temperature": {
                "entity_id": "sensor.temperature",
                "state": "72.5",
                "attributes": {
                    "friendly_name": "Temperature",
                    "unit_of_measurement": "°F",
                    "device_class": "temperature"
                },
                "last_updated": "2026-01-16T10:20:00Z",
                "last_changed": "2026-01-16T10:20:00Z"
            },
            "automation.morning_routine": {
                "entity_id": "automation.morning_routine",
                "state": "on",
                "attributes": {
                    "friendly_name": "Morning Routine",
                    "id": "morning_routine",
                    "last_triggered": "2026-01-16T07:00:00Z"
                },
                "last_updated": "2026-01-16T07:00:00Z",
                "last_changed": "2026-01-16T07:00:00Z"
            },
            "scene.movie_night": {
                "entity_id": "scene.movie_night",
                "state": "scened",
                "attributes": {
                    "friendly_name": "Movie Night"
                },
                "last_updated": "2026-01-16T08:00:00Z",
                "last_changed": "2026-01-16T08:00:00Z"
            }
        }

        # Mock events
        self.events = [
            {
                "event": "state_changed",
                "data": {
                    "entity_id": "light.living_room",
                    "old_state": {"state": "off"},
                    "new_state": {"state": "on"}
                }
            },
            {
                "event": "automation_triggered",
                "data": {
                    "entity_id": "automation.morning_routine"
                }
            }
        ]

        # Mock services
        self.services = {
            "light": {
                "turn_on": {"description": "Turn on light"},
                "turn_off": {"description": "Turn off light"},
                "toggle": {"description": "Toggle light"}
            },
            "climate": {
                "set_temperature": {"description": "Set temperature"},
                "set_hvac_mode": {"description": "Set HVAC mode"}
            },
            "automation": {
                "trigger": {"description": "Trigger automation"}
            },
            "scene": {
                "turn_on": {"description": "Activate scene"}
            }
        }

    async def get_states(self, entity_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all entity states with optional filtering."""
        states = list(self.states.values())

        if entity_filter:
            # Simple string matching filter
            states = [s for s in states if entity_filter.lower() in s["entity_id"].lower() or
                     entity_filter.lower() in s.get("attributes", {}).get("friendly_name", "").lower()]

        return states

    async def get_state(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get specific entity state."""
        return self.states.get(entity_id)

    async def call_service(self, domain: str, service: str, entity_id: Optional[str] = None,
                          **service_data) -> bool:
        """Call a HA service."""
        try:
            # Simulate service execution
            if domain == "light" and service in ["turn_on", "turn_off", "toggle"]:
                if entity_id and entity_id in self.states:
                    current_state = self.states[entity_id]["state"]
                    if service == "toggle":
                        new_state = "off" if current_state == "on" else "on"
                    else:
                        new_state = "on" if service == "turn_on" else "off"

                    self.states[entity_id]["state"] = new_state
                    self.states[entity_id]["last_changed"] = "2026-01-16T10:30:00Z"

                    # Update attributes based on service data
                    if service_data.get("brightness"):
                        self.states[entity_id]["attributes"]["brightness"] = service_data["brightness"]
                    if service_data.get("rgb_color"):
                        self.states[entity_id]["attributes"]["rgb_color"] = service_data["rgb_color"]

                    return True

            elif domain == "climate" and service == "set_temperature":
                if entity_id and entity_id in self.states:
                    temperature = service_data.get("temperature", 72.0)
                    self.states[entity_id]["attributes"]["temperature"] = temperature
                    return True

            elif domain == "automation" and service == "trigger":
                if entity_id and entity_id in self.states:
                    # Simulate automation trigger
                    self.states[entity_id]["attributes"]["last_triggered"] = "2026-01-16T10:30:00Z"
                    return True

            elif domain == "scene" and service == "turn_on":
                if entity_id and entity_id in self.states:
                    # Scenes don't change state but can be "activated"
                    return True

            return False
        except Exception:
            return False

    async def get_entity_info(self) -> Dict[str, Any]:
        """Get entity information summary."""
        states = list(self.states.values())

        # Group by domain
        domains = {}
        for state in states:
            domain = state["entity_id"].split(".")[0]
            domains[domain] = domains.get(domain, 0) + 1

        return {
            "total_entities": len(states),
            "entities_by_domain": domains,
            "domains": list(domains.keys()),
            "available_events": ["state_changed", "automation_triggered", "service_called"]
        }

    async def get_config(self) -> Dict[str, Any]:
        """Get HA configuration."""
        return self.config

    async def get_events(self) -> List[Dict[str, Any]]:
        """Get available events."""
        return self.events

    async def render_template(self, template: str, variables: Optional[Dict[str, Any]] = None) -> Any:
        """Render Jinja2 template."""
        try:
            # Simple template rendering simulation
            result = template

            # Replace basic state references
            for entity_id, state in self.states.items():
                result = result.replace(f"states('{entity_id}')", f"'{state['state']'}'")
                if "temperature" in entity_id:
                    result = result.replace("states('sensor.temperature')", "'72.5'")

            # Replace variable references
            if variables:
                for key, value in variables.items():
                    result = result.replace(f"{{{{ {key} }}}}", str(value))

            # Remove template syntax for simple cases
            result = result.replace("{{", "").replace("}}", "")

            return result.strip()
        except Exception:
            return None

    async def execute_automation(self, entity_id: str) -> bool:
        """Execute an automation."""
        if entity_id in self.states:
            self.states[entity_id]["attributes"]["last_triggered"] = "2026-01-16T10:30:00Z"
            return True
        return False

    async def execute_script(self, entity_id: str, **variables) -> bool:
        """Execute a script."""
        # Scripts are similar to automations in mock
        return await self.execute_automation(entity_id)

    async def activate_scene(self, entity_id: str, transition: Optional[int] = None) -> bool:
        """Activate a scene."""
        if entity_id in self.states and entity_id.startswith("scene."):
            return True
        return False

    async def control_light(self, entity_id: str, action: str, brightness: Optional[int] = None,
                           rgb_color: Optional[List[int]] = None) -> bool:
        """Control a light with advanced features."""
        if entity_id in self.states and entity_id.startswith("light."):
            if action in ["on", "off", "toggle"]:
                current_state = self.states[entity_id]["state"]
                if action == "toggle":
                    new_state = "off" if current_state == "on" else "on"
                else:
                    new_state = action

                self.states[entity_id]["state"] = new_state
                self.states[entity_id]["last_changed"] = "2026-01-16T10:30:00Z"

                # Update attributes
                if brightness is not None:
                    self.states[entity_id]["attributes"]["brightness"] = brightness
                if rgb_color is not None:
                    self.states[entity_id]["attributes"]["rgb_color"] = rgb_color

                return True
        return False

    async def control_climate(self, entity_id: str, action: str, temperature: Optional[float] = None,
                             hvac_mode: Optional[str] = None) -> bool:
        """Control climate system."""
        if entity_id in self.states and entity_id.startswith("climate."):
            if action == "set_temperature" and temperature is not None:
                self.states[entity_id]["attributes"]["temperature"] = temperature
                return True
            elif action == "set_hvac_mode" and hvac_mode:
                self.states[entity_id]["state"] = hvac_mode
                return True
        return False

    async def analyze_patterns(self, days: int) -> Dict[str, Any]:
        """Analyze usage patterns (mock implementation)."""
        return {
            "peak_usage_hours": ["7-9", "18-22"],
            "energy_waste": 2.5,
            "inactive_devices": ["sensor.unused"],
            "efficiency_score": 85
        }

    async def get_energy_usage(self, hours: int) -> Dict[str, Any]:
        """Get energy usage data."""
        return {
            "total_kwh": random.uniform(5.0, 15.0),
            "by_device": {
                "light.living_room": random.uniform(1.0, 3.0),
                "climate.living_room": random.uniform(2.0, 5.0)
            }
        }

    async def get_system_health(self) -> Dict[str, Any]:
        """Get system health information."""
        return {
            "uptime_seconds": 86400,  # 1 day
            "database_size_mb": 45.2,
            "memory_usage_mb": 120.5,
            "cpu_usage_percent": 15.3
        }

    # Advanced orchestration methods
    async def create_emergency_response(self, scenario: str) -> Dict[str, Any]:
        """Create emergency response plan."""
        return {
            "scenario": scenario,
            "actions": ["activate_alarm", "send_notifications", "secure_doors"],
            "safety_measures": ["evacuation_routes", "emergency_contacts"],
            "execution_time": 5.2
        }

    async def execute_emergency_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute emergency response plan."""
        return {
            "success": True,
            "actions_executed": plan["actions"],
            "execution_time": random.uniform(3.0, 8.0),
            "notifications_sent": 2
        }

    async def start_energy_optimization(self, mode: str, duration: int,
                                       learn_patterns: bool, zones: Optional[List[str]]) -> Dict[str, Any]:
        """Start energy optimization."""
        return {
            "mode": mode,
            "duration": duration,
            "actions": ["dim_unused_lights", "adjust_thermostat"],
            "estimated_savings_kwh": random.uniform(1.0, 3.0)
        }

    async def get_optimization_results(self) -> Dict[str, Any]:
        """Get optimization results."""
        return {
            "estimated_savings_kwh": 2.1,
            "actions_applied": 3,
            "efficiency_improved": True
        }

    async def plan_multi_zone_orchestration(self, zones: List[str], scenario: str) -> Dict[str, Any]:
        """Plan multi-zone orchestration."""
        zone_actions = {}
        for zone in zones:
            zone_actions[zone] = [f"adjust_lighting_{zone}", f"control_climate_{zone}"]

        return {
            "scenario": scenario,
            "zone_actions": zone_actions,
            "energy_savings": random.uniform(0.5, 1.5)
        }

    async def execute_multi_zone_orchestration(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multi-zone orchestration."""
        return {
            "success": True,
            "execution_time": random.uniform(2.0, 6.0),
            "zones_coordinated": len(plan["zone_actions"]),
            "actions_completed": sum(len(actions) for actions in plan["zone_actions"].values())
        }

    async def parse_natural_command(self, command: str) -> Dict[str, Any]:
        """Parse natural language command."""
        # Simple mock parsing
        if "light" in command.lower():
            return {
                "intent": "control_light",
                "entities": ["light.living_room"],
                "action": "on" if "on" in command.lower() else "off",
                "confidence": 0.9
            }
        elif "temperature" in command.lower():
            return {
                "intent": "control_climate",
                "entities": ["climate.living_room"],
                "temperature": 72.0,
                "confidence": 0.85
            }
        else:
            return {
                "intent": "unknown",
                "confidence": 0.3
            }

    async def execute_natural_command(self, parsed_command: Dict[str, Any]) -> Dict[str, Any]:
        """Execute parsed natural language command."""
        if parsed_command["intent"] == "control_light":
            success = await self.control_light(
                parsed_command["entities"][0],
                parsed_command["action"]
            )
            return {
                "success": success,
                "action": f"Light control: {parsed_command['action']}",
                "details": parsed_command
            }
        elif parsed_command["intent"] == "control_climate":
            success = await self.control_climate(
                "climate.living_room",
                "set_temperature",
                temperature=parsed_command["temperature"]
            )
            return {
                "success": success,
                "action": f"Climate control: {parsed_command['temperature']}°",
                "details": parsed_command
            }

        return {
            "success": False,
            "action": "Command not understood",
            "details": parsed_command
        }

    async def generate_predictions(self, anticipate: str, timeframe: int) -> Dict[str, Any]:
        """Generate predictive automation suggestions."""
        return {
            "target": anticipate,
            "timeframe_minutes": timeframe,
            "predictions": [
                {"event": "return_home", "confidence": 0.8, "time_estimate": "18:30"},
                {"event": "dinner_time", "confidence": 0.7, "time_estimate": "19:00"}
            ],
            "learning_enabled": True
        }

    async def setup_predictive_automation(self, predictions: Dict[str, Any]) -> Dict[str, Any]:
        """Setup predictive automation."""
        return {
            "automations_created": len(predictions["predictions"]),
            "triggers_setup": ["time_based", "location_based"],
            "monitoring_active": True
        }

    async def create_smart_schedule(self, name: str, activities: List[str]) -> Dict[str, Any]:
        """Create smart schedule."""
        return {
            "schedule_name": name,
            "activities": activities,
            "optimal_times": {
                "morning_routine": "07:00",
                "work_setup": "08:30",
                "evening_windy": "21:00"
            },
            "automations_created": len(activities)
        }

    async def debug_automation(self, entity_id: str) -> Dict[str, Any]:
        """Debug automation."""
        return {
            "issues_found": ["trigger_condition", "missing_variable"],
            "recommendations": ["Add condition validation", "Use template variables"],
            "test_results": {"syntax_check": True, "logic_validation": False}
        }

    async def perform_maintenance_check(self) -> Dict[str, Any]:
        """Perform maintenance check."""
        return {
            "overall_health": "good",
            "issues": [{"severity": "warning", "message": "Database size growing"}],
            "maintenance_tasks": ["backup_database", "clean_old_logs"],
            "performance_metrics": {"response_time": 0.15, "memory_usage": 85.2}
        }