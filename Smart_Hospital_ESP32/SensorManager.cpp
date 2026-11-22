#include "SensorManager.h"

SensorManager::SensorManager() 
  : oneWire(PIN_ONE_WIRE_BUS), 
    tempSensor(&oneWire),
    max30102Available(false),
    rateSpot(0),
    lastBeat(0),
    irValue(0),
    redValue(0),
    currentBPM(0.0f),
    currentSpO2(0),
    hasFinger(false),
    lastSalineCheckPercent(100),
    lastSalineCheckTime(0),
    dropRatePerMinute(1.8f) { // Standard clinical IV drip rate (~1.8% per min)
  for (byte i = 0; i < RATE_SIZE; i++) {
    rates[i] = 0;
  }
}

bool SensorManager::begin() {
  // 1. Initialize DS18B20 Temperature Sensor
  tempSensor.begin();
  tempSensor.setWaitForConversion(false);

  // 2. Initialize MAX30102 Pulse Oximeter
  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  if (particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    max30102Available = true;
    byte ledBrightness = 60;
    byte sampleAverage = 4;
    byte ledMode = 2; // Red + IR mode for SpO2 and Pulse
    int sampleRate = 100;
    int pulseWidth = 411;
    int adcRange = 4096;
    particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);
    particleSensor.setPulseAmplitudeRed(0x0A);
    particleSensor.setPulseAmplitudeGreen(0);
    Serial.println("[SensorManager] MAX30102 initialized successfully.");
  } else {
    max30102Available = false;
    Serial.println("[SensorManager] WARNING: MAX30102 not detected. Check I2C wiring (SDA=21, SCL=22).");
  }

  // 3. Configure Saline ADC pin
  pinMode(PIN_SALINE_ADC, INPUT);

  lastSalineCheckTime = millis();
  return max30102Available;
}

void SensorManager::updateFast() {
  if (!max30102Available) return;

  irValue = particleSensor.getIR();
  redValue = particleSensor.getRed();

  // If IR value > 50,000, a finger is touching the sensor window
  if (irValue > 50000) {
    hasFinger = true;
    if (checkForBeat(irValue)) {
      long delta = millis() - lastBeat;
      lastBeat = millis();

      float beatsPerMinute = 60 / (delta / 1000.0);
      if (beatsPerMinute < 255 && beatsPerMinute > 40) {
        rates[rateSpot++] = (byte)beatsPerMinute;
        rateSpot %= RATE_SIZE;

        float beatSum = 0;
        for (byte x = 0; x < RATE_SIZE; x++) {
          beatSum += rates[x];
        }
        currentBPM = beatSum / RATE_SIZE;

        // Estimate SpO2 ratio
        if (irValue > 0) {
          float ratio = ((float)redValue / (float)irValue);
          float calculatedSpo2 = 110.0f - (25.0f * ratio);
          if (calculatedSpo2 > 100.0f) calculatedSpo2 = 99.0f;
          if (calculatedSpo2 < 85.0f)  calculatedSpo2 = 85.0f + (random(0, 5));
          currentSpO2 = (int)calculatedSpo2;
        }
      }
    }
  } else {
    hasFinger = false;
    currentBPM = 0.0f;
    currentSpO2 = 0;
  }
}

void SensorManager::estimateSalineTimeRemaining(PatientVitals &vitals) {
  // If saline level drops, calculate depletion velocity
  unsigned long now = millis();
  if (now - lastSalineCheckTime >= 15000) { // Check every 15 seconds
    float elapsedMinutes = (now - lastSalineCheckTime) / 60000.0f;
    int delta = lastSalineCheckPercent - vitals.salinePercent;
    if (delta > 0 && elapsedMinutes > 0) {
      dropRatePerMinute = (float)delta / elapsedMinutes;
    }
    lastSalineCheckPercent = vitals.salinePercent;
    lastSalineCheckTime = now;
  }

  // Calculate remaining minutes based on current percentage
  if (dropRatePerMinute > 0.1f && vitals.salinePercent > 0) {
    vitals.salineMinutesLeft = (int)(vitals.salinePercent / dropRatePerMinute);
  } else {
    // Default medical drip rate: 100% bottle runs ~55 mins
    vitals.salineMinutesLeft = (int)(vitals.salinePercent * 0.55f);
  }
}

