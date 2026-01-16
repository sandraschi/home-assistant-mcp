"""
Global state management for Home Assistant MCP.
"""

from typing import Optional

from .ha_client import HomeAssistantClient

# Global HA client instance
_ha_client: Optional[HomeAssistantClient] = None


def get_ha_client() -> HomeAssistantClient:
    """Get the global Home Assistant client instance."""
    if _ha_client is None:
        raise RuntimeError("Home Assistant client not initialized. Call initialize_ha_client() first.")
    return _ha_client


def initialize_ha_client(client: HomeAssistantClient) -> None:
    """Initialize the global Home Assistant client."""
    global _ha_client
    _ha_client = client