
import tkinter as tk
from tkinter import ttk, messagebox

from scrollable_frame import ScrollableFrame
from database.database import (
    load_subjects,
    load_availability,
    update_subject_level,
    update_availability
)

from theme import *


def show_settings(parent):

    # =========================================
    # Main container
    # =========================================

    container = ScrollableFrame(parent)
    frame = container.scrollable_frame
    frame.configure(bg=BACKGROUND)

    dialog_parent = parent if hasattr(parent, "winfo_toplevel") else frame

    if hasattr(container, "canvas"):
        container.canvas.configure(
            bg=BACKGROUND,
            highlightthickness=0
        )

    # =========================================
    # Page header
    # =========================================

    header = tk.Frame(frame, bg=BACKGROUND)
    header.pack(fill="x", padx=35, pady=(30, 20))

    tk.Label(
        header,
        text="PERSONALISE YOUR WORKSPACE",
        font=("Arial", 9, "bold"),
        bg=BACKGROUND,
        fg=PRIMARY
    ).pack(anchor="w", pady=(0, 8))

    tk.Label(
        header,
        text="Settings",
        font=FONT_TITLE,
        bg=BACKGROUND,
        fg=TEXT
    ).pack(anchor="w")

    tk.Label(
        header,
        text="Manage your subjects and decide when you have time to study.",
        font=FONT_NORMAL,
        bg=BACKGROUND,
        fg=MUTED,
        wraplength=700,
        justify="left"
    ).pack(anchor="w", pady=(7, 0))

    # =========================================
    # Main card
    # =========================================

    card = tk.Frame(
        frame,
        bg=SURFACE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack(
        fill="x",
        padx=35,
        pady=(0, 30)
    )

    content = tk.Frame(card, bg=SURFACE)
    content.pack(fill="x", padx=25, pady=25)

    # =========================================
    # Subjects section
    # =========================================

    subject_header = tk.Frame(content, bg=SURFACE)
    subject_header.pack(fill="x", pady=(0, 5))

    tk.Label(
        subject_header,
        text="📚  Your subjects",
        font=FONT_SUBHEADING,
        bg=SURFACE,
        fg=TEXT
    ).pack(anchor="w")

    tk.Label(
        content,
        text="Choose the level you are studying for each subject.",
        font=FONT_NORMAL,
        bg=SURFACE,
        fg=MUTED
    ).pack(anchor="w", pady=(3, 15))

    subject_frame = tk.Frame(
        content,
        bg=BACKGROUND,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    subject_frame.pack(fill="x")

    subject_boxes = {}
    subjects = load_subjects()

    if not subjects:
        tk.Label(
            subject_frame,
            text="No subjects found.",
            font=FONT_NORMAL,
            bg=BACKGROUND,
            fg=MUTED,
            padx=15,
            pady=15
        ).pack(anchor="w")

    for index, (subject, level) in enumerate(subjects):

        row_bg = SURFACE if index % 2 == 0 else BACKGROUND

        row = tk.Frame(
            subject_frame,
            bg=row_bg
        )

        row.pack(fill="x", padx=12, pady=5)

        tk.Label(
            row,
            text=subject,
            font=FONT_NORMAL,
            bg=row_bg,
            fg=TEXT,
            anchor="w"
        ).pack(side="left", fill="x", expand=True, pady=7)

        combo = ttk.Combobox(
            row,
            values=["HL", "SL"],
            width=8,
            state="readonly",
            font=FONT_NORMAL
        )

        combo.set(level)
        combo.pack(side="right", padx=5, pady=4)

        subject_boxes[subject] = combo

    # =========================================
    # Weekly availability section
    # =========================================

    availability_header = tk.Frame(content, bg=SURFACE)
    availability_header.pack(fill="x", pady=(28, 5))

    tk.Label(
        availability_header,
        text="🗓  Weekly availability",
        font=FONT_SUBHEADING,
        bg=SURFACE,
        fg=TEXT
    ).pack(anchor="w")

    tk.Label(
        content,
        text=(
            "Set how many hours you can realistically study each day. "
            "Your study planner uses these values to create your schedule."
        ),
        font=FONT_NORMAL,
        bg=SURFACE,
        fg=MUTED,
        wraplength=700,
        justify="left"
    ).pack(anchor="w", pady=(3, 15))

    availability_frame = tk.Frame(
        content,
        bg=BACKGROUND,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    availability_frame.pack(fill="x")

    availability_boxes = {}
    availability = load_availability()

    if not availability:
        tk.Label(
            availability_frame,
            text="No availability settings found.",
            font=FONT_NORMAL,
            bg=BACKGROUND,
            fg=MUTED,
            padx=15,
            pady=15
        ).pack(anchor="w")

    for index, (day, hours) in enumerate(availability):

        row_bg = SURFACE if index % 2 == 0 else BACKGROUND

        row = tk.Frame(
            availability_frame,
            bg=row_bg
        )

        row.pack(fill="x", padx=12, pady=5)

        tk.Label(
            row,
            text=day,
            font=FONT_NORMAL,
            bg=row_bg,
            fg=TEXT,
            anchor="w"
        ).pack(side="left", fill="x", expand=True, pady=7)

        input_frame = tk.Frame(row, bg=row_bg)
        input_frame.pack(side="right", padx=5)

        spin = tk.Spinbox(
            input_frame,
            from_=0,
            to=12,
            width=5,
            font=FONT_NORMAL,
            bg=WHITE,
            fg=TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER,
            buttonbackground=WHITE
        )

        spin.delete(0, "end")
        spin.insert(0, hours)

        spin.pack(side="left", ipady=4)

        tk.Label(
            input_frame,
            text="hours",
            font=FONT_SMALL,
            bg=row_bg,
            fg=MUTED
        ).pack(side="left", padx=(8, 0))

        availability_boxes[day] = spin

    # =========================================
    # Save changes
    # =========================================

    def save_changes():

        # Validate all availability values before saving.
        validated_hours = {}

        for day, spin in availability_boxes.items():

            value = spin.get().strip()

            try:
                hours = int(value)
            except ValueError:
                messagebox.showerror(
                    "Invalid availability",
                    f"Please enter a whole number of hours for {day}.",
                    parent=container
                )
                return

            if not 0 <= hours <= 12:
                messagebox.showerror(
                    "Invalid availability",
                    f"Study hours for {day} must be between 0 and 12.",
                    parent=container
                )
                return

            validated_hours[day] = hours

        # Validate subject levels before saving.
        for subject, combo in subject_boxes.items():

            if combo.get() not in ("HL", "SL"):
                messagebox.showerror(
                    "Invalid subject level",
                    f"Please select HL or SL for {subject}.",
                    parent=container
                )
                return

        try:
            for subject, combo in subject_boxes.items():
                update_subject_level(
                    subject,
                    combo.get()
                )

            for day, hours in validated_hours.items():
                update_availability(
                    day,
                    hours
                )

        except Exception as error:
            messagebox.showerror(
                "Save failed",
                f"Your settings could not be saved.\n\n{error}",
                parent=container
            )
            return

        messagebox.showinfo(
            "Settings saved",
            "Your settings have been updated successfully!",
            parent=container
        )

    # =========================================
    # Footer and save button
    # =========================================

    footer = tk.Frame(content, bg=SURFACE)
    footer.pack(fill="x", pady=(25, 0))

    tk.Label(
        footer,
        text="Your changes will be used by the study planner.",
        font=FONT_SMALL,
        bg=SURFACE,
        fg=MUTED
    ).pack(side="left", anchor="center", pady=5)

    save_button = tk.Button(
        footer,
        text="Save changes",
        command=save_changes,
        bg=PRIMARY,
        fg=WHITE,
        activebackground="#536957",
        activeforeground=WHITE,
        font=("Arial", 10, "bold"),
        relief="flat",
        bd=0,
        padx=22,
        pady=11,
        cursor="hand2"
    )

    save_button.pack(side="right")

    save_button.bind(
        "<Enter>",
        lambda event: save_button.configure(bg="#536957")
    )

    save_button.bind(
        "<Leave>",
        lambda event: save_button.configure(bg=PRIMARY)
    )

    return container