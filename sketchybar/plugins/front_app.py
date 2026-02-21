#!/usr/bin/env python3

import json
import os
import subprocess


def main():
    name = os.environ.get("NAME", "front_app")

    try:
        result = subprocess.run(
            ["yabai", "-m", "query", "--windows", "--window"],
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        app = data.get("app", "")
    except Exception:
        app = ""

    subprocess.run(["sketchybar", "--set", name, f"label={app}"])


if __name__ == "__main__":
    main()
