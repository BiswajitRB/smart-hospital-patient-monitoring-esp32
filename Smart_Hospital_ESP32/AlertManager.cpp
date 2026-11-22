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

  // --- TIER 1: LIFE-CRITICAL HIGH PRIORITY (Continuous Siren + Voice) ---
  if (vitals.nurseCallActive) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "Nurse Call: Bed 04!";
  }
  else if (vitals.salinePercent <= THRESHOLD_SALINE_EMPTY) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "Saline Drip Empty!";
  }
  else if (vitals.temperatureC >= THRESHOLD_TEMP_CRITICAL) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "Fever > 40C Critical!";
  }
  else if (vitals.fingerDetected && (vitals.spo2 > 0 && vitals.spo2 < THRESHOLD_SPO2_CRITICAL)) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "SpO2 < 88% Hypoxemia!";
  }
  else if (vitals.fingerDetected && (vitals.heartRateBPM > THRESHOLD_HR_CRIT_HIGH || 
           (vitals.heartRateBPM < THRESHOLD_HR_CRIT_LOW && vitals.heartRateBPM > 0))) {
    vitals.alarmLevel = ALARM_HIGH;
    vitals.isEmergency = true;
    vitals.alertMessage = "Cardiac Critical Pulse!";
  }

  // --- TIER 2: MEDIUM PRIORITY PRE-ALERT (Time to intervene before crash) ---
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

  // --- TIER 3: TECHNICAL ADVISORY (Probe Off / No Panic Alarm) ---
  else if (!vitals.fingerDetected) {
    vitals.alarmLevel = ALARM_ADVISORY;
    vitals.alertMessage = "Oximeter Detached";
  }

  // --- BUZZER CONTROL ---
  if (vitals.alarmLevel == ALARM_HIGH && !vitals.isSnoozed) {
    digitalWrite(PIN_BUZZER, HIGH); // Continuous siren
  } else {
    digitalWrite(PIN_BUZZER, LOW);
  }
}
