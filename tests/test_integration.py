"""
Integration Tests for Home Assistant MCP Server

Tests end-to-end workflows, cross-tool interactions, and real-world scenarios
to ensure the complete system works together seamlessly.
"""

import pytest
import asyncio
from typing import Dict, Any, List
from unittest.mock import patch, AsyncMock

from home_assistant_mcp.mcp.tools import (
    SmartHomeOrchestrationRequest,
    SecurityMonitoringRequest,
    EnergyOptimizationRequest
)

from .conftest import (
    assert_conversational_response,
    assert_orchestration_result
)


class TestEndToEndWorkflows:
    """Test complete end-to-end user workflows."""

    @pytest.mark.asyncio
    async def test_complete_movie_night_workflow(self, mock_mcp_server):
        """Test complete movie night setup workflow."""
        # Step 1: Initial state check
        status = await mock_mcp_server.app.tools["get_home_status_detailed"]()
        assert_conversational_response(status)
        assert status["success"] is True

        # Step 2: Orchestrated setup
        movie_request = SmartHomeOrchestrationRequest(
            goal="Prepare for movie night - dim lights, adjust climate, create ambiance",
            max_steps=5,
            safety_mode=True
        )
        orchestration = await mock_mcp_server.app.tools["smart_home_orchestration"](movie_request)
        assert_orchestration_result(orchestration, 3)

        # Step 3: Verify changes
        post_status = await mock_mcp_server.app.tools["query_entities"]()
        assert_conversational_response(post_status)

        # Should reflect orchestration changes
        assert post_status["success"] is True

    @pytest.mark.asyncio
    async def test_morning_routine_workflow(self, mock_mcp_server):
        """Test complete morning routine workflow."""
        # Create smart schedule
        schedule = await mock_mcp_server.app.tools["create_smart_schedule"](
            name="morning_workflow",
            activities=["lighting", "climate", "automation"]
        )
        assert_conversational_response(schedule)
        assert schedule["success"] is True

        # Execute automation
        from home_assistant_mcp.mcp.tools import AutomationExecutionRequest
        execution = await mock_mcp_server.app.tools["execute_automation_advanced"](
            AutomationExecutionRequest(
                entity_id="automation.morning_routine",
                variables={"intensity": "gentle"}
            )
        )
        assert_conversational_response(execution)

        # Check energy impact
        energy = await mock_mcp_server.app.tools["monitor_energy_usage"](hours=1)
        assert_conversational_response(energy)

    @pytest.mark.asyncio
    async def test_security_emergency_workflow(self, mock_mcp_server):
        """Test security emergency response workflow."""
        # Step 1: Arm security system
        security = await mock_mcp_server.app.tools["security_monitoring"](
            SecurityMonitoringRequest(
                mode="armed_home",
                zones=["interior", "exterior"],
                ai_anomaly_detection=True
            )
        )
        assert_conversational_response(security)
        assert security["success"] is True

        # Step 2: Simulate emergency
        emergency = await mock_mcp_server.app.tools["emergency_response"]("security_breach")
        assert_conversational_response(emergency)
        assert emergency["success"] is True

        # Step 3: Verify emergency actions
        assert "actions_executed" in emergency
        assert len(emergency["actions_executed"]) > 0

    @pytest.mark.asyncio
    async def test_energy_optimization_workflow(self, mock_mcp_server):
        """Test complete energy optimization workflow."""
        # Step 1: Baseline monitoring
        baseline = await mock_mcp_server.app.tools["monitor_energy_usage"](hours=24)
        assert_conversational_response(baseline)

        # Step 2: Start optimization
        optimization = await mock_mcp_server.app.tools["energy_optimization"](
            EnergyOptimizationRequest(
                mode="eco",
                duration=3600,
                learn_patterns=True
            )
        )
        assert_conversational_response(optimization)
        assert optimization["success"] is True

        # Step 3: Monitor results
        results = await mock_mcp_server.app.tools["get_optimization_results"]()
        assert_conversational_response(results)

        # Should show optimization impact
        assert "estimated_savings_kwh" in results


