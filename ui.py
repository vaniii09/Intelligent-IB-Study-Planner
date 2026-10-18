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
        bg=SURFACE,
        highlightbackground=BORDER,
        highlightthickness=1,
        padx=30,
        pady=25
    )

    card.pack(
        fill="x",
        expand=True,
        padx=20,
        pady=15
    )

    return card


# ==========================================
# TITLES
# ==========================================

def page_title(parent, text):

    label = tk.Label(
        parent,
        text=text,
        font=FONT_TITLE,
        bg=SURFACE,
        fg=TEXT
    )

    label.pack(
        anchor="w",
        pady=(0, 8)
    )

    return label


def page_subtitle(parent, text):

    label = tk.Label(
        parent,
        text=text,
        font=FONT_NORMAL,
        bg=SURFACE,
        fg=MUTED,
        wraplength=650,
        justify="left"
    )

    label.pack(
        anchor="w",
        pady=(0, 25)
    )

    return label


def section_title(parent, text):

    label = tk.Label(
        parent,
        text=text,
        font=FONT_SUBHEADING,
        bg=SURFACE,
        fg=TEXT
    )

    label.pack(
        anchor="w",
        pady=(15, 10)
    )

    return label


# ==========================================
# LABEL
# ==========================================

def create_label(parent, text):

    label = tk.Label(
        parent,
        text=text,
        font=FONT_NORMAL,
        bg=SURFACE,
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
        font=FONT_NORMAL,
        bg=WHITE,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=PRIMARY,
        bd=0
    )

    entry.pack(
        fill="x",
        ipady=8,
        pady=(5, 15)
    )

    return entry


# ==========================================
# COMBOBOX
# ==========================================

def create_combobox(parent, values):

    style = ttk.Style()

    style.configure(
        "StudySpace.TCombobox",
        padding=7,
        fieldbackground=WHITE,
        background=WHITE,
        foreground=TEXT
    )

    style.map(
        "StudySpace.TCombobox",
        fieldbackground=[("readonly", WHITE)],
        selectbackground=[("readonly", WHITE)],
        selectforeground=[("readonly", TEXT)]
    )

    combo = ttk.Combobox(
        parent,
        values=values,
        width=COMBO_WIDTH,
        state="readonly",
        font=FONT_NORMAL,
        style="StudySpace.TCombobox"
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

    button = tk.Button(
        parent,
        text=text,
        command=command,
        width=BUTTON_WIDTH,
        bg=PRIMARY,
        fg=WHITE,
        activebackground="#536957",
        activeforeground=WHITE,
        font=BUTTON_FONT,
        relief="flat",
        bd=0,
        padx=14,
        pady=9,
        cursor="hand2"
    )

    button.bind(
        "<Enter>",
        lambda event: button.configure(bg="#536957")
    )

    button.bind(
        "<Leave>",
        lambda event: button.configure(bg=PRIMARY)
    )

    return button


def secondary_button(parent, text, command):

    button = tk.Button(
        parent,
        text=text,
        command=command,
        width=BUTTON_WIDTH,
        bg=HOVER,
        fg=TEXT,
        activebackground=BORDER,
        activeforeground=TEXT,
        font=BUTTON_FONT,
        relief="flat",
        bd=0,
        padx=14,
        pady=9,
        cursor="hand2"
    )

    button.bind(
        "<Enter>",
        lambda event: button.configure(bg=BORDER)
    )

    button.bind(
        "<Leave>",
        lambda event: button.configure(bg=HOVER)
    )

    return button