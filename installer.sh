#!/usr/bin/env bash

set -euo pipefail

# ==========================================================
# Modpack Installer Bootstrap
# ==========================================================

# CHANGE THIS TO YOUR RAW GITHUB LINK
INSTALLER_URL="https://raw.githubusercontent.com/BlackSnowman13/snowglobe-stuff/refs/heads/main/install.py"

echo
echo "==========================================="
echo "      Aeronotics Modpack Installer"
echo "==========================================="
echo

# Check for Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 was not found."
    echo
    echo "Please install Python 3 and run this installer again."
    echo
    exit 1
fi

echo "✓ Python found."

# Check for curl
if ! command -v curl >/dev/null 2>&1; then
    echo
    echo "curl is required but is not installed."
    echo
    exit 1
fi

echo "✓ curl found."

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

echo
echo "Downloading installer..."

if ! curl -fsSL "$INSTALLER_URL" -o "$TMP_DIR/install.py"; then
    echo
    echo "Failed to download installer."
    echo "Please check your internet connection."
    exit 1
fi

echo "✓ Download complete."
echo

python3 "$TMP_DIR/install.py"

echo
echo "Installer finished."