# This class handles the grayed-out overlay which occurs when the program is started

import tkinter as tk
import util.screen_recorder as screen_recorder
import util.multi_monitor_util as multi_monitor_util

ALPHACOLOR = "blue"
ALPHA = 0.3
OUTLINE = "white"
CURSOR = "tcross"

shift_down = False
pos1 = -1, -1
pos2 = -1, -1

def track_bounds(event):
    if (pos1[0] > -1):
        canvas.delete("all")
        end = event.x, event.y
        canvas.create_rectangle(pos1 + end,  fill=ALPHACOLOR, outline=OUTLINE, width=2)
    

def click_start(event):
    global pos1
    pos1 = (event.x, event.y)

def click_end(event):
    global pos2
    pos2 = (event.x, event.y)
    print(pos1, pos2)
    root.attributes('-alpha', 0)
    screen_recorder.take_screenshot(pos1, pos2)
    close_program()

def close_program(event=None):
    root.destroy()

def setup_overlay():
    global root
    global canvas
    root = tk.Tk()

    # Setup window
    root.configure(bg='blue')
    root.wm_attributes("-transparentcolor", ALPHACOLOR)
    root.wm_attributes("-alpha", ALPHA)
    root.geometry(multi_monitor_util.get_overlay_bounds())
    root.wm_attributes('-topmost', 1)
    root.overrideredirect(True)

    # Canvas
    canvas = tk.Canvas(root, bg='black', highlightthickness=0, cursor=CURSOR)
    canvas.pack(fill='both', expand=True)

    # Apply bindings
    apply_bindings(root)

    return root

def apply_bindings(root: tk.Tk):
    root.bind('<Motion>', track_bounds)
    root.bind('<Button-1>', click_start)
    root.bind('<ButtonRelease-1>', click_end)
    root.bind('<Escape>', close_program)