#include "CloudTelemetryManager.h"

CloudTelemetryManager::CloudTelemetryManager() {
  vercelApiUrl = VERCEL_TELEMETRY_URL;
}

void CloudTelemetryManager::begin() {
  Serial.println("[CloudTelemetry] Manager Initialized. Target: " + vercelApiUrl);
}

bool CloudTelemetryManager::sendTelemetry(const PatientVitals &vitals) {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }

  WiFiClientSecure client;
  client.setInsecure(); // Allows secure HTTPS connection to Vercel without hardcoding SSL certs

  HTTPClient http;
  if (!http.begin(client, vercelApiUrl)) {
    return false;
  }

  http.addHeader("Content-Type", "application/json");

  // Construct JSON payload matching Next.js Vercel API
  String jsonPayload = "{";
  jsonPayload += "\"bed\":\"" + String(BED_NUMBER) + "\",";
  jsonPayload += "\"ward\":\"" + String(WARD_NAME) + "\",";
  jsonPayload += "\"hospital\":\"" + String(HOSPITAL_NAME) + "\",";
  jsonPayload += "\"patient\":\"" + String(PATIENT_NAME) + "\",";
  jsonPayload += "\"mrn\":\"" + String(PATIENT_MRN) + "\",";
  jsonPayload += "\"heartRate\":" + String((int)vitals.heartRateBPM) + ",";
  jsonPayload += "\"spo2\":" + String(vitals.spo2) + ",";
  jsonPayload += "\"temperature\":" + String(vitals.temperatureC, 1) + ",";
  jsonPayload += "\"salinePercent\":" + String(vitals.salinePercent) + ",";
  jsonPayload += "\"salineMinutesLeft\":" + String(vitals.salineMinutesLeft) + ",";
  jsonPayload += "\"salineStatus\":\"" + String(vitals.salineStatus) + "\",";
  jsonPayload += "\"nurseCallActive\":" + String(vitals.nurseCallActive ? "true" : "false") + ",";
  jsonPayload += "\"ewsScore\":" + String(vitals.ewsScore) + ",";
  jsonPayload += "\"ewsStatus\":\"" + String(vitals.ewsStatus) + "\",";
  jsonPayload += "\"alarmLevel\":" + String((int)vitals.alarmLevel) + ",";
  jsonPayload += "\"isEmergency\":" + String(vitals.isEmergency ? "true" : "false") + ",";
  jsonPayload += "\"isSnoozed\":" + String(vitals.isSnoozed ? "true" : "false") + ",";
  jsonPayload += "\"alertMessage\":\"" + String(vitals.alertMessage) + "\"";
  jsonPayload += "}";

  int httpResponseCode = http.POST(jsonPayload);
  bool success = (httpResponseCode >= 200 && httpResponseCode < 300);

  if (success) {
    Serial.println("[CloudTelemetry] Synced to Vercel & MongoDB successfully (HTTP " + String(httpResponseCode) + ")");
  } else {
    Serial.println("[CloudTelemetry] Warning: Sync failed (HTTP " + String(httpResponseCode) + ")");
  }

  http.end();
  return success;
}
