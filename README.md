# YabaDuma Config (In Progress).

## Tested on Macbook Air M4 with MacOS 26.2 Tahoe.

### Yabai WM + SKHD Keyboard Shortcuts.

#### **[Keybinds.md](Keybinds.md)** - Complete keybind guide.

### Visual & UX
- Minimal gaps 10px
- Window opacity (active: 1.0, inactive: 0.9)
- **JankyBorders** - Dynamic window borders with pywal integration
  - Active: Gradient from pywal colors (color6 → color4)
  - Inactive: Semi-transparent background color
  - Width: 3px, rounded corners
  - Auto-updates with wallpaper changes
- No window animations (macOS limitation)
- **Pywal integration** - Dynamic colors from wallpaper
  - Borders automatically match wallpaper colors
  - SketchyBar color theming
  - Easy theme switching with `reload-theme` command

### Input
- 4-finger MacOS gestures for workspace switch

---

## Components

- **yabai** - Tiling window manager with scripting addition
- **skhd** - Hotkey daemon for keyboard shortcuts
- **borders** (JankyBorders) - Window border system with gradient support
- **pywal** - Dynamic color scheme generator from wallpapers
- **sketchybar** - Status bar with pywal theming

---

## Installation Guide

### Prerequisites
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add FelixKratz tap for borders
brew tap FelixKratz/formulae
```

### Install Components
```bash
# Install yabai and skhd
brew install koekeishiya/formulae/yabai
brew install koekeishiya/formulae/skhd

# Install borders
brew install borders

# Install pywal (Python package)
pip3 install pywal

# Install sketchybar
brew install sketchybar
```

### Setup
```bash
# Clone this config
git clone https://github.com/duma799/yabaduma-config.git ~/.config/yabaduma-config

# Link configs
ln -s ~/.config/yabaduma-config/yabairc ~/.yabairc
ln -s ~/.config/yabaduma-config/skhdrc ~/.skhdrc

# Create borders config directory and link
mkdir -p ~/.config/borders
ln -s ~/.config/yabaduma-config/bordersrc ~/.config/borders/bordersrc

# Link sketchybar config
ln -s ~/.config/yabaduma-config/sketchybar ~/.config/sketchybar

# Add reload-theme command to PATH
mkdir -p ~/.local/bin
ln -sf ~/.config/yabaduma-config/reload-theme.py ~/.local/bin/reload-theme

# Ensure ~/.local/bin is in your PATH (add to ~/.zshrc if needed)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# Start services
brew services start yabai
brew services start skhd
brew services start borders
brew services start sketchybar
```

### Post-Installation
- Disable SIP (System Integrity Protection) partially for yabai scripting addition
- Configure accessibility permissions for yabai and skhd
- Set initial wallpaper with pywal: `wal -i /path/to/wallpaper.jpg`
- Reload theme: `reload-theme`
- Restart services after configuration changes

---

## Pywal Theme Integration

### Quick Start
```bash
# Set wallpaper and generate colors
wal -i /path/to/your/wallpaper.jpg

# Reload borders and sketchybar with new colors
reload-theme

# Or do both at once
reload-theme /path/to/your/wallpaper.jpg
```

### How It Works
- **Pywal** analyzes your wallpaper and generates a color palette
- **Borders** automatically uses colors from the palette:
  - Active gradient: color6 → color4
  - Inactive: Semi-transparent background color
- **SketchyBar** applies pywal colors to the status bar
- **reload-theme** script refreshes all components

### Customization

**Change which colors are used for borders:**
Edit [bordersrc](bordersrc) and modify:
```bash
active_color1=$(echo "$color6" | sed 's/#/0xff/')  # Change color6 to any color0-15
active_color2=$(echo "$color4" | sed 's/#/0xff/')  # Change color4 to any color0-15
```

**Pywal color variables:**
- `color0-7` - Main palette colors
- `color8-15` - Bright variants
- `background` - Background color
- `foreground` - Foreground color

**See current colors:**
```bash
cat ~/.cache/wal/colors.sh
```

**Full installation guide in progress.**