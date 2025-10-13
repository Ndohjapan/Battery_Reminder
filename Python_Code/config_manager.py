"""
Configuration Manager for Battery Reminder
Handles saving and loading user settings
"""

import json
import os


class ConfigManager:
    def __init__(self):
        self.config_file = os.path.join(
            os.path.dirname(__file__), "battery_config.json"
        )
        self.default_config = {
            "charge_threshold": 20,
            "startup_enabled": False,
            "monitoring_active": False,
        }

    def load_config(self):
        """Load configuration from file or return defaults"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    config = json.load(f)
                # Merge with defaults to handle missing keys
                return {**self.default_config, **config}
            return self.default_config.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()

    def save_config(self, config):
        """Save configuration to file"""
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get_charge_threshold(self):
        """Get the current charge threshold"""
        config = self.load_config()
        return config.get("charge_threshold", 20)

    def set_charge_threshold(self, threshold):
        """Set the charge threshold"""
        config = self.load_config()
        config["charge_threshold"] = threshold
        return self.save_config(config)

    def is_startup_enabled(self):
        """Check if startup is enabled"""
        config = self.load_config()
        return config.get("startup_enabled", False)

    def set_startup_enabled(self, enabled):
        """Set startup enabled status"""
        config = self.load_config()
        config["startup_enabled"] = enabled
        return self.save_config(config)

    def is_monitoring_active(self):
        """Check if monitoring is active"""
        config = self.load_config()
        return config.get("monitoring_active", False)

    def set_monitoring_active(self, active):
        """Set monitoring active status"""
        config = self.load_config()
        config["monitoring_active"] = active
        return self.save_config(config)
