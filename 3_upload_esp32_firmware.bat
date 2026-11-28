@echo off
setlocal
title ESP32 Smart Hospital - Compile and Upload Tool

echo =========================================================================
echo       APOLLO SMART HOSPITAL - 1-CLICK ESP32 FIRMWARE UPLOADER
echo =========================================================================
echo This tool compiles and flashes the Smart Hospital firmware on ANY laptop.
echo =========================================================================
echo.

set "TOOL_DIR=%~dp0tools"
set "CLI=%TOOL_DIR%\arduino-cli.exe"

:: 1. Search for portable arduino-cli.exe in project tools folder first
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

if not exist "%CLI%" (
    echo [ERROR] arduino-cli.exe not found!
    echo Please run '1_install_esp32_and_libraries.bat' first to set up tools.
    echo.
    pause
    exit /b 1
)

echo [OK] Active Arduino Engine: %CLI%
echo.

set SKETCH_PATH="%~dp0Smart_Hospital_ESP32"

echo [1/2] Compiling ESP32 sketch with HX711, MAX30102, DS18B20...
"%CLI%" compile --fqbn esp32:esp32:esp32 %SKETCH_PATH%

if errorlevel 1 (
    echo.
    echo [ERROR] Compilation failed!
    echo Please run '1_install_esp32_and_libraries.bat' to ensure libraries are installed.
    echo.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Firmware compiled cleanly into binary!
echo.

:: Detect connected COM ports
echo Scanning for connected USB serial devices...
set "DETECTED_PORTS="
for /f "tokens=*" %%p in ('%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "[System.IO.Ports.SerialPort]::GetPortNames() -join ' '"') do set "DETECTED_PORTS=%%p"

if not "%DETECTED_PORTS%"=="" (
    echo [FOUND] Connected COM Ports: %DETECTED_PORTS%
) else (
    echo [NOTICE] No COM port detected yet.
    echo          Please plug your ESP32 into a USB port on this laptop.
)

echo.
echo NOTE: If upload displays "Connecting........_____.....",
echo       HOLD the physical "BOOT" button on your ESP32 board for 2 seconds!
echo.

set "COMPORT="
set /p "COMPORT=Enter your ESP32 COM port (e.g. COM3, COM4) or press ENTER for Auto: "

if defined COMPORT set "COMPORT=%COMPORT: =%"

if not defined COMPORT (
    echo [2/2] Auto-detecting port and uploading firmware...
    "%CLI%" upload --fqbn esp32:esp32:esp32 %SKETCH_PATH%
) else (
    echo [2/2] Uploading firmware to ESP32 on %COMPORT%...
    "%CLI%" upload -p %COMPORT% --fqbn esp32:esp32:esp32 %SKETCH_PATH%
)

if errorlevel 1 goto UPLOAD_FAILED

echo.
echo =========================================================================
echo [CONGRATULATIONS] ESP32 Programmed and Active!
echo =========================================================================
echo 1. Your 16x2 LCD should now display: "Smart Hospital / Bed 04"
echo 2. Access Point "Smart-Hospital-Bed04" (pass: hospital123) is broadcasting.
echo 3. Live Cloud Web Dashboard: https://smart-hospital-web.vercel.app
echo =========================================================================
goto FINISHED

:UPLOAD_FAILED
echo.
echo =========================================================================
echo [TROUBLESHOOTING TIPS]
echo 1. Make sure your USB cable is a DATA cable.
echo 2. Check Device Manager to verify the correct COM port.
echo 3. When you see "Connecting........_____.....", HOLD the "BOOT" button on
echo    the ESP32 board for 2 seconds.
echo =========================================================================
goto FINISHED

:FINISHED
echo.
pause
