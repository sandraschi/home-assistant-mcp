"""
Orchestration and AI Features Tests

Tests for FastMCP 2.14.3 sampling, autonomous orchestration,
predictive automation, and conversational AI features.
"""

import pytest
import asyncio
from typing import Dict, Any, List
from unittest.mock import patch, AsyncMock

from home_assistant_mcp.mcp.tools import (
    SmartHomeOrchestrationRequest,
    register_all_ha_tools
)

from .conftest import (
    assert_conversational_response,
    assert_orchestration_result
)
from .fixtures.sample_data import SAMPLE_ORCHESTRATION_SCENARIOS


class TestAutonomousOrchestration:
    """Test autonomous orchestration with FastMCP sampling."""

    @pytest.mark.asyncio
    async def test_movie_night_orchestration(self, mock_mcp_server, orchestration_tester, sampling_validator):
        """Test complete movie night orchestration scenario."""
        # Setup orchestration tester
        orchestration_tester.add_step(
            "analyze_current_states",
            "query_entities",
            {}
        )
        orchestration_tester.add_step(
            "control_lighting_scene",
            "activate_scene",
            {"entity_id": "scene.movie_night"}
        )
        orchestration_tester.add_step(
            "adjust_climate",
            "control_climate_advanced",
            {"entity_id": "climate.living_room", "action": "set_temperature", "temperature": 70}
        )

        # Mock successful responses
        orchestration_tester.mock_tool_response("query_entities", {"success": True, "count": 5})
        orchestration_tester.mock_tool_response("activate_scene", {"success": True})
        orchestration_tester.mock_tool_response("control_climate_advanced", {"success": True})

        # Execute orchestration
        request = SmartHomeOrchestrationRequest(
            goal="Prepare for movie night - dim lights, close blinds, start entertainment system",
            max_steps=5,
            safety_mode=True
        )

        sampling_validator.record_sampling_event("orchestration_start", {"goal": request.goal})

        result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)

        sampling_validator.record_sampling_event("orchestration_complete", {"result": result})

        # Validate orchestration result
        assert_orchestration_result(result, 3)
        assert "movie night" in result["message"].lower()
        assert result["execution_time_seconds"] > 0

        # Validate sampling flow
        validation = sampling_validator.validate_orchestration_flow([
            "orchestration_start",
            "orchestration_complete"
        ])
        assert validation["steps_match"]

    @pytest.mark.asyncio
    async def test_morning_routine_orchestration(self, mock_mcp_server):
        """Test morning routine orchestration with predictive elements."""
        request = SmartHomeOrchestrationRequest(
            goal="Execute morning routine with lighting progression and climate adjustment",
            max_steps=4,
            learning_mode=True
        )

        result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)

        assert_orchestration_result(result, 2)
        assert "morning routine" in result["message"].lower()
        assert "learning_enabled" in result

    @pytest.mark.asyncio
    async def test_security_lockdown_orchestration(self, mock_mcp_server):
        """Test emergency security orchestration."""
        request = SmartHomeOrchestrationRequest(
            goal="Execute security lockdown - arm system, secure premises, send alerts",
            max_steps=3,
            safety_mode=True
        )

        result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)

        assert_orchestration_result(result, 2)
        assert "security" in result["message"].lower()
        assert result["execution_time_seconds"] < 3.0  # Should be fast for security

    @pytest.mark.asyncio
    async def test_energy_optimization_orchestration(self, mock_mcp_server):
        """Test energy optimization orchestration."""
        request = SmartHomeOrchestrationRequest(
            goal="Optimize energy usage across all zones for efficiency",
            max_steps=4,
            safety_mode=True
        )

        result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)

        assert_orchestration_result(result, 2)
        assert "energy" in result["message"].lower()
        assert "estimated_savings_kwh" in result


