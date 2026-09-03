import tkinter as tk
from tkinter import ttk


def create_availability_page(
    parent,
    wizard,
    step_number,
    total_steps,
    finish_command,
    back_command
):

    frame = tk.Frame(parent, bg="white")

    # -------------------------
    # Progress
    # -------------------------

    progress = tk.Label(
        frame,
        text=f"Step {step_number} of {total_steps}",
        bg="white",
        fg="grey",
        font=("Arial",11)
    )

    progress.pack(pady=(15,5))

    progressbar = ttk.Progressbar(
        frame,
        length=400,
        mode="determinate"
    )

    progressbar["maximum"] = total_steps
    progressbar["value"] = step_number

    progressbar.pack(pady=(0,20))

    # -------------------------
    # Heading
    # -------------------------

    heading = tk.Label(
        frame,
        text="Weekly Availability",
        bg="white",
        font=("Arial",20,"bold")
    )

    heading.pack(pady=10)

    info = tk.Label(
        frame,
        text="Enter the number of hours you are available to study each day.",
        bg="white",
        font=("Arial",11)
    )

    info.pack(pady=(0,25))

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    for day in days:

        row = tk.Frame(frame, bg="white")
        row.pack(pady=6)

        label = tk.Label(
            row,
            text=day,
            width=15,
            anchor="w",
            bg="white",
            font=("Arial",11)
        )

        label.pack(side="left")

        if day not in wizard.available_hours:

            wizard.available_hours[day] = tk.StringVar(value="2")

        entry = ttk.Spinbox(
            row,
            from_=0,
            to=12,
            width=5,
            textvariable=wizard.available_hours[day]
        )

        entry.pack(side="right")

    # -------------------------
    # Buttons
    # -------------------------

    button_frame = tk.Frame(frame,bg="white")
    button_frame.pack(pady=20)

    back_button = tk.Button(
        button_frame,
        text="← Back",
        width=15,
        command=back_command
    )

    back_button.pack(side="left", padx=10)

    finish_button = tk.Button(
        button_frame,
        text="Finish",
        width=15,
        command=finish_command
    )

    finish_button.pack(side="left", padx=10)

    return frame