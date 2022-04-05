import util.app_gui as app_gui 

def init_root():
    # setup root
    root = app_gui.setup_overlay()
    # Start main loop
    root.mainloop()

if __name__ == '__main__':
    init_root()