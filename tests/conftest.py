"""
Test Configuration and Fixtures for Home Assistant MCP Server

Provides comprehensive test infrastructure for FastMCP 2.14.3 compliance,
conversational AI features, and autonomous orchestration testing.
"""

import asyncio
import pytest
import pytest_asyncio
from typing import Dict, Any, List, Optional
from unittest.mock import AsyncMock, Mock, MagicMock
import json
from pathlib import Path

from fastmcp import FastMCP
from pydantic import BaseModel

# Test data and fixtures
try:
    from .fixtures.mock_ha_api import MockHomeAssistantAPI
    from .fixtures.sample_data import (
        SAMPLE_ENTITIES,
        SAMPLE_STATES,
        SAMPLE_AUTOMATIONS,
        SAMPLE_SCENES,
        SAMPLE_CONFIG
    )
except ImportError:
    # Handle case where conftest is imported directly (not by pytest)
    try:
        from fixtures.mock_ha_api import MockHomeAssistantAPI
        from fixtures.sample_data import (
            SAMPLE_ENTITIES,
            SAMPLE_STATES,
            SAMPLE_AUTOMATIONS,
            SAMPLE_SCENES,
            SAMPLE_CONFIG
        )
    except ImportError:
        # Fallback for when running from different directory
        import sys
        import os
        sys.path.insert(0, os.path.dirname(__file__))
        from fixtures.mock_ha_api import MockHomeAssistantAPI
        from fixtures.sample_data import (
            SAMPLE_ENTITIES,
            SAMPLE_STATES,
            SAMPLE_AUTOMATIONS,
            SAMPLE_SCENES,
            SAMPLE_CONFIG
        )


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        "ha_url": "http://mock-home-assistant:8123",
        "ha_token": "mock_token_12345",
        "mcp_port": 8080,
        "log_level": "DEBUG"
    }


@pytest.fixture
def mock_ha_api():
    """Mock Home Assistant API client."""
    return MockHomeAssistantAPI()


@pytest.fixture
async def mock_mcp_server(mock_ha_api):
    """Mock MCP server with FastMCP 2.14.3 features."""
    from home_assistant_mcp.mcp.server import create_mcp_server
    from home_assistant_mcp.core.globals import set_ha_client

    # Set up mock client
    set_ha_client(mock_ha_api)

    # Create server
    server = create_mcp_server()

    # Mock the server components for testing
    server._ha_client = mock_ha_api

    yield server


@pytest.fixture
def sample_entity_data():
    """Sample entity data for testing."""
    return {
        "light.living_room": {
            "entity_id": "light.living_room",
            "state": "on",
            "attributes": {
                "friendly_name": "Living Room Light",
                "brightness": 255,
                "rgb_color": [255, 255, 255]
            }
        },
        "climate.living_room": {
            "entity_id": "climate.living_room",
            "state": "heat",
            "attributes": {
                "friendly_name": "Living Room Climate",
                "temperature": 72.0,
                "current_temperature": 70.0
            }
        },
        "automation.morning_routine": {
            "entity_id": "automation.morning_routine",
            "state": "on",
            "attributes": {
                "friendly_name": "Morning Routine"
            }
        }
    }


@pytest.fixture
def sample_conversation_context():
    """Sample conversation context for testing."""
    return {
        "user_id": "test_user",
        "session_id": "test_session_123",
        "conversation_history": [
            {"role": "user", "content": "Turn on the living room lights"},
            {"role": "assistant", "content": "I'll turn on the living room lights for you."}
        ],
        "active_entities": ["light.living_room", "climate.living_room"],
        "user_preferences": {
            "temperature_unit": "fahrenheit",
            "brightness_default": 80
        }
    }


@pytest.fixture
def performance_monitor():
    """Performance monitoring fixture."""
    class PerformanceMonitor:
        def __init__(self):
            self.metrics = {}

        def start_timer(self, name: str):
            self.metrics[name] = {"start": asyncio.get_event_loop().time()}

        def end_timer(self, name: str):
            if name in self.metrics:
                start_time = self.metrics[name]["start"]
                end_time = asyncio.get_event_loop().time()
                self.metrics[name]["duration"] = end_time - start_time
                self.metrics[name]["end"] = end_time

        def get_metrics(self):
            return self.metrics

    return PerformanceMonitor()


@pytest.fixture
def orchestration_tester():
    """Orchestration testing utilities."""
    class OrchestrationTester:
        def __init__(self):
            self.orchestration_steps = []
            self.mock_responses = {}

        def add_step(self, step_name: str, tool_name: str, parameters: Dict[str, Any]):
            """Add an orchestration step."""
            self.orchestration_steps.append({
                "name": step_name,
                "tool": tool_name,
                "parameters": parameters,
                "executed": False
            })

        def mock_tool_response(self, tool_name: str, response: Dict[str, Any]):
            """Mock tool response for testing."""
            self.mock_responses[tool_name] = response

        def get_orchestration_plan(self):
            """Get the complete orchestration plan."""
            return {
                "steps": self.orchestration_steps,
                "total_steps": len(self.orchestration_steps),
                "mock_responses": self.mock_responses
            }

        async def execute_orchestration(self):
            """Execute the orchestration plan."""
            results = []
            for step in self.orchestration_steps:
                # Mock execution
                result = self.mock_responses.get(step["tool"], {"success": True})
                step["executed"] = True
                step["result"] = result
                results.append(result)

            return results

    return OrchestrationTester()


