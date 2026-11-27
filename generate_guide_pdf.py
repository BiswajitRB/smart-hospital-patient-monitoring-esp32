import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 756, "APOLLO SMART HOSPITAL | Bedside Telemetry Station & Cloud Sync Guide")
            self.drawRightString(576, 756, "ICU WARD-B | BED-04")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 42, 576, 42)
        
        self.drawString(36, 30, "System Version: ESP32 Firmware v2.6 | Web Cloud: smart-hospital-web.vercel.app")
        self.drawRightString(576, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a')
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0284c7'),
        textTransform='uppercase',
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#0369a1'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0284c7')
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#0f172a')
    )

    story = []

    # Title & Metadata Banner
    story.append(Paragraph("APOLLO SMART HOSPITAL - BEDSIDE IOT HUB", title_style))
    story.append(Paragraph("Standard Operating Procedure: Wi-Fi Setup, Local Bedside Interface & Cloud Synchronization", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0284c7'), spaceAfter=10))

    # Executive Overview
    meta_data = [
        [
            Paragraph("<b>Ward:</b> ICU WARD-B", body_style),
            Paragraph("<b>Bed Station:</b> BED-04", body_style),
            Paragraph("<b>Patient:</b> R. Sharma (MRN-1042)", body_style),
            Paragraph("<b>Local IP:</b> 192.168.4.1", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[135, 135, 135, 135])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # SECTION 1: Wi-Fi Security & 1-Device Exclusive Lock
    story.append(Paragraph("1. ESP32 Wi-Fi Architecture & Security Protocols", h1_style))
    story.append(Paragraph(
        "The bedside station is engineered to eliminate hardcoded credentials while preventing unauthorized interference. "
        "It operates on a dual-layer network stack combining an exclusive local SoftAP and dynamic hotspot roaming (WiFiMulti).",
        body_style
    ))

    sec_data = [
        [
            Paragraph("<b>Parameter</b>", body_style),
            Paragraph("<b>Specification</b>", body_style),
            Paragraph("<b>Clinical / Operational Rationale</b>", body_style)
        ],
        [
            Paragraph("<b>Network SSID</b>", code_style),
            Paragraph("<font color='#0284c7'><b>Smart-Hospital-Bed04</b></font>", body_style),
            Paragraph("Instantly identifies the specific patient bed and ICU ward to attending doctors.", body_style)
        ],
        [
            Paragraph("<b>WPA2 Password</b>", code_style),
            Paragraph("<font color='#0284c7'><b>hospital123</b></font>", body_style),
            Paragraph("Guarantees that only authorized nursing and clinical staff can join the station.", body_style)
        ],
        [
            Paragraph("<b>Connection Limit</b>", code_style),
            Paragraph("<font color='#dc2626'><b>max_connection = 1</b></font>", body_style),
            Paragraph("<b>Exclusive Single-Device Lock:</b> Once Doctor A connects, the ESP32 hardware rejects any other device until Doctor A disconnects. Prevents conflicting controls.", body_style)
        ],
        [
            Paragraph("<b>Zero Hardcoding</b>", code_style),
            Paragraph("Dynamic NVS Flash Memory", body_style),
            Paragraph("Hotspots are configured through the browser and stored in non-volatile flash. No code changes ever required.", body_style)
        ]
    ]
    sec_table = Table(sec_data, colWidths=[120, 160, 260])
    sec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(sec_table)
    story.append(Spacer(1, 10))

    # SECTION 2: Exact Layout of http://192.168.4.1
    story.append(Paragraph("2. Exact Visual Blueprint: Local Bedside Station (http://192.168.4.1)", h1_style))
    story.append(Paragraph(
        "When connected to <b>Smart-Hospital-Bed04</b>, typing <b>http://192.168.4.1</b> in any mobile browser opens the offline bedside station. "
        "It functions 100% autonomously without requiring external internet access:",
        body_style
    ))

    # Visual representation of 192.168.4.1
    ui_mockup_data = [
        [
            Paragraph("<font color='#38bdf8'><b>🏥 APOLLO SMART HOSPITAL</b></font><br/><font color='#94a3b8' size='7'>ICU WARD-B | BEDSIDE TELEMETRY MONITOR</font>", body_style),
            Paragraph("<font color='#e2e8f0'><b>PATIENT: R. Sharma</b></font><br/><font color='#38bdf8' size='7'>BED: BED-04 | MRN-1042</font>", body_style)
        ],
        [
            Paragraph("<font color='#4ade80'><b>● PATIENT STABLE (EWS: 0)</b></font>", body_style),
            Paragraph("<font color='#ffffff'><b>[ SNOOZE (60s) ]</b>&nbsp;&nbsp;&nbsp;&nbsp;<b>[ CONFIG WI-FI ]</b>&nbsp;&nbsp;&nbsp;&nbsp;<b>[ EXPORT CSV ]</b></font>", body_style)
        ],
        [
            Paragraph("<b>HEART RATE (PULSE)</b><br/><font size='16' color='#38bdf8'><b>74</b></font> <font size='8'>BPM</font><br/><font color='#4ade80' size='7'>60 - 100 Normal</font>", body_style),
            Paragraph("<b>BLOOD OXYGEN (SpO2)</b><br/><font size='16' color='#38bdf8'><b>98</b></font> <font size='8'>%</font><br/><font color='#4ade80' size='7'>≥ 95% Optimal</font>", body_style)
        ],
        [
            Paragraph("<b>BODY TEMPERATURE</b><br/><font size='16' color='#38bdf8'><b>36.8</b></font> <font size='8'>°C</font><br/><font color='#4ade80' size='7'>Normothermic (DS18B20)</font>", body_style),
            Paragraph("<b>IV SALINE FLUID</b><br/><font size='16' color='#38bdf8'><b>53.6</b></font> <font size='8'>%</font><br/><font color='#38bdf8' size='7'>HX711 1KG: 268.0g | ~24m remaining</font>", body_style)
        ],
        [
            Paragraph("<b>LEAD-II ECG CARDIAC RHYTHM STRIP (Canvas Oscilloscope)</b><br/><font size='7' color='#94a3b8'>Real-time P-Q-R-S-T synthesis animated at 60 FPS in sync with MAX30102 pulse sensor</font>", body_style),
            Paragraph("<font color='#4ade80'><b>ACTIVE SWEEP: NORMAL SINUS RHYTHM</b></font><br/><font size='7' color='#94a3b8'>Turns red upon arrhythmia; flatlines on probe detach</font>", body_style)
        ]
    ]
    ui_table = Table(ui_mockup_data, colWidths=[270, 270])
    ui_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#38bdf8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#334155')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.white),
    ]))
    story.append(ui_table)
    story.append(Spacer(1, 10))

    # Hotspot Configuration Box Breakdown
    story.append(Paragraph("<b>The Dynamic Multi-Hotspot Setup Box (Opened via 'CONFIG WI-FI'):</b>", h2_style))
    story.append(Paragraph(
        "Tapping <b>[CONFIG WI-FI]</b> opens an interactive form allowing the user to store up to two distinct mobile hotspots "
        "into the ESP32's non-volatile storage. The ESP32 will auto-connect to whichever hotspot is turned on:",
        body_style
    ))

    hotspot_form_data = [
        [
            Paragraph("<b>Field Name</b>", body_style),
            Paragraph("<b>Purpose & Input Format</b>", body_style)
        ],
        [
            Paragraph("<b>PRIMARY HOTSPOT (PHONE 1)</b>", code_style),
            Paragraph("SSID: Phone 1 Hotspot Name (e.g. <i>Biswajit_5G</i>)<br/>Password: Hotspot security passphrase", body_style)
        ],
        [
            Paragraph("<b>BACKUP HOTSPOT (PHONE 2)</b>", code_style),
            Paragraph("SSID: Secondary hotspot or college Wi-Fi (Optional)<br/>Password: Secondary password (Optional)", body_style)
        ],
        [
            Paragraph("<b>ACTION BUTTON</b>", code_style),
            Paragraph("<b>[Save Hotspots & Auto-Connect]</b> — Writes to Preferences NVS and initiates WiFiMulti scan", body_style)
        ]
    ]
    form_table = Table(hotspot_form_data, colWidths=[180, 360])
    form_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(form_table)
    story.append(Spacer(1, 10))

    story.append(PageBreak())

    # SECTION 3: How Local Synchronizes with Cloud
    story.append(Paragraph("3. How the Local Station Synchronizes with the Worldwide Web Dashboard", h1_style))
    story.append(Paragraph(
        "The system employs a <b>Hybrid Edge-Cloud Architecture</b>. The ESP32 maintains simultaneous dual-mode execution: "
        "it serves the bedside monitor locally over SoftAP while transmitting HTTPS JSON telemetry packets to Vercel and MongoDB Atlas every 5 seconds.",
        body_style
    ))

    # Architecture Flow Diagram Table
    flow_data = [
        [
            Paragraph("<b>Layer</b>", body_style),
            Paragraph("<b>Component</b>", body_style),
            Paragraph("<b>Function & Data Transformation</b>", body_style)
        ],
        [
            Paragraph("<b>1. Hardware Layer</b>", body_style),
            Paragraph("ESP32 + Sensors<br/>(MAX30102, DS18B20, HX711)", code_style),
            Paragraph("Samples vitals, calculates EWS score, handles button debounce, and checks 1KG load cell calibration.", body_style)
        ],
        [
            Paragraph("<b>2. Local Edge Layer</b>", body_style),
            Paragraph("SoftAP: 192.168.4.1<br/>Port 80 WebServer", code_style),
            Paragraph("Serves offline bedside UI, handles alarm snooze, provides CSV report downloads directly to physician's phone.", body_style)
        ],
        [
            Paragraph("<b>3. Network Gateway</b>", body_style),
            Paragraph("Mobile Hotspot / Wi-Fi<br/>(WiFiMulti Auto-Roam)", code_style),
            Paragraph("Routes HTTPS JSON payload to Vercel cloud with insecure SSL bypass for zero-friction deployment.", body_style)
        ],
        [
            Paragraph("<b>4. Cloud API Layer</b>", body_style),
            Paragraph("Next.js Serverless API<br/><code>POST /api/telemetry</code>", code_style),
            Paragraph("Validates incoming JSON payload, stores in fast in-memory buffer, and asynchronously updates MongoDB Atlas cluster.", body_style)
        ],
        [
            Paragraph("<b>5. Persistence Layer</b>", body_style),
            Paragraph("MongoDB Atlas Cluster<br/><code>collection: telemetry</code>", code_style),
            Paragraph("Provides permanent patient EHR storage, timestamped vital progression, and clinical audit trail.", body_style)
        ],
        [
            Paragraph("<b>6. Cloud Presentation</b>", body_style),
            Paragraph("Vercel Web Dashboard<br/>smart-hospital-web.vercel.app", code_style),
            Paragraph("Real-time UI polling (2.5s cadence), Lead-II ECG canvas, AI Clinical Decision Support (CDSS), MedBot AI avatar.", body_style)
        ],
        [
            Paragraph("<b>7. Dispatch Layer</b>", body_style),
            Paragraph("Green-API Gateway<br/>Automated WhatsApp", code_style),
            Paragraph("Dispatches instant emergency notifications to duty doctor's WhatsApp upon critical vital threshold triggers.", body_style)
        ]
    ]
    flow_table = Table(flow_data, colWidths=[110, 160, 270])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 10))

    # Parameter Synchronization Table
    story.append(Paragraph("<b>Exact Live Synchronization Parameter Mapping:</b>", h2_style))
    story.append(Paragraph(
        "Notice how the exact same data field flows seamlessly from the ESP32 hardware to both the local bedside screen and the worldwide cloud dashboard:",
        body_style
    ))

    param_data = [
        [
            Paragraph("<b>Vital Parameter</b>", body_style),
            Paragraph("<b>Hardware Reading</b>", body_style),
            Paragraph("<b>Local Display (192.168.4.1)</b>", body_style),
            Paragraph("<b>Cloud Dashboard (Vercel)</b>", body_style)
        ],
        [
            Paragraph("<b>Heart Rate</b>", body_style),
            Paragraph("74 BPM (MAX30102)", code_style),
            Paragraph("Card value: <b>74 BPM</b>", body_style),
            Paragraph("BPM Card + Lead-II ECG Canvas", body_style)
        ],
        [
            Paragraph("<b>Oxygen (SpO2)</b>", body_style),
            Paragraph("98% (MAX30102)", code_style),
            Paragraph("Card value: <b>98%</b>", body_style),
            Paragraph("Respiratory Card: <b>98%</b> (Optimal)", body_style)
        ],
        [
            Paragraph("<b>Body Temp</b>", body_style),
            Paragraph("36.8°C (DS18B20)", code_style),
            Paragraph("Card value: <b>36.8°C</b>", body_style),
            Paragraph("Thermoregulation Card: <b>36.8°C</b>", body_style)
        ],
        [
            Paragraph("<b>Saline Level</b>", body_style),
            Paragraph("268.0g / 500g (HX711)", code_style),
            Paragraph("Card value: <b>53.6%</b> (~24m)", body_style),
            Paragraph("Saline Card: <b>53.6% (268.0g)</b>", body_style)
        ],
        [
            Paragraph("<b>Clinical Triage</b>", body_style),
            Paragraph("Score: 0 / Stable", code_style),
            Paragraph("Badge: <b>● PATIENT STABLE</b>", body_style),
            Paragraph("CDSS: <b>MedBot AI Assessment</b>", body_style)
        ],
        [
            Paragraph("<b>Snooze State</b>", body_style),
            Paragraph("BOOT Pin / Web Route", code_style),
            Paragraph("Status: <b>ALARM SNOOZED (60s)</b>", body_style),
            Paragraph("Banner: <b>STAFF ATTENDING</b>", body_style)
        ]
    ]
    param_table = Table(param_data, colWidths=[100, 140, 150, 150])
    param_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(param_table)
    story.append(Spacer(1, 10))

    # SECTION 4: 6-Step Demonstration Protocol for Viva
    story.append(Paragraph("4. Step-by-Step Demonstration Protocol (For Teachers & Examiners)", h1_style))
    
    steps_data = [
        [
            Paragraph("<b>Step</b>", body_style),
            Paragraph("<b>Action & Operation</b>", body_style),
            Paragraph("<b>Expected System Observation</b>", body_style)
        ],
        [
            Paragraph("<b>Step 1</b>", code_style),
            Paragraph("Power on ESP32 via 5V USB.", body_style),
            Paragraph("16x2 LCD shows: <code>Secure AP Mode1P / Pass:hospital123</code>. Buzzer chirps once.", body_style)
        ],
        [
            Paragraph("<b>Step 2</b>", code_style),
            Paragraph("Join Wi-Fi <b>Smart-Hospital-Bed04</b> with password <b>hospital123</b>.", body_style),
            Paragraph("Phone associates. Single-device lock engages (blocks other phones from connecting).", body_style)
        ],
        [
            Paragraph("<b>Step 3</b>", code_style),
            Paragraph("Open <b>http://192.168.4.1</b> in mobile browser.", body_style),
            Paragraph("Offline Bedside Telemetry Station opens. Displays live cards & ECG rhythm strip.", body_style)
        ],
        [
            Paragraph("<b>Step 4</b>", code_style),
            Paragraph("Tap <b>[CONFIG WI-FI]</b>, enter mobile hotspot name & password, tap Save.", body_style),
            Paragraph("ESP32 confirms save to NVS flash, restarts, and joins hotspot in 3 seconds.", body_style)
        ],
        [
            Paragraph("<b>Step 5</b>", code_style),
            Paragraph("Open <b>https://smart-hospital-web.vercel.app</b> on any device.", body_style),
            Paragraph("Status turns <b>🟢 LIVE STREAMING</b>. AI Clinical Triage & ECG canvas update live.", body_style)
        ],
        [
            Paragraph("<b>Step 6</b>", code_style),
            Paragraph("Touch temperature probe or lift saline bottle.", body_style),
            Paragraph("Buzzer sounds, web turns red, emergency WhatsApp dispatches to doctor's phone.", body_style)
        ]
    ]
    steps_table = Table(steps_data, colWidths=[60, 230, 250])
    steps_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(steps_table)

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF Generated at: {filename}")

if __name__ == "__main__":
    out_path = r"d:\a-hospital project\SMART_HOSPITAL_WIFI_AND_SYNC_GUIDE.pdf"
    build_pdf(out_path)
