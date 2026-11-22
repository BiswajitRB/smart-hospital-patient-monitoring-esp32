# Adafruit IO Cloud Dashboard Setup Guide

This guide explains how to connect your ESP32 Patient Health Monitoring System to **Adafruit IO (`iot.adafruit.com`)**, exactly as demonstrated in the reference video.

---

## 1. Create a Free Account on Adafruit IO
1. Go to **[io.adafruit.com](https://io.adafruit.com)** in your web browser.
2. Click **Get Started for Free** or **Sign In**.
3. Create your free Adafruit account and log in.

---

## 2. Get Your Username & AIO Key
1. In Adafruit IO, look at the top-right corner of the screen.
2. Click the yellow key icon labeled **"IO Key"** (or **"My Key"**).
3. A popup will display:
   - **Username** (e.g. `your_username`)
   - **Active Key** (e.g. `aio_xxxxxxxxxxxxxxxxxxxxxxxxxx`)
4. Copy both of these values.

---

## 3. Create the 4 Feeds
1. In Adafruit IO, click **Feeds** in the top navigation bar.
2. Click **+ New Feed** and create the following 4 feeds (use these exact names):
   - `heartbeat` (For Pulse Rate / BPM)
   - `oxygen-level` (For Blood Oxygen / SpO2)
   - `body-temperature` (For Temperature in °C)
   - `saline-status` (For Saline IV fluid level in %)

---

## 4. Create the Dashboard (Gauges & Text Blocks)
1. Click **Dashboards** in the top navigation bar.
2. Click **+ New Dashboard** and name it: `Patient Monitor`.
3. Open your new dashboard, click the gear icon (top-right) -> **+ Create New Block**:
   - **Block 1 (Heartbeat):** Choose *Gauge* or *Text*, select the `heartbeat` feed. Set Min = 0, Max = 160.
   - **Block 2 (Oxygen Level):** Choose *Gauge*, select `oxygen-level`. Set Min = 80, Max = 100.
   - **Block 3 (Temperature):** Choose *Line Chart* or *Gauge*, select `body-temperature`. Set Min = 25, Max = 45.
   - **Block 4 (Saline Level):** Choose *Progress Bar* or *Gauge*, select `saline-status`. Set Min = 0, Max = 100.

---

## 5. Put Your Details in Config.h
Open [Config.h](file:///D:/a-hospital%20project/Smart_Hospital_ESP32/Config.h) in Arduino IDE, and update these lines:
```cpp
// Your Mobile Hotspot (Turn ON hotspot on your mobile phone)
#define DEFAULT_WIFI_SSID     "YOUR_HOTSPOT_NAME"
#define DEFAULT_WIFI_PASSWORD "YOUR_HOTSPOT_PASSWORD"

// Your Adafruit IO Details
#define AIO_USERNAME          "YOUR_ADAFRUIT_USERNAME"
#define AIO_KEY               "YOUR_AIO_KEY"
```

Once uploaded, when your mobile hotspot is turned on:
- The ESP32 connects automatically.
- Every 5 seconds, it updates your live Adafruit IO dashboard worldwide!
