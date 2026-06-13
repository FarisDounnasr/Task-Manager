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
