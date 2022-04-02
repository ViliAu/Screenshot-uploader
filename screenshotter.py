import util.ss_overlay as ss_overlay 

def init_root():
    # setup root
    root = ss_overlay.setup_overlay()
    # Start main loop
    root.mainloop()

if __name__ == '__main__':
    init_root()