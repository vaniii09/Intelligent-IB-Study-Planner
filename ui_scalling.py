import tkinter as tk


def get_scale(root):
    """
    Returns Windows display scaling.

    100% = 1.0
    125% = 1.25
    150% = 1.5
    """

    return float(root.tk.call("tk", "scaling"))


def scale(value, root):
    """
    Scale any size based on monitor DPI.
    """

    scaling = get_scale(root)

    return int(value / scaling)