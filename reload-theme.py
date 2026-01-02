#!/usr/bin/env python3

import json
import shutil
import subprocess
import sys
from pathlib import Path


def find_wal():
    wal_in_path = shutil.which("wal")
    if wal_in_path:
        return Path(wal_in_path)

    home = Path.home()
    for version in ["3.14", "3.13", "3.12", "3.11", "3.10", "3.9"]:
        candidate = home / "Library" / "Python" / version / "bin" / "wal"
        if candidate.exists():
            return candidate

    return home / "Library" / "Python" / "3.14" / "bin" / "wal"


def set_wallpaper(wal_path, wallpaper_path):
    if not Path(wallpaper_path).exists():
        print(f"Error: Wallpaper not found: {wallpaper_path}")
        return False

    print(f"Setting wallpaper: {wallpaper_path}")
    try:
        subprocess.run(
            [str(wal_path), "-s", "-t", "-n", "-i", wallpaper_path],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Pywal colors generated")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running pywal: {e}")
        return False
    except FileNotFoundError:
        print(f"Error: pywal not found at {wal_path}")
        return False


def reload_borders():
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


def lighten_color(hex_color, amount):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = min(255, int(r + (255 - r) * amount))
    g = min(255, int(g + (255 - g) * amount))
    b = min(255, int(b + (255 - b) * amount))

    return f"#{r:02x}{g:02x}{b:02x}"


def lighten_color_by_amount(hex_color, amount):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)

    return f"#{r:02x}{g:02x}{b:02x}"


def darken_color(hex_color, amount):
    """Darken a color by a percentage (0.0 to 1.0)"""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = max(0, int(r * (1 - amount)))
    g = max(0, int(g * (1 - amount)))
    b = max(0, int(b * (1 - amount)))

    return f"#{r:02x}{g:02x}{b:02x}"


