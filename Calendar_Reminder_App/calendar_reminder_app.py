import tkinter as tk
from tkinter import messagebox
import calendar
from datetime import datetime
import json, os

REMINDER_FILE = "reminders.json"

def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_reminders(reminders):
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

PRIMARY_BG     = "#1976d2"   
PRIMARY_FG     = "white"
PRIMARY_ACTIVE = "#1565c0"

ACCENT_BG      = "#e3f2fd"   
ACCENT_ACTIVE  = "#bbdefb"

ADD_BG         = "#2e7d32"   
ADD_ACTIVE     = "#1b5e20"

DEL_BG         = "#c62828"   
DEL_ACTIVE     = "#8e0000"

TODAY_BG       = "#4caf50"   
TODAY_FG       = "white"

class CalendarReminderApp:
    def __init__(self, master):
        self.master = master
        master.title("Calendar and Reminder App")
        master.geometry("420x500")
        master.resizable(False, False)

        self.reminders     = load_reminders()
        self.current_year  = datetime.now().year
        self.current_month = datetime.now().month

        # ----- Header (month navigation) -----
        self.header_frame = tk.Frame(master)
        self.header_frame.pack(pady=10)

        self.prev_btn = tk.Button(
            self.header_frame, text="⟨", width=3,
            bg=PRIMARY_BG, fg=PRIMARY_FG, activebackground=PRIMARY_ACTIVE,
            command=self.prev_month
        )
        self.prev_btn.grid(row=0, column=0)

        self.month_year_label = tk.Label(
            self.header_frame, text="", font=("Segoe UI", 16, "bold")
        )
        self.month_year_label.grid(row=0, column=1, padx=20)

        self.next_btn = tk.Button(
            self.header_frame, text="⟩", width=3,
            bg=PRIMARY_BG, fg=PRIMARY_FG, activebackground=PRIMARY_ACTIVE,
            command=self.next_month
        )
        self.next_btn.grid(row=0, column=2)

        # ----- Calendars -----
        self.calendar_frame = tk.Frame(master)
        self.calendar_frame.pack()
        self.days_frame     = tk.Frame(master)
        self.days_frame.pack(pady=10)

        self.create_calendar()

    # ---------- Calendar rendering ----------
    def create_calendar(self):
        # Clear old widgets
        for f in (self.calendar_frame, self.days_frame):
            for w in f.winfo_children():
                w.destroy()

        # Month‑year header
        month_name = calendar.month_name[self.current_month]
        self.month_year_label.config(text=f"{month_name} {self.current_year}")

        # Weekday headings
        for i, day in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
            tk.Label(
                self.days_frame, text=day, width=5,
                bg=PRIMARY_BG, fg=PRIMARY_FG, font=("Segoe UI", 10, "bold")
            ).grid(row=0, column=i, padx=1, pady=1)

        # Calendar days
        cal = calendar.Calendar(firstweekday=0)
        today = datetime.now()
        for r, week in enumerate(cal.monthdayscalendar(self.current_year, self.current_month)):
            for c, day in enumerate(week):
                if day == 0:
                    tk.Label(self.calendar_frame, text="", width=5, height=2).grid(row=r, column=c)
                    continue

                key = self.reminder_key(self.current_year, self.current_month, day)
                btn_fg = "red" if self.reminders.get(key) else "black"

                btn = tk.Button(
                    self.calendar_frame, text=day, width=5, height=2,
                    bg=ACCENT_BG, fg=btn_fg, activebackground=ACCENT_ACTIVE,
                    command=lambda d=day: self.open_reminder_window(d)
                )

                # Highlight today
                if day == today.day and self.current_month == today.month and self.current_year == today.year:
                    btn.config(bg=TODAY_BG, fg=TODAY_FG)

                btn.grid(row=r, column=c, padx=2, pady=2)


    def reminder_key(self, y, m, d): return f"{y}-{m:02d}-{d:02d}"

    def open_reminder_window(self, day):
        key = self.reminder_key(self.current_year, self.current_month, day)
        reminder_texts = self.reminders.get(key, [])

        win = tk.Toplevel(self.master)
        win.title(f"Reminders for {key}")
        win.geometry("300x350")
        win.resizable(False, False)

        tk.Label(win, text=f"Reminders for {key}",
                 font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Listbox + scrollbar
        frame = tk.Frame(win); frame.pack(pady=5)
        listbox = tk.Listbox(frame, width=40, height=10)
        listbox.pack(side="left", fill="y")
        sb = tk.Scrollbar(frame, command=listbox.yview); sb.pack(side="right", fill="y")
        listbox.config(yscrollcommand=sb.set)
        for r in reminder_texts: listbox.insert(tk.END, r)

        entry = tk.Entry(win, width=35); entry.pack(pady=10)

        def add_reminder():
            txt = entry.get().strip()
            if not txt:
                messagebox.showwarning("Input Error", "Reminder text cannot be empty.")
                return
            reminder_texts.append(txt)
            self.reminders[key] = reminder_texts
            save_reminders(self.reminders)
            listbox.insert(tk.END, txt)
            entry.delete(0, tk.END)
            self.create_calendar()

        def delete_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("Selection Error", "Select a reminder to delete.")
                return
            reminder_texts.pop(sel[0])
            self.reminders[key] = reminder_texts
            save_reminders(self.reminders)
            listbox.delete(sel[0])
            self.create_calendar()

        tk.Button(win, text="Add Reminder", width=14,
                  bg=ADD_BG, fg="white", activebackground=ADD_ACTIVE,
                  command=add_reminder).pack(pady=4)

        tk.Button(win, text="Delete Selected", width=14,
                  bg=DEL_BG, fg="white", activebackground=DEL_ACTIVE,
                  command=delete_selected).pack(pady=4)

    # ---------- Navigation ----------
    def prev_month(self):
        self.current_month, self.current_year = (
            (12, self.current_year - 1) if self.current_month == 1
            else (self.current_month - 1, self.current_year)
        )
        self.create_calendar()

    def next_month(self):
        self.current_month, self.current_year = (
            (1, self.current_year + 1) if self.current_month == 12
            else (self.current_month + 1, self.current_year)
        )
        self.create_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    CalendarReminderApp(root)
    root.mainloop()

