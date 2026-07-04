def get_statistics(tasks):
    total = len(tasks)
    completed = sum(1 for task in tasks if task.get("done"))
    active = total - completed
    recurring = sum(1 for task in tasks if task.get("is_recurring"))
    one_time = total - recurring

    category_counts = {}
    total_completions = 0

    for task in tasks:
        category = task.get("category") or "Uncategorized"
        completions = len(task.get("completed_dates", []))

        total_completions += completions
        category_counts[category] = category_counts.get(category, 0) + completions

    most_active_category = None

    if category_counts:
        most_active_category = max(
            category_counts.items(),
            key=lambda item: item[1]
        )

    return {
        "total": total,
        "completed": completed,
        "active": active,
        "recurring": recurring,
        "one_time": one_time,
        "total_completions": total_completions,
        "category_counts": category_counts,
        "most_active_category": most_active_category,
    }