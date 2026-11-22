#include "AlertManager.h"

AlertManager::AlertManager() : snoozeUntil(0), lastBootButtonState(HIGH) {}

void AlertManager::begin() {
  pinMode(PIN_BUZZER, OUTPUT);
  digitalWrite(PIN_BUZZER, LOW);
  pinMode(PIN_BOOT_BUTTON, INPUT_PULLUP);
}

void AlertManager::testChirp() {
  digitalWrite(PIN_BUZZER, HIGH);
  delay(120);
  digitalWrite(PIN_BUZZER, LOW);
}

void AlertManager::triggerSnooze() {
  snoozeUntil = millis() + ALARM_SNOOZE_MS;
  Serial.println("[AlertManager] Clinical Alarm Acknowledged & Snoozed for 60s.");
}

void AlertManager::evaluate(PatientVitals &vitals) {
  // Check physical BOOT button on ESP32 to mute alarm
  bool bootPressed = (digitalRead(PIN_BOOT_BUTTON) == LOW);
  if (bootPressed && lastBootButtonState == HIGH) {
    triggerSnooze();
  }
  lastBootButtonState = bootPressed;

  vitals.isSnoozed = (millis() < snoozeUntil);
  vitals.isEmergency = false;
  vitals.alarmLevel = ALARM_NONE;
  vitals.alertMessage = "Patient Stable";

  // --- TIER 1: HIGH PRIORITY LIFE-CRITICAL ALARMS ---
  
  // 1. High Fever Detection (Temp >= 40.0°C) - Immediate Top Priority
  if (vitals.temperatureC >= THRESHOLD_TEMP_CRITICAL) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "Fever >= 40C Critical!";
  }
  // 2. Touch-Sensitive Nurse Call SOS
  else if (vitals.nurseCallActive) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "Nurse Call: Bed 04!";
  }
  // 3. Saline Empty (< 10%) - Critical Air Embolism Hazard
  else if (vitals.salinePercent <= THRESHOLD_SALINE_EMPTY) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "Saline Drip Empty!";
  }
  // 4. Critical Hypoxemia (SpO2 < 88%)
  else if (vitals.fingerDetected && (vitals.spo2 > 0 && vitals.spo2 < THRESHOLD_SPO2_CRITICAL)) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "SpO2 < 88% Hypoxemia!";
  }
  // 5. Critical Cardiac Pulse Rate (> 130 or < 45 BPM)
  else if (vitals.fingerDetected && (vitals.heartRateBPM > THRESHOLD_HR_CRIT_HIGH || 
           (vitals.heartRateBPM < THRESHOLD_HR_CRIT_LOW && vitals.heartRateBPM > 0))) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "Cardiac Critical Pulse!";
  }

  // --- TIER 2: MEDIUM PRIORITY PRE-ALERTS ---
  else if (vitals.salinePercent <= THRESHOLD_SALINE_WARN) {
    vitals.alarmLevel = ALARM_MEDIUM;
    vitals.alertMessage = "Saline Low: Prep Bag";
  }
  else if (vitals.temperatureC >= THRESHOLD_TEMP_WARN) {
    vitals.alarmLevel = ALARM_MEDIUM;
    vitals.alertMessage = "Elevated Temp > 38C";
  }
  else if (vitals.fingerDetected && (vitals.spo2 <= THRESHOLD_SPO2_WARN)) {
    vitals.alarmLevel = ALARM_MEDIUM;
    vitals.alertMessage = "SpO2 Sub-optimal";
  }

  // --- TIER 3: TECHNICAL ADVISORY (Probe Detached / No Panic Siren) ---
  else if (!vitals.fingerDetected) {
    vitals.alarmLevel = ALARM_ADVISORY;
    vitals.alertMessage = "Oximeter Detached";
  }

  // --- SIREN CONTROL ---
  if (vitals.alarmLevel == ALARM_HIGH && !vitals.isSnoozed) {
    digitalWrite(PIN_BUZZER, HIGH); // Continuous siren
  } else {
    digitalWrite(PIN_BUZZER, LOW);
  }
}
