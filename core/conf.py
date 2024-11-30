# config.py

# Configuration settings for the simulation
# This file contains all the parameters and settings used to define the behavior and appearance
# of the cellular automata simulation.

config = {
    # Visualization settings
    "tint": False,  # Use tint for better visual representation of pollution levels

    # Default simulation parameters
    "default_grid_size": (10, 10, 10),  # Dimensions of the simulation grid (X, Y, Z)
    "default_days": 50,  # Duration of the simulation in days

    # Cell type configurations:
    # 0: Ocean | 1: Desert | 2: Cloud | 3: Ice | 4: Forest | 5: City | 6: Air | 7: Rain | 8: Vacuum
    "baseline_temperature": [
        15,   # Ocean: Warm temperature
        30,   # Desert: Hot temperature
        5,    # Cloud: Cool temperature
        -15,  # Ice: Freezing temperature
        20,   # Forest: Moderate temperature
        35,   # City: Hot temperature due to urban heat
        10,   # Air: Cool temperature
        12,   # Rain: Mild temperature
        -20   # Vacuum: Near absolute zero temperature
    ],

    # Pollution levels for different cell types
    "baseline_pollution_level": [
        3,   # Ocean: Some pollution from industrial waste and microplastics
        10,  # Desert: Dust and localized human activity
        1,   # Cloud: Minimal pollution
        0,   # Ice: Pristine areas with negligible pollution
        2,   # Forest: Absorbs pollution, very low levels
        20,  # City: High pollution due to vehicles and factories
        5,   # Air: Variable pollution based on proximity to cities
        0,   # Rain: Cleanses the atmosphere
        0,   # Vacuum: No pollution in empty space
    ],

    # Weight of interaction between different cell types
    "cell_type_weights": {
        0: 1.0,  # Ocean
        1: 1.2,  # Desert
        2: 0.7,  # Cloud
        3: 0.8,  # Ice
        4: 1.5,  # Forest
        5: 2.0,  # City
        6: 0.5,  # Air
        7: 1.0,  # Rain
        8: 0.0,  # Vacuum (no interaction)
    },

   # Forest-specific settings
    "forest_pollution_absorption_rate": 0.2,  # Rate at which forests absorb pollution
    "forest_cooling_effect": 0.2,  # Cooling effect of forests on their environment

    # City-specific settings
    "city_pollution_increase_rate": 0.1,  # Rate of pollution increase in cities
    "city_warming_effect": 0.1,  # Warming effect of cities on their environment
    "city_temperature_upper_limit": 100,  # Maximum temperature cities can reach
    "city_pollution_upper_limit": 100,  # Maximum pollution level cities can reach

    # Ratios for land cell types in the initial grid
    "initial_ratios": {
        "forest": 0.4,  # Proportion of forest cells
        "city": 0.4,    # Proportion of city cells
        "desert": 0.1,  # Proportion of desert cells
        "vacuum": 0.1,  # Proportion of vacuum cells
    },

    # Temperature thresholds for specific behaviors
    "temperature_extinction_point": 60,  # Maximum temperature before extinction effects
    "freezing_point": -15,              # Temperature at which water freezes
    "melting_point": 20,                # Temperature at which ice melts
    "evaporation_point": 35,            # Temperature at which water evaporates

    # Thresholds and rates for water transfer and pollution effects
    "water_transfer_threshold": 0.05,  # Minimum difference in water mass for transfer
    "pollution_damage_threshold": 10.0,  # Pollution level causing damage to ecosystems
    "pollution_level_tipping_point": 50,  # Point at which pollution accelerates damage
    "natural_pollution_decay_rate": 0.1,  # Rate of pollution decay over time

    # Rates for natural changes in temperature
    "natural_temperature_decay_rate": 0.1,  # Rate of temperature equalization to baseline

    # Cloud-specific settings
    "cloud_saturation_threshold": 3.0,  # Minimum water mass for clouds to precipitate as rain

    # Rates for environmental changes
    "melting_rate": 0.15,  # Rate at which ice melts
    "evaporation_rate": 0.05,  # Rate at which water evaporates

    # Base colors for visual representation of cell types
    "base_colors": {
        6: (1.0, 1.0, 1.0, 0.1),  # Air (transparent white)
        2: (0.7, 0.7, 0.7, 1.0),  # Cloud (light gray)
        0: (0.0, 0.3, 1.0, 1.0),  # Ocean (deep blue)
        3: (0.6, 0.8, 1.0, 1.0),  # Ice (light cyan)
        7: (0.5, 0.5, 1.0, 1.0),  # Rain (grayish blue)
        1: (1.0, 0.8, 0.5, 1.0),  # Desert (sandy gold)
        4: (0.0, 0.6, 0.0, 1.0),  # Forest (lush green)
        5: (0.4, 0.0, 0.4, 1.0),  # City (dark purple)
        8: (0.0, 0.0, 0.0, 0.0),  # Vacuum (fully transparent/black)
    },
}

# Labels for configuration keys to provide context in the UI or logs
key_labels = {
    "baseline_temperature": "Baseline Temperature (°C)",
    "cell_type_weights": "Cell Type Weights",
    "baseline_pollution_level": "Baseline Pollution Levels",
    "temperature_extinction_point": "Temperature Extinction Point (°C)",
    "freezing_point": "Freezing Point (°C)",
    "melting_point": "Melting Point (°C)",
    "evaporation_point": "Evaporation Point (°C)",
    "water_transfer_threshold": "Water Transfer Threshold",
    "pollution_damage_threshold": "Pollution Damage Threshold",
    "pollution_level_tipping_point": "Pollution Tipping Point",
    "natural_pollution_decay_rate": "Natural Pollution Decay Rate",
    "natural_temperature_decay_rate": "Natural Temperature Decay Rate",
    "cloud_saturation_threshold": "Cloud Saturation Threshold",
    "melting_rate": "Melting Rate",
    "evaporation_rate": "Evaporation Rate",
    "forest_pollution_absorption_rate": "Forest Pollution Absorption Rate",
    "forest_cooling_effect": "Forest Cooling Effect",
    "city_pollution_increase_rate": "City Pollution Increase Rate",
    "city_warming_effect": "City Warming Effect",
    "city_temperature_upper_limit": "City Temperature Upper Limit (°C)",
    "city_pollution_upper_limit": "City Pollution Upper Limit",
    "initial_ratios": "Initial Ratios (Proportions)",
    "default_grid_size": "Default Grid Size (X, Y, Z)",
    "default_days": "Default Simulation Duration (Days)",
    "tint": "Visualization Tint",
}

# Function to format config values for display or logging
def format_config_value(key, value):
    if key == "baseline_temperature":
        return "  |  ".join(
            [f"{particle_mapping[i]}: {temp}°C" for i, temp in enumerate(value)]
        )
    elif key == "initial_ratios":
        return "  |  ".join([f"{k.capitalize()}: {v}" for k, v in value.items()])
    elif key == "cell_type_weights":
        return "  |  ".join(
            [f"{particle_mapping[k]}: {v}" for k, v in value.items()]
        )
    elif key == "baseline_pollution_level":
        return "  |  ".join(
            [f"{particle_mapping[i]}: {level}" for i, level in enumerate(value)]
        )
    else:
        return str(value)

# Mapping of particle types to descriptive names
particle_mapping = {
    0: "Ocean",
    1: "Desert",
    2: "Cloud",
    3: "Ice",
     4: "Forest",
    5: "City",
    6: "Air",
    7: "Rain",
    8: "Vacuum",
}
