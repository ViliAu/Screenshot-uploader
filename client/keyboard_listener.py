from pynput import keyboard

import screenshotter

def on_start():
    screenshotter.init_root()

def listen_keyboard():
    with keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+<cmd>+s': on_start
        }) as listener:
        listener.join()