@echo off
echo =========================================================================
echo STEP 1: Installing ESP32 Board Core & Required Libraries via Arduino-CLI
echo =========================================================================

set CLI="C:\Users\%USERNAME%\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
set ESP32_URL=https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

if not exist %CLI% (
    echo [ERROR] arduino-cli.exe not found. Please verify Arduino IDE is installed.
    pause
    exit /b 1
)

echo.
echo [1/4] Updating Package Index for ESP32...
%CLI% core update-index --additional-urls %ESP32_URL%

echo.
echo [2/4] Installing ESP32 Board Core (This takes about 1-2 minutes)...
%CLI% core install esp32:esp32 --additional-urls %ESP32_URL%

echo.
echo [3/4] Installing Required Sensor Libraries...
%CLI% lib install "SparkFun MAX3010x Pulse and Proximity Sensor Library"
%CLI% lib install "DallasTemperature"
%CLI% lib install "OneWire"

echo.
echo =========================================================================
echo [SUCCESS] ESP32 Core and All 3 Libraries Installed Successfully!
echo =========================================================================
pause
