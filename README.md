# YabaDuma Config

MacOS tiling WM setup. Yabai + PyWal theming.

**Tested on MacBook Air M4, macOS 26.2 Tahoe.**

## What's in here

- **Yabai** - tiling WM (BSP layout)
- **SKHD** - keyboard shortcuts (see [Keybinds.md](Keybinds.md))
- **JankyBorders** - window borders that pull colors from pywal
- **SketchyBar** - status bar (workspaces, clock, volume, battery, bluetooth)
- **Pywal** - generates color scheme from your wallpaper

Window opacity: active 1.0, inactive 0.9. No animations (macOS doesn't support it through yabai).

4-finger gestures work for switching workspaces.

## Dependencies

| Tool | Purpose | Install Command |
|------|---------|-----------------|
| yabai | Tiling window manager | `brew install koekeishiya/formulae/yabai` |
| skhd | Hotkey daemon | `brew install koekeishiya/formulae/skhd` |
| borders | Window borders | `brew install FelixKratz/formulae/borders` |
| sketchybar | Status bar | `brew install FelixKratz/formulae/sketchybar` |
| pywal | Color scheme generator | `pip3 install pywal` |

**Optional:** `blueutil` for bluetooth status, `kitty` terminal.

**Font:** Hack Nerd Font for icons - `brew install --cask font-hack-nerd-font`

## Installation

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

After install:
- Disable SIP partially for yabai scripting addition ([yabai wiki](https://github.com/koekeishiya/yabai/wiki/Disabling-System-Integrity-Protection))
- Grant accessibility permissions to yabai and skhd (System Settings → Privacy & Security → Accessibility)
- Set a wallpaper: `wal -i /path/to/wallpaper.jpg`
- Run `reload-theme`

## Usage

```bash
wal -i /path/to/wallpaper.jpg   # set wallpaper + generate colors
reload-theme                     # reload borders and sketchybar
reload-theme /path/to/image.jpg  # both at once
```

Pywal generates colors to `~/.cache/wal/colors.sh`. Borders reads color6/color4 for the gradient. SketchyBar picks up the rest.

To change which colors borders uses, edit `bordersrc`:
```bash
active_color1=$(echo "$color6" | sed 's/#/0xff/')  # try color0-15
active_color2=$(echo "$color4" | sed 's/#/0xff/')
```

## Files

```
yabaduma-config/
├── yabairc              # yabai config
├── skhdrc               # skhd keybinds
├── bordersrc            # borders config (sources pywal)
├── reload-theme.py      # reloads borders + sketchybar
├── scripts/             # helper scripts for skhd
└── sketchybar/
    ├── sketchybarrc     # main config
    ├── colors.sh        # pywal color loader
    └── plugins/         # bar widgets
```

## Troubleshooting

**Keybinds not working:** `skhd --restart-service`

**Borders not using pywal colors:** Check `~/.cache/wal/colors.sh` exists, then `brew services restart borders`

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
