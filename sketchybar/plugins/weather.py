#!/usr/bin/env python3

import json
import os
import subprocess
from urllib.request import urlopen
from urllib.error import URLError


WEATHER_URL = "https://wttr.in/?format=j1"
ICON = "󰖐"


def get_weather():
    try:
        response = urlopen(WEATHER_URL, timeout=5)
        data = json.loads(response.read().decode())

        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]

        area = data["nearest_area"][0]
        city = area["areaName"][0]["value"]

        return f"{city} · {temp_c}°C {desc}"
    except (URLError, KeyError, json.JSONDecodeError, Exception):
        return ""


def main():
    name = os.environ.get("NAME", "weather")
    label = get_weather()
    subprocess.run(["sketchybar", "--set", name, f"icon={ICON}", f"label={label}"])


if __name__ == "__main__":
    main()
