from screeninfo import get_monitors

screenshot_offset = (0,0)

def get_overlay_bounds():
    monitors = get_monitors()
    min_pos = [2000, 2000]
    max_pos = [-1, -1]
    for monitor in monitors:
        min_pos[0] = min(min_pos[0], monitor.x)
        min_pos[1] = min(min_pos[1], monitor.y)
        max_pos[0] = max(max_pos[0], monitor.x + monitor.width)
        max_pos[1] = max(max_pos[1], monitor.y + monitor.height)
    global screenshot_offset
    screenshot_offset = (int(min_pos[0]), int(min_pos[1]))
    print(f"{max_pos[0]-min_pos[0]}x{max_pos[1]-min_pos[1]} + {min_pos[0]} + {min_pos[1]}")
    return f"{max_pos[0]-min_pos[0]}x{max_pos[1]-min_pos[1]}+{min_pos[0]}+{min_pos[1]}"