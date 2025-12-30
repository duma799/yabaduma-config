#!/usr/bin/env python3

import datetime
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_DIR = Path(__file__).parent.resolve()
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP_DIR = Path.home() / ".config" / f"yabaduma-backup-{TIMESTAMP}"

GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def log(msg):
    print(f"{BLUE}[INFO]{NC} {msg}")


def success(msg):
    print(f"{GREEN}[SUCCESS]{NC} {msg}")


def warn(msg):
    print(f"{YELLOW}[WARNING]{NC} {msg}")


def run_cmd(cmd, shell=False):
    result = subprocess.run(cmd, shell=shell, text=True)
    return result.returncode == 0


def run_cmd_or_exit(cmd, shell=False):
    if not run_cmd(cmd, shell):
        print(f"Error executing command: {cmd}")
        sys.exit(1)


def check_brew_package(package_name):
    result = subprocess.run(
        ["brew", "list", "--formula"], capture_output=True, text=True
    )
    return package_name in result.stdout.split()


def check_cask(cask_name):
    result = subprocess.run(["brew", "list", "--cask"], capture_output=True, text=True)
    return cask_name in result.stdout.split()


def install_dependencies():
    log("Checking prerequisites...")
    if not shutil.which("brew"):
        warn("Homebrew not found. Installing...")
        run_cmd_or_exit(
            '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
            shell=True,
        )
    else:
        success("Homebrew is installed.")

    log("Tapping repositories...")
    run_cmd_or_exit(["brew", "tap", "koekeishiya/formulae"])
    run_cmd_or_exit(["brew", "tap", "FelixKratz/formulae"])

    packages = [
        "koekeishiya/formulae/yabai",
        "koekeishiya/formulae/skhd",
        "FelixKratz/formulae/borders",
        "FelixKratz/formulae/sketchybar",
        "blueutil",
        "jq",
    ]

    log("Installing dependencies...")
    for pkg in packages:
        pkg_name = pkg.split("/")[-1]

        if check_brew_package(pkg_name):
            log(f"{pkg_name} is already installed.")
        else:
            log(f"Installing {pkg}...")
            run_cmd_or_exit(["brew", "install", pkg])

    font = "font-hack-nerd-font"
    if check_cask(font):
        log(f"{font} is already installed.")
    else:
        log(f"Installing {font}...")
        run_cmd_or_exit(["brew", "install", "--cask", font])

    if not shutil.which("wal"):
        log("Installing pywal...")
        run_cmd_or_exit([sys.executable, "-m", "pip", "install", "pywal"])
    else:
        success("pywal is installed.")


def expand_path(path_str):
    return Path(os.path.expanduser(path_str))


def backup_and_link(src, dest):
    src = Path(src)
    dest = expand_path(str(dest))

    dest_dir = dest.parent

    if dest.exists() or dest.is_symlink():
        shutil.move(str(dest), str(BACKUP_DIR))

    dest_dir.mkdir(parents=True, exist_ok=True)
    os.symlink(src, dest)
    success(f"Linked {src} -> {dest}")


def setup_files():
    log(f"Backing up existing configs to {BACKUP_DIR}...")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    backup_and_link(REPO_DIR / "yabairc", Path.home() / ".yabairc")
    backup_and_link(REPO_DIR / "skhdrc", Path.home() / ".skhdrc")
    backup_and_link(
        REPO_DIR / "bordersrc", Path.home() / ".config" / "borders" / "bordersrc"
    )
    backup_and_link(REPO_DIR / "sketchybar", Path.home() / ".config" / "sketchybar")
    backup_and_link(REPO_DIR / "scripts", Path.home() / ".config" / "skhd" / "scripts")

    log("Setting up globally accessible scripts...")
    local_bin = Path.home() / ".local" / "bin"
    local_bin.mkdir(parents=True, exist_ok=True)

    reload_theme_src = REPO_DIR / "reload-theme.py"
    reload_theme_dest = local_bin / "reload-theme"

    backup_and_link(reload_theme_src, reload_theme_dest)

    reload_theme_src.chmod(reload_theme_src.stat().st_mode | 0o111)

    if str(local_bin) not in os.environ["PATH"]:
        warn(f"Ensure {local_bin} is in your PATH. Add this to your shell rc:")
        print(f'export PATH="{local_bin}:$PATH"')


def start_services():
    log("Starting services...")
    services = [
        "koekeishiya/formulae/yabai",
        "koekeishiya/formulae/skhd",
        "FelixKratz/formulae/borders",
        "FelixKratz/formulae/sketchybar",
    ]

    for service in services:
        short_name = service.split("/")[-1]
        log(f"Restarting {short_name}...")

        if run_cmd(["brew", "services", "restart", service]):
            continue

        log(f"Trying short name {short_name}...")
        if run_cmd(["brew", "services", "restart", short_name]):
            continue

        if short_name in ["yabai", "skhd"]:
            log(f"Trying {short_name} --restart-service...")
            if run_cmd([short_name, "--restart-service"]):
                continue

        warn(
            f"Failed to restart {short_name}. Run 'brew services restart {short_name}' manually."
        )


def main():
    try:
        install_dependencies()
        setup_files()
        start_services()

        success("Installation complete!")
        print("")
        print("Next steps:")
        print("1. Grant Accessibility permissions to yabai and skhd if prompted.")
        print("2. Set a wallpaper to generate colors: wal -i /path/to/img.jpg")
        print("3. Run 'reload-theme' to apply colors.")

    except KeyboardInterrupt:
        print("\nInstallation aborted.")
        sys.exit(1)


if __name__ == "__main__":
    main()
