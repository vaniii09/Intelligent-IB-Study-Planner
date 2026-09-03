import tkinter as tk
from tkinter import ttk, messagebox

from database.database import (
    get_task,
    load_subjects,
    update_task,
    get_subject_level
)

from logic import calculate_priority


def show_edit_task(parent, task_id, refresh_callback):

    task = get_task(task_id)

    if task is None:
        messagebox.showerror(
            "Error",
            "Task not found."
        )
        return

    (
        task_id,
        old_title,
        old_subject,
        old_task_type,
        old_deadline,
        old_hours,
        old_priority,
        completed,
        completed_date,
        archived
    ) = task

    window = tk.Toplevel(parent)
    window.title("Edit Task")
    window.geometry("450x500")
    window.configure(bg="white")

    # -------------------------
    # Title
    # -------------------------

    tk.Label(
        window,
        text="Edit Task",
        font=("Arial", 20, "bold"),
        bg="white"
    ).pack(pady=15)

    # -------------------------
    # Task Title
    # -------------------------

    tk.Label(
        window,
        text="Task Title",
        bg="white"
    ).pack()

    title_entry = tk.Entry(
        window,
        width=35
    )

    title_entry.pack(pady=5)
    title_entry.insert(0, old_title)

    # -------------------------
    # Subject
    # -------------------------

    tk.Label(
        window,
        text="Subject",
        bg="white"
    ).pack()

    subjects = [subject for subject, level in load_subjects()]

    subject_box = ttk.Combobox(
        window,
        values=subjects,
        state="readonly",
        width=32
    )

    subject_box.pack(pady=5)
    subject_box.set(old_subject)

    # -------------------------
    # Task Type
    # -------------------------

    tk.Label(
        window,
        text="Task Type",
        bg="white"
    ).pack()

    task_box = ttk.Combobox(
        window,
        values=[
            "Homework",
            "Test",
            "Quiz",
            "Revision",
            "IA",
            "EE",
            "CAS",
            "Presentation"
        ],
        state="readonly",
        width=32
    )

    task_box.pack(pady=5)
    task_box.set(old_task_type)

    # -------------------------
    # Deadline
    # -------------------------

    tk.Label(
        window,
        text="Deadline (YYYY-MM-DD)",
        bg="white"
    ).pack()

    deadline_entry = tk.Entry(
        window,
        width=35
    )

    deadline_entry.pack(pady=5)
    deadline_entry.insert(0, old_deadline)

    # -------------------------
    # Estimated Hours
    # -------------------------

    tk.Label(
        window,
        text="Estimated Hours",
        bg="white"
    ).pack()

    hours_entry = tk.Entry(
        window,
        width=20
    )

    hours_entry.pack(pady=5)
    hours_entry.insert(0, str(old_hours))

    # -------------------------
    # Save Changes
    # -------------------------

    def save_changes():

        title = title_entry.get()
        subject = subject_box.get()
        task_type = task_box.get()
        deadline = deadline_entry.get()
        hours = hours_entry.get()

        if (
            title == "" or
            subject == "" or
            task_type == "" or
            deadline == "" or
            hours == ""
        ):
            messagebox.showerror(
                "Error",
                "Please complete every field."
            )
            return

        try:
            hours = float(hours)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Estimated hours must be a number."
            )
            return

        level = get_subject_level(subject)

        priority = calculate_priority(
            deadline,
            hours,
            level
        )

        update_task(
            task_id,
            title,
            subject,
            task_type,
            deadline,
            hours,
            priority
        )

        messagebox.showinfo(
            "Success",
            "Task updated successfully!"
        )

        window.destroy()

        refresh_callback()

    save_button = tk.Button(
        window,
        text="Save Changes",
        command=save_changes,
        width=20
    )

    save_button.pack(pady=20)