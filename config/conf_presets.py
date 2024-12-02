
# conf_presets.py
# Mapping of particle types to descriptive names
PARTICLE_MAPPING = {
    0: 'Ocean',
    1: 'Desert',
    2: 'Cloud',
    3: 'Ice',
    4: 'Forest',
    5: 'City',
    6: 'Air',
    7: 'Rain',
    8: 'Vacuum',
}

# Labels for configuration keys to provide context in the UI or logs
KEY_LABELS = {
    'days': 'Default Simulation Duration (Days)',
    'grid_size': 'Default Grid Size (X, Y, Z)',
    'initial_ratios': 'Initial Ratios (Proportions)',
    'baseline_temperature': 'Baseline Temperature (°C)',
    'baseline_pollution_level': 'Baseline Pollution Levels',
    'cell_type_weights': 'Cell Type Weights',
    'forest_pollution_absorption_rate': 'Forest Pollution Absorption Rate',
    'forest_cooling_effect': 'Forest Cooling Effect',
    'forest_pollution_extinction_point': 'Forest Pollution Extinction Point',
    'forest_temperature_extinction_point': 'Forest Temperature Extinction Point',
    'city_pollution_generation_rate': 'City Pollution Increase Rate',
    'city_warming_effect': 'City Warming Effect',
    'city_temperature_extinction_point': 'City Temperature Extinction Point (°C)',
    'city_pollution_extinction_point': 'City Pollution Extinction Point (°C)',
    'freezing_point': 'Freezing Point (°C)',
    'melting_point': 'Melting Point (°C)',
    'evaporation_point': 'Evaporation Point (°C)',
    "water_transfer_threshold": 'Water Transfer Threshold',
    'water_transfer_rate': 'Water Transfer Rate',
    'ocean_conversion_threshold': 'Ocean Conversion Threshold',
    'pollution_damage_threshold': 'Pollution Damage Threshold',
    'pollution_level_tipping_point': 'Pollution Tipping Point',
    'natural_pollution_decay_rate': 'Natural Pollution Decay Rate',
    'natural_temperature_decay_rate': 'Natural Temperature Decay Rate',
    'cloud_saturation_threshold': 'Cloud Saturation Threshold',
    'melting_rate': 'Melting Rate',
    'evaporation_rate': 'Evaporation Rate'
}

DEFAULT_PRESET = {
    "days": 365,
    "grid_size": (10, 10, 10),
    "initial_ratios": {"forest": 0.3, "city": 0.3, "desert": 0.2, "vacuum": 0.2},
    "baseline_temperature": [15.0, 30.0, 5.0, -15.0, 20.0, 125.0, 10.0, 12.0, -20.0],
    "baseline_pollution_level":
    [
        3.0,   # Ocean: Some pollution from industrial waste and microplastics
        10.0,  # Desert: Dust and localized human activity
        1.0,   # Cloud: Minimal pollution
        0.0,   # Ice: Pristine areas with negligible pollution
        2.0,   # Forest: Absorbs pollution, very low levels
        20.0,  # City: High pollution due to vehicles and factories
        50.0,   # Air: Variable pollution based on proximity to cities
        0.0,   # Rain: Cleanses the atmosphere
        0.0,   # Vacuum: No pollution in empty space
    ],
    "cell_type_weights": {
        0: 1.0,
        1: 1.2,
        2: 0.7,
        3: 0.8,
        4: 1.5,
        5: 2.0,
        6: 0.5,
        7: 1.0,
        8: 0.0,
    },
    "forest_pollution_absorption_rate": 0.1,
    "forest_cooling_effect": 0.1,
    "forest_pollution_extinction_point": 100.0,
    "forest_temperature_extinction_point": 100.0,
    "city_pollution_generation_rate": 0.1,
        "city_warming_effect": 0.1,
        "city_temperature_extinction_point": 100.0,
        "city_pollution_extinction_point": 100.0,
        "freezing_point": -15.0,
        "melting_point": 20.0,
        "evaporation_point": 35.0,
        "water_transfer_threshold": 0.05,
        "water_transfer_rate": 0.1,
        "ocean_conversion_threshold": 1.0,
        "pollution_damage_threshold": 10.0,
        "pollution_level_tipping_point": 100.0,
        "natural_pollution_decay_rate": 0.1,
        "natural_temperature_decay_rate": 0.1,
        "cloud_saturation_threshold": 2.0,
        "melting_rate": 0.15,
        "evaporation_rate": 0.05,
        "base_colors": {
            6: (1.0, 1.0, 1.0, 0.3),
            2: (0.7, 0.7, 0.7, 1.0),
            0: (0.0, 0.3, 1.0, 1.0),
            3: (0.6, 0.8, 1.0, 1.0),
            7: (0.5, 0.5, 1.0, 1.0),
            1: (1.0, 0.8, 0.5, 1.0),
            4: (0.0, 0.6, 0.0, 1.0),
            5: (0.4, 0.0, 0.4, 1.0),
            8: (1.0, 1.0, 1.0, 0.0),
    },
}


