import json
from jsonschema import validate, ValidationError

# Save this dictionary to a file called 'profile.json' or read it directly
user_profile_data = {
  "meta": {
    "version": "1.1.0",
    "updated_at": "2026-06-03T15:43:00Z",
    "profile_name": "My Smart Profile"
  },
  "privacy_and_communication": {
    "data_sharing": False,
    "ad_personalization": False,
    "visibility": "private"
  },
  "notifications": {
    "global_mode": "do_not_disturb"
  },
  "display": {
    "theme": "dark",
    "font_size_scale": 1.0
  },
  "sound": {
    "master_volume": 50
  },
  "smart_home": {
    "climate": {
      "preferred_unit": "F",
      "target_temperature_home": 71.5,
      "target_temperature_away": 64.0,
      "eco_mode_enabled": True
    },
    "lighting": {
      "default_brightness": 80,
      "color_temperature_kelvin": 2700,
      "adaptive_lighting": True
    }
  }
}

def validate_preferences(data, schema_file_path="schema.json"):
    """Validates the preferences dictionary against the schema file."""
    try:
        # Load the external schema file
        with open(schema_file_path, "r") as f:
            schema = json.load(f)
            
        # Run validation check
        validate(instance=data, schema=schema)
        print("✅ Validation Successful! The profile format is clean and portable.")
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: The schema definition file '{schema_file_path}' was not found.")
        return False
    except ValidationError as e:
        print("❌ Validation Failed! The profile configuration does not match the schema rules.")
        print(f"Details: {e.message} at path: {' -> '.join(str(p) for p in e.path)}")
        return False

# Execute validation
if __name__ == "__main__":
    # Assuming you have saved the schema above into 'schema.json'
    validate_preferences(user_profile_data, "schema.json")
