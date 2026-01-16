# 🎛️ Basic Control Examples

**Essential smart home control patterns and use cases**

## 💡 **Light Control Examples**

### **Simple On/Off Control**
```python
# Turn on living room lights
await control_light_advanced(LightControlRequest(
    entity_id="light.living_room",
    action="on"
))

# Turn off all bedroom lights
await control_light_advanced(LightControlRequest(
    entity_id=["light.bedroom_ceiling", "light.bedroom_lamp"],
    action="off"
))
```

### **Brightness Control**
```python
# Set bedroom light to 70% brightness
await control_light_advanced(LightControlRequest(
    entity_id="light.bedroom",
    action="on",
    brightness_pct=70
))

# Dim living room lights gradually
await control_light_advanced(LightControlRequest(
    entity_id="light.living_room",
    action="dim",
    brightness_pct=30,
    transition=2.0  # 2 second transition
))
```

### **Color Control**
```python
# Set warm white ambiance
await control_light_advanced(LightControlRequest(
    entity_id="light.dining_room",
    action="on",
    color_temp=2700,  # Warm white in Kelvin
    brightness_pct=80
))

# Romantic red lighting
await control_light_advanced(LightControlRequest(
    entity_id="light.bedroom",
    action="on",
    rgb_color=[255, 50, 100],  # Reddish pink
    brightness_pct=40
))

# Energizing blue for home office
await control_light_advanced(LightControlRequest(
    entity_id="light.office",
    action="on",
    rgb_color=[100, 150, 255],  # Cool blue
    brightness_pct=90
))
```

## 🌡️ **Climate Control Examples**

### **Temperature Control**
```python
# Set living room to comfortable temperature
await control_climate_advanced(ClimateControlRequest(
    entity_id="climate.living_room",
    action="set_temperature",
    temperature=72.0,  # 72°F
    hvac_mode="heat"
))

# Cool down the bedroom
await control_climate_advanced(ClimateControlRequest(
    entity_id="climate.bedroom",
    action="set_temperature",
    temperature=68.0,
    hvac_mode="cool"
))
```

### **HVAC Mode Control**
```python
# Enable auto mode for whole house
await control_climate_advanced(ClimateControlRequest(
    entity_id=["climate.living_room", "climate.bedroom", "climate.office"],
    action="set_hvac_mode",
    hvac_mode="auto"
))

# Turn off HVAC when away
await control_climate_advanced(ClimateControlRequest(
    entity_id="climate.whole_house",
    action="turn_off"
))
```

## 🚪 **Scene & Automation Examples**

### **Scene Activation**
```python
# Activate movie night scene
await activate_scene(SceneActivationRequest(
    entity_id="scene.movie_night",
    transition=3.0  # Smooth 3-second transition
))

# Quick morning scene activation
await activate_scene(SceneActivationRequest(
    entity_id="scene.morning_routine"
))
```

### **Automation Execution**
```python
# Execute security lockdown
await execute_automation_advanced(AutomationExecutionRequest(
    entity_id="automation.security_lockdown"
))

# Run guest arrival routine with variables
await execute_automation_advanced(AutomationExecutionRequest(
    entity_id="automation.guest_arrival",
    variables={
        "guest_name": "John",
        "stay_duration": "weekend"
    }
))
```

## 🔍 **Discovery & Query Examples**

### **Entity Discovery**
```python
# Find all lights
lights = await query_entities(EntityFilter(domain="light"))

# Get bedroom devices
bedroom_devices = await query_entities(EntityFilter(
    friendly_name="bedroom",
    device_class="motion"
))

# Check device states
current_states = await query_entities(EntityFilter(state="on"))
```

### **System Status**
```python
# Get comprehensive home status
status = await get_home_status_detailed()

# Monitor energy usage
energy = await monitor_energy_usage(hours=24)

# Check system health
health = await system_maintenance_check()
```

## 📝 **Template Examples**

### **Dynamic Content Generation**
```python
# Current weather summary
weather_summary = await render_template(TemplateRenderRequest(
    template="""
    Current weather: {{ states('weather.home') }}
    Temperature: {{ states('sensor.temperature') }}°F
    Humidity: {{ states('sensor.humidity') }}%
    """
))

# Device status summary
device_status = await render_template(TemplateRenderRequest(
    template="""
    {% set lights_on = states.light | selectattr('state', 'equalto', 'on') | list %}
    {% set sensors_offline = states.sensor | selectattr('state', 'equalto', 'unavailable') | list %}

    Lights currently on: {{ lights_on | length }}
    Sensors offline: {{ sensors_offline | length }}
    """
))
```

---

## 🎯 **Best Practices for Basic Control**

### **Consistent Naming**
- Use descriptive entity names: `light.living_room_main` vs `light.light_2`
- Group related devices: `climate.downstairs`, `climate.upstairs`

### **State Management**
- Always check device state before control operations
- Use transitions for gradual changes to avoid startling users
- Implement error handling for offline devices

### **Performance Optimization**
- Batch operations when possible (control multiple lights at once)
- Use appropriate polling intervals for status checks
- Cache frequently accessed entity states

### **User Experience**
- Provide clear feedback for all operations
- Use natural transition times (1-3 seconds for lights)
- Implement graceful degradation for failed operations