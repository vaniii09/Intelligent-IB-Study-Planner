
import tkinter as tk
from datetime import datetime

from database.database import (
    load_subjects,
    load_availability,
    get_dashboard_statistics,
    load_tasks
)

from logic import get_priority_label
from theme import *


# =========================================================
# Dashboard Helpers
# =========================================================

def create_stat_card(parent, title, value, accent):

    card = tk.Frame(
        parent,
        bg=SURFACE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    tk.Frame(
        card,
        bg=accent,
        height=4
    ).pack(fill="x")

    body = tk.Frame(
        card,
        bg=SURFACE
    )

    body.pack(
        fill="both",
        expand=True,
        padx=16,
        pady=14
    )

    tk.Label(
        body,
        text=title,
        font=("Arial", 10),
        bg=SURFACE,
        fg=MUTED
    ).pack(anchor="w")

    tk.Label(
        body,
        text=str(value),
        font=("Arial", 25, "bold"),
        bg=SURFACE,
        fg=TEXT
    ).pack(
        anchor="w",
        pady=(7, 0)
    )

    return card


def create_section(parent, title, subtitle=None):

    section = tk.Frame(
        parent,
        bg=SURFACE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    header = tk.Frame(
        section,
        bg=SURFACE
    )

    header.pack(
        fill="x",
        padx=20,
        pady=(18, 12)
    )

    tk.Label(
        header,
        text=title,
        font=("Arial", 14, "bold"),
        bg=SURFACE,
        fg=TEXT
    ).pack(anchor="w")

    if subtitle:

        tk.Label(
            header,
            text=subtitle,
            font=("Arial", 9),
            bg=SURFACE,
            fg=MUTED
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

    return section


def parse_deadline(deadline_text):

    if not deadline_text:
        return None

    try:
        return datetime.strptime(
            str(deadline_text),
            "%Y-%m-%d"
        ).date()

    except (ValueError, TypeError):
        return None


# =========================================================
# Dashboard
# =========================================================

def show_dashboard(parent, app):

    # -----------------------------------------------------
    # Main Page
    # -----------------------------------------------------

    frame = tk.Frame(
        parent,
        bg=BACKGROUND
    )

    # -----------------------------------------------------
    # Scrollable Dashboard
    # -----------------------------------------------------

    canvas = tk.Canvas(
        frame,
        bg=BACKGROUND,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        frame,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    content = tk.Frame(
        canvas,
        bg=BACKGROUND
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
    )

    def update_scroll_region(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    def resize_content(event):

        canvas.itemconfigure(
            canvas_window,
            width=event.width
        )

    content.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        resize_content
    )

    # -----------------------------------------------------
    # Load Data
    # -----------------------------------------------------

    tasks = load_tasks()

    (
        total_tasks,
        completed_tasks,
        pending_count,
        highest_priority,
        progress
    ) = get_dashboard_statistics()

    today = datetime.today().date()

    # Only incomplete tasks
    pending_list = [
        task for task in tasks
        if task[7] == 0
    ]

    # -----------------------------------------------------
    # Header
    # -----------------------------------------------------

    header = tk.Frame(
        content,
        bg=BACKGROUND
    )

    header.pack(
        fill="x",
        padx=32,
        pady=(30, 22)
    )

    greeting = tk.Frame(
        header,
        bg=BACKGROUND
    )

    greeting.pack(
        side="left",
        fill="x",
        expand=True
    )

    tk.Label(
        greeting,
        text="Your workspace",
        font=("Arial", 10, "bold"),
        bg=BACKGROUND,
        fg=PRIMARY
    ).pack(anchor="w")

    tk.Label(
        greeting,
        text="Good to see you!",
        font=("Arial", 27, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    ).pack(
        anchor="w",
        pady=(5, 4)
    )

    tk.Label(
        greeting,
        text="A little progress every day adds up.",
        font=("Arial", 11),
        bg=BACKGROUND,
        fg=MUTED
    ).pack(anchor="w")

    date_frame = tk.Frame(
        header,
        bg=SURFACE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    date_frame.pack(
        side="right",
        anchor="center",
        padx=(12, 0)
    )

    tk.Label(
        date_frame,
        text=today.strftime("%A"),
        font=("Arial", 10),
        bg=SURFACE,
        fg=MUTED
    ).pack(
        padx=18,
        pady=(12, 2)
    )

    tk.Label(
        date_frame,
        text=today.strftime("%d %b %Y"),
        font=("Arial", 13, "bold"),
        bg=SURFACE,
        fg=TEXT
    ).pack(
        padx=18,
        pady=(0, 12)
    )

    # -----------------------------------------------------
    # Statistics
    # -----------------------------------------------------

    tk.Label(
        content,
        text="YOUR OVERVIEW",
        font=("Arial", 9, "bold"),
        bg=BACKGROUND,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=32,
        pady=(0, 12)
    )

    stats = tk.Frame(
        content,
        bg=BACKGROUND
    )

    stats.pack(
        fill="x",
        padx=32
    )

    stat_data = [
        ("Total tasks", total_tasks, PRIMARY),
        ("Pending", pending_count, "#C69A51"),
        ("Completed", completed_tasks, "#739B79"),
        ("High priority", sum(
            1 for task in pending_list
            if task[6] is not None and task[6] >= 8
        ), "#C77979")
    ]

    for column in range(4):
        stats.grid_columnconfigure(
            column,
            weight=1,
            uniform="stats"
        )

    for column, (title, value, accent) in enumerate(stat_data):

        card = create_stat_card(
            stats,
            title,
            value,
            accent
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(0 if column == 0 else 6, 6 if column < 3 else 0)
        )

    # -----------------------------------------------------
    # Progress Card
    # -----------------------------------------------------

    progress_section = create_section(
        content,
        "Overall progress",
        "Keep showing up. Every completed task counts."
    )

    progress_section.pack(
        fill="x",
        padx=32,
        pady=(22, 0)
    )

    progress_body = tk.Frame(
        progress_section,
        bg=SURFACE
    )

    progress_body.pack(
        fill="x",
        padx=20,
        pady=(0, 20)
    )

    progress_top = tk.Frame(
        progress_body,
        bg=SURFACE
    )

    progress_top.pack(fill="x")

    safe_progress = max(
        0,
        min(100, float(progress or 0))
    )

    tk.Label(
        progress_top,
        text=f"{safe_progress:.0f}% completed",
        font=("Arial", 16, "bold"),
        bg=SURFACE,
        fg=PRIMARY
    ).pack(side="left")

    tk.Label(
        progress_top,
        text=f"{completed_tasks} of {total_tasks} tasks",
        font=("Arial", 10),
        bg=SURFACE,
        fg=MUTED
    ).pack(side="right")

    progress_bar = tk.Canvas(
        progress_body,
        height=10,
        bg="#EAECE7",
        highlightthickness=0
    )

    progress_bar.pack(
        fill="x",
        pady=(13, 0)
    )

    def draw_progress(event=None):

        progress_bar.delete("all")

        width = progress_bar.winfo_width()
        height = progress_bar.winfo_height()

        if width <= 1:
            return

        progress_bar.create_rectangle(
            0,
            0,
            width,
            height,
            fill="#EAECE7",
            outline=""
        )

        progress_bar.create_rectangle(
            0,
            0,
            width * safe_progress / 100,
            height,
            fill=PRIMARY,
            outline=""
        )

    progress_bar.bind(
        "<Configure>",
        draw_progress
    )

    # -----------------------------------------------------
    # Main Content Columns
    # -----------------------------------------------------

    columns = tk.Frame(
        content,
        bg=BACKGROUND
    )

    columns.pack(
        fill="both",
        expand=True,
        padx=32,
        pady=(22, 30)
    )

    columns.grid_columnconfigure(
        0,
        weight=3,
        uniform="dashboard"
    )

    columns.grid_columnconfigure(
        1,
        weight=2,
        uniform="dashboard"
    )

    # -----------------------------------------------------
    # Today's Focus
    # -----------------------------------------------------

    focus = create_section(
        columns,
        "Today's focus",
        "Your most important tasks, prioritised by deadline."
    )

    focus.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 8)
    )

    def focus_sort_key(task):

        deadline = parse_deadline(task[4])

        if deadline is None:
            deadline_group = 5
        else:
            days_left = (deadline - today).days

            if days_left < 0:
                deadline_group = 0
            elif days_left == 0:
                deadline_group = 1
            elif days_left == 1:
                deadline_group = 2
            elif days_left <= 3:
                deadline_group = 3
            else:
                deadline_group = 4

        priority = task[6] if task[6] is not None else 0

        return deadline_group, -priority

    pending_list.sort(
        key=focus_sort_key
    )

    if pending_list:

        for task in pending_list[:3]:

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

            item = tk.Frame(
                focus,
                bg=SURFACE
            )

            item.pack(
                fill="x",
                padx=20,
                pady=(4, 12)
            )

            tk.Frame(
                item,
                bg=BORDER,
                height=1
            ).pack(
                fill="x",
                pady=(0, 12)
            )

            title_row = tk.Frame(
                item,
                bg=SURFACE
            )

            title_row.pack(fill="x")

            tk.Label(
                title_row,
                text=title,
                font=("Arial", 11, "bold"),
                bg=SURFACE,
                fg=TEXT,
                wraplength=330,
                justify="left"
            ).pack(
                side="left",
                fill="x",
                expand=True,
                anchor="w"
            )

            tk.Label(
                title_row,
                text=get_priority_label(priority),
                font=("Arial", 9, "bold"),
                bg=SUBJECT_YELLOW,
                fg=TEXT
            ).pack(
                side="right",
                padx=(8, 0)
            )

            deadline_date = parse_deadline(deadline)

            if deadline_date is None:
                deadline_label = f"Due: {deadline or 'No deadline'}"
            else:
                days_left = (deadline_date - today).days

                if days_left < 0:
                    deadline_label = f"Overdue by {abs(days_left)} day(s)"
                elif days_left == 0:
                    deadline_label = "Due today"
                elif days_left == 1:
                    deadline_label = "Due tomorrow"
                else:
                    deadline_label = deadline_date.strftime("%d %b %Y")

            tk.Label(
                item,
                text=f"{subject}  ·  {deadline_label}  ·  {hours} hour(s)",
                font=("Arial", 9),
                bg=SURFACE,
                fg=MUTED,
                wraplength=360,
                justify="left"
            ).pack(
                anchor="w",
                pady=(7, 10)
            )

            tk.Button(
                item,
                text="Start studying  →",
                command=lambda task_id=task_id: app.study_session(task_id),
                font=("Arial", 9, "bold"),
                bg=ACTIVE,
                fg=PRIMARY,
                activebackground=HOVER,
                activeforeground=PRIMARY,
                relief="flat",
                bd=0,
                padx=12,
                pady=7,
                cursor="hand2"
            ).pack(anchor="w")

    else:

        empty = tk.Frame(
            focus,
            bg=SURFACE
        )

        empty.pack(
            fill="x",
            padx=20,
            pady=20
        )

        tk.Label(
            empty,
            text="You're all caught up!",
            font=("Arial", 13, "bold"),
            bg=SURFACE,
            fg=PRIMARY
        ).pack(anchor="w")

        tk.Label(
            empty,
            text="Add a task whenever you're ready for your next goal.",
            font=("Arial", 10),
            bg=SURFACE,
            fg=MUTED,
            wraplength=300,
            justify="left"
        ).pack(
            anchor="w",
            pady=(7, 12)
        )

        tk.Button(
            empty,
            text="+ Add a task",
            command=app.add_task,
            font=("Arial", 10, "bold"),
            bg=ACTIVE,
            fg=PRIMARY,
            relief="flat",
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2"
        ).pack(anchor="w")

    # -----------------------------------------------------
    # Upcoming Tasks
    # -----------------------------------------------------

    upcoming = create_section(
        columns,
        "Upcoming tasks",
        "A quick look at what's on your plate."
    )

    upcoming.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(8, 0)
    )

    # Show incomplete tasks with the nearest deadlines first.
    # Tasks without valid deadlines appear after dated tasks.

    upcoming_tasks = sorted(
        pending_list,
        key=focus_sort_key
    )

    if upcoming_tasks:

        for task in upcoming_tasks[:5]:

            title = task[1]
            subject = task[2]
            deadline = task[4]

            item = tk.Frame(
                upcoming,
                bg=SURFACE
            )

            item.pack(
                fill="x",
                padx=20,
                pady=(2, 10)
            )

            row = tk.Frame(
                item,
                bg=SURFACE
            )

            row.pack(fill="x")

            tk.Label(
                row,
                text="○",
                font=("Arial", 15),
                bg=SURFACE,
                fg=PRIMARY
            ).pack(
                side="left",
                padx=(0, 10)
            )

            details = tk.Frame(
                row,
                bg=SURFACE
            )

            details.pack(
                side="left",
                fill="x",
                expand=True
            )

            tk.Label(
                details,
                text=title,
                font=("Arial", 10, "bold"),
                bg=SURFACE,
                fg=TEXT,
                wraplength=220,
                justify="left"
            ).pack(anchor="w")

            tk.Label(
                details,
                text=f"{subject}  ·  {deadline or 'No deadline'}",
                font=("Arial", 9),
                bg=SURFACE,
                fg=MUTED,
                wraplength=220,
                justify="left"
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

            tk.Frame(
                item,
                bg=BORDER,
                height=1
            ).pack(
                fill="x",
                pady=(10, 0)
            )

        tk.Button(
            upcoming,
            text="View all tasks  →",
            command=app.view_tasks,
            font=("Arial", 10, "bold"),
            bg=SURFACE,
            fg=PRIMARY,
            activebackground=ACTIVE,
            activeforeground=PRIMARY,
            relief="flat",
            bd=0,
            cursor="hand2"
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 18)
        )

    else:

        tk.Label(
            upcoming,
            text="No pending tasks yet.",
            font=("Arial", 11),
            bg=SURFACE,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 20)
        )

    # -----------------------------------------------------
    # Mouse Wheel Scrolling
    # -----------------------------------------------------

    def on_mousewheel(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind(
        "<MouseWheel>",
        on_mousewheel
    )

    return frame
