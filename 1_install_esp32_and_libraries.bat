@echo off
setlocal enabledelayedexpansion
title Setup ESP32 Core and Libraries for Any Laptop

echo =========================================================================
echo STEP 1: Installing ESP32 Board Core (v3.0.7) and Required Libraries
echo =========================================================================
echo This script works on ANY Windows laptop:
echo   - Runs portable standalone Arduino CLI engine (no manual install needed)
echo   - Adds official Espressif ESP32 package repository
echo   - Installs ESP32 Board Core v3.0.7 + esptool flasher
echo   - Installs all 5 sensor libraries (MAX30102, DS18B20, HX711, LCD, OneWire)
echo =========================================================================
echo.

set "TOOL_DIR=%~dp0tools"
set "CLI=%TOOL_DIR%\arduino-cli.exe"

:: 1. Check portable arduino-cli.exe in project tools folder
if not exist "%CLI%" (
    if exist "%LOCALAPPDATA%\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe" (
        set "CLI=%LOCALAPPDATA%\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
    )
)
if not exist "%CLI%" (
    if exist "C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe" (
        set "CLI=C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
    )
)
if not exist "%CLI%" (
    where arduino-cli >nul 2>nul
    if !errorlevel! equ 0 (
        for /f "delims=" %%i in ('where arduino-cli') do set "CLI=%%i"
    )
)

:: 2. If not found on the laptop, auto-download standalone portable engine
if not exist "%CLI%" (
    echo [INFO] Standalone engine not found in system paths.
    echo [INFO] Auto-downloading portable Arduino CLI engine for this laptop...
    if not exist "%TOOL_DIR%" mkdir "%TOOL_DIR%"
    powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip' -OutFile '%TOOL_DIR%\cli.zip'; Expand-Archive '%TOOL_DIR%\cli.zip' -DestinationPath '%TOOL_DIR%' -Force; Get-ChildItem -Path '%TOOL_DIR%' -Filter 'arduino-cli.exe' -Recurse | Select-Object -First 1 | ForEach-Object { Copy-Item $_.FullName '%TOOL_DIR%\arduino-cli.exe' -Force }; Remove-Item '%TOOL_DIR%\cli.zip' -Force -ErrorAction SilentlyContinue"
    set "CLI=%TOOL_DIR%\arduino-cli.exe"
)

if not exist "%CLI%" (
    echo.
    echo [ERROR] Could not initialize Arduino engine!
    echo Please ensure this laptop has an internet connection or copy the
    echo 'tools' folder from your main computer.
    echo.
    pause
    exit /b 1
)

echo [OK] Active Arduino Engine: %CLI%
echo.

set ESP32_URL=https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

echo [1/3] Updating ESP32 Board Repository Index from Espressif...
"%CLI%" core update-index --additional-urls %ESP32_URL%

echo.
echo [2/3] Installing Stable ESP32 Board Core (v3.0.7) and esptool...
echo (Downloading compiler toolchain, headers, and board definitions - please wait)...
"%CLI%" core install esp32:esp32@3.0.7 --additional-urls %ESP32_URL%

echo.
echo [3/3] Installing 5 Required Medical Sensor Libraries...
"%CLI%" lib install "LiquidCrystal"
"%CLI%" lib install "SparkFun MAX3010x Pulse and Proximity Sensor Library"
"%CLI%" lib install "DallasTemperature"
"%CLI%" lib install "OneWire"
"%CLI%" lib install "HX711"

echo.
echo =========================================================================
echo [SUCCESS] ESP32 Core, Compiler, Tools, and Libraries Installed!
echo =========================================================================
echo Next Step:
echo You can now run '2_erase_esp32_memory.bat' to format your ESP32,
echo followed by '3_upload_esp32_firmware.bat' to upload the firmware!
echo =========================================================================
echo.
pause
