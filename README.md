# 🏠 Home Assistant MCP Server

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/sandraschi/home-assistant-mcp/releases)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.14.3-green.svg)](https://github.com/jlowin/fastmcp)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.12+-41BDF5.svg)](https://www.home-assistant.io/)

**AI-Powered Smart Home Control via Model Context Protocol**

Transform your Home Assistant smart home into a conversational AI assistant. Control lights, climate, automations, and all your smart devices using natural language through Claude Desktop and other MCP-compatible AI assistants.

## 🌟 **Why Home Assistant MCP?**

### **🤖 AI-Powered Smart Home Control**
- **Natural Language Control**: "Turn on the living room lights and set the thermostat to 72°F"
- **Context-Aware Automation**: AI understands your home layout and device relationships
- **Intelligent Suggestions**: AI learns your preferences and suggests optimizations
- **Multi-Device Orchestration**: Control complex device interactions with simple commands

### **🔗 Seamless Integration**
- **MCP Protocol**: Works with Claude Desktop, Cursor, and other MCP-compatible tools
- **Home Assistant Native**: Direct integration with HA's REST and WebSocket APIs
- **Real-Time Events**: Live monitoring of device states and home events
- **Template Support**: Dynamic content generation using Jinja2 templates

### **🏠 Complete Smart Home Coverage**
- **Lights & Switches**: Brightness, color, scenes, groups
- **Climate Control**: Thermostats, HVAC modes, temperature scheduling
- **Security**: Cameras, motion sensors, door sensors, alarms
- **Media**: Speakers, TVs, streaming devices
- **Energy**: Smart plugs, appliances, solar monitoring
- **Automation**: Scripts, automations, scenes
- **Sensors**: Temperature, humidity, air quality, presence

## 📋 **Table of Contents**

1. [Quick Start](#-quick-start)
2. [Installation](#-installation)
3. [Configuration](#-configuration)
4. [MCP Tools](#-mcp-tools)
5. [Usage Examples](#-usage-examples)
6. [Integration with Existing Systems](#-integration-with-existing-systems)
7. [Troubleshooting](#-troubleshooting)
8. [Development](#-development)
9. [Contributing](#-contributing)

## 🚀 **Quick Start**

### **Prerequisites**
- **Home Assistant**: Running instance (local or remote)
- **Long-Lived Access Token**: From HA → Profile → Security → Long-Lived Access Tokens
- **Python 3.10+**: For the MCP server
- **MCP Client**: Claude Desktop, Cursor, or compatible MCP client

### **1. Install the MCP Server**

```bash
# Clone the repository
git clone https://github.com/sandraschi/home-assistant-mcp
cd home-assistant-mcp

# Install with pip
pip install -e .

# Or with uv (recommended)
uv sync
```

### **2. Configure Home Assistant Connection**

```bash
# Set environment variables
export HA_URL="http://localhost:8123"
export HA_ACCESS_TOKEN="your_long_lived_access_token_here"

# Or create a config file
cat > ha_config.yaml << EOF
homeassistant:
  url: "http://localhost:8123"
  access_token: "your_long_lived_access_token_here"
EOF
```

### **3. Test the Connection**

```bash
# Test with the CLI
home-assistant-mcp --url http://localhost:8123 --token your_token --debug

# Or with config file
home-assistant-mcp --config-file ha_config.yaml
```

### **4. Configure MCP Client**

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "home-assistant": {
      "command": "home-assistant-mcp",
      "args": ["--config-file", "/path/to/ha_config.yaml"]
    }
  }
}
```

### **5. Start Controlling Your Home!**

Once configured, you can use natural language commands like:
- *"Turn on the kitchen lights"*
- *"Set the living room temperature to 72°F"*
- *"Show me all motion sensors that are active"*
- *"Execute the 'goodnight' automation"*

## 📦 **Installation**

### **From Source (Development)**

```bash
git clone https://github.com/sandraschi/home-assistant-mcp
cd home-assistant-mcp
pip install -e ".[dev]"
```

### **Via pip (when published)**

```bash
pip install home-assistant-mcp
```

### **Via uv**

```bash
uv add home-assistant-mcp
```

### **Docker**

```bash
docker run -e HA_URL=http://host.docker.internal:8123 \
           -e HA_ACCESS_TOKEN=your_token \
           ghcr.io/sandraschi/home-assistant-mcp:latest
```

## ⚙️ **Configuration**

### **Environment Variables**

```bash
# Required
HA_URL=http://localhost:8123                    # Home Assistant URL
HA_ACCESS_TOKEN=your_long_lived_token          # Access token

# Optional
HA_TIMEOUT=30.0                                # Request timeout (seconds)
HA_VERIFY_SSL=true                             # SSL verification
HA_CACHE_TTL=300                               # Cache TTL (seconds)
HA_MAX_CONCURRENT_REQUESTS=10                  # Concurrent request limit
```

### **YAML Configuration File**

```yaml
homeassistant:
  url: "http://localhost:8123"
  access_token: "your_long_lived_access_token"
  timeout: 30.0
  verify_ssl: true
  cache_ttl: 300
  max_concurrent_requests: 10
```

### **Getting Your Access Token**

1. **Open Home Assistant** in your web browser
2. **Go to Profile** (bottom left menu)
3. **Security** tab
4. **Long-Lived Access Tokens** section
5. **Create Token** button
6. **Name**: "Home Assistant MCP"
7. **Copy** the generated token

## 🛠️ **MCP Tools**

### **Entity Management**
- **`query_entities`**: Discover and filter all HA entities
- **`control_entity`**: Universal service calling for any entity
- **`get_home_status`**: Comprehensive system status

### **Device Control**
- **`control_light`**: Light control with brightness/color
- **`control_climate`**: HVAC and thermostat control

### **Automation**
- **`execute_automation`**: Trigger HA automations
- **`execute_script`**: Run HA scripts with variables

### **Advanced Features**
- **`render_template`**: Jinja2 template rendering
- **`get_available_events`**: Event subscription discovery

### **Tool Capabilities**

| Tool | Purpose | Example Use |
|------|---------|-------------|
| `query_entities` | Device discovery | "What lights do I have?" |
| `control_light` | Lighting control | "Turn on bedroom lights to 50% brightness" |
| `control_climate` | Temperature control | "Set thermostat to 72°F" |
| `execute_automation` | Scene activation | "Run the 'movie night' automation" |
| `render_template` | Dynamic content | "Show current temperature in all rooms" |
| `get_home_status` | System overview | "How many devices are online?" |

## 💡 **Usage Examples**

### **Basic Device Control**

```
User: "Turn on the living room lights"
Assistant: Uses control_light tool with entity_id: "light.living_room", action: "on"

User: "Set bedroom temperature to 68°F"
Assistant: Uses control_climate tool with temperature control
```

### **Complex Automation**

```
User: "Start my morning routine"
Assistant:
1. Uses query_entities to find relevant devices
2. Uses execute_automation for "morning_routine"
3. Uses control_light for specific lighting adjustments
4. Reports status of all changes
```

### **Intelligent Queries**

```
User: "Which motion sensors are currently active?"
Assistant:
1. Uses query_entities with domain: "binary_sensor", device_class: "motion"
2. Filters for state: "on"
3. Returns formatted list with locations and timestamps
```

### **Template Rendering**

```
User: "Show me a summary of my home status"
Assistant:
1. Uses render_template with Jinja2 template
2. Incorporates live entity data
3. Returns formatted status report
```

## 🔗 **Integration with Existing Systems**

### **Tapo Camera MCP**
- **Camera Control**: Direct integration with IP cameras
- **Unified Dashboard**: Cameras appear in HA device list
- **Automation Triggers**: Camera events trigger HA automations
- **Repository**: [sandraschi/tapo-camera-mcp](https://github.com/sandraschi/tapo-camera-mcp)

### **Virtualization MCP**
- **HA VM Management**: Automated Home Assistant deployment
- **Snapshot/Restore**: Backup and recovery of HA configurations
- **Resource Control**: Dedicated compute resources for HA
- **Repository**: [sandraschi/virtualization-mcp](https://github.com/sandraschi/virtualization-mcp)

### **Basic Memory**
- **Knowledge Management**: Persistent conversation context across sessions
- **Documentation Storage**: Store HA automation documentation and procedures
- **Query Integration**: Link HA device states with knowledge base
- **Repository**: [sandraschi/basic-memory](https://github.com/sandraschi/basic-memory)

### **Advanced Memory MCP**
- **Enhanced Knowledge**: AI-powered knowledge graph for smart home documentation
- **Context Preservation**: Maintain complex automation workflows and device relationships
- **Search Integration**: Find relevant HA information across all documentation
- **Repository**: [sandraschi/advanced-memory-mcp](https://github.com/sandraschi/advanced-memory-mcp)

### **FastSearch MCP**
- **Rapid File Discovery**: Instantly locate HA configuration files and logs
- **Content Search**: Find specific automation rules and device configurations
- **NTFS Integration**: Direct filesystem access for maximum performance
- **Repository**: [sandraschi/fastsearch-mcp](https://github.com/sandraschi/fastsearch-mcp)

### **Email MCP**
- **Notification Integration**: Send HA alerts via email
- **Report Generation**: Automated email reports of HA system status
- **Event Monitoring**: Email notifications for important HA events
- **Repository**: [sandraschi/email-mcp](https://github.com/sandraschi/email-mcp)

### **Docker MCP**
- **Container Management**: Deploy HA add-ons and custom containers
- **Service Orchestration**: Manage HA-related Docker services
- **Log Monitoring**: Access container logs for troubleshooting
- **Repository**: [sandraschi/docker-mcp](https://github.com/sandraschi/docker-mcp)

### **Filesystem MCP**
- **Configuration Management**: Backup and restore HA configurations
- **Log Analysis**: Parse and analyze HA log files
- **Automation Scripts**: Manage HA automation files and scripts
- **Repository**: [sandraschi/filesystem-mcp](https://github.com/sandraschi/filesystem-mcp)

### **Monitoring MCP**
- **System Health**: Monitor HA performance and resource usage
- **Alert Integration**: Create monitoring alerts for HA services
- **Metrics Collection**: Track HA uptime and response times
- **Repository**: [sandraschi/monitoring-mcp](https://github.com/sandraschi/monitoring-mcp)

### **MCP Central Docs**
- **Comprehensive Documentation**: [Home Assistant Integration Guide](../../mcp-central-docs/integrations/home-assistant/)
- **Architecture Overview**: Understanding HA's unique ecosystem
- **Troubleshooting**: Common issues and solutions
- **Repository**: [sandraschi/mcp-central-docs](https://github.com/sandraschi/mcp-central-docs)

## 🔧 **Troubleshooting**

### **Connection Issues**

#### **"Connection refused"**
```bash
# Check HA is running
curl http://localhost:8123/api/

# Check firewall
sudo ufw allow 8123

# Check Docker networking
docker network inspect bridge
```

#### **Authentication Failed**
```bash
# Verify token
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8123/api/

# Check token expiration
# Create new token in HA → Profile → Security
```

### **MCP Client Issues**

#### **Tool Not Available**
```json
// Check MCP configuration
{
  "mcpServers": {
    "home-assistant": {
      "command": "home-assistant-mcp",
      "args": ["--config-file", "ha_config.yaml"]
    }
  }
}
```

#### **Timeout Errors**
```yaml
# Increase timeout in config
homeassistant:
  timeout: 60.0  # Increase from default 30
```

### **Performance Issues**

#### **Slow Response Times**
- **Enable Caching**: Set `cache_ttl` to reduce API calls
- **Limit Concurrent Requests**: Reduce `max_concurrent_requests`
- **Use Local HA**: Prefer local over remote HA instances

#### **Memory Usage**
- **Monitor Entity Count**: Large HA installations may need more resources
- **Filter Queries**: Use specific entity filters instead of querying all
- **Close Connections**: Ensure proper connection cleanup

### **Debug Mode**

```bash
# Enable debug logging
home-assistant-mcp --config-file ha_config.yaml --debug

# Check HA logs
tail -f /config/home-assistant.log
```

## 🧪 **Development**

### **Setting Up Development Environment**

```bash
git clone https://github.com/sandraschi/home-assistant-mcp
cd home-assistant-mcp

# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run linter
uv run ruff check .

# Format code
uv run ruff format .
```

### **Testing with Mock HA**

```python
# Use mock HA for development
from home_assistant_mcp.core.mock_ha import MockHAClient

# Replace real client for testing
client = MockHAClient()
```

### **Contributing**

1. **Fork** the repository
2. **Create** a feature branch
3. **Write** tests for new functionality
4. **Ensure** all tests pass
5. **Submit** a pull request

### **Architecture**

```
home-assistant-mcp/
├── core/                    # Core functionality
│   ├── config.py           # Configuration management
│   ├── ha_client.py        # HA API client
│   └── mock_ha.py          # Testing mocks
├── mcp/                    # MCP protocol implementation
│   ├── server.py           # FastMCP server
│   └── tools.py            # MCP tools
├── tools/                  # Additional utilities
└── tests/                  # Test suite
```

## 📊 **System Requirements**

### **Minimum Requirements**
- **Python**: 3.10+
- **Memory**: 100MB RAM
- **Storage**: 50MB disk
- **Network**: Access to Home Assistant instance

### **Recommended for Production**
- **Python**: 3.11+
- **Memory**: 256MB RAM
- **Storage**: 200MB disk
- **Network**: Low-latency connection to HA

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### **Development Status**
- **Core Features**: ✅ Implemented
- **MCP Integration**: ✅ FastMCP 2.14.3
- **Testing**: 🟡 In Progress
- **Documentation**: 🟡 In Progress
- **Production Ready**: 🔴 Alpha Release

### **Roadmap**
- [ ] WebSocket event streaming
- [ ] Device discovery automation
- [ ] Voice integration (Alexa/Google)
- [ ] Energy monitoring dashboard
- [ ] Multi-HA instance support

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Home Assistant Community**: For creating the amazing smart home platform
- **FastMCP**: For the excellent MCP framework
- **Anthropic**: For Claude Desktop and MCP specification

---

**Transform your smart home into a conversational AI assistant with Home Assistant MCP!** 🏠🤖