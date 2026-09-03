import tkinter as tk

from scrollable_frame import ScrollableFrame
from logic import generate_study_plan
from theme import *



def show_study_planner(parent):

    container = ScrollableFrame(parent)
    frame = container.scrollable_frame
    

   
    # =====================================
    # Main Card
    # =====================================

    main_card = tk.Frame(
        frame,
        bg=CARD,
        bd=1,
        relief="solid",
        padx=35,
        pady=20,
        
    )

    main_card.pack(
        pady=20,
        padx=40,
        fill="x"
    )


    # =====================================
    # Title
    # =====================================

    tk.Label(
        main_card,
        text="Weekly Study Planner",
        font=TITLE_FONT,
        bg=CARD,
        fg=TEXT
    ).pack(pady=(0, 5))

    tk.Label(
        main_card,
        text="Automatically generated using your deadlines, priorities and weekly availability.",
        font=SUBTITLE_FONT,
        bg=CARD,
        fg=SUBTEXT
    ).pack(pady=(0, 30))

    study_plan, unscheduled = generate_study_plan()

 # =====================================
    # Unscheduled Work Warning
    # =====================================

    if unscheduled:

        warning_card = tk.Frame(
            main_card,
            bg="#FFF3E0",
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )

        warning_card.pack(
            fill="x",
            pady=(20, 10)
        )

        tk.Label(
            warning_card,
            text="⚠️ Some Work Could Not Be Scheduled",
            font=("Arial", 13, "bold"),
            bg="#FFF3E0",
            fg="#E65100"
        ).pack(
            anchor="w"
        )

        tk.Label(
            warning_card,
            text=(
                "There is not enough available study time "
                "before the following deadlines:"
            ),
            font=TEXT_FONT,
            bg="#FFF3E0",
            fg=TEXT
        ).pack(
            anchor="w",
            pady=(5, 10)
        )

        for task_name, subject, remaining, deadline in unscheduled:

            tk.Label(
                warning_card,
                text=(
                    f"• {task_name} ({subject}) — "
                    f"{remaining:.1f} hour(s) remaining "
                    f"— Due {deadline}"
                ),
                font=TEXT_FONT,
                bg="#FFF3E0",
                fg=TEXT
            ).pack(
                anchor="w",
                pady=2
            )    

    # =====================================
    # Days
    # =====================================

    for day, sessions in study_plan.items():

        day_card = tk.Frame(
            main_card,
            bg="#F9FAFB",
            bd=1,
            relief="solid",
            padx=20,
            pady=18
        )

        day_card.pack(
            fill="x",
            pady=10
        )

        # --------------------------
        # Day Title
        # --------------------------

        tk.Label(
            day_card,
            text=day,
            font=SECTION_FONT,
            bg="#F9FAFB",
            fg=PRIMARY
        ).pack(anchor="w", pady=(0, 15))

        # --------------------------
        # Empty Day
        # --------------------------

        if len(sessions) == 0:

            tk.Label(
                day_card,
                text="🎉 No study sessions scheduled",
                font=TEXT_FONT,
                bg="#F9FAFB",
                fg=SUBTEXT
            ).pack(anchor="w")

        # --------------------------
        # Sessions
        # --------------------------

        else:

            for task_name, subject, hours in sessions:

                session = tk.Frame(
                    day_card,
                    bg="white",
                    bd=1,
                    relief="solid",
                    padx=12,
                    pady=10
                )

                session.pack(
                    fill="x",
                    pady=5
                )

                tk.Label(
                    session,
                    text=task_name,
                    font=("Arial", 11, "bold"),
                    bg="white",
                    fg=TEXT
                ).pack(anchor="w")

                tk.Label(
                    session,
                    text=f"📚 {subject}",
                    font=TEXT_FONT,
                    bg="white",
                    fg=SUBTEXT
                ).pack(anchor="w")

                tk.Label(
                    session,
                    text=f"⏱ {hours:.1f} hour(s)",
                    font=TEXT_FONT,
                    bg="white",
                    fg=PRIMARY
                ).pack(anchor="w")
                
    return container