# config.py

# Default settings
external_depth_unit ="ft"
external_length_unit= "ft"
external_diameter_unit ="in"
external_azimuth_unit = "deg"
external_area_unit = "ft2"
external_weight_unit = "lbs"
external_lineardensity_unit = "lb/ft"
external_pressure_unit = "psi"
external_torque_unit = "klbf.ft"
external_barrelofOilequivalent_unit = "boe"
external_bitnozzlediameter_unit = "in"
external_DLS_unit = "deg/100ft"
external_density_unit = "lb/gal"
external_energy_unit = "j"
external_fieldpressure_unit = "psi"
external_fluidvolume_unit = "bbl"
external_force_unit = "klbf"
external_mass_unit = "klb"
external_mudweight_unit = "lb/gal"
external_pumppressure_unit = "psi"
external_saltconcentration_unit = "lb/bbl"
external_stress_unit = "psi"
external_viscosity_unit = "cp"
external_volume_unit = "bbl"
external_velocity_unit = "ft/min"
external_unitcapacity_unit = "bbl/ft"
external_flowrate_unit = "gal/min"
external_weightonbit_unit = "klbf"
external_weightperlength = "lb/bbl"
external_temperature_unit = "degC"

user_settings = {
    external_depth_unit:"ft",
    external_length_unit: "ft",
    external_diameter_unit:"in",
    external_azimuth_unit: "deg",
    external_area_unit: "ft2",
    external_weight_unit: "lbs",
    external_lineardensity_unit: "lb/ft",
    external_pressure_unit: "psi",
    external_torque_unit: "klbf.ft",
    external_barrelofOilequivalent_unit: "boe",
    external_bitnozzlediameter_unit: "in",
    external_DLS_unit: "deg/100ft",
    external_density_unit: "lb/gal",
    external_energy_unit: "j",
    external_fieldpressure_unit: "psi",
    external_fluidvolume_unit: "bbl",
    external_force_unit: "klbf",
    external_mass_unit: "klb",
    external_mudweight_unit: "lb/gal",
    external_pumppressure_unit: "psi",
    external_saltconcentration_unit: "lb/bbl",
    external_stress_unit: "psi",
    external_viscosity_unit: "cp",
    external_volume_unit: "bbl",
    external_velocity_unit: "ft/min",
    external_unitcapacity_unit: "bbl/ft",
    external_flowrate_unit: "gal/min",
    external_weightonbit_unit: "klbf",
    external_weightperlength: "lb/bbl",
    external_temperature_unit: "degC",
}

# # main.py

# import config

# # Accessing a setting
# print(config.user_settings["depth_unit"])

# # Updating a setting
# config.user_settings["depth_unit"] = "m"

# # Verifying the update
# print(config.user_settings["depth_unit"])



# # main.py

# import config

# def update_setting(key, value):
#     if key in config.user_settings:
#         config.user_settings[key] = value
#         print(f"Updated {key} to {value}")
#     else:
#         print(f"Setting {key} not found")

# # Simulate user updating a setting
# update_setting("depth_unit", "m")


# def load_settings(filename='settings.json'):
#     try:
#         with open(filename, 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return config.user_settings  # Return default settings if file not found

# # Example usage
# config.user_settings = load_settings()
