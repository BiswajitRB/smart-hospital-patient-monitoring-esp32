@echo off
echo =========================================================================
echo STEP 2: Compiling and Uploading Code to ESP32
echo =========================================================================

set CLI="C:\Users\%USERNAME%\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
set SKETCH_DIR=%~dp0Smart_Hospital_ESP32
set PORT=COM5
set FQBN=esp32:esp32:esp32

if not exist %CLI% (
    echo [ERROR] arduino-cli.exe not found at %CLI%
    pause
    exit /b 1
)

if not exist "%SKETCH_DIR%" (
    echo [ERROR] Could not find folder: "%SKETCH_DIR%"
    pause
    exit /b 1
)

echo.
echo [1/2] Compiling Smart Hospital Bedside System Sketch...
echo Path: "%SKETCH_DIR%"
%CLI% compile --fqbn %FQBN% "%SKETCH_DIR%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Compilation failed. Please check the error output above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Uploading Firmware to ESP32 on %PORT%...
echo (NOTE: If it stays on Connecting..., press and hold the BOOT button for 2 seconds)
%CLI% upload -p %PORT% --fqbn %FQBN% "%SKETCH_DIR%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =========================================================================
    echo [SUCCESS] FIRMWARE UPLOADED TO ESP32 SUCCESSFULLY!
    echo =========================================================================
) else (
    echo.
    echo [UPLOAD FAILED] Please check your USB cable and COM port.
)

pause
