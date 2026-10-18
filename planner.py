import tkinter as tk

from scrollable_frame import ScrollableFrame
from logic import generate_study_plan
from theme import *


def show_study_planner(parent):

    # =========================================
    # Main container
    # =========================================

    container = ScrollableFrame(parent)
    frame = container.scrollable_frame
    frame.configure(bg=BACKGROUND)

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
        text="YOUR WEEK, AT A GLANCE",
        font=("Arial", 9, "bold"),
        bg=BACKGROUND,
        fg=PRIMARY
    ).pack(anchor="w", pady=(0, 8))

    tk.Label(
        header,
        text="Study Plan",
        font=FONT_TITLE,
        bg=BACKGROUND,
        fg=TEXT
    ).pack(anchor="w")

    tk.Label(
        header,
        text=(
            "A personalised study schedule based on your deadlines, "
            "priorities and weekly availability."
        ),
        font=FONT_NORMAL,
        bg=BACKGROUND,
        fg=MUTED,
        wraplength=750,
        justify="left"
    ).pack(anchor="w", pady=(7, 0))

    # =========================================
    # Generate study plan
    # =========================================

    study_plan, unscheduled = generate_study_plan()

    # =========================================
    # Main content card
    # =========================================

    main_card = tk.Frame(
        frame,
        bg=SURFACE,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    main_card.pack(
        fill="x",
        padx=35,
        pady=(0, 30)
    )

    content = tk.Frame(main_card, bg=SURFACE)
    content.pack(fill="x", padx=25, pady=25)

    # =========================================
    # Plan overview
    # =========================================

    total_sessions = sum(
        len(sessions)
        for sessions in study_plan.values()
    )

    total_hours = sum(
        hours
        for sessions in study_plan.values()
        for _, _, hours in sessions
    )

    overview = tk.Frame(content, bg=SURFACE)
    overview.pack(fill="x", pady=(0, 25))

    overview.grid_columnconfigure(0, weight=1)
    overview.grid_columnconfigure(1, weight=1)
    overview.grid_columnconfigure(2, weight=1)

    overview_items = [
        ("STUDY DAYS", str(sum(
            1 for sessions in study_plan.values() if sessions
        )), SUBJECT_GREEN),
        ("STUDY SESSIONS", str(total_sessions), SUBJECT_BLUE),
        ("PLANNED HOURS", f"{total_hours:.1f}h", SUBJECT_PURPLE)
    ]

    for col, (label, value, colour) in enumerate(overview_items):

        card = tk.Frame(
            overview,
            bg=colour,
            padx=16,
            pady=15
        )

        card.grid(
            row=0,
            column=col,
            sticky="nsew",
            padx=(0 if col == 0 else 6, 6 if col < 2 else 0)
        )

        tk.Label(
            card,
            text=label,
            font=("Arial", 8, "bold"),
            bg=colour,
            fg=MUTED
        ).pack(anchor="w")

        tk.Label(
            card,
            text=value,
            font=("Arial", 20, "bold"),
            bg=colour,
            fg=TEXT
        ).pack(anchor="w", pady=(5, 0))

    # =========================================
    # Unscheduled work warning
    # =========================================

    if unscheduled:

        warning_card = tk.Frame(
            content,
            bg="#FFF7E8",
            highlightbackground="#E8D5AE",
            highlightthickness=1,
            padx=18,
            pady=16
        )

        warning_card.pack(fill="x", pady=(0, 25))

        tk.Label(
            warning_card,
            text="⚠  Work that needs your attention",
            font=FONT_SUBHEADING,
            bg="#FFF7E8",
            fg="#9A641D"
        ).pack(anchor="w")

        tk.Label(
            warning_card,
            text=(
                "There may not be enough available study time "
                "to complete the following tasks before their deadlines."
            ),
            font=FONT_NORMAL,
            bg="#FFF7E8",
            fg=TEXT,
            wraplength=700,
            justify="left"
        ).pack(anchor="w", pady=(7, 12))

        for task_name, subject, remaining, deadline in unscheduled:

            item = tk.Frame(
                warning_card,
                bg="#FFF7E8"
            )

            item.pack(fill="x", pady=4)

            tk.Label(
                item,
                text="•",
                font=("Arial", 12, "bold"),
                bg="#FFF7E8",
                fg="#B47B2B"
            ).pack(side="left", anchor="n", padx=(0, 8))

            details = tk.Frame(item, bg="#FFF7E8")
            details.pack(side="left", fill="x", expand=True)

            tk.Label(
                details,
                text=f"{task_name} · {subject}",
                font=("Arial", 10, "bold"),
                bg="#FFF7E8",
                fg=TEXT,
                wraplength=650,
                justify="left"
            ).pack(anchor="w")

            tk.Label(
                details,
                text=f"{remaining:.1f} hours remaining  ·  Due {deadline}",
                font=FONT_SMALL,
                bg="#FFF7E8",
                fg="#9A641D"
            ).pack(anchor="w", pady=(3, 0))

    # =========================================
    # Weekly schedule heading
    # =========================================

    section_header = tk.Frame(content, bg=SURFACE)
    section_header.pack(fill="x", pady=(0, 12))

    tk.Label(
        section_header,
        text="Your weekly schedule",
        font=FONT_SUBHEADING,
        bg=SURFACE,
        fg=TEXT
    ).pack(side="left")

    tk.Label(
        section_header,
        text="GENERATED PLAN",
        font=("Arial", 8, "bold"),
        bg=SURFACE,
        fg=MUTED
    ).pack(side="right")

    # =========================================
    # Day cards
    # =========================================

    day_colours = [
        SUBJECT_GREEN,
        SUBJECT_BLUE,
        SUBJECT_PURPLE,
        SUBJECT_YELLOW,
        SUBJECT_PINK,
        SUBJECT_ORANGE
    ]

    if not study_plan:

        empty_state = tk.Frame(
            content,
            bg=BACKGROUND,
            padx=20,
            pady=30
        )

        empty_state.pack(fill="x")

        tk.Label(
            empty_state,
            text="No study plan available yet",
            font=FONT_SUBHEADING,
            bg=BACKGROUND,
            fg=TEXT
        ).pack()

        tk.Label(
            empty_state,
            text=(
                "Add tasks and set your weekly availability "
                "to generate a study schedule."
            ),
            font=FONT_NORMAL,
            bg=BACKGROUND,
            fg=MUTED,
            wraplength=600,
            justify="center"
        ).pack(pady=(8, 0))

    for day_index, (day, sessions) in enumerate(study_plan.items()):

        day_card = tk.Frame(
            content,
            bg=BACKGROUND,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        day_card.pack(fill="x", pady=6)

        # Day heading

        day_header = tk.Frame(
            day_card,
            bg=BACKGROUND
        )

        day_header.pack(fill="x", padx=16, pady=(14, 10))

        day_colour = day_colours[day_index % len(day_colours)]

        day_badge = tk.Label(
            day_header,
            text=day.upper(),
            font=("Arial", 10, "bold"),
            bg=day_colour,
            fg=TEXT,
            padx=10,
            pady=5
        )

        day_badge.pack(side="left")

        session_count = len(sessions)

        count_text = (
            f"{session_count} session"
            if session_count == 1
            else f"{session_count} sessions"
        )

        tk.Label(
            day_header,
            text=count_text,
            font=FONT_SMALL,
            bg=BACKGROUND,
            fg=MUTED
        ).pack(side="right", anchor="center")

        # Empty day

        if not sessions:

            empty_day = tk.Frame(
                day_card,
                bg=SURFACE,
                padx=15,
                pady=15
            )

            empty_day.pack(
                fill="x",
                padx=12,
                pady=(0, 12)
            )

            tk.Label(
                empty_day,
                text="A little breathing room",
                font=("Arial", 10, "bold"),
                bg=SURFACE,
                fg=TEXT
            ).pack(anchor="w")

            tk.Label(
                empty_day,
                text="No study sessions scheduled for this day.",
                font=FONT_NORMAL,
                bg=SURFACE,
                fg=MUTED
            ).pack(anchor="w", pady=(4, 0))

        # Scheduled sessions

        else:

            sessions_container = tk.Frame(
                day_card,
                bg=BACKGROUND
            )

            sessions_container.pack(
                fill="x",
                padx=12,
                pady=(0, 12)
            )

            for task_name, subject, hours in sessions:

                session_card = tk.Frame(
                    sessions_container,
                    bg=SURFACE,
                    highlightbackground=BORDER,
                    highlightthickness=1
                )

                session_card.pack(fill="x", pady=4)

                # Small accent on the left

                accent = tk.Frame(
                    session_card,
                    bg=PRIMARY,
                    width=4
                )

                accent.pack(side="left", fill="y")

                session_content = tk.Frame(
                    session_card,
                    bg=SURFACE
                )

                session_content.pack(
                    side="left",
                    fill="both",
                    expand=True,
                    padx=14,
                    pady=12
                )

                top_row = tk.Frame(
                    session_content,
                    bg=SURFACE
                )

                top_row.pack(fill="x")

                tk.Label(
                    top_row,
                    text=task_name,
                    font=("Arial", 11, "bold"),
                    bg=SURFACE,
                    fg=TEXT,
                    wraplength=550,
                    justify="left"
                ).pack(side="left", anchor="w", fill="x", expand=True)

                tk.Label(
                    top_row,
                    text=f"{hours:.1f}h",
                    font=("Arial", 10, "bold"),
                    bg=SUBJECT_GREEN,
                    fg=PRIMARY,
                    padx=9,
                    pady=4
                ).pack(side="right", padx=(10, 0))

                tk.Label(
                    session_content,
                    text=subject,
                    font=FONT_NORMAL,
                    bg=SURFACE,
                    fg=MUTED
                ).pack(anchor="w", pady=(5, 0))

    # =========================================
    # Footer note
    # =========================================

    footer = tk.Frame(frame, bg=BACKGROUND)
    footer.pack(fill="x", padx=35, pady=(0, 25))

    tk.Label(
        footer,
        text=(
            "Tip: Keep your availability realistic and update your tasks "
            "as your deadlines change."
        ),
        font=FONT_SMALL,
        bg=BACKGROUND,
        fg=MUTED,
        wraplength=750,
        justify="left"
    ).pack(anchor="w")

    return container