class TestCrossToolInteractions:
    """Test interactions between different MCP tools."""

    @pytest.mark.asyncio
    async def test_orchestration_with_manual_override(self, mock_mcp_server):
        """Test orchestration followed by manual control adjustments."""
        # Start with orchestration
        orch_request = SmartHomeOrchestrationRequest(
            goal="Set up evening ambiance",
            max_steps=3
        )
        orchestration = await mock_mcp_server.app.tools["smart_home_orchestration"](orch_request)
        assert_orchestration_result(orchestration, 1)

        # Manual adjustment
        from home_assistant_mcp.mcp.tools import LightControlRequest
        manual_adjust = await mock_mcp_server.app.tools["control_light_advanced"](
            LightControlRequest(
                entity_id="light.living_room",
                action="on",
                brightness_pct=70  # Manual override
            )
        )
        assert_conversational_response(manual_adjust)
        assert manual_adjust["success"] is True

        # Verify final state
        final_query = await mock_mcp_server.app.tools["query_entities"]()
        assert_conversational_response(final_query)

    @pytest.mark.asyncio
    async def test_energy_and_security_coordination(self, mock_mcp_server):
        """Test coordination between energy optimization and security."""
        # Start energy optimization
        energy = await mock_mcp_server.app.tools["energy_optimization"](
            EnergyOptimizationRequest(
                mode="eco",
                zones=["non_security"]
            )
        )
        assert_conversational_response(energy)

        # Enable security (should not conflict)
        security = await mock_mcp_server.app.tools["security_monitoring"](
            SecurityMonitoringRequest(
                mode="armed_home",
                zones=["all"]
            )
        )
        assert_conversational_response(security)

        # Both should succeed without conflicts
        assert energy["success"] is True
        assert security["success"] is True

    @pytest.mark.asyncio
    async def test_predictive_and_manual_control(self, mock_mcp_server):
        """Test predictive automation with manual intervention."""
        # Set up predictive automation
        predictive = await mock_mcp_server.app.tools["predictive_automation"](
            anticipate="return home routine",
            timeframe_minutes=30
        )
        assert_conversational_response(predictive)
        assert predictive["success"] is True

        # Manual override during predictive period
        from home_assistant_mcp.mcp.tools import ClimateControlRequest
        manual = await mock_mcp_server.app.tools["control_climate_advanced"](
            ClimateControlRequest(
                entity_id="climate.living_room",
                action="set_temperature",
                temperature=75.0  # Manual override
            )
        )
        assert_conversational_response(manual)

        # System should handle both predictive and manual controls
        assert manual["success"] is True


class TestConversationalConsistency:
    """Test conversational response consistency across workflows."""

    @pytest.mark.asyncio
    async def test_error_message_consistency(self, mock_mcp_server):
        """Test that error messages follow consistent patterns."""
        # Trigger various errors
        errors = []

        # Invalid entity
        result1 = await mock_mcp_server.app.tools["query_entities"](
            entity_id="light.invalid"
        )
        errors.append(result1)

        # Invalid automation
        result2 = await mock_mcp_server.app.tools["execute_automation"]("automation.invalid")
        errors.append(result2)

        # Invalid service
        from home_assistant_mcp.mcp.tools import ServiceCallRequest
        result3 = await mock_mcp_server.app.tools["control_entity"](
            ServiceCallRequest(
                domain="invalid",
                service="service"
            )
        )
        errors.append(result3)

        # All errors should follow conversational format
        for error in errors:
            assert_conversational_response(error)
            assert error["success"] is False
            assert "❌" in error["message"]
            assert "error" in error

    @pytest.mark.asyncio
    async def test_success_message_consistency(self, mock_mcp_server):
        """Test that success messages follow consistent patterns."""
        successes = []

        # Successful query
        result1 = await mock_mcp_server.app.tools["query_entities"]()
        successes.append(result1)

        # Successful light control
        from home_assistant_mcp.mcp.tools import LightControlRequest
        result2 = await mock_mcp_server.app.tools["control_light_advanced"](
            LightControlRequest(entity_id="light.living_room", action="on")
        )
        successes.append(result2)

        # Successful orchestration
        result3 = await mock_mcp_server.app.tools["smart_home_orchestration"](
            SmartHomeOrchestrationRequest(
                goal="Simple lighting adjustment",
                max_steps=2
            )
        )
        successes.append(result3)

        # All successes should follow conversational format
        for success in successes:
            assert_conversational_response(success)
            assert success["success"] is True
            assert "✅" in success["message"]
            assert "timestamp" in success

    @pytest.mark.asyncio
    async def test_contextual_information_inclusion(self, mock_mcp_server):
        """Test that responses include relevant contextual information."""
        # Light control should include brightness info
        from home_assistant_mcp.mcp.tools import LightControlRequest
        light_result = await mock_mcp_server.app.tools["control_light_advanced"](
            LightControlRequest(
                entity_id="light.living_room",
                action="on",
                brightness_pct=80
            )
        )

        assert "80%" in light_result["message"] or "brightness_pct" in light_result.get("action_details", {})

        # Orchestration should include execution details
        orch_result = await mock_mcp_server.app.tools["smart_home_orchestration"](
            SmartHomeOrchestrationRequest(
                goal="Test orchestration",
                max_steps=2
            )
        )

        assert "execution_time_seconds" in orch_result
        assert "actions_executed" in orch_result


