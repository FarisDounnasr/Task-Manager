def get_recommended_tasks(tasks):
    recommendations = []

    for task in tasks:
        if not task.get("is_recurring"):
            continue

        if task.get("done"):
            continue

        recommendations.append({"task": task, "reason": "Recurring task is due again."})

    return recommendations