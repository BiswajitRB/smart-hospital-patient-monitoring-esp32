#include "AdafruitIOManager.h"

AdafruitIOManager::AdafruitIOManager() : configured(false) {}

void AdafruitIOManager::begin() {
  String user = AIO_USERNAME;
  if (user != "YOUR_ADAFRUIT_USERNAME" && user.length() > 0) {
    configured = true;
    Serial.println("[AdafruitIO] Configured for user: " + user);
  } else {
    configured = false;
    Serial.println("[AdafruitIO] Running in local mode. (To enable cloud, set AIO_USERNAME & AIO_KEY in Config.h)");
  }
}

bool AdafruitIOManager::publishVitals(const PatientVitals &vitals) {
  if (!configured || WiFi.status() != WL_CONNECTED) {
    return false;
  }

  Serial.println("[AdafruitIO] Uploading vitals to iot.adafruit.com (5s interval)...");

  // Publish the 4 parameters demonstrated in the video:
  // 1. Heartbeat / Pulse Rate
  sendFeedData(AIO_FEED_HEARTBEAT, String((int)vitals.heartRateBPM));

  // 2. Oxygen Level (SpO2)
  sendFeedData(AIO_FEED_OXYGEN, String(vitals.spo2));

  // 3. Body Temperature
  sendFeedData(AIO_FEED_TEMP, String(vitals.temperatureC, 1));

  // 4. Saline Level
  sendFeedData(AIO_FEED_SALINE, String(vitals.salinePercent));

  return true;
}

bool AdafruitIOManager::sendFeedData(const String &feedKey, const String &value) {
  WiFiClientSecure client;
  client.setInsecure(); // Connect securely without needing manual SSL certificate bundle

  HTTPClient https;
  String url = "https://io.adafruit.com/api/v2/" + String(AIO_USERNAME) + "/feeds/" + feedKey + "/data";

  if (https.begin(client, url)) {
    https.addHeader("Content-Type", "application/json");
    https.addHeader("X-AIO-Key", AIO_KEY);

    String payload = "{\"value\":\"" + value + "\"}";
    int httpCode = https.POST(payload);

    if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_CREATED) {
      Serial.println("[AdafruitIO] " + feedKey + " -> " + value + " [OK]");
      https.end();
      return true;
    } else {
      Serial.println("[AdafruitIO] " + feedKey + " failed. HTTP: " + String(httpCode));
    }
    https.end();
  }
  return false;
}
