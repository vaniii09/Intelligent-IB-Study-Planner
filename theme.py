import tkinter as tk

# ==========================================
# SCREEN SCALING
# ==========================================

_root = tk.Tk()
_root.withdraw()

SCREEN_WIDTH = _root.winfo_screenwidth()
SCREEN_HEIGHT = _root.winfo_screenheight()

_root.destroy()

# Base design resolution
BASE_WIDTH = 1920
BASE_HEIGHT = 1080

SCALE = min(
    SCREEN_WIDTH / BASE_WIDTH,
    SCREEN_HEIGHT / BASE_HEIGHT
)

# Prevent fonts becoming too small or too large
SCALE = max(0.85, min(SCALE, 1.15))


def fs(size):
    return max(9, int(size * SCALE))


# ==========================
# COLOURS
# ==========================

BACKGROUND = "#F5F7FA"

CARD = "#FFFFFF"

SIDEBAR = "#263238"

PRIMARY = "#1976D2"

SUCCESS = "#43A047"

WARNING = "#FB8C00"

DANGER = "#E53935"

TEXT = "#263238"

SUBTEXT = "#607D8B"

BORDER = "#CFD8DC"


# ==========================
# FONTS
# ==========================

TITLE_FONT = ("Arial", fs(24), "bold")

SUBTITLE_FONT = ("Arial", fs(11))

HEADING_FONT = ("Arial", fs(16), "bold")

SECTION_FONT = ("Arial", fs(13), "bold")

LABEL_FONT = ("Arial", fs(11), "bold")

TEXT_FONT = ("Arial", fs(11))

BUTTON_FONT = ("Arial", fs(10), "bold")


# ==========================
# SIZES
# ==========================

ENTRY_WIDTH = int(35 * SCALE)

BUTTON_WIDTH = int(16 * SCALE)

COMBO_WIDTH = int(33 * SCALE)