"""
Home Assistant MCP Configuration

Configuration management for Home Assistant MCP server.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, SecretStr
import yaml


class HomeAssistantConfig(BaseModel):
    """Configuration for Home Assistant MCP server."""

    url: str = Field(
        default="http://localhost:8123",
        description="Home Assistant base URL"
    )

    access_token: Optional[SecretStr] = Field(
        default=None,
        description="Long-lived access token for Home Assistant API"
    )

    websocket_url: Optional[str] = Field(
        default=None,
        description="WebSocket URL (auto-derived from url if not specified)"
    )

    timeout: float = Field(
        default=30.0,
        description="Request timeout in seconds"
    )

    verify_ssl: bool = Field(
        default=True,
        description="Verify SSL certificates"
    )

    cache_ttl: int = Field(
        default=300,
        description="Cache TTL for entity states (seconds)"
    )

    max_concurrent_requests: int = Field(
        default=10,
        description="Maximum concurrent API requests"
    )

    def __init__(self, **data):
        super().__init__(**data)

        # Auto-generate WebSocket URL if not provided
        if not self.websocket_url:
            if self.url.startswith("https://"):
                self.websocket_url = self.url.replace("https://", "wss://") + "/api/websocket"
            else:
                self.websocket_url = self.url.replace("http://", "ws://") + "/api/websocket"

    @classmethod
    def from_yaml_file(cls, file_path: str | Path) -> "HomeAssistantConfig":
        """Load configuration from YAML file."""
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Handle nested homeassistant config
        if "homeassistant" in data:
            data = data["homeassistant"]

        return cls(**data)

    @classmethod
    def from_env(cls) -> "HomeAssistantConfig":
        """Load configuration from environment variables."""
        return cls(
            url=os.getenv("HA_URL", "http://localhost:8123"),
            access_token=os.getenv("HA_ACCESS_TOKEN"),
            timeout=float(os.getenv("HA_TIMEOUT", "30.0")),
            verify_ssl=os.getenv("HA_VERIFY_SSL", "true").lower() == "true",
        )

    def get_token_value(self) -> Optional[str]:
        """Get the actual token value (for internal use)."""
        return self.access_token.get_secret_value() if self.access_token else None

    def validate_connection(self) -> bool:
        """Validate that the configuration has required connection details."""
        return bool(self.url and self.access_token)