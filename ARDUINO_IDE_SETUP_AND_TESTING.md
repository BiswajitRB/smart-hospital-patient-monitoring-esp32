# Arduino IDE Setup, Library Installation & Testing Guide

This guide details the exact steps to configure your programming environment, install dependencies, flash the ESP32 firmware, and access the IoT telemetry dashboard.

---

## Step 1: Install & Configure Arduino IDE for ESP32

1. Download and install **Arduino IDE 2.x** (or 1.8.19) from [arduino.cc](https://www.arduino.cc/en/software).
2. Open Arduino IDE and navigate to:
   - **File** > **Preferences**
3. Locate the field **"Additional boards manager URLs"** and paste the following official ESP32 URL:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. Click **OK**.
5. Go to **Tools** > **Board** > **Boards Manager...**
6. Search for `esp32` and install the package by **Espressif Systems** (version 2.0.x or 3.0.x).

---

## Step 2: Install Required Arduino Libraries

Go to **Sketch** > **Include Library** > **Manage Libraries...** and install each of the following libraries:

1. **SparkFun MAX3010x Pulse and Proximity Sensor Library**
   - *Author:* SparkFun Electronics
   - *Purpose:* Communicates with the MAX30102 sensor, computes heart rate and blood oxygen.
2. **DallasTemperature**
   - *Author:* Miles Burton
   - *Purpose:* Reads digital temperature from DS18B20.
3. **OneWire**
   - *Author:* Paul Stoffregen
   - *Purpose:* Protocol library for DS18B20.
4. **LiquidCrystal**
   - Built-in with Arduino IDE (No separate installation needed for bare 16-pin LCD).
   - *(Optional: If using an I2C LCD backpack, install `LiquidCrystal I2C` by Frank de Brabander).*

---

## Step 3: Configure Wi-Fi & Credentials in Code

Open the sketch file:
```
D:\a-hospital project\Smart_Hospital_ESP32\Smart_Hospital_ESP32.ino
```

Near lines 45–47, update your home Wi-Fi or mobile hotspot credentials:
```cpp
const char* WIFI_SSID     = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
```
*(Note: If Wi-Fi is not in range, the ESP32 automatically creates its own Access Point named **`Smart-Hospital-Bed`** with password **`hospital123`**, so the dashboard always works!)*

---

## Step 4: Upload Program to ESP32

1. Connect your **Khyrud ESP32** board to your PC via a USB Type-C cable.
2. If your PC does not recognize the board, download and install the **CH340 USB Driver** (standard driver for CH340 chip).
3. In Arduino IDE:
   - Select **Tools** > **Board** > **esp32** > **ESP32 Dev Module**
   - Select **Tools** > **Port** > choose the COM port assigned to your ESP32 (e.g., `COM3`, `COM4`, etc.)
   - Set **Upload Speed**: `921600` (or `115200`)
4. Click the **Upload** button (Right arrow icon).
5. *Note:* If the console displays `Connecting........_____.....`, press and hold the **BOOT** button on the ESP32 for 2 seconds until the upload starts.

---

## Step 5: Testing and Real-Time Verification

1. Open the **Serial Monitor** in Arduino IDE (**Tools** > **Serial Monitor**) and set the baud rate to **`115200`**.
2. Press the **EN (Reset)** button on the ESP32.
3. Observe the startup output:
   - Buzzer performs a short diagnostic chirp.
   - LCD displays `"SMART HOSPITAL Initializing..."`.
   - MAX30102 sensor initializes.
   - Wi-Fi connects and prints the **IP Address** (e.g., `192.168.1.45` or AP IP `192.168.4.1`).

### Testing the Web Dashboard:
- Open a web browser on any phone or laptop connected to the same Wi-Fi (or connected to `Smart-Hospital-Bed` AP).
- Enter the IP address shown in the Serial Monitor (e.g., `http://192.168.1.45` or `http://192.168.4.1`).
- The live Smart Hospital Bedside Dashboard will load automatically, updating every 1 second without page refresh!

### Testing Alerts:
- **Saline Empty Alert:** Remove the water level sensor from liquid. Saline will drop below 20%, triggering the warning banner and active buzzer.
- **Heart Rate & SpO2:** Place your finger gently on the MAX30102 sensor. Vitals will display live on both the 16x2 LCD and the Web Dashboard.
- **Temperature:** Hold the DS18B20 probe between your fingers to observe the body temperature rise toward 36.5°C–37°C.
