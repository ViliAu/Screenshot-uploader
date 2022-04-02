import tkinter as tk

root = tk.Tk()

root.overrideredirect(True)
root.geometry("3883x1080")
root.call('wm', 'attributes', '.', '-topmost', '1')

root.mainloop()