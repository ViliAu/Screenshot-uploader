import threading

from sclibrary.screen_recorder import record_frames
from sclibrary.file_writer import write_video
from sclibrary.settings import get_settings_data
import traceback

print_lock = threading.Lock()
settings_lock = threading.Lock()
class ScreenRecorderWorker(threading.Thread):
    def __init__(self, on_success=lambda: None, on_error=lambda: None, pos1=(100, 100), pos2=(200, 200)):
        threading.Thread.__init__(self)
        self.threadID = 1337
        self.name = "RecorderThread"
        self.daemon = True
        self.pos1=pos1
        self.pos2=pos2
        self.on_success = on_success
        self.on_error = on_error

    def run(self):
        with print_lock:
            print("Starting", self.name, self.threadID)
        try:
            frames = record_frames(pos1=self.pos1, pos2=self.pos2)
            self.on_success(frames)
        except:
            self.on_error("Error while recording:", traceback.format_exc())
        finally:
            with print_lock:
                print("Exiting " + self.name)
        

class VideoWriterWorker(threading.Thread):
    def __init__(self, on_success=lambda: None, on_error=lambda: None, pos1=(100, 100), pos2=(200, 200), frames=[]):
        threading.Thread.__init__(self)
        self.threadID = 557
        self.name = "RecorderThread"
        self.daemon = True
        self.pos1=pos1
        self.pos2=pos2
        self.frames = frames
        self.on_success = on_success
        self.on_error = on_error

    def run(self):
        with print_lock:
            print("Starting", self.name, self.threadID)
        try:
            with settings_lock:
                length = float(get_settings_data()['VIDEO']['VideoLength'])

            video_name = write_video(self.pos1, self.pos2, self.frames, length)
            self.on_success(video_name)
        except:
            self.on_error("Error while saving video: ", traceback.format_exc())
        finally:
            with print_lock:
                print("Exiting " + self.name)
        

class GeneralWorker(threading.Thread):
    def __init__(self, executable=lambda: None, on_success=lambda: None, on_error=lambda: None, daemon=True, **kwargs):
        threading.Thread.__init__(self)
        self.threadID = 1234
        self.name = "GeneralThread"
        self.daemon = daemon
        self.executable = executable
        self.args = kwargs.get('args') if kwargs.get('args') else ()
        self.on_success = on_success
        self.on_error = on_error

    def run(self):
        with print_lock:
            print("Starting", self.name, self.threadID)
        print(self.args)
        try:
            self.executable(*self.args)
            self.on_success()
        except:
            self.on_error(traceback.format_exc())
        finally:
            with print_lock:
                print("Exiting " + self.name)