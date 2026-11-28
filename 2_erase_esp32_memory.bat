@echo off
setlocal
title ESP32 Flash Memory Format and Factory Reset Tool

echo =========================================================================
echo             ESP32 COMPLETE MEMORY FORMAT / FACTORY RESET
echo =========================================================================
echo This tool works on ANY Windows laptop without needing Arduino IDE:
echo   [1] Clears all old firmware, flash memory, and corrupt programs
echo   [2] Clears old Wi-Fi credentials, IP bindings, and NVS storage
echo   [3] Restores the ESP32 to 100 percent fresh, factory-clean empty state
echo =========================================================================
echo.

set "TOOL_DIR=%~dp0tools"
set "ESPTOOL=%TOOL_DIR%\esptool.exe"

if exist "%ESPTOOL%" goto ESPTOOL_READY

echo [INFO] Flasher tool not found locally.
echo [INFO] Auto-downloading standalone portable esptool flasher...
if not exist "%TOOL_DIR%" mkdir "%TOOL_DIR%"
powershell -NoProfile -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/espressif/esptool/releases/download/v4.8.1/esptool-v4.8.1-win64.zip' -OutFile '%TOOL_DIR%\esptool.zip'; Expand-Archive '%TOOL_DIR%\esptool.zip' -DestinationPath '%TOOL_DIR%' -Force; Get-ChildItem -Path '%TOOL_DIR%' -Filter 'esptool.exe' -Recurse | Select-Object -First 1 | ForEach-Object { Copy-Item $_.FullName '%TOOL_DIR%\esptool.exe' -Force }; Remove-Item '%TOOL_DIR%\esptool.zip' -Force -ErrorAction SilentlyContinue"

if not exist "%ESPTOOL%" (
    echo.
    echo [ERROR] Could not find or download esptool.exe flasher!
    echo Please make sure this laptop has an internet connection or copy the
    echo 'tools' folder from your main computer.
    echo.
    pause
    exit /b 1
)

:ESPTOOL_READY
echo [OK] Portable ESP32 Flasher Ready: %ESPTOOL%
echo.

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
echo =========================================================================
echo READY TO FORMAT ESP32 FLASH
echo =========================================================================
echo NOTE: If connecting hangs at "Connecting........_____.....",
echo       PRESS AND HOLD the physical "BOOT" button on the ESP32 board for 2 seconds!
echo =========================================================================
echo.

set "COMPORT="
set /p "COMPORT=Enter COM port (e.g. COM3, COM4) or press ENTER for Auto-Detect: "

if defined COMPORT set "COMPORT=%COMPORT: =%"

echo.
echo [STARTING] Erasing and Formatting ESP32 Flash Memory...
echo Please do not unplug the USB cable while formatting...
echo.

if not defined COMPORT (
    "%ESPTOOL%" --chip esp32 erase_flash
) else (
    "%ESPTOOL%" --chip esp32 --port %COMPORT% erase_flash
)

if errorlevel 1 goto ERASE_FAILED

echo.
echo =========================================================================
echo [SUCCESS] ESP32 FLASH MEMORY IS 100 PERCENT FORMATTED AND FRESH!
echo =========================================================================
echo The ESP32 is now completely wiped and ready for clean firmware upload:
echo   1. Run '1_install_esp32_and_libraries.bat' to set up board core and libraries
echo   2. Run '3_upload_esp32_firmware.bat' to upload Smart Hospital Firmware
echo =========================================================================
goto FINISHED

:ERASE_FAILED
echo.
echo =========================================================================
echo [TROUBLESHOOTING TIPS]
echo 1. Ensure the micro-USB cable is a DATA cable (not a power-only cable).
echo 2. Check Device Manager to verify your ESP32 COM port.
echo 3. When you see "Connecting........_____.....", HOLD the "BOOT" button on
echo    your ESP32 board for 2 seconds until the erase starts.
echo =========================================================================
goto FINISHED

:FINISHED
echo.
pause
