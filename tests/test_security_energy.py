"""
Security and Energy Features Tests

Tests for security monitoring, emergency response, energy optimization,
and safety-critical automation features.
"""

import asyncio

import pytest
from conftest import assert_conversational_response

from home_assistant_mcp.mcp.tools import EnergyOptimizationRequest, SecurityMonitoringRequest


class TestSecurityMonitoring:
    """Test security system monitoring and control."""

    @pytest.mark.asyncio
    async def test_security_arm_home(self, tool_functions):
        """Test arming security system in home mode."""
        request = SecurityMonitoringRequest(
            mode="armed_home",
            zones=["interior"],
            notify_on_events=True,
            ai_anomaly_detection=True
        )

        result = await tool_functions["security_monitoring"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "armed_home" in result["message"]
        assert result["security_mode"] == "armed_home"
        assert result["ai_anomaly_detection"] is True
        assert "current_status" in result

    @pytest.mark.asyncio
    async def test_security_arm_away(self, tool_functions):
        """Test arming security system in away mode."""
        request = SecurityMonitoringRequest(
            mode="armed_away",
            zones=["interior", "exterior", "perimeter"],
            notify_on_events=True
        )

        result = await tool_functions["security_monitoring"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "armed_away" in result["message"]
        assert result["security_mode"] == "armed_away"
        assert len(result["monitored_zones"]) >= 3

    @pytest.mark.asyncio
    async def test_security_disarm(self, tool_functions):
        """Test disarming security system."""
        request = SecurityMonitoringRequest(
            mode="disarmed",
            zones=[]
        )

        result = await tool_functions["security_monitoring"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "disarmed" in result["message"]
        assert result["security_mode"] == "disarmed"

    @pytest.mark.asyncio
    async def test_security_with_ai_anomaly_detection(self, tool_functions):
        """Test security monitoring with AI anomaly detection."""
        request = SecurityMonitoringRequest(
            mode="armed_home",
            ai_anomaly_detection=True,
            notify_on_events=True
        )

        result = await tool_functions["security_monitoring"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert result["ai_anomaly_detection"] is True
        assert "AI anomaly detection is active" in result["recommendations"]


class TestEmergencyResponse:
    """Test emergency response orchestration."""

    @pytest.mark.asyncio
    async def test_fire_emergency_response(self, tool_functions):
        """Test fire emergency response protocol."""
        result = await tool_functions["emergency_response"]("fire_detected")

        assert_conversational_response(result)
        assert result["success"] is True
        assert "fire_detected" in result["message"]
        assert "actions_executed" in result
        assert "safety_measures" in result
        assert result["execution_time_seconds"] > 0
        assert result["execution_time_seconds"] < 5.0  # Emergency should be fast

    @pytest.mark.asyncio
    async def test_security_breach_response(self, tool_functions):
        """Test security breach emergency response."""
        result = await tool_functions["emergency_response"]("security_breach")

        assert_conversational_response(result)
        assert result["success"] is True
        assert "security_breach" in result["message"]
        assert len(result["actions_executed"]) > 0
        assert "notifications_sent" in result

    @pytest.mark.asyncio
    async def test_medical_emergency_response(self, tool_functions):
        """Test medical emergency response."""
        result = await tool_functions["emergency_response"]("medical_emergency")

        assert_conversational_response(result)
        assert result["success"] is True
        assert "medical_emergency" in result["message"]
        assert "emergency_contacts" in str(result).lower() or "medical" in str(result).lower()

    @pytest.mark.asyncio
    async def test_emergency_response_timing(self, tool_functions):
        """Test that emergency responses execute quickly."""
        import time

        start_time = time.time()
        result = await tool_functions["emergency_response"]("fire_detected")
        execution_time = time.time() - start_time

        assert result["success"] is True
        assert execution_time < 2.0  # Emergency response should be under 2 seconds
        assert result["execution_time_seconds"] < 2.0


class TestEnergyOptimization:
    """Test energy optimization and monitoring."""

    @pytest.mark.asyncio
    async def test_energy_eco_mode(self, tool_functions):
        """Test energy optimization in eco mode."""
        request = EnergyOptimizationRequest(
            mode="eco",
            duration=3600,  # 1 hour
            learn_patterns=True,
            zones=["living_areas", "bedrooms"]
        )

        result = await tool_functions["energy_optimization"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "eco mode" in result["message"]
        assert result["optimization_mode"] == "eco"
        assert result["duration"] == 3600
        assert "estimated_savings_kwh" in result
        assert result["learning_enabled"] is True

    @pytest.mark.asyncio
    async def test_energy_comfort_mode(self, tool_functions):
        """Test energy optimization in comfort mode."""
        request = EnergyOptimizationRequest(
            mode="comfort",
            duration=7200,  # 2 hours
            learn_patterns=True
        )

        result = await tool_functions["energy_optimization"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "comfort mode" in result["message"]
        assert result["optimization_mode"] == "comfort"
        assert result["estimated_savings_kwh"] >= 0

    @pytest.mark.asyncio
    async def test_energy_performance_mode(self, tool_functions):
        """Test energy optimization in performance mode."""
        request = EnergyOptimizationRequest(
            mode="performance",
            duration=1800,  # 30 minutes
            learn_patterns=False
        )

        result = await tool_functions["energy_optimization"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "performance mode" in result["message"]
        assert result["learning_enabled"] is False

    @pytest.mark.asyncio
    async def test_energy_optimization_zones(self, tool_functions):
        """Test energy optimization for specific zones."""
        request = EnergyOptimizationRequest(
            mode="eco",
            zones=["living_room", "kitchen", "bedroom"],
            duration=3600
        )

        result = await tool_functions["energy_optimization"](request)

        assert_conversational_response(result)
        assert result["success"] is True
        assert "living_room" in result["target_zones"]
        assert "kitchen" in result["target_zones"]
        assert "bedroom" in result["target_zones"]


class TestEnergyMonitoring:
    """Test energy usage monitoring and analysis."""

    @pytest.mark.asyncio
    async def test_energy_monitoring_24h(self, tool_functions):
        """Test 24-hour energy monitoring."""
        result = await tool_functions["monitor_energy_usage"](hours=24)

        assert_conversational_response(result)
        assert result["success"] is True
        assert result["period_hours"] == 24
        assert "total_consumption_kwh" in result
        assert "consumption_by_device" in result
        assert "insights" in result
        assert isinstance(result["insights"], list)

    @pytest.mark.asyncio
    async def test_energy_monitoring_weekly(self, tool_functions):
        """Test weekly energy monitoring."""
        result = await tool_functions["monitor_energy_usage"](hours=168)  # 1 week

        assert_conversational_response(result)
        assert result["success"] is True
        assert result["period_hours"] == 168
        assert "savings_opportunities" in result
        assert "efficiency_score" in result

    @pytest.mark.asyncio
    async def test_energy_high_consumption_detection(self, tool_functions):
        """Test detection of high energy consumption."""
        result = await tool_functions["monitor_energy_usage"](hours=24)

        assert_conversational_response(result)
        # Should identify high consumers
        insights = " ".join(result["insights"]).lower()
        assert "top" in insights or "consumer" in insights or "usage" in insights

    @pytest.mark.asyncio
    async def test_energy_savings_recommendations(self, tool_functions):
        """Test energy savings recommendations."""
        result = await tool_functions["monitor_energy_usage"](hours=48)

        assert_conversational_response(result)
        assert "savings_opportunities" in result
        assert isinstance(result["savings_opportunities"], list)

        # Should have at least basic recommendations
        if result["total_consumption_kwh"] > 5:
            assert len(result["savings_opportunities"]) > 0


class TestSystemMaintenance:
    """Test system maintenance and health monitoring."""

    @pytest.mark.asyncio
    async def test_comprehensive_maintenance_check(self, tool_functions):
        """Test full system maintenance check."""
        result = await tool_functions["system_maintenance_check"]()

        assert_conversational_response(result)
        assert result["success"] is True
        assert "overall_health" in result
        assert "issues" in result
        assert "maintenance_tasks" in result
        assert "performance_metrics" in result

    @pytest.mark.asyncio
    async def test_maintenance_health_assessment(self, tool_functions):
        """Test system health assessment."""
        result = await tool_functions["system_maintenance_check"]()

        health = result["overall_health"]
        assert health in ["good", "warning", "critical"]

        if health == "good":
            assert len(result["issues"]) == 0
        elif health == "warning":
            assert len(result["issues"]) > 0
            assert all(issue["severity"] in ["info", "warning"] for issue in result["issues"])
        elif health == "critical":
            assert len(result["issues"]) > 0
            assert any(issue["severity"] == "critical" for issue in result["issues"])

    @pytest.mark.asyncio
    async def test_maintenance_performance_metrics(self, tool_functions):
        """Test performance metrics in maintenance check."""
        result = await tool_functions["system_maintenance_check"]()

        metrics = result["performance_metrics"]
        assert "response_time" in metrics
        assert "memory_usage" in metrics
        assert metrics["response_time"] > 0
        assert metrics["memory_usage"] > 0

    @pytest.mark.asyncio
    async def test_maintenance_task_recommendations(self, tool_functions):
        """Test maintenance task recommendations."""
        result = await tool_functions["system_maintenance_check"]()

        tasks = result["maintenance_tasks"]
        assert isinstance(tasks, list)

        # Should recommend common maintenance tasks
        task_names = [task.lower() for task in tasks]
        common_tasks = ["backup", "update", "clean", "optimize", "monitor"]
        has_common_task = any(any(ct in task for ct in common_tasks) for task in task_names)
        assert has_common_task, "Should recommend common maintenance tasks"


class TestAutomationDebugging:
    """Test automation debugging and analysis."""

    @pytest.mark.asyncio
    async def test_automation_debugging_basic(self, tool_functions):
        """Test basic automation debugging."""
        result = await tool_functions["debug_automation"]("automation.morning_routine")

        assert_conversational_response(result)
        assert result["success"] is True
        assert result["automation_id"] == "automation.morning_routine"
        assert "issues_found" in result
        assert "recommendations" in result

    @pytest.mark.asyncio
    async def test_automation_debugging_with_issues(self, tool_functions):
        """Test debugging automation with known issues."""
        result = await tool_functions["debug_automation"]("automation.problematic")

        assert_conversational_response(result)
        assert result["success"] is True
        assert len(result["issues_found"]) > 0
        assert len(result["recommendations"]) > 0

    @pytest.mark.asyncio
    async def test_automation_debugging_performance(self, tool_functions):
        """Test automation debugging performance analysis."""
        result = await tool_functions["debug_automation"]("automation.morning_routine")

        assert "performance_metrics" in result
        metrics = result["performance_metrics"]
        assert isinstance(metrics, dict)

    @pytest.mark.asyncio
    async def test_automation_debugging_test_results(self, tool_functions):
        """Test automation debugging test execution."""
        result = await tool_functions["debug_automation"]("automation.morning_routine")

        assert "test_results" in result
        test_results = result["test_results"]
        assert isinstance(test_results, dict)
        assert len(test_results) > 0


class TestPatternAnalysis:
    """Test pattern analysis and learning features."""

    @pytest.mark.asyncio
    async def test_pattern_analysis_weekly(self, tool_functions):
        """Test weekly pattern analysis."""
        result = await tool_functions["analyze_home_patterns"](days=7)

        assert_conversational_response(result)
        assert result["success"] is True
        assert result["analysis_period_days"] == 7
        assert "peak_usage_hours" in result
        assert "energy_waste" in result
        assert "efficiency_score" in result

    @pytest.mark.asyncio
    async def test_pattern_analysis_monthly(self, tool_functions):
        """Test monthly pattern analysis."""
        result = await tool_functions["analyze_home_patterns"](days=30)

        assert_conversational_response(result)
        assert result["success"] is True
        assert result["data_quality"] == "high"
        assert len(result["insights"]) > 0

    @pytest.mark.asyncio
    async def test_pattern_analysis_insights(self, tool_functions):
        """Test pattern analysis insights generation."""
        result = await tool_functions["analyze_home_patterns"](days=7)

        insights = result["insights"]
        assert isinstance(insights, list)
        assert len(insights) > 0

        # Should contain actionable insights
        insight_text = " ".join(insights).lower()
        actionable_words = ["consider", "optimize", "reduce", "improve", "adjust"]
        has_actionable = any(word in insight_text for word in actionable_words)
        assert has_actionable, "Insights should be actionable"

    @pytest.mark.asyncio
    async def test_pattern_analysis_recommendations(self, tool_functions):
        """Test pattern analysis recommendations."""
        result = await tool_functions["analyze_home_patterns"](days=14)

        # Should generate specific recommendations
        assert "recommendations" in result or "insights" in result


class TestSecurityPerformance:
    """Test security system performance and reliability."""

    @pytest.mark.asyncio
    async def test_security_response_time(self, tool_functions):
        """Test security system response time."""
        import time

        start_time = time.time()
        request = SecurityMonitoringRequest(
            mode="armed_away",
            zones=["all"],
            ai_anomaly_detection=True
        )
        result = await tool_functions["security_monitoring"](request)
        response_time = time.time() - start_time

        assert result["success"] is True
        assert response_time < 2.0  # Security should respond quickly

    @pytest.mark.asyncio
    async def test_emergency_response_reliability(self, tool_functions):
        """Test emergency response reliability under load."""
        # Execute multiple emergency responses
        tasks = []
        for i in range(3):
            task = tool_functions["emergency_response"](f"emergency_{i}")
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        # All should succeed
        for result in results:
            assert result["success"] is True
            assert "execution_time_seconds" in result
            assert result["execution_time_seconds"] < 3.0

    @pytest.mark.asyncio
    async def test_energy_optimization_safety(self, tool_functions):
        """Test that energy optimization doesn't compromise safety."""
        request = EnergyOptimizationRequest(
            mode="eco",
            duration=3600,
            zones=["security_zones"]
        )

        result = await tool_functions["energy_optimization"](request)

        assert result["success"] is True
        # Should not disable security-critical systems
        assert "security_disabled" not in str(result).lower()
        assert "safety_compromised" not in str(result).lower()
