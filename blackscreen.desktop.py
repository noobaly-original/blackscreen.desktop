import os
import sys
import tkinter as tk

def get_resource_path(relative_path: str) -> str:
    """Resolve file path for normal python execution and PyInstaller bundles."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class BlackScreenDesktop:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Black Screen")

        # Set title bar / taskbar icon 🖼️
        icon_path = get_resource_path("app.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        # Color cycle palette
        self.colors = ["black", "white", "red", "green", "blue"]
        self.color_index = 0
        current_bg = self.colors[self.color_index]
        self.root.configure(bg=current_bg)

        # Subtle status indicator in the top-left corner 🏷️
        self.status_label = tk.Label(
            self.root,
            text="blackscreen.desktop is running !",
            font=("Segoe UI", 8),
            fg="#555555",
            bg=current_bg,
            bd=0,
            padx=4,
            pady=2
        )
        self.status_label.place(x=10, y=8)

        # Fullscreen state & cursor timer
        self.is_fullscreen = True
        self.root.attributes("-fullscreen", self.is_fullscreen)
        self.cursor_timer = None

        # Key & Mouse Bindings
        self.root.bind("<Double-Button-1>", self.toggle_fullscreen)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen_or_quit)
        self.root.bind("q", lambda e: self.root.destroy())
        self.root.bind("<space>", self.cycle_color)
        self.root.bind("<Motion>", self.on_mouse_activity)

        self.reset_cursor_timer()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        if not self.is_fullscreen:
            self.show_cursor()

    def exit_fullscreen_or_quit(self, event=None):
        if self.is_fullscreen:
            self.toggle_fullscreen()
        else:
            self.root.destroy()

    def cycle_color(self, event=None):
        self.color_index = (self.color_index + 1) % len(self.colors)
        new_color = self.colors[self.color_index]
        self.root.configure(bg=new_color)

        # Adjust label colors to stay readable against background shifts 🎨
        label_fg = "#222222" if new_color in ["white", "green"] else "#777777"
        self.status_label.configure(bg=new_color, fg=label_fg)

    def show_cursor(self):
        self.root.config(cursor="")

    def hide_cursor(self):
        if self.is_fullscreen:
            self.root.config(cursor="none")

    def on_mouse_activity(self, event=None):
        self.show_cursor()
        self.reset_cursor_timer()

    def reset_cursor_timer(self):
        if self.cursor_timer:
            self.root.after_cancel(self.cursor_timer)
        self.cursor_timer = self.root.after(2000, self.hide_cursor)


if __name__ == "__main__":
    root = tk.Tk()
    app = BlackScreenDesktop(root)
    root.mainloop()