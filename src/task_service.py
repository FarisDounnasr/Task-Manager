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

        if days_left > 1:
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

    print(f"{index + 1}. {title} [{status}] — {due_text}")
