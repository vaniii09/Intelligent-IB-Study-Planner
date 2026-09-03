import tkinter as tk


class ScrollableFrame(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent, bg="white")

        self.canvas = tk.Canvas(
            self,
            bg="white",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg="white"
        )

        self.window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.scrollable_frame.bind(
            "<Configure>",
            self.on_frame_configure
        )

        self.canvas.bind(
            "<Configure>",
            self.on_canvas_configure
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Mouse wheel only works while cursor is inside
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    # -----------------------------

    def on_frame_configure(self, event):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # -----------------------------

    def on_canvas_configure(self, event):

        self.canvas.itemconfig(
            self.window,
            width=event.width
        )

    # -----------------------------

    def _bind_mousewheel(self, event):

        self.canvas.bind_all(
            "<MouseWheel>",
            self._on_mousewheel
        )

    # -----------------------------

    def _unbind_mousewheel(self, event):

        self.canvas.unbind_all("<MouseWheel>")

    # -----------------------------

    def _on_mousewheel(self, event):

        if self.canvas.winfo_exists():

            self.canvas.yview_scroll(
                int(-event.delta / 120),
                "units"
            )