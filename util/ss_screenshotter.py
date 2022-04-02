import mss
import mss.tools
import util.ss_multi_monitor_util as mmu

def take_screenshot(pos1, pos2):
    of = mmu.screenshot_offset
    # Normalize area
    bounds = (min(pos1[0], pos2[0]) + of[0], min(pos1[1], pos2[1]) + of[1], max(pos1[0], pos2[0]) + of[0], max(pos1[1], pos2[1]) + of[1])

    print(bounds)

    # Take pic from the area
    with mss.mss() as pic:
        img = pic.grab(bounds)
        mss.tools.to_png(img.rgb, img.size, output="Picture.png")

