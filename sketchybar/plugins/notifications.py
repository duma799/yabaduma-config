#!/usr/bin/env python3

import os
import subprocess


ICON = "󰂚"


def main():
    name = os.environ.get("NAME", "notifications")
    subprocess.run(["sketchybar", "--set", name, f"icon={ICON}"])


if __name__ == "__main__":
    main()
