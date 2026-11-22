# Patient Health Monitoring System Using ESP32 and IoT (Clinical Smart Hospital Model)

> **Based on Reference Project:** *How to make a Patient Health Monitoring System using ESP32 and IoT | Smart Hospital Working Model* by Projectronics  
> **Development Standard:** Clinical Hospital Bedside Monitoring Architecture (IEC 60601-1-8 Alarm Tiers, Patient EHR, Telemetry, and Intercom Voice Alerts)

---

## 1. Project Overview & System Architecture

This project transforms standard electronic prototyping components into a **real-world clinical bedside monitoring station**. It continuously monitors four core physiological and medical parameters, protects against medical complications (air embolism, extreme fever, hypoxemia), displays metrics on a bedside 16x2 LCD, streams telemetry to a mobile/PC Web Dashboard and Adafruit IO Cloud, and speaks communicative voice alerts over phone speakers.

```
       +-------------------------------------------------------------------------+
       |                           PATIENT BEDSIDE SENSORS                       |
       |  - Khyrud MAX30102      : Pulse Rate (BPM) & Blood Oxygen Saturation (SpO2)
       |  - Electrobot DS18B20   : Clinical Body Temperature (°C / °F)           |
       |  - TekBud SEN18         : IV Drip Saline Fluid Level (%) & Time Left    |
       |  - Capacitive Touch Wire: Bedside Nurse Call / Emergency SOS Button     |
       +------------------------------------+------------------------------------+
                                            |
                                            v
       +-------------------------------------------------------------------------+
       |               ESP32 WROOM-32 DUAL-CORE MICROCONTROLLER HUB              |
       |  - 4-Bit Parallel LCD Driver   - IEC 60601-1-8 Tiered Alarm State Machine
       |  - Smart Drip Velocity Engine  - Medical Early Warning Scoring (EWS)    |
       |  - Web Server & REST API       - Native Adafruit IO HTTPS Telemetry     |
       +--------------------+-------------------------------+--------------------+
                            |                               |
                            v                               v
       +------------------------------------+   +--------------------------------+
       |       BEDSIDE LOCAL OUTPUTS        |   |    REMOTE IOT & INTERCOM       |
       |  - SixOhms 16x2 LCD (Custom Icons) |   |  - Mobile/PC Web Intercom      |
       |  - Sunriders Active Alarm Siren    |   |  - Real Human Voice Alerts     |
       |  - Physical BOOT Snooze Button     |   |  - Lead II Cardiac ECG Trace   |
       +------------------------------------+   |  - Adafruit IO Cloud Dashboard |
                                                |  - Doctor's CSV Chart Export   |
                                                +--------------------------------+
```

---

## 2. Hardware Components & Pin Connection Mapping

All software is configured for your purchased components:

| Hardware Module | Physical Pins | ESP32 Pin | Protocol / Description |
| :--- | :--- | :--- | :--- |
| **Khyrud ESP32 WROOM-32** | 30-Pin Microcontroller | — | Dual Core 240MHz, 2.4GHz Wi-Fi, Type-C |
| **Khyrud MAX30102 Oximeter** | `VIN, GND, SDA, SCL` | **3.3V, GND, GPIO 21, GPIO 22** | I2C Serial Bus (`0x57`) |
| **Electrobot DS18B20 Temp** | `+, -, out` | **3.3V, GND, GPIO 4** | OneWire Digital Bus (Onboard pull-up active) |
| **TekBud SEN18 Saline Strip** | `+, -, S` | **3.3V, GND, GPIO 34** | Pure ADC1 Analog Channel (Wi-Fi safe) |
| **Sunriders Alarm Siren** | Red (`+`), Black (`-`) | **GPIO 25, GND** | Active Continuous Piezo Buzzer |
| **SixOhms 16x2 LCD (Bare)** | Pins 1 to 16 | **RS=19, EN=18, D4=5, D5=17, D6=16, D7=15** | 4-bit Parallel Bus (VSS=GND, VDD=5V, RW=GND) |
| **Touch Nurse Call SOS Wire** | Jumper wire to bed | **GPIO 13** | Built-in ESP32 Capacitive Touch (`T4`) |
| **Alarm Snooze / Mute Button**| Physical Onboard Button| **GPIO 0 (BOOT)** | Built directly on the ESP32 board |

---

## 3. Complete List of Functionalities & How They Work

### Functionality 1: Cardiac Pulse & Blood Oxygen ($SpO_2$) Monitoring
* **Sensor:** Khyrud MAX30102 (Optical Photoplethysmography).
* **How It Works:** Red (660nm) and Infrared (880nm) LEDs illuminate oxygenated vs. deoxygenated hemoglobin in capillary blood vessels.
* **Clinical Behavior:**
  - When finger is placed gently, it stabilizes within **5 to 10 seconds** (as demonstrated in the video).
  - Displays steady Pulse Rate (BPM) and Blood Oxygen ($SpO_2\%$).
  - **Probe-Off Protection:** If the patient removes their finger, the system displays `[PROBE DETACHED]` quietly without sounding a false emergency alarm (preventing hospital alarm fatigue).

