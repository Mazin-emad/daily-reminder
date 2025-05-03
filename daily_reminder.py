
import tkinter as tk
import schedule
import time
import threading
import os
from datetime import datetime

REMINDER_LOG = "last_reminder.txt"
remind_later = False

def has_been_shown_today():
    if not os.path.exists(REMINDER_LOG):
        return False
    with open(REMINDER_LOG, "r") as f:
        last_date = f.read().strip()
    return last_date == datetime.now().date().isoformat()

def mark_as_shown():
    with open(REMINDER_LOG, "w") as f:
        f.write(datetime.now().date().isoformat())

def show_reminder():
    global remind_later
    remind_later = False

    def on_done():
        mark_as_shown()
        root.destroy()

    def on_remind():
        global remind_later
        remind_later = True
        root.destroy()

    root = tk.Tk()
    root.title("Daily Reminder")
    root.geometry("300x150")
    root.resizable(False, False)

    label = tk.Label(root, text="Did you commit to GitHub today?", font=("Arial", 12))
    label.pack(pady=20)

    btn_done = tk.Button(root, text="Done", width=10, command=on_done)
    btn_done.pack(side=tk.LEFT, padx=30)

    btn_remind = tk.Button(root, text="Remind me later", width=15, command=on_remind)
    btn_remind.pack(side=tk.RIGHT, padx=30)

    root.mainloop()

    if remind_later:
        schedule.every(15).minutes.do(show_reminder).tag("remind_later")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Show the reminder if not shown today
if not has_been_shown_today():
    show_reminder()

# Start scheduler for "Remind me later"
threading.Thread(target=run_scheduler).start()