@pytest.fixture
def conversational_validator():
    """Conversational response validation."""
    class ConversationalValidator:
        def __init__(self):
            self.validations = []

        def validate_response(self, response: Dict[str, Any], expected_features: List[str]):
            """Validate conversational response features."""
            validation = {
                "response": response,
                "timestamp": response.get("timestamp"),
                "has_message": "message" in response,
                "has_success": "success" in response,
                "features_present": [],
                "issues": []
            }

            # Check required features
            for feature in expected_features:
                if feature == "conversational" and "message" in response:
                    validation["features_present"].append("conversational")
                elif feature == "contextual" and any(key in response for key in ["entity_id", "action", "details"]):
                    validation["features_present"].append("contextual")
                elif feature == "actionable" and "error" in response or "suggestions" in response:
                    validation["features_present"].append("actionable")

            # Check for common issues
            if not response.get("success") and "error" not in response:
                validation["issues"].append("Missing error details on failure")

            if response.get("success") and not any(key in response for key in ["message", "result", "data"]):
                validation["issues"].append("Missing success feedback")

            self.validations.append(validation)
            return validation

        def get_validation_summary(self):
            """Get summary of all validations."""
            total = len(self.validations)
            passed = sum(1 for v in self.validations if not v["issues"])
            return {
                "total_validations": total,
                "passed": passed,
                "failed": total - passed,
                "success_rate": passed / total if total > 0 else 0
            }

    return ConversationalValidator()


@pytest.fixture
def sampling_validator():
    """FastMCP 2.14.3 sampling validation."""
    class SamplingValidator:
        def __init__(self):
            self.sampling_events = []

        def record_sampling_event(self, event_type: str, details: Dict[str, Any]):
            """Record a sampling event for validation."""
            self.sampling_events.append({
                "type": event_type,
                "timestamp": asyncio.get_event_loop().time(),
                "details": details
            })

        def validate_orchestration_flow(self, expected_steps: List[str]):
            """Validate that sampling orchestration followed expected flow."""
            actual_steps = [event["type"] for event in self.sampling_events]

            validation = {
                "expected_steps": expected_steps,
                "actual_steps": actual_steps,
                "steps_match": actual_steps == expected_steps,
                "missing_steps": [step for step in expected_steps if step not in actual_steps],
                "extra_steps": [step for step in actual_steps if step not in expected_steps]
            }

            return validation

        def get_sampling_summary(self):
            """Get summary of sampling events."""
            event_types = {}
            for event in self.sampling_events:
                event_type = event["type"]
                event_types[event_type] = event_types.get(event_type, 0) + 1

            return {
                "total_events": len(self.sampling_events),
                "event_types": event_types,
                "duration": self._calculate_duration()
            }

        def _calculate_duration(self):
            """Calculate total sampling duration."""
            if not self.sampling_events:
                return 0

            start_time = min(event["timestamp"] for event in self.sampling_events)
            end_time = max(event["timestamp"] for event in self.sampling_events)
            return end_time - start_time

    return SamplingValidator()


# Test utilities
def assert_conversational_response(response: Dict[str, Any]):
    """Assert that a response follows conversational guidelines."""
    assert "success" in response, "Response missing success field"
    assert "timestamp" in response, "Response missing timestamp"
    assert "message" in response, "Response missing conversational message"

    if response["success"]:
        assert "✅" in response["message"], "Success message should contain checkmark"
    else:
        assert "❌" in response["message"], "Error message should contain X mark"


def assert_tool_execution_time(execution_time: float, max_time: float = 1.0):
    """Assert that tool execution time is within acceptable limits."""
    assert execution_time <= max_time, f"Tool execution took {execution_time}s, max allowed {max_time}s"


def assert_orchestration_result(result: Dict[str, Any], expected_steps: int):
    """Assert that orchestration completed with expected structure."""
    assert "success" in result, "Orchestration result missing success field"
    assert "execution_time_seconds" in result, "Missing execution time"
    assert "actions_executed" in result, "Missing executed actions"

    if expected_steps > 0:
        assert len(result["actions_executed"]) >= expected_steps, \
            f"Expected at least {expected_steps} actions, got {len(result['actions_executed'])}"


# Test data helpers
def create_mock_entity(entity_id: str, state: str = "on", **attributes):
    """Create a mock HA entity for testing."""
    return {
        "entity_id": entity_id,
        "state": state,
        "attributes": {
            "friendly_name": entity_id.split(".")[-1].replace("_", " ").title(),
            **attributes
        },
        "last_updated": "2026-01-16T10:00:00Z",
        "last_changed": "2026-01-16T10:00:00Z"
    }


def create_mock_automation(name: str, enabled: bool = True):
    """Create a mock automation for testing."""
    return {
        "entity_id": f"automation.{name.lower().replace(' ', '_')}",
        "state": "on" if enabled else "off",
        "attributes": {
            "friendly_name": name,
            "id": name.lower().replace(" ", "_")
        }
    }


def create_mock_scene(name: str):
    """Create a mock scene for testing."""
    return {
        "entity_id": f"scene.{name.lower().replace(' ', '_')}",
        "state": "scened",
        "attributes": {
            "friendly_name": name
        }
    }