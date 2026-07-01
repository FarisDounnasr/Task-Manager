from datetime import datetime


def get_recommendation_reason(task):
    interval = task.get("target_interval_days")
    last_completed = task.get("last_completed_date")

    if last_completed:
        last_completed_date = datetime.strptime(last_completed, "%Y-%m-%d").date()
        days_since = (datetime.today().date() - last_completed_date).days

        if interval:
            return (
                f"Last completed {days_since} day(s) ago. "
                f"Target interval is every {interval} day(s)."
            )

        return f"Last completed {days_since} day(s) ago."

    if interval:
        return f"Target interval is every {interval} day(s)."

    return "This recurring task has not been completed yet."


def get_recommended_tasks(tasks):
    recommendations = []

    for task in tasks:
        if not task.get("is_recurring"):
            continue

        if task.get("done"):
            continue

        recommendations.append({
            "task": task,
            "reason": get_recommendation_reason(task)
        })

    return recommendations