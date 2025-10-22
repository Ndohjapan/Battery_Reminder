"""
Startup Manager for Andersen Battery Reminder
Handles Windows startup registry operations with Andersen branding
"""

import os
import sys
import winreg


class StartupManager:
    def __init__(self):
        self.app_name = "Andersen_Battery_Reminder"
        self.registry_key = r"Software\Microsoft\Windows\CurrentVersion\Run"

    def get_app_path(self):
        """Get the current application path"""
        app_path = os.path.abspath(sys.argv[0])

        # If running as .py file, we need the python executable
        if app_path.endswith(".py"):
            app_path = f'"{sys.executable}" "{app_path}"'

        return app_path

    def add_to_startup(self):
        """Add the application to Windows startup"""
        try:
            app_path = self.get_app_path()

            # Registry key for startup applications
            key = winreg.HKEY_CURRENT_USER

            # Open the registry key
            with winreg.OpenKey(
                key, self.registry_key, 0, winreg.KEY_ALL_ACCESS
            ) as reg_key:
                # Set the registry value
                winreg.SetValueEx(reg_key, self.app_name, 0, winreg.REG_SZ, app_path)

            return True
        except Exception as e:
            print(f"Error adding to startup: {e}")
            return False

    def remove_from_startup(self):
        """Remove the application from Windows startup"""
        try:
            key = winreg.HKEY_CURRENT_USER

            with winreg.OpenKey(
                key, self.registry_key, 0, winreg.KEY_ALL_ACCESS
            ) as reg_key:
                winreg.DeleteValue(reg_key, self.app_name)

            return True
        except FileNotFoundError:
            # Value doesn't exist, which is fine
            return True
        except Exception as e:
            print(f"Error removing from startup: {e}")
            return False

    def is_in_startup(self):
        """Check if the application is in startup"""
        try:
            key = winreg.HKEY_CURRENT_USER

            with winreg.OpenKey(key, self.registry_key, 0, winreg.KEY_READ) as reg_key:
                winreg.QueryValueEx(reg_key, self.app_name)

            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False
