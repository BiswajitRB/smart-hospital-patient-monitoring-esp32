@echo off
setlocal enabledelayedexpansion
title ESP32 Flash Memory Erase Tool

echo =========================================================================
echo             ESP32 COMPLETE MEMORY ERASE / FACTORY RESET
echo =========================================================================
echo This tool will completely wipe the ESP32 flash memory:
echo   - Clears old sketches and corrupt program data
echo   - Clears old saved Wi-Fi credentials and NVS partition
echo   - Restores the ESP32 to clean, empty factory state
echo =========================================================================
echo.

:: 1. Search for esptool.exe in Arduino15 directory
set ESPTOOL=
if exist "%LOCALAPPDATA%\Arduino15\packages\esp32\tools\esptool_py\4.5.1\esptool.exe" (
    set "ESPTOOL=%LOCALAPPDATA%\Arduino15\packages\esp32\tools\esptool_py\4.5.1\esptool.exe"
)

if "%ESPTOOL%"=="" (
    for /d %%D in ("%LOCALAPPDATA%\Arduino15\packages\esp32\tools\esptool_py\*") do (
        if exist "%%D\esptool.exe" set "ESPTOOL=%%D\esptool.exe"
    )
)

if "%ESPTOOL%"=="" (
    echo [INFO] Searching system for esptool...
    where esptool.exe >nul 2>nul
    if %errorlevel% equ 0 (
        for /f "delims=" %%i in ('where esptool.exe') do set "ESPTOOL=%%i"
    )
)

if "%ESPTOOL%"=="" (
    echo [INFO] Checking python esptool module...
    python -m esptool version >nul 2>nul
    if %errorlevel% equ 0 (
        set "ESPTOOL=python -m esptool"
    )
)

if "%ESPTOOL%"=="" (
    echo [ERROR] esptool.exe not found!
    echo Please make sure Arduino IDE and ESP32 board support are installed.
    echo (You can run '1_install_esp32_and_libraries.bat' to install them).
    echo.
    pause
    exit /b 1
)

echo [OK] Found esptool: %ESPTOOL%
echo.
echo Make sure your ESP32 is plugged into your laptop via USB cable!
echo.
echo [NOTE] If connecting hangs at "Connecting........_____.....",
echo        press and hold the "BOOT" button on the ESP32 for 2 seconds.
echo.

set /p COMPORT="Enter COM port (e.g. COM3, COM5) or press ENTER for Auto-Detect: "

echo.
echo Erasing ESP32 Flash Memory... Please wait.
echo.

if "%COMPORT%"=="" (
    %ESPTOOL% erase_flash
) else (
    %ESPTOOL% --port %COMPORT% erase_flash
)

if %errorlevel% equ 0 (
    echo.
    echo =========================================================================
    echo [SUCCESS] ESP32 Memory is completely EMPTY and FRESH!
    echo =========================================================================
    echo You can now open Arduino IDE and upload your 'Smart_Hospital_ESP32.ino' sketch!
    echo =========================================================================
) else (
    echo.
    echo =========================================================================
    echo [WARNING] Erase process encountered an issue.
    echo 1. Ensure your ESP32 USB cable supports DATA (not just charging).
    echo 2. Check Device Manager -> Ports (COM & LPT) to see your COM port number.
    echo 3. Hold down the "BOOT" button on your ESP32 while it says "Connecting...".
    echo =========================================================================
)

echo.
pause
