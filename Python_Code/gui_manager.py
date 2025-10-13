"""
GUI Manager for Verraki Battery Reminder
Handles the main configuration window with Verraki Partners branding
"""

import tkinter as tk
from tkinter import *
import tkinter.font as font
from tkinter import messagebox


class GUIManager:
    def __init__(
        self, config_manager, startup_manager, battery_monitor, system_tray=None
    ):
        self.config_manager = config_manager
        self.startup_manager = startup_manager
        self.battery_monitor = battery_monitor
        self.system_tray = system_tray
        self.root = None
        self.is_window_open = False

    def create_main_window(self):
        """Create and show the main configuration window"""
        if self.is_window_open and self.root and self.root.winfo_exists():
            # Window is already open, just bring it to front
            self.root.lift()
            self.root.attributes("-topmost", True)
            self.root.attributes("-topmost", False)
            return

        self.root = tk.Tk()
        self.is_window_open = True

        # Load current configuration
        config = self.config_manager.load_config()

        # Variables for the form
        self.threshold_var = tk.StringVar(value=str(config.get("charge_threshold", 20)))
        self.startup_var = tk.BooleanVar(value=config.get("startup_enabled", False))
        self.monitoring_var = tk.BooleanVar(value=self.battery_monitor.is_monitoring())

        self.setup_window()
        self.create_widgets()

        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

        # Start the GUI loop
        self.root.mainloop()

    def setup_window(self):
        """Setup window properties with Verraki branding"""
        self.root.title("Verraki Battery Reminder - Settings")
        
        # Try to use Verraki icon, fall back to original if needed
        icon_files = ["verraki_white_bg.ico", "verraki_black_bg.ico"]
        for icon_file in icon_files:
            try:
                self.root.wm_iconbitmap(icon_file)
                break
            except:
                continue

        self.root.geometry("550x450")
        self.root.resizable(False, False)
        
        # Verraki brand colors - Orange and professional styling
        self.root.configure(bg='#f8f9fa')

        # Center the window
        self.root.eval("tk::PlaceWindow . center")

    def create_widgets(self):
        """Create all GUI widgets with Verraki branding"""
        # Verraki brand colors
        verraki_orange = '#FF7A1A'  # Verraki orange
        verraki_dark = '#2c3e50'    # Dark text
        verraki_bg = '#ffffff'      # Clean white background
        verraki_light_bg = '#f8f9fa'  # Light background
        
        # Professional fonts
        title_font = font.Font(weight="bold", size=14, family="Segoe UI")
        main_font = font.Font(weight="bold", size=11, family="Segoe UI")
        label_font = font.Font(size=10, family="Segoe UI")
        
        # Verraki Header with Logo
        header_frame = Frame(self.root, bg=verraki_orange, height=60)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_title = Label(
            header_frame,
            text="VERRAKI BATTERY REMINDER",
            font=font.Font(weight="bold", size=16, family="Segoe UI"),
            bg=verraki_orange,
            fg="white"
        )
        header_title.pack(pady=15)
        
        tagline = Label(
            header_frame,
            text="Business Solutions for Africa",
            font=font.Font(size=9, family="Segoe UI"),
            bg=verraki_orange,
            fg="white"
        )
        tagline.pack(pady=(0, 5))

        # Main configuration frame
        main_frame = LabelFrame(
            self.root,
            text="Battery Management Configuration",
            bg=verraki_bg,
            fg=verraki_dark,
            font=main_font,
            relief="flat",
            bd=2
        )
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Status display with Verraki styling
        status_frame = Frame(main_frame, bg=verraki_bg, relief="ridge", bd=1)
        status_frame.pack(fill="x", padx=15, pady=10)

        status_label = Label(
            status_frame, 
            text="📊 Current Status:", 
            font=main_font, 
            bg=verraki_bg,
            fg=verraki_dark
        )
        status_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.status_text = Label(
            status_frame,
            text=self.battery_monitor.get_status_text(),
            font=label_font,
            bg=verraki_bg,
            fg=verraki_orange if self.battery_monitor.is_monitoring() else "#e74c3c",
        )
        self.status_text.pack(anchor="w", padx=25, pady=(0, 10))

        # Threshold setting with improved styling
        threshold_frame = Frame(main_frame, bg=verraki_bg)
        threshold_frame.pack(fill="x", padx=15, pady=10)

        threshold_label = Label(
            threshold_frame,
            text="⚡ Charge Reminder Threshold (%):",
            font=main_font,
            bg=verraki_bg,
            fg=verraki_dark
        )
        threshold_label.pack(anchor="w", pady=(0, 5))

        threshold_entry = Entry(
            threshold_frame,
            textvariable=self.threshold_var,
            font=font.Font(size=11, family="Segoe UI"),
            width=10,
            relief="solid",
            bg="white",
            fg=verraki_dark,
            bd=1,
            highlightbackground=verraki_orange,
            highlightcolor=verraki_orange,
            highlightthickness=1
        )
        threshold_entry.pack(anchor="w", padx=0, pady=5)

        # Startup checkbox with better styling
        startup_check = Checkbutton(
            main_frame,
            text="🚀 Start with Windows",
            variable=self.startup_var,
            bg=verraki_bg,
            fg=verraki_dark,
            font=label_font,
            activebackground=verraki_light_bg,
            selectcolor=verraki_orange,
            command=self.on_startup_toggle,
        )
        startup_check.pack(anchor="w", padx=15, pady=10)

        # Monitoring toggle with professional styling
        monitoring_frame = Frame(main_frame, bg=verraki_bg)
        monitoring_frame.pack(fill="x", padx=15, pady=20)

        if self.battery_monitor.is_monitoring():
            monitor_btn_text = "⏹ Stop Monitoring"
            monitor_btn_color = "#e74c3c"
            monitor_btn_fg = "white"
        else:
            monitor_btn_text = "▶ Start Monitoring"
            monitor_btn_color = verraki_orange
            monitor_btn_fg = "white"

        self.monitor_btn = Button(
            monitoring_frame,
            text=monitor_btn_text,
            command=self.toggle_monitoring,
            relief="flat",
            bg=monitor_btn_color,
            fg=monitor_btn_fg,
            font=font.Font(weight="bold", size=11, family="Segoe UI"),
            width=15,
            activebackground="#c0392b" if self.battery_monitor.is_monitoring() else "#e67e22",
            bd=0,
            padx=10,
            pady=8
        )
        self.monitor_btn.pack(side=LEFT, padx=(0, 10))

        # Apply settings button with Verraki styling
        apply_btn = Button(
            monitoring_frame,
            text="💾 Apply Settings",
            command=self.apply_settings,
            relief="flat",
            bg="#3498db",
            fg="white",
            font=font.Font(weight="bold", size=11, family="Segoe UI"),
            width=15,
            activebackground="#2980b9",
            bd=0,
            padx=10,
            pady=8
        )
        apply_btn.pack(side=RIGHT, padx=(10, 5))
        
        # About button with Verraki styling
        about_btn = Button(
            monitoring_frame,
            text="🏢 About",
            command=self.show_about,
            relief="flat",
            bg="#9b59b6",
            fg="white",
            font=font.Font(weight="bold", size=11, family="Segoe UI"),
            width=12,
            activebackground="#8e44ad",
            bd=0,
            padx=10,
            pady=8
        )
        about_btn.pack(side=RIGHT, padx=(0, 0))

        # Instructions with Verraki styling
        instructions_frame = LabelFrame(
            main_frame, 
            text="📋 How to Use Verraki Battery Reminder", 
            bg=verraki_bg, 
            fg=verraki_dark,
            font=main_font,
            relief="flat",
            bd=1
        )
        instructions_frame.pack(fill="both", expand=True, padx=15, pady=10)

        instructions_text = Text(
            instructions_frame,
            height=6,
            bg=verraki_light_bg,
            fg=verraki_dark,
            font=("Segoe UI", 9),
            wrap=WORD,
            state=DISABLED,
            relief="flat",
            bd=1
        )
        instructions_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Add Verraki-branded instructions
        instructions_content = """🔋 Set your preferred battery percentage for charging reminders
🚀 Enable 'Start with Windows' to automatically run the app on startup  
▶ Click 'Start Monitoring' to begin intelligent battery monitoring
🔊 The app will sound an alert when battery reaches 100% while charging
🔕 Silent notifications will remind you to charge when battery is low
⚙️ Access this window anytime from the system tray icon
🏢 Developed by Verraki Partners - Business Solutions for Africa
📱 Close this window to minimize to system tray"""

        instructions_text.config(state=NORMAL)
        instructions_text.insert(END, instructions_content)
        instructions_text.config(state=DISABLED)

    def on_startup_toggle(self):
        """Handle startup checkbox toggle"""
        if self.startup_var.get():
            if self.startup_manager.add_to_startup():
                self.config_manager.set_startup_enabled(True)
            else:
                messagebox.showerror("Error", "Failed to add to Windows startup")
                self.startup_var.set(False)
        else:
            if self.startup_manager.remove_from_startup():
                self.config_manager.set_startup_enabled(False)
            else:
                messagebox.showerror("Error", "Failed to remove from Windows startup")
                self.startup_var.set(True)

    def toggle_monitoring(self):
        """Toggle battery monitoring on/off"""
        if self.battery_monitor.is_monitoring():
            # Stop monitoring
            if self.battery_monitor.stop_monitoring():
                self.monitor_btn.config(text="Start Monitoring", bg="lightgreen")
                self.update_status_display()
                messagebox.showinfo(
                    "Monitoring Stopped", "Battery monitoring has been stopped."
                )
        else:
            # Start monitoring (apply settings first)
            if self.apply_settings():
                if self.battery_monitor.start_monitoring():
                    self.monitor_btn.config(text="Stop Monitoring", bg="lightcoral")
                    self.update_status_display()
                else:
                    messagebox.showerror("Error", "Failed to start monitoring")

    def apply_settings(self):
        """Apply the current settings"""
        try:
            # Validate threshold
            threshold = int(self.threshold_var.get())
            if threshold < 1 or threshold > 99:
                raise ValueError("Threshold must be between 1 and 99")

            # Save threshold
            if self.config_manager.set_charge_threshold(threshold):
                messagebox.showinfo(
                    "Settings Applied", f"Charge threshold set to {threshold}%"
                )
                return True
            else:
                messagebox.showerror("Error", "Failed to save settings")
                return False

        except ValueError as e:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid number between 1 and 99 for the threshold",
            )
            return False

    def update_status_display(self):
        """Update the status display"""
        if hasattr(self, "status_text"):
            self.status_text.config(
                text=self.battery_monitor.get_status_text(),
                fg="darkgreen" if self.battery_monitor.is_monitoring() else "darkred",
            )

    def on_window_close(self):
        """Handle window close event"""
        self.is_window_open = False
        self.root.withdraw()  # Hide instead of destroying

        # Show notification that app is running in background
        if hasattr(self.battery_monitor, "show_notification"):
            self.battery_monitor.show_notification(
                "Battery Reminder",
                "App is now running in the background. Access it from the system tray.",
                duration=4,
            )

    def show_window(self):
        """Show the window if it's hidden"""
        if self.root and self.root.winfo_exists():
            self.root.deiconify()
            self.root.lift()
            self.is_window_open = True
            self.update_status_display()
        else:
            self.create_main_window()

    def show_about(self):
        """Show Verraki about dialog"""
        try:
            from verraki_about import VerrakiAboutDialog
            about_dialog = VerrakiAboutDialog()
            about_dialog.show_about()
        except ImportError:
            # Fallback to basic messagebox if about dialog isn't available
            messagebox.showinfo(
                "About Verraki Battery Reminder",
                "🏢 Verraki Battery Reminder\n\n"
                "Developed by Verraki Partners\n"
                "Business Solutions for Africa\n\n"
                "🔋 Intelligent Battery Management\n"
                "⚡ Optimizing productivity across Africa\n\n"
                "Version: 2.0"
            )

    def quit_application(self):
        """Completely quit the application"""
        self.is_window_open = False
        if self.root:
            self.root.quit()
            self.root.destroy()