---

### Functionality 2: Clinical Body Temperature Measurement
* **Sensor:** Electrobot DS18B20 digital temperature probe.
* **How It Works:** Reads calibrated digital temperature over a single OneWire data pin (`GPIO 4`).
* **Clinical Behavior:**
  - Displays body temperature in Celsius and Fahrenheit (e.g., `36.8°C / 98.2°F`).
  - **High Fever Siren:** If temperature rises above **40.0°C**, the siren sounds continuously and phone announces: *"Emergency: High fever detected on Bed 4."*

---

### Functionality 3: IV Drip Saline Fluid Level & Air Embolism Prevention
* **Sensor:** TekBud SEN18 conductive water level strip mounted on IV drip chamber.
* **How It Works:** Reads fluid conductivity on `GPIO 34`. Submerged = high percentage; dry/air = low percentage.
* **Clinical Behavior:**
  - **Pre-Warning (Saline < 25%):** System warns staff to prepare the replacement saline bag.
  - **Critical Empty Drip (Saline < 10%):** When water leaves the sensor, siren sounds an alarm to alert the nurse to clamp the line before air enters the patient's bloodstream.

---

### Functionality 4: Smart IV Saline "Time Remaining" Estimator
* **How It Works:** The ESP32 tracks the velocity of liquid drop per minute ($v = \Delta\text{Saline} / \Delta t$).
* **Clinical Behavior:**
  - Displays estimated time left on both LCD and Web Dashboard (e.g., `Sal: 85% ~45m`).
  - Allows nurses on duty to schedule their IV bag rounds accurately.

---

### Functionality 5: Touch-Sensitive Bedside "Nurse Call / Emergency SOS"
* **Sensor:** Built-in ESP32 Capacitive Silicon on `GPIO 13` (Zero extra hardware).
* **How It Works:** A single wire placed next to the patient's hand detects human electrical capacitance when touched.
* **Clinical Behavior:**
  - Instantly sounds an alert, updates the LCD to `! NURSE CALL ! BED 04 SOS ALERT`, and speaks out loud: *"Emergency: Nurse assistance requested from Bed 4."*

---

### Functionality 6: IEC 60601-1-8 Tiered Alarm Management & Snooze
* **How It Works:** Alarms are categorized into 3 clinical tiers to avoid alarm fatigue:
  1. **🔴 HIGH PRIORITY:** Life-critical emergencies (Temp $> 40^\circ\text{C}$, Saline $< 10\%$, $SpO_2 < 88\%$, SOS Touch).
  2. **🟡 MEDIUM PRIORITY:** Pre-warning advisories (Saline $< 25\%$, Temp $> 38^\circ\text{C}$).
  3. **🔵 TECHNICAL ADVISORY:** Probe detached / finger off (Silent display notice).
* **Physical & Web Alarm Snooze:**
  - Press the **BOOT button (GPIO 0)** on the ESP32 board or click **"🔕 Mute Alarm (60s)"** on the phone dashboard.
  - Mutes the audio siren for 60 seconds while staff treats the patient. LCD displays `[ALARM SNOOZED]`.

---

### Functionality 7: Real Human Voice Audio Intercom (Web Speech API)
* **How It Works:** The Web Dashboard uses the browser's native **Web Speech API** (`window.speechSynthesis`).
* **Clinical Behavior:**
  - Automatically speaks clear human voice announcements through your mobile phone or laptop speaker:
    - 📢 *"Critical Alert: Saline bottle is empty on Bed 4. Please replace intravenous drip immediately."*
    - 📢 *"Emergency: High fever detected on Bed 4. Temperature is over 40 degrees Celsius."*
    - 📢 *"Emergency: Nurse assistance requested from Bed 4."*
    - 📢 *"Warning: Severe low blood oxygen detected on Bed 4."*

---

### Functionality 8: Live Hospital Lead II Cardiac ECG Tracing
* **How It Works:** Built with HTML5 `<canvas>` on the Web Dashboard.
* **Clinical Behavior:**
  - Traces a smooth, glowing green hospital-style cardiac sweep with P, Q, R, S, T complex spikes synchronized to the patient's heart rate.

---

### Functionality 9: Clinical Early Warning Score (EWS)
* **How It Works:** Clinical scoring algorithm combining Heart Rate, $SpO_2$, Body Temperature, and Saline status.
* **Clinical Behavior:**
  - 🟢 **STABLE (Score 0–1):** All physiological vitals within normal bounds.
  - 🟡 **OBSERVE (Score 2–3):** Elevated temp or mild saline depletion.
  - 🔴 **CRITICAL (Score 4+):** Emergency intervention required.

---

### Functionality 10: Automated Doctor's Rounds Vital Signs Chart (CSV Export)
* **How It Works:** In-memory circular buffer logs vital sign snapshots every 15 seconds with timestamps.
* **Clinical Behavior:**
  - Click **"📥 Export Rounds Chart (CSV)"** on the dashboard.
  - Downloads an Excel-compatible spreadsheet (`Doctor_Rounds_Bed04.csv`) containing the complete clinical audit history for morning rounds.

