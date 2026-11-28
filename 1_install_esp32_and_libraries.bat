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

set "GLOBAL_CLI=%LOCALAPPDATA%\ArduinoCLI\arduino-cli.exe"
set "LOCAL_CLI=%~dp0tools\arduino-cli.exe"

set "CLI="
if exist "%LOCAL_CLI%" set "CLI=%LOCAL_CLI%"
if not defined CLI if exist "%GLOBAL_CLI%" set "CLI=%GLOBAL_CLI%"
if not defined CLI if exist "%LOCALAPPDATA%\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe" set "CLI=%LOCALAPPDATA%\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
if not defined CLI if exist "C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe" set "CLI=C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"

if not defined CLI (
    where arduino-cli >nul 2>nul
    if !errorlevel! equ 0 (
        for /f "delims=" %%i in ('where arduino-cli') do set "CLI=%%i"
    )
)

:: Auto-download standalone engine permanently to LOCALAPPDATA and tools
if not defined CLI (
    echo [INFO] Standalone engine not found in system paths.
    echo [INFO] Auto-downloading portable Arduino CLI engine for this laptop...
    if not exist "%LOCALAPPDATA%\ArduinoCLI" mkdir "%LOCALAPPDATA%\ArduinoCLI"
    if not exist "%~dp0tools" mkdir "%~dp0tools"
    powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip' -OutFile '%LOCALAPPDATA%\ArduinoCLI\cli.zip'; Expand-Archive '%LOCALAPPDATA%\ArduinoCLI\cli.zip' -DestinationPath '%LOCALAPPDATA%\ArduinoCLI' -Force; Get-ChildItem -Path '%LOCALAPPDATA%\ArduinoCLI' -Filter 'arduino-cli.exe' -Recurse | Select-Object -First 1 | ForEach-Object { Copy-Item $_.FullName '%LOCALAPPDATA%\ArduinoCLI\arduino-cli.exe' -Force; Copy-Item $_.FullName '%~dp0tools\arduino-cli.exe' -Force -ErrorAction SilentlyContinue }; Remove-Item '%LOCALAPPDATA%\ArduinoCLI\cli.zip' -Force -ErrorAction SilentlyContinue"
    if exist "%LOCALAPPDATA%\ArduinoCLI\arduino-cli.exe" set "CLI=%LOCALAPPDATA%\ArduinoCLI\arduino-cli.exe"
    if exist "%LOCAL_CLI%" set "CLI=%LOCAL_CLI%"
)

if not defined CLI (
    echo.
    echo [ERROR] Could not initialize Arduino engine!
    echo Please ensure this laptop has an internet connection or copy the
    echo 'tools' folder from your main computer.
    echo.
    pause
    exit /b 1
)

:: Keep a copy in both places so 3_upload_esp32_firmware.bat always finds it
if not exist "%LOCALAPPDATA%\ArduinoCLI" mkdir "%LOCALAPPDATA%\ArduinoCLI"
if not exist "%GLOBAL_CLI%" copy /y "%CLI%" "%GLOBAL_CLI%" >nul 2>nul

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
echo You can now run '3_upload_esp32_firmware.bat' to upload the firmware!
echo =========================================================================
echo.
pause
