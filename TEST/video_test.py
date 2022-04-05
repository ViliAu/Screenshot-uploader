import mss
import mss.tools
import time
import imageio
from PIL import ImageGrab
import numpy
import cv2

GIF_TIME = 5
FRAME_RATE = 24
monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

video = cv2.VideoWriter("Testi_mp4.mp4v", 14, FRAME_RATE*2, (1920,1080))
with mss.mss() as sct:
    start = time.time()
    while (time.time() < GIF_TIME + start):
        video.write(numpy.array(sct.grab(monitor)))


print("Start!")
start = time.time()
video.release()
cv2.destroyAllWindows()
print(f"Done: {time.time()-start}")