def adjust_saturation(hex_color, amount):
    """Adjust saturation of a color. Positive amount increases, negative decreases."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Convert to HSL-like adjustment
    gray = (r + g + b) // 3

    if amount > 0:
        # Increase saturation - move away from gray
        r = min(255, int(r + (r - gray) * amount))
        g = min(255, int(g + (g - gray) * amount))
        b = min(255, int(b + (b - gray) * amount))
    else:
        # Decrease saturation - move toward gray
        factor = 1 + amount  # amount is negative, so this reduces
        r = int(gray + (r - gray) * factor)
        g = int(gray + (g - gray) * factor)
        b = int(gray + (b - gray) * factor)

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))

    return f"#{r:02x}{g:02x}{b:02x}"


def blend_colors(hex_color1, hex_color2, ratio=0.5):
    """Blend two colors together. ratio=0 gives color1, ratio=1 gives color2."""
    c1 = hex_color1.lstrip("#")
    c2 = hex_color2.lstrip("#")

    r1, g1, b1 = int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)
    r2, g2, b2 = int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)

    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)

    return f"#{r:02x}{g:02x}{b:02x}"


def update_zed_theme():
    colors_file = Path.home() / ".cache" / "wal" / "colors.json"
    zed_themes_dir = Path.home() / ".config" / "zed" / "themes"
    theme_file = zed_themes_dir / "pywal.json"
    settings_file = Path.home() / ".config" / "zed" / "settings.json"

    if not colors_file.exists():
        print("Pywal colors not found, skipping Zed update")
        return False

    if not zed_themes_dir.exists():
        print("Zed themes directory not found, skipping Zed update")
        return False

    print("Updating Zed theme...")
    try:
        with open(colors_file) as f:
            wal_colors = json.load(f)

        bg = wal_colors["special"]["background"]
        fg = wal_colors["special"]["foreground"]
        color1 = wal_colors["colors"]["color1"]
        color2 = wal_colors["colors"]["color2"]
        color3 = wal_colors["colors"]["color3"]
        color4 = wal_colors["colors"]["color4"]
        color5 = wal_colors["colors"]["color5"]
        color6 = wal_colors["colors"]["color6"]
        color7 = wal_colors["colors"]["color7"]
        color8 = wal_colors["colors"]["color8"]

        # Base semantic colors
        accent_color = color1
        icon_color = color4
        label_color = color6
        selection_bg = lighten_color(bg, 0.25)

        # Background variations for visual hierarchy
        bg_elevated = lighten_color(bg, 0.08)  # Panels, sidebars
        bg_surface = lighten_color(bg, 0.04)  # Tab bar, status bar
        bg_active = lighten_color(bg, 0.12)  # Active tab, active line

        # Tonal variations for syntax highlighting
        # Keywords family (accent-based tones)
        keyword_color = color1
        keyword_light = lighten_color(color1, 0.15)
        keyword_dim = darken_color(color1, 0.2)

        # String family (color2-based tones)
        string_color = color2
        string_light = lighten_color(color2, 0.2)
        string_dim = darken_color(color2, 0.15)

        # Function family (color3-based tones)
        function_color = color3
        function_light = lighten_color(color3, 0.15)
        function_dim = darken_color(color3, 0.2)

        # Type family (color4-based tones)
        type_color = color4
        type_light = lighten_color(color4, 0.15)
        type_dim = darken_color(color4, 0.2)

        # Neutral tones for punctuation and operators
        punctuation_color = blend_colors(color8, label_color, 0.3)
        operator_color = blend_colors(label_color, color3, 0.25)
        bracket_color = blend_colors(color8, label_color, 0.5)

        # Comment tones
        comment_color = color8
        comment_doc = lighten_color(color8, 0.15)

        # Variable tones
        variable_color = label_color
        variable_special = blend_colors(label_color, color5, 0.3)
        parameter_color = blend_colors(label_color, color4, 0.2)

        # Property and attribute tones
        property_color = blend_colors(label_color, color6, 0.4)
        attribute_color = blend_colors(color4, color6, 0.4)

        zed_theme = {
            "$schema": "https://zed.dev/schema/themes/v0.1.0.json",
            "name": "Pywal",
            "author": "Auto-generated from pywal",
            "themes": [
                {
                    "name": "Pywal",
                    "appearance": "dark",
                    "style": {
                        "border": bg_surface,
                        "border.variant": bg_elevated,
                        "border.focused": accent_color,
                        "border.selected": accent_color,
                        "border.transparent": "#00000000",
                        "border.disabled": bg_surface,
                        "elevated_surface.background": bg_elevated,
                        "surface.background": bg_surface,
                        "background": bg,
                        "element.background": bg_surface,
                        "element.hover": selection_bg,
                        "element.active": selection_bg,
                        "element.selected": selection_bg,
                        "element.disabled": bg,
                        "drop_target.background": f"{selection_bg}cc",
                        "ghost_element.background": "#00000000",
                        "ghost_element.hover": selection_bg,
                        "ghost_element.active": selection_bg,
                        "ghost_element.selected": selection_bg,
                        "ghost_element.disabled": bg,
                        "text": label_color,
                        "text.muted": color8,
                        "text.placeholder": color8,
                        "text.disabled": color8,
                        "text.accent": accent_color,
                        "icon": icon_color,
                        "icon.muted": color8,
                        "icon.disabled": color8,
                        "icon.placeholder": color8,
                        "icon.accent": accent_color,
                        "status_bar.background": bg_surface,
                        "title_bar.background": bg,
                        "toolbar.background": bg_surface,
                        "tab_bar.background": bg_surface,
                        "tab.inactive_background": bg_surface,
                        "tab.active_background": bg,
                        "search.match_background": selection_bg,
                        "panel.background": bg_elevated,
                        "panel.focused_border": accent_color,
                        "pane.focused_border": accent_color,
                        "scrollbar.thumb.background": f"{selection_bg}80",
                        "scrollbar.thumb.hover_background": f"{selection_bg}cc",
                        "scrollbar.thumb.border": "#00000000",
                        "scrollbar.track.background": "#00000000",
                        "scrollbar.track.border": "#00000000",
                        "editor.foreground": label_color,
                        "editor.background": bg,
                        "editor.gutter.background": bg,
                        "editor.subheader.background": bg_surface,
                        "editor.active_line.background": bg_active,
                        "editor.highlighted_line.background": bg_active,
                        "editor.line_number": color8,
                        "editor.active_line_number": label_color,
                        "editor.invisible": color8,
                        "editor.wrap_guide": bg,
                        "editor.active_wrap_guide": bg,
                        "editor.document_highlight.read_background": f"{selection_bg}80",
                        "editor.document_highlight.write_background": f"{selection_bg}80",
                        "terminal.background": bg,
                        "terminal.foreground": label_color,
                        "terminal.ansi.black": bg,
                        "terminal.ansi.bright_black": color8,
                        "terminal.ansi.dim_black": bg,
                        "terminal.ansi.red": accent_color,
                        "terminal.ansi.bright_red": accent_color,
                        "terminal.ansi.dim_red": accent_color,
                        "terminal.ansi.green": color2,
                        "terminal.ansi.bright_green": color2,
                        "terminal.ansi.dim_green": color2,
                        "terminal.ansi.yellow": color3,
                        "terminal.ansi.bright_yellow": color3,
                        "terminal.ansi.dim_yellow": color3,
                        "terminal.ansi.blue": icon_color,
                        "terminal.ansi.bright_blue": icon_color,
                        "terminal.ansi.dim_blue": icon_color,
                        "terminal.ansi.magenta": color3,
                        "terminal.ansi.bright_magenta": color3,
                        "terminal.ansi.dim_magenta": color3,
                        "terminal.ansi.cyan": label_color,
                        "terminal.ansi.bright_cyan": label_color,
                        "terminal.ansi.dim_cyan": label_color,
                        "terminal.ansi.white": label_color,
                        "terminal.ansi.bright_white": label_color,
                        "terminal.ansi.dim_white": label_color,
                        "link_text.hover": accent_color,
                        "conflict": accent_color,
                        "conflict.background": bg,
                        "conflict.border": accent_color,
                        "created": color2,
                        "created.background": bg,
                        "created.border": color2,
                        "deleted": accent_color,
                        "deleted.background": bg,
                        "deleted.border": accent_color,
                        "error": accent_color,
                        "error.background": bg,
                        "error.border": accent_color,
                        "hidden": color8,
                        "hidden.background": bg,
                        "hidden.border": color8,
                        "hint": icon_color,
                        "hint.background": bg,
                        "hint.border": icon_color,
                        "ignored": color8,
                        "ignored.background": bg,
                        "ignored.border": color8,
                        "info": icon_color,
                        "info.background": bg,
                        "info.border": icon_color,
                        "modified": color3,
                        "modified.background": bg,
                        "modified.border": color3,
                        "predictive": color8,
                        "predictive.background": bg,
                        "predictive.border": color8,
                        "renamed": color2,
                        "renamed.background": bg,
                        "renamed.border": color2,
                        "success": color2,
                        "success.background": bg,
                        "success.border": color2,
                        "unreachable": color8,
                        "unreachable.background": bg,
                        "unreachable.border": color8,
                        "warning": color3,
                        "warning.background": bg,
                        "warning.border": color3,
                        "players": [],
                        "syntax": {
                            "attribute": {"color": attribute_color},
                            "boolean": {"color": keyword_light, "font_weight": 700},
                            "comment": {"color": comment_color, "font_style": "italic"},
                            "comment.doc": {
                                "color": comment_doc,
                                "font_style": "italic",
                            },
                            "constant": {"color": keyword_color, "font_weight": 700},
                            "constructor": {
                                "color": function_light,
                                "font_weight": 700,
                            },
                            "embedded": {"color": variable_color},
                            "emphasis": {"font_style": "italic"},
                            "emphasis.strong": {"font_weight": 700},
                            "enum": {"color": type_light, "font_weight": 700},
                            "function": {"color": function_color, "font_weight": 700},
                            "hint": {"color": comment_color, "font_weight": 700},
                            "keyword": {"color": keyword_color, "font_weight": 700},
                            "label": {"color": label_color},
                            "link_text": {
                                "color": keyword_light,
                                "font_style": "italic",
                            },
                            "link_uri": {"color": string_light},
                            "number": {"color": keyword_dim},
                            "operator": {"color": operator_color},
                            "predictive": {
                                "color": comment_color,
                                "font_style": "italic",
                            },
                            "preproc": {"color": keyword_dim},
                            "primary": {"color": label_color},
                            "property": {"color": property_color},
                            "punctuation": {"color": punctuation_color},
                            "punctuation.bracket": {"color": bracket_color},
                            "punctuation.delimiter": {"color": punctuation_color},
                            "punctuation.list_marker": {"color": punctuation_color},
                            "punctuation.special": {"color": comment_color},
                            "string": {"color": string_color},
                            "string.escape": {"color": string_dim},
                            "string.regex": {"color": string_light},
                            "string.special": {"color": string_light},
                            "string.special.symbol": {"color": string_dim},
                            "tag": {"color": type_color},
                            "text.literal": {"color": string_color},
                            "title": {"color": keyword_light, "font_weight": 700},
                            "type": {"color": type_color, "font_weight": 700},
                            "variable": {"color": variable_color},
                            "variable.special": {
                                "color": variable_special,
                                "font_style": "italic",
                            },
                            "variant": {"color": type_dim},
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
                '"theme": {\n    "mode": "system",\n    "light": "Ayu Light",\n    "dark": "Pywal"',
                content,
            )

            with open(settings_file, "w") as f:
                f.write(updated_content)

        print("Zed theme updated")
        return True
    except Exception as e:
        print(f"Error updating Zed theme: {e}")
        return False


def update_vscode_settings():
    colors_file = Path.home() / ".cache" / "wal" / "colors.json"
    settings_file = (
        Path.home()
        / "Library"
        / "Application Support"
        / "Code"
        / "User"
        / "settings.json"
    )

    if not colors_file.exists():
        print("Pywal colors not found, skipping VSCode update")
        return False

    if not settings_file.exists():
        print("VSCode settings not found, skipping VSCode update")
        return False

    print("Updating VSCode settings...")
    try:
        with open(colors_file) as f:
            wal_colors = json.load(f)

        with open(settings_file) as f:
            vscode_settings = json.load(f)

        bg = wal_colors["special"]["background"]
        fg = wal_colors["special"]["foreground"]
        color1 = wal_colors["colors"]["color1"]
        color2 = wal_colors["colors"]["color2"]
        color3 = wal_colors["colors"]["color3"]
        color4 = wal_colors["colors"]["color4"]
        color5 = wal_colors["colors"]["color5"]
        color6 = wal_colors["colors"]["color6"]
        color7 = wal_colors["colors"]["color7"]
        color8 = wal_colors["colors"]["color8"]

        # Base semantic colors
        accent_color = color1
        icon_color = color4
        label_color = color6
        selection_bg = lighten_color(bg, 0.25)

        # Tonal variations for syntax highlighting
        # Keywords family (accent-based tones)
        keyword_color = color1
        keyword_light = lighten_color(color1, 0.15)
        keyword_dim = darken_color(color1, 0.2)

        # String family (color2-based tones)
        string_color = color2
        string_light = lighten_color(color2, 0.2)
        string_dim = darken_color(color2, 0.15)

        # Function family (color3-based tones)
        function_color = color3
        function_light = lighten_color(color3, 0.15)
        function_dim = darken_color(color3, 0.2)

        # Type family (color4-based tones)
        type_color = color4
        type_light = lighten_color(color4, 0.15)
        type_dim = darken_color(color4, 0.2)

        # Neutral tones for punctuation and operators
        punctuation_color = blend_colors(color8, label_color, 0.3)
        operator_color = blend_colors(label_color, color3, 0.25)
        bracket_color = blend_colors(color8, label_color, 0.5)

        # Comment tones
        comment_color = color8
        comment_doc = lighten_color(color8, 0.15)

        # Variable tones
        variable_color = label_color
        variable_special = blend_colors(label_color, color5, 0.3)
        parameter_color = blend_colors(label_color, color4, 0.2)

        # Property and attribute tones
        property_color = blend_colors(label_color, color6, 0.4)
        attribute_color = blend_colors(color4, color6, 0.4)

        vscode_settings["workbench.colorCustomizations"] = {
            "editor.background": bg,
            "editor.foreground": label_color,
            "activityBar.background": bg,
            "activityBar.foreground": icon_color,
            "activityBar.inactiveForeground": color8,
            "activityBar.border": bg,
            "activityBarBadge.background": accent_color,
            "activityBarBadge.foreground": bg,
            "sideBar.background": bg,
            "sideBar.foreground": label_color,
            "sideBar.border": bg,
            "sideBarSectionHeader.background": bg,
            "sideBarSectionHeader.foreground": label_color,
            "sideBarSectionHeader.border": bg,
            "statusBar.background": bg,
            "statusBar.foreground": label_color,
            "statusBar.border": bg,
            "titleBar.activeBackground": bg,
            "titleBar.activeForeground": label_color,
            "titleBar.inactiveBackground": bg,
            "titleBar.inactiveForeground": color8,
            "titleBar.border": bg,
            "panel.background": bg,
            "panel.border": bg,
            "panelTitle.activeBorder": accent_color,
            "panelTitle.activeForeground": label_color,
            "panelTitle.inactiveForeground": color8,
            "editorCursor.foreground": accent_color,
            "editorLineNumber.foreground": color8,
            "editorLineNumber.activeForeground": label_color,
            "editorGutter.background": bg,
            "editorGutter.addedBackground": color2,
            "editorGutter.modifiedBackground": color3,
            "editorGutter.deletedBackground": accent_color,
            "editor.lineHighlightBackground": bg,
            "editor.lineHighlightBorder": bg,
            "editor.selectionBackground": selection_bg,
            "editor.inactiveSelectionBackground": bg,
            "editorHoverWidget.background": bg,
            "editorHoverWidget.border": bg,
            "editorSuggestWidget.background": bg,
            "editorSuggestWidget.border": bg,
            "editorSuggestWidget.selectedBackground": selection_bg,
            "scrollbarSlider.background": f"{selection_bg}80",
            "scrollbarSlider.hoverBackground": f"{selection_bg}cc",
            "scrollbarSlider.activeBackground": f"{selection_bg}cc",
            "focusBorder": accent_color,
            "tab.activeBackground": bg,
            "tab.activeForeground": label_color,
            "tab.inactiveBackground": bg,
            "tab.inactiveForeground": color8,
            "tab.activeBorder": accent_color,
            "tab.activeBorderTop": accent_color,
            "tab.border": bg,
            "tab.hoverBackground": bg,
            "tab.hoverForeground": label_color,
            "editorGroupHeader.tabsBackground": bg,
            "editorGroupHeader.tabsBorder": bg,
            "breadcrumb.background": bg,
            "breadcrumb.foreground": color8,
            "breadcrumb.focusForeground": label_color,
            "breadcrumb.activeSelectionForeground": accent_color,
            "list.activeSelectionBackground": selection_bg,
            "list.activeSelectionForeground": label_color,
            "list.inactiveSelectionBackground": bg,
            "list.inactiveSelectionForeground": label_color,
            "list.hoverBackground": bg,
            "list.hoverForeground": label_color,
            "list.focusBackground": selection_bg,
            "list.focusForeground": label_color,
            "list.highlightForeground": accent_color,
            "button.background": accent_color,
            "button.foreground": bg,
            "button.hoverBackground": color3,
            "button.secondaryBackground": bg,
            "button.secondaryForeground": label_color,
            "button.secondaryHoverBackground": bg,
            "input.background": bg,
            "input.foreground": label_color,
            "input.border": bg,
            "input.placeholderForeground": color8,
            "inputOption.activeBackground": accent_color,
            "inputOption.activeForeground": bg,
            "dropdown.background": bg,
            "dropdown.foreground": label_color,
            "dropdown.border": bg,
            "notifications.background": bg,
            "notifications.foreground": label_color,
            "notifications.border": bg,
            "notificationCenter.border": bg,
            "notificationCenterHeader.background": bg,
            "notificationCenterHeader.foreground": label_color,
            "notificationToast.border": bg,
            "notificationsErrorIcon.foreground": accent_color,
            "notificationsWarningIcon.foreground": color3,
            "notificationsInfoIcon.foreground": icon_color,
            "quickInput.background": bg,
            "quickInput.foreground": label_color,
            "quickInputList.focusBackground": selection_bg,
            "quickInputList.focusForeground": label_color,
            "quickInputTitle.background": bg,
            "badge.background": accent_color,
            "badge.foreground": bg,
            "progressBar.background": accent_color,
            "editorWidget.background": bg,
            "editorWidget.border": bg,
            "editorWidget.foreground": label_color,
            "widget.shadow": bg,
            "settings.headerForeground": label_color,
            "settings.modifiedItemIndicator": accent_color,
            "welcomePage.background": bg,
            "walkThrough.embeddedEditorBackground": bg,
            "terminal.background": bg,
            "terminal.foreground": label_color,
            "terminal.ansiBlack": bg,
            "terminal.ansiRed": accent_color,
            "terminal.ansiGreen": color2,
            "terminal.ansiYellow": color3,
            "terminal.ansiBlue": icon_color,
            "terminal.ansiMagenta": color3,
            "terminal.ansiCyan": label_color,
            "terminal.ansiWhite": label_color,
            "terminal.ansiBrightBlack": color8,
            "terminal.ansiBrightRed": accent_color,
            "terminal.ansiBrightGreen": color2,
            "terminal.ansiBrightYellow": color3,
            "terminal.ansiBrightBlue": icon_color,
            "terminal.ansiBrightMagenta": color3,
            "terminal.ansiBrightCyan": label_color,
            "terminal.ansiBrightWhite": label_color,
            "terminalCursor.background": bg,
            "terminalCursor.foreground": accent_color,
        }

        vscode_settings["editor.tokenColorCustomizations"] = {
            "comments": {"foreground": comment_color, "fontStyle": "italic"},
            "keywords": {"foreground": keyword_color, "fontStyle": "bold"},
            "functions": {"foreground": function_color, "fontStyle": "bold"},
            "variables": {"foreground": variable_color},
            "strings": {"foreground": string_color},
            "types": {"foreground": type_color, "fontStyle": "bold"},
            "numbers": {"foreground": keyword_dim},
            "textMateRules": [
                # Storage keywords (let, const, var, function, class, etc.)
                {
                    "scope": ["storage.type", "storage.modifier"],
                    "settings": {"foreground": keyword_color, "fontStyle": "bold"},
                },
                # Type names and classes
                {
                    "scope": ["entity.name.type", "entity.name.class"],
                    "settings": {"foreground": type_color, "fontStyle": "bold"},
                },
                # Interfaces and type parameters - lighter type tone
                {
                    "scope": [
                        "entity.name.type.interface",
                        "entity.name.type.type-parameter",
                    ],
                    "settings": {"foreground": type_light, "fontStyle": "bold"},
                },
                # Enums - lighter type tone
                {
                    "scope": "entity.name.type.enum",
                    "settings": {"foreground": type_light, "fontStyle": "bold"},
                },
                # Functions and methods
                {
                    "scope": ["entity.name.function", "support.function"],
                    "settings": {"foreground": function_color, "fontStyle": "bold"},
                },
                # Method calls - lighter function tone
                {
                    "scope": "entity.name.function.member",
                    "settings": {"foreground": function_light, "fontStyle": "bold"},
                },
                # Constructors - lighter function tone
                {
                    "scope": "entity.name.function.constructor",
                    "settings": {"foreground": function_light, "fontStyle": "bold"},
                },
                # Parameters - italic with parameter color
                {
                    "scope": "variable.parameter",
                    "settings": {"foreground": parameter_color, "fontStyle": "italic"},
                },
                # Language constants (true, false, null, etc.) - lighter keyword
                {
                    "scope": "constant.language",
                    "settings": {"foreground": keyword_light, "fontStyle": "bold"},
                },
                # Numeric constants - dim keyword
                {
                    "scope": "constant.numeric",
                    "settings": {"foreground": keyword_dim},
                },
                # Object properties
                {
                    "scope": [
                        "variable.other.property",
                        "variable.other.object.property",
                    ],
                    "settings": {"foreground": property_color},
                },
                # Special variables (this, self, super)
                {
                    "scope": ["variable.language", "variable.language.this"],
                    "settings": {"foreground": variable_special, "fontStyle": "italic"},
                },
                # String punctuation - dim string
                {
                    "scope": "punctuation.definition.string",
                    "settings": {"foreground": string_dim},
                },
                # Escape sequences in strings
                {
                    "scope": "constant.character.escape",
                    "settings": {"foreground": string_dim},
                },
                # Regex - lighter string
                {
                    "scope": "string.regexp",
                    "settings": {"foreground": string_light},
                },
                # Template literals
                {
                    "scope": "string.template",
                    "settings": {"foreground": string_color},
                },
                # Template expression punctuation
                {
                    "scope": "punctuation.definition.template-expression",
                    "settings": {"foreground": keyword_dim},
                },
                # General punctuation
                {
                    "scope": [
                        "punctuation.definition.variable",
                        "punctuation.definition.parameters",
                        "punctuation.definition.array",
                    ],
                    "settings": {"foreground": punctuation_color},
                },
                # Separators (commas, semicolons)
                {
                    "scope": ["punctuation.separator", "punctuation.terminator"],
                    "settings": {"foreground": punctuation_color},
                },
                # Brackets and braces
                {
                    "scope": ["meta.brace", "punctuation.definition.block"],
                    "settings": {"foreground": bracket_color},
                },
                # Operators
                {
                    "scope": "keyword.operator",
                    "settings": {"foreground": operator_color},
                },
                # Comparison and assignment operators
                {
                    "scope": [
                        "keyword.operator.comparison",
                        "keyword.operator.assignment",
                    ],
                    "settings": {"foreground": operator_color},
                },
                # Attributes (decorators, annotations)
                {
                    "scope": ["entity.name.function.decorator", "meta.decorator"],
                    "settings": {"foreground": attribute_color},
                },
                # Tags (HTML, JSX)
                {
                    "scope": "entity.name.tag",
                    "settings": {"foreground": type_color},
                },
                # Tag attributes
                {
                    "scope": "entity.other.attribute-name",
                    "settings": {"foreground": attribute_color},
                },
                # Doc comments - slightly lighter
                {
                    "scope": ["comment.block.documentation", "comment.block.javadoc"],
                    "settings": {"foreground": comment_doc, "fontStyle": "italic"},
                },
                # Import/export keywords
                {
                    "scope": ["keyword.control.import", "keyword.control.export"],
                    "settings": {"foreground": keyword_dim},
                },
                # Module names in imports
                {
                    "scope": "entity.name.type.module",
                    "settings": {"foreground": string_color},
                },
            ],
        }

        with open(settings_file, "w") as f:
            json.dump(vscode_settings, f, indent=4)

        print("VSCode settings updated")
        return True
    except Exception as e:
        print(f"Error updating VSCode settings: {e}")
        return False


def main():
    wallpaper = sys.argv[1] if len(sys.argv) > 1 else None
    wal_path = find_wal()

    if wallpaper:
        if not set_wallpaper(wal_path, wallpaper):
            sys.exit(1)

    zed_ok = update_zed_theme()
    vscode_ok = update_vscode_settings()
    borders_ok = reload_borders()
    sketchybar_ok = reload_sketchybar()

    print("")
    if zed_ok or vscode_ok or borders_ok or sketchybar_ok:
        print("Theme reloaded")
    else:
        print("Theme reload completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
