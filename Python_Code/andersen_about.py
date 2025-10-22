"""
Andersen About Dialog
Professional about window for Andersen Battery Reminder
"""
import tkinter as tk
from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk


class AndersenAboutDialog:
    def __init__(self, parent=None):
        self.window = None
        
    def show_about(self):
        """Show the Andersen about dialog"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
            
        # Create about window
        self.window = tk.Toplevel() if hasattr(self, 'parent') else tk.Tk()
        self.window.title("About Andersen Battery Reminder")
        self.window.geometry("450x350")
        self.window.resizable(False, False)
        self.window.configure(bg='#ffffff')
        
        # Try to set icon
        try:
            self.window.wm_iconbitmap("andersen_white_bg.ico")
        except:
            try:
                self.window.wm_iconbitmap("verraki_white_bg.ico")
            except:
                pass
            
        # Andersen colors
        andersen_red = '#871820'
        andersen_dark = '#2c3e50'
        
        # Header with Andersen branding
        header_frame = Frame(self.window, bg=andersen_red, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Try to load logo
        try:
            logo_img = Image.open("andersen_white.png")
            logo_img = logo_img.resize((40, 40), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            
            logo_label = Label(header_frame, image=self.logo_photo, bg=andersen_red)
            logo_label.pack(pady=10, side=LEFT, padx=20)
        except:
            # Try Verraki logo as fallback
            try:
                logo_img = Image.open("verraki_white.png")
                logo_img = logo_img.resize((40, 40), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                
                logo_label = Label(header_frame, image=self.logo_photo, bg=andersen_red)
                logo_label.pack(pady=10, side=LEFT, padx=20)
            except:
                pass
        
        title_label = Label(
            header_frame,
            text="ANDERSEN BATTERY REMINDER",
            font=font.Font(weight="bold", size=16, family="Segoe UI"),
            bg=andersen_red,
            fg="white"
        )
        title_label.pack(pady=20, side=LEFT, padx=(0, 20))
        
        # Main content
        content_frame = Frame(self.window, bg='#ffffff')
        content_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Version info
        version_label = Label(
            content_frame,
            text="Version 1.0 - Professional Edition",
            font=font.Font(size=12, weight="bold", family="Segoe UI"),
            bg='#ffffff',
            fg=andersen_dark
        )
        version_label.pack(pady=(0, 10))
        
        # Company info
        company_label = Label(
            content_frame,
            text="Developed by Andersen",
            font=font.Font(size=14, weight="bold", family="Segoe UI"),
            bg='#ffffff',
            fg=andersen_red
        )
        company_label.pack(pady=5)
        
        tagline_label = Label(
            content_frame,
            text="Business Solutions for Africa",
            font=font.Font(size=11, family="Segoe UI"),
            bg='#ffffff',
            fg=andersen_dark
        )
        tagline_label.pack(pady=(0, 15))
        
        # Description
        desc_text = '''Andersen Battery Reminder is a professional battery 
management solution designed to optimize laptop battery 
health and extend battery lifespan through intelligent 
monitoring and timely notifications.

🔋 Intelligent Battery Monitoring
⚡ Customizable Charging Thresholds  
🔊 Audio Alerts for Full Battery
🔕 Silent Low Battery Reminders
🚀 Windows Startup Integration
📱 System Tray Convenience

Empowering productivity across Africa with smart 
technology solutions.'''
        
        desc_label = Label(
            content_frame,
            text=desc_text,
            font=font.Font(size=10, family="Segoe UI"),
            bg='#ffffff',
            fg=andersen_dark,
            justify=LEFT,
            wraplength=350
        )
        desc_label.pack(pady=10)
        
        # Close button
        close_btn = Button(
            content_frame,
            text="Close",
            command=self.window.destroy,
            bg=andersen_red,
            fg="white",
            font=font.Font(weight="bold", size=11, family="Segoe UI"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8
        )
        close_btn.pack(pady=20)
        
        # Center the window
        self.window.eval('tk::PlaceWindow . center')
        
        # Keep window on top initially
        self.window.attributes('-topmost', True)
        self.window.after(100, lambda: self.window.attributes('-topmost', False))


if __name__ == "__main__":
    # Test the about dialog
    about = AndersenAboutDialog()
    about.show_about()
    about.window.mainloop()