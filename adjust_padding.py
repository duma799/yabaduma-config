#!/usr/bin/env python3
import subprocess, json

def get_top_padding(display):
    w = display["frame"]["w"]
    h = display["frame"]["h"]

    aspect_ratio = w / h if h > 0 else 1.0
    is_external = aspect_ratio > 1.65 or h in [1080, 1440, 2160, 2880]

    if is_external:
        return "14"
    else:
        return "4"

displays = json.loads(subprocess.check_output(["yabai", "-m", "query", "--displays"]))
spaces = json.loads(subprocess.check_output(["yabai", "-m", "query", "--spaces"]))

for space in spaces:
    disp = next((d for d in displays if d["index"] == space["display"]), None)
    if disp:
        pad = get_top_padding(disp)
        subprocess.run(["yabai", "-m", "config", "--space", str(space["index"]), "top_padding", pad])
