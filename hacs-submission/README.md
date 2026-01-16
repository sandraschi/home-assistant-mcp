# 🏠 Home Assistant MCP Server

[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](https://github.com/sandraschi/home-assistant-mcp)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.12+-41BDF5.svg)](https://www.home-assistant.io/)
[![MCP](https://img.shields.io/badge/MCP-2.14.3-blue.svg)](https://mcp-standard.org/)

**AI-Powered Natural Language Control for Home Assistant**

> **For the DIY Community**: This enhances your HA setup without replacing your knowledge or control. Think of it as a skilled assistant that handles the repetitive tasks while you focus on the creative automation.

## 🤔 **Why MCP for Home Assistant?**

### **The Problem**
Home Assistant is incredibly powerful, but controlling it often requires:
- Remembering entity IDs (`light.living_room_ceiling`)
- Writing YAML automation code
- Using the web interface for simple tasks
- Understanding HA's service architecture

### **The MCP Solution**
This integration brings **natural language control** to your HA setup:

```
You: "Turn on the living room lights and set the thermostat to 72°F"
AI Assistant: Uses MCP tools to discover devices → control lights → adjust climate
Result: Your home responds naturally, but you maintain full control
```

### **For the Hardware Enthusiast**
- **Your automations stay yours** - MCP enhances, doesn't replace
- **Learn by example** - See what services/entities are called
- **Debug assistance** - AI can help troubleshoot your YAML
- **Advanced control** - Complex multi-device scenarios become conversational

## 📦 **Installation**

### **Via HACS (Recommended)**

1. **Add Custom Repository**:
   - Open HACS in Home Assistant
   - Go to "Integrations" → "⋮" → "Custom repositories"
   - Add: `https://github.com/sandraschi/home-assistant-mcp`
   - Category: Integration

2. **Install**:
   - Search for "Home Assistant MCP Server"
   - Click "Download" → Select latest version
   - Restart Home Assistant

3. **Configure**:
   - Go to Settings → Devices & Services → Add Integration
   - Search for "Home Assistant MCP Server"
   - Enter your configuration (see below)

### **Manual Installation**

```bash
# Clone the repository
git clone https://github.com/sandraschi/home-assistant-mcp
cd home-assistant-mcp

# Install
pip install -e .

# Run
home-assistant-mcp --config-file config.yaml
```

## ⚙️ **Configuration**

### **Required Settings**

```yaml
# Home Assistant connection
ha_url: "http://homeassistant.local:8123"  # Your HA URL
ha_token: "your_long_lived_access_token"   # From HA → Profile → Security → Long-Lived Access Tokens

# MCP server settings
mcp_port: 8080                              # Port for MCP clients to connect
log_level: "INFO"                          # DEBUG, INFO, WARNING, ERROR
```

### **Getting Your Access Token**

1. **Open Home Assistant** → **Profile** (bottom left)
2. **Security** tab
3. **Long-Lived Access Tokens** section
4. **Create Token** → Name: "Home Assistant MCP"
5. **Copy** the generated token

## 🤖 **MCP Client Setup**

### **Claude Desktop**
Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "home-assistant": {
      "command": "home-assistant-mcp",
      "args": ["--config-file", "/path/to/config.yaml"]
    }
  }
}
```

### **Cursor IDE**
Add to Cursor MCP settings:

```json
{
  "mcpServers": {
    "home-assistant": {
      "command": "home-assistant-mcp",
      "args": ["--config-file", "/path/to/config.yaml"]
    }
  }
}
```

## 💡 **Usage Examples**

### **Basic Control**
```
"Turn on the kitchen lights"
"Set bedroom temperature to 68°F"
"What's the current status of all motion sensors?"
```

### **Complex Automation**
```
"Start my morning routine - lights, coffee maker, and news briefing"
"Set up a movie night: dim lights, close blinds, start projector"
"Prepare for guests: clean mode on robot vacuum, music in living room"
```

### **Smart Queries**
```
"Which lights are currently on?"
"Show me all devices that haven't reported in the last hour"
"What's the energy usage trend for this week?"
```

### **Learning & Debugging**
```
"How do I create an automation for sunrise lighting?"
"Why isn't my motion sensor triggering the light?"
"Show me the YAML for controlling my climate devices"
```

## 🔧 **MCP Tools Available**

| Tool | Purpose | Example |
|------|---------|---------|
| `query_entities` | Discover devices | "What lights do I have?" |
| `control_light` | Light control | "Set bedroom light to 50% warm white" |
| `control_climate` | HVAC control | "Set thermostat to 72°F heat" |
| `execute_automation` | Run automations | "Execute 'goodnight' scene" |
| `execute_script` | Run scripts | "Start the vacuum cleaning script" |
| `get_home_status` | System overview | "Show me all device statuses" |
| `render_template` | Dynamic content | "What's the average temperature today?" |

## 🛠️ **For the DIY Community**

### **This is NOT about replacing your HA knowledge**
- **Your YAML automations remain** - MCP enhances them
- **Learn by observation** - See what services are called
- **Debug assistance** - AI can help fix your configurations
- **Advanced scenarios** - Complex multi-device control made simple

### **Hardware Integration Focus**
Works perfectly with your:
- **ESPHome devices** (MQTT, API)
- **Zigbee/Z-Wave networks** (deCONZ, ZHA)
- **Custom sensors** (DHT22, soil moisture, etc.)
- **DIY projects** (Arduino, Raspberry Pi GPIO)

### **Privacy & Security**
- **Local only** - No cloud dependencies
- **Your data stays home** - MCP server runs locally
- **Full HA authentication** - Uses HA's security model
- **Audit trail** - All actions logged for review

## 🚨 **Important Notes**

### **Experimental Status**
- **Beta software** - Actively developed and tested
- **Community project** - Not officially affiliated with Home Assistant
- **Your feedback matters** - Help shape the future of AI + HA integration

### **Requirements**
- **Home Assistant**: 2024.12.0 or later
- **Python**: 3.10+ (for MCP server)
- **MCP Client**: Claude Desktop, Cursor, or compatible

### **Performance**
- **Lightweight** - Minimal resource usage
- **Async design** - Non-blocking operations
- **Connection pooling** - Efficient HA API usage

## 📚 **Documentation**

- **Full Documentation**: [Main Repository](https://github.com/sandraschi/home-assistant-mcp)
- **HA Integration Guide**: [MCP Central Docs](../../mcp-central-docs/integrations/home-assistant/)
- **API Reference**: [HA REST API](https://developers.home-assistant.io/docs/api/rest/)
- **MCP Specification**: [Model Context Protocol](https://mcp-standard.org/)

## 🆘 **Support**

- **Issues**: [GitHub Issues](https://github.com/sandraschi/home-assistant-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sandraschi/home-assistant-mcp/discussions)
- **HA Community**: Mention in [HA Forums](https://community.home-assistant.io/) with tag `mcp`

## 🙏 **Credits**

- **Home Assistant Community** - The incredible smart home platform
- **FastMCP** - Excellent MCP framework
- **Anthropic** - Claude Desktop and MCP specification

---

**Bringing AI assistance to the world's most powerful smart home platform** 🏠🤖

*Built by the DIY community, for the DIY community*