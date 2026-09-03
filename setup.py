import tkinter as tk
from tkinter import ttk

from subjects_data import IB_SUBJECTS


def show_setup(parent):

    frame = tk.Frame(parent, bg="white")

    title = tk.Label(
        frame,
        text="Welcome to Intelligent IB Study Planner",
        font=("Arial",24,"bold"),
        bg="white"
    )

    title.pack(pady=(20,10))

    subtitle = tk.Label(
        frame,
        text="Please select your IB subjects before continuing.",
        font=("Arial",12),
        bg="white"
    )

    subtitle.pack()
    content = tk.Frame(frame, bg="white")
    content.pack(fill="both", expand=True, pady=20)
    for group_name, subjects in IB_SUBJECTS.items():
        group_label = tk.Label(
            content,
            text=group_name,
            font=("Arial",12,"bold"),
            bg="white"
        )

        group_label.pack(anchor="w", padx=20, pady=(15,5))

        subject_dropdown = ttk.Combobox(
            content,
            values=subjects,
            state="readonly",
            width=40
        )

        subject_dropdown.pack(anchor="w", padx=20)

        level = tk.StringVar()

        level_frame = tk.Frame(content, bg="white")
        level_frame.pack(anchor="w", padx=20, pady=(5,15))

        tk.Radiobutton(
            level_frame,
            text="HL",
            variable=level,
            value="HL",
            bg="white"
        ).pack(side="left")

        tk.Radiobutton(
            level_frame,
            text="SL",
            variable=level,
            value="SL",
            bg="white"
        ).pack(side="left", padx=10)
    return frame