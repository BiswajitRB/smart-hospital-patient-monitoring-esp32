#ifndef SENSOR_MANAGER_H
#define SENSOR_MANAGER_H

#include "Config.h"
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "MAX30105.h"
#include "heartRate.h"
#include "HX711.h"

class SensorManager {
public:
  SensorManager();
  bool begin();
  void updateFast();
  void updatePeriodic(PatientVitals &vitals);
  float getSalineGrams() const { return currentSalineGrams; }

private:
  OneWire oneWire;
  DallasTemperature tempSensor;
  MAX30105 particleSensor;
  bool max30102Available;

  // HX711 1KG Load Cell Saline Weight Sensor
  HX711 scale;
  bool  hx711Available;
  float currentSalineGrams;

  // Pulse & SpO2 estimation variables
  static const byte RATE_SIZE = 4;
  byte rates[RATE_SIZE];
  byte rateSpot;
  long lastBeat;
  long irValue;
  long redValue;
  float currentBPM;
  int   currentSpO2;
  bool  hasFinger;

  // Smart Saline Depletion Analytics
  int lastSalineCheckPercent;
  unsigned long lastSalineCheckTime;
  float dropRatePerMinute;

  void computeEarlyWarningScore(PatientVitals &vitals);
  void estimateSalineTimeRemaining(PatientVitals &vitals);
};

#endif // SENSOR_MANAGER_H
