"""
Core MCP Tools Tests

Tests for fundamental entity discovery, control, and automation tools.
Comprehensive coverage of conversational responses and error handling.
"""

import pytest
import asyncio
from typing import Dict, Any
from unittest.mock import patch

from home_assistant_mcp.mcp.tools import register_all_ha_tools
from home_assistant_mcp.mcp.tools import (
    EntityFilter, ServiceCallRequest, LightControlRequest,
    ClimateControlRequest, TemplateRenderRequest
)

from .conftest import (
    assert_conversational_response,
    assert_tool_execution_time,
    create_mock_entity
)


class TestEntityDiscovery:
    """Test entity discovery and querying tools."""

    @pytest.mark.asyncio
    async def test_query_entities_basic(self, mock_mcp_server, performance_monitor):
        """Test basic entity querying without filters."""
        performance_monitor.start_timer("query_entities_basic")

        # Execute tool
        result = await mock_mcp_server.app.tools["query_entities"]()

        performance_monitor.end_timer("query_entities_basic")

        # Validate conversational response
        assert_conversational_response(result)

        # Validate content
        assert result["success"] is True
        assert "entities" in result
        assert "count" in result
        assert result["count"] > 0
        assert "grouped_by_domain" in result

        # Validate performance
        metrics = performance_monitor.get_metrics()
        assert_tool_execution_time(metrics["query_entities_basic"]["duration"], 0.1)

    @pytest.mark.asyncio
    async def test_query_entities_with_filter(self, mock_mcp_server):
        """Test entity querying with domain filter."""
        filter_obj = EntityFilter(domain="light")

        result = await mock_mcp_server.app.tools["query_entities"](filter_obj)

        assert_conversational_response(result)
        assert result["success"] is True
        assert all(entity["entity_id"].startswith("light.") for entity in result["entities"])

    @pytest.mark.asyncio
    async def test_query_entities_specific_entity(self, mock_mcp_server):
        """Test querying a specific entity."""
        filter_obj = EntityFilter(entity_id="light.living_room")

        result = await mock_mcp_server.app.tools["query_entities"](filter_obj)

        assert_conversational_response(result)
        assert result["success"] is True
        assert len(result["entities"]) == 1
        assert result["entities"][0]["entity_id"] == "light.living_room"

    @pytest.mark.asyncio
    async def test_query_entities_not_found(self, mock_mcp_server):
        """Test querying non-existent entity."""
        filter_obj = EntityFilter(entity_id="light.nonexistent")

        result = await mock_mcp_server.app.tools["query_entities"](filter_obj)

        assert_conversational_response(result)
        assert result["success"] is False
        assert "not found" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_query_entities_friendly_name_filter(self, mock_mcp_server):
        """Test filtering by friendly name."""
        filter_obj = EntityFilter(friendly_name="living room")

        result = await mock_mcp_server.app.tools["query_entities"](filter_obj)

        assert_conversational_response(result)
        assert result["success"] is True
        # Should find entities with "living room" in friendly name


