"""
Home Assistant MCP Server

FastMCP-based server providing AI-powered control of Home Assistant smart home systems.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from ..core.ha_client import HomeAssistantClient
from ..core.config import HomeAssistantConfig
from ..core.globals import initialize_ha_client as init_global_client, get_ha_client
from .tools import register_all_ha_tools

logger = logging.getLogger(__name__)


def initialize_ha_client(config: HomeAssistantConfig) -> None:
    """Initialize the global Home Assistant client."""
    client = HomeAssistantClient(config)
    init_global_client(client)
    logger.info(f"Home Assistant client initialized for {config.url}")


def create_mcp_server() -> FastMCP:
    """Create and configure the Home Assistant MCP server."""
    server = FastMCP(
        name="home-assistant-mcp",
        instructions="""
        You are a smart home assistant powered by Home Assistant.

        You can control lights, switches, climate devices, cameras, and execute automations.
        Always use natural language responses and be helpful with smart home control.

        Available capabilities:
        - Query and control all HA entities (lights, switches, sensors, etc.)
        - Execute automations and scripts
        - Monitor real-time events
        - Render templates for dynamic content
        - Manage device configuration

        Be conversational and confirm actions when appropriate.
        """,
    )

    # Register all Home Assistant tools
    register_all_ha_tools(server)

    logger.info("Home Assistant MCP server created")
    return server


async def run_server(config: HomeAssistantConfig) -> None:
    """Run the Home Assistant MCP server."""
    # Initialize HA client
    initialize_ha_client(config)

    # Create MCP server
    mcp_server = create_mcp_server()

    # Test connection
    try:
        client = get_ha_client()
        await client.test_connection()
        logger.info("Successfully connected to Home Assistant")
    except Exception as e:
        logger.error(f"Failed to connect to Home Assistant: {e}")
        raise

    # Run the MCP server
    await mcp_server.run_stdio_async()


# CLI entry point
def main() -> None:
    """Main CLI entry point."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Home Assistant MCP Server")
    parser.add_argument(
        "--url",
        default="http://localhost:8123",
        help="Home Assistant URL (default: http://localhost:8123)"
    )
    parser.add_argument(
        "--token",
        help="Home Assistant long-lived access token"
    )
    parser.add_argument(
        "--config-file",
        help="Path to YAML configuration file"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Load configuration
    if args.config_file:
        config = HomeAssistantConfig.from_yaml_file(args.config_file)
    else:
        config = HomeAssistantConfig(
            url=args.url,
            access_token=args.token
        )

    # Validate configuration
    if not config.access_token:
        print("ERROR: Home Assistant access token is required.", file=sys.stderr)
        print("Get one from: Home Assistant → Profile → Security → Long-Lived Access Tokens", file=sys.stderr)
        sys.exit(1)

    # Run server
    try:
        asyncio.run(run_server(config))
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()