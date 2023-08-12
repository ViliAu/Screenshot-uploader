import mss
import mss.tools
import cv2
import numpy
import time

from sclibrary.screen_util import get_screen_bounds
from sclibrary.settings import get_settings_data

MIN_AREA_WIDTH = 8
COMPRESSION_LEVEL = -1 #Higher = more compression

def take_screenshot(pos1, pos2):
    # Normalize area
    bounds = get_screen_bounds(pos1, pos2)
    # Check if the picture is too small
    if (bounds[2]-bounds[0] < MIN_AREA_WIDTH or bounds[3]-bounds[1] < MIN_AREA_WIDTH):
        return

    # Take pic from the area
    with mss.mss() as sct:
        img = sct.grab(bounds)
        return img

def record_frames(pos1, pos2):
    fps = int(get_settings_data()['VIDEO']['FramesPerSecond'])
    length = float(get_settings_data()['VIDEO']['VideoLength'])
    bounds = get_screen_bounds(pos1, pos2)
    # Check if the picture is too small
    if (bounds[2]-bounds[0] < MIN_AREA_WIDTH or bounds[3]-bounds[1] < MIN_AREA_WIDTH):
        return
    frames = []

    with mss.mss() as sct:
        # TODO Dynamical compression level
        sct.compression_level = COMPRESSION_LEVEL
        frame_start = time.perf_counter()
        start = time.perf_counter()
        # TODO More accurate frame counter
        while (frame_start < length + start):
            frames.append(numpy.array(sct.grab(bounds)))
            delta = time.perf_counter() - frame_start
            if (delta < float(1/fps)):
                time.sleep(1/fps-delta)
            frame_start = time.perf_counter()
    return frames