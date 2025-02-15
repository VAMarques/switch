import time
import sys
import threading
from windows_toasts import (
    InteractableWindowsToaster, Toast, ToastButton, ToastInputTextBox,
    ToastActivatedEventArgs, ToastInputSelectionBox, ToastSelection,
    ToastDuration
)
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

def activated_callback(activatedEventArgs: ToastActivatedEventArgs):
    print(activatedEventArgs.inputs)

def send_reminder():
    interactable_toaster = InteractableWindowsToaster('Time to Switch!')
    new_toast = Toast(duration=ToastDuration.Long)
    new_toast.text_fields = ['Time to Switch!']
    new_toast.AddInput(ToastInputTextBox('thing', 'Next Thing', 'Do nothing at all xd'))
    new_toast.AddAction(ToastButton('Okay', 'submit'))
    new_toast.on_activated = activated_callback
    while True:
        interactable_toaster.show_toast(new_toast)
        time.sleep(1200)  # Wait for 20 minutes

def create_icon():
    image = Image.new("RGB", (64, 64), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.ellipse((10, 10, 54, 54), fill=(0, 0, 255))
    return image

def on_exit(icon, item):
    icon.stop()

def main():
    reminder_thread = threading.Thread(target=send_reminder, daemon=True)
    reminder_thread.start()
    icon = Icon("Task Reminder", create_icon(), menu=Menu(MenuItem("Exit", on_exit)))
    icon.run()

if __name__ == "__main__":
    main()
    sys.exit()
