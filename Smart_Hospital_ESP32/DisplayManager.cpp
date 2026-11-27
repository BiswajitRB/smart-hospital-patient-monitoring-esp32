#include "DisplayManager.h"

// 5x8 Pixel Art Custom Emojis/Icons for 16x2 HD44780 LCD
const byte ICON_HEART[8] = {
  0b00000, 0b01010, 0b11111, 0b11111, 0b01110, 0b00100, 0b00000, 0b00000
};

const byte ICON_OXYGEN[8] = {
  0b00100, 0b00100, 0b01010, 0b01010, 0b10001, 0b11111, 0b01110, 0b00000
};

const byte ICON_THERMO[8] = {
  0b00100, 0b01010, 0b01010, 0b01110, 0b01110, 0b11111, 0b11111, 0b01110
};

const byte ICON_SALINE[8] = {
  0b01110, 0b00100, 0b11111, 0b10001, 0b11111, 0b11111, 0b11111, 0b01110
};

const byte ICON_DEGREE[8] = {
  0b00110, 0b01001, 0b01001, 0b00110, 0b00000, 0b00000, 0b00000, 0b00000
};

const byte ICON_BELL[8] = {
  0b00100, 0b01110, 0b01110, 0b01110, 0b11111, 0b00000, 0b00100, 0b00000
};

#if USE_I2C_LCD
DisplayManager::DisplayManager() : lcd(LCD_I2C_ADDR, 16, 2), currentPage(0) {}
#else
DisplayManager::DisplayManager() 
  : lcd(PIN_LCD_RS, PIN_LCD_EN, PIN_LCD_D4, PIN_LCD_D5, PIN_LCD_D6, PIN_LCD_D7), 
    currentPage(0) {}
#endif

void DisplayManager::initCustomIcons() {
  lcd.createChar(0, (uint8_t*)ICON_HEART);
  lcd.createChar(1, (uint8_t*)ICON_OXYGEN);
  lcd.createChar(2, (uint8_t*)ICON_THERMO);
  lcd.createChar(3, (uint8_t*)ICON_SALINE);
  lcd.createChar(4, (uint8_t*)ICON_DEGREE);
  lcd.createChar(5, (uint8_t*)ICON_BELL);
}

void DisplayManager::begin() {
#if USE_I2C_LCD
  lcd.init();
  lcd.backlight();
#else
  lcd.begin(16, 2);
#endif
  initCustomIcons();
  lcd.clear();
}

void DisplayManager::showBootMessage() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.write(byte(0));
  lcd.print(" " BED_NUMBER " CLINICAL ");
  lcd.write(byte(3));
  lcd.setCursor(0, 1);
  lcd.print(WARD_NAME " Init..");
}

void DisplayManager::showWifiStatus(bool connected, const String &ip) {
  lcd.clear();
  if (connected) {
    lcd.setCursor(0, 0);
    lcd.print("Hotspot Connected");
    lcd.setCursor(0, 1);
    lcd.print(ip.substring(0, 16));
  } else {
    lcd.setCursor(0, 0);
    lcd.print("Open AP Mode: 1P");
    lcd.setCursor(0, 1);
    lcd.print("AP:" AP_SSID);
  }
}

void DisplayManager::updateDisplay(const PatientVitals &vitals) {
  lcd.clear();

  // 1. Nurse Call SOS Screen Override
  if (vitals.nurseCallActive) {
    lcd.setCursor(0, 0);
    lcd.write(byte(5));
    lcd.print("! NURSE CALL !");
    lcd.write(byte(5));
    lcd.setCursor(0, 1);
    lcd.print(BED_NUMBER " SOS ALERT ");
    return;
  }

  // 2. Alarm Snooze Indicator Override
  if (vitals.isSnoozed && vitals.isEmergency) {
    lcd.setCursor(0, 0);
    lcd.print("[ALARM SNOOZED] ");
    lcd.setCursor(0, 1);
    lcd.print("STAFF ATTENDING ");
    return;
  }

  // 3. High Priority Emergency Flashing Screen
  if (vitals.alarmLevel == ALARM_HIGH && (currentPage % 2 == 1)) {
    lcd.setCursor(0, 0);
    lcd.write(byte(5));
    lcd.print("! EMERGENCY !");
    lcd.write(byte(5));
    lcd.setCursor(0, 1);
    lcd.print(vitals.alertMessage.substring(0, 16));
    currentPage++;
    return;
  }
  currentPage++;

  // Alternate between Hospital ID Screen (Page 0) and Physiological Vitals (Page 1)
  if (currentPage % 3 == 0) {
    // Hospital Identification Screen
    lcd.setCursor(0, 0);
    lcd.print(WARD_NAME " " BED_NUMBER);
    lcd.setCursor(0, 1);
    lcd.print(PATIENT_NAME " " PATIENT_MRN);
    return;
  }

  // --- PHYSIOLOGICAL VITALS SCREEN ---
  // Top Line: [♥] 82  [🫁]98% STAB
  lcd.setCursor(0, 0);
  lcd.write(byte(0)); // Heart Emoji
  if (vitals.fingerDetected) {
    if (vitals.heartRateBPM < 100) lcd.print(" ");
    lcd.print((int)vitals.heartRateBPM);
    lcd.print(" ");
    lcd.write(byte(1)); // Oxygen Droplet Emoji
    lcd.print(vitals.spo2);
    lcd.print("% ");
  } else {
    lcd.print(" -- ");
    lcd.write(byte(1));
    lcd.print("--% ");
  }
  // Clinical status badge (3 chars)
  if (vitals.ewsStatus == "CRITICAL") lcd.print("CRIT");
  else if (vitals.ewsStatus == "OBSERVE") lcd.print("WARN");
  else lcd.print("STAB");

  // Bottom Line: [🌡]36.8°C [💧]53.6%
  lcd.setCursor(0, 1);
  lcd.write(byte(2)); // Thermometer Emoji
  lcd.print(vitals.temperatureC, 1);
  lcd.write(byte(4)); // Degree Symbol
  lcd.print("C ");

  lcd.write(byte(3)); // Saline Bottle Emoji
  lcd.print(vitals.salinePercent, 1);
  lcd.print("%");
}
