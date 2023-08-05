import sclibrary.app_gui as app_gui 
#import util.keyboard_listener as key_listener 

#def init_listener():
#    key_listener.listen_keyboard()

def init_root():
    # setup root
    root = app_gui.setup_overlay()
    
    # Start main loop
    root.mainloop()

if __name__ == '__main__':
    init_root()
