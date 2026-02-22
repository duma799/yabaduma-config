#!/usr/bin/env python3
import subprocess, json, ctypes, ctypes.util

cg = ctypes.cdll.LoadLibrary(ctypes.util.find_library("CoreGraphics"))
cg.CGDisplayIsBuiltin.argtypes = [ctypes.c_uint32]
cg.CGDisplayIsBuiltin.restype = ctypes.c_int32

displays = json.loads(subprocess.check_output(["yabai", "-m", "query", "--displays"]))
display_map = {d["index"]: d["id"] for d in displays}

spaces = json.loads(subprocess.check_output(["yabai", "-m", "query", "--spaces"]))
for space in spaces:
    display_id = display_map.get(space["display"], 0)
    is_builtin = cg.CGDisplayIsBuiltin(display_id) != 0
    top_padding = "10" if is_builtin else "47"
    subprocess.run(["yabai", "-m", "config", "--space", str(space["index"]), "top_padding", top_padding])
