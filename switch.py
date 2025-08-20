"""This app will remind you to switch tasks every once in a while. It also disables wifi to prevent
cheating."""

import time
import sys
import ctypes
import threading
import subprocess
import datetime
from windows_toasts import (
    InteractableWindowsToaster, Toast, ToastButton, ToastInputTextBox,
    ToastActivatedEventArgs, ToastInputSelectionBox, ToastSelection,
    ToastDuration
)
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# ======================
# ==== CONSTANTS =======
# ======================

# REMINDER_INTERVAL = 5  # seconds between reminders
# ANGER_THRESHOLD = 3    # reminders ignored before forced Wi-Fi disable
# DURATION_ON_ANGER = 1 * 10  # 40 minutes in seconds
# DURATION_ON_MANUAL = 1 * 10 # 20 minutes in seconds


NOTIFICATION_DURATION_NEUTRAL = 1200  # ms
NOTIFICATION_DURATION_ANGRY = 0 # ms
NOTIFICATION_DURATION_DISABLED = 2400  # ms


REMINDER_INTERVAL = 10  # seconds between reminders
ANGER_THRESHOLD = 10    # reminders ignored before forced Wi-Fi disable
DURATION_ON_ANGER = 40 * 60  # 40 minutes in seconds
DURATION_ON_MANUAL = 20 * 60 # 20 minutes in seconds



WIFI_INTERFACE_NAME = "Wi-Fi"  # Change if your Wi-Fi interface name is different


WIFI_LOOPING_TIME = 5


class TaskReminder:

    ############################
    # Variables and properties #
    ############################

    def __init__(self):
        self.toaster = InteractableWindowsToaster('Time to Switch!')
        self.running = True
        self.icon = None
        self.anger = 0
        self.wifi_disable_until = None  # datetime when Wi-Fi should be re-enabled
        self.lock = threading.Lock()

        self.reminder_thread = threading.Thread(target=self.send_reminder, daemon=True)
        self.wifi_thread = threading.Thread(target=self.wifi_manager_loop, daemon=True)


    @property
    def dynamic_text(self):
        """ Returns the text to be displayed in the notification """
        if self.anger == 0:
            return 'Time to Switch!'
        elif self.anger > 0:
            return 'Please do not ignore me!'
        else:
            return 'You have angered me! Internet disabled temporarily.'

    @property
    def dynamic_duration(self):
        """ Returns the duration of the notification """
        if self.anger == 0:
            return NOTIFICATION_DURATION_NEUTRAL
        elif self.anger > 0:
            return NOTIFICATION_DURATION_ANGRY
        else:
            return NOTIFICATION_DURATION_DISABLED

    ############################
    # Notification Methods     #
    ############################

    def activated_callback(self, butter: ToastActivatedEventArgs):
        "Actions to be taken when the toast is interacted with"
        # Butter is the activated toast
        print(butter.arguments, butter.inputs)

        if butter.arguments == 'submit' and butter.inputs["thing"] and self.anger >= 0:
            self.anger = 0
            # Reset anger and show user compliance
            print("User complied with task switch.")
        elif self.anger >= 0:
            # User did not comply, increase anger
            self.anger += 1
            print("User ignored task switch, increasing anger level.")
        else:
            # User did not comply while angered, anger is untouched
            print("Anger stays -1.")
            print(self.anger)

    def add_disable_time(self, seconds):
        with self.lock:
            now = time.time()
            if self.wifi_disable_until is None or now > self.wifi_disable_until:
                self.wifi_disable_until = now + seconds
                self.disable_wifi()
            else:
                self.wifi_disable_until += seconds
            print(f"Wi-Fi disabled until {datetime.datetime.fromtimestamp(self.wifi_disable_until).strftime('%H:%M:%S')}")


    def send_reminder(self):
        """ Continuously sends reminder notifications """
        new_toast = Toast(duration=ToastDuration.Long)
        new_toast.AddInput(ToastInputTextBox('thing', 'Next Thing', 'Do nothing at all xd'))
        new_toast.AddAction(ToastButton('Okay', 'submit'))
        new_toast.on_activated = self.activated_callback
        while self.running:
            if self.wifi_disable_until is None:
                print(self.anger)
                if self.anger >= ANGER_THRESHOLD:
                    self.anger = -1
                    self.add_disable_time(DURATION_ON_ANGER)

                new_toast.text_fields = [self.dynamic_text]
                self.toaster.show_toast(new_toast)
                time.sleep(REMINDER_INTERVAL)
                time.sleep(self.dynamic_duration)

    def wifi_manager_loop(self):
        """Monitor and re-enable Wi-Fi when time is up"""
        while self.running:
            with self.lock:
                if self.wifi_disable_until and time.time() > self.wifi_disable_until:
                    self.enable_wifi()
                    self.wifi_disable_until = None
            time.sleep(WIFI_LOOPING_TIME)

    ############################
    # System Tray Icon Methods #
    ############################

    def disable_wifi(self):
        try:
            subprocess.run(["netsh", "interface", "set", "interface", WIFI_INTERFACE_NAME, "admin=disable"], check=True)
            print("Wi-Fi disabled.")
        except subprocess.CalledProcessError as e:
            print("Error disabling Wi-Fi:", e)

    def enable_wifi(self):
        try:
            subprocess.run(["netsh", "interface", "set", "interface", WIFI_INTERFACE_NAME, "admin=enable"], check=True)
            print("Wi-Fi re-enabled.")
        except subprocess.CalledProcessError as e:
            print("Error enabling Wi-Fi:", e)

    def create_icon(self):
        """ Creates the tray icon """
        image = Image.new("RGB", (64, 64), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.ellipse((10, 10, 54, 54), fill=(0, 0, 255))
        return image

    def on_exit(self, icon):
        """ Stops the application """
        self.running = False
        icon.stop()

    def disable_wifi_temp(self):
        """Manually add 20 minutes of Wi-Fi disable"""
        self.add_disable_time(DURATION_ON_MANUAL)

    def disable_wifi_temp_long(self):
        """Manually add 1 hour of Wi-Fi disable"""
        self.add_disable_time(DURATION_ON_MANUAL*3)

    def run(self):
        self.reminder_thread.start()
        self.wifi_thread.start()
        self.menu_icon = Menu(
            MenuItem("Exit", self.on_exit),
            MenuItem("Disable Wifi (+20 min)", self.disable_wifi_temp),
            MenuItem("Disable Wifi (+1 hour)", self.disable_wifi_temp_long)
        )
        self.icon = Icon("Task Reminder", self.create_icon(), menu=self.menu_icon)
        self.icon.run()

def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("Requesting admin privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

if __name__ == "__main__":
    run_as_admin()

    app = TaskReminder()
    app.run()
    sys.exit()
