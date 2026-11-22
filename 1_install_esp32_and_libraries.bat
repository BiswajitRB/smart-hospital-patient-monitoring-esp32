@echo off
echo =========================================================================
echo STEP 1: Installing Stable ESP32 Board Core (v3.0.7) and Libraries
echo =========================================================================

set CLI="C:\Users\%USERNAME%\AppData\Local\Programs\Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe"
set ESP32_URL=https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

if not exist %CLI% (
    echo [ERROR] arduino-cli.exe not found at %CLI%
    echo Please verify Arduino IDE is installed.
    pause
    exit /b 1
)

echo.
echo [1/3] Updating ESP32 Package Index...
%CLI% core update-index --additional-urls %ESP32_URL%

echo.
echo [2/3] Installing Stable ESP32 Core v3.0.7 (Fixes 4.0.0 missing compiler bug)...
%CLI% core uninstall esp32:esp32
%CLI% core install esp32:esp32@3.0.7 --additional-urls %ESP32_URL%

echo.
echo [3/3] Installing Required Libraries...
%CLI% lib install "LiquidCrystal"
%CLI% lib install "SparkFun MAX3010x Pulse and Proximity Sensor Library"
%CLI% lib install "DallasTemperature"
%CLI% lib install "OneWire"

echo.
echo =========================================================================
echo [SUCCESS] Stable ESP32 Core v3.0.7 Installed Successfully!
echo =========================================================================
pause
