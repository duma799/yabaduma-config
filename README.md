# YabaDuma Config

MacOS tiling WM setup with dynamic color theming. Built with Yabai, SketchyBar, and PyWal. All scripts are Python-driven for maintainability.

**Tested on MacBook Air M4, macOS 26.2 Tahoe.**

## Showcase

<div align="center">
  <img src="screenshots/1.jpeg" alt="Desktop with tiling windows" width="800"/>
  <p><i>Tiling window management with dynamic PyWal theming</i></p>
</div>

<div align="center">
  <img src="screenshots/2.png" alt="SketchyBar and window borders" width="800"/>
  <p><i>Custom SketchyBar with system info and JankyBorders integration</i></p>
</div>

### Features
- **Dynamic theming** - Colors automatically generated from your wallpaper using PyWal
- **Tiling window management** - BSP-like layout with Yabai
- **Custom status bar** - SketchyBar with battery, bluetooth, wifi, volume, and workspace indicators
- **Window borders** - JankyBorders with gradient colors from PyWal
- **Editor integration** - Script updates VSCode and Zed themes to match your wallpaper
- **Keyboard-driven** - Extensive keybinds for window manipulation (see [Keybinds.md](Keybinds.md))

## What's in here

- **Yabai** - tiling WM
- **SKHD** - keyboard shortcuts (see [Keybinds.md](Keybinds.md))
- **JankyBorders** - window borders that pull colors from pywal
- **SketchyBar** - status bar
- **Pywal** - generates color scheme from your wallpaper


## Dependencies

| Tool | Purpose | Install Command |
|------|---------|-----------------|
| yabai | Tiling window manager | `brew install koekeishiya/formulae/yabai` |
| skhd | Hotkey daemon | `brew install koekeishiya/formulae/skhd` |
| borders | Window borders | `brew install FelixKratz/formulae/borders` |
| sketchybar | Status bar | `brew install FelixKratz/formulae/sketchybar` |
| pywal | Color scheme generator | `pip3 install pywal` |

**Optional:** `blueutil` for bluetooth status, `kitty` terminal.

**Python:** Scripts use standard library only, no `requirements.txt` needed.

**Font:** Hack Nerd Font for icons - `brew install --cask font-hack-nerd-font`

## Quick Start (Recommended)

1. **Disable SIP partially** for yabai scripting addition. Follow the [yabai wiki](https://github.com/koekeishiya/yabai/wiki/Disabling-System-Integrity-Protection) guide - requires rebooting into recovery mode.

2. **Run the automated installer:**
   ```bash
   git clone https://github.com/duma799/yabaduma-config.git ~/projects/yabaduma-config
   cd ~/projects/yabaduma-config
   ./install.py
   ```

3. **Post-installation:**
   - Grant accessibility permissions when prompted (System Settings → Privacy & Security → Accessibility)
   - Set a wallpaper: `wal -i /path/to/wallpaper.jpg` or use one from [backgrounds/](backgrounds/)
   - Run `reload-theme` to apply colors

## Manual Installation

```bash
# Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Taps
brew tap koekeishiya/formulae
brew tap FelixKratz/formulae

# Install everything
brew install yabai skhd borders sketchybar
pip3 install pywal

# Clone and link
git clone https://github.com/duma799/yabaduma-config.git ~/projects/yabaduma-config
cd ~/projects/yabaduma-config

ln -sf ~/projects/yabaduma-config/yabairc ~/.yabairc
ln -sf ~/projects/yabaduma-config/skhdrc ~/.skhdrc
mkdir -p ~/.config/skhd
ln -sf ~/projects/yabaduma-config/scripts ~/.config/skhd/scripts
ln -sf ~/projects/yabaduma-config/bordersrc ~/.config/borders/bordersrc
ln -sf ~/projects/yabaduma-config/sketchybar ~/.config/sketchybar

# reload-theme command
mkdir -p ~/.local/bin
ln -sf ~/projects/yabaduma-config/reload-theme.py ~/.local/bin/reload-theme
chmod +x ~/projects/yabaduma-config/reload-theme.py
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc

# Start services
brew services start yabai
brew services start skhd
brew services start borders
brew services start sketchybar
```

After manual install, follow the same post-installation steps as in Quick Start above.



## Usage

```bash
wal -i /path/to/wallpaper.jpg   # set wallpaper + generate colors
reload-theme                     # reload borders and sketchybar
reload-theme /path/to/image.jpg  # both at once
```

Pywal generates colors to `~/.cache/wal/colors.json`. SketchyBar plugins read colors via `colors.py`. Borders reads color6/color4 for the gradient.

To change which colors borders uses, edit `bordersrc`:
```bash
active_color1=$(echo "$color6" | sed 's/#/0xff/')  # try color0-15
active_color2=$(echo "$color4" | sed 's/#/0xff/')
```

## Troubleshooting

**Keybinds not working:** `skhd --restart-service`

**Borders not using pywal colors:** Check `~/.cache/wal/colors.json` exists, then `brew services restart borders`

**Bluetooth shows N/A:** Install blueutil - `brew install blueutil`

**Services acting up:** Restart everything:
```bash
brew services restart yabai skhd borders sketchybar
```

## Links

- [Yabai Wiki](https://github.com/koekeishiya/yabai/wiki)
- [SKHD](https://github.com/koekeishiya/skhd)
- [SketchyBar](https://github.com/FelixKratz/SketchyBar)
- [Pywal](https://github.com/dylanaraps/pywal)
