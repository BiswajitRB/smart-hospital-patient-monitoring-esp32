#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// =========================================================================================
// 1. HOSPITAL WARD & PATIENT ELECTRONIC HEALTH RECORD (EHR) SETTINGS
// =========================================================================================
#define HOSPITAL_NAME         "APOLLO SMART HOSPITAL"
#define WARD_NAME             "ICU WARD-B"
#define BED_NUMBER            "BED-04"
#define PATIENT_NAME          "R. Sharma"
#define PATIENT_MRN           "MRN-1042"

// =========================================================================================
// 2. HARDWARE PIN DEFINITIONS (ESP32 WROOM-32 30-PIN)
// =========================================================================================

// --- 16x2 LCD Display Configuration (SixOhms JHD162A 16-Pin) ---
#define USE_I2C_LCD 0

#if !USE_I2C_LCD
  #define PIN_LCD_RS 19
  #define PIN_LCD_EN 18
  #define PIN_LCD_D4 5
  #define PIN_LCD_D5 17
  #define PIN_LCD_D6 16
  #define PIN_LCD_D7 15
#else
  #define LCD_I2C_ADDR 0x27
#endif

// --- MAX30102 Pulse Oximeter (I2C) ---
#define PIN_I2C_SDA 21
#define PIN_I2C_SCL 22

// --- DS18B20 Digital Body Temperature Sensor ---
#define PIN_ONE_WIRE_BUS 4

// --- Saline / IV Fluid Level Sensor (TekBud SEN18) ---
#define PIN_SALINE_ADC 34

// --- Active Siren / Medical Alarm Buzzer ---
#define PIN_BUZZER 25

// --- Onboard BOOT Button for Alarm Snooze / Acknowledgment ---
#define PIN_BOOT_BUTTON 0

// --- Touch-Sensitive Nurse Call / SOS Wire (ESP32 Capacitive Touch) ---
#define PIN_TOUCH_NURSE_CALL 13
#define TOUCH_SENSITIVITY_THRESHOLD 35

// =========================================================================================
// 3. NETWORK & ADAFRUIT IO CLOUD CREDENTIALS
// =========================================================================================
#define DEFAULT_WIFI_SSID     "YOUR_MOBILE_HOTSPOT_NAME"
#define DEFAULT_WIFI_PASSWORD "YOUR_HOTSPOT_PASSWORD"

// Standalone Fallback Access Point (Broadcast when mobile hotspot is off)
#define AP_SSID               "Smart-Hospital-Bed04"
#define AP_PASSWORD           "hospital123"

// Adafruit IO Credentials (from https://io.adafruit.com)
#define AIO_USERNAME          "YOUR_ADAFRUIT_USERNAME"
#define AIO_KEY               "YOUR_ADAFRUIT_AIO_KEY"

// Adafruit IO Feed Keys
#define AIO_FEED_HEARTBEAT    "heartbeat"
#define AIO_FEED_OXYGEN       "oxygen-level"
#define AIO_FEED_TEMP         "body-temperature"
#define AIO_FEED_SALINE       "saline-status"

#define WEB_SERVER_PORT       80

// =========================================================================================
// 4. CLINICAL ALARM TIERS (IEC 60601-1-8 ALARM MANAGEMENT)
// =========================================================================================
// High Priority Thresholds (Set to 37.0°C for instant finger-touch demo)
#define THRESHOLD_TEMP_CRITICAL 37.0f // Lowered from 40°C so touching sensor with warm finger triggers demo!
#define THRESHOLD_SALINE_EMPTY  10    // Critical air embolism hazard (< 10%)
#define THRESHOLD_SPO2_CRITICAL 88    // Severe hypoxemia (< 88%)
#define THRESHOLD_HR_CRIT_HIGH  130   // Severe tachycardia (> 130 BPM)
#define THRESHOLD_HR_CRIT_LOW   45    // Severe bradycardia (< 45 BPM)

// Medium Priority Thresholds (Pre-warning advisory)
#define THRESHOLD_SALINE_WARN   25    // Saline prep threshold (< 25%)
#define THRESHOLD_TEMP_WARN     38.0f // Low-grade fever threshold (> 38°C)
#define THRESHOLD_SPO2_WARN     92    // Mild desaturation (< 92%)

#define TELEMETRY_INTERVAL_MS 5000  // 5-second stepwise cloud update interval
#define ALARM_SNOOZE_MS       60000 // 60 seconds nurse snooze duration

// =========================================================================================
// 5. SHARED PATIENT TELEMETRY DATA STRUCTURE
// =========================================================================================
enum AlarmPriority {
  ALARM_NONE = 0,
  ALARM_ADVISORY = 1, // Probe detached, no siren
  ALARM_MEDIUM = 2,   // Pre-alert (saline low prep, mild fever)
  ALARM_HIGH = 3      // Life-critical emergency (siren + voice intercom)
};

struct PatientVitals {
  float heartRateBPM;
  int   spo2;
  bool  fingerDetected;
  float temperatureC;
  float temperatureF;
  int   salinePercent;
  int   salineMinutesLeft;  // Estimated IV fluid exhaustion time in minutes
  String salineStatus;      // "FULL", "NORMAL", "LOW", "EMPTY"
  bool  nurseCallActive;    // Touch-sensitive nurse call state
  int   ewsScore;           // Early Warning Score (0 to 10)
  String ewsStatus;         // "STABLE", "OBSERVE", "CRITICAL"
  AlarmPriority alarmLevel; // None, Advisory, Medium, High
  bool  isEmergency;
  bool  isSnoozed;          // True when nurse has muted the audio alarm
  String alertMessage;
};

#endif // CONFIG_H
