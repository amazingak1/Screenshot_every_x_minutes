import pyautogui
import time
from datetime import datetime
import os
from winotify import Notification, audio

# Folder where screenshots will be saved
save_folder = "screenshots"
os.makedirs(save_folder, exist_ok=True)

# Interval in minutes
interval = 2  # change as needed

print(f"Starting screenshot capture every {interval} minutes...")
print("Press Ctrl + C to stop.\n")

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(save_folder, f"screenshot_{timestamp}.png")

        pyautogui.screenshot(filename)
        print(f"📸 Saved: {filename}")

        try:
            toast = Notification(app_id="Screenshot Taker",
                                 title="Screenshot Captured",
                                 msg=f"Saved: {filename}")
            toast.set_audio(audio.Default, loop=False)
            toast.show()
        except Exception as e:
            print(f"(Notification failed: {e})")

        time.sleep(interval * 60)

except KeyboardInterrupt:
    print("\nStopped capturing screenshots.")
#
