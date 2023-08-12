
import configparser
import traceback
import os
import mss
import cv2

from sclibrary.screen_util import get_screen_bounds, get_video_resolution

SETTINGS_PATH = "./cfg/cfg.cfg"
IMAGE_PATH = "./media/images/"
VIDEO_PATH = "./media/videos/"

def read_settings() -> configparser.ConfigParser: 
    config = configparser.ConfigParser()
    config.read(SETTINGS_PATH)
    # Check if read is successful
    if len(config.sections()) == 0:
        # Read not successful (most likely to file not found => try to write file)
        config = assign_defaults()
        write_settings(config)
    return config

def assign_defaults():
    config = configparser.ConfigParser()
    config['VIDEO'] = {'FramesPerSecond': 24,
                    'VideoLength': 5,
                    'SaveLocalCopy': True}
    return config

# TODO: Throw error
def write_settings(config: configparser.ConfigParser):
    if config == None:
        print("No data passed!")
        return False
    
    if not os.path.exists(SETTINGS_PATH):
        os.makedirs(SETTINGS_PATH)
    try:
        with open(SETTINGS_PATH, "w") as cfgfile:
            config.write(cfgfile)
            return True
    except:
        traceback.print_exc()
        return False

# TODO Filename
def write_image(img):
    image_name = IMAGE_PATH + "Picture.png"
    if img == None:
        raise ValueError("No image data passed!")
    
    if not os.path.exists(VIDEO_PATH):
        os.makedirs(VIDEO_PATH)
    try:
        mss.tools.to_png(img.rgb, img.size, output=image_name)
        return image_name
    except:
        raise

# TODO Filename
def write_video(pos1, pos2, frames, length):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    area = get_video_resolution(get_screen_bounds(pos1, pos2))
    print(f"{len(frames)/length} fps")
    video_name = VIDEO_PATH  + "output.mp4v"
    video = cv2.VideoWriter(video_name, fourcc, len(frames)/length, area)

    if not os.path.exists(VIDEO_PATH):
        os.makedirs(VIDEO_PATH)
    try:
        for frame in frames:
            video.write(frame)
        return video_name
    except:
        raise
    finally:
        video.release