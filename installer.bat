@echo off
setlocal enabledelayedexpansion

title Aeronotics Modpack Installer

echo.
echo ===========================================
echo       Aeronotics Modpack Installer
echo ===========================================
echo.

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    where python3 >nul 2>nul
    if %errorlevel% neq 0 (
        echo [X] Python was not found on your system.
        echo.
        echo Please install Python 3 from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        echo.
        pause
        exit /b 1
    ) else (
        set "PY_CMD=python3"
    )
) else (
    set "PY_CMD=python"
)

echo [OK] Python found (%PY_CMD%).

:: Create temporary directory
set "TMP_DIR=%TEMP%\aeronautics_installer_%RANDOM%"
mkdir "%TMP_DIR%" 2>nul

set "INSTALLER_URL=https://raw.githubusercontent.com/BlackSnowman13/snowglobe-stuff/refs/heads/main/install.py"
set "TARGET_PY=%TMP_DIR%\install.py"

echo.
echo Downloading installer...

:: Try downloading via curl or powershell fallback
where curl >nul 2>nul
if %errorlevel% equ 0 (
    curl -fsSL "%INSTALLER_URL%" -o "%TARGET_PY%"
) else (
    powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('%INSTALLER_URL%', '%TARGET_PY%')"
)

if not exist "%TARGET_PY%" (
    echo.
    echo [X] Failed to download installer.
    echo Please check your internet connection.
    echo.
    pause
    exit /b 1
)

echo [OK] Download complete.
echo.

:: Execute Python installer
"%PY_CMD%" "%TARGET_PY%"

:: Cleanup
rmdir /s /q "%TMP_DIR%" 2>nul

echo.
echo Installer finished.
pause
