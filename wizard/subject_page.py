import tkinter as tk
from tkinter import ttk

from subjects_data import IB_SUBJECTS


def create_subject_page(parent, wizard, group_name,
                        step_number,
                        total_steps,
                        next_command,
                        back_command):

    frame = tk.Frame(parent, bg="white")

    # -----------------------------
    # Progress
    # -----------------------------

    progress = tk.Label(
        frame,
        text=f"Step {step_number} of {total_steps}",
        font=("Arial", 11),
        fg="grey",
        bg="white"
    )

    progress.pack(pady=(10, 0))

    progress_bar = ttk.Progressbar(
        frame,
        length=400,
        mode="determinate"
    )

    progress_bar["maximum"] = total_steps
    progress_bar["value"] = step_number

    progress_bar.pack(pady=(5, 20))

    # -----------------------------
    # Heading
    # -----------------------------

    heading = tk.Label(
        frame,
        text=group_name,
        font=("Arial", 20, "bold"),
        bg="white"
    )

    heading.pack(pady=10)

    # -----------------------------
    # Instructions
    # -----------------------------

    info = tk.Label(
        frame,
        text="Select every subject you are studying in this group.",
        bg="white",
        font=("Arial", 11)
    )

    info.pack(pady=(0, 20))

    # -----------------------------
    # Subject Counter
    # -----------------------------

    current_total = sum(
        1
        for data in wizard.subject_variables.values()
        if data["selected"].get()
    )

    counter = tk.Label(
        frame,
        text=f"Selected Subjects: {current_total} / 6",
        font=("Arial", 11, "bold"),
        bg="white"
    )

    counter.pack(pady=(0, 15))

    # -----------------------------
    # Update Counter
    # -----------------------------

    def update_counter():

        total = sum(
            1
            for data in wizard.subject_variables.values()
            if data["selected"].get()
        )

        counter.config(
            text=f"Selected Subjects: {total} / 6"
        )

    # -----------------------------
    # Subject Rows
    # -----------------------------

    for subject in IB_SUBJECTS[group_name]:

        data = wizard.subject_variables[subject]

        selected = data["selected"]
        level = data["level"]

        row = tk.Frame(frame, bg="white")
        row.pack(fill="x", padx=80, pady=4)

        level_box = ttk.Combobox(
            row,
            values=["HL", "SL"],
            textvariable=level,
            width=5,
            state="readonly" if selected.get() else "disabled"
        )

        def toggle(var=selected, box=level_box):

            if var.get():
                box.configure(state="readonly")
            else:
                box.configure(state="disabled")

            update_counter()

        check = tk.Checkbutton(
            row,
            text=subject,
            variable=selected,
            command=toggle,
            bg="white",
            font=("Arial", 11)
        )

        check.pack(side="left")

        level_box.pack(side="right")

    # -----------------------------
    # Buttons
    # -----------------------------

    button_frame = tk.Frame(frame, bg="white")
    button_frame.pack(pady=20)

    back_button = tk.Button(
        button_frame,
        text="← Back",
        width=15,
        command=back_command
    )

    back_button.pack(side="left", padx=10)

    next_button = tk.Button(
        button_frame,
        text="Next →",
        width=15,
        command=next_command
    )

    next_button.pack(side="left", padx=10)

    return frame