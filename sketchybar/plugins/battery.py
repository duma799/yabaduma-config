#!/usr/bin/env python3

import os
import re
import subprocess

ICON_FULL = "󰁹"
ICON_HIGH = "󰂀"
ICON_MEDIUM = "󰁾"
ICON_LOW = "󰁻"
ICON_CRITICAL = "󰁺"
ICON_CHARGING = "󰂄"


def get_battery_info() -> tuple[int, bool]:
    result = subprocess.run(
        ["pmset", "-g", "batt"],
        capture_output=True,
        text=True,
    )
    output = result.stdout

    match = re.search(r"(\d+)%", output)
    percentage = int(match.group(1)) if match else 0

    charging = "AC Power" in output

    return percentage, charging


def get_icon(percentage: int, charging: bool) -> str:
    if charging:
        return ICON_CHARGING
    if percentage >= 90:
        return ICON_FULL
    elif percentage >= 60:
        return ICON_HIGH
    elif percentage >= 30:
        return ICON_MEDIUM
    elif percentage >= 10:
        return ICON_LOW
    return ICON_CRITICAL


def main():
    name = os.environ.get("NAME", "battery")
    percentage, charging = get_battery_info()
    icon = get_icon(percentage, charging)
    subprocess.run(
        ["sketchybar", "--set", name, f"icon={icon}", f"label={percentage}%"]
    )


if __name__ == "__main__":
    main()
