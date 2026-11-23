import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group, Circle

def build_pdf():
    pdf_filename = r"D:\a-hospital project\SMART_HOSPITAL_TROUBLESHOOTING_AND_WIRING_GUIDE.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom typography
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        alignment=1,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        alignment=1,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334155')
    )

    alert_box = ParagraphStyle(
        'AlertBox',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#991B1B')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell,
        fontName='Helvetica-Bold'
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell,
        alignment=1
    )

    story = []

    # Title Banner
    story.append(Paragraph("SMART HOSPITAL PATIENT MONITORING - ESP32", title_style))
    story.append(Paragraph("LCD Display Fix & Mobile Web Dashboard Connection Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=8))

    # SECTION 1: MOBILE NO DATA FOUND FIX
    story.append(Paragraph("1. FIX: MOBILE SHOWS 'NO DATA' / 'NO INTERNET' ON WI-FI", h1_style))
    wifi_explanation = (
        "<b>Why this happens:</b> When connecting to Wi-Fi SSID <b>Smart-Hospital-Bed04</b> (Password: <b>hospital123</b>), "
        "your smartphone expects an active Internet gateway. Because the ESP32 is a local medical telemetry hub without an external ISP, "
        "Android/iPhone displays <i>'Connected, without internet'</i> or <i>'No data found'</i> and tries to drop the connection back to 4G/5G mobile data."
    )
    story.append(Paragraph(wifi_explanation, body_style))
    story.append(Spacer(1, 4))

    steps_wifi = [
        ("Step 1", "<b>Turn OFF Mobile Data (4G/5G)</b> on your smartphone. This forces your mobile browser to communicate exclusively over the ESP32 local Wi-Fi link."),
        ("Step 2", "In your Wi-Fi settings, connect to <b>Smart-Hospital-Bed04</b> (Password: <b>hospital123</b>)."),
        ("Step 3", "When your phone shows a prompt: <i>'This network has no internet access. Stay connected?'</i> — tap <b>'YES'</b> (or <b>'Keep Wi-Fi connection'</b>)."),
        ("Step 4", "Open <b>Google Chrome</b> or <b>Safari</b> on your phone and type the exact IP in the URL bar:"),
        ("URL", "<font color='#2563EB' size='11'><b>http://192.168.4.1</b></font>  <i>(Note: Must use <b>http://</b>, NOT https://)</i>"),
        ("Result", "The <b>Apollo Smart Hospital Bedside Dashboard</b> will load immediately with live Lead-II ECG trace, vitals telemetry, alarm snooze, and voice speech intercom!")
    ]

    wifi_table_data = [[Paragraph(s[0], table_cell_bold), Paragraph(s[1], table_cell)] for s in steps_wifi]
    w_tab = Table(wifi_table_data, colWidths=[60, 480])
    w_tab.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BFDBFE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(w_tab)
    story.append(Spacer(1, 10))

    # SECTION 2: LCD DISPLAY FIX
    story.append(Paragraph("2. FIX: 16x2 LCD SCREEN LIGHTS UP BUT SHOWS NO CHARACTERS", h1_style))
    lcd_explanation = (
        "<b>Root Cause:</b> Your photo confirms the backlight is on (Pins 15 & 16 powered). However, on standard 16-pin LCDs (JHD162A), "
        "<b>Pin 3 (V0) controls liquid crystal contrast</b>. If Pin 3 is floating or disconnected, the character pixels have zero contrast voltage, "
        "making the text completely invisible! In addition, <b>Pin 5 (RW) must be connected to GND</b>; if left floating, the LCD stays in Read mode and rejects all commands."
    )
    story.append(Paragraph(lcd_explanation, body_style))
    story.append(Spacer(1, 6))

    # LCD Pinout Table
    lcd_headers = [
        Paragraph("Pin #", table_header),
        Paragraph("LCD Label", table_header),
        Paragraph("Connect Exactly To", table_header),
        Paragraph("Wire Role / Critical Fix Instructions", table_header)
    ]

    lcd_rows = [
        ("Pin 1", "VSS", "ESP32 GND", "Power Ground (Negative rail)"),
        ("Pin 2", "VDD", "ESP32 VIN (5V)", "Logic 5V Power (Must be 5V for strong contrast)"),
        ("Pin 3", "V0 (Contrast)", "ESP32 GND", "CRITICAL FIX: Connect directly to GND! Sets max contrast so letters appear instantly!"),
        ("Pin 4", "RS", "GPIO 19", "Register Select (Command / Data toggling)"),
        ("Pin 5", "RW", "ESP32 GND", "CRITICAL FIX: Must be tied to GND (Enables Write mode)"),
        ("Pin 6", "EN", "GPIO 18", "Enable Strobe Clock"),
        ("Pins 7-10", "D0 - D3", "DO NOT CONNECT", "Leave empty / disconnected (4-bit mode doesn't use D0-D3)"),
        ("Pin 11", "D4", "GPIO 5", "Data Line Bit 4"),
        ("Pin 12", "D5", "GPIO 17", "Data Line Bit 5"),
        ("Pin 13", "D6", "GPIO 16", "Data Line Bit 6"),
        ("Pin 14", "D7", "GPIO 15", "Data Line Bit 7"),
        ("Pin 15", "A (LED+)", "ESP32 VIN (5V)", "Backlight Anode (+)"),
        ("Pin 16", "K (LED-)", "ESP32 GND", "Backlight Cathode (-)")
    ]

    lcd_table_content = [lcd_headers]
    for r in lcd_rows:
        is_crit = "CRITICAL" in r[3]
        bg = colors.HexColor('#FEF2F2') if is_crit else colors.white
        lcd_table_content.append([
            Paragraph(r[0], table_cell_bold),
            Paragraph(r[1], table_cell_bold),
            Paragraph(f"<font color='#B91C1C'><b>{r[2]}</b></font>" if is_crit else f"<b>{r[2]}</b>", table_cell),
            Paragraph(f"<b>{r[3]}</b>" if is_crit else r[3], table_cell)
        ])

    lcd_tab = Table(lcd_table_content, colWidths=[45, 65, 110, 320])
    lcd_tab.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(lcd_tab)
    story.append(Spacer(1, 10))

    # Page Break for Visual Pin Diagram
    story.append(PageBreak())

    # SECTION 3: VISUAL LCD WIRING DRAWING
    story.append(Paragraph("3. VISUAL PIN-BY-PIN LCD TO ESP32 SCHEMATIC", h1_style))
    story.append(Paragraph("Look at your LCD with the screen facing you and the green header pins along the top left:", body_style))
    story.append(Spacer(1, 6))

    # Canvas Drawing: LCD Visual Pinout
    dwg = Drawing(540, 240)
    dwg.add(Rect(0, 0, 540, 240, fillColor=colors.HexColor('#F8FAFC'), strokeColor=colors.HexColor('#E2E8F0'), strokeWidth=1, rx=6, ry=6))

    # LCD Board representation
    dwg.add(Rect(20, 40, 230, 160, fillColor=colors.HexColor('#065F46'), strokeColor=colors.HexColor('#047857'), strokeWidth=2, rx=6, ry=6))
    dwg.add(Rect(35, 75, 200, 75, fillColor=colors.HexColor('#BEF264'), strokeColor=colors.HexColor('#84CC16'), strokeWidth=2, rx=3, ry=3))
    dwg.add(String(135, 120, "APOLLO HOSPITAL", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor('#064E3B'), textAnchor="middle"))
    dwg.add(String(135, 95, "ICU BED-04 INIT", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.HexColor('#064E3B'), textAnchor="middle"))
    dwg.add(String(135, 52, "16x2 LCD (JHD162A)", fontName="Helvetica", fontSize=8, fillColor=colors.white, textAnchor="middle"))

    # ESP32 Board representation
    esp_x, esp_y = 360, 30
    dwg.add(Rect(esp_x, esp_y, 150, 180, fillColor=colors.HexColor('#0F172A'), strokeColor=colors.HexColor('#38BDF8'), strokeWidth=2, rx=6, ry=6))
    dwg.add(String(esp_x + 75, esp_y + 160, "ESP32 NodeMCU", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.white, textAnchor="middle"))

    # Key Pin Wires
    wires = [
        ("Pin 1 (VSS) -> GND", 195, '#1E293B'),
        ("Pin 2 (VDD) -> VIN (5V)", 175, '#DC2626'),
        ("Pin 3 (V0)  -> GND (Fix!)", 155, '#1E293B'),
        ("Pin 4 (RS)  -> GPIO 19", 135, '#EAB308'),
        ("Pin 5 (RW)  -> GND (Fix!)", 115, '#1E293B'),
        ("Pin 6 (EN)  -> GPIO 18", 95, '#8B5CF6'),
        ("Pin 11 (D4) -> GPIO 5", 75, '#3B82F6'),
        ("Pin 12 (D5) -> GPIO 17", 58, '#10B981'),
        ("Pin 13 (D6) -> GPIO 16", 42, '#F97316'),
        ("Pin 14 (D7) -> GPIO 15", 26, '#EC4899'),
    ]

    for label, y_pos, col in wires:
        dwg.add(Line(250, y_pos, 360, y_pos, strokeColor=colors.HexColor(col), strokeWidth=1.5))
        dwg.add(String(305, y_pos + 2, label, fontName="Helvetica-Bold", fontSize=6.5, fillColor=colors.HexColor(col), textAnchor="middle"))

    story.append(dwg)
    story.append(Spacer(1, 10))

    # SECTION 4: MASTER SENSORS TABLE
    story.append(Paragraph("4. MASTER PINOUT FOR ALL OTHER SENSORS", h1_style))
    
    sens_headers = [
        Paragraph("Component", table_header),
        Paragraph("Sensor Pin", table_header),
        Paragraph("ESP32 Pin", table_header),
        Paragraph("Purpose / Function", table_header)
    ]

    sens_rows = [
        ("MAX30102 Pulse Oximeter", "VIN", "3V3 (3.3V)", "Power (Never connect to 5V!)"),
        ("MAX30102 Pulse Oximeter", "GND", "GND", "Ground"),
        ("MAX30102 Pulse Oximeter", "SDA", "GPIO 21", "I2C Data Bus"),
        ("MAX30102 Pulse Oximeter", "SCL", "GPIO 22", "I2C Clock Bus"),
        ("DS18B20 Temp Probe", "VCC / GND / DATA", "3V3 / GND / GPIO 4", "Digital Body Temperature (Onboard 4.7kΩ pull-up)"),
        ("TekBud SEN18 Saline Drip", "+ / - / S (Signal)", "3V3 / GND / GPIO 34", "Saline Fluid Level (Dip in water cup to test!)"),
        ("Active Buzzer", "+ / -", "GPIO 25 / GND", "Medical Siren (Long leg to GPIO 25, Short leg to GND)"),
        ("Touch Nurse SOS", "Bare Wire Pin", "GPIO 13", "Capacitive touch wire (Touch with bare finger!)"),
        ("Hardware Alarm Snooze", "BOOT Button", "GPIO 0", "Physical push button on ESP32 (Snoozes siren for 60s)")
    ]

    sens_content = [sens_headers]
    for sr in sens_rows:
        sens_content.append([
            Paragraph(sr[0], table_cell_bold),
            Paragraph(sr[1], table_cell),
            Paragraph(f"<b>{sr[2]}</b>", table_cell),
            Paragraph(sr[3], table_cell)
        ])

    sens_tab = Table(sens_content, colWidths=[110, 85, 95, 250])
    sens_tab.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(sens_tab)

    # Build Document
    doc.build(story)
    print("SUCCESS: Generated PDF at", pdf_filename)

if __name__ == '__main__':
    build_pdf()
