"""PyInstaller entry point for home-assistant-mcp HTTP sidecar."""
import _strptime  # noqa: F401
import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    base = Path(sys._MEIPASS)
else:
    base = Path(__file__).resolve().parent
if str(base) not in sys.path:
    sys.path.insert(0, str(base))

port = int(os.environ.get("MCP_PORT", os.environ.get("PORT", "10835")))
host = os.environ.get("MCP_HOST", "127.0.0.1")

from web_sota.backend.server import app
import uvicorn
uvicorn.run(app, host=host, port=port, log_level="info")
