import tkinter as tk
from tkinter import filedialog
import datetime
import time
import threading
import winsound
import os

alarm_triggered = False
selected_sound = None

def update_current_time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    current_time_label.config(text=f"Current Time: {current_time}")
    root.after(1000, update_current_time)

def convert_to_24hr_format(hour, minute, second, am_pm):
    hour = int(hour)
    minute = int(minute)
    second = int(second)
    if am_pm == "PM" and hour != 12:
        hour += 12
    if am_pm == "AM" and hour == 12:
        hour = 0
    return f"{hour:02d}:{minute:02d}:{second:02d}"

def trigger_alarm():
    global alarm_triggered
    alarm_triggered = True

    # Custom non-blocking popup window
    notify_window = tk.Toplevel(root)
    notify_window.title("Alarm")
    notify_window.geometry("250x100")
    notify_window.configure(bg="#fff8dc")
    notify_window.attributes("-topmost", True)
    notify_window.resizable(False, False)

    tk.Label(notify_window, text="⏰ Time's up!", font=("Helvetica", 14, "bold"), bg="#fff8dc", fg="red").pack(expand=True)

    
    notify_window.after(5000, notify_window.destroy)

    
    try:
        if selected_sound and os.path.exists(selected_sound):
            winsound.PlaySound(selected_sound, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            winsound.Beep(1000, 1500)
    except Exception as e:
        status_label.config(text=f"Playback Error: {e}")

    stop_button.config(state="normal")
    snooze_button.config(state="normal")

def alarm_check_thread(alarm_time):
    while not alarm_triggered:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        if current_time == alarm_time:
            trigger_alarm()
            break
        time.sleep(1)

def set_alarm():
    global alarm_triggered
    alarm_triggered = False

    hour = hour_entry.get()
    minute = minute_entry.get()
    second = second_entry.get()
    am_pm = am_pm_var.get()

    if not (hour.isdigit() and minute.isdigit() and second.isdigit()):
        status_label.config(text="❌ Please enter valid numbers.")
        return

    if int(hour) < 1 or int(hour) > 12 or int(minute) > 59 or int(second) > 59:
        status_label.config(text="❌ Please enter a valid time.")
        return

    alarm_time = convert_to_24hr_format(hour, minute, second, am_pm)
    status_label.config(text=f"✅ Alarm set for {alarm_time} (24-hour format)")

    stop_button.config(state="disabled")
    snooze_button.config(state="disabled")

    threading.Thread(target=alarm_check_thread, args=(alarm_time,), daemon=True).start()

def stop_alarm():
    global alarm_triggered
    alarm_triggered = True
    winsound.PlaySound(None, winsound.SND_PURGE)
    status_label.config(text="Alarm stopped.")
    stop_button.config(state="disabled")
    snooze_button.config(state="disabled")

def snooze_alarm():
    global alarm_triggered
    alarm_triggered = True
    winsound.PlaySound(None, winsound.SND_PURGE)
    status_label.config(text="Alarm snoozed for 5 minutes.")
    new_time = (datetime.datetime.now() + datetime.timedelta(minutes=5)).strftime("%H:%M:%S")
    threading.Thread(target=alarm_check_thread, args=(new_time,), daemon=True).start()
    stop_button.config(state="disabled")
    snooze_button.config(state="disabled")

def browse_sound():
    global selected_sound
    file_path = filedialog.askopenfilename(
        title="Select Alarm Sound (.wav)",
        filetypes=[("WAV files", "*.wav")]
    )
    if file_path:
        selected_sound = file_path
        sound_label.config(text=os.path.basename(file_path))
    else:
        selected_sound = None
        sound_label.config(text="No sound selected")


root = tk.Tk()
root.title("Styled Alarm Clock")
root.geometry("500x420")
root.config(bg="#f0f8ff")

font_title = ("Helvetica", 18, "bold")
font_label = ("Helvetica", 11)
font_button = ("Helvetica", 12, "bold")

tk.Label(root, text="Alarm Clock", font=font_title, bg="#f0f8ff", fg="#333").pack(pady=10)


time_frame = tk.Frame(root, bg="#f0f8ff")
time_frame.pack(pady=10)

tk.Label(time_frame, text="Hour", font=font_label, bg="#f0f8ff").grid(row=0, column=0)
hour_entry = tk.Entry(time_frame, width=5, font=font_label, justify='center')
hour_entry.grid(row=1, column=0, padx=5)

tk.Label(time_frame, text="Minute", font=font_label, bg="#f0f8ff").grid(row=0, column=1)
minute_entry = tk.Entry(time_frame, width=5, font=font_label, justify='center')
minute_entry.grid(row=1, column=1, padx=5)

tk.Label(time_frame, text="Second", font=font_label, bg="#f0f8ff").grid(row=0, column=2)
second_entry = tk.Entry(time_frame, width=5, font=font_label, justify='center')
second_entry.grid(row=1, column=2, padx=5)

am_pm_var = tk.StringVar(value="AM")
am_pm_menu = tk.OptionMenu(time_frame, am_pm_var, "AM", "PM")
am_pm_menu.config(font=font_label)
am_pm_menu.grid(row=1, column=3, padx=10)


tk.Button(root, text="Choose Alarm Sound ", font=font_button, bg="#e0ffff", command=browse_sound).pack(pady=8)
sound_label = tk.Label(root, text="No sound selected", fg="blue", bg="#f0f8ff", font=("Helvetica", 10, "italic"))
sound_label.pack()

tk.Button(root, text="Set Alarm", command=set_alarm, font=font_button, bg="#d1e7dd", width=20).pack(pady=12)
stop_button = tk.Button(root, text="Stop", command=stop_alarm, state="disabled", bg="#dc3545", fg="white", font=font_button, width=10)
stop_button.pack(pady=3)

snooze_button = tk.Button(root, text="Snooze 5 min", command=snooze_alarm, state="disabled", bg="#fd7e14", fg="white", font=font_button, width=10)
snooze_button.pack(pady=3)

status_label = tk.Label(root, text="", fg="green", bg="#f0f8ff", font=("Helvetica", 11))
status_label.pack(pady=5)

current_time_label = tk.Label(root, text="", font=("Courier New", 12, "bold"), bg="#f0f8ff")
current_time_label.pack()

update_current_time()
root.mainloop()


