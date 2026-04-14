"""Home Assistant REST API client (Bearer token)."""
import logging
import os

import httpx

logger = logging.getLogger("home-assistant-mcp.client")

DEFAULT_HA_URL = "http://homeassistant.local:8123"
TIMEOUT = 15.0


def _base_url() -> str:
    url = os.environ.get("HA_URL", DEFAULT_HA_URL).strip().rstrip("/")
    return f"{url}/api"


def _headers() -> dict:
    token = os.environ.get("HA_TOKEN", "").strip()
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def is_configured() -> bool:
    return bool(os.environ.get("HA_TOKEN", "").strip())


async def get_states(entity_id: str | None = None) -> list[dict] | dict:
    """GET /api/states or /api/states/<entity_id>. Returns list of state objects or single state."""
    url = _base_url()
    if entity_id:
        url = f"{url}/states/{entity_id}"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.get(url, headers=_headers())
        r.raise_for_status()
        data = r.json()
    return data


async def call_service(domain: str, service: str, data: dict | None = None) -> list[dict]:
    """POST /api/services/<domain>/<service>. Body optional service_data."""
    url = f"{_base_url()}/services/{domain}/{service}"
    body = data or {}
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.post(url, headers=_headers(), json=body)
        r.raise_for_status()
        return r.json() if r.content else []


async def get_config() -> dict:
    """GET /api/config."""
    url = f"{_base_url()}/config"
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        r = await client.get(url, headers=_headers())
        r.raise_for_status()
        return r.json()


async def get_automations() -> list[dict]:
    """Return states for entities in automation domain."""
    states = await get_states()
    if not isinstance(states, list):
        return []
    return [s for s in states if s.get("entity_id", "").startswith("automation.")]


async def trigger_automation(entity_id: str) -> list[dict]:
    """Call automation.turn_on for given entity_id."""
    return await call_service("automation", "turn_on", {"entity_id": entity_id})
