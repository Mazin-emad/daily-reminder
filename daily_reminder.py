import tkinter as tk
import schedule
import time
import threading
import os
from datetime import datetime, timedelta

# Constants
REMINDER_LOG = "github_reminder_log.txt"
CONFIG_FILE = "github_reminder_config.txt"
DEFAULT_REMINDER_HOUR = 18  # 6 PM default reminder time
DEFAULT_SNOOZE_MINUTES = 30

class GitHubReminderApp:
    def __init__(self):
        self.remind_later = False
        self.reminder_hour = self._load_config().get('hour', DEFAULT_REMINDER_HOUR)
        self.snooze_minutes = self._load_config().get('snooze', DEFAULT_SNOOZE_MINUTES)
        
        # Start the scheduling system
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        # Schedule next day's reminder
        self._schedule_next_daily_reminder()
        
        # Show immediately if needed
        if not self._has_been_shown_today():
            self.show_reminder()

    def _load_config(self):
        """Load configuration settings"""
        config = {'hour': DEFAULT_REMINDER_HOUR, 'snooze': DEFAULT_SNOOZE_MINUTES}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    for line in f:
                        if "=" in line:
                            key, value = line.strip().split("=")
                            config[key] = int(value)
            except:
                pass  # Use defaults if config file is invalid
        return config

    def _save_config(self, hour=None, snooze=None):
        """Save configuration settings"""
        if hour is not None:
            self.reminder_hour = hour
        if snooze is not None:
            self.snooze_minutes = snooze
            
        with open(CONFIG_FILE, "w") as f:
            f.write(f"hour={self.reminder_hour}\n")
            f.write(f"snooze={self.snooze_minutes}\n")

    def _has_been_shown_today(self):
        """Check if reminder has been shown today"""
        if not os.path.exists(REMINDER_LOG):
            return False
        
        try:
            with open(REMINDER_LOG, "r") as f:
                last_date = f.read().strip()
            return last_date == datetime.now().date().isoformat()
        except:
            return False  # If file is corrupt or unreadable, show reminder

    def _mark_as_shown(self):
        """Mark reminder as shown for today"""
        with open(REMINDER_LOG, "w") as f:
            f.write(datetime.now().date().isoformat())

    def _clear_reminders(self, tag=None):
        """Clear existing scheduled reminders"""
        if tag:
            schedule.clear(tag)
        else:
            schedule.clear()

    def _schedule_next_daily_reminder(self):
        """Schedule the reminder for tomorrow"""
        self._clear_reminders("daily")
        schedule.every().day.at(f"{self.reminder_hour:02d}:00").do(self.show_reminder).tag("daily")
        print(f"Next reminder scheduled for tomorrow at {self.reminder_hour:02d}:00")

    def _schedule_snooze(self):
        """Schedule a reminder for later today"""
        self._clear_reminders("snooze")
        schedule.every(self.snooze_minutes).minutes.do(self.show_reminder).tag("snooze")
        print(f"Reminder snoozed for {self.snooze_minutes} minutes")

    def _run_scheduler(self):
        """Run the scheduler in background"""
        while True:
            schedule.run_pending()
            time.sleep(1)

    def show_reminder(self):
        """Show the reminder dialog"""
        self.remind_later = False
        
        def on_done():
            self._mark_as_shown()
            self._schedule_next_daily_reminder()
            root.destroy()

        def on_snooze():
            self.remind_later = True
            self._schedule_snooze()
            root.destroy()
            
        def on_settings():
            settings_window = tk.Toplevel(root)
            settings_window.title("Settings")
            settings_window.geometry("300x200")
            settings_window.resizable(False, False)
            
            # Time setting
            time_frame = tk.Frame(settings_window)
            time_frame.pack(pady=10)
            tk.Label(time_frame, text="Daily reminder hour (0-23):").pack(side=tk.LEFT, padx=5)
            hour_var = tk.StringVar(value=str(self.reminder_hour))
            hour_entry = tk.Entry(time_frame, textvariable=hour_var, width=5)
            hour_entry.pack(side=tk.LEFT)
            
            # Snooze setting
            snooze_frame = tk.Frame(settings_window)
            snooze_frame.pack(pady=10)
            tk.Label(snooze_frame, text="Snooze minutes:").pack(side=tk.LEFT, padx=5)
            snooze_var = tk.StringVar(value=str(self.snooze_minutes))
            snooze_entry = tk.Entry(snooze_frame, textvariable=snooze_var, width=5)
            snooze_entry.pack(side=tk.LEFT)
            
            def save_settings():
                try:
                    hour = int(hour_var.get())
                    snooze = int(snooze_var.get())
                    
                    if 0 <= hour <= 23 and snooze > 0:
                        self._save_config(hour=hour, snooze=snooze)
                        self._schedule_next_daily_reminder()
                        settings_window.destroy()
                    else:
                        tk.Label(settings_window, text="Invalid values", fg="red").pack()
                except ValueError:
                    tk.Label(settings_window, text="Please enter valid numbers", fg="red").pack()
            
            save_btn = tk.Button(settings_window, text="Save", command=save_settings)
            save_btn.pack(pady=10)

        root = tk.Tk()
        root.title("GitHub Commit Reminder")
        root.geometry("400x200")
        root.resizable(False, False)
        
        # Make window appear on top
        root.attributes("-topmost", True)
        
        # Main reminder text
        label = tk.Label(root, text="Did you commit to GitHub today?", font=("Arial", 14, "bold"))
        label.pack(pady=20)
        
        # Current time display
        time_label = tk.Label(root, text=f"Current time: {datetime.now().strftime('%H:%M:%S')}")
        time_label.pack(pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15, fill=tk.X)
        
        # Action buttons
        btn_done = tk.Button(btn_frame, text="Yes, I did!", width=12, bg="#4CAF50", fg="white", command=on_done)
        btn_done.pack(side=tk.LEFT, padx=15)
        
        btn_remind = tk.Button(btn_frame, text=f"Snooze ({self.snooze_minutes}m)", width=12, command=on_snooze)
        btn_remind.pack(side=tk.LEFT, padx=15)
        
        btn_settings = tk.Button(btn_frame, text="⚙️", width=4, command=on_settings)
        btn_settings.pack(side=tk.LEFT, padx=15)
        
        # Update time continuously
        def update_time():
            time_label.config(text=f"Current time: {datetime.now().strftime('%H:%M:%S')}")
            root.after(1000, update_time)
        update_time()
        
        root.mainloop()

if __name__ == "__main__":
    app = GitHubReminderApp()
    
    # Keep the main thread alive
    while True:
        time.sleep(1)