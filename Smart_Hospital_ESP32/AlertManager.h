#ifndef ALERT_MANAGER_H
#define ALERT_MANAGER_H

#include "Config.h"

class AlertManager {
public:
  AlertManager();
  void begin();
  void evaluate(PatientVitals &vitals);
  void testChirp();
  void triggerSnooze();

private:
  unsigned long snoozeUntil;
  bool lastBootButtonState;
};

#endif // ALERT_MANAGER_H
