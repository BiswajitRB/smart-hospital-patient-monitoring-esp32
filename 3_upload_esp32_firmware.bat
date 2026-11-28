@echo off
setlocal
title ESP32 Smart Hospital - Compile and Upload Tool

echo =========================================================================
echo       APOLLO SMART HOSPITAL - 1-CLICK ESP32 FIRMWARE UPLOADER
echo =========================================================================
echo This tool compiles and flashes the Smart Hospital firmware directly.
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

:: 1. Search if 1_install_esp32_and_libraries.bat already downloaded it in Temp
if not defined CLI (
    echo [INFO] Searching for Arduino engine downloaded by Step 1...
    for /f "delims=" %%f in ('powershell -NoProfile -Command "Get-ChildItem -Path $env:LOCALAPPDATA -Filter 'arduino-cli.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName -First 1"') do (
        set "CLI=%%f"
    )
)

:: 2. Auto-fetch standalone engine directly if still missing
if not defined CLI (
    echo [INFO] Auto-fetching standalone portable engine (takes ~5 seconds)...
    if not exist "%LOCALAPPDATA%\ArduinoCLI" mkdir "%LOCALAPPDATA%\ArduinoCLI"
    powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip' -OutFile '%LOCALAPPDATA%\ArduinoCLI\cli.zip'; Expand-Archive '%LOCALAPPDATA%\ArduinoCLI\cli.zip' -DestinationPath '%LOCALAPPDATA%\ArduinoCLI' -Force; Get-ChildItem -Path '%LOCALAPPDATA%\ArduinoCLI' -Filter 'arduino-cli.exe' -Recurse | Select-Object -First 1 | ForEach-Object { Copy-Item $_.FullName '%LOCALAPPDATA%\ArduinoCLI\arduino-cli.exe' -Force }; Remove-Item '%LOCALAPPDATA%\ArduinoCLI\cli.zip' -Force -ErrorAction SilentlyContinue"
    if exist "%LOCALAPPDATA%\ArduinoCLI\arduino-cli.exe" set "CLI=%LOCALAPPDATA%\ArduinoCLI\arduino-cli.exe"
)

if not defined CLI (
    echo.
    echo [ERROR] arduino-cli.exe engine could not be initialized!
    echo Please ensure this laptop has an active internet connection.
    echo.
    pause
    exit /b 1
)

echo [OK] Active Arduino Engine: %CLI%
echo.

set SKETCH_PATH="%~dp0Smart_Hospital_ESP32"

if not exist %SKETCH_PATH% (
    echo.
    echo [WARNING] The sketch folder 'Smart_Hospital_ESP32' was not found next to this script!
    echo (This happens if you run directly inside a ZIP file without extracting it first).
    echo.
    echo PLEASE DO THIS:
    echo 1. Right-click the downloaded zip file in Downloads
    echo 2. Click 'Extract All...' and click 'Extract'
    echo 3. Open the extracted folder and run this file again!
    echo.
    pause
    exit /b 1
)

echo [1/2] Compiling ESP32 sketch with HX711, MAX30102, DS18B20...
"%CLI%" compile --fqbn esp32:esp32:esp32 %SKETCH_PATH%

if errorlevel 1 (
    echo.
    echo [ERROR] Compilation failed!
    echo Checking core and libraries...
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
