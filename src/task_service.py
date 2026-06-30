from datetime import datetime
from colorama import Fore, Style

def get_due_text(task):
    if task.get("done"):
        return f"{Fore.GREEN}completed{Style.RESET_ALL}"

    due_str = task.get("due_date", "N/A")

    if due_str == "N/A":
        return "no due date"

    try:
        due_date = datetime.strptime(due_str, "%Y-%m-%d").date()
        today = datetime.today().date()
        days_left = (due_date - today).days

        if days_left > 3:
            return f"due in {days_left} days"
        elif days_left > 1:
            return f"{Fore.YELLOW}due in {days_left} days{Style.RESET_ALL}"
        elif days_left == 1:
            return f"{Fore.YELLOW}due tomorrow{Style.RESET_ALL}"
        elif days_left == 0:
            return f"{Fore.YELLOW}due today{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}overdue by {-days_left} days{Style.RESET_ALL}"

    except ValueError:
        return "invalid date"
    
def get_status_text(task):
    if task["done"]:
        return f"{Fore.GREEN}✅{Style.RESET_ALL}"
    return f"{Fore.RED}❌{Style.RESET_ALL}"


def display_task(task, index, title_display=None):
    status = get_status_text(task)
    title = title_display if title_display is not None else task["title"]
    due_text = get_due_text(task)
    category = task.get("category")

    if category:
        print(f"{index + 1}. {title} [{status}] - {due_text} - {category}")
    else:
        print(f"{index + 1}. {title} [{status}] - {due_text}")

def update_recurring_tasks(tasks):
    today = datetime.today().date()
    updated = False

    for task in tasks:
        if not task.get("is_recurring"):
            continue

        if task.get("done") is not True:
            continue

        interval = task.get("target_interval_days")
        if not isinstance(interval, int) or interval < 1:
            continue

        last_completed = task.get("last_completed_date")
        if not last_completed:
            continue

        try:
            last_completed_date = datetime.strptime(last_completed, "%Y-%m-%d").date()
        except ValueError:
            continue

        days_since = (today - last_completed_date).days

        if days_since >= interval:
            task["done"] = False
            updated = True

    return updated