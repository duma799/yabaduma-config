#!/usr/bin/env python3

import os
import subprocess

WIFI_INTERFACE = "en0"

ICON_OFF = "󰤭"
ICON_DISCONNECTED = "󰤯"
ICON_CONNECTED = "󰤨"


def get_wifi_power() -> bool:
    result = subprocess.run(
        ["networksetup", "-getairportpower", WIFI_INTERFACE],
        capture_output=True,
        text=True,
    )
    return "On" in result.stdout


def get_ssid() -> "str | None":
    result = subprocess.run(
        ["ipconfig", "getsummary", WIFI_INTERFACE],
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        if "SSID" in line and "BSSID" not in line:
            parts = line.split(" : ")
            if len(parts) >= 2:
                return parts[1].strip()
    return None


def main():
    name = os.environ.get("NAME", "wifi")

    if not get_wifi_power():
        icon = ICON_OFF
    elif get_ssid() is None:
        icon = ICON_DISCONNECTED
    else:
        icon = ICON_CONNECTED

    subprocess.run(["sketchybar", "--set", name, f"icon={icon}", "label="])


if __name__ == "__main__":
    main()
