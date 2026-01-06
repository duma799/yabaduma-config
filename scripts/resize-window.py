#!/usr/bin/env python3

import shutil
import subprocess
import sys

RESIZE_AMOUNT = 50

RESIZE_MAP = {
    "left": (f"left:-{RESIZE_AMOUNT}:0", f"right:-{RESIZE_AMOUNT}:0"),
    "right": (f"right:{RESIZE_AMOUNT}:0", f"left:{RESIZE_AMOUNT}:0"),
    "up": (f"top:0:-{RESIZE_AMOUNT}", f"bottom:0:-{RESIZE_AMOUNT}"),
    "down": (f"bottom:0:{RESIZE_AMOUNT}", f"top:0:{RESIZE_AMOUNT}"),
}


def check_yabai() -> bool:
    """Check if yabai is installed and running."""
    if not shutil.which("yabai"):
        print("Error: yabai is not installed or not in PATH", file=sys.stderr)
        return False

    result = subprocess.run(
        ["yabai", "-m", "query", "--windows"],
        capture_output=True,
    )
    if result.returncode != 0:
        print("Error: yabai is not running", file=sys.stderr)
        return False

    return True


def resize_window(resize_arg: str) -> bool:
    result = subprocess.run(
        ["yabai", "-m", "window", "--resize", resize_arg],
        capture_output=True,
    )
    return result.returncode == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: resize-window.py <left|right|up|down>", file=sys.stderr)
        sys.exit(1)

    direction = sys.argv[1]

    if direction not in RESIZE_MAP:
        print("Usage: resize-window.py <left|right|up|down>", file=sys.stderr)
        sys.exit(1)

    if not check_yabai():
        sys.exit(1)

    primary, fallback = RESIZE_MAP[direction]
    if not resize_window(primary):
        resize_window(fallback)


if __name__ == "__main__":
    main()
