"""
Performance Tests for Home Assistant MCP Server

Comprehensive performance benchmarking, load testing, and optimization validation
for the state-of-the-art HA MCP implementation.
"""

import pytest
import asyncio
import time
import statistics
from typing import Dict, Any, List
import psutil
import os

from home_assistant_mcp.mcp.tools import SmartHomeOrchestrationRequest

from .conftest import assert_tool_execution_time


class TestResponseTimeBenchmarks:
    """Test response time performance benchmarks."""

    @pytest.fixture
    def performance_metrics(self):
        """Performance metrics collector."""
        return {
            "response_times": [],
            "memory_usage": [],
            "cpu_usage": [],
            "timestamps": []
        }

    @pytest.mark.asyncio
    async def test_query_entities_performance(self, mock_mcp_server, performance_metrics):
        """Benchmark query_entities response time."""
        # Warm up
        await mock_mcp_server.app.tools["query_entities"]()

        # Benchmark
        for i in range(10):
            start_time = time.time()
            result = await mock_mcp_server.app.tools["query_entities"]()
            end_time = time.time()

            assert result["success"] is True

            response_time = end_time - start_time
            performance_metrics["response_times"].append(response_time)
            performance_metrics["memory_usage"].append(psutil.Process().memory_info().rss / 1024 / 1024)  # MB
            performance_metrics["cpu_usage"].append(psutil.cpu_percent(interval=0.1))
            performance_metrics["timestamps"].append(time.time())

        # Performance assertions
        avg_response_time = statistics.mean(performance_metrics["response_times"])
        p95_response_time = statistics.quantiles(performance_metrics["response_times"], n=20)[18]  # 95th percentile

        # Query should be fast
        assert avg_response_time < 0.1, f"Average response time {avg_response_time:.3f}s exceeds 100ms"
        assert p95_response_time < 0.2, f"P95 response time {p95_response_time:.3f}s exceeds 200ms"

    @pytest.mark.asyncio
    async def test_light_control_performance(self, mock_mcp_server):
        """Benchmark light control response time."""
        response_times = []

        # Test multiple light control operations
        for i in range(5):
            start_time = time.time()

            from home_assistant_mcp.mcp.tools import LightControlRequest
            result = await mock_mcp_server.app.tools["control_light_advanced"](
                LightControlRequest(
                    entity_id="light.living_room",
                    action="toggle"
                )
            )

            end_time = time.time()

            assert result["success"] is True
            response_times.append(end_time - start_time)

        avg_time = statistics.mean(response_times)
        assert avg_time < 0.5, f"Light control avg time {avg_time:.3f}s exceeds 500ms"

    @pytest.mark.asyncio
    async def test_orchestration_performance(self, mock_mcp_server):
        """Benchmark orchestration performance."""
        orchestration_times = []

        for i in range(3):
            start_time = time.time()

            request = SmartHomeOrchestrationRequest(
                goal=f"Performance test orchestration {i}",
                max_steps=3
            )

            result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)
            end_time = time.time()

            assert result["success"] is True
            orchestration_times.append(end_time - start_time)

        avg_time = statistics.mean(orchestration_times)
        assert avg_time < 3.0, f"Orchestration avg time {avg_time:.3f}s exceeds 3s"

        # Orchestration should scale reasonably
        max_time = max(orchestration_times)
        assert max_time < 5.0, f"Max orchestration time {max_time:.3f}s exceeds 5s"


