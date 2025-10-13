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
        
        # Sound loop control
        self.sound_loop_active = False
        self.sound_thread = None
        self.sound_stop_event = threading.Event()

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

    def play_alert_sound_loop(self):
        """Play alert sound in a continuous loop until stopped"""
        sound_file = os.path.join(os.path.dirname(__file__), "car_crash.wav")
        
        while self.sound_loop_active and not self.sound_stop_event.is_set():
            try:
                if os.path.exists(sound_file):
                    winsound.PlaySound(sound_file, winsound.SND_FILENAME)
                else:
                    # Use system sound if custom sound doesn't exist
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                
                # Wait 2 seconds before playing again (adjust as needed)
                if not self.sound_stop_event.wait(2):
                    continue
                else:
                    break
                    
            except Exception as e:
                print(f"Error playing sound: {e}")
                # Wait before trying again if there's an error
                if not self.sound_stop_event.wait(5):
                    continue
                else:
                    break
    
    def start_sound_loop(self):
        """Start the continuous sound loop in a separate thread"""
        if not self.sound_loop_active:
            self.sound_loop_active = True
            self.sound_stop_event.clear()
            self.sound_thread = threading.Thread(target=self.play_alert_sound_loop, daemon=True)
            self.sound_thread.start()
            print("🔊 Started continuous battery alert sound loop")
    
    def stop_sound_loop(self):
        """Stop the continuous sound loop"""
        if self.sound_loop_active:
            self.sound_loop_active = False
            self.sound_stop_event.set()
            print("🔕 Stopped battery alert sound loop")

    def monitor_battery(self):
        """Main battery monitoring loop with continuous sound for full battery"""
        threshold = self.config_manager.get_charge_threshold()
        was_full_and_charging = False

        while not self.stop_event.is_set() and self.monitoring:
            try:
                percent, plugged, battery_info = self.get_battery_info()

                if percent is None:
                    time.sleep(10)  # Check more frequently
                    continue

                current_time = time.time()
                is_full_and_charging = percent >= 100 and plugged

                # Handle full battery while charging - CONTINUOUS SOUND LOOP
                if is_full_and_charging:
                    # Show notification only once when first detected
                    if not was_full_and_charging and (
                        current_time - self.last_full_notification > self.notification_cooldown
                    ):
                        self.show_notification(
                            "🔋 Verraki Battery Alert - UNPLUG NOW!",
                            f"⚡ Battery: {percent}% - FULLY CHARGED!\n🔌 PLEASE UNPLUG YOUR CHARGER NOW!\n🚨 Continuous alert until unplugged\n🏢 Verraki Partners - Protecting your battery",
                            duration=15,
                        )
                        self.last_full_notification = current_time
                    
                    # Start continuous sound loop if not already running
                    if not self.sound_loop_active:
                        self.start_sound_loop()
                
                else:
                    # Stop sound loop when no longer full+charging
                    if self.sound_loop_active:
                        self.stop_sound_loop()
                    
                    # Handle low battery while not charging
                    if percent <= threshold and not plugged:
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

                # Update state for next iteration
                was_full_and_charging = is_full_and_charging

                # Check more frequently when full+charging for immediate response to unplugging
                sleep_time = 5 if is_full_and_charging else 30
                time.sleep(sleep_time)

            except Exception as e:
                print(f"Error in battery monitoring: {e}")
                time.sleep(10)

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
        """Stop battery monitoring and sound loop"""
        if not self.monitoring:
            return False

        self.monitoring = False
        self.stop_event.set()
        self.config_manager.set_monitoring_active(False)
        
        # Stop any active sound loop
        self.stop_sound_loop()

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
        sound_status = " | 🔊 ALERT ACTIVE" if self.sound_loop_active else ""
        return f"Monitoring: ON | Battery: {percent}% ({status}){sound_status}"
