import tkinter as tk
from tkinter import messagebox

from milestones import generate_milestone_tasks

from database.database import (
    save_task,
    get_subject_level
)

from logic import calculate_priority

from ui import (
    create_page,
    create_card,
    page_title,
    page_subtitle,
    create_label,
    create_entry,
    create_combobox,
    primary_button
)


def show_task_page(parent, subjects):

    page, content = create_page(parent)

    card = create_card(content)

    page_title(
        card,
        "Add New Task"
    )

    page_subtitle(
        card,
        "Plan your next assignment or revision session."
    )

    # -----------------------------
    # Task Title
    # -----------------------------

    create_label(
        card,
        "Task Title"
    )

    title_entry = create_entry(card)

    # -----------------------------
    # Subject
    # -----------------------------

    create_label(
        card,
        "Subject"
    )

    subject_box = create_combobox(
        card,
        subjects
    )

    # -----------------------------
    # Task Type
    # -----------------------------

    create_label(
        card,
        "Task Type"
    )

    task_type = create_combobox(
        card,
        [
            "Homework",
            "Quiz",
            "Test",
            "Revision",
            "IA",
            "EE",
            "CAS",
            "Presentation"
        ]
    )

    # -----------------------------
    # Deadline
    # -----------------------------

    create_label(
        card,
        "Deadline (YYYY-MM-DD)"
    )

    deadline_entry = create_entry(card)

    # -----------------------------
    # Estimated Hours
    # -----------------------------

    create_label(
        card,
        "Estimated Hours"
    )

    hours_entry = create_entry(card)

    # -----------------------------
    # Save
    # -----------------------------

    def save():

        title = title_entry.get().strip()
        subject = subject_box.get()
        task = task_type.get()
        deadline = deadline_entry.get().strip()
        hours = hours_entry.get().strip()

        if not all([title, subject, task, deadline, hours]):

            messagebox.showerror(
                "Error",
                "Please complete every field."
            )
            return

        level = get_subject_level(subject)

        priority = calculate_priority(
            deadline,
            hours,
            level
        )

        save_task(
            title,
            subject,
            task,
            deadline,
            hours,
            priority
        )

        # Automatically generate milestone tasks

        milestones = generate_milestone_tasks(
            title,
            subject,
            task,
            deadline,
            hours,
            level
        )

        for milestone in milestones:

            save_task(*milestone)

        messagebox.showinfo(
            "Success",
            "Task added successfully!"
        )

        title_entry.delete(0, tk.END)
        deadline_entry.delete(0, tk.END)
        hours_entry.delete(0, tk.END)

        subject_box.set("")
        task_type.set("")

    primary_button(
        card,
        "Save Task",
        save
    ).pack(
        pady=15
    )

    return page