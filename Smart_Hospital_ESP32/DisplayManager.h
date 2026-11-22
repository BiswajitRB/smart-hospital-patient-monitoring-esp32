#ifndef DISPLAY_MANAGER_H
#define DISPLAY_MANAGER_H

#include "Config.h"

#if USE_I2C_LCD
  #include <LiquidCrystal_I2C.h>
#else
  #include <LiquidCrystal.h>
#endif

class DisplayManager {
public:
  DisplayManager();
  void begin();
  void showBootMessage();
  void showWifiStatus(bool connected, const String &ip);
  void updateDisplay(const PatientVitals &vitals);

private:
#if USE_I2C_LCD
  LiquidCrystal_I2C lcd;
#else
  LiquidCrystal lcd;
#endif
  int currentPage;
  void initCustomIcons();
};

#endif // DISPLAY_MANAGER_H
