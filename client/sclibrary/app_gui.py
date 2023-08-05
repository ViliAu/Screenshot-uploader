# This class handles the grayed-out overlay which occurs when the program is started
#TODO rework => muuta classiks

import threading
import tkinter as tk
import sclibrary.screen_recorder as screen_recorder
import sclibrary.multi_monitor_util as multi_monitor_util
import sclibrary.settings as settings

ALPHACOLOR = "blue"
ALPHA = 0.3
OUTLINE = "white"
CURSOR = "crosshair"

shift_down = False
pos1 = -1, -1
pos2 = -1, -1
video = False
recording = False

def setup_overlay():
    global root
    global canvas
    root = tk.Tk()
    # Setups
    setup_overlay()
    setup_context_menu()
    apply_bindings(root)
    return root

# Setup the grayed-out overlay
def setup_overlay():
    root.configure(bg='blue')
    root.wm_attributes("-transparentcolor", ALPHACOLOR)
    enable_overlay(True)
    root.geometry(multi_monitor_util.get_overlay_bounds())
    root.wm_attributes('-topmost', 1)
    root.overrideredirect(True)
    # Canvas
    canvas = tk.Canvas(root, bg='black', highlightthickness=0, cursor=CURSOR)
    canvas.pack(fill='both', expand=True)

def setup_context_menu():
    # Setup context menu
    global cmenu
    cmenu = tk.Menu(root, tearoff=0)
    cmenu.add_command(label ="Settings", command=open_settings)
    cmenu.add_separator()
    cmenu.add_command(label ="Exit", command=close_program)

def track_bounds(event):
    if (not recording):
        if (pos1[0] > -1):
            canvas.delete("all")
            end = event.x, event.y
            canvas.create_rectangle(pos1 + end,  fill=ALPHACOLOR, outline=OUTLINE, width=2)

def click_start(event):
    global pos1
    pos1 = (event.x, event.y)

# Open context menu
def right_click(event):
    try:
        cmenu.tk_popup(event.x_root, event.y_root)
    finally:
        cmenu.grab_release()

def open_settings():
    enable_overlay(False)
    settings.open_settings(root)

def click_end(event):
    global pos2
    pos2 = (event.x, event.y)
    enable_overlay(False)
    screen_recorder.take_screenshot(pos1, pos2)
    close_program()

def click_end_video(event):
    global pos2
    pos2 = (event.x, event.y)
    canvas.configure(bg=ALPHACOLOR)
    #canvas.update_idletasks() # Workaround
    thread = threading.Thread(target=screen_recorder.record_frames, args=(pos1, pos2, root,))
    global recording
    recording = True
    thread.start() # TODO rework this shit
    #video_frames = screen_recorder.record_frames(pos1, pos2) # Täs on nyt bugi... tee tää toisel threadil nii alkaa homma toimimaa
    #screen_recorder.write_video(pos1, pos2, video_frames)
    #close_program()

def enable_overlay(enabled=True):
    root.attributes("-alpha", ALPHA if enabled else 0)

def close_program(event=None):
    root.destroy()

def apply_bindings(root: tk.Tk):
    root.bind('<Motion>', track_bounds)
    root.bind('<Button-1>', click_start)
    root.bind('<Button-3>', right_click)
    root.bind('<ButtonRelease-1>', click_end)
    root.bind('<Control-ButtonRelease-1>', click_end_video)
    root.bind('<Escape>', close_program)
