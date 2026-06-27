"""
purpose: A command-line task manager with features to add, view, mark as done, delete, and search tasks.
Inputs/Outputs: User inputs via command line; outputs task list and statuses to console.
Key data structures: List of dictionaries to store tasks, each with title, status, and due date.
Main control flow: Menu-driven interface with a loop to handle user choices.
Error handling & edge cases: Handles invalid inputs, empty task list, and date parsing errors.
Performance notes: Suitable for small to medium task lists; uses JSON for persistence.
dependencies: colorama for colored terminal output, json for data persistence.
"""
from datetime import datetime
from colorama import Fore, Style, init
from storage import save_tasks, load_tasks
from task_service import get_due_text, display_task

init(autoreset=True)

def show_menu():
    print("\nTask Manager")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Mark Task as Done")
    print("4. Delete Task")
    print("5. Search Tasks by Keyword")  
    print("6. Exit") 
"""      
Displays the main menu options to the user.
Inputs/Outputs: None; prints menu to console.
Invariants/assumptions: None.
Algorithm steps: Print menu options.
Complexity: O(1).
Edge cases: None.
"""

tasks = load_tasks()

def choose_category():
    categories = [
        "Health",
        "Study",
        "Career",
        "Personal",
        "Chores",
        "Social",
        "Other",
        "None"
    ]

    print("\nChoose a category:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    choice = input("Enter category number: ").strip()

    if not choice.isdigit():
        return None

    index = int(choice) - 1

    if 0 <= index < len(categories):
        selected = categories[index]
        return None if selected == "None" else selected

    return None


def add_task(tasks):
    title = input("Enter task title: ")
    due_date_str = input("Enter due date (YYYY-MM-DD): ")

    try:
        datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    category = choose_category()

    recurring_input = input("Is this a recurring task? (y/n): ").strip().lower()
    is_recurring = recurring_input == "y"

    target_interval_days = None

    if is_recurring:
        interval_input = input(
            "Optional starting interval in days (press Enter to skip): "
        ).strip()

        if interval_input:
            if interval_input.isdigit():
                target_interval_days = int(interval_input)
            else:
                print("Invalid interval. Task will be added without a target interval.")

    task = {
        "title": title,
        "done": False,
        "due_date": due_date_str,
        "category": category,
        "is_recurring": is_recurring,
        "target_interval_days": target_interval_days,
        "created_date": datetime.today().strftime("%Y-%m-%d"),
        "completed_dates": [],
        "last_completed_date": None
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{title}' added with due date {due_date_str}.")

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

def view_tasks(tasks):
    if not tasks:
        print("No tasks yet.")
        return
    
    sorted_tasks = sorted(tasks, key=get_sort_key)

    for i, task in enumerate(sorted_tasks):
        display_task(task, i)

def mark_task_done(tasks):
    for i, task in enumerate(tasks):
        print(f"{i+1}. {task['title']}")

    index = int(input("Enter task number to mark as done: ")) - 1

    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)
        print("Task marked as done.")
    else:
        print("Invalid number.")

def delete_task(tasks):
    for i, task in enumerate(tasks):
        print(f"{i+1}. {task['title']}")
    index = int(input("Enter task number to delete: ")) - 1
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"Deleted task: {removed['title']}")
    else:
        print("Invalid number.")

def search_tasks(tasks):
    keyword = input("Enter a keyword to search for: ").strip().lower()

    matching_tasks = []
    for i, task in enumerate(tasks):
        if keyword in task["title"].lower():
            matching_tasks.append((i, task))
        
    if not matching_tasks:
        print("No tasks found matching that keyword.")
    else:
        print(f"\nFound {len(matching_tasks)} matching task(s):")
        for i, task in matching_tasks:
            title = task["title"]

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
            display_task(task, i, title_display)
def main():
    while True:
        show_menu()
        choice = input("Choose an option(1-6): ")
        if choice == '1':  
            add_task(tasks)
            
        elif choice == "2":
           view_tasks(tasks)

        elif choice == "3":
           mark_task_done(tasks)

        elif choice == '4':
            delete_task(tasks)
        
        elif choice == '5':
            search_tasks(tasks)

        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()