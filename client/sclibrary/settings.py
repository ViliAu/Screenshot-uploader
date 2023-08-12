
import tkinter as tk
import traceback
from tkinter import ttk
from tkinter import messagebox

from sclibrary.file_writer import write_settings, read_settings

settings_data = None

class Settings:
    def __init__(self, app_gui):
        self.app_gui = app_gui
        self.window = tk.Toplevel(self.app_gui.master)
        self.window.geometry("300x100")
        self.window.title("Settings")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        load_settings()
        self.set_vars()
        self.set_vars()
        self.setup_window_layout()

    def set_vars(self):
        self.int_fps = tk.IntVar()
        self.double_len = tk.DoubleVar()

        self.int_fps.set(settings_data['VIDEO']['FramesPerSecond'])
        self.double_len.set(settings_data['VIDEO']['VideoLength'])

        # Assign callbacks



    def setup_window_layout(self):        
        # Declare elements
        lbl_fps = ttk.Label(self.window, text="Frames per second")
        lbl_len = ttk.Label(self.window, text="Video length")
        s_fps = tk.Scale(self.window, bg='white', fg='white', 
                         variable=self.int_fps, orient="horizontal", 
                         from_=1, to=24, resolution=1, showvalue=0)
        s_len = tk.Scale(self.window, bg='white', fg='white', 
                         variable=self.double_len, orient="horizontal",
                         from_=0.1, to=10.0, resolution=0.1, showvalue=0)

        en_fps = ttk.Entry(self.window, textvariable=self.int_fps, width=2)
        en_len = ttk.Entry(self.window, textvariable=self.double_len, width=4)
        
        btn_exit = tk.Button(self.window, text="Exit", command=self.on_closing)

        # Position elements
        lbl_fps.grid(row=0, column=0)
        s_fps.grid(row=0, column=1)
        en_fps.grid(row=0, column=2)

        lbl_len.grid(row=1, column=0)
        s_len.grid(row=1, column=1)
        en_len.grid(row=1, column=2)

        btn_exit.grid(row=2, column=1)
    
    def on_closing(self):
        settings_data['VIDEO']['FramesPerSecond'] = str(self.int_fps.get())
        settings_data['VIDEO']['VideoLength'] = str(self.double_len.get())
        try:
            save_settings()
        except:
            messagebox.showerror('Error', 'Unable to save settings: ' + traceback.format_exc())
        finally:
            self.app_gui.enable_overlay(True)
            self.window.destroy()

def get_settings_data():
    global settings_data
    if settings_data == None:
        load_settings()
    return settings_data

def load_settings():
    global settings_data
    settings_data = read_settings()

def save_settings():
    write_settings(settings_data)
