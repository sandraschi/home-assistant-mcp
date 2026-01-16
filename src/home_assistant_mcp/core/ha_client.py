"""
Home Assistant API Client

Handles all communication with Home Assistant REST and WebSocket APIs.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Callable
import aiohttp
import websockets
from websockets.exceptions import ConnectionClosed

from .config import HomeAssistantConfig

logger = logging.getLogger(__name__)


class HomeAssistantClient:
    """Client for Home Assistant API communication."""

    def __init__(self, config: HomeAssistantConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.event_listeners: Dict[str, List[Callable]] = {}
        self._message_id = 0

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()

    async def connect(self) -> None:
        """Establish connection to Home Assistant."""
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers={
                    "Authorization": f"Bearer {self.config.get_token_value()}",
                    "Content-Type": "application/json",
                }
            )
        logger.info(f"Connected to Home Assistant at {self.config.url}")

    async def disconnect(self) -> None:
        """Close connections to Home Assistant."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None

        if self.session:
            await self.session.close()
            self.session = None

        logger.info("Disconnected from Home Assistant")

    async def test_connection(self) -> bool:
        """Test connection to Home Assistant."""
        try:
            async with self.session.get(f"{self.config.url}/api/") as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Connected to HA {data.get('ha_version', 'unknown version')}")
                    return True
                else:
                    logger.error(f"HA API returned status {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    async def get_states(self, entity_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all entity states, optionally filtered."""
        try:
            async with self.session.get(f"{self.config.url}/api/states") as response:
                response.raise_for_status()
                states = await response.json()

                if entity_filter:
                    # Simple filtering by entity_id or domain
                    filter_lower = entity_filter.lower()
                    states = [
                        state for state in states
                        if filter_lower in state["entity_id"].lower() or
                        filter_lower in state.get("attributes", {}).get("friendly_name", "").lower()
                    ]

                return states
        except Exception as e:
            logger.error(f"Failed to get states: {e}")
            return []

    async def get_state(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get state of a specific entity."""
        try:
            async with self.session.get(f"{self.config.url}/api/states/{entity_id}") as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    logger.warning(f"Entity not found: {entity_id}")
                    return None
                else:
                    response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to get state for {entity_id}: {e}")
            return None

    async def call_service(
        self,
        domain: str,
        service: str,
        entity_id: Optional[str] = None,
        **kwargs
    ) -> bool:
        """Call a Home Assistant service."""
        try:
            data = kwargs.copy()
            if entity_id:
                data["entity_id"] = entity_id

            async with self.session.post(
                f"{self.config.url}/api/services/{domain}/{service}",
                json=data
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Service {domain}.{service} called successfully")
                return True

        except Exception as e:
            logger.error(f"Failed to call service {domain}.{service}: {e}")
            return False

    async def get_config(self) -> Optional[Dict[str, Any]]:
        """Get Home Assistant configuration."""
        try:
            async with self.session.get(f"{self.config.url}/api/config") as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Failed to get config: {e}")
            return None

    async def render_template(self, template: str, variables: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Render a Jinja2 template."""
        try:
            data = {"template": template}
            if variables:
                data["variables"] = variables

            async with self.session.post(
                f"{self.config.url}/api/template",
                json=data
            ) as response:
                response.raise_for_status()
                result = await response.json()
                return result.get("result")
        except Exception as e:
            logger.error(f"Failed to render template: {e}")
            return None

    async def get_events(self) -> List[Dict[str, Any]]:
        """Get available events."""
        try:
            async with self.session.get(f"{self.config.url}/api/events") as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            logger.error(f"Failed to get events: {e}")
            return []

    async def execute_automation(self, automation_entity_id: str) -> bool:
        """Execute a Home Assistant automation."""
        return await self.call_service("automation", "trigger", entity_id=automation_entity_id)

    async def execute_script(self, script_entity_id: str, **variables) -> bool:
        """Execute a Home Assistant script."""
        return await self.call_service("script", "turn_on", entity_id=script_entity_id, **variables)

    async def control_light(
        self,
        entity_id: str,
        action: str,
        brightness: Optional[int] = None,
        rgb_color: Optional[List[int]] = None,
        **kwargs
    ) -> bool:
        """Control a light entity."""
        service_map = {
            "on": "turn_on",
            "off": "turn_off",
            "toggle": "toggle"
        }

        if action not in service_map:
            logger.error(f"Unknown light action: {action}")
            return False

        service = service_map[action]
        data = kwargs.copy()

        if brightness is not None:
            data["brightness"] = brightness
        if rgb_color is not None:
            data["rgb_color"] = rgb_color

        return await self.call_service("light", service, entity_id=entity_id, **data)

    async def control_climate(
        self,
        entity_id: str,
        action: str,
        temperature: Optional[float] = None,
        hvac_mode: Optional[str] = None,
        **kwargs
    ) -> bool:
        """Control a climate entity."""
        service_map = {
            "set_temperature": "set_temperature",
            "set_hvac_mode": "set_hvac_mode",
            "turn_on": "turn_on",
            "turn_off": "turn_off"
        }

        if action not in service_map:
            logger.error(f"Unknown climate action: {action}")
            return False

        service = service_map[action]
        data = kwargs.copy()

        if temperature is not None:
            data["temperature"] = temperature
        if hvac_mode is not None:
            data["hvac_mode"] = hvac_mode

        return await self.call_service("climate", service, entity_id=entity_id, **data)

    async def get_entity_info(self) -> Dict[str, Any]:
        """Get comprehensive information about all entities."""
        states = await self.get_states()
        config = await self.get_config()
        events = await self.get_events()

        # Group entities by domain
        by_domain = {}
        for state in states:
            domain = state["entity_id"].split(".")[0]
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(state)

        return {
            "total_entities": len(states),
            "entities_by_domain": {domain: len(entities) for domain, entities in by_domain.items()},
            "ha_config": config,
            "available_events": len(events),
            "domains": list(by_domain.keys())
        }

    def _get_next_message_id(self) -> int:
        """Get next WebSocket message ID."""
        self._message_id += 1
        return self._message_id

    async def connect_websocket(self) -> None:
        """Connect to Home Assistant WebSocket API."""
        try:
            self.websocket = await websockets.connect(
                self.config.websocket_url,
                extra_headers={
                    "Authorization": f"Bearer {self.config.get_token_value()}"
                }
            )

            # Authenticate
            auth_msg = {
                "type": "auth",
                "access_token": self.config.get_token_value()
            }
            await self.websocket.send(json.dumps(auth_msg))

            # Wait for auth response
            response = await self.websocket.recv()
            auth_response = json.loads(response)

            if auth_response.get("type") == "auth_ok":
                logger.info("WebSocket authentication successful")
            else:
                raise Exception(f"WebSocket auth failed: {auth_response}")

        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            self.websocket = None
            raise

    async def subscribe_events(self, event_type: str = "state_changed") -> None:
        """Subscribe to Home Assistant events."""
        if not self.websocket:
            await self.connect_websocket()

        msg = {
            "id": self._get_next_message_id(),
            "type": "subscribe_events",
            "event_type": event_type
        }

        await self.websocket.send(json.dumps(msg))
        logger.info(f"Subscribed to {event_type} events")

    async def listen_events(self) -> None:
        """Listen for WebSocket events (runs indefinitely)."""
        if not self.websocket:
            await self.connect_websocket()

        try:
            async for message in self.websocket:
                event_data = json.loads(message)

                if event_data.get("type") == "event":
                    event = event_data.get("event", {})
                    event_type = event.get("event_type")

                    # Notify listeners
                    if event_type in self.event_listeners:
                        for listener in self.event_listeners[event_type]:
                            try:
                                await listener(event)
                            except Exception as e:
                                logger.error(f"Event listener error: {e}")

        except ConnectionClosed:
            logger.warning("WebSocket connection closed")
        except Exception as e:
            logger.error(f"WebSocket listen error: {e}")

    def add_event_listener(self, event_type: str, callback: Callable) -> None:
        """Add an event listener for a specific event type."""
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(callback)