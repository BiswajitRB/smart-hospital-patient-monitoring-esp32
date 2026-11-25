#ifndef CLOUD_TELEMETRY_MANAGER_H
#define CLOUD_TELEMETRY_MANAGER_H

#include "Config.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>

class CloudTelemetryManager {
public:
  CloudTelemetryManager();
  void begin();
  bool sendTelemetry(const PatientVitals &vitals);

private:
  String vercelApiUrl;
};

#endif // CLOUD_TELEMETRY_MANAGER_H
