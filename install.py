#!/usr/bin/env python3
"""
install.py - Minecraft Modpack Installer

Architecture:
  - Imports
  - Mod Dataclass & Configuration
  - Helper Functions
  - Main Execution Flow
"""

import os
import sys
import platform
import urllib.request
import urllib.error
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set

# ==============================================================================
# 1. CONFIGURATION & DATA STRUCTURE
# ==============================================================================

@dataclass
class Mod:
    name: str
    filename: str
    url: str
    required: bool = True
    question: Optional[str] = None
    description: Optional[str] = None

# THIS IS THE ONLY THING YOU EDIT TO CHANGE THE MODPACK LIST
MODS: List[Mod] = [
    # Required Mods
    Mod(
        name="Create: Copycats+",
        filename="copycats-3.0.4+mc.1.21.1-neoforge.jar",
        url="https://cdn.modrinth.com/data/UT2M39wf/versions/kecZ0sl7/copycats-3.0.4%2Bmc.1.21.1-neoforge.jar",
        required=True,
    ),
    Mod(
        name="Create",
        filename="create-1.21.1-6.0.10.jar",
        url="https://cdn.modrinth.com/data/LNytGWDc/versions/UjX6dr61/create-1.21.1-6.0.10.jar",
        required=True,
    ),
    Mod(
        name="Create Aeronautics",
        filename="create-aeronautics-bundled-1.21.1-1.2.1.jar",
        url="https://cdn.modrinth.com/data/oWaK0Q19/versions/YhZLrAFC/create-aeronautics-bundled-1.21.1-1.2.1.jar",
        required=True,
    ),
    Mod(
        name="Create Chain Compat",
        filename="createchaincompat-0.1.0.jar",
        url="https://cdn.modrinth.com/data/rcs3LOu2/versions/47SGcjpY/createchaincompat-0.1.0.jar",
        required=True,
    ),
    Mod(
        name="Create Diesel Generators",
        filename="createdieselgenerators-1.21.1-1.3.14.jar",
        url="https://cdn.modrinth.com/data/ZM3tt6p1/versions/Kijd1iDy/createdieselgenerators-1.21.1-1.3.14.jar",
        required=True,
    ),
    Mod(
        name="Create: New Age",
        filename="create-new-age-1.2.0+neoforge-mc1.21.1.jar",
        url="https://cdn.modrinth.com/data/FTeXqI9v/versions/IwtuwMZy/create-new-age-1.2.0%2Bneoforge-mc1.21.1.jar",
        required=True,
    ),
    Mod(
        name="Curios API",
        filename="curios-neoforge-9.5.1+1.21.1.jar",
        url="https://cdn.modrinth.com/data/vvuO3ImH/versions/yohfFbgD/curios-neoforge-9.5.1%2B1.21.1.jar",
        required=True,
    ),
    Mod(
        name="Farmer's Delight",
        filename="FarmersDelight-1.21.1-1.3.2.jar",
        url="https://cdn.modrinth.com/data/R2OftAxM/versions/GbNuOZ4S/FarmersDelight-1.21.1-1.3.2.jar",
        required=True,
    ),
    Mod(
        name="Forgified Fabric API",
        filename="forgified-fabric-api-0.116.14+2.3.0+1.21.1.jar",
        url="https://cdn.modrinth.com/data/Aqlf1Shp/versions/dAxle9F7/forgified-fabric-api-0.116.14%2B2.3.0%2B1.21.1.jar",
        required=True,
    ),
    Mod(
        name="Lootr",
        filename="lootr-neoforge-1.21.1-1.11.37.122.jar",
        url="https://cdn.modrinth.com/data/EltpO5cN/versions/mDyzapFj/lootr-neoforge-1.21.1-1.11.37.122.jar",
        required=True,
    ),
    Mod(
        name="Create: Steam & Rails",
        filename="railways-0.3.0-beta+neoforge-mc1.21.1.jar",
        url="https://cdn.modrinth.com/data/L3Jv0QZI/versions/mvE5W1r2/railways-0.3.0-beta%2Bneoforge-mc1.21.1.jar",
        required=True,
    ),
    Mod(
        name="Reese's Sodium Options",
        filename="reeses-sodium-options-neoforge-1.8.3+mc1.21.4.jar",
        url="https://cdn.modrinth.com/data/Bh37bMuy/versions/xAiCe6w8/reeses-sodium-options-neoforge-1.8.3%2Bmc1.21.4.jar",
        required=True,
    ),
    Mod(
        name="Sable",
        filename="sable-neoforge-1.21.1-1.2.2.jar",
        url="https://cdn.modrinth.com/data/T9PomCSv/versions/3FMsUjO4/sable-neoforge-1.21.1-1.2.2.jar",
        required=True,
    ),
    Mod(
        name="Sodium Extra",
        filename="sodium-extra-neoforge-0.6.0+mc1.21.1.jar",
        url="https://cdn.modrinth.com/data/PtjYWJkn/versions/pFmw1eci/sodium-extra-neoforge-0.6.0%2Bmc1.21.1.jar",
        required=True,
    ),
    Mod(
        name="Sodium",
        filename="sodium-neoforge-0.6.13+mc1.21.1.jar",
        url="https://cdn.modrinth.com/data/AANobbMI/versions/Pb3OXVqC/sodium-neoforge-0.6.13%2Bmc1.21.1.jar",
        required=True,
    ),
    Mod(
        name="Sophisticated Backpacks",
        filename="sophisticatedbackpacks-1.21.1-3.25.71.1997.jar",
        url="https://cdn.modrinth.com/data/TyCTlI4b/versions/77ZcitZl/sophisticatedbackpacks-1.21.1-3.25.71.1997.jar",
        required=True,
    ),
    Mod(
        name="Sophisticated Core",
        filename="sophisticatedcore-1.21.1-1.4.76.2170.jar",
        url="https://cdn.modrinth.com/data/nmoqTijg/versions/92jCynbj/sophisticatedcore-1.21.1-1.4.76.2170.jar",
        required=True,
    ),

    # Optional Mods
    Mod(
        name="AppleSkin",
        filename="appleskin-neoforge-mc1.21-3.0.9.jar",
        url="https://cdn.modrinth.com/data/EsAfCjCV/versions/uAKA6Laj/appleskin-neoforge-mc1.21-3.0.9.jar",
        required=False,
        question="Install AppleSkin?",
        description="Shows how much hunger and saturation an item will restore on your HUD.",
    ),
    Mod(
        name="Inventory HUD+",
        filename="inventoryhud.neoforged.1.21.1-3.4.28.jar",
        url="https://cdn.modrinth.com/data/Kp2uclYl/versions/gOEEnxa6/inventoryhud.neoforged.1.21.1-3.4.28.jar",
        required=False,
        question="Install Inventory HUD+?",
        description="Displays inventory, armor durability, and status effects on HUD.",
    ),
    Mod(
        name="Iris Shaders",
        filename="iris-neoforge-1.8.12+mc1.21.1.jar",
        url="https://cdn.modrinth.com/data/YL57xq9U/versions/t3ruzodq/iris-neoforge-1.8.12%2Bmc1.21.1.jar",
        required=False,
        question="Install Iris Shaders?",
        description="Adds shaderpack support for enhanced visuals.",
    ),
    Mod(
        name="Jade",
        filename="Jade-1.21.1-NeoForge-15.10.5.jar",
        url="https://cdn.modrinth.com/data/nvQzSEkH/versions/yd8FKCmx/Jade-1.21.1-NeoForge-15.10.5.jar",
        required=False,
        question="Install Jade?",
        description="Displays HUD tooltips for blocks and entities.",
    ),
    Mod(
        name="Just Enough Items (JEI)",
        filename="jei-1.21.1-neoforge-19.39.0.368.jar",
        url="https://cdn.modrinth.com/data/u6dRKJwZ/versions/bEGnP8IF/jei-1.21.1-neoforge-19.39.0.368.jar",
        required=False,
        question="Install Just Enough Items (JEI)?",
        description="Adds recipe viewing and item searching overlay.",
    ),
    Mod(
        name="JourneyMap",
        filename="journeymap-neoforge-1.21.1-6.0.1.jar",
        url="https://cdn.modrinth.com/data/lfHFW1mp/versions/plEVc4Oq/journeymap-neoforge-1.21.1-6.0.1.jar",
        required=False,
        question="Install JourneyMap?",
        description="Adds real-time minimap, full-screen map, and waypoints.",
    ),
    Mod(
        name="LambDynamicLights",
        filename="lambdynamiclights-4.8.10+1.21.1.jar",
        url="https://cdn.modrinth.com/data/yBW8D80W/versions/DZDOX6ps/lambdynamiclights-4.8.10%2B1.21.1.jar",
        required=False,
        question="Install Dynamic Lights?",
        description="Emits dynamic light from handheld items like torches.",
    ),
    Mod(
        name="Locator Bar",
        filename="LocatorBar-neoforge-1.2.1+1.21.1.jar",
        url="https://cdn.modrinth.com/data/BD7N7OcY/versions/W26rnjoZ/LocatorBar-neoforge-1.2.1%2B1.21.1.jar",
        required=False,
        question="Install Locator Bar?",
        description="Adds a bar to the HUD that shows the direction and distance to the nearest waypoint.",
    ),
    Mod(
        name="Ok Zoomer",
        filename="ok_zoomer-neo-10.0.0-beta.13.jar",
        url="https://cdn.modrinth.com/data/aXf2OSFU/versions/AkPuuAgJ/ok_zoomer-neo-10.0.0-beta.13.jar",
        required=False,
        question="Install Ok Zoomer?",
        description="Adds customizable and smooth camera zooming.",
    ),
]