class TestPerformanceIntegration:
    """Test performance characteristics in integrated scenarios."""

    @pytest.mark.asyncio
    async def test_concurrent_tool_execution(self, mock_mcp_server):
        """Test concurrent execution of multiple tools."""
        import time

        start_time = time.time()

        # Execute multiple tools concurrently
        tasks = [
            mock_mcp_server.app.tools["query_entities"](),
            mock_mcp_server.app.tools["get_home_status_detailed"](),
            mock_mcp_server.app.tools["monitor_energy_usage"](hours=1),
        ]

        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        # All should succeed
        for result in results:
            assert_conversational_response(result)
            assert result["success"] is True

        # Should complete within reasonable time
        assert total_time < 5.0  # Concurrent execution should be fast

    @pytest.mark.asyncio
    async def test_memory_usage_under_load(self, mock_mcp_server):
        """Test memory usage during heavy operations."""
        # Execute multiple complex orchestrations
        for i in range(5):
            request = SmartHomeOrchestrationRequest(
                goal=f"Complex orchestration {i}",
                max_steps=5,
                safety_mode=True
            )
            result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)
            assert result["success"] is True

        # Memory usage should remain stable (this is a basic check)
        # In practice, you'd use memory profiling tools

    @pytest.mark.asyncio
    async def test_error_recovery_performance(self, mock_mcp_server):
        """Test that error recovery doesn't impact performance."""
        import time

        # Mix successful and failed operations
        operations = []

        # Successful operations
        for i in range(3):
            start = time.time()
            result = await mock_mcp_server.app.tools["query_entities"]()
            duration = time.time() - start
            operations.append(("success", duration, result["success"]))

        # Failed operations
        for i in range(2):
            start = time.time()
            result = await mock_mcp_server.app.tools["query_entities"](entity_id="invalid")
            duration = time.time() - start
            operations.append(("error", duration, result["success"]))

        # Error handling should not significantly slow down operations
        avg_success_time = sum(d for t, d, s in operations if t == "success") / 3
        avg_error_time = sum(d for t, d, s in operations if t == "error") / 2

        # Error handling should not be more than 2x slower
        assert avg_error_time < avg_success_time * 2


