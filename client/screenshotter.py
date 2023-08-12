from tkinter import Tk

from sclibrary.app_gui import AppGui
#import util.keyboard_listener as key_listener 

#def init_listener():
#    key_listener.listen_keyboard()

def init_root():
    # setup root
    root = Tk()
    
    app_gui = AppGui(root)
    
    # Start main loop
    root.mainloop()

if __name__ == '__main__':
    init_root()
