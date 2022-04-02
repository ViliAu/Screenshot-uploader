import mss
import mss.tools
import tkinter as tk
from screeninfo import get_monitors

ALPHACOLOR = "blue"
ALPHA = 0.3
OUTLINE = "white"

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
    bounds = (min(pos1[0], pos2[0]), min(pos1[1], pos2[1]), max(pos1[0], pos2[0]), max(pos1[1], pos2[1]))
    img = mss.mss().grab(bounds)
    mss.tools.to_png(img.rgb, img.size, output="Jere.png")
    close_program()

def close_program(event=None):
    root.destroy()


def init_window():
    # Create window
    global root
    global canvas
    root = tk.Tk()

    # Setup window
    root.configure(bg='blue')
    root.wm_attributes("-transparentcolor", ALPHACOLOR)
    root.wm_attributes("-alpha", ALPHA)

    root.geometry("3883x1080+-1920+0") #TODO Remove hard coded dimensions, detect main screen etc etc

    root.wm_attributes('-topmost', 1)
    root.overrideredirect(True)

    # Canvas
    canvas = tk.Canvas(root, bg='black', highlightthickness=0, cursor="tcross")
    canvas.pack(fill='both', expand=True)

    # Apply bindings
    apply_bindings()

    # Start main loop
    root.mainloop()


def apply_bindings():
    root.bind('<Motion>', track_bounds)
    root.bind('<Button-1>', click_start)
    root.bind('<ButtonRelease-1>', click_end)
    root.bind('<Escape>', close_program)

if __name__ == '__main__':
    init_window()