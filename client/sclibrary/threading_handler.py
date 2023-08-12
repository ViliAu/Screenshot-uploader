import threading

from sclibrary.screen_recorder import record_frames
from sclibrary.file_writer import write_video
from sclibrary.settings import get_settings_data

print_lock = threading.Lock()
settings_lock = threading.Lock()
class ScreenRecorderWorker(threading.Thread):
    def __init__(self, callback=lambda: None, pos1=(100, 100), pos2=(200, 200)):
        threading.Thread.__init__(self)
        self.threadID = 1337
        self.name = "RecorderThread"
        self.callback = callback
        self.daemon = True
        self.pos1=pos1
        self.pos2=pos2

    def run(self):
        with print_lock:
            print("Starting", self.name, self.threadID)
        frames = record_frames(pos1=self.pos1, pos2=self.pos2)
        with print_lock:
            print("Exiting " + self.name)
        self.callback(frames)

class VideoWriterWorker(threading.Thread):
    def __init__(self, callback=lambda: None, pos1=(100, 100), pos2=(200, 200), frames=[]):
        threading.Thread.__init__(self)
        self.threadID = 557
        self.name = "RecorderThread"
        self.callback = callback
        self.daemon = True
        self.pos1=pos1
        self.pos2=pos2
        self.frames = frames

    def run(self):
        with print_lock:
            print("Starting", self.name, self.threadID)

        with settings_lock:
            length = float(get_settings_data()['VIDEO']['VideoLength'])

        video_name = write_video(self.pos1, self.pos2, self.frames, length)
        with print_lock:
            print("Exiting " + self.name)
        self.callback(video_name)

class GeneralWorker(threading.Thread):
    def __init__(self, executable=lambda: None, callback=lambda: None, daemon=True, *args):
        threading.Thread.__init__(self)
        self.threadID = 666
        self.name = "GeneralThread"
        self.daemon = daemon
        self.executable = executable
        self.args = args
        self.callback = callback

    def run(self):
        with print_lock:
            print("Starting", self.name, self.threadID)
        self.executable(*self.args)
        with print_lock:
            print("Exiting " + self.name)
        self.callback