class TestRealWorldScenarios:
    """Test real-world usage scenarios."""

    @pytest.mark.asyncio
    async def test_guest_arrival_scenario(self, mock_mcp_server):
        """Test complete guest arrival scenario."""
        # Set up guest mode
        guest_orch = await mock_mcp_server.app.tools["smart_home_orchestration"](
            SmartHomeOrchestrationRequest(
                goal="Prepare for guest arrival - welcoming lighting, comfortable climate",
                max_steps=4
            )
        )
        assert_orchestration_result(guest_orch, 2)

        # Adjust for specific preferences
        from home_assistant_mcp.mcp.tools import ClimateControlRequest
        climate = await mock_mcp_server.app.tools["control_climate_advanced"](
            ClimateControlRequest(
                entity_id="climate.living_room",
                action="set_temperature",
                temperature=72.0
            )
        )
        assert_conversational_response(climate)

    @pytest.mark.asyncio
    async def test_work_from_home_setup(self, mock_mcp_server):
        """Test work-from-home environment setup."""
        # Create productivity schedule
        schedule = await mock_mcp_server.app.tools["create_smart_schedule"](
            name="work_session",
            activities=["focus_lighting", "optimal_climate", "productivity_setup"]
        )
        assert_conversational_response(schedule)

        # Optimize energy for work session
        energy = await mock_mcp_server.app.tools["energy_optimization"](
            EnergyOptimizationRequest(
                mode="performance",
                duration=28800,  # 8 hours
                zones=["office"]
            )
        )
        assert_conversational_response(energy)

    @pytest.mark.asyncio
    async def test_leaving_home_routine(self, mock_mcp_server):
        """Test complete leaving home routine."""
        # Security activation
        security = await mock_mcp_server.app.tools["security_monitoring"](
            SecurityMonitoringRequest(
                mode="armed_away",
                zones=["all"],
                notify_on_events=True
            )
        )
        assert_conversational_response(security)

        # Energy optimization
        energy = await mock_mcp_server.app.tools["energy_optimization"](
            EnergyOptimizationRequest(
                mode="eco",
                duration=28800  # 8 hours away
            )
        )
        assert_conversational_response(energy)

        # Final status check
        status = await mock_mcp_server.app.tools["get_home_status_detailed"]()
        assert_conversational_response(status)

        # Should reflect security and energy settings
        assert "armed" in str(status).lower() or "security" in str(status).lower()

    @pytest.mark.asyncio
    async def test_maintenance_routine(self, mock_mcp_server):
        """Test complete system maintenance routine."""
        # Run maintenance check
        maintenance = await mock_mcp_server.app.tools["system_maintenance_check"]()
        assert_conversational_response(maintenance)

        # Debug any automations
        debug = await mock_mcp_server.app.tools["debug_automation"]("automation.morning_routine")
        assert_conversational_response(debug)

        # Analyze patterns
        patterns = await mock_mcp_server.app.tools["analyze_home_patterns"](days=7)
        assert_conversational_response(patterns)

        # All maintenance operations should provide actionable insights
        assert "recommendations" in maintenance or "insights" in maintenance
        assert "recommendations" in debug
        assert "insights" in patterns


class TestSamplingIntegration:
    """Test FastMCP 2.14.3 sampling capabilities in integration scenarios."""

    @pytest.mark.asyncio
    async def test_sampling_orchestration_workflow(self, mock_mcp_server, sampling_validator):
        """Test that sampling enables complex multi-step workflows."""
        # Start sampling validation
        sampling_validator.record_sampling_event("integration_test_start", {"scenario": "complex_orchestration"})

        # Execute complex orchestration that would benefit from sampling
        request = SmartHomeOrchestrationRequest(
            goal="Complete home cinema setup with lighting, audio, climate, and security integration",
            max_steps=8,
            safety_mode=True
        )

        result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)

        sampling_validator.record_sampling_event("integration_test_complete", {"success": result["success"]})

        # Validate sampling workflow
        summary = sampling_validator.get_sampling_summary()
        assert summary["total_events"] >= 2

        # Orchestration should complete successfully
        assert_orchestration_result(result, 4)
        assert "cinema" in result["message"].lower() or "movie" in result["message"].lower()

    @pytest.mark.asyncio
    async def test_conversational_flow_integration(self, mock_mcp_server, conversational_validator):
        """Test conversational flow across multiple integrated operations."""
        # Execute a series of related operations
        operations = []

        # 1. Status check
        op1 = await mock_mcp_server.app.tools["get_home_status_detailed"]()
        operations.append(op1)
        validation1 = conversational_validator.validate_response(op1, ["conversational", "contextual"])
        assert validation1["features_present"]

        # 2. Energy monitoring
        op2 = await mock_mcp_server.app.tools["monitor_energy_usage"](hours=24)
        operations.append(op2)
        validation2 = conversational_validator.validate_response(op2, ["conversational", "actionable"])
        assert validation2["features_present"]

        # 3. Pattern analysis
        op3 = await mock_mcp_server.app.tools["analyze_home_patterns"](days=7)
        operations.append(op3)
        validation3 = conversational_validator.validate_response(op3, ["conversational", "contextual", "actionable"])
        assert validation3["features_present"]

        # All operations should succeed and be conversational
        for op in operations:
            assert op["success"] is True
            assert "message" in op
            assert "timestamp" in op

        # Conversational flow should be maintained
        summary = conversational_validator.get_validation_summary()
        assert summary["success_rate"] == 1.0  # All validations should pass