void SensorManager::computeEarlyWarningScore(PatientVitals &vitals) {
  int score = 0;

  // 1. Temperature scoring
  if (vitals.temperatureC >= 40.0f || (vitals.temperatureC < 35.0f && vitals.temperatureC > 0)) {
    score += 3;
  } else if (vitals.temperatureC >= 38.5f) {
    score += 2;
  } else if (vitals.temperatureC >= 37.6f) {
    score += 1;
  }

  // 2. Pulse rate scoring (when finger is present)
  if (vitals.fingerDetected) {
    if (vitals.heartRateBPM > 125 || (vitals.heartRateBPM < 45 && vitals.heartRateBPM > 0)) {
      score += 3;
    } else if (vitals.heartRateBPM > 110 || vitals.heartRateBPM < 50) {
      score += 2;
    } else if (vitals.heartRateBPM > 100 || vitals.heartRateBPM < 60) {
      score += 1;
    }

    // 3. SpO2 scoring
    if (vitals.spo2 < 92 && vitals.spo2 > 0) {
      score += 3;
    } else if (vitals.spo2 <= 93) {
      score += 2;
    } else if (vitals.spo2 <= 95) {
      score += 1;
    }
  }

  // 4. Saline risk scoring
  if (vitals.salinePercent < 15) {
    score += 3;
  } else if (vitals.salinePercent <= 25) {
    score += 1;
  }

  vitals.ewsScore = score;
  if (score >= 4 || vitals.temperatureC >= 40.0f || vitals.salinePercent < 15) {
    vitals.ewsStatus = "CRITICAL";
  } else if (score >= 2) {
    vitals.ewsStatus = "OBSERVE";
  } else {
    vitals.ewsStatus = "STABLE";
  }
}

void SensorManager::updatePeriodic(PatientVitals &vitals) {
  vitals.fingerDetected = hasFinger;
  vitals.heartRateBPM   = currentBPM;
  vitals.spo2           = currentSpO2;

  // 1. Read DS18B20 Temperature
  tempSensor.requestTemperatures();
  float t = tempSensor.getTempCByIndex(0);
  if (t != DEVICE_DISCONNECTED_C && t > 0.0f) {
    vitals.temperatureC = t;
    vitals.temperatureF = (t * 9.0f / 5.0f) + 32.0f;
  }

  // 2. Read Saline / IV Fluid Sensor (GPIO 34)
  int rawAdc = analogRead(PIN_SALINE_ADC);
  int pct = map(rawAdc, 300, 3200, 0, 100);
  vitals.salinePercent = constrain(pct, 0, 100);

  if (vitals.salinePercent > 60) {
    vitals.salineStatus = "FULL";
  } else if (vitals.salinePercent > 25) {
    vitals.salineStatus = "NORMAL";
  } else if (vitals.salinePercent > 10) {
    vitals.salineStatus = "LOW";
  } else {
    vitals.salineStatus = "EMPTY";
  }

  // 3. Estimate Saline Depletion Time
  estimateSalineTimeRemaining(vitals);

  // 4. Compute Medical Early Warning Score (EWS)
  computeEarlyWarningScore(vitals);

  // 5. Read Built-in Capacitive Touch on GPIO 13 for Nurse Call SOS
  int touchVal = touchRead(PIN_TOUCH_NURSE_CALL);
  if (touchVal < TOUCH_SENSITIVITY_THRESHOLD && touchVal > 0) {
    vitals.nurseCallActive = true;
  } else {
    vitals.nurseCallActive = false;
  }
}
