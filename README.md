
# 📌 Daily Reminder

A simple Python desktop reminder app

It includes a user-friendly popup with two options:
- ✅ **Done** — marks the reminder as completed for the day.
- 🔁 **Remind me later** — snoozes the reminder for 15 minutes.

---

## ✨ Features

- 📅 Runs **once a day** whenever you start your PC
- 🔁 "Remind me later" option shows the popup again in 15 minutes
- ✅ Marks the reminder as "done" once per day
- 🪟 Built with `tkinter` for a native GUI
- 🧠 Uses `schedule` for lightweight daily scheduling
- 🧰 Easily converted into a `.exe` using `PyInstaller`

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/github-reminder.git
cd github-reminder
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv reminder-env
reminder-env\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python daily_reminder.py
```

---

## 🛠️ Build as Executable (Windows)

Use [PyInstaller](https://pyinstaller.org/) to build a `.exe`:

```bash
pyinstaller --onefile --noconsole daily_reminder.py
```

- The `.exe` will be located in the `dist/` folder.
- To make it auto-start with Windows, copy the `.exe` to:
  ```
  shell:startup
  ```

---

## 📁 File Structure

```
github-reminder/
│
├── daily_reminder.py      # Main app script
├── requirements.txt       # Dependencies
├── README.md              # You're here!
├── .gitignore             # Git ignored files
└── dist/                  # (created after building .exe)
```

---

## 📦 Dependencies

- `schedule` – lightweight job scheduling
- `tkinter` – built-in GUI library (no installation needed)
- `pyinstaller` – optional, for creating the `.exe`

Install with:

```bash
pip install -r requirements.txt
```

