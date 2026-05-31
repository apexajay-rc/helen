import math
import threading
import tkinter as tk
from tkinter import ttk

from assistant import announce_capabilities, listen, route_command
from utils.events import set_event_listener


COLORS = {
    "bg": "#07111f",
    "panel": "#0d1b2d",
    "panel_alt": "#10243a",
    "text": "#f3f8ff",
    "muted": "#91a5bd",
    "line": "#1b3854",
    "idle": "#42d3a5",
    "listening": "#6ca8ff",
    "processing": "#f6c85f",
    "speaking": "#ce8cff",
}


class HelenUI:
    def __init__(self, root):
        self.root = root
        self.state = "idle"
        self.phase = 0.0
        self.busy = False
        self.status_text = tk.StringVar(value="Ready")
        self.transcript_text = tk.StringVar(
            value="Tap the microphone or choose a quick action."
        )
        self.command_text = tk.StringVar()

        self._configure_window()
        self._build_layout()
        set_event_listener(self._on_assistant_event)
        self._animate()
        self.root.after(550, lambda: self._run_background(announce_capabilities))

    def _configure_window(self):
        self.root.title("Helen | Multimodal AI Assistant")
        self.root.geometry("920x700")
        self.root.minsize(760, 620)
        self.root.configure(bg=COLORS["bg"])
        self.root.protocol("WM_DELETE_WINDOW", self._close)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Helen.TEntry",
            fieldbackground=COLORS["panel_alt"],
            foreground=COLORS["text"],
            insertcolor=COLORS["text"],
            bordercolor=COLORS["line"],
            padding=12,
        )

    def _build_layout(self):
        header = tk.Frame(self.root, bg=COLORS["bg"])
        header.pack(fill="x", padx=34, pady=(28, 0))

        tk.Label(
            header,
            text="HELEN",
            bg=COLORS["bg"],
            fg=COLORS["text"],
            font=("Segoe UI Semibold", 22),
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Multimodal accessibility assistant",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(2, 0))

        self.canvas = tk.Canvas(
            self.root,
            width=440,
            height=350,
            bg=COLORS["bg"],
            highlightthickness=0,
        )
        self.canvas.pack(pady=(10, 0))

        self.status_label = tk.Label(
            self.root,
            textvariable=self.status_text,
            bg=COLORS["bg"],
            fg=COLORS["idle"],
            font=("Segoe UI Semibold", 15),
        )
        self.status_label.pack()

        tk.Label(
            self.root,
            textvariable=self.transcript_text,
            wraplength=700,
            justify="center",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Segoe UI", 11),
        ).pack(padx=42, pady=(9, 12))

        action_bar = tk.Frame(self.root, bg=COLORS["bg"])
        action_bar.pack()
        self._button(action_bar, "Hear options", "help").pack(side="left", padx=5)
        self._button(action_bar, "Read text", "read text").pack(side="left", padx=5)
        self._button(action_bar, "Describe", "describe objects").pack(side="left", padx=5)
        self._button(action_bar, "Gesture music", "gesture music").pack(side="left", padx=5)

        tk.Label(
            self.root,
            text=(
                "ASK NATURALLY\n"
                "Read a document or label  |  Describe nearby objects  |  "
                "Search the web  |  Play music  |  Hear options"
            ),
            justify="center",
            bg=COLORS["panel"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
            padx=16,
            pady=10,
        ).pack(fill="x", padx=92, pady=(15, 0))

        command_bar = tk.Frame(self.root, bg=COLORS["bg"])
        command_bar.pack(fill="x", padx=92, pady=(14, 0))

        entry = ttk.Entry(
            command_bar,
            textvariable=self.command_text,
            style="Helen.TEntry",
            font=("Segoe UI", 11),
        )
        entry.pack(side="left", fill="x", expand=True)
        entry.bind("<Return>", lambda _: self._submit_text())

        self._button(command_bar, "Send", None, self._submit_text).pack(
            side="left", padx=(8, 0)
        )

        self.mic_button = tk.Button(
            self.root,
            text="Start listening",
            command=self._start_listening,
            bg=COLORS["listening"],
            fg="#061323",
            activebackground="#8bbcff",
            activeforeground="#061323",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI Semibold", 11),
            padx=22,
            pady=12,
        )
        self.mic_button.pack(pady=(18, 26))

    def _button(self, parent, label, command_text=None, command=None):
        callback = command or (lambda: self._run_command(command_text))
        return tk.Button(
            parent,
            text=label,
            command=callback,
            bg=COLORS["panel_alt"],
            fg=COLORS["text"],
            activebackground=COLORS["line"],
            activeforeground=COLORS["text"],
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10),
            padx=14,
            pady=9,
        )

    def _animate(self):
        self.canvas.delete("all")
        center_x, center_y = 220, 172
        color = COLORS.get(self.state, COLORS["idle"])
        motion = 1 if self.state == "idle" else 2.6

        for index in range(4, 0, -1):
            wave = math.sin(self.phase * motion + index * 0.72)
            radius = 74 + index * 20 + wave * (4 + index * 2)
            shade = self._blend(color, COLORS["bg"], 0.28 + index * 0.12)
            self.canvas.create_oval(
                center_x - radius,
                center_y - radius,
                center_x + radius,
                center_y + radius,
                outline=shade,
                width=2,
            )

        orb_radius = 66 + math.sin(self.phase * motion) * (
            3 if self.state == "idle" else 8
        )
        self.canvas.create_oval(
            center_x - orb_radius,
            center_y - orb_radius,
            center_x + orb_radius,
            center_y + orb_radius,
            fill=color,
            outline=self._blend(color, "#ffffff", 0.28),
            width=3,
        )
        self.canvas.create_text(
            center_x,
            center_y - 3,
            text="HELEN",
            fill="#061323",
            font=("Segoe UI Semibold", 16),
        )
        self.canvas.create_text(
            center_x,
            center_y + 22,
            text=self.state.upper(),
            fill="#16334a",
            font=("Segoe UI Semibold", 8),
        )

        self.phase += 0.09
        self.root.after(34, self._animate)

    @staticmethod
    def _blend(first, second, amount):
        first_rgb = tuple(int(first[i : i + 2], 16) for i in (1, 3, 5))
        second_rgb = tuple(int(second[i : i + 2], 16) for i in (1, 3, 5))
        mixed = tuple(
            int(a + (b - a) * amount) for a, b in zip(first_rgb, second_rgb)
        )
        return "#{:02x}{:02x}{:02x}".format(*mixed)

    def _set_state(self, state, message):
        self.state = state
        self.status_text.set("Options" if state == "guide" else state.title())
        self.status_label.configure(fg=COLORS.get(state, COLORS["idle"]))
        if message:
            self.transcript_text.set(message)

    def _on_assistant_event(self, state, message):
        self.root.after(0, self._set_state, state, message)

    def _start_listening(self):
        if self.busy:
            return
        self._run_background(self._listen_and_route)

    def _listen_and_route(self):
        command = listen()
        if command:
            route_command(command)

    def _submit_text(self):
        command = self.command_text.get().strip()
        if not command:
            return
        self.command_text.set("")
        self._run_command(command)

    def _run_command(self, command):
        if self.busy or not command:
            return
        self._run_background(lambda: route_command(command))

    def _run_background(self, operation):
        if self.busy:
            return
        self.busy = True
        self.mic_button.configure(state="disabled", text="Working...")

        def worker():
            try:
                operation()
            except KeyboardInterrupt:
                self.root.after(0, self._close)
            except Exception as error:
                self.root.after(
                    0,
                    self._set_state,
                    "idle",
                    f"Something went wrong: {error}",
                )
            finally:
                self.root.after(0, self._finish_operation)

        threading.Thread(target=worker, daemon=True).start()

    def _finish_operation(self):
        self.busy = False
        self.mic_button.configure(state="normal", text="Start listening")
        if self.state != "speaking":
            self._set_state("idle", self.transcript_text.get())

    def _close(self):
        set_event_listener(None)
        self.root.destroy()


def main():
    root = tk.Tk()
    HelenUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
