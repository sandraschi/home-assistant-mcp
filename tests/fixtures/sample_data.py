"""
Sample data fixtures for comprehensive testing

Provides realistic test data for all MCP tool categories and scenarios.
"""

from typing import Dict, Any, List

# Sample entity data
SAMPLE_ENTITIES = {
    "lights": [
        {
            "entity_id": "light.living_room_main",
            "state": "on",
            "attributes": {
                "friendly_name": "Living Room Main Light",
                "brightness": 255,
                "rgb_color": [255, 255, 255],
                "color_temp": 4000,
                "supported_features": 63
            }
        },
        {
            "entity_id": "light.bedroom",
            "state": "off",
            "attributes": {
                "friendly_name": "Bedroom Light",
                "brightness": 0,
                "supported_features": 63
            }
        },
        {
            "entity_id": "light.kitchen_under_cabinet",
            "state": "on",
            "attributes": {
                "friendly_name": "Kitchen Under Cabinet",
                "brightness": 180,
                "rgb_color": [255, 255, 255],
                "effect": "none",
                "supported_features": 63
            }
        }
    ],
    "climate": [
        {
            "entity_id": "climate.living_room",
            "state": "heat",
            "attributes": {
                "friendly_name": "Living Room Climate",
                "temperature": 72.0,
                "current_temperature": 70.5,
                "hvac_modes": ["off", "heat", "cool", "auto"],
                "preset_modes": ["home", "away", "boost"],
                "fan_modes": ["auto", "low", "medium", "high"],
                "supported_features": 7
            }
        },
        {
            "entity_id": "climate.bedroom",
            "state": "off",
            "attributes": {
                "friendly_name": "Bedroom Climate",
                "temperature": 68.0,
                "current_temperature": 68.0,
                "hvac_modes": ["off", "heat", "cool"],
                "supported_features": 3
            }
        }
    ],
    "sensors": [
        {
            "entity_id": "sensor.temperature_living_room",
            "state": "72.5",
            "attributes": {
                "friendly_name": "Living Room Temperature",
                "unit_of_measurement": "°F",
                "device_class": "temperature"
            }
        },
        {
            "entity_id": "sensor.humidity_living_room",
            "state": "45",
            "attributes": {
                "friendly_name": "Living Room Humidity",
                "unit_of_measurement": "%",
                "device_class": "humidity"
            }
        },
        {
            "entity_id": "sensor.motion_living_room",
            "state": "off",
            "attributes": {
                "friendly_name": "Living Room Motion",
                "device_class": "motion"
            }
        }
    ],
    "automations": [
        {
            "entity_id": "automation.morning_routine",
            "state": "on",
            "attributes": {
                "friendly_name": "Morning Routine",
                "id": "morning_routine",
                "last_triggered": "2026-01-16T07:00:00Z"
            }
        },
        {
            "entity_id": "automation.goodnight",
            "state": "off",
            "attributes": {
                "friendly_name": "Goodnight Routine",
                "id": "goodnight",
                "last_triggered": "2026-01-16T22:30:00Z"
            }
        }
    ],
    "scenes": [
        {
            "entity_id": "scene.movie_night",
            "state": "scened",
            "attributes": {
                "friendly_name": "Movie Night"
            }
        },
        {
            "entity_id": "scene.dinner_party",
            "state": "scened",
            "attributes": {
                "friendly_name": "Dinner Party"
            }
        }
    ]
}

# Flatten entities for easier access
SAMPLE_STATES = {}
for category, entities in SAMPLE_ENTITIES.items():
    for entity in entities:
        SAMPLE_STATES[entity["entity_id"]] = entity

# Sample automations
SAMPLE_AUTOMATIONS = [
    {
        "id": "morning_routine",
        "alias": "Morning Routine",
        "trigger": [
            {
                "platform": "time",
                "at": "07:00:00"
            }
        ],
        "action": [
            {
                "service": "light.turn_on",
                "entity_id": "light.living_room_main"
            },
            {
                "service": "climate.set_temperature",
                "data": {
                    "temperature": 72
                }
            }
        ]
    },
    {
        "id": "motion_lighting",
        "alias": "Motion Activated Lighting",
        "trigger": [
            {
                "platform": "state",
                "entity_id": "sensor.motion_living_room",
                "to": "on"
            }
        ],
        "action": [
            {
                "service": "light.turn_on",
                "entity_id": "light.living_room_main",
                "data": {
                    "brightness": 180,
                    "transition": 2
                }
            }
        ]
    }
]

