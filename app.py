
import tkinter as tk

from study_session import open_study_session
from theme import ACTIVE, BACKGROUND, BORDER, HOVER, MUTED, PRIMARY, SIDEBAR, TEXT
from planner import show_study_planner
from dashboard import show_dashboard
from task_page import show_task_page
from view_tasks import show_view_tasks
from database.database import load_subjects
from settings import show_settings


# =========================================================
# StudySpace — Main Application
# =========================================================

class MainApplication:

    def __init__(self, parent):

        self.parent = parent
        self.active_page = None
        self.nav_buttons = {}

        # -------------------------------------------------
        # Window
        # -------------------------------------------------

        self.parent.configure(bg=BACKGROUND)

        # -------------------------------------------------
        # Main Container
        # -------------------------------------------------

        self.container = tk.Frame(
            self.parent,
            bg=BACKGROUND
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        # -------------------------------------------------
        # Sidebar
        # -------------------------------------------------

        self.sidebar = tk.Frame(
            self.container,
            bg=SIDEBAR,
            width=235
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        self.sidebar.grid_propagate(False)

        # -------------------------------------------------
        # Main Content
        # -------------------------------------------------

        self.content = tk.Frame(
            self.container,
            bg=BACKGROUND
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        # -------------------------------------------------
        # Build Interface
        # -------------------------------------------------

        self.create_sidebar()
        self.dashboard()

    # =====================================================
    # Sidebar
    # =====================================================

    def create_sidebar(self):

        # -------------------------------------------------
        # Brand
        # -------------------------------------------------

        brand_frame = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )

        brand_frame.pack(
            fill="x",
            padx=22,
            pady=(30, 28)
        )

        logo = tk.Label(
            brand_frame,
            text="S.",
            font=("Arial", 20, "bold"),
            bg=PRIMARY,
            fg="white",
            width=2,
            height=1
        )

        logo.pack(
            anchor="w",
            pady=(0, 10)
        )

        title = tk.Label(
            brand_frame,
            text="StudySpace",
            font=("Arial", 17, "bold"),
            bg=SIDEBAR,
            fg=TEXT
        )

        title.pack(anchor="w")

        subtitle = tk.Label(
            brand_frame,
            text="YOUR IB STUDY COMPANION",
            font=("Arial", 8),
            bg=SIDEBAR,
            fg=MUTED
        )

        subtitle.pack(
            anchor="w",
            pady=(5, 0)
        )

        # -------------------------------------------------
        # Navigation Heading
        # -------------------------------------------------

        nav_heading = tk.Label(
            self.sidebar,
            text="WORKSPACE",
            font=("Arial", 9, "bold"),
            bg=SIDEBAR,
            fg=MUTED
        )

        nav_heading.pack(
            anchor="w",
            padx=24,
            pady=(0, 12)
        )

        # -------------------------------------------------
        # Navigation Items
        # -------------------------------------------------

        buttons = [
            ("Dashboard", "01", self.dashboard),
            ("Add a task", "02", self.add_task),
            ("My tasks", "03", self.view_tasks),
            ("Study planner", "04", self.study_plan),
            ("Settings", "05", self.settings),
        ]

        for label, icon, command in buttons:

            self.create_nav_button(
                label=label,
                icon=icon,
                command=command
            )

        # -------------------------------------------------
        # Sidebar Bottom
        # -------------------------------------------------

        spacer = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )

        spacer.pack(
            fill="both",
            expand=True
        )

        separator = tk.Frame(
            self.sidebar,
            bg=BORDER,
            height=1
        )

        separator.pack(
            fill="x",
            padx=20,
            pady=(0, 16)
        )

        footer = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )

        footer.pack(
            fill="x",
            padx=22,
            pady=(0, 24)
        )

        footer_title = tk.Label(
            footer,
            text="Made for your goals.",
            font=("Arial", 10, "bold"),
            bg=SIDEBAR,
            fg=TEXT
        )

        footer_title.pack(anchor="w")

        footer_subtitle = tk.Label(
            footer,
            text="One task at a time.",
            font=("Arial", 9),
            bg=SIDEBAR,
            fg=MUTED
        )

        footer_subtitle.pack(
            anchor="w",
            pady=(4, 0)
        )

    # =====================================================
    # Navigation Button
    # =====================================================

    def create_nav_button(self, label, icon, command):

        button_frame = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )

        button_frame.pack(
            fill="x",
            padx=12,
            pady=3
        )

        button = tk.Button(
            button_frame,
            text=f"  {icon}     {label}",
            command=lambda: self.navigate(label, command),
            font=("Arial", 11),
            bg=SIDEBAR,
            fg=TEXT,
            activebackground=HOVER,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            anchor="w",
            padx=12,
            pady=12,
            cursor="hand2",
            highlightthickness=0
        )

        button.pack(
            fill="x"
        )

        # Hover effects

        button.bind(
            "<Enter>",
            lambda event, b=button, name=label:
                self.on_hover(b, name)
        )

        button.bind(
            "<Leave>",
            lambda event, b=button, name=label:
                self.on_leave(b, name)
        )

        self.nav_buttons[label] = button

    # =====================================================
    # Navigation Behaviour
    # =====================================================

    def navigate(self, label, command):

        self.set_active_page(label)
        command()

    def set_active_page(self, label):

        self.active_page = label

        for name, button in self.nav_buttons.items():

            if name == label:

                button.configure(
                    bg=ACTIVE,
                    fg=PRIMARY,
                    font=("Arial", 11, "bold"),
                    activebackground=ACTIVE
                )

            else:

                button.configure(
                    bg=SIDEBAR,
                    fg=TEXT,
                    font=("Arial", 11),
                    activebackground=HOVER
                )

    def on_hover(self, button, label):

        if label != self.active_page:

            button.configure(
                bg=HOVER
            )

    def on_leave(self, button, label):

        if label != self.active_page:

            button.configure(
                bg=SIDEBAR
            )

    # =====================================================
    # Clear Content
    # =====================================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # =====================================================
    # Study Session
    # =====================================================

    def study_session(self, task_id):

        self.clear_content()

        page = open_study_session(
            self.content,
            task_id
        )

        if page is not None:

            page.pack(
                fill="both",
                expand=True
            )

    # =====================================================
    # Dashboard
    # =====================================================

    def dashboard(self):

        self.set_active_page("Dashboard")
        self.clear_content()

        page = show_dashboard(
            self.content,
            self
        )

        if page is not None:

            page.pack(
                fill="both",
                expand=True
            )

    # =====================================================
    # Add Task
    # =====================================================

    def add_task(self):

        self.set_active_page("Add a task")
        self.clear_content()

        subjects = [
            subject[0]
            for subject in load_subjects()
        ]

        page = show_task_page(
            self.content,
            subjects
        )

        if page is not None:

            page.pack(
                fill="both",
                expand=True
            )

    # =====================================================
    # View Tasks
    # =====================================================

    def view_tasks(self):

        self.set_active_page("My tasks")
        self.clear_content()

        page = show_view_tasks(
            self.content,
            self
        )

        if page is not None:

            page.pack(
                fill="both",
                expand=True
            )

    # =====================================================
    # Settings
    # =====================================================

    def settings(self):

        self.set_active_page("Settings")
        self.clear_content()

        page = show_settings(
            self.content
        )

        if page is not None:

            page.pack(
                fill="both",
                expand=True
            )

    # =====================================================
    # Study Planner
    # =====================================================

    def study_plan(self):

        self.set_active_page("Study planner")
        self.clear_content()

        page = show_study_planner(
            self.content
        )

        if page is not None:

            page.pack(
                fill="both",
                expand=True
            )
