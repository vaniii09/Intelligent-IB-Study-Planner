import tkinter as tk
from tkinter import messagebox

from database.database import get_task
from logic import get_priority_label


def show_study_page(parent, task_id):

    frame = tk.Frame(
        parent,
        bg="white"
    )

    # =====================================
    # Load Task
    # =====================================

    task = get_task(task_id)

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

    # =====================================
    # Title
    # =====================================

    tk.Label(
        frame,
        text="🍅 Study Session",
        font=("Arial", 24, "bold"),
        bg="white"
    ).pack(pady=(20,5))

    tk.Label(
        frame,
        text="Focus on one task at a time.",
        font=("Arial",11),
        fg="gray",
        bg="white"
    ).pack(pady=(0,20))

    # =====================================
    # Task Card
    # =====================================

    task_card = tk.LabelFrame(
        frame,
        text="Today's Task",
        bg="white",
        padx=20,
        pady=15,
        font=("Arial",12,"bold")
    )

    task_card.pack(
        fill="x",
        padx=20,
        pady=10
    )

    info = [

        ("📚 Subject", subject),

        ("📝 Task", title),

        ("📂 Type", task_type),

        ("📅 Deadline", deadline),

        ("⏱ Estimated Hours", f"{hours} hour(s)"),

        ("⭐ Priority", get_priority_label(priority))

    ]

    for label, value in info:

        tk.Label(
            task_card,
            text=label,
            font=("Arial",11,"bold"),
            bg="white",
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            task_card,
            text=value,
            font=("Arial",12),
            bg="white",
            anchor="w"
        ).pack(
            fill="x",
            padx=20,
            pady=(0,10)
        )

    # =====================================
    # Timer
    # =====================================

    timer = tk.Label(
        frame,
        text="25:00",
        font=("Consolas",46,"bold"),
        bg="white"
    )

    timer.pack(pady=25)

    # =====================================
    # Progress
    # =====================================

    study_minutes = 25
    break_minutes = 5

    current_session = 1
    total_sessions = max(1, round((hours * 60) / study_minutes))

    progress = tk.LabelFrame(
        frame,
        text="Progress",
        bg="white",
        padx=20,
        pady=20,
        font=("Arial",12,"bold")
    )

    progress.pack(
        fill="x",
        padx=20,
        pady=15
    )

    session_label = tk.Label(
        progress,
        text=f"🍅 Session {current_session} of {total_sessions}",
        font=("Arial",12,"bold"),
        bg="white"
    )
    session_label.pack()

    # =====================================
    # Timer Variables
    # =====================================

    time_left = study_minutes * 60

    running = False
    timer_id = None
    on_break = False
   

     # =====================================
    # Timer Functions
    # =====================================

    def update_timer():

        nonlocal time_left
        nonlocal running
        nonlocal timer_id
        nonlocal on_break
        nonlocal current_session

        minutes = time_left // 60
        seconds = time_left % 60

        timer.config(
            text=f"{minutes:02}:{seconds:02}"
        )

        if not running:
            return

        if time_left > 0:

            time_left -= 1

            timer_id = frame.after(
                1000,
                update_timer
            )

        else:

            running = False

            if not on_break:

                messagebox.showinfo(
                    "Pomodoro",
                    "Study session finished!\nTime for a break."
                )

                on_break = True
                time_left = break_minutes * 60

                start_timer()

            else:

                messagebox.showinfo(
                    "Pomodoro",
                    "Break finished!\nBack to studying!"
                )

                on_break = False

                current_session += 1

                if current_session > total_sessions:

                    timer.config(text="✔ Finished")

                    messagebox.showinfo(
                        "Study Complete",
                        f"You completed all {total_sessions} Pomodoro sessions!"
                    )

                    return

                session_label.config(
                    text=f"🍅 Session {current_session} of {total_sessions}"
                )

                time_left = study_minutes * 60

                start_timer()


    def start_timer():

        nonlocal running

        if not running:

            running = True

            update_timer()


    def pause_timer():

        nonlocal running

        running = False


    def reset_timer():

        nonlocal running
        nonlocal time_left
        nonlocal on_break

        running = False

        on_break = False

        time_left = study_minutes * 60

        timer.config(
            text=f"{study_minutes:02}:00"
        )
    # =====================================
    # Buttons
    # =====================================

    buttons = tk.Frame(
        frame,
        bg="white"
    )

    buttons.pack(
        pady=20
    )

    tk.Button(
        buttons,
        text="▶ Start",
        command=start_timer,
        width=12,
        bg="#2E7D32",
        fg="white",
        font=("Arial", 10, "bold")
    ).grid(row=0, column=0, padx=8)

    tk.Button(
        buttons,
        text="⏸ Pause",
        command=pause_timer,
        width=12,
        bg="#F9A825",
        fg="white",
        font=("Arial", 10, "bold")
    ).grid(row=0, column=1, padx=8)

    tk.Button(
        buttons,
        text="🔄 Reset",
        command=reset_timer,
        width=12,
        bg="#1976D2",
        fg="white",
        font=("Arial", 10, "bold")
    ).grid(row=0, column=2, padx=8)

    tk.Button(
        buttons,
        text="⏭ Skip",
        width=12,
        bg="#757575",
        fg="white",
        font=("Arial", 10, "bold")
    ).grid(row=0, column=3, padx=8)

    return frame