# Sample scenes
SAMPLE_SCENES = [
    {
        "name": "movie_night",
        "entities": {
            "light.living_room_main": {
                "state": "on",
                "brightness": 100,
                "rgb_color": [255, 150, 50]
            },
            "light.kitchen_under_cabinet": {
                "state": "off"
            },
            "climate.living_room": {
                "state": "heat",
                "temperature": 70
            }
        }
    },
    {
        "name": "dinner_party",
        "entities": {
            "light.living_room_main": {
                "state": "on",
                "brightness": 200,
                "rgb_color": [255, 200, 150]
            },
            "light.kitchen_under_cabinet": {
                "state": "on",
                "brightness": 255,
                "rgb_color": [255, 255, 255]
            }
        }
    }
]

# Sample HA configuration
SAMPLE_CONFIG = {
    "version": "2024.12.0",
    "location_name": "Test Smart Home",
    "time_zone": "America/New_York",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "elevation": 10,
    "unit_system": {
        "length": "mi",
        "mass": "lb",
        "temperature": "°F",
        "volume": "gal"
    },
    "currency": "USD",
    "country": "US",
    "language": "en"
}

# Sample orchestration scenarios
SAMPLE_ORCHESTRATION_SCENARIOS = {
    "movie_night": {
        "goal": "Prepare for movie night - dim lights, close blinds, start entertainment system",
        "expected_steps": [
            "query_current_states",
            "control_lighting_scene",
            "adjust_climate",
            "activate_entertainment"
        ],
        "tools_involved": ["query_entities", "activate_scene", "control_climate_advanced"],
        "expected_duration": 5.0
    },
    "morning_routine": {
        "goal": "Execute morning routine with lighting progression and climate adjustment",
        "expected_steps": [
            "check_time_context",
            "gradual_lighting",
            "climate_preheat",
            "notification_send"
        ],
        "tools_involved": ["smart_home_orchestration", "control_light_advanced", "control_climate_advanced"],
        "expected_duration": 3.5
    },
    "security_lockdown": {
        "goal": "Execute security lockdown - arm system, secure premises, send alerts",
        "expected_steps": [
            "arm_security_system",
            "lock_all_doors",
            "activate_cameras",
            "send_notifications"
        ],
        "tools_involved": ["security_monitoring", "emergency_response"],
        "expected_duration": 2.0
    },
    "energy_optimization": {
        "goal": "Optimize energy usage across all zones for efficiency",
        "expected_steps": [
            "analyze_current_usage",
            "identify_savings_opportunities",
            "implement_optimizations",
            "monitor_results"
        ],
        "tools_involved": ["energy_optimization", "monitor_energy_usage"],
        "expected_duration": 8.0
    }
}

# Sample natural language commands
SAMPLE_NATURAL_COMMANDS = [
    {
        "command": "Turn on the living room lights",
        "expected_intent": "control_light",
        "expected_entities": ["light.living_room_main"],
        "expected_action": "on"
    },
    {
        "command": "Set the bedroom temperature to 68 degrees",
        "expected_intent": "control_climate",
        "expected_entities": ["climate.bedroom"],
        "expected_temperature": 68.0
    },
    {
        "command": "Make it cozy in here - dim the lights and adjust the heat",
        "expected_intent": "smart_orchestration",
        "expected_scenario": "cozy_atmosphere"
    },
    {
        "command": "Start the morning routine automation",
        "expected_intent": "execute_automation",
        "expected_entities": ["automation.morning_routine"]
    },
    {
        "command": "Activate the movie night scene",
        "expected_intent": "activate_scene",
        "expected_entities": ["scene.movie_night"]
    },
    {
        "command": "What's the current temperature in the living room?",
        "expected_intent": "query_state",
        "expected_entities": ["sensor.temperature_living_room"]
    }
]

