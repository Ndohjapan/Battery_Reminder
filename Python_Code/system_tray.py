"""
System Tray Manager for Andersen Battery Reminder
Handles the system tray icon and context menu with Andersen branding
"""

import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading


class SystemTrayManager:
    def __init__(
        self, config_manager, startup_manager, battery_monitor, gui_manager=None
    ):
        self.config_manager = config_manager
        self.startup_manager = startup_manager
        self.battery_monitor = battery_monitor
        self.gui_manager = gui_manager
        self.icon = None
        self.running = False

    def create_icon_image(self):
        """Create an Andersen-branded icon image for the system tray"""
        # Try to load Andersen logo first, fall back to generated icon
        try:
            # Try different Andersen icon files
            icon_files = ["andersen_white_bg.png", "andersen_black_bg.png", "andersen_white.png", "verraki_white_bg.png", "verraki_black_bg.png", "verraki_white.png"]
            for icon_file in icon_files:
                try:
                    image = Image.open(icon_file)
                    # Resize to system tray size
                    image = image.resize((32, 32), Image.Resampling.LANCZOS)
                    return image
                except:
                    continue
        except:
            pass
        
        # Fallback: Create Andersen-branded battery icon
        image = Image.new("RGB", (32, 32), color="white")
        draw = ImageDraw.Draw(image)
        
        # Andersen red color
        andersen_red = (135, 24, 32)  # #871820
        
        # Draw battery outline with Andersen branding
        draw.rectangle([8, 10, 22, 25], outline=andersen_red, width=2)
        draw.rectangle([45, 28, 50, 42], fill="black")  # Battery tip

        draw.rectangle([22, 12, 26, 18], fill=andersen_red)  # Battery tip
        
        # Draw battery level based on monitoring status
        if self.battery_monitor.is_monitoring():
            # Andersen red for active monitoring
            draw.rectangle([10, 12, 20, 23], fill=andersen_red)
        else:
            # Red for inactive
            draw.rectangle([10, 20, 20, 23], fill=(231, 76, 60))

        return image

    def create_context_menu(self):
        """Create the Andersen-branded context menu for the system tray icon"""
        return (
            item("🏢 Open Andersen Battery Reminder", self.show_gui, default=True),
            item("📊 Battery Status", self.show_battery_status),
            pystray.Menu.SEPARATOR,
            item(
                "▶ Start Monitoring" if not self.battery_monitor.is_monitoring() else "⏹ Stop Monitoring",
                self.toggle_monitoring,
            ),
            pystray.Menu.SEPARATOR,
            item("⚙️ Settings", self.show_gui),
            item("ℹ️ About Andersen", self.show_about),
            item("❌ Exit", self.quit_app),
        )

    def show_gui(self, icon=None, item=None):
        """Show the main GUI window"""
        if self.gui_manager:
            threading.Thread(target=self.gui_manager.show_window, daemon=True).start()

    def show_battery_status(self):
        """Show current battery status with Andersen branding"""
        percent, plugged, _ = self.battery_monitor.get_battery_info()
        if percent is not None:
            status = "Charging" if plugged else "On Battery"
            self.battery_monitor.show_notification(
                "Andersen Battery Status",
                f"🔋 Battery: {percent}% ({status})\n📊 Monitoring: {'ON' if self.battery_monitor.is_monitoring() else 'OFF'}\n🏢 Andersen",
                duration=5,
            )
        else:
            self.battery_monitor.show_notification(
                "Verraki Battery Status", 
                "⚠️ Unable to read battery information\n🏢 Verraki Partners", 
                duration=3
            )
    
    def show_about(self, icon=None, item=None):
        """Show Verraki about dialog"""
        try:
            from verraki_about import VerrakiAboutDialog
            about_dialog = VerrakiAboutDialog()
            threading.Thread(target=about_dialog.show_about, daemon=True).start()
        except ImportError:
            # Fallback to notification if about dialog isn't available
            self.battery_monitor.show_notification(
                "About Verraki Battery Reminder",
                "🏢 Developed by Verraki Partners\n🌍 Business Solutions for Africa\n🔋 Intelligent Battery Management\n⚡ Optimizing productivity across Africa",
                duration=8
            )

    def toggle_monitoring(self, icon=None, item=None):
        """Toggle battery monitoring from tray"""
        if self.battery_monitor.is_monitoring():
            self.battery_monitor.stop_monitoring()
        else:
            self.battery_monitor.start_monitoring()

        # Update the icon and menu
        self.update_icon()

    def update_icon(self):
        """Update the tray icon"""
        if self.icon:
            self.icon.icon = self.create_icon_image()
            self.icon.menu = self.create_context_menu()

    def quit_app(self, icon=None, item=None):
        """Quit the entire application"""
        self.running = False

        # Stop monitoring if active
        if self.battery_monitor.is_monitoring():
            self.battery_monitor.stop_monitoring()

        # Show goodbye notification
        self.battery_monitor.show_notification(
            "Verraki Battery Reminder", 
            "🏢 Thank you for using Verraki Partners solutions!\n💼 Application is shutting down", 
            duration=3
        )

        # Stop the tray icon
        if self.icon:
            self.icon.stop()

        # Close GUI if open
        if self.gui_manager:
            self.gui_manager.quit_application()

    def run_tray(self):
        """Start the Verraki system tray icon"""
        if self.running:
            return

        self.running = True

        # Create the tray icon with Verraki branding
        self.icon = pystray.Icon(
            "verraki_battery_reminder",
            self.create_icon_image(),
            "Verraki Battery Reminder",
            self.create_context_menu(),
        )

        # Show initial Verraki notification
        self.battery_monitor.show_notification(
            "Verraki Battery Reminder", 
            "🏢 Verraki Partners - Battery Reminder\n📱 App is now running in the system tray\n🌍 Business Solutions for Africa", 
            duration=5
        )

        # Run the tray (this blocks)
        try:
            self.icon.run()
        except Exception as e:
            print(f"Error running system tray: {e}")
        finally:
            self.running = False

    def stop_tray(self):
        """Stop the system tray icon"""
        self.running = False
        if self.icon:
            self.icon.stop()

    def set_gui_manager(self, gui_manager):
        """Set the GUI manager reference"""
        self.gui_manager = gui_manager
