#!/usr/bin/env python3

import json
from pathlib import Path

COLORS_FILE = Path.home() / ".cache" / "wal" / "colors.json"

DEFAULTS = {
    "BAR_COLOR": "0xff000000",
    "ITEM_BG_COLOR": "0x00000000",
    "ACCENT_COLOR": "0xff5f87af",
    "ICON_COLOR": "0xffDFE5F3",
    "LABEL_COLOR": "0xffDFE5F3",
    "POPUP_BACKGROUND_COLOR": "0xff1e3a5f",
    "POPUP_BORDER_COLOR": "0xff5f87af",
    "SHADOW_COLOR": "0x80000000",
}


def hex_to_argb(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    return f"0xff{hex_color}"


def lighten_hex(hex_color: str, amount: int = 20) -> str:
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)

    return f"0xff{r:02x}{g:02x}{b:02x}"


def get_colors() -> dict[str, str]:
    if not COLORS_FILE.exists():
        return DEFAULTS.copy()

    try:
        with open(COLORS_FILE) as f:
            wal = json.load(f)

        bg = wal["special"]["background"]
        color1 = wal["colors"]["color1"]
        color4 = wal["colors"]["color4"]
        color6 = wal["colors"]["color6"]

        return {
            "BAR_COLOR": hex_to_argb(bg),
            "ITEM_BG_COLOR": "0x00000000",
            "ACCENT_COLOR": hex_to_argb(color1),
            "ICON_COLOR": hex_to_argb(color4),
            "LABEL_COLOR": hex_to_argb(color6),
            "POPUP_BACKGROUND_COLOR": hex_to_argb(bg),
            "POPUP_BORDER_COLOR": hex_to_argb(color1),
            "SHADOW_COLOR": "0x80000000",
        }
    except (json.JSONDecodeError, KeyError):
        return DEFAULTS.copy()


if __name__ == "__main__":
    colors = get_colors()
    for name, value in colors.items():
        print(f"export {name}={value}")