# Sample conversational responses
SAMPLE_CONVERSATIONAL_RESPONSES = {
    "success_light_control": {
        "success": True,
        "timestamp": "2026-01-16T10:30:00Z",
        "message": "✅ Light control completed successfully for light.living_room_main",
        "action": "Light turned on",
        "entity_id": "light.living_room_main",
        "new_state": {"state": "on", "brightness": 255}
    },
    "error_entity_not_found": {
        "success": False,
        "timestamp": "2026-01-16T10:30:00Z",
        "message": "❌ Entity lookup failed: light.nonexistent not found",
        "action": "Entity lookup",
        "error": "Entity light.nonexistent not found"
    },
    "orchestration_completed": {
        "success": True,
        "timestamp": "2026-01-16T10:30:00Z",
        "message": "✅ Smart home orchestration completed: Movie night preparation",
        "action": "Smart home orchestration",
        "execution_time_seconds": 4.2,
        "actions_executed": ["lighting_adjusted", "climate_set", "entertainment_started"],
        "energy_impact": "minimal_increase"
    }
}

# Sample performance benchmarks
SAMPLE_PERFORMANCE_BENCHMARKS = {
    "query_entities_basic": {
        "operation": "query_entities",
        "max_duration": 0.1,
        "expected_calls": 1,
        "description": "Basic entity query should be fast"
    },
    "light_control_advanced": {
        "operation": "control_light_advanced",
        "max_duration": 0.5,
        "expected_calls": 2,  # API call + state verification
        "description": "Advanced light control with multiple parameters"
    },
    "orchestration_complex": {
        "operation": "smart_home_orchestration",
        "max_duration": 5.0,
        "expected_calls": 5,
        "description": "Complex multi-step orchestration"
    },
    "natural_language_processing": {
        "operation": "natural_language_control",
        "max_duration": 2.0,
        "expected_calls": 3,
        "description": "Natural language command processing and execution"
    }
}

# Sample error conditions
SAMPLE_ERROR_CONDITIONS = {
    "entity_not_found": {
        "input": {"entity_id": "light.nonexistent"},
        "expected_error": "Entity not found",
        "expected_response_type": "conversational_error"
    },
    "service_unavailable": {
        "input": {"domain": "invalid", "service": "service"},
        "expected_error": "Service unavailable",
        "expected_response_type": "conversational_error"
    },
    "permission_denied": {
        "input": {"entity_id": "automation.restricted"},
        "expected_error": "Permission denied",
        "expected_response_type": "conversational_error"
    },
    "network_timeout": {
        "input": {"timeout_scenario": True},
        "expected_error": "Network timeout",
        "expected_response_type": "conversational_error"
    }
}

# Sample security scenarios
SAMPLE_SECURITY_SCENARIOS = {
    "home_armed": {
        "mode": "armed_home",
        "expected_actions": ["arm_interior_sensors", "delay_entry"],
        "expected_notifications": ["family_only"],
        "expected_response_time": 2.0
    },
    "away_armed": {
        "mode": "armed_away",
        "expected_actions": ["arm_all_sensors", "immediate_entry"],
        "expected_notifications": ["authorities"],
        "expected_response_time": 1.5
    },
    "emergency_fire": {
        "scenario": "fire_detected",
        "expected_actions": ["activate_alarms", "unlock_doors", "call_emergency"],
        "expected_zones": ["all"],
        "expected_response_time": 1.0
    }
}

# Sample energy optimization scenarios
SAMPLE_ENERGY_SCENARIOS = {
    "eco_mode": {
        "mode": "eco",
        "expected_savings": "20-30%",
        "comfort_impact": "minimal",
        "learning_enabled": True
    },
    "comfort_mode": {
        "mode": "comfort",
        "expected_savings": "10-20%",
        "comfort_impact": "none",
        "learning_enabled": True
    },
    "performance_mode": {
        "mode": "performance",
        "expected_savings": "0-10%",
        "comfort_impact": "enhanced",
        "learning_enabled": False
    }
}

# Sample predictive automation scenarios
SAMPLE_PREDICTIVE_SCENARIOS = {
    "commute_home": {
        "anticipate": "return from work",
        "timeframe_minutes": 30,
        "expected_predictions": ["arrival_time", "lighting_prep", "climate_prep"],
        "confidence_threshold": 0.7
    },
    "meal_prep": {
        "anticipate": "dinner preparation",
        "timeframe_minutes": 60,
        "expected_predictions": ["cooking_start", "appliance_prep", "lighting_adjust"],
        "confidence_threshold": 0.8
    },
    "sleep_routine": {
        "anticipate": "bedtime approach",
        "timeframe_minutes": 45,
        "expected_predictions": ["lighting_dim", "climate_adjust", "security_arm"],
        "confidence_threshold": 0.6
    }
}