from datetime import datetime, timedelta


MILESTONE_TEMPLATES = {

    "IA": [
        "Research",
        "Planning",
        "Data Collection",
        "Analysis",
        "First Draft",
        "Final Review"
    ],

    "EE": [
        "Research",
        "Outline",
        "Writing",
        "Editing",
        "Final Review"
    ],

    "Presentation": [
        "Research",
        "Create Slides",
        "Practice",
        "Final Review"
    ]
}
def generate_milestones(task_type):

    return MILESTONE_TEMPLATES.get(task_type, [])

def calculate_milestone_dates(deadline, milestone_count):

    today = datetime.today()

    deadline = datetime.strptime(
        deadline,
        "%Y-%m-%d"
    )

    total_days = (deadline - today).days

    if total_days <= 0:
        return []

    spacing = total_days / milestone_count

    dates = []

    for i in range(milestone_count):

        milestone_date = today + timedelta(
            days=spacing * (i + 1)
        )

        dates.append(
            milestone_date.strftime("%Y-%m-%d")
        )

    return dates

from logic import calculate_priority


def generate_milestone_tasks(
    title,
    subject,
    task_type,
    deadline,
    hours,
    level
):

    names = generate_milestones(task_type)

    if len(names) == 0:
        return []

    dates = calculate_milestone_dates(
        deadline,
        len(names)
    )

    milestone_hours = float(hours) / len(names)

    tasks = []

    for name, date in zip(names, dates):

        priority = calculate_priority(
            date,
            milestone_hours,
            level
        )

        tasks.append(
            (
                f"{title} - {name}",
                subject,
                "Milestone",
                date,
                round(milestone_hours, 1),
                priority
            )
        )

    return tasks
