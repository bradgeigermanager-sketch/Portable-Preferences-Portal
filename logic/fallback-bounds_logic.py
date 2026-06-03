def resolve_hardware_preferences(user_profile: dict, device_hardware: dict) -> dict:
    """
    Transforms the ideal portable schema into a hardware-safe configuration
    by applying default fallbacks and enforcing hardware ranges.
    """
    resolved_settings = {}

    # --- Fallback 1: Display Theme Strategy ---
    # Scenario: User requests Dark Mode, but hardware is an E-Ink screen or basic status display.
    if device_hardware.get("supports_dark_mode", True):
        resolved_settings["display_theme"] = user_profile["display"]["theme"]
    else:
        resolved_settings["display_theme"] = "light"  # Safe default fallback

    # --- Fallback 2: Light Bulb Color Temperate Bounds Matching ---
    # Scenario: User wants warm 2,700K lighting, but bulb only supports 3,000K to 6,000K.
    requested_kelvin = user_profile["smart_home"]["lighting"]["color_temperature_kelvin"]
    
    if device_hardware.get("has_tunable_white", False):
        min_k = device_hardware.get("min_kelvin", 2700)
        max_k = device_hardware.get("max_kelvin", 6500)
        # Clamps the value safely within hardware capability limits
        resolved_settings["light_kelvin"] = max(min_k, min(max_k, requested_kelvin))
    else:
        resolved_settings["light_kelvin"] = "hardware_default_fixed_white"

    # --- Fallback 3: Missing Feature Strategy (Climate Controls) ---
    # Scenario: Profile contains precise HVAC metrics, but target device is a basic wall plug switch.
    if device_hardware.get("has_thermostat_controls", False):
        resolved_settings["temp_target"] = user_profile["smart_home"]["climate"]["target_temperature_home"]
        resolved_settings["temp_unit"] = user_profile["smart_home"]["climate"]["preferred_unit"]
    else:
        resolved_settings["temp_target"] = None  # Feature ignored gracefully by hardware

    return resolved_settings


# --- Demonstration Executable ---
if __name__ == "__main__":
    # Extracted user configuration profile
    mock_user_profile = {
        "display": {"theme": "dark"},
        "smart_home": {
            "lighting": {"default_brightness": 80, "color_temperature_kelvin": 2200},
            "climate": {"target_temperature_home": 72.0, "preferred_unit": "F"}
        }
    }

    # Restrictive hardware profile (e.g., an outdated smart screen or entry-level smart bulb)
    hardware_capabilities = {
        "supports_dark_mode": False,
        "has_tunable_white": True,
        "min_kelvin": 3000,
        "max_kelvin": 6000,
        "has_thermostat_controls": False
    }

    final_device_instructions = resolve_hardware_preferences(mock_user_profile, hardware_capabilities)
    print("Resolved Hardware Instructions:\n", final_device_instructions)
