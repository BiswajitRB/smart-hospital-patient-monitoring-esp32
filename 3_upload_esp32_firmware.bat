@echo off
setlocal enabledelayedexpansion
title ESP32 Smart Hospital - Compile and Upload Tool

echo =========================================================================
echo       APOLLO SMART HOSPITAL - 1-CLICK ESP32 FIRMWARE UPLOADER
echo =========================================================================
echo.

set CLI="C:\Users\%USERNAME%\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
set SKETCH_PATH="%~dp0Smart_Hospital_ESP32"

if not exist %CLI% (
    echo [ERROR] arduino-cli.exe not found at %CLI%
    echo Please open 'Smart_Hospital_ESP32.ino' directly in Arduino IDE to upload.
    pause
    exit /b 1
)

echo [1/2] Compiling ESP32 sketch with HX711, MAX30102, DS18B20...
%CLI% compile --fqbn esp32:esp32:esp32 %SKETCH_PATH%

if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed! Check code or library installations.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Firmware compiled cleanly!
echo.
echo Make sure your ESP32 is plugged in via USB!
echo.
set /p COMPORT="Enter your ESP32 COM port (e.g. COM3, COM4, COM5): "

if "%COMPORT%"=="" (
    echo [INFO] No COM port typed, trying auto-detect upload...
    %CLI% upload --fqbn esp32:esp32:esp32 %SKETCH_PATH%
) else (
    echo [2/2] Uploading firmware to ESP32 on %COMPORT%...
    %CLI% upload -p %COMPORT% --fqbn esp32:esp32:esp32 %SKETCH_PATH%
)

if %errorlevel% equ 0 (
    echo.
    echo =========================================================================
    echo [CONGRATULATIONS] ESP32 Programmed Successfully!
    echo =========================================================================
    echo 1. Open Serial Monitor at 115200 baud to see live vitals.
    echo 2. Open https://smart-hospital-web.vercel.app to view your live dashboard!
    echo =========================================================================
) else (
    echo.
    echo [NOTE] If upload failed with "Connecting...", hold the BOOT button on
    echo        the ESP32 board for 2 seconds when uploading begins.
)

echo.
pause
