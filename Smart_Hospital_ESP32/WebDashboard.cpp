#include "WebDashboard.h"
#include "AlertManager.h"

// Medical Log Buffer for Clinical Rounds
struct VitalLogEntry {
  unsigned long timestampSec;
  int bpm;
  int spo2;
  float tempC;
  int saline;
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
    
    /* Hospital Bed Banner */
    .hospital-header { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(14px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 20px 25px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
    .hospital-title h1 { font-size: 24px; font-weight: 700; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .hospital-title p { font-size: 13px; color: #94a3b8; margin-top: 4px; }
    .patient-badge { background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.25); padding: 8px 16px; border-radius: 12px; text-align: right; }
    .patient-badge .name { font-weight: 700; color: #e2e8f0; font-size: 14px; }
    .patient-badge .mrn { font-size: 12px; color: #38bdf8; }
    
    /* Action & Intercom Bar */
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
    .btn-export { background: #059669; }
    .btn-export:hover { background: #047857; }
    
    /* Status Banner */
    .status-banner { padding: 14px 18px; border-radius: 14px; text-align: center; font-weight: 600; font-size: 15px; margin-bottom: 18px; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.3s; }
    .status-normal { background: rgba(34, 197, 94, 0.12); border: 1px solid rgba(34, 197, 94, 0.25); color: #4ade80; }
    .status-alert { background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; animation: pulse 1s infinite alternate; }
    @keyframes pulse { from { opacity: 0.85; transform: scale(1); } to { opacity: 1; transform: scale(1.01); } }
    
    /* ECG Waveform Card */
    .ecg-card { background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 18px; padding: 18px; margin-bottom: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
    .ecg-header { display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #38bdf8; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 10px; }
    canvas { width: 100%; height: 110px; background: #030712; border-radius: 10px; display: block; border: 1px solid rgba(56, 189, 248, 0.1); }
    
    /* Vitals Grid */
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-bottom: 20px; }
    .card { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 18px; padding: 20px; position: relative; transition: transform 0.2s; box-shadow: 0 8px 25px rgba(0,0,0,0.2); }
    .card:hover { transform: translateY(-3px); }
    
    .card-icon { font-size: 28px; margin-bottom: 8px; display: inline-block; }
    .beating { animation: beat 0.9s infinite cubic-bezier(0.215, 0.61, 0.355, 1); }
    @keyframes beat { 0% { transform: scale(1); } 50% { transform: scale(1.25); } 100% { transform: scale(1); } }
    
    .card-title { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; }
    .card-value { font-size: 38px; font-weight: 800; margin: 6px 0; color: #ffffff; }
    .card-unit { font-size: 16px; font-weight: 500; color: #64748b; margin-left: 4px; }
    .card-sub { font-size: 13px; color: #94a3b8; margin-top: 6px; }
    
    /* Saline Progress Bar */
    .progress-bar-container { width: 100%; background: rgba(255, 255, 255, 0.08); border-radius: 10px; height: 16px; margin-top: 12px; overflow: hidden; }
    .progress-bar { height: 100%; border-radius: 10px; transition: width 0.6s ease, background 0.4s ease; background: linear-gradient(90deg, #06b6d4, #3b82f6); }
    
    .footer { text-align: center; font-size: 12px; color: #64748b; margin-top: 20px; padding-bottom: 20px; }
    .footer a { color: #38bdf8; text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <!-- Clinical Bed Banner -->
    <div class="hospital-header">
      <div class="hospital-title">
        <h1>🏥 Apollo Smart Hospital</h1>
        <p>Ward: <b>ICU WARD-B</b> &bull; Station: <b>BED-04</b> &bull; Telemetry Hub</p>
      </div>
      <div class="patient-badge">
        <div class="name">Patient: R. Sharma</div>
        <div class="mrn">MRN: #1042 &bull; Adult Male</div>
      </div>
    </div>

    <!-- Action Bar: Clinical Status & Controls -->
    <div class="action-bar">
      <div style="display: flex; align-items: center; gap: 12px;">
        <span id="ewsBadge" class="status-pill pill-stable">🟢 STABLE (Score: 0)</span>
      </div>
      <div class="btn-group">
        <button class="action-btn" onclick="testVoice()">🔊 Voice Intercom</button>
        <button class="action-btn btn-snooze" onclick="snoozeAlarm()">🔕 Mute Alarm (60s)</button>
        <a href="/download-report" class="action-btn btn-export">📥 Export Rounds Chart (CSV)</a>
      </div>
    </div>

    <!-- Live Status Banner -->
    <div id="statusBanner" class="status-banner status-normal">
      <span>✅</span> <span id="bannerText">Connecting to bedside telemetry...</span>
    </div>

    <!-- Real-time Hospital ECG Waveform Tracing -->
    <div class="ecg-card">
      <div class="ecg-header">
        <span>📈 LIVE CARDIAC ECG / PULSE TRACE</span>
        <span id="ecgRate">LEAD II &bull; 60 BPM</span>
      </div>
      <canvas id="ecgCanvas" width="900" height="110"></canvas>
    </div>

    <div class="grid">
      <!-- Heartbeat Card -->
      <div class="card">
        <div class="card-icon beating">❤️</div>
        <div class="card-title">Pulse Rate (Heartbeat)</div>
        <div class="card-value"><span id="bpm">--</span><span class="card-unit">BPM</span></div>
        <div class="card-sub" id="fingerState">🔍 Optical oximeter active</div>
      </div>

      <!-- SpO2 Card -->
      <div class="card">
        <div class="card-icon">🫁</div>
        <div class="card-title">Blood Oxygen (SpO₂)</div>
        <div class="card-value"><span id="spo2">--</span><span class="card-unit">%</span></div>
        <div class="card-sub">Normal Range: 95% – 100%</div>
      </div>

      <!-- Body Temperature Card -->
      <div class="card">
        <div class="card-icon">🌡️</div>
        <div class="card-title">Body Temperature</div>
        <div class="card-value"><span id="tempC">--</span><span class="card-unit">&deg;C</span></div>
        <div class="card-sub"><span id="tempF">--</span> &deg;F (Normal: 36.5&deg;C – 37.5&deg;C)</div>
      </div>

      <!-- Saline IV Drip Card -->
      <div class="card">
        <div class="card-icon">💧</div>
        <div class="card-title">Saline Drip Level</div>
        <div class="card-value"><span id="salineVal">--</span><span class="card-unit">%</span></div>
        <div class="progress-bar-container">
          <div id="salineBar" class="progress-bar" style="width: 0%;"></div>
        </div>
        <div class="card-sub" id="salineSub">Status: Checking fluid...</div>
      </div>
    </div>

    <div class="footer">
      ESP32 Clinical Bedside Station &bull; Cloud Telemetry via <a href="https://io.adafruit.com" target="_blank">Adafruit IO</a>
    </div>
  </div>

  <script>
    // --- Web Speech API: Communicative Audio Engine ---
    let voiceActive = true;
    let lastSpokenText = "";
    let lastSpokeTime = 0;

    function speakAnnouncement(text) {
      if (!voiceActive || !('speechSynthesis' in window)) return;
      const now = Date.now();
      if (text === lastSpokenText && (now - lastSpokeTime < 12000)) return;

      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(text);
      utter.rate = 0.95;
      utter.pitch = 1.0;
      utter.volume = 1.0;
      utter.lang = 'en-US';
      window.speechSynthesis.speak(utter);
      lastSpokenText = text;
      lastSpokeTime = now;
    }

    function testVoice() {
      speakAnnouncement("Bed four intercom test: hospital audio telemetry active.");
    }

    function snoozeAlarm() {
      fetch('/snooze')
        .then(() => {
          speakAnnouncement("Alarm acknowledged and muted for sixty seconds.");
          document.getElementById('bannerText').innerText = "🔕 Siren Muted by Staff (60s)";
        })
        .catch(err => console.error(err));
    }

    // --- Live ECG Waveform Animation ---
    const canvas = document.getElementById('ecgCanvas');
    const ctx = canvas.getContext('2d');
    let x = 0;
    let lastY = canvas.height / 2;
    let currentBpm = 75;
    let beatStep = 0;

    function drawECG() {
      ctx.fillStyle = 'rgba(3, 7, 18, 0.08)';
      ctx.fillRect(x, 0, 4, canvas.height);

      ctx.beginPath();
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 2.2;
      ctx.shadowBlur = 4;
      ctx.shadowColor = '#22c55e';
      ctx.moveTo(x, lastY);

      let targetY = canvas.height / 2;
      beatStep = (beatStep + 1) % 45;

      if (beatStep === 20) targetY -= 8;
      else if (beatStep === 22) targetY += 12;
      else if (beatStep === 24) targetY -= 48;
      else if (beatStep === 26) targetY += 24;
      else if (beatStep === 30) targetY -= 14;

      x += 2;
      if (x > canvas.width) {
        x = 0;
      }

      ctx.lineTo(x, targetY);
      ctx.stroke();
      lastY = targetY;

      requestAnimationFrame(drawECG);
    }
    drawECG();

    // --- Live Telemetry Data Fetching ---
    function updateTelemetry() {
      fetch('/data')
        .then(response => response.json())
        .then(data => {
          currentBpm = data.finger ? data.bpm : 70;
          document.getElementById('bpm').innerText = data.finger ? data.bpm : '--';
          document.getElementById('spo2').innerText = data.finger ? data.spo2 : '--';
          document.getElementById('fingerState').innerText = data.finger ? '✅ Pulse Detected' : '🔍 Oximeter probe detached';
          document.getElementById('tempC').innerText = data.tempC.toFixed(1);
          document.getElementById('tempF').innerText = data.tempF.toFixed(1);
          document.getElementById('ecgRate').innerText = 'LEAD II • ' + (data.finger ? data.bpm + ' BPM' : 'Probe Detached');
          
          document.getElementById('salineVal').innerText = data.saline;
          const sBar = document.getElementById('salineBar');
          sBar.style.width = data.saline + '%';
          if (data.saline < 10) {
            sBar.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
          } else if (data.saline < 25) {
            sBar.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
          } else {
            sBar.style.background = 'linear-gradient(90deg, #06b6d4, #3b82f6)';
          }
          document.getElementById('salineSub').innerText = 'Level: ' + data.salineStatus + ' (~' + data.salineMins + 'm remaining)';

          const badge = document.getElementById('ewsBadge');
          if (data.ewsStatus === "CRITICAL") {
            badge.className = 'status-pill pill-critical';
            badge.innerText = '🔴 CRITICAL (Score: ' + data.ewsScore + ')';
          } else if (data.ewsStatus === "OBSERVE") {
            badge.className = 'status-pill pill-observe';
            badge.innerText = '🟡 OBSERVE (Score: ' + data.ewsScore + ')';
          } else {
            badge.className = 'status-pill pill-stable';
            badge.innerText = '🟢 STABLE (Score: ' + data.ewsScore + ')';
          }

          const banner = document.getElementById('statusBanner');
          const bannerText = document.getElementById('bannerText');

          if (data.emergency) {
            banner.className = 'status-banner status-alert';
            bannerText.innerText = (data.snoozed ? '🔕 SNOOZED: ' : '🚨 EMERGENCY SIREN: ') + data.alertMsg;

            if (!data.snoozed) {
              if (data.tempC >= 40.0) {
                speakAnnouncement("Emergency: High fever detected on Bed 4. Temperature is over 40 degrees Celsius.");
              } else if (data.nurseCall) {
                speakAnnouncement("Emergency: Nurse assistance requested from Bed 4.");
              } else if (data.saline < 10) {
                speakAnnouncement("Critical Alert: Saline bottle is empty on Bed 4. Please replace intravenous drip immediately.");
              } else if (data.spo2 < 88 && data.finger) {
                speakAnnouncement("Warning: Severe low blood oxygen detected on Bed 4.");
              }
            }
          } else {
            banner.className = 'status-banner status-normal';
            bannerText.innerText = '✅ Patient Status: Stable & Monitored';
          }
        })
        .catch(err => {
          console.error("Telemetry error:", err);
        });
    }
    setInterval(updateTelemetry, 1000);
    window.onload = updateTelemetry;
  </script>
</body>
</html>
)rawliteral";

WebDashboard::WebDashboard() : server(WEB_SERVER_PORT), vitalsRef(nullptr), alertMgrRef(nullptr) {}

void WebDashboard::begin(PatientVitals *sharedVitals, AlertManager *alertManagerRef) {
  vitalsRef = sharedVitals;
  alertMgrRef = alertManagerRef;

  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(DEFAULT_WIFI_SSID, DEFAULT_WIFI_PASSWORD);
  WiFi.softAP(AP_SSID, AP_PASSWORD);

  Serial.println("[WebDashboard] Standalone Hospital SoftAP Started: " AP_SSID);
  Serial.print("[WebDashboard] AP IP: ");
  Serial.println(WiFi.softAPIP());

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 10) {
    delay(500);
    Serial.print(".");
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WebDashboard] Connected to Station Wi-Fi!");
    Serial.print("[WebDashboard] Hospital Station IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WebDashboard] Hotspot not found. Running in Standalone Bedside AP mode.");
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
      csv += String(vitalHistory[i].saline) + ",";
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
    json += "\"saline\":" + String(vitalsRef->salinePercent) + ",";
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