class TestLightControl:
    """Test advanced light control functionality."""

    @pytest.mark.asyncio
    async def test_light_control_basic_on(self, mock_mcp_server):
        """Test basic light turn on."""
        request = LightControlRequest(
            entity_id="light.living_room",
            action="on"
        )

        result = await mock_mcp_server.app.tools["control_light_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "turned on" in result["message"].lower()
        assert result["entity_id"] == "light.living_room"

    @pytest.mark.asyncio
    async def test_light_control_brightness(self, mock_mcp_server):
        """Test light control with brightness."""
        request = LightControlRequest(
            entity_id="light.living_room",
            action="on",
            brightness_pct=75
        )

        result = await mock_mcp_server.app.tools["control_light_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "75%" in result["message"]

    @pytest.mark.asyncio
    async def test_light_control_rgb_color(self, mock_mcp_server):
        """Test light control with RGB color."""
        request = LightControlRequest(
            entity_id="light.living_room",
            action="on",
            rgb_color=[255, 100, 150]  # Pink
        )

        result = await mock_mcp_server.app.tools["control_light_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "[255, 100, 150]" in result["message"]

    @pytest.mark.asyncio
    async def test_light_control_multiple_entities(self, mock_mcp_server):
        """Test controlling multiple lights simultaneously."""
        request = LightControlRequest(
            entity_id=["light.living_room", "light.bedroom"],
            action="off"
        )

        result = await mock_mcp_server.app.tools["control_light_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "2" in result["message"]  # Should indicate multiple lights

    @pytest.mark.asyncio
    async def test_light_control_transition(self, mock_mcp_server):
        """Test light control with transition time."""
        request = LightControlRequest(
            entity_id="light.living_room",
            action="on",
            brightness_pct=50,
            transition=2.5
        )

        result = await mock_mcp_server.app.tools["control_light_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert result["action_details"]["transition"] == 2.5

    @pytest.mark.asyncio
    async def test_light_control_invalid_entity(self, mock_mcp_server):
        """Test light control with invalid entity."""
        request = LightControlRequest(
            entity_id="light.nonexistent",
            action="on"
        )

        result = await mock_mcp_server.app.tools["control_light_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is False
        assert "failed" in result["message"].lower()


class TestClimateControl:
    """Test advanced climate control functionality."""

    @pytest.mark.asyncio
    async def test_climate_set_temperature(self, mock_mcp_server):
        """Test setting climate temperature."""
        request = ClimateControlRequest(
            entity_id="climate.living_room",
            action="set_temperature",
            temperature=74.0
        )

        result = await mock_mcp_server.app.tools["control_climate_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "74.0°" in result["message"]

    @pytest.mark.asyncio
    async def test_climate_set_hvac_mode(self, mock_mcp_server):
        """Test setting HVAC mode."""
        request = ClimateControlRequest(
            entity_id="climate.living_room",
            action="set_hvac_mode",
            hvac_mode="cool"
        )

        result = await mock_mcp_server.app.tools["control_climate_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "cool mode" in result["message"]

    @pytest.mark.asyncio
    async def test_climate_multiple_entities(self, mock_mcp_server):
        """Test controlling multiple climate entities."""
        request = ClimateControlRequest(
            entity_id=["climate.living_room", "climate.bedroom"],
            action="set_hvac_mode",
            hvac_mode="off"
        )

        result = await mock_mcp_server.app.tools["control_climate_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is True


class TestAutomationExecution:
    """Test automation and scene execution."""

    @pytest.mark.asyncio
    async def test_execute_automation_basic(self, mock_mcp_server):
        """Test basic automation execution."""
        result = await mock_mcp_server.app.tools["execute_automation"]("automation.morning_routine")

        assert_conversational_response(result)
        assert result["success"] is True
        assert "executed" in result["message"]
        assert result["entity_id"] == "automation.morning_routine"

    @pytest.mark.asyncio
    async def test_execute_automation_advanced(self, mock_mcp_server):
        """Test advanced automation execution with variables."""
        from home_assistant_mcp.mcp.tools import AutomationExecutionRequest

        request = AutomationExecutionRequest(
            entity_id="automation.morning_routine",
            variables={"brightness": 80, "temperature": 72}
        )

        result = await mock_mcp_server.app.tools["execute_automation_advanced"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert result["execution_time_seconds"] > 0

    @pytest.mark.asyncio
    async def test_activate_scene(self, mock_mcp_server):
        """Test scene activation."""
        from home_assistant_mcp.mcp.tools import SceneActivationRequest

        request = SceneActivationRequest(
            entity_id="scene.movie_night",
            transition=3
        )

        result = await mock_mcp_server.app.tools["activate_scene"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "movie night" in result["message"].lower()
        assert result["transition_seconds"] == 3


class TestTemplateRendering:
    """Test Jinja2 template rendering."""

    @pytest.mark.asyncio
    async def test_render_simple_template(self, mock_mcp_server):
        """Test rendering a simple template."""
        request = TemplateRenderRequest(
            template="Current temperature: {{ states('sensor.temperature_living_room') }}"
        )

        result = await mock_mcp_server.app.tools["render_template"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "current temperature" in result["result"].lower()

    @pytest.mark.asyncio
    async def test_render_template_with_variables(self, mock_mcp_server):
        """Test template rendering with custom variables."""
        request = TemplateRenderRequest(
            template="Hello {{ name }}, the temperature is {{ temp }}°F",
            variables={"name": "Alice", "temp": 72}
        )

        result = await mock_mcp_server.app.tools["render_template"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "alice" in result["result"].lower()
        assert "72°f" in result["result"].lower()

    @pytest.mark.asyncio
    async def test_render_complex_template(self, mock_mcp_server):
        """Test complex template with conditionals and loops."""
        request = TemplateRenderRequest(
            template="""
            {% set temp = states('sensor.temperature_living_room') | float %}
            {% if temp > 75 %}
                It's warm at {{ temp }}°F
            {% elif temp < 65 %}
                It's cool at {{ temp }}°F
            {% else %}
                It's comfortable at {{ temp }}°F
            {% endif %}
            """
        )

        result = await mock_mcp_server.app.tools["render_template"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "comfortable" in result["result"].lower()


class TestErrorHandling:
    """Test comprehensive error handling."""

    @pytest.mark.asyncio
    async def test_invalid_entity_reference(self, mock_mcp_server):
        """Test handling of invalid entity references."""
        request = ServiceCallRequest(
            domain="light",
            service="turn_on",
            entity_id="light.invalid_entity"
        )

        result = await mock_mcp_server.app.tools["control_entity"](request)

        assert_conversational_response(result)
        assert result["success"] is False
        assert "failed" in result["message"]

    @pytest.mark.asyncio
    async def test_network_timeout_simulation(self, mock_mcp_server):
        """Test handling of network timeouts."""
        # This would require mocking network failures
        # For now, test with invalid service call
        request = ServiceCallRequest(
            domain="invalid_domain",
            service="invalid_service"
        )

        result = await mock_mcp_server.app.tools["control_entity"](request)

        assert_conversational_response(result)
        assert result["success"] is False

    @pytest.mark.asyncio
    async def test_template_render_error(self, mock_mcp_server):
        """Test template rendering error handling."""
        request = TemplateRenderRequest(
            template="{{ invalid_syntax }"  # Missing closing brace
        )

        result = await mock_mcp_server.app.tools["render_template"](request)

        assert_conversational_response(result)
        assert result["success"] is False


class TestPerformance:
    """Test performance characteristics."""

    @pytest.mark.asyncio
    async def test_query_performance_under_load(self, mock_mcp_server, performance_monitor):
        """Test query performance with multiple concurrent requests."""
        performance_monitor.start_timer("concurrent_queries")

        # Execute multiple queries concurrently
        tasks = []
        for i in range(5):
            task = mock_mcp_server.app.tools["query_entities"]()
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        performance_monitor.end_timer("concurrent_queries")

        # Validate all results
        for result in results:
            assert_conversational_response(result)
            assert result["success"] is True

        # Check performance
        metrics = performance_monitor.get_metrics()
        avg_time = metrics["concurrent_queries"]["duration"] / 5
        assert_tool_execution_time(avg_time, 0.2)  # Allow slightly higher for concurrent load

    @pytest.mark.asyncio
    async def test_light_control_response_time(self, mock_mcp_server, performance_monitor):
        """Test light control response time."""
        performance_monitor.start_timer("light_control_timing")

        request = LightControlRequest(
            entity_id="light.living_room",
            action="toggle"
        )

        result = await mock_mcp_server.app.tools["control_light_advanced"](request)

        performance_monitor.end_timer("light_control_timing")

        assert_conversational_response(result)
        assert result["success"] is True

        metrics = performance_monitor.get_metrics()
        assert_tool_execution_time(metrics["light_control_timing"]["duration"], 0.5)


class TestConversationalResponses:
    """Test conversational response formatting."""

    @pytest.mark.asyncio
    async def test_success_response_format(self, mock_mcp_server):
        """Test that success responses follow conversational guidelines."""
        result = await mock_mcp_server.app.tools["query_entities"]()

        # Check required conversational elements
        assert "message" in result
        assert "timestamp" in result
        assert "success" in result
        assert result["success"] is True
        assert "✅" in result["message"]

    @pytest.mark.asyncio
    async def test_error_response_format(self, mock_mcp_server):
        """Test that error responses follow conversational guidelines."""
        filter_obj = EntityFilter(entity_id="light.nonexistent")

        result = await mock_mcp_server.app.tools["query_entities"](filter_obj)

        # Check error response elements
        assert "message" in result
        assert "timestamp" in result
        assert "success" in result
        assert result["success"] is False
        assert "❌" in result["message"]
        assert "error" in result

    @pytest.mark.asyncio
    async def test_response_context_inclusion(self, mock_mcp_server):
        """Test that responses include relevant context."""
        request = LightControlRequest(
            entity_id="light.living_room",
            action="on",
            brightness_pct=80
        )

        result = await mock_mcp_server.app.tools["control_light_advanced"](request)

        # Check context inclusion
        assert "entity_id" in result
        assert result["entity_id"] == "light.living_room"
        assert "action_details" in result
        assert result["action_details"]["brightness_pct"] == 80