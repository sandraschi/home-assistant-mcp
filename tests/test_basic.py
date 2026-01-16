"""
Basic tests for Home Assistant MCP server.
"""

import pytest
from home_assistant_mcp.core.config import HomeAssistantConfig
from home_assistant_mcp.core.ha_client import HomeAssistantClient


def test_config_creation():
    """Test Home Assistant configuration creation."""
    config = HomeAssistantConfig(
        url="http://localhost:8123",
        access_token="test_token"
    )

    assert config.url == "http://localhost:8123"
    assert config.websocket_url == "ws://localhost:8123/api/websocket"
    assert config.get_token_value() == "test_token"


def test_config_from_yaml():
    """Test loading configuration from YAML."""
    import tempfile
    import yaml

    config_data = {
        "homeassistant": {
            "url": "http://test:8123",
            "access_token": "yaml_token",
            "timeout": 60.0
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(config_data, f)
        config_file = f.name

    try:
        config = HomeAssistantConfig.from_yaml_file(config_file)
        assert config.url == "http://test:8123"
        assert config.get_token_value() == "yaml_token"
        assert config.timeout == 60.0
    finally:
        import os
        os.unlink(config_file)


def test_ha_client_initialization():
    """Test Home Assistant client initialization."""
    config = HomeAssistantConfig(
        url="http://localhost:8123",
        access_token="test_token"
    )

    client = HomeAssistantClient(config)
    assert client.config.url == "http://localhost:8123"
    assert client.session is None  # Not connected yet


@pytest.mark.asyncio
async def test_ha_client_connection_test():
    """Test HA client connection testing (will fail without real HA)."""
    config = HomeAssistantConfig(
        url="http://invalid:8123",
        access_token="test_token"
    )

    client = HomeAssistantClient(config)

    # This should fail gracefully
    result = await client.test_connection()
    assert result is False