# This class handles the grayed-out overlay which occurs when the program is started

import threading
import traceback
import tkinter as tk
import time
from tkinter import ttk
from tkinter import messagebox

import sclibrary.screen_recorder as screen_recorder
import sclibrary.screen_util as screen_util
from sclibrary.settings import Settings, get_settings_data
from sclibrary.threading_handler import ScreenRecorderWorker, VideoWriterWorker, GeneralWorker
from sclibrary.file_writer import write_image, write_video

class AppGui:

    ALPHACOLOR = "blue"
    ALPHA = 0.3
    OUTLINE_COLOR_PHOTO = "white"
    OUTLINE_COLOR_VIDEO = "red"
    CURSOR = "crosshair"

    def __init__(self, master):
        self.video_mode = False # Whether we're recording on release or not
        self.recording = False
        self.pos1 = -1, -1
        self.pos2 = -1, -1
        
        self.master = master
        self.setup_overlay()
        self.setup_context_menu()
        self.apply_bindings()

    # Setup the grayed-out overlay
    def setup_overlay(self):
        self.master.configure(bg='blue')
        self.master.wm_attributes("-transparentcolor", self.ALPHACOLOR)
        self.enable_overlay(True)
        self.master.geometry(screen_util.get_overlay_bounds())
        self.master.wm_attributes('-topmost', 1)
        self.master.overrideredirect(True)
        # Canvas
        self.canvas = tk.Canvas(self.master, bg='black', highlightthickness=0, cursor=self.CURSOR)
        self.canvas.pack(fill='both', expand=True)
        self.rectangle = self.canvas.create_rectangle((0,0,0,0), fill=self.ALPHACOLOR, outline="white", width=2)

    def setup_context_menu(self):
        # Setup context menu
        self.cmenu = tk.Menu(self.master, tearoff=0)
        self.cmenu.add_command(label ="Settings", command=self.open_settings)
        self.cmenu.add_separator()
        self.cmenu.add_command(label ="Exit", command=self.close_program)

    # TODO Broaden the rectangle to remove outline from frame
    def track_bounds(self, event):
        if (not self.recording):
            if (self.pos1[0] > -1):
                end = (event.x, event.y)
                self.canvas.coords(self.rectangle, self.pos1 + end)

    def click_start(self, event):
        self.pos1 = (event.x, event.y)

    # Open context menu
    def right_click(self, event):
        if (self.pos1[0] > -1):
            return
        try:
            self.cmenu.tk_popup(event.x_root, event.y_root)
        finally:
            self.cmenu.grab_release()

    def open_settings(self):
        self.enable_overlay(False)
        settings = Settings(self)

    def click_end(self, event):
        if not self.video_mode:
            self.setup_image(event)
        else:
            self.setup_video(event)

    def setup_image(self, event):
        self.pos2 = (event.x, event.y)
        self.enable_overlay(False)
        img = screen_recorder.take_screenshot(self.pos1, self.pos2)
        try:
            write_image(img=img)
        except Exception:
            messagebox.showerror('Error', 'Unable to save image: ' + traceback.format_exc())
        finally:
            self.close_program()

    def setup_video(self, event):
        self.pos2 = (event.x, event.y)
        self.canvas.configure(bg=self.ALPHACOLOR)
        self.recording = True
        self.frames = []
        self.canvas.config(cursor="arrow")
        video_thread = ScreenRecorderWorker(callback=self.handle_video, pos1=self.pos1, pos2=self.pos2)
        progress_bar_thread = GeneralWorker(executable=self.update_progress_bar)
        video_thread.start()
        progress_bar_thread.start()

    def update_progress_bar(self):
        self.bar = ttk.Progressbar(self.master, orient='horizontal', length=200, mode='determinate')
        bar_x = (self.pos1[0] + self.pos2[0]) * 0.5 - 100
        bar_y = max(self.pos1[1], self.pos2[1]) + 10
        self.bar.place(x=bar_x, y=bar_y)

        start = time.perf_counter()
        current = time.perf_counter()
        length = float(get_settings_data()['VIDEO']['VideoLength'])
        while current < start + length:
            self.bar['value'] = float((current - start) / length) * 100
            current = time.perf_counter()
        self.bar.destroy()

    # TODO Error handling (on_success, on_exception callbacks)
    def handle_video(self, frames):
        self.canvas.delete("all")
        thread = VideoWriterWorker(callback=self.handle_upload, pos1=self.pos1, pos2=self.pos2, frames=frames)
        thread.start()
    
    def handle_upload(self, video_name):
        print(video_name)
        self.close_program()

    def on_error(self):
        messagebox.showerror('Error', traceback.format_exc())
        self.close_program()

    def enable_overlay(self, enabled=True):
        self.master.attributes("-alpha", self.ALPHA if enabled else 0)

    def enable_video(self, event, enabled):
        if self.recording:
            return
        color = self.OUTLINE_COLOR_VIDEO if enabled else self.OUTLINE_COLOR_PHOTO
        self.canvas.itemconfig(self.rectangle, outline=color)
        self.video_mode = enabled

    def close_program(self, event=None):
        self.master.quit()
        self.master.destroy()

    def apply_bindings(self):
        self.master.bind('<Motion>', self.track_bounds)
        self.master.bind('<Button-1>', self.click_start)
        self.master.bind('<Button-3>', self.right_click)
        self.master.bind('<ButtonRelease-1>', self.click_end)
        self.master.bind('<KeyPress-Control_L>', lambda x: self.enable_video(x, True))
        self.master.bind('<KeyRelease-Control_L>', lambda x: self.enable_video(x, False))
        self.master.bind('<Escape>', self.close_program)
