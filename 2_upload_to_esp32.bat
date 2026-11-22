@echo off
echo =========================================================================
echo STEP 2: Compiling & Uploading Code to ESP32 (COM5)
echo =========================================================================

set CLI="C:\Users\%USERNAME%\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
set SKETCH_DIR=D:\a-hospital project\Smart_Hospital_ESP32
set PORT=COM5
set FQBN=esp32:esp32:esp32

if not exist %CLI% (
    echo [ERROR] arduino-cli.exe not found.
    pause
    exit /b 1
)

echo.
echo [1/2] Compiling Smart Hospital Bedside System Sketch...
%CLI% compile --fqbn %FQBN% "%SKETCH_DIR%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Compilation failed. Please check the error messages above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Uploading Firmware to ESP32 on %PORT%...
echo (NOTE: If it gets stuck on Connecting..., press & hold BOOT button for 2s)
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
