import tkinter as tk
from tkinter import ttk

from scrollable_frame import ScrollableFrame

from database.database import (
    load_tasks,
    search_tasks,
    delete_task,
    mark_task_complete
)

from edit_task import show_edit_task

from logic import (
    get_deadline_status,
    get_priority_label
)

from theme import *


def show_view_tasks(parent, app):

    # =====================================
    # Main Container
    # =====================================

    container = ScrollableFrame(parent)
    frame = container.scrollable_frame

    # =====================================
    # Title
    # =====================================

    tk.Label(
        frame,
        text="View Tasks",
        font=TITLE_FONT,
        bg=BACKGROUND,
        fg=TEXT
    ).pack(pady=(20, 8))

    tk.Label(
        frame,
        text="Search, organise and manage all your study tasks.",
        font=SUBTITLE_FONT,
        bg=BACKGROUND,
        fg=SUBTEXT
    ).pack(pady=(0, 20))

    # =====================================
    # Filter Bar
    # =====================================

    filter_frame = tk.Frame(
        frame,
        bg=BACKGROUND
    )

    filter_frame.pack(
        fill="x",
        padx=20,
        pady=(0,20)
    )

    # -------------------------
    # Search
    # -------------------------

    tk.Label(
        filter_frame,
        text="Search",
        bg=BACKGROUND,
        font=LABEL_FONT
    ).grid(row=0,column=0,padx=5)

    search_entry = tk.Entry(
        filter_frame,
        width=24
    )

    search_entry.grid(
        row=0,
        column=1,
        padx=5
    )

    # -------------------------
    # Subject Filter
    # -------------------------

    subjects = sorted(
        list(
            set(
                task[2]
                for task in load_tasks()
            )
        )
    )

    subject_filter = ttk.Combobox(
        filter_frame,
        values=["All"] + subjects,
        width=16,
        state="readonly"
    )

    subject_filter.set("All")

    subject_filter.grid(
        row=0,
        column=2,
        padx=8
    )

    # -------------------------
    # Status Filter
    # -------------------------

    status_filter = ttk.Combobox(
        filter_frame,
        values=[
            "All",
            "Pending",
            "Completed",
            "Archived"
        ],
        width=12,
        state="readonly"
    )

    status_filter.set("All")

    status_filter.grid(
        row=0,
        column=3,
        padx=8
    )

    # -------------------------
    # Sort Filter
    # -------------------------

    sort_filter = ttk.Combobox(
        filter_frame,
        values=[
            "Priority",
            "Deadline",
            "Title",
            "Subject"
        ],
        width=12,
        state="readonly"
    )

    sort_filter.set("Priority")

    sort_filter.grid(
        row=0,
        column=4,
        padx=8
    )

    # =====================================
    # Task Area
    # =====================================

    task_container = tk.Frame(
        frame,
        bg=BACKGROUND
    )

    task_container.pack(
        fill="both",
        expand=True
    )
    # =====================================
    # Load Task Cards
    # =====================================

    def load_cards():

        # Clear previous cards

        for widget in task_container.winfo_children():
            widget.destroy()

        # Get filtered tasks

        tasks = search_tasks(

            search=search_entry.get(),

            subject=subject_filter.get(),

            status=status_filter.get(),

            sort=sort_filter.get()

        )

        # No tasks

        if len(tasks) == 0:

            tk.Label(

                task_container,

                text="📋 No tasks found.",

                font=TEXT_FONT,

                bg=BACKGROUND,

                fg=SUBTEXT

            ).pack(pady=70)

            return

        # =====================================
        # Create Cards
        # =====================================

        for task in tasks:

            (
                task_id,
                title,
                subject,
                task_type,
                deadline,
                hours,
                priority,
                completed,
                completed_date,
                archived
            ) = task

            status = get_deadline_status(
                deadline,
                completed
            )

            priority_label = get_priority_label(
                priority
            )

            # ------------------------
            # Card Colour
            # ------------------------

            if status == "overdue":
                card_colour = "#FFEBEE"

            elif status == "today":
                card_colour = "#FFEBEE"

            elif status == "tomorrow":
                card_colour = "#FFF3E0"

            elif status == "soon":
                card_colour = "#FFFDE7"

            elif status == "completed":
                card_colour = "#E8F5E9"

            else:
                card_colour = CARD

            # ------------------------
            # Alert
            # ------------------------

            alert_text = None
            alert_colour = TEXT

            if status == "overdue":
                alert_text = "🔥 OVERDUE"
                alert_colour = "#D32F2F"

            elif status == "today":
                alert_text = "🚨 DUE TODAY"
                alert_colour = "#C62828"

            elif status == "tomorrow":
                alert_text = "⚠ DUE TOMORROW"
                alert_colour = "#EF6C00"

            elif status == "soon":
                alert_text = "📅 Due Within 3 Days"
                alert_colour = "#F9A825"

            elif status == "completed":
                alert_text = "✅ COMPLETED"
                alert_colour = "#2E7D32"

            # ------------------------
            # Card
            # ------------------------

            card = tk.Frame(

                task_container,

                bg=card_colour,

                bd=1,

                relief="solid",

                padx=25,

                pady=20

            )

            card.pack(

                fill="x",

                padx=60,

                pady=12

            )

            tk.Label(

                card,

                text=title,

                font=("Arial",17,"bold"),

                bg=card_colour,

                fg=TEXT

            ).pack(anchor="w")

            if alert_text:

                tk.Label(

                    card,

                    text=alert_text,

                    font=("Arial",10,"bold"),

                    bg=card_colour,

                    fg=alert_colour

                ).pack(anchor="w", pady=(4,8))
                           # ------------------------
            # Priority Badge
            # ------------------------

            badge_text = {
                "Urgent": "🔥 URGENT",
                "Critical": "🔴 CRITICAL",
                "High": "🟠 HIGH",
                "Medium": "🟡 MEDIUM",
                "Low": "🟢 LOW"
            }[priority_label]

            if priority_label == "Urgent":
                badge_colour = "#8B0000"
            elif priority_label == "Critical":
                badge_colour = "#D32F2F"
            elif priority_label == "High":
                badge_colour = "#F57C00"
            elif priority_label == "Medium":
                badge_colour = "#FBC02D"
            else:
                badge_colour = "#43A047"

            tk.Label(
                card,
                text=badge_text,
                bg=badge_colour,
                fg="white",
                padx=12,
                pady=4,
                font=("Arial", 9, "bold")
            ).pack(anchor="w", pady=(0,12))

            # ------------------------
            # Details
            # ------------------------

            details = [

                f"📚 Subject: {subject}",

                f"📝 Type: {task_type}",

                f"📅 Deadline: {deadline}",

                f"⏱ Estimated Study Time: {hours} hour(s)",

                f"Status: {'Completed' if completed else 'Pending'}"

            ]

            for line in details:

                tk.Label(
                    card,
                    text=line,
                    bg=card_colour,
                    fg=TEXT,
                    font=TEXT_FONT
                ).pack(anchor="w", pady=2)

            # ------------------------
            # Buttons
            # ------------------------

            button_frame = tk.Frame(
                card,
                bg=card_colour
            )

            button_frame.pack(
                anchor="w",
                pady=(18,0)
            )

            tk.Button(
                button_frame,
                text="▶ Start",
                width=10,
                bg=PRIMARY,
                fg="white",
                command=lambda id=task_id: app.study_session(id)
            ).pack(side="left", padx=4)

            tk.Button(
                button_frame,
                text="✏ Edit",
                width=10,
                bg=PRIMARY,
                fg="white",
                command=lambda id=task_id: show_edit_task(
                    parent,
                    id,
                    load_cards
                )
            ).pack(side="left", padx=4)

            tk.Button(
                button_frame,
                text="🗑 Delete",
                width=10,
                bg=DANGER,
                fg="white",
                command=lambda id=task_id: (
                    delete_task(id),
                    load_cards()
                )
            ).pack(side="left", padx=4)

            complete_button = tk.Button(
                button_frame,
                text="✓ Complete",
                width=10,
                bg=SUCCESS,
                fg="white",
                command=lambda id=task_id: (
                    mark_task_complete(id),
                    load_cards()
                )
            )

            complete_button.pack(side="left", padx=4)

            if completed:
                complete_button.config(state="disabled")

    # =====================================
    # Events
    # =====================================

    search_entry.bind(
        "<KeyRelease>",
        lambda e: load_cards()
    )

    subject_filter.bind(
        "<<ComboboxSelected>>",
        lambda e: load_cards()
    )

    status_filter.bind(
        "<<ComboboxSelected>>",
        lambda e: load_cards()
    )

    sort_filter.bind(
        "<<ComboboxSelected>>",
        lambda e: load_cards()
    )

    # Initial Load

    load_cards()

    return container 