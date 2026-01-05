#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime


def main():
    name = os.environ.get("NAME", "clock")
    current_time = datetime.now().strftime("%H:%M")
    subprocess.run(["sketchybar", "--set", name, f"label={current_time}"])


if __name__ == "__main__":
    main()
