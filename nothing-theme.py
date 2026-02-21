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

NDOT_FONT = "NDOT 47 (inspired by NOTHING)"

BG = "#000000"
FG = "#ffffff"
ACCENT = "#d71921"
MUTED = "#666666"
SURFACE = "#0d0d0d"
ELEVATED = "#141414"
ACTIVE = "#1a1a1a"
BORDER = "#1a1a1a"
SELECTION = "#2a0508"
GRAY_DARK = "#333333"
GRAY_MID = "#808080"
GRAY_LIGHT = "#b0b0b0"


def lighten_color(hex_color, amount):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = min(255, int(r + (255 - r) * amount))
    g = min(255, int(g + (255 - g) * amount))
    b = min(255, int(b + (255 - b) * amount))

    return f"#{r:02x}{g:02x}{b:02x}"


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


def update_zed_theme():
    zed_themes_dir = Path.home() / ".config" / "zed" / "themes"
    theme_file = zed_themes_dir / "nothing.json"
    settings_file = Path.home() / ".config" / "zed" / "settings.json"

    if not zed_themes_dir.exists():
        print("Zed themes directory not found, skipping Zed update")
        return False

    print("Updating Zed theme...")
    try:
        zed_theme = {
            "$schema": "https://zed.dev/schema/themes/v0.1.0.json",
            "name": "Nothing",
            "author": "Nothing theme",
            "themes": [
                {
                    "name": "Nothing",
                    "appearance": "dark",
                    "style": {
                        "border": BORDER,
                        "border.variant": ELEVATED,
                        "border.focused": ACCENT,
                        "border.selected": ACCENT,
                        "border.transparent": "#00000000",
                        "border.disabled": SURFACE,
                        "elevated_surface.background": ELEVATED,
                        "surface.background": SURFACE,
                        "background": BG,
                        "element.background": SURFACE,
                        "element.hover": ACTIVE,
                        "element.active": ACTIVE,
                        "element.selected": ACTIVE,
                        "element.disabled": BG,
                        "drop_target.background": f"{ACTIVE}cc",
                        "ghost_element.background": "#00000000",
                        "ghost_element.hover": ACTIVE,
                        "ghost_element.active": ACTIVE,
                        "ghost_element.selected": ACTIVE,
                        "ghost_element.disabled": BG,
                        "text": FG,
                        "text.muted": MUTED,
                        "text.placeholder": MUTED,
                        "text.disabled": GRAY_DARK,
                        "text.accent": ACCENT,
                        "icon": GRAY_LIGHT,
                        "icon.muted": MUTED,
                        "icon.disabled": GRAY_DARK,
                        "icon.placeholder": MUTED,
                        "icon.accent": ACCENT,
                        "status_bar.background": SURFACE,
                        "title_bar.background": BG,
                        "toolbar.background": SURFACE,
                        "tab_bar.background": SURFACE,
                        "tab.inactive_background": SURFACE,
                        "tab.active_background": BG,
                        "search.match_background": SELECTION,
                        "panel.background": ELEVATED,
                        "panel.focused_border": ACCENT,
                        "pane.focused_border": ACCENT,
                        "scrollbar.thumb.background": f"{ACTIVE}80",
                        "scrollbar.thumb.hover_background": f"{ACTIVE}cc",
                        "scrollbar.thumb.border": "#00000000",
                        "scrollbar.track.background": "#00000000",
                        "scrollbar.track.border": "#00000000",
                        "editor.foreground": FG,
                        "editor.background": BG,
                        "editor.gutter.background": BG,
                        "editor.subheader.background": SURFACE,
                        "editor.active_line.background": SURFACE,
                        "editor.highlighted_line.background": SURFACE,
                        "editor.line_number": GRAY_DARK,
                        "editor.active_line_number": FG,
                        "editor.invisible": GRAY_DARK,
                        "editor.wrap_guide": BG,
                        "editor.active_wrap_guide": BG,
                        "editor.document_highlight.read_background": f"{ACTIVE}80",
                        "editor.document_highlight.write_background": f"{ACTIVE}80",
                        "terminal.background": BG,
                        "terminal.foreground": FG,
                        "terminal.ansi.black": BG,
                        "terminal.ansi.bright_black": MUTED,
                        "terminal.ansi.dim_black": BG,
                        "terminal.ansi.red": ACCENT,
                        "terminal.ansi.bright_red": ACCENT,
                        "terminal.ansi.dim_red": ACCENT,
                        "terminal.ansi.green": GRAY_LIGHT,
                        "terminal.ansi.bright_green": GRAY_LIGHT,
                        "terminal.ansi.dim_green": GRAY_MID,
                        "terminal.ansi.yellow": GRAY_MID,
                        "terminal.ansi.bright_yellow": GRAY_LIGHT,
                        "terminal.ansi.dim_yellow": MUTED,
                        "terminal.ansi.blue": GRAY_LIGHT,
                        "terminal.ansi.bright_blue": GRAY_LIGHT,
                        "terminal.ansi.dim_blue": GRAY_MID,
                        "terminal.ansi.magenta": ACCENT,
                        "terminal.ansi.bright_magenta": ACCENT,
                        "terminal.ansi.dim_magenta": ACCENT,
                        "terminal.ansi.cyan": GRAY_LIGHT,
                        "terminal.ansi.bright_cyan": FG,
                        "terminal.ansi.dim_cyan": GRAY_MID,
                        "terminal.ansi.white": FG,
                        "terminal.ansi.bright_white": FG,
                        "terminal.ansi.dim_white": GRAY_LIGHT,
                        "link_text.hover": ACCENT,
                        "conflict": ACCENT,
                        "conflict.background": BG,
                        "conflict.border": ACCENT,
                        "created": GRAY_LIGHT,
                        "created.background": BG,
                        "created.border": GRAY_LIGHT,
                        "deleted": ACCENT,
                        "deleted.background": BG,
                        "deleted.border": ACCENT,
                        "error": ACCENT,
                        "error.background": BG,
                        "error.border": ACCENT,
                        "hidden": GRAY_DARK,
                        "hidden.background": BG,
                        "hidden.border": GRAY_DARK,
                        "hint": MUTED,
                        "hint.background": BG,
                        "hint.border": MUTED,
                        "ignored": GRAY_DARK,
                        "ignored.background": BG,
                        "ignored.border": GRAY_DARK,
                        "info": GRAY_LIGHT,
                        "info.background": BG,
                        "info.border": GRAY_LIGHT,
                        "modified": GRAY_MID,
                        "modified.background": BG,
                        "modified.border": GRAY_MID,
                        "predictive": GRAY_DARK,
                        "predictive.background": BG,
                        "predictive.border": GRAY_DARK,
                        "renamed": GRAY_LIGHT,
                        "renamed.background": BG,
                        "renamed.border": GRAY_LIGHT,
                        "success": GRAY_LIGHT,
                        "success.background": BG,
                        "success.border": GRAY_LIGHT,
                        "unreachable": GRAY_DARK,
                        "unreachable.background": BG,
                        "unreachable.border": GRAY_DARK,
                        "warning": GRAY_MID,
                        "warning.background": BG,
                        "warning.border": GRAY_MID,
                        "players": [],
                        "syntax": {
                            "attribute": {"color": GRAY_LIGHT},
                            "boolean": {"color": FG, "font_weight": 700},
                            "comment": {"color": GRAY_DARK, "font_style": "italic"},
                            "comment.doc": {
                                "color": MUTED,
                                "font_style": "italic",
                            },
                            "constant": {"color": FG, "font_weight": 700},
                            "constructor": {
                                "color": FG,
                                "font_weight": 700,
                            },
                            "embedded": {"color": GRAY_LIGHT},
                            "emphasis": {"font_style": "italic"},
                            "emphasis.strong": {"font_weight": 700},
                            "enum": {"color": GRAY_LIGHT, "font_weight": 700},
                            "function": {"color": GRAY_LIGHT, "font_weight": 700},
                            "hint": {"color": GRAY_DARK, "font_weight": 700},
                            "keyword": {"color": ACCENT, "font_weight": 700},
                            "label": {"color": FG},
                            "link_text": {
                                "color": ACCENT,
                                "font_style": "italic",
                            },
                            "link_uri": {"color": GRAY_MID},
                            "number": {"color": GRAY_MID},
                            "operator": {"color": MUTED},
                            "predictive": {
                                "color": GRAY_DARK,
                                "font_style": "italic",
                            },
                            "preproc": {"color": ACCENT},
                            "primary": {"color": FG},
                            "property": {"color": GRAY_LIGHT},
                            "punctuation": {"color": MUTED},
                            "punctuation.bracket": {"color": MUTED},
                            "punctuation.delimiter": {"color": MUTED},
                            "punctuation.list_marker": {"color": MUTED},
                            "punctuation.special": {"color": GRAY_DARK},
                            "string": {"color": GRAY_MID},
                            "string.escape": {"color": ACCENT},
                            "string.regex": {"color": GRAY_LIGHT},
                            "string.special": {"color": GRAY_LIGHT},
                            "string.special.symbol": {"color": GRAY_MID},
                            "tag": {"color": ACCENT},
                            "text.literal": {"color": GRAY_MID},
                            "title": {"color": FG, "font_weight": 700},
                            "type": {"color": GRAY_LIGHT, "font_weight": 700},
                            "variable": {"color": FG},
                            "variable.special": {
                                "color": GRAY_LIGHT,
                                "font_style": "italic",
                            },
                            "variant": {"color": GRAY_MID},
                        },
                    },
                }
            ],
        }

        with open(theme_file, "w") as f:
            json.dump(zed_theme, f, indent=2)

        if settings_file.exists():
            with open(settings_file) as f:
                content = f.read()

            import re

            updated_content = re.sub(
                r'"theme":\s*\{[^}]*"dark":\s*"[^"]*"',
                '"theme": {\n    "mode": "system",\n    "light": "Ayu Light",\n    "dark": "Nothing"',
                content,
            )

            if '"ui_font_family"' in updated_content:
                updated_content = re.sub(
                    r'"ui_font_family":\s*"[^"]*"',
                    f'"ui_font_family": "{NDOT_FONT}"',
                    updated_content,
                )
            else:
                updated_content = updated_content.replace(
                    '"theme":', f'"ui_font_family": "{NDOT_FONT}",\n  "theme":'
                )

            with open(settings_file, "w") as f:
                f.write(updated_content)

        print("Zed theme updated to Nothing")
        return True
    except Exception as e:
        print(f"Error updating Zed theme: {e}")
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


