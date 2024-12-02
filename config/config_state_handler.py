# config_state_handler.py
import logging
from collections import defaultdict
from config.conf_presets import PRESET_CONFIGS, DEFAULT_PRESET, REQUIRED_KEYS
# Global configuration dictionary
CONFIG = DEFAULT_PRESET



# Configuration settings for the simulation
# This file contains all the parameters and settings used to define the behavior and appearance
# of the cellular automata simulation.
def get_config_preset(preset_name=None):
    if preset_name:
        if preset_name in PRESET_CONFIGS:            
            return PRESET_CONFIGS[preset_name].copy()
        else:
            raise ValueError('Either preset_name or custom_config must be provided.')
        
    else:
        logging.debug("preset_name is None. returning default config preset")

def get_config():
    global CONFIG
    return CONFIG.copy()

def update_config(preset_name=None, custom_config=None):
    '''
    Update the global CONFIG with a preset or custom configuration.

    Args:
        preset_name (str, optional): The name of the preset configuration to load.
        custom_config (dict, optional): A custom configuration dictionary.

    Raises:
        ValueError: If neither preset_name nor custom_config is provided.
    '''
    global CONFIG
    if preset_name:
        if preset_name in PRESET_CONFIGS:            
            CONFIG = PRESET_CONFIGS[preset_name]
            logging.info(f'Loaded preset configuration: {preset_name}')
        else:
            raise ValueError(f'Preset {preset_name} does not exist.')
    elif custom_config:
        CONFIG = custom_config
        logging.info('Loaded custom configuration.')
    else:
        raise ValueError('Either preset_name or custom_config must be provided.')
    
def validate_config(config):
    """
    Validate that all required keys and nested keys exist in the configuration.

    Args:
        config (dict): The configuration dictionary to validate.

    Raises:
        KeyError: If any required key or sub-key is missing.
    """

    def check_keys(sub_config, required_sub_keys, path=""):

        for key, expected_type in required_sub_keys.items():
            full_key = f"{path}.{key}" if path else key
            if key not in sub_config:
                raise KeyError(f"Missing required configuration key: {full_key}")
            if isinstance(expected_type, dict):
                if not isinstance(sub_config[key], dict):
                    raise TypeError(
                        f"Key {full_key} must be a dictionary, but got {type(sub_config[key])}."
                    )
                check_keys(sub_config[key], expected_type, full_key)
            else:
                if not isinstance(sub_config[key], expected_type):
                    if isinstance(expected_type, tuple) and isinstance(sub_config[key], expected_type):
                        continue  # Allow multiple types
                    raise TypeError(
                        f"Key {full_key} must be of type {expected_type}, "
                        f"but got {type(sub_config[key]).__name__}."
                    )

    check_keys(config, REQUIRED_KEYS)


