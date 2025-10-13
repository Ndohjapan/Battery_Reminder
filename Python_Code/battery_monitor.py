"""
Battery Monitor for Verraki Battery Reminder
Handles intelligent battery monitoring and notifications with Verraki branding
"""

import os
import psutil
import winsound
import threading
import time
from win10toast import ToastNotifier


class BatteryMonitor:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.toast = ToastNotifier()
        self.monitoring = False
        self.monitor_thread = None
        self.stop_event = threading.Event()

        # Notification state tracking to prevent spam
        self.last_full_notification = 0
        self.last_low_notification = 0
        self.notification_cooldown = 300  # 5 minutes in seconds

    def get_battery_info(self):
        """Get current battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return None, None, None

            percent = battery.percent
            plugged = battery.power_plugged
            return percent, plugged, battery
        except Exception as e:
            print(f"Error getting battery info: {e}")
            return None, None, None

    def show_notification(self, title, message, duration=10):
        """Show a toast notification"""
        try:
            self.toast.show_toast(
                title,
                message,
                duration=duration,
                icon_path="verraki_white_bg.ico" if self._icon_exists() else None,
                threaded=True,
            )
        except Exception as e:
            print(f"Error showing notification: {e}")

    def _icon_exists(self):
        """Check if the icon file exists"""
        import os

        return os.path.exists(
            os.path.join(os.path.dirname(__file__), "verraki_white_bg.ico")
        )

    def play_alert_sound(self):
        """Play alert sound for full battery"""
        try:
            sound_file = "car_crash.wav"
            if not os.path.exists(os.path.join(os.path.dirname(__file__), sound_file)):
                # Use system sound if custom sound doesn't exist
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            else:
                for _ in range(2):
                    winsound.PlaySound(sound_file, winsound.SND_NOSTOP)
        except Exception as e:
            print(f"Error playing sound: {e}")

    def monitor_battery(self):
        """Main battery monitoring loop"""
        threshold = self.config_manager.get_charge_threshold()

        while not self.stop_event.is_set() and self.monitoring:
            try:
                percent, plugged, battery_info = self.get_battery_info()

                if percent is None:
                    time.sleep(30)
                    continue

                current_time = time.time()

                # Check for full battery while charging
                if percent >= 100 and plugged:
                    if (
                        current_time - self.last_full_notification
                        > self.notification_cooldown
                    ):
                        self.play_alert_sound()
                        self.show_notification(
                            "🔋 Verraki Battery Alert",
                            f"⚡ Battery Fully Charged ({percent}%)\n🔌 Please unplug your charger\n🏢 Verraki Partners - Protecting your battery",
                            duration=10,
                        )
                        self.last_full_notification = current_time

                # Check for low battery while not charging
                elif percent <= threshold and not plugged:
                    if (
                        current_time - self.last_low_notification
                        > self.notification_cooldown
                    ):
                        self.show_notification(
                            "🔋 Verraki Charging Reminder",
                            f"⚠️ Battery: {percent}% - Time to charge!\n🔌 Please plug in your charger\n🏢 Verraki Partners keeps you productive",
                            duration=10,
                        )
                        self.last_low_notification = current_time

                # Wait before next check
                time.sleep(30)

            except Exception as e:
                print(f"Error in battery monitoring: {e}")
                time.sleep(30)

    def start_monitoring(self):
        """Start battery monitoring"""
        if self.monitoring:
            return False

        self.monitoring = True
        self.stop_event.clear()
        self.config_manager.set_monitoring_active(True)

        # Start monitoring in a separate thread
        self.monitor_thread = threading.Thread(target=self.monitor_battery, daemon=True)
        self.monitor_thread.start()

        # Show initial Verraki notification
        self.show_notification(
            "🔋 Verraki Battery Reminder",
            "✅ Intelligent monitoring activated!\n📱 Running in background\n🏢 Verraki Partners - Your productivity partner",
            duration=5,
        )

        return True

    def stop_monitoring(self):
        """Stop battery monitoring"""
        if not self.monitoring:
            return False

        self.monitoring = False
        self.stop_event.set()
        self.config_manager.set_monitoring_active(False)

        # Show stop notification
        self.show_notification(
            "🔋 Verraki Battery Reminder", 
            "⏹️ Monitoring stopped\n🏢 Verraki Partners - Always here when you need us", 
            duration=3
        )

        return True

    def is_monitoring(self):
        """Check if currently monitoring"""
        return self.monitoring

    def get_status_text(self):
        """Get current status text for display"""
        if not self.monitoring:
            return "Monitoring: OFF"

        percent, plugged, _ = self.get_battery_info()
        if percent is None:
            return "Monitoring: ON (Battery info unavailable)"

        status = "Charging" if plugged else "On Battery"
        return f"Monitoring: ON | Battery: {percent}% ({status})"
