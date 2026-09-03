import tkinter as tk
from tkinter import messagebox

from dashboard import show_dashboard
from database.database import (save_subjects, save_availability)
from wizard.subject_page import create_subject_page
from wizard.availability_page import create_availability_page
from subjects_data import IB_SUBJECTS
from validation import validate_subject_selection


class SetupWizard:

    def __init__(self, parent):

        self.parent = parent
        self.current_step = 0

        self.groups = [
            "Group 1 - Studies in Language and Literature",
            "Group 2 - Language Acquisition",
            "Group 3 - Individuals & Societies",
            "Group 4 - Sciences",
            "Group 5 - Mathematics",
            "Group 6 - Arts"
        ]

        self.selected_subjects = []
        self.selected_levels = {}
        self.available_hours = {}

        # Stores every checkbox and HL/SL variable
        self.subject_variables = {}

        for group in self.groups:
            for subject in IB_SUBJECTS[group]:

                self.subject_variables[subject] = {
                    "selected": tk.BooleanVar(value=False),
                    "level": tk.StringVar(value="SL")
                }

    # -------------------------------------------------
    # Welcome Page
    # -------------------------------------------------

    def show(self):

        self.frame = tk.Frame(self.parent, bg="white")

        title = tk.Label(
            self.frame,
            text="Welcome to Intelligent IB Study Planner",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            self.frame,
            text="Let's personalise your study planner.",
            font=("Arial", 12),
            bg="white"
        )
        subtitle.pack()

        progress = tk.Label(
            self.frame,
            text="Step 1 of 9",
            font=("Arial", 11),
            fg="grey",
            bg="white"
        )
        progress.pack(pady=10)

        next_button = tk.Button(
            self.frame,
            text="Next →",
            width=15,
            command=self.next_step
        )
        next_button.pack(pady=40)

        return self.frame

    # -------------------------------------------------
    # Save selections
    # -------------------------------------------------

    def save_selected_subjects(self):

        self.selected_subjects.clear()
        self.selected_levels.clear()

        for subject, data in self.subject_variables.items():

            if data["selected"].get():

                self.selected_subjects.append(subject)
                self.selected_levels[subject] = data["level"].get()

        print("Subjects:", self.selected_subjects)
        print("Levels:", self.selected_levels)

    def finish_setup(self):

        # Save everything
        save_subjects(
            self.selected_subjects,
            self.selected_levels
        )

        save_availability(
            self.available_hours
        )

        print("\n---------- SETUP COMPLETE ----------")
        print(self.selected_subjects)
        print(self.selected_levels)

        if hasattr(self, "frame"):
            self.frame.destroy()

        from app import MainApplication

        app = MainApplication(self.parent)

        app.dashboard()

    # -------------------------------------------------
    # Next Page
    # -------------------------------------------------

    def next_step(self):

        self.save_selected_subjects()

        #valdate only after the final subject page
        if self.current_step == len(self.groups):
            valid, message = validate_subject_selection(self)
            if not valid:
                messagebox.showerror("Invalid Selection", message)
                return
        self.current_step += 1

        if hasattr(self, "frame"):
            self.frame.destroy()

        # If still within subject group steps, show the subject page
        if self.current_step <= len(self.groups):
            group = self.groups[self.current_step - 1]
            self.frame = create_subject_page(
                self.parent,
                self,
                group,
                self.current_step + 1,
                len(self.groups) + 3,
                self.next_step,
                self.previous_step
            )

        # After subject pages, show availability page
        elif self.current_step == len(self.groups) + 1:
            self.frame = create_availability_page(
                self.parent,
                self,
                self.current_step + 1,
                len(self.groups) + 3,
                self.finish_setup,
                self.previous_step
            )

        else:
            # For any further steps, finish setup
            self.finish_setup()

        if hasattr(self, "frame") and self.frame is not None:
            self.frame.pack(fill="both", expand=True)
        return

        # -------------------------------------------------
    # Previous Page
    # -------------------------------------------------

    def previous_step(self):

        if self.current_step <= 1:
            return

        self.save_selected_subjects()

        self.current_step -= 1

        if hasattr(self, "frame"):
            self.frame.destroy()

        # Back into subject pages
        if self.current_step <= len(self.groups):

            group = self.groups[self.current_step - 1]

            self.frame = create_subject_page(
                self.parent,
                self,
                group,
                self.current_step + 1,
                len(self.groups) + 3,
                self.next_step,
                self.previous_step
            )

        # Back to availability page
        else:

            self.frame = create_availability_page(
                self.parent,
                self,
                self.current_step + 1,
                len(self.groups) + 3,
                self.finish_setup,
                self.previous_step
            )

        self.frame.pack(fill="both", expand=True)