# ==============================================================================
# 2. HELPER FUNCTIONS
# ==============================================================================

def print_header(title: str) -> None:
    """Print a clean visual section header."""
    print()
    print("==================================================")
    print(f"  {title}")
    print("==================================================")
    print()

def print_success(msg: str) -> None:
    """Print a success message with a checkmark indicator."""
    print(f"  [✓] {msg}")

def print_error(msg: str) -> None:
    """Print an error message."""
    print(f"  [✗] {msg}")

def print_info(msg: str) -> None:
    """Print an informational message."""
    print(f"  [•] {msg}")

def ensure_tty_stdin() -> None:
    """Redirect file descriptor 0 (stdin) to the controlling terminal if input is piped (e.g., via curl ... | bash)."""
    if not sys.stdin.isatty():
        try:
            tty_path = "CON" if platform.system() == "Windows" else "/dev/tty"
            tty_fd = os.open(tty_path, os.O_RDONLY)
            os.dup2(tty_fd, 0)
            os.close(tty_fd)
            sys.stdin = open(0, "r", encoding=sys.stdin.encoding or "utf-8", errors="replace")
        except Exception:
            pass

def ask_yes_no(question: str, default: bool = True) -> bool:
    """Prompt the user with a Yes/No question."""
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        try:
            choice = input(f"{question} {suffix} ").strip().lower()
            if not choice:
                return default
            if choice in ("y", "yes"):
                return True
            if choice in ("n", "no"):
                return False
            print("Please enter 'y' or 'n'.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(1)

def get_target_folder() -> Path:
    """Prompt the user for the target download folder path and create it if necessary."""
    while True:
        try:
            path_str = input("Please enter the path to the folder to download the mods into: ").strip()
            if path_str:
                target_path = Path(path_str).expanduser().resolve()
                if not target_path.exists():
                    try:
                        target_path.mkdir(parents=True, exist_ok=True)
                        print_success(f"Created target directory: {target_path}")
                    except Exception as err:
                        print_error(f"Could not create directory '{target_path}': {err}")
                        continue
                elif not target_path.is_dir():
                    print_error(f"The path '{target_path}' exists but is not a directory.")
                    continue

                print_success(f"Target folder set to: {target_path}")
                return target_path
            else:
                print("Path cannot be empty. Please try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(1)

def download_file(url: str, destination_path: Path) -> bool:
    """Download a file with basic progress display."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Minecraft-Modpack-Installer/1.0"}
        )
        with urllib.request.urlopen(req) as response, open(destination_path, "wb") as out_file:
            total_size = response.getheader("Content-Length")
            total_bytes = int(total_size) if total_size and total_size.isdigit() else None
            downloaded = 0
            block_size = 8192

            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                downloaded += len(buffer)
                out_file.write(buffer)

                if total_bytes:
                    percent = (downloaded / total_bytes) * 100
                    sys.stdout.write(f"\r  [↓] Downloading {destination_path.name}... {percent:.1f}%")
                else:
                    sys.stdout.write(f"\r  [↓] Downloading {destination_path.name}... {downloaded} bytes")
                sys.stdout.flush()

        print()  # Newline after download complete
        return True
    except Exception as err:
        print()
        print_error(f"Failed to download {url}: {err}")
        if destination_path.exists():
            destination_path.unlink()
        return False

def verify_download(filepath: Path) -> bool:
    """Verify that the downloaded file exists and is not empty."""
    if filepath.exists() and filepath.stat().st_size > 0:
        return True
    return False

def get_installed_mods(mods_folder: Path) -> Set[str]:
    """Get filenames of all currently installed mods in the mods folder."""
    if not mods_folder.exists():
        return set()
    return {f.name for f in mods_folder.iterdir() if f.is_file()}

def install_mod(mod: Mod, mods_folder: Path) -> str:
    """
    Install a mod if it does not already exist.
    Returns: 'installed', 'skipped', or 'failed'
    """
    target_path = mods_folder / mod.filename

    if target_path.exists() and verify_download(target_path):
        print_info(f"Skipping '{mod.name}' ({mod.filename} already present).")
        return "skipped"

    print_info(f"Installing '{mod.name}'...")
    if download_file(mod.url, target_path) and verify_download(target_path):
        print_success(f"Successfully installed '{mod.name}'.")
        return "installed"
    else:
        print_error(f"Failed to install '{mod.name}'.")
        return "failed"

def disable_unknown_mods(mods_folder: Path, known_filenames: Set[str]) -> int:
    """
    Rename unknown .jar files to .jar.disabled.
    Ignores directories, existing .disabled files, and known filenames.
    """
    if not mods_folder.exists():
        return 0

    disabled_count = 0
    for item in mods_folder.iterdir():
        if item.is_dir():
            continue
        if item.name.endswith(".disabled") or item.name.endswith(".tmp"):
            continue

        if item.name not in known_filenames:
            disabled_name = f"{item.name}.disabled"
            disabled_path = mods_folder / disabled_name
            try:
                item.rename(disabled_path)
                print_info(f"Disabled unknown mod: '{item.name}' -> '{disabled_name}'")
                disabled_count += 1
            except Exception as err:
                print_error(f"Failed to disable '{item.name}': {err}")

    return disabled_count


# ==============================================================================
# 3. MAIN INSTALLER
# ==============================================================================

def main() -> None:
    ensure_tty_stdin()
    print_header("Minecraft Modpack Installer")

    # Prompt user for destination directory
    mods_folder = get_target_folder()

    # Track statistics
    installed_count = 0
    skipped_count = 0
    disabled_count = 0

    # Install Required Mods
    print_header("Installing Required Mods")
    required_mods = [m for m in MODS if m.required]
    for mod in required_mods:
        status = install_mod(mod, mods_folder)
        if status == "installed":
            installed_count += 1
        elif status == "skipped":
            skipped_count += 1

    # Install Optional Mods
    optional_mods = [m for m in MODS if not m.required]
    if optional_mods:
        print_header("Optional Mods")
        for mod in optional_mods:
            print(f"--- {mod.name} ---")
            if mod.description:
                print(f"    {mod.description}")
            question = mod.question or f"Install {mod.name}?"
            if ask_yes_no(question, default=True):
                status = install_mod(mod, mods_folder)
                if status == "installed":
                    installed_count += 1
                elif status == "skipped":
                    skipped_count += 1
            else:
                print_info(f"Skipped optional mod '{mod.name}'.")
                skipped_count += 1
            print()

    # Disable Unknown Mods
    print_header("Disabling Unknown Mods")
    known_filenames = {mod.filename for mod in MODS}
    disabled_count = disable_unknown_mods(mods_folder, known_filenames)
    if disabled_count == 0:
        print_info("No unknown mods to disable.")

    # Summary
    print_header("Installation Summary")
    print(f"  Target Folder:  {mods_folder}")
    print(f"  Installed Mods: {installed_count}")
    print(f"  Skipped Mods:   {skipped_count}")
    print(f"  Disabled Mods:  {disabled_count}")
    print()

if __name__ == "__main__":
    main()