class TestLoadTesting:
    """Load testing for concurrent operations."""

    @pytest.mark.asyncio
    async def test_concurrent_queries(self, mock_mcp_server):
        """Test concurrent entity queries."""
        async def single_query():
            result = await mock_mcp_server.app.tools["query_entities"]()
            return result["success"]

        # Execute 20 concurrent queries
        tasks = [single_query() for _ in range(20)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # All should succeed
        assert all(results), "Some concurrent queries failed"

        total_time = end_time - start_time
        avg_time_per_query = total_time / 20

        # Concurrent queries should be reasonably fast
        assert avg_time_per_query < 0.5, f"Avg concurrent query time {avg_time_per_query:.3f}s too slow"
        assert total_time < 5.0, f"Total concurrent execution {total_time:.3f}s too slow"

    @pytest.mark.asyncio
    async def test_mixed_workload_performance(self, mock_mcp_server):
        """Test mixed workload performance."""
        operations = []

        # Mix of different operation types
        async def run_query():
            result = await mock_mcp_server.app.tools["query_entities"]()
            return ("query", result["success"], time.time())

        async def run_light_control():
            from home_assistant_mcp.mcp.tools import LightControlRequest
            result = await mock_mcp_server.app.tools["control_light_advanced"](
                LightControlRequest(entity_id="light.living_room", action="toggle")
            )
            return ("light", result["success"], time.time())

        async def run_orchestration():
            request = SmartHomeOrchestrationRequest(goal="Quick test", max_steps=2)
            result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)
            return ("orchestration", result["success"], time.time())

        # Execute mixed workload
        start_time = time.time()
        tasks = []
        for i in range(5):
            tasks.extend([run_query(), run_light_control(), run_orchestration()])

        results = await asyncio.gather(*tasks)
        end_time = time.time()

        # Analyze results
        operation_counts = {"query": 0, "light": 0, "orchestration": 0}
        successful_operations = 0

        for op_type, success, timestamp in results:
            operation_counts[op_type] += 1
            if success:
                successful_operations += 1

        # All operations should succeed
        assert successful_operations == len(results), f"{len(results) - successful_operations} operations failed"

        total_time = end_time - start_time
        avg_time_per_operation = total_time / len(results)

        # Mixed workload should complete within reasonable time
        assert total_time < 15.0, f"Mixed workload took {total_time:.3f}s"
        assert avg_time_per_operation < 1.0, f"Avg operation time {avg_time_per_operation:.3f}s too slow"

    @pytest.mark.asyncio
    async def test_memory_usage_under_load(self, mock_mcp_server):
        """Test memory usage during load."""
        initial_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

        # Generate load
        tasks = []
        for i in range(50):
            if i % 3 == 0:
                task = mock_mcp_server.app.tools["query_entities"]()
            elif i % 3 == 1:
                from home_assistant_mcp.mcp.tools import LightControlRequest
                task = mock_mcp_server.app.tools["control_light_advanced"](
                    LightControlRequest(entity_id="light.living_room", action="toggle")
                )
            else:
                request = SmartHomeOrchestrationRequest(goal=f"Load test {i}", max_steps=2)
                task = mock_mcp_server.app.tools["smart_home_orchestration"](request)
            tasks.append(task)

        await asyncio.gather(*tasks)

        final_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50, f"Memory increased by {memory_increase:.1f}MB during load test"


class TestScalabilityTesting:
    """Test scalability characteristics."""

    @pytest.mark.asyncio
    async def test_entity_count_scalability(self, mock_mcp_server):
        """Test performance with varying entity counts."""
        # This would test with different numbers of entities
        # For now, test with current mock data
        result = await mock_mcp_server.app.tools["query_entities"]()
        assert result["success"] is True

        # Should handle current entity count efficiently
        assert result["count"] > 0
        assert "entities" in result

    @pytest.mark.asyncio
    async def test_orchestration_complexity_scaling(self, mock_mcp_server):
        """Test orchestration performance with increasing complexity."""
        complexity_levels = [2, 3, 5, 8]  # max_steps
        execution_times = []

        for complexity in complexity_levels:
            start_time = time.time()

            request = SmartHomeOrchestrationRequest(
                goal=f"Complexity {complexity} orchestration",
                max_steps=complexity
            )

            result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)
            end_time = time.time()

            assert result["success"] is True
            execution_times.append(end_time - start_time)

        # Execution time should scale reasonably with complexity
        # Allow some variance but not exponential growth
        for i in range(1, len(execution_times)):
            ratio = execution_times[i] / execution_times[i-1]
            assert ratio < 3.0, f"Execution time scaled poorly: {ratio:.2f}x increase from complexity {complexity_levels[i-1]} to {complexity_levels[i]}"


class TestResourceEfficiency:
    """Test resource usage efficiency."""

    @pytest.mark.asyncio
    async def test_cpu_usage_during_operations(self, mock_mcp_server):
        """Test CPU usage during intensive operations."""
        # Baseline CPU
        baseline_cpu = psutil.cpu_percent(interval=0.1)

        # Intensive operation
        start_time = time.time()
        tasks = []
        for i in range(10):
            request = SmartHomeOrchestrationRequest(
                goal=f"CPU test {i}",
                max_steps=5
            )
            tasks.append(mock_mcp_server.app.tools["smart_home_orchestration"](request))

        await asyncio.gather(*tasks)
        end_time = time.time()

        # Peak CPU during operation
        peak_cpu = psutil.cpu_percent(interval=0.1)

        # CPU usage should be reasonable
        assert peak_cpu < 90, f"Peak CPU usage {peak_cpu}% too high"

        execution_time = end_time - start_time
        cpu_time_ratio = (peak_cpu * execution_time) / 100  # Rough estimate

        # Should be efficient
        assert cpu_time_ratio < execution_time * 2, "CPU usage inefficient"

    @pytest.mark.asyncio
    async def test_idle_resource_usage(self, mock_mcp_server):
        """Test resource usage when idle."""
        # Let system settle
        await asyncio.sleep(0.5)

        memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        cpu_usage = psutil.cpu_percent(interval=0.5)

        # Idle usage should be reasonable
        assert memory_usage < 200, f"Idle memory usage {memory_usage:.1f}MB too high"
        assert cpu_usage < 10, f"Idle CPU usage {cpu_usage:.1f}% too high"


