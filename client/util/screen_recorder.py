import mss
import mss.tools
import cv2
import numpy
import time
import util.multi_monitor_util as mmu
import util.app_gui as gui

VIDEO_LENGTH = 10
FPS = 24
MIN_AREA_WIDTH = 8
COMPRESSION_LEVEL = 2 #The higher the lower compression

def take_screenshot(pos1, pos2):
    # Normalize area
    bounds = get_screen_bounds(pos1, pos2)
    # Check if the picture is too small
    if (bounds[2]-bounds[0] < MIN_AREA_WIDTH or bounds[3]-bounds[1] < MIN_AREA_WIDTH):
        return
    print(bounds)
    # Take pic from the area
    with mss.mss() as sct:
        img = sct.grab(bounds)
        mss.tools.to_png(img.rgb, img.size, output="Picture.png")

def record_frames(pos1, pos2, root):
    bounds = get_screen_bounds(pos1, pos2)
    # Check if the picture is too small
    if (bounds[2]-bounds[0] < MIN_AREA_WIDTH or bounds[3]-bounds[1] < MIN_AREA_WIDTH):
        return
    frames = []

    with mss.mss() as sct:
        sct.compression_level = COMPRESSION_LEVEL
        frame_start = time.perf_counter()
        start = time.perf_counter()
        # TODO More accurate frame counter
        while (frame_start < VIDEO_LENGTH + start):
            frames.append(numpy.array(sct.grab(bounds)))
            delta = time.perf_counter() - frame_start
            if (delta < float(1/FPS)):
                time.sleep(1/FPS-delta)
            frame_start = time.perf_counter()
    
    #return frames
    write_video(pos1, pos2, frames, root)

def write_video(pos1, pos2, frames, root):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    area = get_video_resolution(get_screen_bounds(pos1, pos2))
    print(f"{len(frames)/VIDEO_LENGTH} fps")
    video = cv2.VideoWriter("output.mp4v", fourcc, len(frames)/VIDEO_LENGTH, area)
    for frame in frames:
        video.write(frame)
    video.release()
    root.after(10, root.destroy) # TODO Workaround korjaa joskus

def get_screen_bounds(pos1, pos2):
    of = mmu.screenshot_offset
    return (min(pos1[0], pos2[0]) + of[0], min(pos1[1], pos2[1]) + of[1], max(pos1[0], pos2[0]) + of[0], max(pos1[1], pos2[1]) + of[1])

def get_video_resolution(bounds):
    return (bounds[2]-bounds[0], bounds[3]-bounds[1])