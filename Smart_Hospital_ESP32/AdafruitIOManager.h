#ifndef ADAFRUIT_IO_MANAGER_H
#define ADAFRUIT_IO_MANAGER_H

#include "Config.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>

class AdafruitIOManager {
public:
  AdafruitIOManager();
  void begin();
  bool publishVitals(const PatientVitals &vitals);

private:
  bool configured;
  bool sendFeedData(const String &feedKey, const String &value);
};

#endif // ADAFRUIT_IO_MANAGER_H
