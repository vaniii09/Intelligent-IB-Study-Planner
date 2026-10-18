
import tkinter as tk
from tkinter import ttk, messagebox

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


# =========================================================
# StudySpace — Task Manager
# =========================================================

def show_view_tasks(parent, app):

    # -----------------------------------------------------
    # Main Container
    # -----------------------------------------------------

    container = tk.Frame(
        parent,
        bg=BACKGROUND
    )

    # Scrollable content
    scroll_container = ScrollableFrame(container)
    scroll_container.pack(
        fill="both",
        expand=True
    )

    frame = scroll_container.scrollable_frame
    frame.configure(bg=BACKGROUND)

    # -----------------------------------------------------
    # Configure Scrollable Canvas
    # -----------------------------------------------------

    if hasattr(scroll_container, "canvas"):
        scroll_container.canvas.configure(
            bg=BACKGROUND,
            highlightthickness=0
        )

    # -----------------------------------------------------
    # Header
    # -----------------------------------------------------

    header = tk.Frame(
        frame,
        bg=BACKGROUND
    )

    header.pack(
        fill="x",
        padx=32,
        pady=(30, 24)
    )

    tk.Label(
        header,
        text="YOUR WORKSPACE",
        font=("Arial", 9, "bold"),
        bg=BACKGROUND,
        fg=PRIMARY
    ).pack(anchor="w")

    tk.Label(
        header,
        text="My Tasks",
        font=("Arial", 28, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    ).pack(
        anchor="w",
        pady=(5, 5)
    )

    tk.Label(
        header,
        text="Everything you need to study, organised in one place.",
        font=("Arial", 11),
        bg=BACKGROUND,
        fg=MUTED
    ).pack(anchor="w")

    # -----------------------------------------------------
    # Summary Statistics
    # -----------------------------------------------------

    summary = tk.Frame(
        frame,
        bg=BACKGROUND
    )

    summary.pack(
        fill="x",
        padx=32,
        pady=(0, 22)
    )

    summary.grid_columnconfigure(
        (0, 1, 2),
        weight=1,
        uniform="summary"
    )

    def make_summary_card(parent, title, value, accent):

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
            pady=12
        )

        tk.Label(
            body,
            text=title,
            font=("Arial", 10),
            bg=SURFACE,
            fg=MUTED
        ).pack(anchor="w")

        value_label = tk.Label(
            body,
            text=str(value),
            font=("Arial", 22, "bold"),
            bg=SURFACE,
            fg=TEXT
        )

        value_label.pack(
            anchor="w",
            pady=(5, 0)
        )

        return card, value_label

    all_tasks = load_tasks()

    total_count = len([
        task for task in all_tasks
        if len(task) < 10 or not task[9]
    ])

    pending_count = len([
        task for task in all_tasks
        if task[7] == 0 and (len(task) < 10 or not task[9])
    ])

    completed_count = len([
        task for task in all_tasks
        if task[7] == 1 and (len(task) < 10 or not task[9])
    ])

    summary_cards = []

    for column, data in enumerate([
        ("Active tasks", total_count, PRIMARY),
        ("To complete", pending_count, "#C69A51"),
        ("Completed", completed_count, "#739B79")
    ]):

        title, value, accent = data

        card, value_label = make_summary_card(
            summary,
            title,
            value,
            accent
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=(0 if column == 0 else 7, 7 if column < 2 else 0)
        )

        summary_cards.append(value_label)

    # -----------------------------------------------------
    # Filter Panel
    # -----------------------------------------------------

    filter_panel = tk.Frame(
        frame,
        bg=SURFACE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    filter_panel.pack(
        fill="x",
        padx=32,
        pady=(0, 22)
    )

    tk.Label(
        filter_panel,
        text="Find and organise",
        font=("Arial", 13, "bold"),
        bg=SURFACE,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=18,
        pady=(16, 12)
    )

    filters = tk.Frame(
        filter_panel,
        bg=SURFACE
    )

    filters.pack(
        fill="x",
        padx=18,
        pady=(0, 18)
    )

    filters.grid_columnconfigure(
        0,
        weight=3
    )

    filters.grid_columnconfigure(
        1,
        weight=2
    )

    filters.grid_columnconfigure(
        2,
        weight=2
    )

    filters.grid_columnconfigure(
        3,
        weight=2
    )

    # Search
    search_frame = tk.Frame(
        filters,
        bg=SURFACE
    )

    search_frame.grid(
        row=0,
        column=0,
        sticky="ew",
        padx=(0, 8)
    )

    tk.Label(
        search_frame,
        text="Search tasks",
        font=("Arial", 9, "bold"),
        bg=SURFACE,
        fg=MUTED
    ).pack(anchor="w", pady=(0, 6))

    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 10),
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=PRIMARY
    )

    search_entry.pack(
        fill="x",
        ipady=7
    )

    # Subject filter
    subject_frame = tk.Frame(
        filters,
        bg=SURFACE
    )

    subject_frame.grid(
        row=0,
        column=1,
        sticky="ew",
        padx=8
    )

    tk.Label(
        subject_frame,
        text="Subject",
        font=("Arial", 9, "bold"),
        bg=SURFACE,
        fg=MUTED
    ).pack(anchor="w", pady=(0, 6))

    subjects = sorted(set(
        task[2]
        for task in all_tasks
        if len(task) > 2 and task[2]
    ))

    subject_filter = ttk.Combobox(
        subject_frame,
        values=["All"] + subjects,
        state="readonly",
        font=("Arial", 10)
    )

    subject_filter.set("All")

    subject_filter.pack(
        fill="x",
        ipady=4
    )

    # Status filter
    status_frame = tk.Frame(
        filters,
        bg=SURFACE
    )

    status_frame.grid(
        row=0,
        column=2,
        sticky="ew",
        padx=8
    )

    tk.Label(
        status_frame,
        text="Status",
        font=("Arial", 9, "bold"),
        bg=SURFACE,
        fg=MUTED
    ).pack(anchor="w", pady=(0, 6))

    status_filter = ttk.Combobox(
        status_frame,
        values=[
            "All",
            "Pending",
            "Completed",
            "Archived"
        ],
        state="readonly",
        font=("Arial", 10)
    )

    status_filter.set("All")

    status_filter.pack(
        fill="x",
        ipady=4
    )

    # Sort filter
    sort_frame = tk.Frame(
        filters,
        bg=SURFACE
    )

    sort_frame.grid(
        row=0,
        column=3,
        sticky="ew",
        padx=(8, 0)
    )

    tk.Label(
        sort_frame,
        text="Sort by",
        font=("Arial", 9, "bold"),
        bg=SURFACE,
        fg=MUTED
    ).pack(anchor="w", pady=(0, 6))

    sort_filter = ttk.Combobox(
        sort_frame,
        values=[
            "Priority",
            "Deadline",
            "Title",
            "Subject"
        ],
        state="readonly",
        font=("Arial", 10)
    )

    sort_filter.set("Priority")

    sort_filter.pack(
        fill="x",
        ipady=4
    )

    # -----------------------------------------------------
    # Results Heading
    # -----------------------------------------------------

    results_header = tk.Frame(
        frame,
        bg=BACKGROUND
    )

    results_header.pack(
        fill="x",
        padx=32,
        pady=(0, 12)
    )

    tk.Label(
        results_header,
        text="Your tasks",
        font=("Arial", 17, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    ).pack(side="left")

    result_count_label = tk.Label(
        results_header,
        text="",
        font=("Arial", 10),
        bg=BACKGROUND,
        fg=MUTED
    )

    result_count_label.pack(side="right")

    # -----------------------------------------------------
    # Task Results
    # -----------------------------------------------------

    task_container = tk.Frame(
        frame,
        bg=BACKGROUND
    )

    task_container.pack(
        fill="both",
        expand=True,
        padx=32,
        pady=(0, 30)
    )

    # -----------------------------------------------------
    # Task Cards
    # -----------------------------------------------------

    def load_cards():

        for widget in task_container.winfo_children():
            widget.destroy()

        tasks = search_tasks(
            search=search_entry.get(),
            subject=subject_filter.get(),
            status=status_filter.get(),
            sort=sort_filter.get()
        )

        result_count_label.configure(
            text=f"{len(tasks)} task(s)"
        )

        # Empty state
        if not tasks:

            empty_card = tk.Frame(
                task_container,
                bg=SURFACE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            empty_card.pack(
                fill="x",
                pady=10
            )

            tk.Label(
                empty_card,
                text="No tasks found",
                font=("Arial", 16, "bold"),
                bg=SURFACE,
                fg=TEXT
            ).pack(pady=(30, 8))

            tk.Label(
                empty_card,
                text="Try changing your filters or create a new task.",
                font=("Arial", 10),
                bg=SURFACE,
                fg=MUTED
            ).pack(pady=(0, 16))

            tk.Button(
                empty_card,
                text="+ Add a task",
                command=app.add_task,
                font=("Arial", 10, "bold"),
                bg=ACTIVE,
                fg=PRIMARY,
                activebackground=HOVER,
                relief="flat",
                bd=0,
                padx=14,
                pady=8,
                cursor="hand2"
            ).pack(pady=(0, 28))

            return

        # Create cards
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

            # ---------------------------------------------
            # Card appearance
            # ---------------------------------------------

            card = tk.Frame(
                task_container,
                bg=SURFACE,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            card.pack(
                fill="x",
                pady=7
            )

            # Left accent
            if completed:
                accent = SUCCESS
            elif status == "overdue":
                accent = DANGER
            elif status in ("today", "tomorrow"):
                accent = WARNING
            else:
                accent = PRIMARY

            tk.Frame(
                card,
                bg=accent,
                width=5
            ).pack(
                side="left",
                fill="y"
            )

            body = tk.Frame(
                card,
                bg=SURFACE
            )

            body.pack(
                side="left",
                fill="both",
                expand=True,
                padx=18,
                pady=16
            )

            # ---------------------------------------------
            # Title and priority
            # ---------------------------------------------

            title_row = tk.Frame(
                body,
                bg=SURFACE
            )

            title_row.pack(
                fill="x"
            )

            tk.Label(
                title_row,
                text=("✓  " if completed else "") + title,
                font=("Arial", 14, "bold"),
                bg=SURFACE,
                fg=MUTED if completed else TEXT,
                wraplength=480,
                justify="left"
            ).pack(
                side="left",
                fill="x",
                expand=True,
                anchor="w"
            )

            priority_colours = {
                "Urgent": ("#F8E3E3", "#A63C3C"),
                "Critical": ("#F8E3E3", "#A63C3C"),
                "High": ("#F8EBDD", "#A65D26"),
                "Medium": ("#F5F0D9", "#8C762D"),
                "Low": ("#E5EEE5", "#4E7855")
            }

            badge_bg, badge_fg = priority_colours.get(
                priority_label,
                (ACTIVE, PRIMARY)
            )

            tk.Label(
                title_row,
                text=priority_label.upper(),
                font=("Arial", 8, "bold"),
                bg=badge_bg,
                fg=badge_fg,
                padx=10,
                pady=5
            ).pack(
                side="right",
                padx=(12, 0)
            )

            # ---------------------------------------------
            # Deadline status
            # ---------------------------------------------

            status_labels = {
                "overdue": ("OVERDUE", "#B84040"),
                "today": ("DUE TODAY", "#B84040"),
                "tomorrow": ("DUE TOMORROW", "#A65D26"),
                "soon": ("DUE SOON", "#8C762D"),
                "completed": ("COMPLETED", "#4E7855")
            }

            if status in status_labels:

                label_text, label_colour = status_labels[status]

                tk.Label(
                    body,
                    text=label_text,
                    font=("Arial", 9, "bold"),
                    bg=SURFACE,
                    fg=label_colour
                ).pack(
                    anchor="w",
                    pady=(7, 0)
                )

            # ---------------------------------------------
            # Subject and task details
            # ---------------------------------------------

            details = tk.Frame(
                body,
                bg=SURFACE
            )

            details.pack(
                fill="x",
                pady=(10, 0)
            )

            details_text = (
                f"{subject}    ·    "
                f"{task_type}    ·    "
                f"{hours} hour(s)"
            )

            tk.Label(
                details,
                text=details_text,
                font=("Arial", 10),
                bg=SURFACE,
                fg=MUTED,
                wraplength=650,
                justify="left"
            ).pack(anchor="w")

            tk.Label(
                details,
                text=f"Deadline: {deadline or 'Not set'}",
                font=("Arial", 9),
                bg=SURFACE,
                fg=MUTED
            ).pack(
                anchor="w",
                pady=(5, 0)
            )

            # ---------------------------------------------
            # Action buttons
            # ---------------------------------------------

            buttons = tk.Frame(
                body,
                bg=SURFACE
            )

            buttons.pack(
                fill="x",
                pady=(14, 0)
            )

            def make_button(
                parent,
                text,
                command,
                bg,
                fg,
                active_bg=None
            ):

                button = tk.Button(
                    parent,
                    text=text,
                    command=command,
                    font=("Arial", 9, "bold"),
                    bg=bg,
                    fg=fg,
                    activebackground=active_bg or bg,
                    activeforeground=fg,
                    relief="flat",
                    bd=0,
                    padx=13,
                    pady=8,
                    cursor="hand2"
                )

                button.pack(
                    side="left",
                    padx=(0, 7)
                )

                return button

            make_button(
                buttons,
                "▶  Start",
                lambda task_id=task_id: app.study_session(task_id),
                PRIMARY,
                WHITE,
                HOVER
            )

            make_button(
                buttons,
                "Edit",
                lambda task_id=task_id: show_edit_task(
                    parent,
                    task_id,
                    load_cards
                ),
                ACTIVE,
                PRIMARY,
                HOVER
            )

            make_button(
                buttons,
                "Delete",
                lambda task_id=task_id: confirm_delete(task_id),
                "#F8E3E3",
                "#A63C3C",
                "#F1D3D3"
            )

            complete_button = make_button(
                buttons,
                "✓  Completed" if completed else "✓  Mark complete",
                lambda task_id=task_id: complete_task(task_id),
                "#E5EEE5",
                "#4E7855",
                "#D6E5D6"
            )

            if completed:
                complete_button.configure(
                    state="disabled"
                )

    # -----------------------------------------------------
    # Actions
    # -----------------------------------------------------

    def confirm_delete(task_id):

        confirmed = messagebox.askyesno(
            "Delete task",
            "Are you sure you want to delete this task?",
            parent=parent
        )

        if confirmed:

            delete_task(task_id)
            refresh_summary()
            load_cards()

    def complete_task(task_id):

        mark_task_complete(task_id)
        refresh_summary()
        load_cards()

    def refresh_summary():

        current_tasks = load_tasks()

        active = [
            task for task in current_tasks
            if len(task) < 10 or not task[9]
        ]

        pending = [
            task for task in active
            if task[7] == 0
        ]

        completed = [
            task for task in active
            if task[7] == 1
        ]

        summary_cards[0].configure(
            text=str(len(active))
        )

        summary_cards[1].configure(
            text=str(len(pending))
        )

        summary_cards[2].configure(
            text=str(len(completed))
        )

    # -----------------------------------------------------
    # Filter Events
    # -----------------------------------------------------

    search_entry.bind(
        "<KeyRelease>",
        lambda event: load_cards()
    )

    subject_filter.bind(
        "<<ComboboxSelected>>",
        lambda event: load_cards()
    )

    status_filter.bind(
        "<<ComboboxSelected>>",
        lambda event: load_cards()
    )

    sort_filter.bind(
        "<<ComboboxSelected>>",
        lambda event: load_cards()
    )

    # -----------------------------------------------------
    # Initial Load
    # -----------------------------------------------------

    load_cards()

    return container
