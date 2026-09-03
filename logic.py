from datetime import datetime, timedelta


def calculate_priority(deadline, estimated_hours, level):
    """
    Calculates the priority score for a task.

    Higher score = higher priority.
    """

    today = datetime.today()

    due_date = datetime.strptime(
        deadline,
        "%Y-%m-%d"
    )

    days_left = (due_date - today).days

    if days_left <= 0:
        days_left = 1

    if level == "HL":
        weight = 1.5
    else:
        weight = 1.0

    priority = (
        float(estimated_hours) * weight
    ) / days_left

    return round(priority, 2)

from database.database import (load_tasks, load_availability)


def generate_study_plan():
    """
    Generates a weekly study plan based on:
    - task priority
    - task deadline
    - estimated study hours
    - user's daily availability

    Also identifies work that cannot fit before its deadline.
    """

    weekly_hours = get_weekly_hours()
    tasks = load_tasks()

    # -------------------------------------------------
    # Pending tasks only
    # -------------------------------------------------

    pending = []

    for task in tasks:

        if task[7] == 0:
            pending.append(task)

    # -------------------------------------------------
    # Highest priority first
    # -------------------------------------------------

    pending.sort(
        key=lambda task: task[6] if task[6] is not None else 0,
        reverse=True
    )

    # -------------------------------------------------
    # Days
    # -------------------------------------------------

    all_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    today = datetime.today().date()
    today_index = datetime.today().weekday()

    days = (
        all_days[today_index:]
        + all_days[:today_index]
    )

    # -------------------------------------------------
    # Empty study plan
    # -------------------------------------------------

    study_plan = {}

    for day in days:
        study_plan[day] = []

    # -------------------------------------------------
    # Unscheduled tasks
    # -------------------------------------------------

    unscheduled = []

    # -------------------------------------------------
    # Schedule tasks
    # -------------------------------------------------

    for task in pending:

        task_name = task[1]
        subject = task[2]
        deadline = task[4]
        hours_needed = float(task[5])

        # ---------------------------------------------
        # Convert deadline
        # ---------------------------------------------

        try:

            deadline_date = datetime.strptime(
                deadline,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            continue

        # ---------------------------------------------
        # Find valid days
        # ---------------------------------------------

        valid_days = []

        for day in days:

            day_index = all_days.index(day)

            days_from_today = (
                day_index - today_index
            ) % 7

            scheduled_date = (
                today
                + timedelta(days=days_from_today)
            )

            if scheduled_date <= deadline_date:

                valid_days.append(day)

        # ---------------------------------------------
        # Allocate available time
        # ---------------------------------------------

        remaining = hours_needed

        for day in valid_days:

            if remaining <= 0:
                break

            available = weekly_hours.get(
                day,
                0
            )

            if available <= 0:
                continue

            hours_today = min(
                available,
                remaining
            )

            study_plan[day].append(
                (
                    task_name,
                    subject,
                    hours_today
                )
            )

            weekly_hours[day] -= hours_today

            remaining -= hours_today

        # ---------------------------------------------
        # Couldn't fit everything
        # ---------------------------------------------

        if remaining > 0:

            unscheduled.append(
                (
                    task_name,
                    subject,
                    remaining,
                    deadline
                )
            )

    return study_plan, unscheduled


def create_schedule():

    tasks = generate_study_plan()

    availability = load_availability()

    schedule = {}

    task_index = 0
    remaining_hours = 0
    current_task = None

    for day, available in availability:

        available = int(available)

        schedule[day] = []

        while available > 0 and task_index < len(tasks):

            if current_task is None:

                current_task = tasks[task_index]

                remaining_hours = current_task[5]

            study = min(
                available,
                remaining_hours
            )

            schedule[day].append(
                (
                    current_task[1],
                    study
                )
            )

            available -= study

            remaining_hours -= study

            if remaining_hours == 0:

                task_index += 1

                current_task = None

    return schedule

def get_weekly_hours():
    """
    Returns the user's available study hours
    for each day of the week.
    """

    availability = load_availability()

    weekly_hours = {}

    for day, hours in availability:

        weekly_hours[day] = int(hours)

    return weekly_hours

from datetime import datetime


def get_deadline_status(deadline, completed):

    if completed:
        return "completed"

    today = datetime.today().date()
    deadline = datetime.strptime(deadline, "%Y-%m-%d").date()

    days = (deadline - today).days

    if days < 0:
        return "overdue"

    elif days == 0:
        return "today"

    elif days == 1:
        return "tomorrow"

    elif days <= 3:
        return "soon"

    else:
        return "normal"
# ==========================================
# Priority Label
# ==========================================
def get_priority_label(priority):

    if priority is None:
        return "None"

    elif priority >= 10:
        return "Urgent"

    elif priority >= 8:
        return "Critical"

    elif priority >= 5:
        return "High"

    elif priority >= 2:
        return "Medium"

    else:
        return "Low"