PRESET_CONFIGS = {

    "Low Air Pollution Levels": {
    "days": 365,
    "grid_size": (10, 10, 10),
    "initial_ratios": {"forest": 0.3, "city": 0.3, "desert": 0.2, "vacuum": 0.2},
    "baseline_temperature": [15.0, 30.0, 5.0, -15.0, 20.0, 125.0, 10.0, 12.0, -20.0],
    "baseline_pollution_level":
    [
        3.0,   # Ocean: Some pollution from industrial waste and microplastics
        10.0,  # Desert: Dust and localized human activity
        1.0,   # Cloud: Minimal pollution
        0.0,   # Ice: Pristine areas with negligible pollution
        2.0,   # Forest: Absorbs pollution, very low levels
        20.0,  # City: High pollution due to vehicles and factories
        0.0,   # Air: Variable pollution based on proximity to cities
        0.0,   # Rain: Cleanses the atmosphere
        0.0,   # Vacuum: No pollution in empty space
    ],
    "cell_type_weights": {
        0: 1.0,
        1: 1.2,
        2: 0.7,
        3: 0.8,
        4: 1.5,
        5: 2.0,
        6: 0.5,
        7: 1.0,
        8: 0.0,
    },
    "forest_pollution_absorption_rate": 0.1,
    "forest_cooling_effect": 0.1,
    "forest_pollution_extinction_point": 100.0,
    "forest_temperature_extinction_point": 100.0,
    "city_pollution_generation_rate": 0.1,
        "city_warming_effect": 0.1,
        "city_temperature_extinction_point": 100.0,
        "city_pollution_extinction_point": 100.0,
        "freezing_point": -15.0,
        "melting_point": 20.0,
        "evaporation_point": 35.0,
        "water_transfer_threshold": 0.05,
        "water_transfer_rate": 0.1,
        "ocean_conversion_threshold": 1.0,
        "pollution_damage_threshold": 10.0,
        "pollution_level_tipping_point": 100.0,
        "natural_pollution_decay_rate": 0.1,
        "natural_temperature_decay_rate": 0.1,
        "cloud_saturation_threshold": 2.0,
        "melting_rate": 0.15,
        "evaporation_rate": 0.05,
        "base_colors": {
            6: (1.0, 1.0, 1.0, 0.3),
            2: (0.7, 0.7, 0.7, 1.0),
            0: (0.0, 0.3, 1.0, 1.0),
            3: (0.6, 0.8, 1.0, 1.0),
            7: (0.5, 0.5, 1.0, 1.0),
            1: (1.0, 0.8, 0.5, 1.0),
            4: (0.0, 0.6, 0.0, 1.0),
            5: (0.4, 0.0, 0.4, 1.0),
            8: (1.0, 1.0, 1.0, 0.0),
    },
},
   
    "Medium Air Pollution Levels": {
    "days": 365,
    "grid_size": (10, 10, 10),
    "initial_ratios": {"forest": 0.3, "city": 0.3, "desert": 0.2, "vacuum": 0.2},
    "baseline_temperature": [15.0, 30.0, 5.0, -15.0, 20.0, 125.0, 10.0, 12.0, -20.0],
    "baseline_pollution_level":
    [
        3.0,   # Ocean: Some pollution from industrial waste and microplastics
        10.0,  # Desert: Dust and localized human activity
        1.0,   # Cloud: Minimal pollution
        0.0,   # Ice: Pristine areas with negligible pollution
        2.0,   # Forest: Absorbs pollution, very low levels
        20.0,  # City: High pollution due to vehicles and factories
        30.0,   # Air: Variable pollution based on proximity to cities
        0.0,   # Rain: Cleanses the atmosphere
        0.0,   # Vacuum: No pollution in empty space
    ],
    "cell_type_weights": {
        0: 1.0,
        1: 1.2,
        2: 0.7,
        3: 0.8,
        4: 1.5,
        5: 2.0,
        6: 0.5,
        7: 1.0,
        8: 0.0,
    },
    "forest_pollution_absorption_rate": 0.1,
    "forest_cooling_effect": 0.1,
    "forest_pollution_extinction_point": 100.0,
    "forest_temperature_extinction_point": 100.0,
    "city_pollution_generation_rate": 0.1,
        "city_warming_effect": 0.1,
        "city_temperature_extinction_point": 100.0,
        "city_pollution_extinction_point": 100.0,
        "freezing_point": -15.0,
        "melting_point": 20.0,
        "evaporation_point": 35.0,
        "water_transfer_threshold": 0.05,
        "water_transfer_rate": 0.1,
        "ocean_conversion_threshold": 1.0,
        "pollution_damage_threshold": 10.0,
        "pollution_level_tipping_point": 100.0,
        "natural_pollution_decay_rate": 0.1,
        "natural_temperature_decay_rate": 0.1,
        "cloud_saturation_threshold": 2.0,
        "melting_rate": 0.15,
        "evaporation_rate": 0.05,
        "base_colors": {
            6: (1.0, 1.0, 1.0, 0.3),
            2: (0.7, 0.7, 0.7, 1.0),
            0: (0.0, 0.3, 1.0, 1.0),
            3: (0.6, 0.8, 1.0, 1.0),
            7: (0.5, 0.5, 1.0, 1.0),
            1: (1.0, 0.8, 0.5, 1.0),
            4: (0.0, 0.6, 0.0, 1.0),
            5: (0.4, 0.0, 0.4, 1.0),
            8: (1.0, 1.0, 1.0, 0.0),
    },
},
 
    "High Air Pollution Levels": {
    "days": 365,
    "grid_size": (10, 10, 10),
    "initial_ratios": {"forest": 0.3, "city": 0.3, "desert": 0.2, "vacuum": 0.2},
    "baseline_temperature": [15.0, 30.0, 5.0, -15.0, 20.0, 125.0, 10.0, 12.0, -20.0],
    "baseline_pollution_level":
    [
        3.0,   # Ocean: Some pollution from industrial waste and microplastics
        10.0,  # Desert: Dust and localized human activity
        1.0,   # Cloud: Minimal pollution
        0.0,   # Ice: Pristine areas with negligible pollution
        2.0,   # Forest: Absorbs pollution, very low levels
        20.0,  # City: High pollution due to vehicles and factories
        60.0,   # Air: Variable pollution based on proximity to cities
        0.0,   # Rain: Cleanses the atmosphere
        0.0,   # Vacuum: No pollution in empty space
    ],
    "cell_type_weights": {
        0: 1.0,
        1: 1.2,
        2: 0.7,
        3: 0.8,
        4: 1.5,
        5: 2.0,
        6: 0.5,
        7: 1.0,
        8: 0.0,
    },
    "forest_pollution_absorption_rate": 0.1,
    "forest_cooling_effect": 0.1,
    "forest_pollution_extinction_point": 100.0,
    "forest_temperature_extinction_point": 100.0,
    "city_pollution_generation_rate": 0.1,
        "city_warming_effect": 0.1,
        "city_temperature_extinction_point": 100.0,
        "city_pollution_extinction_point": 100.0,
        "freezing_point": -15.0,
        "melting_point": 20.0,
        "evaporation_point": 35.0,
        "water_transfer_threshold": 0.05,
        "water_transfer_rate": 0.1,
        "ocean_conversion_threshold": 1.0,
        "pollution_damage_threshold": 10.0,
        "pollution_level_tipping_point": 100.0,
        "natural_pollution_decay_rate": 0.1,
        "natural_temperature_decay_rate": 0.1,
        "cloud_saturation_threshold": 2.0,
        "melting_rate": 0.15,
        "evaporation_rate": 0.05,
        "base_colors": {
            6: (1.0, 1.0, 1.0, 0.3),
            2: (0.7, 0.7, 0.7, 1.0),
            0: (0.0, 0.3, 1.0, 1.0),
            3: (0.6, 0.8, 1.0, 1.0),
            7: (0.5, 0.5, 1.0, 1.0),
            1: (1.0, 0.8, 0.5, 1.0),
            4: (0.0, 0.6, 0.0, 1.0),
            5: (0.4, 0.0, 0.4, 1.0),
            8: (1.0, 1.0, 1.0, 0.0),
    },
},

"Unstable Ecosystem (Scenario 3)": {
    "days": 365,
    "grid_size": (10, 10, 10),
    "initial_ratios": {"forest": 0.3, "city": 0.3, "desert": 0.2, "vacuum": 0.2},
    "baseline_temperature": [15.0, 30.0, 5.0, -15.0, 20.0, 125.0, 10.0, 12.0, -20.0],
    "baseline_pollution_level":
    [
        3.0,   # Ocean: Some pollution from industrial waste and microplastics
        10.0,  # Desert: Dust and localized human activity
        1.0,   # Cloud: Minimal pollution
        0.0,   # Ice: Pristine areas with negligible pollution
        2.0,   # Forest: Absorbs pollution, very low levels
        20.0,  # City: High pollution due to vehicles and factories
        50.0,   # Air: Variable pollution based on proximity to cities
        0.0,   # Rain: Cleanses the atmosphere
        0.0,   # Vacuum: No pollution in empty space
    ],
    "cell_type_weights": {
        0: 1.0,
        1: 1.2,
        2: 0.7,
        3: 0.8,
        4: 1.5,
        5: 2.0,
        6: 0.5,
        7: 1.0,
        8: 0.0,
    },
    "forest_pollution_absorption_rate": 0.1,
    "forest_cooling_effect": 0.1,
    "forest_pollution_extinction_point": 100.0,
    "forest_temperature_extinction_point": 100.0,
    "city_pollution_generation_rate": 0.1,
        "city_warming_effect": 0.1,
        "city_temperature_extinction_point": 100.0,
        "city_pollution_extinction_point": 100.0,
        "freezing_point": -15.0,
        "melting_point": 20.0,
        "evaporation_point": 35.0,
        "water_transfer_threshold": 0.05,
        "water_transfer_rate": 0.1,
        "ocean_conversion_threshold": 1.0,
        "pollution_damage_threshold": 10.0,
        "pollution_level_tipping_point": 100.0,
        "natural_pollution_decay_rate": 0.1,
        "natural_temperature_decay_rate": 0.1,
        "cloud_saturation_threshold": 2.0,
        "melting_rate": 0.15,
        "evaporation_rate": 0.05,
        "base_colors": {
            6: (1.0, 1.0, 1.0, 0.3),
            2: (0.7, 0.7, 0.7, 1.0),
            0: (0.0, 0.3, 1.0, 1.0),
            3: (0.6, 0.8, 1.0, 1.0),
            7: (0.5, 0.5, 1.0, 1.0),
            1: (1.0, 0.8, 0.5, 1.0),
            4: (0.0, 0.6, 0.0, 1.0),
            5: (0.4, 0.0, 0.4, 1.0),
            8: (1.0, 1.0, 1.0, 0.0),
    },
}

}

