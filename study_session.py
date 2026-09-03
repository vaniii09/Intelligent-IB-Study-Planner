import tkinter as tk

from database.database import get_task
from logic import get_priority_label
from pomodoro import PomodoroTimer


def open_study_session(parent, task_id):

    task = get_task(task_id)

    if task is None:
        return None

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

    # =====================================================
    # MAIN PAGE
    # =====================================================

    page = tk.Frame(
        parent,
        bg="white"
    )

    # =====================================================
    # TITLE
    # =====================================================

    tk.Label(
        page,
        text="🎯 Today's Study Session",
        font=("Arial", 24, "bold"),
        bg="white",
        fg="#263238"
    ).pack(pady=(30, 8))

    tk.Label(
        page,
        text="Focus on one task at a time using Pomodoro sessions.",
        font=("Arial", 11),
        bg="white",
        fg="#607D8B"
    ).pack(pady=(0, 20))

    # =====================================================
    # TASK INFORMATION
    # =====================================================

    info_frame = tk.Frame(
        page,
        bg="#F5F7FA",
        bd=1,
        relief="solid",
        padx=25,
        pady=20
    )

    info_frame.pack(
        fill="x",
        padx=80,
        pady=10
    )

    tk.Label(
        info_frame,
        text=title,
        font=("Arial", 18, "bold"),
        bg="#F5F7FA",
        fg="#263238"
    ).pack(
        anchor="w",
        pady=(0, 15)
    )

    info = [
        ("📚 Subject", subject),
        ("📂 Type", task_type),
        ("📅 Deadline", deadline),
        ("⏱ Estimated Hours", f"{hours} hour(s)"),
        ("⭐ Priority", get_priority_label(priority))
    ]

    for label, value in info:

        row = tk.Frame(
            info_frame,
            bg="#F5F7FA"
        )

        row.pack(
            fill="x",
            pady=3
        )

        tk.Label(
            row,
            text=label,
            font=("Arial", 10, "bold"),
            bg="#F5F7FA",
            fg="#607D8B",
            width=20,
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=value,
            font=("Arial", 10),
            bg="#F5F7FA",
            fg="#263238",
            anchor="w"
        ).pack(
            side="left"
        )

    # =====================================================
    # POMODORO SETTINGS
    # =====================================================

    tk.Label(
        page,
        text="🍅 Pomodoro Settings",
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#263238"
    ).pack(
        pady=(20, 10)
    )

    settings_frame = tk.Frame(
        page,
        bg="white"
    )

    settings_frame.pack()

    # =====================================================
    # STUDY TIME
    # =====================================================

    row1 = tk.Frame(
        settings_frame,
        bg="white"
    )

    row1.pack(pady=6)

    tk.Label(
        row1,
        text="Study (minutes)",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#263238"
    ).pack(side="left")

    study_spin = tk.Spinbox(
        row1,
        from_=1,
        to=90,
        width=6
    )

    study_spin.delete(0, "end")
    study_spin.insert(0, 25)

    study_spin.pack(
        side="left",
        padx=15
    )
    def update_recommended_sessions(*args):

        try:

            study_minutes = int(
                study_spin.get()
            )

            recommended = max(
                1,
                round((hours * 60) / study_minutes)
            )

            session_spin.delete(
                0,
                "end"
            )

            session_spin.insert(
                0,
                recommended
            )

            recommendation_label.config(
                text=f"💡 Recommended: {recommended} session(s)"
            )

        except ValueError:
            pass
        # =====================================================
    # BREAK TIME
    # =====================================================

    row2 = tk.Frame(
        settings_frame,
        bg="white"
    )

    row2.pack(pady=6)

    tk.Label(
        row2,
        text="Break (minutes)",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#263238"
    ).pack(side="left")

    break_spin = tk.Spinbox(
        row2,
        from_=1,
        to=30,
        width=6
    )

    break_spin.delete(0, "end")
    break_spin.insert(0, 5)

    break_spin.pack(
        side="left",
        padx=15
    )

    # =====================================================
    # NUMBER OF POMODOROS
    # =====================================================

    recommended = max(
        1,
        round((hours * 60) / int(study_spin.get()))
    )

    row3 = tk.Frame(
        settings_frame,
        bg="white"
    )

    row3.pack(pady=6)

    tk.Label(
        row3,
        text="Pomodoros",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#263238"
    ).pack(side="left")

    session_spin = tk.Spinbox(
        row3,
        from_=1,
        to=50,
        width=6
    )

    session_spin.delete(0, "end")
    session_spin.insert(0, recommended)

    session_spin.pack(
        side="left",
        padx=15
    )

    # =====================================================
    # RECOMMENDATION LABEL
    # =====================================================

    recommendation_label = tk.Label(
        page,
        text=f"💡 Recommended: {recommended} Pomodoro session(s)",
        font=("Arial", 10),
        bg="white",
        fg="#607D8B"
    )

    recommendation_label.pack(
        pady=10
    )

    # =====================================================
    # UPDATE RECOMMENDATION
    # =====================================================

    def update_recommendation(event=None):

        try:

            study_minutes = int(
                study_spin.get()
            )

            if study_minutes <= 0:
                return

            recommended = max(
                1,
                round(
                    (hours * 60) / study_minutes
                )
            )

            recommendation_label.config(
                text=f"💡 Recommended: {recommended} Pomodoro session(s)"
            )

            # Also update the Pomodoro count
            # automatically when the user changes
            # study duration.

            session_spin.delete(
                0,
                "end"
            )

            session_spin.insert(
                0,
                recommended
            )

        except ValueError:
            pass

    study_spin.bind(
        "<KeyRelease>",
        update_recommendation
    )

    study_spin.bind(
        "<<Increment>>",
        update_recommendation
    )

    # =====================================================
    # START TIMER
    # =====================================================

    def start_timer():

        try:

            study_minutes = int(
                study_spin.get()
            )

            break_minutes = int(
                break_spin.get()
            )

            sessions = int(
                session_spin.get()
            )

            if study_minutes <= 0:
                return

            if break_minutes <= 0:
                return

            if sessions <= 0:
                return

        except ValueError:

            return

        PomodoroTimer(
            page,
            study_minutes,
            break_minutes,
            sessions,
            task_id
        )

    tk.Button(
        page,
        text="▶ Start Timer",
        bg="#2E7D32",
        fg="white",
        font=("Arial", 11, "bold"),
        width=18,
        height=2,
        relief="flat",
        cursor="hand2",
        command=start_timer
    ).pack(
        pady=15
    )

    return page