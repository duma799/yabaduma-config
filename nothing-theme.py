#!/usr/bin/env python3

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


NOTHING_COLORS = {
    "special": {
        "background": "#000000",
        "foreground": "#ffffff",
        "cursor": "#d71921",
    },
    "colors": {
        "color0": "#000000",
        "color1": "#d71921",
        "color2": "#4a4a4a",
        "color3": "#808080",
        "color4": "#b0b0b0",
        "color5": "#d71921",
        "color6": "#e0e0e0",
        "color7": "#ffffff",
        "color8": "#666666",
        "color9": "#d71921",
        "color10": "#5a5a5a",
        "color11": "#909090",
        "color12": "#c0c0c0",
        "color13": "#d71921",
        "color14": "#f0f0f0",
        "color15": "#ffffff",
    },
}

BG = "#000000"
FG = "#ffffff"
ACCENT = "#d71921"
MUTED = "#666666"
BORDER = "#1a1a1a"
GRAY_DARK = "#333333"
GRAY_MID = "#808080"
GRAY_LIGHT = "#b0b0b0"


def darken_color(hex_color, amount):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))

    return f"#{r:02x}{g:02x}{b:02x}"


def write_pywal_cache():
    cache_dir = Path.home() / ".cache" / "wal"
    cache_dir.mkdir(parents=True, exist_ok=True)

    with open(cache_dir / "colors.json", "w") as f:
        json.dump(NOTHING_COLORS, f, indent=2)

    colors = NOTHING_COLORS["colors"]
    with open(cache_dir / "colors.sh", "w") as f:
        for key, value in colors.items():
            f.write(f"{key}='{value}'\n")
        f.write(f"background='{NOTHING_COLORS['special']['background']}'\n")
        f.write(f"foreground='{NOTHING_COLORS['special']['foreground']}'\n")
        f.write(f"cursor='{NOTHING_COLORS['special']['cursor']}'\n")

    print("Pywal cache written with Nothing colors")
    return True


def reload_borders():
    result = subprocess.run(
        ["pgrep", "-x", "borders"], capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Borders not running, skipping")
        return False

    print("Reloading borders...")
    try:
        subprocess.run(
            ["brew", "services", "restart", "borders"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Borders reloaded")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error reloading borders: {e}")
        return False


def reload_sketchybar():
    result = subprocess.run(
        ["pgrep", "-x", "sketchybar"], capture_output=True, text=True
    )
    if result.returncode != 0:
        print("Sketchybar not running, skipping")
        return False

    print("Reloading sketchybar...")
    try:
        subprocess.run(
            ["sketchybar", "--reload"], check=True, capture_output=True, text=True
        )
        print("Sketchybar reloaded")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error reloading sketchybar: {e}")
        return False


def update_gemini_theme():
    settings_file = Path.home() / ".gemini" / "settings.json"

    if not settings_file.parent.exists():
        print("Gemini CLI config directory not found, skipping Gemini CLI update")
        return False

    print("Updating Gemini CLI theme...")
    try:
        gemini_theme = {
            "type": "custom",
            "name": "Nothing",
            "text": {
                "primary": FG,
                "secondary": MUTED,
                "link": ACCENT,
                "accent": ACCENT,
            },
            "background": {
                "primary": BG,
                "diff": {
                    "added": GRAY_DARK,
                    "removed": darken_color(ACCENT, 0.6),
                },
            },
            "border": {
                "default": BORDER,
                "focused": ACCENT,
            },
            "ui": {
                "comment": MUTED,
                "symbol": GRAY_LIGHT,
                "gradient": [ACCENT, GRAY_MID, FG],
            },
            "status": {
                "error": ACCENT,
                "success": GRAY_LIGHT,
                "warning": GRAY_MID,
            },
            "Background": BG,
            "Foreground": FG,
            "LightBlue": GRAY_LIGHT,
            "AccentBlue": GRAY_LIGHT,
            "AccentPurple": ACCENT,
            "AccentCyan": GRAY_LIGHT,
            "AccentGreen": GRAY_MID,
            "AccentYellow": GRAY_MID,
            "AccentRed": ACCENT,
            "DiffAdded": GRAY_DARK,
            "DiffRemoved": darken_color(ACCENT, 0.6),
            "Comment": MUTED,
            "Gray": MUTED,
            "DarkGray": GRAY_DARK,
            "GradientColors": [ACCENT, GRAY_MID, FG],
        }

        gemini_settings: Dict[str, Any] = {}
        if settings_file.exists():
            with open(settings_file) as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    gemini_settings = {str(k): v for k, v in loaded.items()}

        if "ui" not in gemini_settings or not isinstance(gemini_settings["ui"], dict):
            gemini_settings["ui"] = {}

        ui_settings: Dict[str, Any] = gemini_settings["ui"]
        if "customThemes" not in ui_settings or not isinstance(
            ui_settings["customThemes"], dict
        ):
            ui_settings["customThemes"] = {}

        custom_themes: Dict[str, Any] = ui_settings["customThemes"]
        custom_themes["Nothing"] = gemini_theme
        ui_settings["theme"] = "Nothing"

        with open(settings_file, "w") as f:
            json.dump(gemini_settings, f, indent=2)

        print("Gemini CLI theme updated to Nothing")
        return True
    except Exception as e:
        print(f"Error updating Gemini CLI theme: {e}")
        return False


def main():
    print("Applying Nothing theme...")
    print("")

    cache_ok = write_pywal_cache()

    gemini_ok = update_gemini_theme()
    borders_ok = reload_borders()
    sketchybar_ok = reload_sketchybar()

    print("")
    if cache_ok or gemini_ok or borders_ok or sketchybar_ok:
        print("Nothing theme applied")
    else:
        print("Nothing theme applied with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
