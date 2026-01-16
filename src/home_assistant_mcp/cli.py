"""
CLI module for Home Assistant MCP server.
"""

import sys
from .mcp.server import main

if __name__ == "__main__":
    sys.exit(main())