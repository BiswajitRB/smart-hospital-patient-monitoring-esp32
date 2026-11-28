@echo off
setlocal enabledelayedexpansion
title Setup ESP32 Core and Libraries for Arduino IDE

echo =========================================================================
echo STEP 1: Installing ESP32 Board Core (v3.0.7) and Required Libraries
echo =========================================================================
echo This script sets up a fresh laptop with everything needed for the project:
echo   - Adds Espressif ESP32 package repository
echo   - Installs ESP32 Board Core v3.0.7 + esptool flasher
echo   - Installs all 5 sensor libraries (MAX30102, DS18B20, HX711, LCD, OneWire)
echo =========================================================================
echo.

:: 1. Search for arduino-cli.exe across standard installation paths
set CLI=
if exist "%LOCALAPPDATA%\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe" (
    set "CLI=%LOCALAPPDATA%\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
)
if "%CLI%"=="" (
    if exist "C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe" (
        set "CLI=C:\Program Files\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
    )
)
if "%CLI%"=="" (
    where arduino-cli >nul 2>nul
    if %errorlevel% equ 0 (
        for /f "delims=" %%i in ('where arduino-cli') do set "CLI=%%i"
    )
)

if "%CLI%"=="" (
    echo [ERROR] arduino-cli.exe not found!
    echo Please verify that Arduino IDE 2.x is installed on this laptop.
    echo Default expected path: %LOCALAPPDATA%\Programs\Arduino IDE
    echo.
    pause
    exit /b 1
)

echo [OK] Found Arduino Engine at: !CLI!
echo.

set ESP32_URL=https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

echo [1/3] Updating ESP32 Package Index from Espressif...
"!CLI!" core update-index --additional-urls %ESP32_URL%

echo.
echo [2/3] Installing Stable ESP32 Board Core (v3.0.7) and esptool...
echo (This downloads the compiler, esptool, and ESP32 board definitions - please wait)...
"!CLI!" core install esp32:esp32@3.0.7 --additional-urls %ESP32_URL%

echo.
echo [3/3] Installing 5 Required Medical Sensor Libraries...
"!CLI!" lib install "LiquidCrystal"
"!CLI!" lib install "SparkFun MAX3010x Pulse and Proximity Sensor Library"
"!CLI!" lib install "DallasTemperature"
"!CLI!" lib install "OneWire"
"!CLI!" lib install "HX711"

echo.
echo =========================================================================
echo [SUCCESS] ESP32 Core, Compiler, Tools, and Libraries Installed!
echo =========================================================================
echo Next Step:
echo You can now run '2_erase_esp32_memory.bat' to format your ESP32!
echo =========================================================================
echo.
pause
