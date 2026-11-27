#ifndef WEB_DASHBOARD_H
#define WEB_DASHBOARD_H

#include "Config.h"
#include <WiFi.h>
#include <WiFiMulti.h>
#include <WebServer.h>

class AlertManager; // Forward declaration

class WebDashboard {
public:
  WebDashboard();
  void begin(PatientVitals *sharedVitals, AlertManager *alertManagerRef);
  void handleClient();
  String getLocalIP() const;
  bool isConnectedToStation() const;

private:
  WebServer server;
  WiFiMulti wifiMulti;
  PatientVitals *vitalsRef;
  AlertManager  *alertMgrRef;

  void setupRoutes();
};

#endif // WEB_DASHBOARD_H