---

### Functionality 11: Bedside 16x2 LCD Display with Custom Pixel-Art Emojis
* **How It Works:** Utilizes the HD44780 CGRAM to generate five custom 5x8 pixel icons:
  - `[♥]` Heart Icon for Pulse Rate
  - `[🫁]` Oxygen Droplet Icon for $SpO_2$
  - `[🌡]` Thermometer Icon for Temperature
  - `[💧]` Saline IV Bottle Icon for Saline Level
  - `[🔔]` Alert Bell Icon for Siren Emergencies
* **Clinical Behavior:**
  - **Screen 1 (Hospital ID):** `ICU WARD-B  BED-04` / `R. Sharma  MRN-1042`
  - **Screen 2 (Vitals):** `[♥] 82  [🫁]98% STAB` / `[🌡]36.8°C [💧]85% ~45m`
  - **Emergency:** Flashes `[🔔]! EMERGENCY ![🔔]` with the active medical reason.

---

### Functionality 12: Dual-Mode IoT Cloud Telemetry
* **Mode A (Adafruit IO - Global Cloud):** Connects to your mobile hotspot and streams data to `iot.adafruit.com` every 5 seconds so doctors can monitor patients anywhere in the world.
* **Mode B (Standalone Bedside Hotspot):** If no Wi-Fi router is nearby, the ESP32 broadcasts its own network (**`Smart-Hospital-Bed04`**, password: **`hospital123`**) so your phone connects directly at `http://192.168.4.1`.

---

## 4. Step-by-Step Instructions to Test Every Functionality

| Test | Action | Expected Result |
| :--- | :--- | :--- |
| **Boot Test** | Turn on power | Buzzer chirps once; LCD displays `BED-04 CLINICAL ICU Init..` |
| **Probe-Off Test** | Remove finger from MAX30102 | LCD displays `HR:-- SpO2:--`; no false siren occurs |
| **Pulse & SpO2 Test** | Place index finger gently on MAX30102 for 8s | Steady BPM (e.g. 74) and SpO2 (e.g. 98%) appear on LCD & Web Dashboard |
| **Fever Alarm Test** | Warm the DS18B20 tip above 40°C | Siren sounds continuously; phone speaks: *"Emergency: High fever detected on Bed 4"* |
| **Saline Depletion Test**| Lift red SEN18 sensor into air (dry) | Saline drops $< 10\%$; siren rings; phone speaks: *"Critical Alert: Saline bottle is empty on Bed 4"* |
| **Saline Normal Test** | Dip SEN18 sensor into cup of water | Saline jumps to $> 80\%$; siren stops immediately |
| **Touch Nurse Call Test**| Touch the wire connected to GPIO 13 | Siren sounds; LCD flashes `! NURSE CALL ! BED-04 SOS`; phone speaks Nurse Call alert |
| **Alarm Snooze Test** | While siren is ringing, press the **BOOT button** | Buzzer silences for 60 seconds; LCD displays `[ALARM SNOOZED]` |
| **Doctor Report Test** | Click **"Export Rounds Chart (CSV)"** on phone | A `.csv` spreadsheet file downloads with historical clinical vital logs |

---

## 5. Software Architecture File Structure

```
d:\a-hospital project\Smart_Hospital_ESP32\
│
├── Smart_Hospital_ESP32.ino   --> Main firmware orchestrator (setup & loop)
├── Config.h                   --> Ward EHR, pins, alarm thresholds, and settings
├── SensorManager.h / .cpp     --> MAX30102, DS18B20, Saline velocity, and EWS score
├── DisplayManager.h / .cpp    --> 16x2 LCD custom emoji bitmaps and screen cycler
├── AlertManager.h / .cpp      --> IEC 60601-1-8 alarm state machine & buzzer control
├── WebDashboard.h / .cpp      --> Web server, Lead II ECG canvas, voice speech intercom
└── AdafruitIOManager.h / .cpp --> Native HTTPS telemetry to iot.adafruit.com
```

---

## 6. How to Flash the ESP32 in Arduino IDE

1. Open **Arduino IDE**.
2. Go to **File** > **Open...** and select:  
   `D:\a-hospital project\Smart_Hospital_ESP32\Smart_Hospital_ESP32.ino`
3. Go to **Tools** > **Board** > **esp32** > select **ESP32 Dev Module**.
4. Go to **Tools** > **Port** > select your ESP32's COM port.
5. In **Sketch** > **Include Library** > **Manage Libraries...**, install:
   - `SparkFun MAX3010x Pulse and Proximity Sensor Library` (by SparkFun)
   - `DallasTemperature` (by Miles Burton)
   - `OneWire` (by Paul Stoffregen)
6. Click the **Upload (➜)** button.  
   *(If prompted with `Connecting........_____`, press and hold the **BOOT** button on the ESP32 for 2 seconds until the upload starts).*
7. Once finished, open Serial Monitor at **`115200`** baud to see live clinical logs!
