# Hardware Connection & Pinout Mapping Guide

**Project:** Patient Health Monitoring System Using ESP32 and IoT (Smart Hospital Working Model)  
**Microcontroller:** ESP32 WROOM-32 NodeMCU (30-Pin Board with Type-C)

---

## 1. Pin Allocation Summary Table

| Hardware Component | Component Pin / Wire | ESP32 Pin | Function / Notes |
| :--- | :--- | :--- | :--- |
| **MAX30102 (Pulse & SpO2)** | `VIN` | **3.3V** | Power (Do not feed 5V directly to sensor logic) |
| | `GND` | **GND** | Ground |
| | `SDA` | **GPIO 21** | I2C Serial Data |
| | `SCL` | **GPIO 22** | I2C Serial Clock |
| | `INT / IRD / RD` | *Not connected* | Leave floating |
| **DS18B20 Temp Module** | `+` (VCC) | **3.3V** | Power |
| *(Electrobot 3-pin board)* | `-` (GND) | **GND** | Ground |
| | `out` (Data) | **GPIO 4** | OneWire Communication (Pull-up resistor already onboard!) |
| **Saline / Water Sensor** | `+` / `VCC` | **3.3V** | Power |
| *(TekBud SEN18 / Soil AO)* | `-` / `GND` | **GND** | Ground |
| | `S` (Signal) / `A0` | **GPIO 34** | ADC1 Input (Dedicated pure analog pin; unaffected by Wi-Fi) |
| **Active Buzzer** | Red Lead (`+`) | **GPIO 25** | Digital Output (High = Beep, Low = Silent) |
| *(Sunriders 5V-12V Alarm)* | Black Lead (`-`) | **GND** | Ground |
| **16x2 LCD Display** | Pin 1 (`VSS`) | **GND** | Power Ground |
| *(SixOhms JHD162A Bare)* | Pin 2 (`VDD`) | **VIN (5V)** | LCD Logic Power (5V from USB pin) |
| | Pin 3 (`V0`) | **Potentiometer center** | Contrast Adjustment (Or connect to GND with 1k resistor) |
| | Pin 4 (`RS`) | **GPIO 19** | Register Select |
| | Pin 5 (`RW`) | **GND** | Read/Write (Grounded for write mode) |
| | Pin 6 (`EN` / `E`) | **GPIO 18** | Enable Clock Signal |
| | Pins 7, 8, 9, 10 | *Not connected* | Data pins D0-D3 unused in 4-bit mode |
| | Pin 11 (`D4`) | **GPIO 5** | Data bit 4 |
| | Pin 12 (`D5`) | **GPIO 17** | Data bit 5 |
| | Pin 13 (`D6`) | **GPIO 16** | Data bit 6 |
| | Pin 14 (`D7`) | **GPIO 15** | Data bit 7 |
| | Pin 15 (`A` / `LED+`) | **VIN (5V)** or **3.3V** | Backlight Anode (through a 220 ohm resistor or direct 3.3V) |
| | Pin 16 (`K` / `LED-`) | **GND** | Backlight Cathode Ground |

---

## 2. Detailed Connection Instructions

### A. MAX30102 Pulse Oximeter & Heart Rate Sensor
- The MAX30102 board communicates via I2C.
- Connect **`VIN`** to **`3.3V`** of ESP32.
- Connect **`GND`** to **`GND`** of ESP32.
- Connect **`SDA`** to **`GPIO 21`**.
- Connect **`SCL`** to **`GPIO 22`**.
- *Tip:* When taking readings, place your index finger gently over the optical sensor window. Do not press hard, as excessive pressure cuts off microvascular blood flow and distorts readings.

### B. Electrobot DS18B20 Temperature Sensor Module
- Your module has 3 pins clearly labeled: **`-`**, **`out`**, **`+`**.
- Connect **`+`** to **`3.3V`**.
- Connect **`-`** to **`GND`**.
- Connect **`out`** to **`GPIO 4`**.
- Because this is an Electrobot breakout board, the **4.7kΩ pull-up resistor is already soldered on the PCB**, so you do not need an external resistor!

### C. Saline Level Sensor (TekBud SEN18 or EASTRA Soil Moisture)
- **TekBud SEN18 Water Level Sensor:**
  - `+` to **`3.3V`**
  - `-` to **`GND`**
  - `S` (Signal) to **`GPIO 34`**
  - Mount the red sensor strip along the bottom side of the saline drip chamber/bottle.
- *Alternative (EASTRA Soil Moisture):*
  - Connect probe to the blue LM393 board.
  - `VCC` to **`3.3V`**, `GND` to **`GND`**, `A0` to **`GPIO 34`**.

### D. SixOhms 16x2 LCD Display (Bare 16-Pin)
- The display operates in efficient 4-bit parallel mode using the standard `<LiquidCrystal.h>` library.
- If text looks faint or invisible on the LCD, adjust the potentiometer connected to **Pin 3 (`V0`)** until clear black letters appear.

---

## 3. Power Supply Notes
- Power the ESP32 using a standard 5V USB-C cable connected to a laptop/PC or a 5V/2A phone charger.
- The `VIN` pin on the ESP32 provides 5V directly from the USB supply, which is ideal for the 16x2 LCD backlight and logic.
- All sensors (MAX30102, DS18B20, Water Sensor) run reliably on the ESP32's regulated **`3.3V`** rail.
