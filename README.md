# Black Screen Desktop 🖥️

A lightweight, distraction-free desktop utility inspired by and modeled after the minimalist web tool [blackscreen.app](https://blackscreen.app/).

Useful for deep focus, OLED power saving, monitor cleaning, or stuck/dead pixel testing.

---

## Inspiration 💡

This project was directly inspired by **[blackscreen.app](https://blackscreen.app/)**, an elegant, single-purpose web application by Kevin Py that provides a quick fullscreen black canvas at the double-click of a mouse. This desktop port brings that exact zero-friction utility to an offline, standalone native binary with system-level hotkeys and color cycling diagnostics. 🚀

---

## Features 🌟

* **Auto-Hiding Cursor:** Seamlessly hides the cursor after 2 seconds of inactivity while in fullscreen.
* **Diagnostic Color Cycling:** Cycle between black, white, and primary RGB screens using the spacebar.
* **Diagnostic Color Cycling:** Cycle between black, white, and primary RGB screens using the spacebar.
* **Discrete Running Indicator:** Features a subtle status label in the top-left corner reminding you the utility is active without breaking immersion.
* **Portable Ready:** Easily compile into a standalone `.exe` or macOS binary with PyInstaller.
* **System Tray:** When the app is closed it exits into system tray using "pystray" (You can right-click to exit completely in the system tray.)

---

## Keyboard & Mouse Shortcuts 🎮

| Input | Action |
| :--- | :--- |
| **Double Left-Click** | Toggle Fullscreen (matches web behavior) |
| **`F11`** | Toggle Fullscreen |
| **`Space`** | Cycle background colors (`Black` ➔ `White` ➔ `Red` ➔ `Green` ➔ `Blue`) |
| **`Esc`** | Exit fullscreen mode (press again to close application) |
| **`Q`** | Quit application immediately |

---

## Getting Started

### Prerequisites

* Python 3.8 or higher installed on your machine.

### Running from Source

Clone the repository and run the script directly:

```bash
gh repo clone noobaly-original/blackscreen.desktop
cd blackscreen.desktop
python blackscreen.desktop.py
```

---

## Building a Standalone Executable 📦

To bundle the application into a single portable binary without requiring a local Python installation:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Package the app:

   * **Windows:**
     ```bash
     pyinstaller --noconsole --onefile --icon=app.ico --add-data "app.ico;." blackscreen.desktop.py
     ```

   * **macOS / Linux:**
     ```bash
     pyinstaller --noconsole --onefile --icon=app.icns --add-data "app.ico:." blackscreen.desktop.py
     ```

3. Find the compiled executable inside the generated `dist/` directory.

Note: You should convert the app.ico into a app.icns file for Mac/Linux. Many online tools can be used for this purpose.

---

## Credits & Attribution 🙏

* **Project Inspiration:** Inspired by the [blackscreen.app](https://blackscreen.app/) web tool created by Kevin Py.
* **Application Icon:** [Favorites Icon from the "My Seven Icons" set by itzikgur](https://www.iconarchive.com/show/my-seven-icons-by-itzikgur/Favorities-icon.html), hosted on IconArchive.

---

## License

This project is open source and available under the [MIT License](LICENSE).
