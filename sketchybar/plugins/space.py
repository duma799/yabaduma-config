#!/usr/bin/env python3

import json
import os
import subprocess
from pathlib import Path

COLORS_FILE = Path.home() / ".cache" / "wal" / "colors.json"
TOTAL_SPACES = 7

FALLBACK_ACCENT = "0xffd71921"
FALLBACK_ICON = "0xffb0b0b0"


def get_colors():
    try:
        with open(COLORS_FILE) as f:
            wal = json.load(f)
        c1 = wal["colors"]["color1"].lstrip("#")
        c4 = wal["colors"]["color4"].lstrip("#")
        return f"0xff{c1}", f"0xff{c4}"
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return FALLBACK_ACCENT, FALLBACK_ICON


def get_focused_space():
    try:
        result = subprocess.run(
            ["yabai", "-m", "query", "--spaces", "--space"],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        return data.get("index", 0)
    except Exception:
        return 0


def main():
    accent, icon = get_colors()
    focused = get_focused_space()

    args = ["sketchybar"]
    for sid in range(1, TOTAL_SPACES + 1):
        is_active = sid == focused
        color = accent if is_active else icon
        bg = "on" if is_active else "off"
        args += [
            "--set", f"space.{sid}",
            f"icon.color={color}",
            f"background.drawing={bg}",
        ]

    subprocess.run(args)


if __name__ == "__main__":
    main()
