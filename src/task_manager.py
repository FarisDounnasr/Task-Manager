"""
purpose: A command-line task manager with features to add, view, mark as done, delete, and search tasks.
Inputs/Outputs: User inputs via command line; outputs task list and statuses to console.
Key data structures: List of dictionaries to store tasks, each with title, status, and due date.
Main control flow: Menu-driven interface with a loop to handle user choices.
Error handling & edge cases: Handles invalid inputs, empty task list, and date parsing errors.
Performance notes: Suitable for small to medium task lists; uses JSON for persistence.
dependencies: colorama for colored terminal output, json for data persistence.
"""
import json
import os
from datetime import datetime
from colorama import Fore, Style, init
from storage import save_tasks, load_tasks
from task_service import get_due_text

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

while True:
    show_menu()
    choice = input("Choose an option(1-6): ")
    if choice == '1':  
        """
    What it does: Adds a new task with a title and due date.
    Inputs/Outputs: Takes user input for title and due date; outputs confirmation message.
    Invariants/assumptions: Title is a non-empty string; due date is in YYYY-MM-DD format.
    Algorithm steps: Prompt for title and due date, validate date, append to tasks list, save tasks.
    Complexity: O(1) for adding a task; O(n) for saving tasks.
    Edge cases: Handles invalid date format.
     """
        title = input("Enter task title: ")
        due_date_str = input("Enter due date (YYYY-MM-DD): ")

        try:
          due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
          tasks.append({
            "title": title,
            "done": False,
            "due_date": due_date_str
          })
          save_tasks(tasks)
          print(f"Task '{title}' added with due date {due_date_str}.")
        except ValueError:
         print("Invalid date format. Please use YYYY-MM-DD.")
    elif choice == "2":
        """
        What it does: Displays all tasks sorted by due date, with color-coded statuses.
        Inputs/Outputs: Outputs task list to console.   
        Invariants/assumptions: Tasks have 'title', 'done', and optional 'due_date'.
        Algorithm steps: Sort tasks, color-code based on status and due date, print tasks.
        Complexity: O(n log n) for sorting; O(n) for displaying.
        Edge cases: Handles empty task list and invalid/missing due dates.
        """
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

                due_text = get_due_text(task)
                
                if task["done"]:
                    status = f"{Fore.GREEN}{status}{Style.RESET_ALL}"

                print(f"{i+1}. {title} [{status}] — {due_text}")
    elif choice == "3":
        """
        What it does: Marks a specified task as done.
        Inputs/Outputs: Takes user input for task number; outputs confirmation message.
        Invariants/assumptions: Task number is valid and corresponds to an existing task.
        Algorithm steps: Display tasks, prompt for task number, update status, save tasks.
        Complexity: O(n) for displaying tasks; O(1) for updating status; O(n) for saving tasks.
        Edge cases: Handles invalid task numbers and empty task list.
        """
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task['title']}")
        index = int(input("Enter task number to mark as done: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            save_tasks(tasks)
            print("Task marked as done.")
        else:
            print("Invalid number.")
    elif choice == '4':
        """
        What it does: Deletes a specified task from the list.
        Inputs/Outputs: Takes user input for task number; outputs confirmation message.
        Invariants/assumptions: Task number is valid and corresponds to an existing task.
        Algorithm steps: Display tasks, prompt for task number, remove task, save tasks.
        Complexity: O(n) for displaying tasks; O(1) for removing task; O(n) for saving tasks.
        Edge cases: Handles invalid task numbers and empty task list.
        """
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task['title']}")
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            save_tasks(tasks)
            print(f"Deleted task: {removed['title']}")
        else:
            print("Invalid number.")
    elif choice == '5':
        """
        What it does: Searches tasks by a keyword and displays matching tasks with highlights.
        Inputs/Outputs: Takes user input for keyword; outputs matching tasks to console.
        Invariants/assumptions: Tasks have 'title', 'done', and optional 'due_date'.
        Algorithm steps: Prompt for keyword, search tasks, color-code matches, print results.
        Complexity: O(n) for searching and displaying tasks.
        Edge cases: Handles no matches and empty task list.
        """
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

                if task["done"]:
                    due_text = f"{Fore.GREEN}completed{Style.RESET_ALL}"
                elif due_str != "N/A":
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
        """
        What it does: Exits the task manager program.
        Inputs/Outputs: Outputs a goodbye message.
        Invariants/assumptions: None.
        Algorithm steps: Print goodbye message, break loop.
        Complexity: O(1).
        Edge cases: None.
        """
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please try again.")

