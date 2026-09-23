import os
import sys
import threading
import tkinter as tk
from PIL import Image, ImageDraw
import pystray


def get_resource_path(relative_path: str) -> str:
    """Resolve file path for normal python execution and PyInstaller bundles."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class BlackScreenDesktop:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Black Screen")

        # Resolve icon path
        self.icon_path = get_resource_path("app.ico")
        if os.path.exists(self.icon_path):
            try:
                self.root.iconbitmap(self.icon_path)
            except Exception:
                pass

        # Color cycle palette
        self.colors = ["black", "white", "red", "green", "blue"]
        self.color_index = 0
        current_bg = self.colors[self.color_index]
        self.root.configure(bg=current_bg)

        # Subtle status indicator
        self.status_label = tk.Label(
            self.root,
            text="blackscreen.desktop is running !",
            font=("Segoe UI", 8),
            fg="#555555",
            bg=current_bg,
            bd=0,
            padx=4,
            pady=2,
        )
        self.status_label.place(x=10, y=8)

        # Fullscreen state & cursor timer
        self.is_fullscreen = True
        self.root.attributes("-fullscreen", self.is_fullscreen)
        self.cursor_timer = None

        # System tray attributes
        self.tray_icon = None

        # Intercept window close protocols (X button and keyboard triggers)
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        self.root.bind("<Double-Button-1>", self.toggle_fullscreen)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen_or_tray)
        self.root.bind("q", lambda e: self.minimize_to_tray())
        self.root.bind("<space>", self.cycle_color)
        self.root.bind("<Motion>", self.on_mouse_activity)

        self.reset_cursor_timer()

    def create_tray_image(self):
        """Loads app.ico if available, otherwise generates a fallback icon."""
        if os.path.exists(self.icon_path):
            try:
                return Image.open(self.icon_path)
            except Exception:
                pass
        # Fallback dark icon 🎨
        img = Image.new("RGB", (64, 64), color="#1e1e1e")
        draw = ImageDraw.Draw(img)
        draw.rectangle([16, 16, 48, 48], fill="#3a3a3a")
        return img

    def minimize_to_tray(self):
        """Hides the window, starts the system tray icon, and displays a notification."""
        self.root.withdraw()

        if self.tray_icon is None:
            image = self.create_tray_image()
            menu = pystray.Menu(
                pystray.MenuItem("Show Black Screen", self.restore_from_tray, default=True),
                pystray.MenuItem("Exit", self.quit_completely),
            )
            self.tray_icon = pystray.Icon("BlackScreen", image, "Black Screen", menu)
            threading.Thread(target=self.tray_icon.run, daemon=True).start()

        # Send tray notification 📣
        self.tray_icon.notify(
            "Blackscreen is now in your system tray !",
            title="Black Screen",
        )

    def restore_from_tray(self, icon=None, item=None):
        """Restores the window from the tray."""
        if self.tray_icon:
            self.tray_icon.stop()
            self.tray_icon = None

        # Thread-safe UI update
        self.root.after(0, self._restore_ui)

    def _restore_ui(self):
        self.root.deiconify()
        if self.is_fullscreen:
            self.root.attributes("-fullscreen", True)
        self.root.lift()
        self.root.focus_force()

    def quit_completely(self, icon=None, item=None):
        """Stops tray icon and destroys Tkinter app cleanly."""
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.after(0, self.root.destroy)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        if not self.is_fullscreen:
            self.show_cursor()

    def exit_fullscreen_or_tray(self, event=None):
        if self.is_fullscreen:
            self.toggle_fullscreen()
        else:
            self.minimize_to_tray()

    def cycle_color(self, event=None):
        self.color_index = (self.color_index + 1) % len(self.colors)
        new_color = self.colors[self.color_index]
        self.root.configure(bg=new_color)

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