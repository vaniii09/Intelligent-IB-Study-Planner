
# =========================================
# StudySpace — Central Theme Configuration
# =========================================

# -----------------------------------------
# Main colours
# -----------------------------------------

BACKGROUND = "#F7F7F5"   # Main application background
SIDEBAR = "#F0F0ED"      # Sidebar background
SURFACE = "#FFFFFF"      # Cards and input backgrounds

PRIMARY = "#647C68"      # Sage green accent
ACTIVE = "#E4ECE4"       # Selected navigation item
HOVER = "#E7E7E2"        # Hover backgrounds

TEXT = "#292B28"         # Main text
MUTED = "#85877F"        # Secondary text
SUBTEXT = MUTED          # Compatibility with older files

WHITE = "#FFFFFF"
BORDER = "#E3E4DE"       # Subtle borders


# -----------------------------------------
# Status colours
# -----------------------------------------

SUCCESS = "#6C9272"
WARNING = "#D5A45B"
DANGER = "#C96F6F"


# -----------------------------------------
# Subject colours
# -----------------------------------------

SUBJECT_GREEN = "#E4ECE4"
SUBJECT_BLUE = "#E4EAF5"
SUBJECT_PURPLE = "#EAE5F3"
SUBJECT_YELLOW = "#F4EFD9"
SUBJECT_PINK = "#F3E4E6"
SUBJECT_ORANGE = "#F5E8DB"


# -----------------------------------------
# Typography
# -----------------------------------------

FONT_FAMILY = "Arial"

FONT_SMALL = (FONT_FAMILY, 9)
FONT_NORMAL = (FONT_FAMILY, 11)
FONT_SUBHEADING = (FONT_FAMILY, 14, "bold")
FONT_HEADING = (FONT_FAMILY, 22, "bold")
FONT_TITLE = (FONT_FAMILY, 28, "bold")


# -----------------------------------------
# Compatibility with older files
# -----------------------------------------
# These aliases prevent NameError exceptions
# in modules that still use the original names.


# Colours
CARD = SURFACE

# Text colours
SUBTEXT = MUTED


# Font aliases
TITLE_FONT = FONT_TITLE
SUBTITLE_FONT = FONT_NORMAL
SECTION_FONT = FONT_SUBHEADING
LABEL_FONT = FONT_NORMAL
TEXT_FONT = FONT_NORMAL


# -----------------------------------------
# Optional legacy aliases
# -----------------------------------------

# Some older UI components may use these.
# They preserve the new theme's appearance.

TITLE = TEXT
ACCENT = PRIMARY
SECONDARY = MUTED
LIGHT_BG = BACKGROUND
CARD_BG = SURFACE
BORDER_COLOR = BORDER
# =========================================
# UI dimensions and typography
# =========================================

ENTRY_WIDTH = 35
COMBO_WIDTH = 35
BUTTON_WIDTH = 15

BUTTON_FONT = (FONT_FAMILY, 10, "bold")
