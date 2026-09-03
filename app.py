import tkinter as tk

from study_session import open_study_session
from theme import*
from planner import show_study_planner
from dashboard import show_dashboard
from task_page import show_task_page
from view_tasks import show_view_tasks
from database.database import load_subjects
from settings import show_settings


class MainApplication:

    def __init__(self, parent):

        self.parent = parent

        # ----------------------
        # Main Container
        # ----------------------

        self.container = tk.Frame(
            parent,
            bg=BACKGROUND
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        # ----------------------
        # Sidebar
        # ----------------------

        self.sidebar = tk.Frame(
            self.container,
            width=220,
            bg=SIDEBAR
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # ----------------------
        # Content Area
        # ----------------------

        self.content = tk.Frame(
            self.container,
            bg="white"
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()

        # ----------------------
        # Show Dashboard Immediately
        # ----------------------

        self.dashboard()

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
    # Sidebar
    # =====================================================

    def create_sidebar(self):

        title = tk.Label(
            self.sidebar,
            text="🎓 Active Planner",
            font=("Arial", 20, "bold"),
            bg=SIDEBAR,
            fg="white"
        )
        title.pack(pady=(30, 10))

        subtitle = tk.Label(
            self.sidebar,
            text="IB Study Planner",
            bg=SIDEBAR,
            fg="#B0BEC5",
            font=("Arial", 10)
        )
        subtitle.pack(pady=(0, 25))

        buttons = [

            ("🏠 Dashboard", self.dashboard),

            ("➕ Add Task", self.add_task),

            ("📋 View Tasks", self.view_tasks),

            ("📅 Study Plan", self.study_plan),

            ("⚙ Settings", self.settings)

        ]

        for text, command in buttons:

            button = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg="#37474F",
                fg="white",
                activebackground=PRIMARY,
                activeforeground="white",
                relief="flat",
                font=("Arial", 11, "bold"),
                cursor="hand2",
                pady=12
            )

            button.pack(
                fill="x",
                padx=15,
                pady=5
            )

        # =====================================================
    # Helper
    # =====================================================

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()        
    # =====================================================
    # Dashboard
    # =====================================================

    def dashboard(self):

        self.clear_content()

        page = show_dashboard(
            self.content,
            self
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # Add Task
    # =====================================================

    def add_task(self):

        self.clear_content()

        subjects = [
            subject[0]
            for subject in load_subjects()
        ]

        page = show_task_page(
            self.content,
            subjects
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # View Tasks
    # =====================================================

    def view_tasks(self):

        self.clear_content()

        page = show_view_tasks(
            self.content,
            self
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # Subjects
    # =====================================================

    def settings(self):

        self.clear_content()

        page = show_settings(
            self.content
        )

        page.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # Study Planner
    # =====================================================

    def study_plan(self):

        self.clear_content()

        page = show_study_planner(
            self.content
        )

        page.pack(
            fill="both",
            expand=True
        )
    