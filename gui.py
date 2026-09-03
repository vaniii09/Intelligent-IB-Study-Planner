import tkinter as tk

from database.database import (
    create_database,
    has_completed_setup,
    archive_old_tasks
)

from wizard.wizard import SetupWizard
from ui_scalling import scale

# -------------------------------------------------
# Create database
# -------------------------------------------------

create_database()
archive_old_tasks()


# -------------------------------------------------
# Main Window
# -------------------------------------------------

root = tk.Tk()

root.title("Intelligent IB Study Planner")

# -------------------------
# Responsive Window Size
# -------------------------

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = scale(1200, root)
window_height = scale(700, root)

# Centre window

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(
    f"{window_width}x{window_height}+{x}+{y}"
)

root.minsize(
    scale(1100, root),
    scale(650, root)
)

root.configure(bg="white")

# -------------------------------------------------
# Launch Application
# -------------------------------------------------

if has_completed_setup():

    from app import MainApplication

    MainApplication(root)

else:

    wizard = SetupWizard(root)

    page = wizard.show()

    page.pack(fill="both", expand=True)


# -------------------------------------------------
# Run
# -------------------------------------------------

root.mainloop()