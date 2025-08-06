import json
import os
from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)

def show_menu():
    print("\nTask Manager")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Done")
    print("4. Delete Task")
    print("5. Search Tasks by Keyword")  
    print("6. Exit")                     

tasks = []

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

def load_tasks():
    global tasks
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    else:
        tasks = []

load_tasks()

while True:
    show_menu()
    choice = input("Choose an option(1-6): ")
    if choice == '1':
        title = input("Enter task title: ")
        due_date_str = input("Enter due date (YYYY-MM-DD): ")

        try:
          due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
          tasks.append({
            "title": title,
            "done": False,
            "due_date": due_date_str
          })
          save_tasks()
          print(f"Task '{title}' added with due date {due_date_str}.")
        except ValueError:
         print("Invalid date format. Please use YYYY-MM-DD.")
    elif choice == "2":
     if not tasks:
        print("No tasks yet.")
     else:
        today = datetime.today().date()

        def get_sort_key(task):
            if task["done"]:
                return datetime.max.date()  # push completed tasks to the bottom
            due_str = task.get("due_date", "")
            if due_str:
                try:
                    return datetime.strptime(due_str, "%Y-%m-%d").date()
                except ValueError:
                    return datetime.max.date()  # push invalid dates down
            return datetime.max.date()  # push undated tasks down

        sorted_tasks = sorted(tasks, key=get_sort_key)

        for i, task in enumerate(sorted_tasks):
            status = "✅" if task["done"] else "❌"
            title = task["title"]
            due_str = task.get("due_date", "N/A")

            if due_str != "N/A":
                try:
                    due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
                    days_left = (due_date - today).days

                    if days_left > 1:
                         due_text = f"{Fore.YELLOW}due in {days_left} days{Style.RESET_ALL}"
                    elif days_left == 1:
                        due_text = f"{Fore.YELLOW}due tomorrow{Style.RESET_ALL}"
                    elif days_left == 0:
                        due_text = f"{Fore.YELLOW}due today{Style.RESET_ALL}"
                    else:
                        due_text = f"{Fore.RED}overdue by {-days_left} days{Style.RESET_ALL}"
                except ValueError:
                    due_text = "invalid date"
            else:
                due_text = "no due date"
            
            if task["done"]:
             status = f"{Fore.GREEN}{status}{Style.RESET_ALL}"

            print(f"{i+1}. {title} [{status}] — {due_text}")
    elif choice == "3":
            for i, task in enumerate(tasks):
                print(f"{i+1}. {task['title']}")
            index = int(input("Enter task number to mark as done: ")) - 1
            if 0 <= index < len(tasks):
                tasks[index]["done"] = True
                save_tasks()
                print("Task marked as done.")
            else:
                print("Invalid number.")
    elif choice == '4':
         for i, task in enumerate(tasks):
            print(f"{i+1}. {task['title']}")
         index = int(input("Enter task number to delete: ")) - 1
         if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks()
            print(f"Deleted task: {removed['title']}")
         else:
            print("Invalid number.")
    elif choice == '5':
        keyword = input("Enter a keyword to search for: ").lower()

        matching_tasks = []
        for i, task in enumerate(tasks):
            if keyword in task["title"].lower():
                matching_tasks.append((i, task))
            
        if not matching_tasks:
            print("No tasks found matching that keyword.")
        else:
            print(f"\nFound {len(matching_tasks)} matching task(s):")
            for i, task in matching_tasks:
                status = "✅" if task["done"] else "❌"
                title = task["title"]
                due_str = task.get("due_date", "N/A")

                # Color-code due_text
                if due_str != "N/A":
                    try:
                        due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
                        days_left = (due_date - datetime.today().date()).days

                        if days_left > 1:
                            due_text = f"{Fore.YELLOW}due in {days_left} days{Style.RESET_ALL}"
                        elif days_left == 1:
                            due_text = f"{Fore.YELLOW}due tomorrow{Style.RESET_ALL}"
                        elif days_left == 0:
                            due_text = f"{Fore.YELLOW}due today{Style.RESET_ALL}"
                        else:
                            due_text = f"{Fore.RED}overdue by {-days_left} days{Style.RESET_ALL}"
                    except ValueError:
                        due_text = "invalid date"
                else:
                    due_text = "no due date"

                # Color-code status icon
                if task["done"]:
                    status = f"{Fore.GREEN}✅{Style.RESET_ALL}"
                else:
                    status = f"{Fore.RED}❌{Style.RESET_ALL}"

                # Highlight keyword in title
                title_lower = title.lower()
                start = title_lower.find(keyword)
                if start != -1:
                    end = start + len(keyword)
                    title_display = (
                        title[:start]
                        + f"{Fore.YELLOW}{title[start:end]}{Style.RESET_ALL}"
                        + title[end:]
                    )
                else:
                    title_display = title

                # Final display
                print(f"{i+1}. {title_display} [{status}] — {due_text}")
    elif choice == '6':
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please try again.")
