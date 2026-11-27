#include "WebDashboard.h"
#include "AlertManager.h"
#include <Preferences.h>

Preferences prefs;

// Medical Log Buffer for Clinical Rounds
struct VitalLogEntry {
  unsigned long timestampSec;
  int bpm;
  int spo2;
  float tempC;
  float saline;
  char status[12];
  char event[24];
};

const int MAX_LOGS = 30;
VitalLogEntry vitalHistory[MAX_LOGS];
int logCount = 0;
unsigned long lastLogTime = 0;

const char DASHBOARD_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Smart Hospital - Bedside Telemetry Station</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    body { background: linear-gradient(135deg, #090e17 0%, #162033 100%); color: #f8fafc; min-height: 100vh; padding: 16px; }
    .container { max-width: 980px; margin: 0 auto; }
    
    .hospital-header { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 20px 25px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
    .hospital-title h1 { font-size: 24px; font-weight: 700; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hospital-title p { font-size: 13px; color: #94a3b8; margin-top: 4px; }
    .patient-badge { background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.25); padding: 8px 16px; border-radius: 12px; text-align: right; }
    .patient-badge .name { font-weight: 700; color: #e2e8f0; font-size: 14px; }
    .patient-badge .mrn { font-size: 12px; color: #38bdf8; }
    
    .action-bar { display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 12px 18px; border-radius: 14px; margin-bottom: 16px; flex-wrap: wrap; gap: 10px; }
    .status-pill { display: inline-flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 600; padding: 6px 14px; border-radius: 20px; }
    .pill-stable { background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
    .pill-observe { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .pill-critical { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); animation: pulse 1s infinite alternate; }
    
    .btn-group { display: flex; gap: 10px; flex-wrap: wrap; }
    .action-btn { background: #0284c7; color: white; border: none; padding: 8px 14px; border-radius: 10px; cursor: pointer; font-size: 13px; font-weight: 600; transition: background 0.2s; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; }
    .action-btn:hover { background: #0369a1; }
    .btn-snooze { background: #d97706; }
    .btn-snooze:hover { background: #b45309; }
    .btn-wifi { background: #475569; }
    .btn-wifi:hover { background: #334155; }
    
    .vitals-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; margin-bottom: 16px; }
    .vital-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 18px; position: relative; overflow: hidden; }
    .vital-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; }
    .card-bpm::before { background: #ef4444; }
    .card-spo2::before { background: #06b6d4; }
    .card-temp::before { background: #f59e0b; }
    .card-saline::before { background: #3b82f6; }
    
    .vital-title { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #94a3b8; display: flex; align-items: center; gap: 6px; }
    .vital-value { font-size: 38px; font-weight: 800; font-family: monospace; margin: 10px 0 4px; color: #ffffff; }
    .vital-unit { font-size: 14px; font-weight: 500; color: #94a3b8; margin-left: 4px; }
    .vital-status { font-size: 11px; font-weight: 600; }
    .text-good { color: #4ade80; }
    .text-warn { color: #fbbf24; }
    .text-alert { color: #f87171; }
    
    .ecg-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 18px; margin-bottom: 16px; }
    .ecg-title { font-size: 13px; font-weight: 700; text-transform: uppercase; color: #38bdf8; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    canvas { width: 100%; height: 140px; background: #040810; border-radius: 10px; display: block; }
    
    /* Wi-Fi Setup Form Modal */
    .wifi-box { background: rgba(15, 23, 42, 0.95); border: 1px solid #38bdf8; border-radius: 16px; padding: 20px; margin-bottom: 16px; display: none; }
    .wifi-box h3 { font-size: 16px; color: #38bdf8; margin-bottom: 10px; }
    .wifi-box input { width: 100%; padding: 10px; margin-bottom: 10px; background: #1e293b; border: 1px solid #475569; border-radius: 8px; color: white; font-size: 13px; }
    .wifi-box button { width: 100%; padding: 10px; background: #0284c7; border: none; border-radius: 8px; color: white; font-weight: bold; cursor: pointer; }
    
    @keyframes pulse { from { opacity: 0.7; } to { opacity: 1; } }
  </style>
</head>
<body>
  <div class="container">
    <div class="hospital-header">
      <div class="hospital-title">
        <h1>APOLLO SMART HOSPITAL</h1>
        <p>ICU WARD-B | BEDSIDE TELEMETRY MONITOR</p>
      </div>
      <div class="patient-badge">
        <div class="name">PATIENT: R. Sharma</div>
        <div class="mrn">BED: BED-04 | MRN-1042</div>
      </div>
    </div>

    <div class="action-bar">
      <div id="statusPill" class="status-pill pill-stable">● PATIENT STABLE</div>
      <div class="btn-group">
        <button class="action-btn btn-snooze" onclick="snoozeAlarm()">SNOOZE (60s)</button>
        <button class="action-btn btn-wifi" onclick="toggleWifiBox()">CONFIG WI-FI</button>
        <a class="action-btn" href="/download-report">EXPORT CSV</a>
      </div>
    </div>

    <!-- Dynamic Multi-Hotspot Wi-Fi Setup Box -->
    <div id="wifiBox" class="wifi-box">
      <h3>Multi-Hotspot Wi-Fi Manager</h3>
      <p style="font-size:12px;color:#94a3b8;margin-bottom:12px;">Save up to 2 mobile hotspots. ESP32 will automatically connect to whichever is active!</p>
      <form action="/save-wifi" method="POST">
        <label style="font-size:11px;color:#38bdf8;font-weight:bold;display:block;margin-bottom:4px;">PRIMARY HOTSPOT (PHONE 1):</label>
        <input type="text" name="ssid" placeholder="Hotspot 1 Name (SSID)" required>
        <input type="password" name="pass" placeholder="Hotspot 1 Password">

        <label style="font-size:11px;color:#38bdf8;font-weight:bold;display:block;margin-bottom:4px;">BACKUP HOTSPOT (PHONE 2 / SECONDARY):</label>
        <input type="text" name="ssid2" placeholder="Hotspot 2 Name (Optional)">
        <input type="password" name="pass2" placeholder="Hotspot 2 Password (Optional)">

        <button type="submit">Save Hotspots & Auto-Connect</button>
      </form>
    </div>

    <div class="vitals-grid">
      <div class="vital-card card-bpm">
        <div class="vital-title">Heart Rate (Pulse)</div>
        <div class="vital-value"><span id="bpm">--</span><span class="vital-unit">BPM</span></div>
        <div id="bpmStatus" class="vital-status text-good">60 - 100 Normal</div>
      </div>

      <div class="vital-card card-spo2">
        <div class="vital-title">Blood Oxygen (SpO2)</div>
        <div class="vital-value"><span id="spo2">--</span><span class="vital-unit">%</span></div>
        <div id="spo2Status" class="vital-status text-good">&ge; 95% Optimal</div>
      </div>

      <div class="vital-card card-temp">
        <div class="vital-title">Body Temperature</div>
        <div class="vital-value"><span id="temp">--</span><span class="vital-unit">&deg;C</span></div>
        <div id="tempStatus" class="vital-status text-good">36.1 - 37.0 Normal</div>
      </div>

      <div class="vital-card card-saline">
        <div class="vital-title">IV Saline Fluid</div>
        <div class="vital-value"><span id="saline">--</span><span class="vital-unit">%</span></div>
        <div id="salineStatus" class="vital-status text-good">~<span id="salineMins">--</span>m remaining</div>
      </div>
    </div>

    <div class="ecg-card">
      <div class="ecg-title">
        <span>LEAD-II ECG WAVEFORM (Dynamic 25mm/s)</span>
        <span style="font-size:11px;color:#94a3b8;">Filter: 0.05-40Hz</span>
      </div>
      <canvas id="ecgCanvas" width="900" height="140"></canvas>
    </div>
  </div>

  <script>
    function toggleWifiBox() {
      const box = document.getElementById('wifiBox');
      box.style.display = box.style.display === 'block' ? 'none' : 'block';
    }

    function snoozeAlarm() {
      fetch('/snooze').then(() => alert("Bedside Alarm Snoozed for 60 seconds"));
    }

    // ECG Canvas Simulator
    const canvas = document.getElementById('ecgCanvas');
    const ctx = canvas.getContext('2d');
    let x = 0;
    let step = 0;
    const midY = canvas.height / 2;

    function drawECG() {
      step = (step + 1) % 80;
      let y = midY;
      if (step === 15) y = midY - 8;
      else if (step === 25) y = midY + 4;
      else if (step === 27) y = midY - 45;
      else if (step === 29) y = midY + 12;
      else if (step === 40) y = midY - 12;

      ctx.fillStyle = 'rgba(4, 8, 16, 0.05)';
      ctx.fillRect(x, 0, 4, canvas.height);

      ctx.beginPath();
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 2;
      ctx.moveTo(x, y);
      x = (x + 2) % canvas.width;
      ctx.lineTo(x, y);
      ctx.stroke();

      requestAnimationFrame(drawECG);
    }
    drawECG();

    // Live Telemetry Poller
    setInterval(() => {
      fetch('/data')
        .then(res => res.json())
        .then(data => {
          document.getElementById('bpm').innerText = data.bpm > 0 ? data.bpm : '--';
          document.getElementById('spo2').innerText = data.spo2 > 0 ? data.spo2 : '--';
          document.getElementById('temp').innerText = data.tempC > 0 ? data.tempC.toFixed(1) : '--';
          document.getElementById('saline').innerText = data.saline;
          document.getElementById('salineMins').innerText = data.salineMins;

          const pill = document.getElementById('statusPill');
          pill.className = 'status-pill ' + (data.emergency ? 'pill-critical' : (data.ewsScore > 0 ? 'pill-observe' : 'pill-stable'));
          pill.innerText = data.emergency ? '🚨 ' + data.alertMsg.toUpperCase() : '● PATIENT ' + data.ewsStatus;
        })
        .catch(err => console.log(err));
    }, 2000);
  </script>
</body>
</html>
)rawliteral";

WebDashboard::WebDashboard() : server(80), vitalsRef(nullptr), alertMgrRef(nullptr) {}

void WebDashboard::begin(PatientVitals *vitals, AlertManager *alertMgr) {
  vitalsRef = vitals;
  alertMgrRef = alertMgr;

  // 1. Always start SoftAP so http://192.168.4.1 is ALWAYS reachable!
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAP(AP_SSID, AP_PASSWORD);

  Serial.println("[WebDashboard] Standalone Hospital SoftAP Started: " AP_SSID);
  Serial.print("[WebDashboard] AP IP: ");
  Serial.println(WiFi.softAPIP());

  // 2. Read saved hotspot credentials from ESP32 NVS (Non-Volatile Flash)
  prefs.begin("hospital_wifi", false);
  String savedSSID1 = prefs.getString("ssid", DEFAULT_WIFI_SSID);
  String savedPass1 = prefs.getString("pass", DEFAULT_WIFI_PASSWORD);
  String savedSSID2 = prefs.getString("ssid2", BACKUP_WIFI_SSID);
  String savedPass2 = prefs.getString("pass2", BACKUP_WIFI_PASSWORD);
  prefs.end();

  // 3. Register all known and fallback mobile hotspots into WiFiMulti
  if (savedSSID1.length() > 0 && savedSSID1 != "YOUR_MOBILE_HOTSPOT_NAME") {
    wifiMulti.addAP(savedSSID1.c_str(), savedPass1.c_str());
    Serial.println("[WebDashboard] Hotspot 1 Registered: " + savedSSID1);
  }
  if (savedSSID2.length() > 0 && savedSSID2 != "BACKUP_HOTSPOT_NAME") {
    wifiMulti.addAP(savedSSID2.c_str(), savedPass2.c_str());
    Serial.println("[WebDashboard] Hotspot 2 Registered: " + savedSSID2);
  }
  if (String(DEFAULT_WIFI_SSID) != "YOUR_MOBILE_HOTSPOT_NAME" && String(DEFAULT_WIFI_SSID) != savedSSID1) {
    wifiMulti.addAP(DEFAULT_WIFI_SSID, DEFAULT_WIFI_PASSWORD);
  }
  if (String(BACKUP_WIFI_SSID) != "BACKUP_HOTSPOT_NAME" && String(BACKUP_WIFI_SSID) != savedSSID2) {
    wifiMulti.addAP(BACKUP_WIFI_SSID, BACKUP_WIFI_PASSWORD);
  }

  Serial.println("[WebDashboard] Scanning for active mobile hotspots...");
  int attempts = 0;
  while (wifiMulti.run() != WL_CONNECTED && attempts < 8) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WebDashboard] Connected to active hotspot: " + WiFi.SSID());
    Serial.print("[WebDashboard] Hospital Station IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WebDashboard] Hotspot not found. You can configure any mobile hotspot via http://192.168.4.1");
  }

  setupRoutes();
  server.begin();
  Serial.println("[WebDashboard] HTTP Clinical Server Started.");
}

void WebDashboard::setupRoutes() {
  server.on("/", [this]() {
    server.send_P(200, "text/html", DASHBOARD_HTML);
  });

  server.on("/snooze", [this]() {
    if (alertMgrRef) {
      alertMgrRef->triggerSnooze();
      server.send(200, "text/plain", "Snoozed");
    } else {
      server.send(500, "text/plain", "AlertManager not linked");
    }
  });

  // Dynamic Multi-Hotspot Saver (Stores multiple hotspots into Non-Volatile Flash)
  server.on("/save-wifi", HTTP_POST, [this]() {
    String newSSID = server.arg("ssid");
    String newPass = server.arg("pass");
    String newSSID2 = server.arg("ssid2");
    String newPass2 = server.arg("pass2");

    if (newSSID.length() > 0) {
      prefs.begin("hospital_wifi", false);
      prefs.putString("ssid", newSSID);
      prefs.putString("pass", newPass);
      if (newSSID2.length() > 0) {
        prefs.putString("ssid2", newSSID2);
        prefs.putString("pass2", newPass2);
      }
      prefs.end();

      String html = "<html><body style='font-family:sans-serif;background:#0f172a;color:white;text-align:center;padding:40px;'>";
      html += "<h2 style='color:#38bdf8;'>Multi-Hotspot Wi-Fi Saved!</h2>";
      html += "<p>Primary Hotspot: <b>" + newSSID + "</b></p>";
      if (newSSID2.length() > 0) {
        html += "<p>Backup Hotspot: <b>" + newSSID2 + "</b></p>";
      }
      html += "<p>ESP32 will auto-connect to whichever is active.</p>";
      html += "<p>Rebooting in 3 seconds...</p></body></html>";
      server.send(200, "text/html", html);

      delay(2000);
      ESP.restart();
    } else {
      server.send(400, "text/plain", "Primary SSID cannot be empty");
    }
  });

  // Doctor's Rounds CSV Export Route
  server.on("/download-report", [this]() {
    String csv = "Clinical Rounds Vital Signs Report - " HOSPITAL_NAME "\n";
    csv += "Ward: " WARD_NAME ", Bed: " BED_NUMBER ", Patient: " PATIENT_NAME " (" PATIENT_MRN ")\n";
    csv += "Log_Index,Elapsed_Time_Sec,HeartRate_BPM,SpO2_Pct,Temp_C,Saline_Pct,EWS_Status,Clinical_Event\n";

    for (int i = 0; i < logCount; i++) {
      csv += String(i + 1) + ",";
      csv += String(vitalHistory[i].timestampSec) + ",";
      csv += String(vitalHistory[i].bpm) + ",";
      csv += String(vitalHistory[i].spo2) + ",";
      csv += String(vitalHistory[i].tempC, 2) + ",";
      csv += String(vitalHistory[i].saline, 1) + ",";
      csv += String(vitalHistory[i].status) + ",";
      csv += String(vitalHistory[i].event) + "\n";
    }

    server.sendHeader("Content-Disposition", "attachment; filename=Doctor_Rounds_Bed04.csv");
    server.send(200, "text/csv", csv);
  });

  server.on("/data", [this]() {
    if (!vitalsRef) {
      server.send(500, "text/plain", "Vitals not linked");
      return;
    }

    // Periodically log to in-memory chart for Doctor's report (every 15 seconds)
    if (millis() - lastLogTime >= 15000) {
      lastLogTime = millis();
      int idx = logCount % MAX_LOGS;
      vitalHistory[idx].timestampSec = millis() / 1000;
      vitalHistory[idx].bpm = (int)vitalsRef->heartRateBPM;
      vitalHistory[idx].spo2 = vitalsRef->spo2;
      vitalHistory[idx].tempC = vitalsRef->temperatureC;
      vitalHistory[idx].saline = vitalsRef->salinePercent;
      strncpy(vitalHistory[idx].status, vitalsRef->ewsStatus.c_str(), 11);
      strncpy(vitalHistory[idx].event, vitalsRef->alertMessage.c_str(), 23);
      if (logCount < MAX_LOGS) logCount++;
    }

    String json = "{";
    json += "\"bpm\":" + String((int)vitalsRef->heartRateBPM) + ",";
    json += "\"spo2\":" + String(vitalsRef->spo2) + ",";
    json += "\"finger\":" + String(vitalsRef->fingerDetected ? "true" : "false") + ",";
    json += "\"tempC\":" + String(vitalsRef->temperatureC, 2) + ",";
    json += "\"tempF\":" + String(vitalsRef->temperatureF, 2) + ",";
    json += "\"saline\":" + String(vitalsRef->salinePercent, 1) + ",";
    json += "\"salineGrams\":" + String(vitalsRef->salineWeightGrams, 1) + ",";
    json += "\"salineMins\":" + String(vitalsRef->salineMinutesLeft) + ",";
    json += "\"salineStatus\":\"" + vitalsRef->salineStatus + "\",";
    json += "\"nurseCall\":" + String(vitalsRef->nurseCallActive ? "true" : "false") + ",";
    json += "\"ewsScore\":" + String(vitalsRef->ewsScore) + ",";
    json += "\"ewsStatus\":\"" + vitalsRef->ewsStatus + "\",";
    json += "\"alarmLevel\":" + String((int)vitalsRef->alarmLevel) + ",";
    json += "\"snoozed\":" + String(vitalsRef->isSnoozed ? "true" : "false") + ",";
    json += "\"emergency\":" + String(vitalsRef->isEmergency ? "true" : "false") + ",";
    json += "\"alertMsg\":\"" + vitalsRef->alertMessage + "\"";
    json += "}";
    server.send(200, "application/json", json);
  });
}

void WebDashboard::handleClient() {
  server.handleClient();

  // Automatic seamless hotspot auto-reconnection and roaming
  static unsigned long lastWifiCheck = 0;
  if (millis() - lastWifiCheck > 8000) { // Check every 8 seconds
    lastWifiCheck = millis();
    if (WiFi.status() != WL_CONNECTED) {
      wifiMulti.run();
    }
  }
}

String WebDashboard::getLocalIP() const {
  if (WiFi.status() == WL_CONNECTED) {
    return WiFi.localIP().toString();
  }
  return WiFi.softAPIP().toString();
}

bool WebDashboard::isConnectedToStation() const {
  return WiFi.status() == WL_CONNECTED;
}