REQUIRED_KEYS = {
    "days": int,
    "grid_size": tuple,
    "initial_ratios": {
        "forest": float,
        "city": float,
        "desert": float,
        "vacuum": float,
    },
    "baseline_temperature": list,
    "baseline_pollution_level": list,
    "cell_type_weights": {
        0: float,  # Ocean
        1: float,  # Desert
        2: float,  # Cloud
        3: float,  # Ice
        4: float,  # Forest
        5: float,  # City
        6: float,  # Air
        7: float,  # Rain
        8: float  # Vacuum
    },
    "forest_pollution_absorption_rate": float,
    "forest_cooling_effect": float,
    "forest_pollution_extinction_point": float,
    "forest_temperature_extinction_point": float,
    "city_pollution_generation_rate": float,
    "city_warming_effect": float,
    "city_temperature_extinction_point": float,
    "city_pollution_extinction_point": float,
    "freezing_point": float,
    "melting_point": float,
    "evaporation_point": float,
    "water_transfer_threshold": float,
    "water_transfer_rate": float,
    "ocean_conversion_threshold": float,
    "pollution_damage_threshold": float,
    "pollution_level_tipping_point": float,
    "natural_pollution_decay_rate": float,
    "natural_temperature_decay_rate": float,
    "cloud_saturation_threshold": float,
    "melting_rate": float,
    "evaporation_rate": float,
    "base_colors": {
        0: tuple,  # Ocean
        1: tuple,  # Desert
        2: tuple,  # Cloud
        3: tuple,  # Ice
        4: tuple,  # Forest
        5: tuple,  # City
        6: tuple,  # Air
        7: tuple,  # Rain
        8: tuple,  # Vacuum
    },
}
