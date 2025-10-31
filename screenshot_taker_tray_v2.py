import pyautogui
import time
from datetime import datetime
import os
import threading
from PIL import Image, ImageDraw
import pystray
import webbrowser
import tkinter as tk
from tkinter import simpledialog

# === SETTINGS ===
INTERVAL_MIN = 2
SAVE_FOLDER = "screenshots"
os.makedirs(SAVE_FOLDER, exist_ok=True)

running = True
stopped = False

# === SCREENSHOT LOOP ===
def screenshot_loop():
    global running, stopped, INTERVAL_MIN
    while not stopped:
        if running:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(SAVE_FOLDER, f"screenshot_{timestamp}.png")
            pyautogui.screenshot(filename)
            print(f"📸 Saved: {filename}")
        for _ in range(INTERVAL_MIN * 60):
            if stopped:
                break
            time.sleep(1)

# === TRAY ICON SETUP ===
def create_image():
    """Create a small blue circle icon for tray"""
    image = Image.new("RGB", (64, 64), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill=(80, 150, 255))
    return image

def on_open_folder(icon, item):
    webbrowser.open(os.path.abspath(SAVE_FOLDER))

def on_pause_resume(icon, item):
    global running
    running = not running
    item.text = "▶ Resume" if not running else "⏸ Pause"

def on_change_interval(icon, item):
    global INTERVAL_MIN
    # Use tkinter popup for input
    root = tk.Tk()
    root.withdraw()
    try:
        new_val = simpledialog.askinteger(
            "Change Interval",
            "Enter new interval in minutes:",
            minvalue=1,
            maxvalue=120
        )
        if new_val:
            INTERVAL_MIN = new_val
            print(f"⏱ Interval changed to {INTERVAL_MIN} minutes")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        root.destroy()

def on_exit(icon, item):
    global stopped
    stopped = True
    icon.stop()

def setup_tray():
    icon = pystray.Icon(
        "Screenshot Taker",
        create_image(),
        "Screenshot Taker",
        menu=pystray.Menu(
            pystray.MenuItem("📁 Open Folder", on_open_folder),
            pystray.MenuItem("⏱ Change Interval", on_change_interval),
            pystray.MenuItem("⏸ Pause", on_pause_resume),
            pystray.MenuItem("❌ Exit", on_exit)
        )
    )
    threading.Thread(target=screenshot_loop, daemon=True).start()
    icon.run()

if __name__ == "__main__":
    setup_tray()
