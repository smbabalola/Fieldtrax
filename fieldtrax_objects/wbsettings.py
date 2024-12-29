import json
import config

def save_settings(settings, filename='settings.json'):
    with open(filename, 'w') as f:
        json.dump(settings, f)

# Example usage
#save_settings(config.user_settings)

def load_settings(filename='settings.json'):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return config.user_settings  # Return default settings if file not found

def update_setting(key, value):
    if key in config.user_settings:
        config.user_settings[key] = value
        save_settings(config.user_settings)
        print(f"Updated {key} to {value}")
    else:
        print(f"Setting {key} not found")

# Load settings at the start
config.user_settings = load_settings()

# Simulate user updating a setting
update_setting("depth_unit", "m")

# Verify the update
print(config.user_settings["depth_unit"])
