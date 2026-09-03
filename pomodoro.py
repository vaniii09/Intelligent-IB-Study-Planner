import tkinter as tk
from tkinter import messagebox
import time

from database.database import mark_task_complete


class PomodoroTimer:

    def __init__(
        self,
        parent,
        study_minutes,
        break_minutes,
        sessions,
        task_id
    ):

        # =====================================================
        # WINDOW
        # =====================================================

        self.window = tk.Toplevel(parent)

        self.window.title("Pomodoro Timer")
        self.window.geometry("420x480")
        self.window.configure(bg="white")

        # =====================================================
        # TIMER SETTINGS
        # =====================================================

        self.study_seconds = study_minutes * 60
        self.break_seconds = break_minutes * 60

        self.remaining = self.study_seconds

        self.sessions = sessions
        self.current_session = 1
        self.task_id = task_id

        self.on_break = False
        self.running = False

        # Used for accurate timing
        self.end_time = None

        # Stores the scheduled Tkinter callback
        self.after_id = None

        # =====================================================
        # TITLE
        # =====================================================

        tk.Label(
            self.window,
            text="🍅 Pomodoro Timer",
            font=("Arial", 22, "bold"),
            bg="white",
            fg="#263238"
        ).pack(pady=(25, 10))

        # =====================================================
        # PHASE
        # =====================================================

        self.phase_label = tk.Label(
            self.window,
            text="📚 Study Session",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#263238"
        )

        self.phase_label.pack(pady=5)

        # =====================================================
        # TIMER
        # =====================================================

        self.timer_label = tk.Label(
            self.window,
            text="25:00",
            font=("Consolas", 42, "bold"),
            bg="white",
            fg="#1976D2"
        )

        self.timer_label.pack(pady=20)

        # =====================================================
        # SESSION PROGRESS
        # =====================================================

        self.progress = tk.Label(
            self.window,
            text=f"Session 1 of {sessions}",
            bg="white",
            fg="#607D8B",
            font=("Arial", 11)
        )

        self.progress.pack(pady=5)

        # =====================================================
        # BUTTONS
        # =====================================================

        button_frame = tk.Frame(
            self.window,
            bg="white"
        )

        button_frame.pack(pady=25)

        # START

        tk.Button(
            button_frame,
            text="▶ Start",
            width=10,
            command=self.start
        ).grid(
            row=0,
            column=0,
            padx=4
        )

        # PAUSE

        tk.Button(
            button_frame,
            text="⏸ Pause",
            width=10,
            command=self.pause
        ).grid(
            row=0,
            column=1,
            padx=4
        )

        # SKIP

        tk.Button(
            button_frame,
            text="⏭ Skip",
            width=10,
            command=self.skip
        ).grid(
            row=0,
            column=2,
            padx=4
        )

        # RESET

        tk.Button(
            button_frame,
            text="🔄 Reset",
            width=10,
            command=self.reset
        ).grid(
            row=1,
            column=0,
            columnspan=3,
            pady=10
        )

        # =====================================================
        # INITIAL DISPLAY
        # =====================================================

        self.update_display()

    # =========================================================
    # DISPLAY
    # =========================================================

    def update_display(self):

        minutes = int(self.remaining // 60)
        seconds = int(self.remaining % 60)

        self.timer_label.config(
            text=f"{minutes:02}:{seconds:02}"
        )

    # =========================================================
    # START
    # =========================================================

    def start(self):

        if self.running:
            return

        self.running = True

        # Record the exact moment the timer starts
        self.end_time = time.monotonic() + self.remaining

        self.countdown()

    # =========================================================
    # PAUSE
    # =========================================================

    def pause(self):

        if not self.running:
            return

        # Calculate the actual remaining time
        self.remaining = max(
            0,
            self.end_time - time.monotonic()
        )

        self.running = False
        self.end_time = None

        # Cancel the scheduled callback
        if self.after_id is not None:

            try:
                self.window.after_cancel(
                    self.after_id
                )

            except tk.TclError:
                pass

            self.after_id = None

        self.update_display()

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.running = False
        self.end_time = None

        # Cancel existing callback

        if self.after_id is not None:

            try:
                self.window.after_cancel(
                    self.after_id
                )

            except tk.TclError:
                pass

            self.after_id = None

        if self.on_break:

            self.remaining = self.break_seconds

        else:

            self.remaining = self.study_seconds

        self.update_display()

    # =========================================================
    # SKIP
    # =========================================================

    def skip(self):

        # Stop current timer

        self.running = False
        self.end_time = None

        # Cancel scheduled callback

        if self.after_id is not None:

            try:
                self.window.after_cancel(
                    self.after_id
                )

            except tk.TclError:
                pass

            self.after_id = None

        # Move immediately to the next phase

        self.next_phase(
            skipped=True
        )

    # =========================================================
    # ACCURATE COUNTDOWN
    # =========================================================

    def countdown(self):

        if not self.running:
            return

        # Calculate actual remaining time
        self.remaining = max(
            0,
            self.end_time - time.monotonic()
        )

        self.update_display()

        # Timer finished

        if self.remaining <= 0:

            self.running = False
            self.end_time = None

            self.after_id = None

            self.next_phase()

            return

        # Update display approximately every 100 ms
        #
        # IMPORTANT:
        # We are NOT subtracting 0.1 seconds.
        # The actual remaining time is recalculated
        # using time.monotonic().

        self.after_id = self.window.after(
            100,
            self.countdown
        )

    # =========================================================
    # NEXT PHASE
    # =========================================================

    def next_phase(
        self,
        skipped=False
    ):

        # -----------------------------------------------------
        # STUDY → BREAK
        # -----------------------------------------------------

        if not self.on_break:

            self.on_break = True

            self.remaining = self.break_seconds

            self.phase_label.config(
                text="☕ Break Time"
            )

            self.update_display()

            self.start()

        # -----------------------------------------------------
        # BREAK → NEXT STUDY
        # -----------------------------------------------------

        else:

            self.current_session += 1

            # -------------------------------------------------
            # Finished all sessions
            # -------------------------------------------------

            if self.current_session > self.sessions:

                self.running = False

                self.show_completion_screen()

                return

            # -------------------------------------------------
            # Next study session
            # -------------------------------------------------

            self.on_break = False

            self.remaining = self.study_seconds

            self.phase_label.config(
                text="📚 Study Session"
            )

            self.progress.config(
                text=(
                    f"Session "
                    f"{self.current_session} "
                    f"of "
                    f"{self.sessions}"
                )
            )

            self.update_display()

            self.start()

    # =========================================================
    # TASK COMPLETION
    # =========================================================

    def show_completion_screen(self):

        # Remove everything currently inside
        # the timer window

        for widget in self.window.winfo_children():

            widget.destroy()

        tk.Label(
            self.window,
            text="🎉",
            font=("Arial", 40),
            bg="white"
        ).pack(
            pady=(40, 10)
        )

        tk.Label(
            self.window,
            text="All Pomodoro sessions completed!",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#263238"
        ).pack(
            pady=10
        )

        tk.Label(
            self.window,
            text="Did you finish this task?",
            font=("Arial", 12),
            bg="white",
            fg="#607D8B"
        ).pack(
            pady=10
        )

        # -----------------------------------------------------
        # MARK COMPLETED
        # -----------------------------------------------------

        def finish_task():

            mark_task_complete(
                self.task_id
            )

            messagebox.showinfo(
                "Task Completed",
                "✅ Task marked as completed!"
            )

            self.window.destroy()

        tk.Button(
            self.window,
            text="✅ Mark Task as Completed",
            font=("Arial", 11, "bold"),
            bg="#43A047",
            fg="white",
            width=25,
            height=2,
            relief="flat",
            cursor="hand2",
            command=finish_task
        ).pack(
            pady=20
        )

        # -----------------------------------------------------
        # KEEP WORKING
        # -----------------------------------------------------

        tk.Button(
            self.window,
            text="Continue Working",
            font=("Arial", 10),
            bg="#ECEFF1",
            fg="#263238",
            width=20,
            relief="flat",
            cursor="hand2",
            command=self.window.destroy
        ).pack(
            pady=5
        )