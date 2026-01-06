#!/usr/bin/env python3

import os
import subprocess

ICON_HIGH = "󰕾"
ICON_MEDIUM = "󰖀"
ICON_LOW = "󰕿"
ICON_MUTE = "󰖁"


def get_current_volume() -> int:
    """Get current system volume using osascript."""
    result = subprocess.run(
        ["osascript", "-e", "output volume of (get volume settings)"],
        capture_output=True,
        text=True,
    )
    try:
        return int(result.stdout.strip())
    except ValueError:
        return 0


def get_icon(volume: int) -> str:
    if volume >= 60:
        return ICON_HIGH
    elif volume >= 30:
        return ICON_MEDIUM
    elif volume >= 1:
        return ICON_LOW
    return ICON_MUTE


def update_volume(name: str, volume: int) -> None:
    icon = get_icon(volume)
    subprocess.run(["sketchybar", "--set", name, f"icon={icon}", f"label={volume}%"])


def main():
    name = os.environ.get("NAME", "volume")
    sender = os.environ.get("SENDER", "")

    if sender == "volume_change":
        volume_str = os.environ.get("INFO", "0")
        try:
            volume = int(volume_str)
        except ValueError:
            volume = 0
    else:
        # Initial load - get current volume from system
        volume = get_current_volume()

    update_volume(name, volume)


if __name__ == "__main__":
    main()
