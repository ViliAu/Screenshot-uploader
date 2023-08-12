from screeninfo import get_monitors

screenshot_offset = (0,0)

def get_overlay_bounds():
    monitors = get_monitors()
    min_pos = [monitors[0].x, monitors[0].y]
    max_pos = [monitors[0].x + monitors[0].width, monitors[0].y + monitors[0].height]
    for monitor in monitors:
        min_pos[0] = min(min_pos[0], monitor.x)
        min_pos[1] = min(min_pos[1], monitor.y)
        max_pos[0] = max(max_pos[0], monitor.x + monitor.width)
        max_pos[1] = max(max_pos[1], monitor.y + monitor.height)
    global screenshot_offset
    screenshot_offset = (int(min_pos[0]), int(min_pos[1]))
    print(f"{max_pos[0]-min_pos[0]}x{max_pos[1]-min_pos[1]} + {min_pos[0]} + {min_pos[1]}")
    return f"{max_pos[0]-min_pos[0]}x{max_pos[1]-min_pos[1]}+{min_pos[0]}+{min_pos[1]}"

def get_screen_bounds(pos1, pos2):
    return (min(pos1[0], pos2[0]) + screenshot_offset[0], min(pos1[1], pos2[1]) + screenshot_offset[1],
            max(pos1[0], pos2[0]) + screenshot_offset[0], max(pos1[1], pos2[1]) + screenshot_offset[1])

def get_video_resolution(bounds):
    return (bounds[2]-bounds[0], bounds[3]-bounds[1])