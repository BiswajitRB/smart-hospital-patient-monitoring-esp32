import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group, Polygon

def generate_single_page_blueprint(filename):
    # Strictly letter size (612 x 792 pt) with 20pt margins
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # 1. Background clean technical gradient / frame
    c.setFillColor(colors.HexColor("#090e17")) # Deep medical dark theme
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Outer cyan border
    c.setStrokeColor(colors.HexColor("#0284c7"))
    c.setLineWidth(2)
    c.roundRect(14, 14, width - 28, height - 28, 10, fill=0, stroke=1)

    # Inner subtle border
    c.setStrokeColor(colors.HexColor("#1e293b"))
    c.setLineWidth(1)
    c.roundRect(18, 18, width - 36, height - 36, 8, fill=0, stroke=1)

    # 2. Top Title Header
    c.setFillColor(colors.HexColor("#38bdf8"))
    c.setFont("Helvetica-Bold", 15)
    c.drawString(28, height - 42, "🏥 APOLLO SMART HOSPITAL — BEDSIDE STATION & MULTI-HOTSPOT BLUEPRINT")
    
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.setFont("Helvetica", 8)
    c.drawString(28, height - 54, "COMPLETE VISUAL SCHEMATIC OF http://192.168.4.1 (ESP32 EDGE SERVER) & CLOUD SYNC PIPELINE")

    c.setFillColor(colors.HexColor("#10b981"))
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(width - 28, height - 42, "● LIVE OFFLINE AP: 192.168.4.1")
    c.setFillColor(colors.HexColor("#cbd5e1"))
    c.drawRightString(width - 28, height - 54, "WPA2: hospital123 | Lock: 1 Device Only")

    # Divider line
    c.setStrokeColor(colors.HexColor("#38bdf8"))
    c.setLineWidth(1.5)
    c.line(28, height - 60, width - 28, height - 60)

    # -------------------------------------------------------------
    # SECTION A: THE LOCAL BEDSIDE MONITOR SCREEN (MOCKUP ON SCREEN)
    # Box position: x=30, y=345, w=345, h=370
    # -------------------------------------------------------------
    scr_x = 28
    scr_y = 355
    scr_w = 340
    scr_h = 365

    # Screen Outer Bezel (Simulating Doctor's Phone / Tablet Screen)
    c.setFillColor(colors.HexColor("#0b1329"))
    c.setStrokeColor(colors.HexColor("#38bdf8"))
    c.setLineWidth(1.5)
    c.roundRect(scr_x, scr_y, scr_w, scr_h, 8, fill=1, stroke=1)

    # URL Address Bar on phone
    c.setFillColor(colors.HexColor("#1e293b"))
    c.roundRect(scr_x + 8, scr_y + scr_h - 22, scr_w - 16, 15, 4, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#38bdf8"))
    c.setFont("Courier-Bold", 8)
    c.drawString(scr_x + 14, scr_y + scr_h - 18, "🔒 http://192.168.4.1/  (Standalone Bedside)")
    c.setFillColor(colors.HexColor("#10b981"))
    c.setFont("Helvetica-Bold", 7)
    c.drawRightString(scr_x + scr_w - 14, scr_y + scr_h - 18, "DIRECT WI-FI")

    # Header in Mockup
    c.setFillColor(colors.HexColor("#38bdf8"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(scr_x + 12, scr_y + scr_h - 38, "APOLLO SMART HOSPITAL")
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.setFont("Helvetica", 6.5)
    c.drawString(scr_x + 12, scr_y + scr_h - 47, "ICU WARD-B | BEDSIDE TELEMETRY MONITOR")

    # Patient badge right
    c.setFillColor(colors.HexColor("#e2e8f0"))
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(scr_x + scr_w - 12, scr_y + scr_h - 38, "PATIENT: R. Sharma")
    c.setFillColor(colors.HexColor("#38bdf8"))
    c.setFont("Courier-Bold", 7)
    c.drawRightString(scr_x + scr_w - 12, scr_y + scr_h - 47, "BED: BED-04 | MRN-1042")

    # Action Bar Mockup (y ≈ scr_y + scr_h - 75)
    ay = scr_y + scr_h - 75
    # Status Pill
    c.setFillColor(colors.HexColor("#14532d"))
    c.setStrokeColor(colors.HexColor("#22c55e"))
    c.setLineWidth(0.8)
    c.roundRect(scr_x + 10, ay, 95, 18, 4, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#4ade80"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(scr_x + 14, ay + 5, "● PATIENT STABLE")

    # Button 1: Snooze
    c.setFillColor(colors.HexColor("#b45309"))
    c.setStrokeColor(colors.HexColor("#f59e0b"))
    c.roundRect(scr_x + 110, ay, 68, 18, 4, fill=1, stroke=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(scr_x + 115, ay + 5, "SNOOZE (60s)")

    # Button 2: Config WiFi
    c.setFillColor(colors.HexColor("#0284c7"))
    c.setStrokeColor(colors.HexColor("#38bdf8"))
    c.roundRect(scr_x + 182, ay, 78, 18, 4, fill=1, stroke=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(scr_x + 187, ay + 5, "CONFIG WI-FI ⚙")

    # Button 3: Export CSV
    c.setFillColor(colors.HexColor("#334155"))
    c.setStrokeColor(colors.HexColor("#64748b"))
    c.roundRect(scr_x + 264, ay, 66, 18, 4, fill=1, stroke=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(scr_x + 270, ay + 5, "EXPORT CSV")

    # 4 Vital Cards Grid (2x2)
    card_w = (scr_w - 28) / 2 # 156 pt
    card_h = 58

    # Card 1: Heart Rate (Top Left)
    c1_x = scr_x + 10
    c1_y = ay - 68
    c.setFillColor(colors.HexColor("#1e1b4b"))
    c.setStrokeColor(colors.HexColor("#818cf8"))
    c.setLineWidth(1)
    c.roundRect(c1_x, c1_y, card_w, card_h, 6, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#a5b4fc"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(c1_x + 8, c1_y + card_h - 12, "HEART RATE (BPM)")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(c1_x + 8, c1_y + 18, "74")
    c.setFont("Helvetica", 9)
    c.drawString(c1_x + 38, c1_y + 19, "BPM")
    c.setFillColor(colors.HexColor("#4ade80"))
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(c1_x + 8, c1_y + 6, "● 60 - 100 Normal Sinus")

    # Card 2: SpO2 (Top Right)
    c2_x = scr_x + 18 + card_w
    c2_y = c1_y
    c.setFillColor(colors.HexColor("#064e3b"))
    c.setStrokeColor(colors.HexColor("#34d399"))
    c.roundRect(c2_x, c2_y, card_w, card_h, 6, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#a7f3d0"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(c2_x + 8, c2_y + card_h - 12, "BLOOD OXYGEN (SpO2)")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(c2_x + 8, c2_y + 18, "98")
    c.setFont("Helvetica", 9)
    c.drawString(c2_x + 36, c2_y + 19, "%")
    c.setFillColor(colors.HexColor("#4ade80"))
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(c2_x + 8, c2_y + 6, "● ≥ 95% Optimal Oxygen")

    # Card 3: Body Temp (Bottom Left)
    c3_x = c1_x
    c3_y = c1_y - 66
    c.setFillColor(colors.HexColor("#451a03"))
    c.setStrokeColor(colors.HexColor("#fb923c"))
    c.roundRect(c3_x, c3_y, card_w, card_h, 6, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#fed7aa"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(c3_x + 8, c3_y + card_h - 12, "BODY TEMPERATURE")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(c3_x + 8, c3_y + 18, "36.8")
    c.setFont("Helvetica", 9)
    c.drawString(c3_x + 50, c3_y + 19, "°C")
    c.setFillColor(colors.HexColor("#4ade80"))
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(c3_x + 8, c3_y + 6, "● Normothermic Skin")

    # Card 4: IV Saline Level (Bottom Right)
    c4_x = c2_x
    c4_y = c3_y
    c.setFillColor(colors.HexColor("#082f49"))
    c.setStrokeColor(colors.HexColor("#38bdf8"))
    c.roundRect(c4_x, c4_y, card_w, card_h, 6, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#bae6fd"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(c4_x + 8, c4_y + card_h - 12, "IV SALINE (HX711 1KG)")
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(c4_x + 8, c4_y + 18, "53.6")
    c.setFont("Helvetica", 9)
    c.drawString(c4_x + 50, c4_y + 19, "%")
    c.setFillColor(colors.HexColor("#38bdf8"))
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(c4_x + 8, c4_y + 6, "● 268.0g (ETA: ~24 mins)")

    # Lead-II ECG Canvas Box (y ≈ c3_y - 70)
    ecg_y = c3_y - 70
    c.setFillColor(colors.HexColor("#020617"))
    c.setStrokeColor(colors.HexColor("#10b981"))
    c.roundRect(scr_x + 10, ecg_y, scr_w - 20, 62, 6, fill=1, stroke=1)
    
    # ECG Grid Background
    c.setStrokeColor(colors.HexColor("#064e3b"))
    c.setLineWidth(0.3)
    for gx in range(int(scr_x + 10), int(scr_x + scr_w - 10), 16):
        c.line(gx, ecg_y, gx, ecg_y + 62)
    for gy in range(int(ecg_y), int(ecg_y + 62), 12):
        c.line(scr_x + 10, gy, scr_w + scr_x - 10, gy)

    # ECG Waveform Simulated Trace
    c.setStrokeColor(colors.HexColor("#10b981"))
    c.setLineWidth(1.8)
    path = c.beginPath()
    # Baseline
    path.moveTo(scr_x + 14, ecg_y + 30)
    path.lineTo(scr_x + 60, ecg_y + 30)
    # P wave
    path.lineTo(scr_x + 72, ecg_y + 35)
    path.lineTo(scr_x + 80, ecg_y + 30)
    # Q dip
    path.lineTo(scr_x + 95, ecg_y + 26)
    # R peak
    path.lineTo(scr_x + 105, ecg_y + 54)
    # S dip
    path.lineTo(scr_x + 115, ecg_y + 18)
    path.lineTo(scr_x + 125, ecg_y + 30)
    # T wave
    path.lineTo(scr_x + 155, ecg_y + 38)
    path.lineTo(scr_x + 175, ecg_y + 30)
    # Second beat
    path.lineTo(scr_x + 215, ecg_y + 30)
    path.lineTo(scr_x + 225, ecg_y + 35)
    path.lineTo(scr_x + 233, ecg_y + 30)
    path.lineTo(scr_x + 245, ecg_y + 26)
    path.lineTo(scr_x + 255, ecg_y + 54)
    path.lineTo(scr_x + 265, ecg_y + 18)
    path.lineTo(scr_x + 275, ecg_y + 30)
    path.lineTo(scr_x + 305, ecg_y + 38)
    path.lineTo(scr_x + 325, ecg_y + 30)
    c.drawPath(path, fill=0, stroke=1)

    c.setFillColor(colors.HexColor("#a7f3d0"))
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(scr_x + 16, ecg_y + 52, "LEAD-II ECG (25mm/s Sweep) — NORMAL SINUS RHYTHM")

    # -------------------------------------------------------------
    # SECTION B: CALLOUT ARROWS & EXPLANATORY BOXES (RIGHT COLUMN)
    # x=382 to width-28 (width ~ 202 pt)
    # -------------------------------------------------------------
    call_x = 385
    call_w = width - 28 - call_x # ~ 199 pt

    def draw_callout_box(x, y, w, h, title, text, tag_color):
        c.setFillColor(colors.HexColor("#0f172a"))
        c.setStrokeColor(tag_color)
        c.setLineWidth(1)
        c.roundRect(x, y, w, h, 5, fill=1, stroke=1)
        # Title bar
        c.setFillColor(tag_color)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(x + 6, y + h - 11, title)
        # Content
        c.setFillColor(colors.HexColor("#cbd5e1"))
        c.setFont("Helvetica", 6.8)
        lines = text.split("\n")
        line_y = y + h - 22
        for l in lines:
            c.drawString(x + 6, line_y, l)
            line_y -= 9.5

    def draw_arrow(x1, y1, x2, y2, color):
        c.setStrokeColor(color)
        c.setLineWidth(1.2)
        c.line(x1, y1, x2, y2)
        # Arrowhead at (x1, y1) pointing towards screen
        c.setFillColor(color)
        poly = c.beginPath()
        if x1 < x2: # pointing left
            poly.moveTo(x1, y1)
            poly.lineTo(x1 + 4, y1 + 3)
            poly.lineTo(x1 + 4, y1 - 3)
        else: # pointing right
            poly.moveTo(x1, y1)
            poly.lineTo(x1 - 4, y1 + 3)
            poly.lineTo(x1 - 4, y1 - 3)
        poly.close()
        c.drawPath(poly, fill=1, stroke=0)

    # Box 1: Address & Security Callout
    b1_y = scr_y + scr_h - 32
    b1_h = 42
    draw_callout_box(call_x, b1_y, call_w, b1_h, "1. SECURE STANDALONE AP (NO INTERNET NEEDED)", 
                     "• SSID: Smart-Hospital-Bed04 | Pass: hospital123\n• max_connection = 1: Once connected, ESP32\n  blocks all other devices at MAC level!", colors.HexColor("#38bdf8"))
    draw_arrow(scr_x + scr_w, scr_y + scr_h - 15, call_x, b1_y + 20, colors.HexColor("#38bdf8"))

    # Box 2: Actions Bar Callout
    b2_y = b1_y - 68
    b2_h = 58
    draw_callout_box(call_x, b2_y, call_w, b2_h, "2. CLINICAL CONTROLS & CSV EXPORT", 
                     "• SNOOZE (60s): Mutes physical buzzer siren.\n• CONFIG WI-FI: Opens Multi-Hotspot modal.\n• EXPORT CSV: Downloads patient vital history\n  spreadsheet directly into doctor's phone!", colors.HexColor("#f59e0b"))
    draw_arrow(scr_x + 220, ay + 9, call_x, b2_y + 28, colors.HexColor("#f59e0b"))

    # Box 3: Optical Heart Rate & SpO2
    b3_y = b2_y - 72
    b3_h = 60
    draw_callout_box(call_x, b3_y, call_w, b3_h, "3. MAX30102 PULSE & SpO2 SENSOR", 
                     "• Photoplethysmography (PPG) capillary sensing.\n• Live BPM & blood oxygen saturation (%)\n• IEC 60601-1-8 Alarm: Lead-off detection\n  prevents false sirens when finger detached.", colors.HexColor("#818cf8"))
    draw_arrow(c1_x + card_w, c1_y + 30, call_x, b3_y + 30, colors.HexColor("#818cf8"))

    # Box 4: DS18B20 Temp & HX711 Load Cell
    b4_y = b3_y - 82
    b4_h = 70
    draw_callout_box(call_x, b4_y, call_w, b4_h, "4. TEMP & 1KG LOAD CELL (HX711)", 
                     "• DS18B20: Waterproof digital probe (±0.5°C)\n• HX711 1KG Bar: Gram-accurate saline fluid.\n• 1-Decimal Readout: Shows 53.6%, 10.5%\n• Smart Velocity: Calculates minutes remaining\n  (ETA: ~24m) before air embolism occurs!", colors.HexColor("#38bdf8"))
    draw_arrow(c4_x + card_w, c4_y + 30, call_x, b4_y + 35, colors.HexColor("#38bdf8"))

    # Box 5: Live ECG Oscilloscope
    b5_y = b4_y - 68
    b5_h = 56
    draw_callout_box(call_x, b5_y, call_w, b5_h, "5. LIVE LEAD-II ECG CARDIAC CANVAS", 
                     "• 60 FPS HTML5 canvas oscilloscope.\n• Dynamic P-Q-R-S-T synthesis synced to pulse.\n• Turns warning RED on tachycardia / crisis;\n  drops to flatline baseline on sensor detach.", colors.HexColor("#10b981"))
    draw_arrow(scr_x + scr_w - 10, ecg_y + 31, call_x, b5_y + 28, colors.HexColor("#10b981"))

    # -------------------------------------------------------------
    # SECTION C: THE MULTI-HOTSPOT MODAL (EXPANDED BLUEPRINT)
    # x=28, y=182, w=556, h=155
    # -------------------------------------------------------------
    mod_x = 28
    mod_y = 192
    mod_w = width - 56
    mod_h = 145

    # Modal Background Container
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setStrokeColor(colors.HexColor("#38bdf8"))
    c.setLineWidth(1.5)
    c.roundRect(mod_x, mod_y, mod_w, mod_h, 8, fill=1, stroke=1)

    # Modal Header
    c.setFillColor(colors.HexColor("#38bdf8"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(mod_x + 14, mod_y + mod_h - 18, "⚙ DYNAMIC MULTI-HOTSPOT WI-FI MANAGER (OPENED VIA 'CONFIG WI-FI')")
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.setFont("Helvetica", 7.5)
    c.drawString(mod_x + 14, mod_y + mod_h - 29, "Stores multiple credentials in ESP32 Non-Volatile Storage (NVS). Auto-connects to whichever hotspot is turned on!")

    # Input Fields Layout (2 Columns)
    col_w = (mod_w - 38) / 2 # ~ 259 pt

    # Left Column: Primary Hotspot
    in1_x = mod_x + 14
    in1_y = mod_y + 42

    c.setFillColor(colors.HexColor("#38bdf8"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(in1_x, in1_y + 54, "PRIMARY HOTSPOT (PHONE 1 / DOCTOR'S PHONE):")

    # SSID 1
    c.setFillColor(colors.HexColor("#1e293b"))
    c.setStrokeColor(colors.HexColor("#475569"))
    c.setLineWidth(0.8)
    c.roundRect(in1_x, in1_y + 28, col_w, 20, 4, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#e2e8f0"))
    c.setFont("Courier", 7.5)
    c.drawString(in1_x + 8, in1_y + 35, "SSID: Biswajit_5G (or MyHotspot)")

    # Pass 1
    c.setFillColor(colors.HexColor("#1e293b"))
    c.roundRect(in1_x, in1_y + 4, col_w, 20, 4, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.drawString(in1_x + 8, in1_y + 11, "Password: ••••••••••••")

    # Right Column: Backup Hotspot
    in2_x = in1_x + col_w + 10
    in2_y = in1_y

    c.setFillColor(colors.HexColor("#38bdf8"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(in2_x, in2_y + 54, "BACKUP HOTSPOT (PHONE 2 / SECONDARY / CAMPUS):")

    # SSID 2
    c.setFillColor(colors.HexColor("#1e293b"))
    c.roundRect(in2_x, in2_y + 28, col_w, 20, 4, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#e2e8f0"))
    c.setFont("Courier", 7.5)
    c.drawString(in2_x + 8, in2_y + 35, "SSID: Friend_Phone (or College_WiFi)")

    # Pass 2
    c.setFillColor(colors.HexColor("#1e293b"))
    c.roundRect(in2_x, in2_y + 4, col_w, 20, 4, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.drawString(in2_x + 8, in2_y + 11, "Password: •••••••••••• (Optional)")

    # Bottom Submit Button
    btn_y = mod_y + 10
    c.setFillColor(colors.HexColor("#0284c7"))
    c.setStrokeColor(colors.HexColor("#38bdf8"))
    c.setLineWidth(1)
    c.roundRect(in1_x, btn_y, mod_w - 28, 22, 5, fill=1, stroke=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawCentredString(mod_x + (mod_w / 2), btn_y + 7, "💾 SAVE HOTSPOTS & AUTO-CONNECT (Saves to Flash -> Scans with WiFiMulti -> Reboots in 3s)")

    # -------------------------------------------------------------
    # SECTION D: HOW LOCAL SYNCHRONIZES WITH WORLDWIDE WEB (FLOW)
    # y=24 to 175 (Height ~ 150 pt)
    # -------------------------------------------------------------
    sync_y = 26
    sync_h = 152
    c.setFillColor(colors.HexColor("#0b1329"))
    c.setStrokeColor(colors.HexColor("#10b981"))
    c.setLineWidth(1.5)
    c.roundRect(mod_x, sync_y, mod_w, sync_h, 8, fill=1, stroke=1)

    c.setFillColor(colors.HexColor("#10b981"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(mod_x + 14, sync_y + sync_h - 16, "🔄 CLOUD SYNCHRONIZATION ARCHITECTURE: LOCAL BED (192.168.4.1) ➔ WORLDWIDE CLOUD (VERCEL)")
    
    # 4 Flow Steps Blocks
    step_w = (mod_w - 46) / 4 # ~ 127 pt
    step_h = 100
    s_y = sync_y + 16

    steps_info = [
        ("1. BEDSIDE TRANSDUCTION", "#818cf8", [
            "• MAX30102 Optical PPG",
            "• DS18B20 1-Wire Temp",
            "• HX711 1KG Load Cell",
            "• Touch SOS on GPIO 13",
            "Zero block non-timeout"
        ]),
        ("2. DUAL-MODE ESP32", "#38bdf8", [
            "• Direct SoftAP on port 80",
            "• Serves 192.168.4.1 UI",
            "• WiFiMulti Hotspot Gateway",
            "• HTTPS JSON serializer",
            "Every 5-second interval"
        ]),
        ("3. VERCEL SERVERLESS", "#f59e0b", [
            "• POST /api/telemetry",
            "• Resilient in-memory cache",
            "• MongoDB Atlas Cluster",
            "• Long-term EHR archiving",
            "15s offline watchdog"
        ]),
        ("4. WORLDWIDE CLOUD", "#10b981", [
            "• smart-hospital-web",
            "• MedBot AI v2.4 Triage",
            "• Lead-II ECG 60 FPS",
            "• Automated WhatsApp Bot",
            "Global Duty Doctor Alert"
        ])
    ]

    for idx, (stitle, scolor, slines) in enumerate(steps_info):
        sx = mod_x + 12 + idx * (step_w + 8)
        c.setFillColor(colors.HexColor("#0f172a"))
        c.setStrokeColor(colors.HexColor(scolor))
        c.setLineWidth(1)
        c.roundRect(sx, s_y, step_w, step_h, 5, fill=1, stroke=1)

        # Header tag
        c.setFillColor(colors.HexColor(scolor))
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(sx + 6, s_y + step_h - 13, stitle)

        # Content
        c.setFillColor(colors.HexColor("#cbd5e1"))
        c.setFont("Helvetica", 6.8)
        ly = s_y + step_h - 26
        for line in slines:
            c.drawString(sx + 6, ly, line)
            ly -= 12

        # Connecting Flow Arrow between boxes
        if idx < 3:
            arr_x = sx + step_w
            arr_y = s_y + (step_h / 2)
            c.setStrokeColor(colors.HexColor("#38bdf8"))
            c.setLineWidth(1.8)
            c.line(arr_x + 1, arr_y, arr_x + 7, arr_y)
            # Arrowhead
            poly = c.beginPath()
            poly.moveTo(arr_x + 7, arr_y)
            poly.lineTo(arr_x + 4, arr_y + 3)
            poly.lineTo(arr_x + 4, arr_y - 3)
            poly.close()
            c.setFillColor(colors.HexColor("#38bdf8"))
            c.drawPath(poly, fill=1, stroke=0)

    # Bottom summary tag
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.setFont("Helvetica-Oblique", 7)
    c.drawString(mod_x + 14, sync_y + 5, "✔ Result: When you warm the temp probe or lift the saline bottle, both 192.168.4.1 and smart-hospital-web.vercel.app update synchronously in real-time!")

    c.save()
    print(f"[SUCCESS] 1-Page Blueprint Generated: {filename}")

if __name__ == "__main__":
    out_file = r"d:\a-hospital project\BEDSIDE_STATION_AND_WIFI_BLUEPRINT_1PAGE.pdf"
    generate_single_page_blueprint(out_file)