class TestReliabilityTesting:
    """Test system reliability under various conditions."""

    @pytest.mark.asyncio
    async def test_operation_consistency(self, mock_mcp_server):
        """Test that operations produce consistent results."""
        # Run same operation multiple times
        results = []
        for i in range(5):
            result = await mock_mcp_server.app.tools["query_entities"]()
            results.append(result)

        # All results should be consistent
        first_result = results[0]
        for result in results[1:]:
            assert result["success"] == first_result["success"]
            assert result["count"] == first_result["count"]
            assert len(result["entities"]) == len(first_result["entities"])

    @pytest.mark.asyncio
    async def test_error_recovery_consistency(self, mock_mcp_server):
        """Test that error recovery is consistent."""
        error_results = []

        # Trigger same error multiple times
        for i in range(3):
            result = await mock_mcp_server.app.tools["query_entities"](entity_id="invalid")
            error_results.append(result)

        # All errors should be handled consistently
        for result in error_results:
            assert result["success"] is False
            assert "message" in result
            assert "error" in result
            assert "❌" in result["message"]

    @pytest.mark.asyncio
    async def test_concurrent_operation_isolation(self, mock_mcp_server):
        """Test that concurrent operations don't interfere with each other."""
        async def isolated_operation(op_id: int):
            # Each operation uses different entities to avoid conflicts
            entities = ["light.living_room", "light.bedroom", "climate.living_room"]

            if op_id % 2 == 0:
                # Query operation
                result = await mock_mcp_server.app.tools["query_entities"]()
                return ("query", result["success"])
            else:
                # Control operation
                from home_assistant_mcp.mcp.tools import LightControlRequest
                result = await mock_mcp_server.app.tools["control_light_advanced"](
                    LightControlRequest(
                        entity_id=entities[op_id % len(entities)],
                        action="toggle"
                    )
                )
                return ("control", result["success"])

        # Run concurrent operations
        tasks = [isolated_operation(i) for i in range(10)]
        results = await asyncio.gather(*tasks)

        # All operations should succeed without interference
        for op_type, success in results:
            assert success, f"{op_type} operation failed in concurrent execution"


class TestBenchmarkReporting:
    """Generate comprehensive benchmark reports."""

    @pytest.mark.asyncio
    async def test_performance_report_generation(self, mock_mcp_server):
        """Test that performance reports can be generated."""
        # Run various operations to collect data
        operations = []

        # Quick operations
        for i in range(5):
            start = time.time()
            result = await mock_mcp_server.app.tools["query_entities"]()
            end = time.time()
            operations.append(("query", end - start, result["success"]))

        # Complex operations
        for i in range(3):
            start = time.time()
            request = SmartHomeOrchestrationRequest(goal=f"Benchmark {i}", max_steps=3)
            result = await mock_mcp_server.app.tools["smart_home_orchestration"](request)
            end = time.time()
            operations.append(("orchestration", end - start, result["success"]))

        # Generate report
        report = {
            "timestamp": time.time(),
            "operations": operations,
            "summary": {
                "total_operations": len(operations),
                "successful_operations": sum(1 for _, _, success in operations if success),
                "average_response_time": statistics.mean(time for _, time, _ in operations),
                "p95_response_time": statistics.quantiles([time for _, time, _ in operations], n=20)[18]
            }
        }

        # Report should be comprehensive
        assert report["summary"]["total_operations"] == len(operations)
        assert report["summary"]["successful_operations"] == len(operations)  # All should succeed
        assert report["summary"]["average_response_time"] > 0
        assert report["summary"]["p95_response_time"] > 0

        # Save report for analysis
        import json
        with open("performance_report.json", "w") as f:
            json.dump(report, f, indent=2)

        # Cleanup
        if os.path.exists("performance_report.json"):
            os.remove("performance_report.json")