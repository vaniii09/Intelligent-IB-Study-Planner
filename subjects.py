import tkinter as tk


def show_subjects(parent):

    frame = tk.Frame(parent, bg="white")

    title = tk.Label(
        frame,
        text="Subjects",
        font=("Arial", 24, "bold"),
        bg="white"
    )

    title.pack(pady=20)

    description = tk.Label(
        frame,
        text="Manage the subjects you study.",
        font=("Arial", 12),
        bg="white"
    )

    description.pack()

    return frame