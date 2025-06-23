import tkinter as tk
from tkinter import messagebox, simpledialog
import calendar
from datetime import datetime
import json
import os

REMINDER_FILE = "reminders.json"

# Load reminders from file or create empty dict
def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    return {}

# Save reminders dict to file
def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

class CalendarReminderApp:
    def __init__(self, master):
        self.master = master
        master.title("Calendar and Reminder App")
        master.geometry("420x500")
        master.resizable(False, False)

        self.reminders = load_reminders()

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.header_frame = tk.Frame(master)
        self.header_frame.pack(pady=10)

        self.prev_btn = tk.Button(self.header_frame, text="<", width=3, command=self.prev_month)
        self.prev_btn.grid(row=0, column=0)

        self.month_year_label = tk.Label(self.header_frame, text="", font=("Segoe UI", 16, "bold"))
        self.month_year_label.grid(row=0, column=1, padx=20)

        self.next_btn = tk.Button(self.header_frame, text=">", width=3, command=self.next_month)
        self.next_btn.grid(row=0, column=2)

        self.calendar_frame = tk.Frame(master)
        self.calendar_frame.pack()

        self.days_frame = tk.Frame(master)
        self.days_frame.pack(pady=10)

        self.create_calendar()

    def create_calendar(self):
        # Clear previous buttons if any
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        for widget in self.days_frame.winfo_children():
            widget.destroy()

        # Display month-year
        month_name = calendar.month_name[self.current_month]
        self.month_year_label.config(text=f"{month_name} {self.current_year}")

        # Display day names
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.days_frame, text=day, font=("Segoe UI", 10, "bold"), width=5).grid(row=0, column=i)

        # Get calendar matrix for the month/year
        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(self.current_year, self.current_month)

        for r, week in enumerate(month_days):
            for c, day in enumerate(week):
                if day == 0:
                    # Days outside the month
                    tk.Label(self.calendar_frame, text="", width=5, height=2).grid(row=r, column=c)
                else:
                    # Button for the day
                    btn = tk.Button(self.calendar_frame, text=str(day), width=5, height=2,
                                    command=lambda d=day: self.open_reminder_window(d))
                    # Highlight today
                    today = datetime.now()
                    if (day == today.day and self.current_month == today.month and
                        self.current_year == today.year):
                        btn.config(bg="#4caf50", fg="white")
                    # Highlight if reminder exists
                    key = self.reminder_key(self.current_year, self.current_month, day)
                    if key in self.reminders and self.reminders[key]:
                        btn.config(fg="red")
                    btn.grid(row=r, column=c, padx=2, pady=2)

    def reminder_key(self, year, month, day):
        return f"{year}-{month:02d}-{day:02d}"

    def open_reminder_window(self, day):
        key = self.reminder_key(self.current_year, self.current_month, day)
        reminder_texts = self.reminders.get(key, [])

        window = tk.Toplevel(self.master)
        window.title(f"Reminders for {key}")
        window.geometry("300x350")
        window.resizable(False, False)

        label = tk.Label(window, text=f"Reminders for {key}", font=("Segoe UI", 14, "bold"))
        label.pack(pady=10)

        reminders_frame = tk.Frame(window)
        reminders_frame.pack(pady=5)

        # List current reminders
        listbox = tk.Listbox(reminders_frame, width=40, height=10)
        listbox.pack(side="left", fill="y")

        scrollbar = tk.Scrollbar(reminders_frame)
        scrollbar.pack(side="right", fill="y")

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        for r in reminder_texts:
            listbox.insert(tk.END, r)

        # Entry to add new reminder
        entry = tk.Entry(window, width=35)
        entry.pack(pady=10)

        def add_reminder():
            new_text = entry.get().strip()
            if new_text == "":
                messagebox.showwarning("Input Error", "Reminder text cannot be empty.")
                return
            reminder_texts.append(new_text)
            self.reminders[key] = reminder_texts
            save_reminders(self.reminders)
            listbox.insert(tk.END, new_text)
            entry.delete(0, tk.END)
            self.create_calendar()

        def delete_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("Selection Error", "Select a reminder to delete.")
                return
            index = selected[0]
            reminder_texts.pop(index)
            self.reminders[key] = reminder_texts
            save_reminders(self.reminders)
            listbox.delete(index)
            self.create_calendar()

        add_btn = tk.Button(window, text="Add Reminder", command=add_reminder)
        add_btn.pack(pady=5)

        del_btn = tk.Button(window, text="Delete Selected", command=delete_selected)
        del_btn.pack(pady=5)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.create_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.create_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarReminderApp(root)
    root.mainloop()
