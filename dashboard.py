import tkinter as tk

from datetime import datetime
from database.database import (
    load_subjects,
    load_availability,
    get_dashboard_statistics,
    load_tasks
)
from logic import get_priority_label


# --------------------------------------------------
# Small Dashboard Card
# --------------------------------------------------

def create_stat_card(parent, title, value):

    card = tk.Frame(
        parent,
        bg="#F8F9FA",
        bd=1,
        relief="solid",
        padx=20,
        pady=15
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 11),
        bg="#F8F9FA",
        fg="#555555"
    ).pack()

    tk.Label(
        card,
        text=str(value),
        font=("Arial", 22, "bold"),
        bg="#F8F9FA"
    ).pack(pady=5)

    return card


# --------------------------------------------------
# Dashboard
# --------------------------------------------------

def show_dashboard(parent, app):

    frame = tk.Frame(
        parent,
        bg="white"
    )

    subjects = load_subjects()
    availability = load_availability()
    tasks = load_tasks()

    (
        total_tasks,
        completed_tasks,
        pending_tasks,
        highest_priority,
        progress
    ) = get_dashboard_statistics()

    # =====================================
    # TITLE
    # =====================================

    tk.Label(
        frame,
        text="Dashboard",
        font=("Arial", 26, "bold"),
        bg="white"
    ).pack(
        pady=(20, 5)
    )

    tk.Label(
        frame,
        text="Welcome back! Here's your study overview.",
        font=("Arial", 12),
        bg="white",
        fg="gray"
    ).pack(
        pady=(0, 25)
    )

    # =====================================
    # STATISTICS CARDS
    # =====================================

    cards = tk.Frame(
        frame,
        bg="white"
    )

    cards.pack()

    create_stat_card(
        cards,
        "📋 Total Tasks",
        total_tasks
    ).grid(row=0, column=0, padx=12)

    create_stat_card(
        cards,
        "⏳ Pending",
        pending_tasks
    ).grid(row=0, column=1, padx=12)

    create_stat_card(
        cards,
        "✅ Completed",
        completed_tasks
    ).grid(row=0, column=2, padx=12)

    urgent_count = 0

    for task in tasks:

        if task[7] == 0:

            if task[6] is not None and task[6] >= 8:

                urgent_count += 1

    create_stat_card(
        cards,
        "🔥 Urgent",
        urgent_count
    ).grid(row=0, column=3, padx=12)

    # =====================================
    # PROGRESS
    # =====================================

    progress_frame = tk.LabelFrame(
        frame,
        text="📈 Overall Progress",
        bg="white",
        padx=15,
        pady=10,
        font=("Arial", 12, "bold")
    )

    progress_frame.pack(
        fill="x",
        padx=20,
        pady=15
    )

    progress_bar = tk.Canvas(
        progress_frame,
        width=500,
        height=25,
        bg="white",
        highlightthickness=0
    )

    progress_bar.pack(pady=10)

    progress_bar.create_rectangle(
        0,
        0,
        500,
        25,
        fill="#E0E0E0",
        outline=""
    )

    filled = (progress / 100) * 500

    progress_bar.create_rectangle(
        0,
        0,
        filled,
        25,
        fill="#4CAF50",
        outline=""
    )

    tk.Label(
        progress_frame,
        text=f"{progress:.0f}% Complete ({completed_tasks}/{total_tasks} tasks)",
        bg="white",
        font=("Arial", 11)
    ).pack()

    # =====================================
    # TODAY'S FOCUS
    # =====================================

    focus = tk.LabelFrame(
        frame,
        text="🎯 Today's Focus",
        bg="white",
        padx=20,
        pady=15,
        font=("Arial", 12, "bold")
    )

    focus.pack(
        fill="x",
        padx=20,
        pady=15
    )

    # -------------------------------------------------
    # Get pending tasks
    # -------------------------------------------------

    pending_tasks = [
        task for task in tasks
        if task[7] == 0
    ]

    # -------------------------------------------------
    # Calculate how urgent each task is
    # -------------------------------------------------

    today = datetime.today().date()


    def focus_sort_key(task):

        deadline_text = task[4]

        try:
            deadline = datetime.strptime(
                deadline_text,
                "%Y-%m-%d"
            ).date()

            days_left = (deadline - today).days

        except ValueError:

            # Invalid deadline goes to the bottom
            days_left = 9999

        priority = (
            task[6]
            if task[6] is not None
            else 0
        )

        # ---------------------------------------------
        # Deadline has the strongest influence
        # ---------------------------------------------

        if days_left < 0:
            deadline_group = 0       # Overdue

        elif days_left == 0:
            deadline_group = 1       # Today

        elif days_left == 1:
            deadline_group = 2       # Tomorrow

        elif days_left <= 3:
            deadline_group = 3       # Within 3 days

        else:
            deadline_group = 4       # Later

        return (
            deadline_group,
            -priority
        )


    # -------------------------------------------------
    # Sort Today's Focus
    # -------------------------------------------------

    pending_tasks.sort(
        key=focus_sort_key
    )

    # -------------------------------------------------
    # Display top 3 priority tasks
    # -------------------------------------------------

    if pending_tasks:

        for task in pending_tasks[:3]:

            (
                task_id,
                title,
                subject,
                task_type,
                deadline,
                hours,
                priority,
                completed
            ) = task[:8]

            # -----------------------------
            # Task container
            # -----------------------------

            task_frame = tk.Frame(
                focus,
                bg="white"
            )

            task_frame.pack(
                fill="x",
                pady=8
            )

            # -----------------------------
            # Task title
            # -----------------------------

            tk.Label(
                task_frame,
                text=title,
                font=("Arial", 14, "bold"),
                bg="white"
            ).pack(
                anchor="w"
            )

            # -----------------------------
            # Task information
            # -----------------------------

            tk.Label(
                task_frame,
                text=(
                    f"📚 {subject}    "
                    f"📅 Due: {deadline}    "
                    f"⏱ {hours} hour(s)"
                ),
                font=("Arial", 10),
                bg="white",
                fg="gray"
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

            # -----------------------------
            # Priority
            # -----------------------------

            tk.Label(
                task_frame,
                text=get_priority_label(priority),
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#E65100"
            ).pack(
                anchor="w",
                pady=(3, 3)
            )

            # -----------------------------
            # Start Studying
            # -----------------------------

            tk.Button(
                task_frame,
                text="▶ Start Studying",
                bg="#2E7D32",
                fg="white",
                font=("Arial", 10, "bold"),
                padx=12,
                pady=5,
                command=lambda id=task_id: app.study_session(id)
            ).pack(
                anchor="w",
                pady=(2, 5)
            )

    else:

        tk.Label(
            focus,
            text="You're all caught up! 🎉",
            font=("Arial", 12),
            bg="white"
        ).pack(
            anchor="w"
        ) 
    # =====================================
    # UPCOMING TASKS
    # =====================================

    upcoming = tk.LabelFrame(
        frame,
        text="📅 Upcoming Tasks",
        bg="white",
        padx=15,
        pady=10,
        font=("Arial", 12, "bold")
    )

    upcoming.pack(
        fill="x",
        padx=20,
        pady=10
    )

    if len(tasks) == 0:

        tk.Label(
            upcoming,
            text="No tasks yet.",
            bg="white"
        ).pack(anchor="w")

    else:

        for task in tasks[:5]:

            tk.Label(
                upcoming,
                text=f"• {task[1]} ({task[4]})",
                bg="white",
                font=("Arial", 11)
            ).pack(anchor="w")


    return frame