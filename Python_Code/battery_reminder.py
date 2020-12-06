import psutil
import winsound
import tkinter
from tkinter import *
import tkinter.font as font
from tkinter import messagebox
from win10toast import ToastNotifier


def battery_function(charge_percent):

    toast = ToastNotifier()
    toast.show_toast("Battery Saver", "Battery Saver is doing work in background", duration=5, icon_path="gst-sdk"
                                                                                                         "-template.ico")

    while True:
        percent = psutil.sensors_battery().percent
        if percent == 100 and psutil.sensors_battery().power_plugged:
            for _ in range(2):
                winsound.PlaySound("car_crash.wav", winsound.SND_NOSTOP)
            toast.show_toast("Battery Fully Charged", f"{percent}% \n UnPlug Your Charger", duration=10,
                             icon_path="gst-sdk-template.ico")

        elif percent == int(charge_percent) and not psutil.sensors_battery().power_plugged:
            for _ in range(2):
                winsound.PlaySound("car_crash.wav", winsound.SND_NOSTOP)
            toast.show_toast("Connect Your Charger", f"Battery Percent: {percent}%", duration=10,
                             icon_path="gst-sdk-template.ico")


def start_app():
    root = tkinter.Tk()

    def close_window(battery_percent):
        try:
            if int(battery_percent) > 100 or int(battery_percent) < 1:
                raise ValueError
            else:
                root.destroy()
                battery_function(int(battery_percent))

        except ValueError:
            messagebox.showerror("Invalid Input", """INVALID INPUT\nNUMBER MUST BE LESS THAN 100 AND GREATER THAN 0""")

    root.title("Battery")
    root.wm_iconbitmap("gst-sdk-template.ico")
    root.geometry("468x150")
    myFont = font.Font(weight="bold", size=14, family="Courier")
    root.resizable(False, False)

    mighty = LabelFrame(root, text="Mighty Python", bg="grey")
    mighty.grid(row=0, column=0, sticky=W, ipady=10)

    lbl = tkinter.Label(mighty, text="When Do You Want To Plug Your Charger?", bg="grey")
    lbl['font'] = myFont
    lbl.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

    lbl1 = tkinter.Label(mighty, text="Percent:", bg="grey")
    lbl1['font'] = myFont
    lbl1.grid(row=1, column=0)

    entry = tkinter.Entry(mighty, relief=SUNKEN, bg="light blue")
    entry['font'] = myFont
    entry.focus()
    entry.grid(row=1, column=1, sticky=W, ipadx=30)

    btn = tkinter.Button(mighty, text="Ok", command=lambda: close_window(entry.get()), relief=GROOVE, bg="light green")
    btn.grid(row=2, column=1, pady=10, sticky=W, ipadx=10)
    root.mainloop()


window = tkinter.Tk()
window.title("Battery")
window.wm_iconbitmap("gst-sdk-template.ico")
window.geometry("450x420")
myFont = font.Font(weight="bold", size=14, family="Courier")
window.resizable(False, False)

def open_application():
    window.destroy()
    start_app()

label = LabelFrame(window, text="How To Use Battery", bg="grey")
label.grid(row=0, column=0, sticky=W, ipady=10)


lbl3 = Label(label, text="""\nOvercharging your PC affects the durability of your PC battery. Sometimes we plug \nour PC to charge and forget about it.
\n\nBattery Reminder is a simple application that reminds you to
unplug your charger and to plug it in when the battery percent is at a certain level\n""", bg="grey")
lbl3.grid(row=0, column=0, sticky=W)

lbl2 = Label(label, text="""STEPS""", bg="grey")
lbl2['font'] = font.Font(weight="bold", size=16, family="Courier")
lbl2.grid(row=1, column=0, sticky=W, ipadx=179, ipady=10)

lb4 = Label(label, text="""1. Click the 'OK' button

2. Input the percentage when you want to plug in your charger

3. Click the 'OK' button to start

4. The application will ring out loud when the battery percent is at 100% 
while charging

5. The application will also ring out loud when the battery goes down 
to the percentage for it to be plugged in.""")
lb4.grid(row=2, column=0)

btn1 = tkinter.Button(label, text="Ok", command=lambda: open_application(), relief=GROOVE, bg="light green")
btn1.grid(row=3, column=0, pady=20, ipadx=180, sticky=W, padx=30)


window.mainloop()