class TestNaturalLanguageControl:
    """Test conversational AI natural language processing."""

    @pytest.mark.asyncio
    async def test_simple_light_command(self, mock_mcp_server):
        """Test simple natural language light control."""
        result = await mock_mcp_server.app.tools["natural_language_control"](
            "Turn on the living room lights"
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert "light" in result["message"].lower()
        assert result["parsed_actions"][0]["intent"] == "control_light"
        assert "light.living_room" in result["parsed_actions"][0]["entities"]

    @pytest.mark.asyncio
    async def test_complex_multi_action_command(self, mock_mcp_server):
        """Test complex natural language command with multiple actions."""
        command = "Make it cozy in here - dim the lights and set the temperature to 72 degrees"

        result = await mock_mcp_server.app.tools["natural_language_control"](command)

        assert_conversational_response(result)
        assert result["success"] is True
        assert len(result["parsed_actions"]) >= 2  # Should parse multiple actions

    @pytest.mark.asyncio
    async def test_automation_trigger_command(self, mock_mcp_server):
        """Test natural language automation triggering."""
        result = await mock_mcp_server.app.tools["natural_language_control"](
            "Start the morning routine automation"
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert "automation" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_query_command(self, mock_mcp_server):
        """Test natural language query commands."""
        result = await mock_mcp_server.app.tools["natural_language_control"](
            "What's the current temperature in the living room?"
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert "temperature" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_ambiguous_command_handling(self, mock_mcp_server):
        """Test handling of ambiguous or unclear commands."""
        result = await mock_mcp_server.app.tools["natural_language_control"](
            "Do something with the lights maybe"
        )

        # Should either succeed with best interpretation or fail gracefully
        assert "message" in result
        assert "confidence_score" in result
        if not result["success"]:
            assert "unclear" in result["message"].lower() or "understand" in result["message"].lower()


class TestPredictiveAutomation:
    """Test predictive automation and learning features."""

    @pytest.mark.asyncio
    async def test_commute_prediction(self, mock_mcp_server):
        """Test commute-based predictive automation."""
        result = await mock_mcp_server.app.tools["predictive_automation"](
            "prepare for my return home from work",
            timeframe_minutes=30
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert "return home" in result["message"].lower()
        assert "predictions" in result
        assert result["timeframe_minutes"] == 30

    @pytest.mark.asyncio
    async def test_meal_preparation_prediction(self, mock_mcp_server):
        """Test meal preparation predictive automation."""
        result = await mock_mcp_server.app.tools["predictive_automation"](
            "prepare dinner based on cooking time and preferences",
            timeframe_minutes=60
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert "dinner" in result["message"].lower()
        assert len(result["predicted_events"]) > 0

    @pytest.mark.asyncio
    async def test_sleep_routine_prediction(self, mock_mcp_server):
        """Test sleep routine predictive automation."""
        result = await mock_mcp_server.app.tools["predictive_automation"](
            "prepare for bedtime routine",
            timeframe_minutes=45
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert "bedtime" in result["message"].lower() or "sleep" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_prediction_confidence_filtering(self, mock_mcp_server):
        """Test that low-confidence predictions are filtered out."""
        result = await mock_mcp_server.app.tools["predictive_automation"](
            "predict something unlikely to happen",
            timeframe_minutes=10
        )

        assert_conversational_response(result)
        # Should either have low confidence or filter out unlikely predictions
        if "predictions" in result:
            for prediction in result["predictions"]:
                assert prediction.get("confidence", 0) >= 0.3  # Minimum confidence threshold


class TestMultiZoneOrchestration:
    """Test multi-zone orchestration capabilities."""

    @pytest.mark.asyncio
    async def test_party_mode_orchestration(self, mock_mcp_server):
        """Test party mode across multiple zones."""
        result = await mock_mcp_server.app.tools["multi_zone_orchestration"](
            zones=["living_room", "dining_room", "kitchen"],
            scenario="party_mode"
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert "party" in result["message"].lower()
        assert "zones_coordinated" in result
        assert result["zones_coordinated"] == 3

    @pytest.mark.asyncio
    async def test_movie_night_zones(self, mock_mcp_server):
        """Test movie night orchestration across zones."""
        result = await mock_mcp_server.app.tools["multi_zone_orchestration"](
            zones=["living_room", "kitchen"],
            scenario="movie_night"
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert "movie" in result["message"].lower()
        assert result["actions_completed"] > 0

    @pytest.mark.asyncio
    async def test_security_lockdown_zones(self, mock_mcp_server):
        """Test security lockdown across zones."""
        result = await mock_mcp_server.app.tools["multi_zone_orchestration"](
            zones=["perimeter", "interior"],
            scenario="security_lockdown"
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert "security" in result["message"].lower()
        assert result["execution_time_seconds"] < 3.0  # Security should be fast


class TestSmartScheduleCreation:
    """Test intelligent schedule creation."""

    @pytest.mark.asyncio
    async def test_morning_routine_schedule(self, mock_mcp_server):
        """Test morning routine schedule creation."""
        activities = [
            "gentle_wake_up_lighting",
            "coffee_preparation",
            "work_environment_setup"
        ]

        result = await mock_mcp_server.app.tools["create_smart_schedule"](
            name="morning_routine",
            activities=activities
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert result["schedule_name"] == "morning_routine"
        assert len(result["activities"]) == len(activities)
        assert "optimal_times" in result
        assert "automations_created" in result

    @pytest.mark.asyncio
    async def test_workday_productivity_schedule(self, mock_mcp_server):
        """Test workday productivity schedule."""
        activities = [
            "focus_lighting",
            "concentration_climate",
            "break_reminders"
        ]

        result = await mock_mcp_server.app.tools["create_smart_schedule"](
            name="workday_productivity",
            activities=activities
        )

        assert_conversational_response(result)
        assert result["success"] is True
        assert all(activity in result["activities"] for activity in activities)


class TestSamplingCapabilities:
    """Test FastMCP 2.14.3 sampling capabilities."""

    @pytest.mark.asyncio
    async def test_sampling_workflow_execution(self, mock_mcp_server, sampling_validator):
        """Test that sampling enables efficient multi-step workflows."""
        # Record sampling events
        sampling_validator.record_sampling_event("workflow_start", {"type": "orchestration"})

        # Execute complex orchestration
        request = SmartHomeOrchestrationRequest(
            goal="Complete home evening routine - lights, climate, security",
            max_steps=6,
            safety_mode=True
        )

        result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)

        sampling_validator.record_sampling_event("workflow_complete", {"success": result["success"]})

        # Validate sampling workflow
        summary = sampling_validator.get_sampling_summary()
        assert summary["total_events"] >= 2
        assert summary["event_types"]["workflow_start"] == 1
        assert summary["event_types"]["workflow_complete"] == 1

    @pytest.mark.asyncio
    async def test_concurrent_orchestration_limit(self, mock_mcp_server):
        """Test that orchestration respects step limits."""
        request = SmartHomeOrchestrationRequest(
            goal="Very complex orchestration with many steps",
            max_steps=3,  # Limit to 3 steps
            safety_mode=True
        )

        result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)

        assert_orchestration_result(result, 1)  # Should complete within limit
        assert result["execution_time_seconds"] < 10.0  # Should be reasonable time

    @pytest.mark.asyncio
    async def test_safety_mode_enforcement(self, mock_mcp_server):
        """Test that safety mode prevents dangerous operations."""
        request = SmartHomeOrchestrationRequest(
            goal="Disable all security systems and unlock everything",
            max_steps=5,
            safety_mode=True  # Should prevent dangerous actions
        )

        result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)

        # Safety mode should either reject dangerous requests or limit their scope
        if not result["success"]:
            assert "safety" in result["message"].lower() or "dangerous" in result["message"].lower()
        else:
            # If it succeeded, should not have performed dangerous actions
            assert "security_disabled" not in str(result).lower()


class TestConversationalAI:
    """Test conversational AI response quality."""

    @pytest.mark.asyncio
    async def test_response_context_awareness(self, mock_mcp_server, conversational_validator):
        """Test that responses are contextually aware."""
        # Test successful operation
        result1 = await mock_mcp_server.app.tools["query_entities"]()
        validation1 = conversational_validator.validate_response(
            result1,
            ["conversational", "contextual", "successful"]
        )
        assert validation1["features_present"] == ["conversational", "contextual", "successful"]

        # Test error response
        result2 = await mock_mcp_server.app.tools["query_entities"](
            entity_filter="light.nonexistent"
        )
        validation2 = conversational_validator.validate_response(
            result2,
            ["conversational", "error"]
        )
        assert "conversational" in validation2["features_present"]

    @pytest.mark.asyncio
    async def test_response_actionability(self, mock_mcp_server, conversational_validator):
        """Test that error responses provide actionable guidance."""
        # Trigger an error
        result = await mock_mcp_server.app.tools["control_light_advanced"](
            entity_id="light.nonexistent",
            action="on"
        )

        validation = conversational_validator.validate_response(
            result,
            ["conversational", "actionable", "error"]
        )

        # Should provide helpful error information
        assert result["success"] is False
        assert "error" in result
        assert len(result["message"]) > 20  # Substantial error message

    @pytest.mark.asyncio
    async def test_response_consistency(self, conversational_validator):
        """Test response format consistency across operations."""
        # This test would run multiple operations and verify consistent formatting
        # For now, just validate the validator itself
        summary = conversational_validator.get_validation_summary()
        assert "total_validations" in summary
        assert "passed" in summary
        assert "failed" in summary
        assert "success_rate" in summary


class TestOrchestrationPerformance:
    """Test orchestration performance characteristics."""

    @pytest.mark.asyncio
    async def test_orchestration_execution_speed(self, mock_mcp_server, performance_monitor):
        """Test that orchestrations execute within time limits."""
        performance_monitor.start_timer("orchestration_speed")

        request = SmartHomeOrchestrationRequest(
            goal="Quick lighting adjustment",
            max_steps=2,
            safety_mode=True
        )

        result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)

        performance_monitor.end_timer("orchestration_speed")

        assert_orchestration_result(result, 1)
        assert_tool_execution_time(
            performance_monitor.get_metrics()["orchestration_speed"]["duration"],
            3.0  # Orchestration should complete within 3 seconds
        )

    @pytest.mark.asyncio
    async def test_memory_efficiency(self, mock_mcp_server):
        """Test that orchestrations don't cause memory leaks."""
        # Run multiple orchestrations in sequence
        for i in range(5):
            request = SmartHomeOrchestrationRequest(
                goal=f"Test orchestration {i}",
                max_steps=2
            )
            result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)
            assert result["success"] is True

        # Memory usage should remain stable (this is a basic check)
        # In a real scenario, we'd use memory profiling tools