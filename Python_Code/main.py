"""
Andersen Battery Reminder - Main Application
A professional system tray application by Andersen that monitors laptop battery 
and provides intelligent charging reminders for optimal battery health.

Features:
- Intelligent battery percentage and charging status monitoring
- Audio alerts when battery reaches 100% while charging
- Silent notifications for low battery warnings
- Professional system tray integration with context menu
- Windows startup integration
- Configurable battery threshold
- Start/stop monitoring capability
- Andersen branding and professional UI

Developed by Andersen - Business Solutions for Africa
"""

import sys
import threading
import time

# Import our custom modules
from config_manager import ConfigManager
from startup_manager import StartupManager
from battery_monitor import BatteryMonitor
from gui_manager import GUIManager
from system_tray import SystemTrayManager


class BatteryReminderApp:
    def __init__(self):
        """Initialize the Andersen Battery Reminder application"""
        print("Initializing Andersen Battery Reminder...")

        # Initialize managers
        self.config_manager = ConfigManager()
        self.startup_manager = StartupManager()
        self.battery_monitor = BatteryMonitor(self.config_manager)

        # Initialize GUI and System Tray (with cross-references)
        self.gui_manager = GUIManager(
            self.config_manager, self.startup_manager, self.battery_monitor
        )

        self.system_tray = SystemTrayManager(
            self.config_manager,
            self.startup_manager,
            self.battery_monitor,
            self.gui_manager,
        )

        # Set cross-references
        self.gui_manager.system_tray = self.system_tray

        # Check if this is first run or if we should auto-start monitoring
        self.check_startup_behavior()

    def check_startup_behavior(self):
        """Check if we should start monitoring automatically"""
        config = self.config_manager.load_config()

        # If monitoring was active when app was last closed, and we're starting with Windows
        if (
            config.get("monitoring_active", False)
            and config.get("startup_enabled", False)
            and "--startup" in sys.argv
        ):

            # Auto-start monitoring in background
            print("Auto-starting monitoring from startup...")
            self.battery_monitor.start_monitoring()
            self.run_in_background()
        else:
            # Show GUI for first-time setup or manual launch
            self.show_initial_gui()

    def show_initial_gui(self):
        """Show the initial GUI for first-time setup"""
        print("Starting with GUI...")

        # Start system tray in background thread
        tray_thread = threading.Thread(target=self.system_tray.run_tray, daemon=True)
        tray_thread.start()

        # Small delay to let tray initialize
        time.sleep(0.5)

        # Show the main GUI window
        self.gui_manager.create_main_window()

    def run_in_background(self):
        """Run the app in background mode (tray only)"""
        print("Running in background mode...")

        # Just run the system tray (this will block until quit)
        self.system_tray.run_tray()

    def run(self):
        """Main application entry point"""
        try:
            # The initialization already handles the startup behavior
            pass
        except KeyboardInterrupt:
            print("Application interrupted by user")
            self.shutdown()
        except Exception as e:
            print(f"Application error: {e}")
            self.shutdown()

    def shutdown(self):
        """Clean shutdown of the application"""
        print("Shutting down Battery Reminder...")

        # Stop monitoring if running
        if self.battery_monitor.is_monitoring():
            self.battery_monitor.stop_monitoring()

        # Stop system tray
        self.system_tray.stop_tray()

        print("Battery Reminder shut down complete.")


def main():
    """Main entry point"""
    print("Battery Reminder starting...")

    # Create and run the application
    app = BatteryReminderApp()
    app.run()


if __name__ == "__main__":
    main()
