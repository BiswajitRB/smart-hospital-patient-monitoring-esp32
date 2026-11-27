/*
 * PROJECT: Clinical Bedside Patient Monitoring System (ESP32 Smart Hospital Model)
 * ARCHITECTURE: Real-World Clinical Hospital Standard (Tiered Alarms & EHR Integration)
 * 
 * 4 CORE CLINICAL PARAMETERS:
 * 1. Pulse Rate / Heartbeat (MAX30102 Oximeter)
 * 2. Blood Oxygen / SpO2 (MAX30102 Oximeter)
 * 3. Body Temperature (DS18B20 Digital Temp Sensor)
 * 4. Saline Fluid Level (TekBud SEN18 Saline Drip Sensor)
 * 
 * REAL-WORLD HOSPITAL PROTOCOLS IMPLEMENTED:
 * - Patient EHR & Ward Assignment (Apollo Smart Hospital, ICU Ward-B, Bed-04, R. Sharma)
 * - Tiered Clinical Alarm Management (IEC 60601-1-8 Standard: High, Medium, Advisory)
 * - Probe Detached Advisory (No false alarms when finger is removed)
 * - Automatic Communicative Spoken Voice Intercom on Phone / Laptop
 * - Touch-Sensitive Nurse Call SOS Wire on GPIO 13
 * - Smart Saline Depletion Time Remaining Estimator
 * - Alarm Snooze / Mute (ESP32 BOOT Button & Web Intercom)
 * - Live Hospital Lead II ECG Canvas Tracing
 * - Clinical Early Warning Score (EWS: STABLE / OBSERVE / CRITICAL)
 * - One-Click Doctor's Rounds Vital Signs Chart Export (CSV / Excel format)
 * - Cloud Telemetry via Adafruit IO (iot.adafruit.com)
 */

#include "Config.h"
#include "SensorManager.h"
#include "DisplayManager.h"
#include "AlertManager.h"
#include "WebDashboard.h"
#include "AdafruitIOManager.h"
#include "CloudTelemetryManager.h"

// Global Subsystem Managers
SensorManager           sensorMgr;
DisplayManager          displayMgr;
AlertManager            alertMgr;
WebDashboard            webDashboard;
AdafruitIOManager       adafruitIO;
CloudTelemetryManager   cloudTelemetry;

// Shared Patient Telemetry State
PatientVitals patientData = {
  0.0f,       // heartRateBPM
  0,          // spo2
  false,      // fingerDetected
  0.0f,       // temperatureC
  0.0f,       // temperatureF
  100,        // salinePercent (Default full)
  500.0f,     // salineWeightGrams (grams)
  55,         // salineMinutesLeft
  "FULL",     // salineStatus
  false,      // nurseCallActive
  0,          // ewsScore
  "STABLE",   // ewsStatus
  ALARM_NONE, // alarmLevel
  false,      // isEmergency
  false,      // isSnoozed
  "Normal"    // alertMessage
};

// Periodic Timers (5-second stepwise reporting as specified in video)
unsigned long lastTelemetryTime = 0;
unsigned long lastDisplayTime   = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\nAPOLLO SMART HOSPITAL - CLINICAL BEDSIDE HUB");
  Serial.println("Ward: " WARD_NAME " | Bed: " BED_NUMBER " | Patient: " PATIENT_NAME);

  // 1. Initialize Siren / Buzzer Subsystem & Diagnostic Chirp
  alertMgr.begin();
  alertMgr.testChirp();

  // 2. Initialize 16x2 LCD Display & Show Boot Screen
  displayMgr.begin();
  displayMgr.showBootMessage();
  delay(1500);

  // 3. Initialize Sensors (MAX30102 Oximeter, DS18B20 Temp, Saline ADC)
  sensorMgr.begin();

  // 4. Connect to Hotspot / Wi-Fi & Start Local Web Dashboard with Snooze link
  webDashboard.begin(&patientData, &alertMgr);
  displayMgr.showWifiStatus(webDashboard.isConnectedToStation(), webDashboard.getLocalIP());
  delay(2000);

  // 5. Initialize Adafruit IO Cloud & Vercel MongoDB Cloud
  adafruitIO.begin();
  cloudTelemetry.begin();

  Serial.println("[System] All clinical modules initialized. Ready.");
}

void loop() {
  // 1. Handle incoming web dashboard requests
  webDashboard.handleClient();

  // 2. High-speed optical pulse sampling (MAX30102)
  sensorMgr.updateFast();

  // 3. 5-Second Stepwise Telemetry Cycle (Exact delay from video transcript)
  if (millis() - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = millis();

    // Read DS18B20 Temperature, Saline Level, Time Remaining, and Touch SOS
    sensorMgr.updatePeriodic(patientData);

    // Evaluate Clinical Alarm Tiers (High, Medium, Advisory) & Control Siren / Snooze
    alertMgr.evaluate(patientData);

    // Publish to Adafruit IO Cloud (iot.adafruit.com)
    adafruitIO.publishVitals(patientData);

    // Stream live to Vercel Next.js Cloud Dashboard & MongoDB Atlas
    cloudTelemetry.sendTelemetry(patientData);

    // Log live clinical telemetry to Serial Monitor
    Serial.print("HR: "); Serial.print((int)patientData.heartRateBPM); Serial.print(" BPM | ");
    Serial.print("SpO2: "); Serial.print(patientData.spo2); Serial.print("% | ");
    Serial.print("Temp: "); Serial.print(patientData.temperatureC, 1); Serial.print(" C | ");
    Serial.print("Saline: "); Serial.print(patientData.salinePercent); Serial.print("% (");
    Serial.print(patientData.salineWeightGrams, 1); Serial.print("g, ~");
    Serial.print(patientData.salineMinutesLeft); Serial.print("m left) | ");
    Serial.print("EWS: "); Serial.print(patientData.ewsStatus); Serial.print(" | ");
    Serial.print("Alarm: Tier-"); Serial.print((int)patientData.alarmLevel); Serial.print(" | ");
    Serial.print("Siren: "); Serial.println(patientData.isEmergency ? (patientData.isSnoozed ? "SNOOZED" : "RINGING!") : "OFF");
  }

  // 4. Refresh 16x2 LCD Display every 1.5 seconds
  if (millis() - lastDisplayTime >= 1500) {
    lastDisplayTime = millis();
    displayMgr.updateDisplay(patientData);
  }
}
