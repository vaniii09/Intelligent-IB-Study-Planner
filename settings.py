import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from scrollable_frame import ScrollableFrame
from database.database import (
    load_subjects,
    load_availability,
    update_subject_level,
    update_availability
)

from theme import *


def show_settings(parent):

    container = ScrollableFrame(parent)
    frame = container.scrollable_frame


    # =====================================
    # Main Card
    # =====================================

    card = tk.Frame(
        frame,
        bg=CARD,
        bd=1,
        relief="solid",
        padx=35,
        pady=20,
        
    )

    card.pack(
        pady=20,
        padx=40,
        fill="x"
    )


    # =====================================
    # Title
    # =====================================

    tk.Label(
        card,
        text="Settings",
        font=TITLE_FONT,
        bg=CARD,
        fg=TEXT
    ).pack(pady=(0, 5))

    tk.Label(
        card,
        text="Manage your subjects and weekly study availability.",
        font=SUBTITLE_FONT,
        bg=CARD,
        fg=SUBTEXT
    ).pack(pady=(0, 25))

    # =====================================
    # Subjects Section
    # =====================================

    subject_frame = tk.LabelFrame(
        card,
        text="📚 Subjects",
        font=SECTION_FONT,
        bg=CARD,
        fg=PRIMARY,
        padx=20,
        pady=20
    )

    subject_frame.pack(
        fill="x",
        pady=10
    )

    subject_boxes = {}

    subjects = load_subjects()

    for subject, level in subjects:

        row = tk.Frame(
            subject_frame,
            bg=CARD
        )

        row.pack(
            fill="x",
            pady=6
        )

        tk.Label(
            row,
            text=subject,
            width=30,
            anchor="w",
            font=TEXT_FONT,
            bg=CARD,
            fg=TEXT
        ).pack(side="left")

        combo = ttk.Combobox(
            row,
            values=["HL", "SL"],
            width=10,
            state="readonly"
        )

        combo.set(level)

        combo.pack(side="right")

        subject_boxes[subject] = combo

    # =====================================
    # Availability Section
    # =====================================

    availability_frame = tk.LabelFrame(
        card,
        text="⏰ Weekly Availability",
        font=SECTION_FONT,
        bg=CARD,
        fg=PRIMARY,
        padx=20,
        pady=20
    )

    availability_frame.pack(
        fill="x",
        pady=20
    )

    availability_boxes = {}

    availability = load_availability()

    for day, hours in availability:

        row = tk.Frame(
            availability_frame,
            bg=CARD
        )

        row.pack(
            fill="x",
            pady=6
        )

        tk.Label(
            row,
            text=day,
            width=20,
            anchor="w",
            font=TEXT_FONT,
            bg=CARD,
            fg=TEXT
        ).pack(side="left")

        spin = tk.Spinbox(
            row,
            from_=0,
            to=12,
            width=5,
            font=TEXT_FONT
        )

        spin.delete(0, "end")
        spin.insert(0, hours)

        spin.pack(side="right")

        availability_boxes[day] = spin

    # =====================================
    # Save Changes
    # =====================================

    def save_changes():

        for subject in subject_boxes:
            update_subject_level(
                subject,
                subject_boxes[subject].get()
            )

        for day in availability_boxes:
            update_availability(
                day,
                availability_boxes[day].get()
            )

        messagebox.showinfo(
            "Success",
            "Settings updated successfully!"
        )

    tk.Button(
        card,
        text="💾 Save Changes",
        command=save_changes,
        bg=PRIMARY,
        fg="white",
        font=BUTTON_FONT,
        width=20,
        height=2,
        cursor="hand2"
    ).pack(pady=(20, 5))

    return container