def update_vscode_settings(settings_file=None, app_name="VSCode"):
    if settings_file is None:
        settings_file = (
            Path.home()
            / "Library"
            / "Application Support"
            / "Code"
            / "User"
            / "settings.json"
        )

    if not settings_file.exists():
        print(f"{app_name} settings not found, skipping {app_name} update")
        return False

    print(f"Updating {app_name} settings...")
    try:
        with open(settings_file) as f:
            vscode_settings = json.load(f)

        vscode_settings["workbench.colorCustomizations"] = {
            "editor.background": BG,
            "editor.foreground": FG,
            "editorCursor.foreground": ACCENT,
            "editorLineNumber.foreground": GRAY_DARK,
            "editorLineNumber.activeForeground": FG,
            "editorGutter.background": BG,
            "editorGutter.addedBackground": GRAY_LIGHT,
            "editorGutter.modifiedBackground": GRAY_MID,
            "editorGutter.deletedBackground": ACCENT,
            "editor.lineHighlightBackground": SURFACE,
            "editor.lineHighlightBorder": SURFACE,
            "editor.selectionBackground": SELECTION,
            "editor.inactiveSelectionBackground": SURFACE,
            "activityBar.background": BG,
            "activityBar.foreground": GRAY_LIGHT,
            "activityBar.inactiveForeground": MUTED,
            "activityBar.border": BORDER,
            "activityBarBadge.background": ACCENT,
            "activityBarBadge.foreground": FG,
            "sideBar.background": ELEVATED,
            "sideBar.foreground": FG,
            "sideBar.border": BORDER,
            "sideBarSectionHeader.background": ELEVATED,
            "sideBarSectionHeader.foreground": FG,
            "sideBarSectionHeader.border": BORDER,
            "statusBar.background": BG,
            "statusBar.foreground": MUTED,
            "statusBar.border": BORDER,
            "titleBar.activeBackground": BG,
            "titleBar.activeForeground": FG,
            "titleBar.inactiveBackground": BG,
            "titleBar.inactiveForeground": MUTED,
            "titleBar.border": BORDER,
            "panel.background": ELEVATED,
            "panel.border": BORDER,
            "panelTitle.activeBorder": ACCENT,
            "panelTitle.activeForeground": FG,
            "panelTitle.inactiveForeground": MUTED,
            "editorHoverWidget.background": ELEVATED,
            "editorHoverWidget.border": BORDER,
            "editorSuggestWidget.background": ELEVATED,
            "editorSuggestWidget.border": BORDER,
            "editorSuggestWidget.selectedBackground": SELECTION,
            "scrollbarSlider.background": f"{ACTIVE}80",
            "scrollbarSlider.hoverBackground": f"{ACTIVE}cc",
            "scrollbarSlider.activeBackground": f"{ACTIVE}cc",
            "focusBorder": ACCENT,
            "tab.activeBackground": BG,
            "tab.activeForeground": FG,
            "tab.inactiveBackground": SURFACE,
            "tab.inactiveForeground": MUTED,
            "tab.activeBorder": ACCENT,
            "tab.activeBorderTop": ACCENT,
            "tab.border": BORDER,
            "tab.hoverBackground": ELEVATED,
            "tab.hoverForeground": FG,
            "editorGroupHeader.tabsBackground": SURFACE,
            "editorGroupHeader.tabsBorder": BORDER,
            "breadcrumb.background": SURFACE,
            "breadcrumb.foreground": MUTED,
            "breadcrumb.focusForeground": FG,
            "breadcrumb.activeSelectionForeground": ACCENT,
            "list.activeSelectionBackground": SELECTION,
            "list.activeSelectionForeground": FG,
            "list.inactiveSelectionBackground": SURFACE,
            "list.inactiveSelectionForeground": FG,
            "list.hoverBackground": ACTIVE,
            "list.hoverForeground": FG,
            "list.focusBackground": SELECTION,
            "list.focusForeground": FG,
            "list.highlightForeground": ACCENT,
            "button.background": ACCENT,
            "button.foreground": FG,
            "button.hoverBackground": lighten_color(ACCENT, 0.15),
            "button.secondaryBackground": SURFACE,
            "button.secondaryForeground": FG,
            "button.secondaryHoverBackground": ELEVATED,
            "input.background": BG,
            "input.foreground": FG,
            "input.border": BORDER,
            "input.placeholderForeground": MUTED,
            "inputOption.activeBackground": ACCENT,
            "inputOption.activeForeground": FG,
            "dropdown.background": ELEVATED,
            "dropdown.foreground": FG,
            "dropdown.border": BORDER,
            "notifications.background": ELEVATED,
            "notifications.foreground": FG,
            "notifications.border": BORDER,
            "notificationCenter.border": BORDER,
            "notificationCenterHeader.background": ELEVATED,
            "notificationCenterHeader.foreground": FG,
            "notificationToast.border": BORDER,
            "notificationsErrorIcon.foreground": ACCENT,
            "notificationsWarningIcon.foreground": GRAY_MID,
            "notificationsInfoIcon.foreground": GRAY_LIGHT,
            "quickInput.background": ELEVATED,
            "quickInput.foreground": FG,
            "quickInputList.focusBackground": SELECTION,
            "quickInputList.focusForeground": FG,
            "quickInputTitle.background": ELEVATED,
            "badge.background": ACCENT,
            "badge.foreground": FG,
            "progressBar.background": ACCENT,
            "editorWidget.background": ELEVATED,
            "editorWidget.border": BORDER,
            "editorWidget.foreground": FG,
            "widget.shadow": f"{BG}80",
            "settings.headerForeground": FG,
            "settings.modifiedItemIndicator": ACCENT,
            "welcomePage.background": BG,
            "walkThrough.embeddedEditorBackground": ELEVATED,
            "terminal.background": BG,
            "terminal.foreground": FG,
            "terminal.ansiBlack": BG,
            "terminal.ansiRed": ACCENT,
            "terminal.ansiGreen": GRAY_LIGHT,
            "terminal.ansiYellow": GRAY_MID,
            "terminal.ansiBlue": GRAY_LIGHT,
            "terminal.ansiMagenta": ACCENT,
            "terminal.ansiCyan": GRAY_LIGHT,
            "terminal.ansiWhite": FG,
            "terminal.ansiBrightBlack": MUTED,
            "terminal.ansiBrightRed": ACCENT,
            "terminal.ansiBrightGreen": GRAY_LIGHT,
            "terminal.ansiBrightYellow": GRAY_MID,
            "terminal.ansiBrightBlue": GRAY_LIGHT,
            "terminal.ansiBrightMagenta": ACCENT,
            "terminal.ansiBrightCyan": FG,
            "terminal.ansiBrightWhite": FG,
            "terminalCursor.background": BG,
            "terminalCursor.foreground": ACCENT,
        }

        vscode_settings["editor.tokenColorCustomizations"] = {
            "comments": {"foreground": GRAY_DARK, "fontStyle": "italic"},
            "keywords": {"foreground": ACCENT, "fontStyle": "bold"},
            "functions": {"foreground": GRAY_LIGHT, "fontStyle": "bold"},
            "variables": {"foreground": FG},
            "strings": {"foreground": GRAY_MID},
            "types": {"foreground": GRAY_LIGHT, "fontStyle": "bold"},
            "numbers": {"foreground": GRAY_MID},
            "textMateRules": [
                {
                    "scope": ["storage.type", "storage.modifier"],
                    "settings": {"foreground": ACCENT, "fontStyle": "bold"},
                },
                {
                    "scope": ["entity.name.type", "entity.name.class"],
                    "settings": {"foreground": GRAY_LIGHT, "fontStyle": "bold"},
                },
                {
                    "scope": [
                        "entity.name.type.interface",
                        "entity.name.type.type-parameter",
                    ],
                    "settings": {"foreground": GRAY_LIGHT, "fontStyle": "bold"},
                },
                {
                    "scope": "entity.name.type.enum",
                    "settings": {"foreground": GRAY_LIGHT, "fontStyle": "bold"},
                },
                {
                    "scope": ["entity.name.function", "support.function"],
                    "settings": {"foreground": GRAY_LIGHT, "fontStyle": "bold"},
                },
                {
                    "scope": "entity.name.function.member",
                    "settings": {"foreground": GRAY_LIGHT, "fontStyle": "bold"},
                },
                {
                    "scope": "entity.name.function.constructor",
                    "settings": {"foreground": FG, "fontStyle": "bold"},
                },
                {
                    "scope": "variable.parameter",
                    "settings": {"foreground": FG, "fontStyle": "italic"},
                },
                {
                    "scope": "constant.language",
                    "settings": {"foreground": FG, "fontStyle": "bold"},
                },
                {
                    "scope": "constant.numeric",
                    "settings": {"foreground": GRAY_MID},
                },
                {
                    "scope": [
                        "variable.other.property",
                        "variable.other.object.property",
                    ],
                    "settings": {"foreground": GRAY_LIGHT},
                },
                {
                    "scope": ["variable.language", "variable.language.this"],
                    "settings": {"foreground": GRAY_LIGHT, "fontStyle": "italic"},
                },
                {
                    "scope": "punctuation.definition.string",
                    "settings": {"foreground": MUTED},
                },
                {
                    "scope": "constant.character.escape",
                    "settings": {"foreground": ACCENT},
                },
                {
                    "scope": "string.regexp",
                    "settings": {"foreground": GRAY_LIGHT},
                },
                {
                    "scope": "string.template",
                    "settings": {"foreground": GRAY_MID},
                },
                {
                    "scope": "punctuation.definition.template-expression",
                    "settings": {"foreground": ACCENT},
                },
                {
                    "scope": [
                        "punctuation.definition.variable",
                        "punctuation.definition.parameters",
                        "punctuation.definition.array",
                    ],
                    "settings": {"foreground": MUTED},
                },
                {
                    "scope": ["punctuation.separator", "punctuation.terminator"],
                    "settings": {"foreground": MUTED},
                },
                {
                    "scope": ["meta.brace", "punctuation.definition.block"],
                    "settings": {"foreground": MUTED},
                },
                {
                    "scope": "keyword.operator",
                    "settings": {"foreground": MUTED},
                },
                {
                    "scope": [
                        "keyword.operator.comparison",
                        "keyword.operator.assignment",
                    ],
                    "settings": {"foreground": MUTED},
                },
                {
                    "scope": ["entity.name.function.decorator", "meta.decorator"],
                    "settings": {"foreground": GRAY_LIGHT},
                },
                {
                    "scope": "entity.name.tag",
                    "settings": {"foreground": ACCENT},
                },
                {
                    "scope": "entity.other.attribute-name",
                    "settings": {"foreground": GRAY_LIGHT},
                },
                {
                    "scope": ["comment.block.documentation", "comment.block.javadoc"],
                    "settings": {"foreground": MUTED, "fontStyle": "italic"},
                },
                {
                    "scope": ["keyword.control.import", "keyword.control.export"],
                    "settings": {"foreground": ACCENT},
                },
                {
                    "scope": "entity.name.type.module",
                    "settings": {"foreground": GRAY_MID},
                },
            ],
        }

        with open(settings_file, "w") as f:
            json.dump(vscode_settings, f, indent=4)

        print(f"{app_name} settings updated to Nothing theme")
        return True
    except Exception as e:
        print(f"Error updating {app_name} settings: {e}")
        return False


def update_antigravity_settings():
    settings_file = (
        Path.home()
        / "Library"
        / "Application Support"
        / "Antigravity"
        / "User"
        / "settings.json"
    )
    return update_vscode_settings(settings_file=settings_file, app_name="Antigravity")


def main():
    print("Applying Nothing theme...")
    print("")

    cache_ok = write_pywal_cache()

    zed_ok = update_zed_theme()
    vscode_ok = update_vscode_settings()
    antigravity_ok = update_antigravity_settings()
    gemini_ok = update_gemini_theme()
    borders_ok = reload_borders()
    sketchybar_ok = reload_sketchybar()

    print("")
    if cache_ok or zed_ok or vscode_ok or antigravity_ok or gemini_ok or borders_ok or sketchybar_ok:
        print("Nothing theme applied")
    else:
        print("Nothing theme applied with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
