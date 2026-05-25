#  Intelligent Task Manager (CLI)

A **command-line task manager** written in Python that lets you add, view, search, and manage tasks with **due dates, sorting, and colorful visual indicators**.  
Tasks are saved to a JSON file so your list is always there when you return.

---

## 📸 Screenshots

### Main Menu
![Main Menu Screenshot](https://github.com/user-attachments/assets/daf61325-3e5d-4f04-82f1-b59b3467b52c)

### Viewing Tasks (with colors)
![View Tasks Screenshot](https://github.com/user-attachments/assets/3f89b04d-200e-4e1b-af12-fa431f90e6da)

---

##  Features

- **Add Tasks** — with optional due dates in `YYYY-MM-DD` format
- **View Tasks** — sorted by due date, completed tasks pushed to the bottom
- **Mark Tasks as Done** — ✅ in green
- **Delete Tasks** — remove unwanted tasks
- **Search by Keyword** — highlights matches in yellow
- **Color Coding**:
  - 🟢 Green ✅ — Completed tasks
  - 🔴 Red ❌ — Incomplete tasks
  - 🟡 Yellow — Due today/tomorrow/upcoming
  - 🔴 Red text — Overdue tasks
- **Persistent Storage** — tasks saved in `tasks.json`

---

##  Built With

- **Python 3**
- **colorama** — for colorful output
- **datetime** — for date handling
- **json** — for lightweight file storage

---

##  Installation

Make sure you have **Python 3.10+** installed.

```bash
# Clone the repository
git clone https://github.com/FarisDounnasr/Task-Manager.git
cd Task-Manager

# Install dependencies
pip install -r requirements.txt


