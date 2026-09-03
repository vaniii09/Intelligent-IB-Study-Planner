import tkinter as tk
from tkinter import ttk

from theme import *


# ==========================================
# PAGE
# ==========================================

def create_page(parent):

    page = tk.Frame(
        parent,
        bg=BACKGROUND
    )

    page.pack_propagate(False)

    content = tk.Frame(
        page,
        bg=BACKGROUND
    )

    content.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    return page, content


# ==========================================
# CARD
# ==========================================

def create_card(parent):

    card = tk.Frame(
        parent,
        bg=CARD,
        bd=1,
        relief="solid",
        padx=35,
        pady=20,
        # width was previously referencing an undefined variable; rely on packing instead
    )

    card.pack(
        fill="x",
        expand=True,
        padx=20
    )

    return card


# ==========================================
# TITLES
# ==========================================

def page_title(parent, text):

    tk.Label(
        parent,
        text=text,
        font=TITLE_FONT,
        bg=CARD,
        fg=TEXT
    ).pack(pady=(0, 8))


def page_subtitle(parent, text):

    tk.Label(
        parent,
        text=text,
        font=SUBTITLE_FONT,
        bg=CARD,
        fg=SUBTEXT
    ).pack(pady=(0, 25))


def section_title(parent, text):

    tk.Label(
        parent,
        text=text,
        font=SECTION_FONT,
        bg=CARD,
        fg=TEXT
    ).pack(anchor="w", pady=(15, 10))


# ==========================================
# LABEL
# ==========================================

def create_label(parent, text):

    label = tk.Label(
        parent,
        text=text,
        font=LABEL_FONT,
        bg=CARD,
        fg=TEXT
    )

    label.pack(anchor="w")

    return label


# ==========================================
# ENTRY
# ==========================================

def create_entry(parent):

    entry = tk.Entry(
        parent,
        width=ENTRY_WIDTH,
        font=TEXT_FONT
    )

    entry.pack(
        fill="x",
        pady=(5, 15)
    )

    return entry


# ==========================================
# COMBOBOX
# ==========================================

def create_combobox(parent, values):

    combo = ttk.Combobox(
        parent,
        values=values,
        width=COMBO_WIDTH,
        state="readonly"
    )

    combo.pack(
        fill="x",
        pady=(5, 15)
    )

    return combo


# ==========================================
# BUTTONS
# ==========================================

def primary_button(parent, text, command):

    return tk.Button(
        parent,
        text=text,
        command=command,
        width=BUTTON_WIDTH,
        bg=PRIMARY,
        fg="white",
        font=BUTTON_FONT,
        relief="flat",
        cursor="hand2"
    )


def secondary_button(parent, text, command):

    return tk.Button(
        parent,
        text=text,
        command=command,
        width=BUTTON_WIDTH,
        bg="#ECEFF1",
        fg=TEXT,
        font=BUTTON_FONT,
        relief="flat",
        cursor="hand2"
    )