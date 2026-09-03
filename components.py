import tkinter as tk

# ==========================================================
# COLOURS
# ==========================================================

BACKGROUND = "#F5F7FA"
CARD = "#FFFFFF"

PRIMARY = "#1976D2"
SUCCESS = "#43A047"
WARNING = "#FB8C00"
DANGER = "#E53935"

TEXT = "#263238"
SUBTEXT = "#607D8B"


# ==========================================================
# TITLE
# ==========================================================

def create_title(parent, text):

    label = tk.Label(
        parent,
        text=text,
        font=("Arial", 24, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    )

    return label


# ==========================================================
# SUBTITLE
# ==========================================================

def create_subtitle(parent, text):

    label = tk.Label(
        parent,
        text=text,
        font=("Arial", 11),
        bg=BACKGROUND,
        fg=SUBTEXT
    )

    return label


# ==========================================================
# CARD
# ==========================================================

def create_card(parent, title):

    card = tk.LabelFrame(
        parent,
        text=title,
        bg=CARD,
        font=("Arial", 12, "bold"),
        padx=20,
        pady=20,
        bd=1,
        relief="solid"
    )

    return card


# ==========================================================
# BUTTON
# ==========================================================

def create_button(parent, text, colour, command):

    button = tk.Button(

        parent,

        text=text,

        command=command,

        bg=colour,

        fg="white",

        activebackground=colour,

        activeforeground="white",

        relief="flat",

        cursor="hand2",

        font=("Arial", 10, "bold"),

        padx=15,

        pady=8
    )

    return button