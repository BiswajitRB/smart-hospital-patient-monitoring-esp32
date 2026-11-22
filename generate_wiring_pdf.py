import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group, Circle, Polygon

def build_pdf():
    pdf_filename = r"D:\a-hospital project\ESP32_Smart_Hospital_Hardware_Wiring_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        alignment=1, # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2563EB'),
        alignment=1,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
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

    note_style = ParagraphStyle(
        'NoteText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#475569')
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("SMART HOSPITAL PATIENT HEALTH MONITORING SYSTEM", title_style))
    story.append(Paragraph("Step-by-Step Hardware Wiring & Pinout Guide | ESP32 WROOM-32 NodeMCU", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=10))

    # Architecture Overview Paragraph
    overview_text = (
        "<b>Overview:</b> This bedside unit continuously acquires patient vitals via MAX30102 (BPM & SpO2), "
        "DS18B20 (Body Temp), and TekBud SEN18 (IV Saline Fluid Level). All critical alerts trigger an active acoustic "
        "buzzer (GPIO 25) with a physical BOOT-button snooze and a capacitive touch Nurse SOS wire (GPIO 13). "
        "A 16x2 LCD display provides bedside metrics, mirrored simultaneously onto the local Wi-Fi web dashboard."
    )
    story.append(Paragraph(overview_text, body_style))
    story.append(Spacer(1, 10))

    # 1. Master Pinout Table
    story.append(Paragraph("1. MASTER COMPONENT WIRING TABLE", h1_style))
    
    headers = [
        Paragraph("Component", table_header),
        Paragraph("Sensor Pin", table_header),
        Paragraph("ESP32 Pin", table_header),
        Paragraph("Voltage", table_header),
        Paragraph("Wire / Color", table_header),
        Paragraph("Functional Purpose", table_header)
    ]

    raw_data = [
        ("MAX30102 Pulse & SpO2", "VIN / VCC", "3V3", "3.3V", "Red", "Power 3.3V (Do not use 5V)"),
        ("MAX30102 Pulse & SpO2", "GND", "GND", "0V", "Black", "System Ground"),
        ("MAX30102 Pulse & SpO2", "SDA", "GPIO 21", "3.3V", "Green", "I2C Serial Data Bus"),
        ("MAX30102 Pulse & SpO2", "SCL", "GPIO 22", "3.3V", "Yellow", "I2C Serial Clock Bus"),
        ("DS18B20 Temp Sensor", "VCC (Red)", "3V3", "3.3V", "Red", "Probe Power"),
        ("DS18B20 Temp Sensor", "GND (Black)", "GND", "0V", "Black", "Ground"),
        ("DS18B20 Temp Sensor", "DATA (Yellow)", "GPIO 4", "3.3V", "Yellow", "OneWire Bus (Onboard 4.7kΩ pullup)"),
        ("SEN18 Saline Drip", "+ (VCC)", "3V3", "3.3V", "Red", "3.3V Excitation voltage"),
        ("SEN18 Saline Drip", "- (GND)", "GND", "0V", "Black", "Ground reference"),
        ("SEN18 Saline Drip", "S (Signal)", "GPIO 34", "Analog", "Blue", "ADC1 Analog Channel (Wi-Fi safe)"),
        ("Active Alarm Buzzer", "Long leg (+)", "GPIO 25", "3.3V", "Red", "DAC1 digital siren drive"),
        ("Active Alarm Buzzer", "Short leg (-)", "GND", "0V", "Black", "Ground reference"),
        ("Nurse Call SOS", "Bare Wire", "GPIO 13", "Touch", "Orange", "ESP32 Capacitive Touch Channel"),
        ("Alarm Snooze", "BOOT Button", "GPIO 0", "Internal", "N/A", "Onboard physical button on ESP32"),
        ("16x2 LCD (SixOhms)", "Pin 1 (VSS)", "GND", "0V", "Black", "LCD Ground"),
        ("16x2 LCD (SixOhms)", "Pin 2 (VDD)", "VIN (5V)", "5V", "Red", "LCD Logic 5V Power"),
        ("16x2 LCD (SixOhms)", "Pin 3 (V0)", "Pot Wiper", "0-5V", "Gray", "Contrast adjust (or tie to GND)"),
        ("16x2 LCD (SixOhms)", "Pin 4 (RS)", "GPIO 19", "3.3V", "Yellow", "Register Select (Command/Data)"),
        ("16x2 LCD (SixOhms)", "Pin 5 (RW)", "GND", "0V", "Black", "Write Mode (Tied to Ground)"),
        ("16x2 LCD (SixOhms)", "Pin 6 (EN)", "GPIO 18", "3.3V", "White", "Clock Enable Strobe"),
        ("16x2 LCD (SixOhms)", "Pin 11 (D4)", "GPIO 5", "3.3V", "Blue", "Data Bit 4"),
        ("16x2 LCD (SixOhms)", "Pin 12 (D5)", "GPIO 17", "3.3V", "Green", "Data Bit 5"),
        ("16x2 LCD (SixOhms)", "Pin 13 (D6)", "GPIO 16", "3.3V", "Orange", "Data Bit 6"),
        ("16x2 LCD (SixOhms)", "Pin 14 (D7)", "GPIO 15", "3.3V", "Purple", "Data Bit 7"),
        ("16x2 LCD (SixOhms)", "Pin 15 (A)", "VIN (5V)", "5V", "Red", "Backlight LED Anode (+)"),
        ("16x2 LCD (SixOhms)", "Pin 16 (K)", "GND", "0V", "Black", "Backlight LED Cathode (-)")
    ]

    table_content = [headers]
    for row in raw_data:
        table_content.append([
            Paragraph(row[0], table_cell_bold),
            Paragraph(row[1], table_cell),
            Paragraph(row[2], table_cell_bold),
            Paragraph(row[3], table_cell_center),
            Paragraph(row[4], table_cell_center),
            Paragraph(row[5], table_cell)
        ])

    table = Table(table_content, colWidths=[105, 75, 60, 45, 55, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(table)
    story.append(Spacer(1, 14))

    # Page Break for Visual Architecture Diagrams & Detailed Breakdowns
    story.append(PageBreak())

    # 2. Visual Schematic Diagram
    story.append(Paragraph("2. COMPLETE VISUAL HARDWARE SCHEMATIC DIAGRAM", h1_style))
    story.append(Paragraph("Connect all common GNDs and 3.3V rails cleanly on the breadboard side strips.", note_style))
    story.append(Spacer(1, 6))

    # DRAWING: Clean SVG-style Schematic on ReportLab Canvas
    # Canvas Dimensions: width 540, height 330
    dwg = Drawing(540, 330)

    # Background Canvas Box
    dwg.add(Rect(0, 0, 540, 330, fillColor=colors.HexColor('#F8FAFC'), strokeColor=colors.HexColor('#E2E8F0'), strokeWidth=1, rx=6, ry=6))

    # ESP32 Center Block
    esp_x, esp_y, esp_w, esp_h = 190, 45, 160, 255
    dwg.add(Rect(esp_x, esp_y, esp_w, esp_h, fillColor=colors.HexColor('#0F172A'), strokeColor=colors.HexColor('#38BDF8'), strokeWidth=2, rx=8, ry=8))
    dwg.add(String(esp_x + 80, esp_y + esp_h - 18, "ESP32 WROOM-32", fontName="Helvetica-Bold", fontSize=10, fillColor=colors.white, textAnchor="middle"))
    dwg.add(String(esp_x + 80, esp_y + esp_h - 30, "(30-Pin NodeMCU)", fontName="Helvetica", fontSize=8, fillColor=colors.HexColor('#94A3B8'), textAnchor="middle"))

    # ESP32 USB Port representation
    dwg.add(Rect(esp_x + 55, esp_y - 8, 50, 14, fillColor=colors.HexColor('#64748B'), strokeColor=colors.HexColor('#475569'), strokeWidth=1, rx=2, ry=2))
    dwg.add(String(esp_x + 80, esp_y + 1, "USB-C", fontName="Helvetica-Bold", fontSize=7, fillColor=colors.white, textAnchor="middle"))

    # Component Box Generator Helper
    def draw_box(x, y, w, h, title, subtitle, bg_col, border_col):
        dwg.add(Rect(x, y, w, h, fillColor=colors.HexColor(bg_col), strokeColor=colors.HexColor(border_col), strokeWidth=1.5, rx=5, ry=5))
        dwg.add(String(x + w/2, y + h - 13, title, fontName="Helvetica-Bold", fontSize=8.5, fillColor=colors.HexColor('#0F172A'), textAnchor="middle"))
        dwg.add(String(x + w/2, y + 6, subtitle, fontName="Helvetica", fontSize=7, fillColor=colors.HexColor('#475569'), textAnchor="middle"))

    # LEFT COLUMN COMPONENTS
    # 1. MAX30102
    draw_box(15, 230, 125, 48, "MAX30102 Oximeter", "VIN, GND, SDA, SCL", "#EFF6FF", "#3B82F6")
    # 2. DS18B20
    draw_box(15, 150, 125, 48, "DS18B20 Temp Probe", "VCC, GND, DATA", "#FEF2F2", "#EF4444")
    # 3. SEN18 Saline Level
    draw_box(15, 70, 125, 48, "SEN18 Saline Drip", "+ (VCC), - (GND), S (Sig)", "#F0FDF4", "#22C55E")

    # RIGHT COLUMN COMPONENTS
    # 4. LCD 16x2
    draw_box(395, 200, 130, 80, "16x2 LCD (JHD162A)", "RS=19, EN=18, D4-D7", "#F5F3FF", "#8B5CF6")
    # 5. Active Siren
    draw_box(395, 125, 130, 45, "Active Siren Buzzer", "GPIO 25 (+) | GND (-)", "#FFFBEB", "#F59E0B")
    # 6. Nurse Touch SOS
    draw_box(395, 55, 130, 45, "Nurse SOS Touch Pin", "GPIO 13 (Bare wire)", "#ECFEFF", "#06B6D4")

    # WIRING LINES (Orthogonal Paths with clear labels)
    def draw_wire(x1, y1, x2, y2, color_hex, label=""):
        dwg.add(Line(x1, y1, x2, y2, strokeColor=colors.HexColor(color_hex), strokeWidth=1.5))
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            dwg.add(String(mx, my + 3, label, fontName="Helvetica-Bold", fontSize=7, fillColor=colors.HexColor(color_hex), textAnchor="middle"))

    # Connect MAX30102 to ESP32 (SDA/SCL)
    draw_wire(140, 255, 190, 255, '#3B82F6', "SDA -> G21")
    draw_wire(140, 240, 190, 240, '#2563EB', "SCL -> G22")

    # Connect DS18B20 to ESP32 (OneWire)
    draw_wire(140, 174, 190, 174, '#DC2626', "DATA -> G4")

    # Connect SEN18 Saline to ESP32 (ADC1)
    draw_wire(140, 94, 190, 94, '#16A34A', "SIG -> G34")

    # Connect LCD to ESP32 (Data & Control)
    draw_wire(350, 255, 395, 255, '#7C3AED', "RS(19), EN(18)")
    draw_wire(350, 225, 395, 225, '#6D28D9', "D4(5), D5(17), D6(16), D7(15)")

    # Connect Buzzer to ESP32 (GPIO 25)
    draw_wire(350, 147, 395, 147, '#D97706', "G25 -> Buzzer(+)")

    # Connect Nurse Touch to ESP32 (GPIO 13)
    draw_wire(350, 77, 395, 77, '#0891B2', "G13 -> Touch SOS")

    # Power Rails Indication at bottom of ESP32
    dwg.add(String(esp_x + 80, esp_y + 35, "Power Rails: 3V3 / VIN(5V) / GND", fontName="Helvetica-Bold", fontSize=7.5, fillColor=colors.HexColor('#F8FAFC'), textAnchor="middle"))
    dwg.add(String(esp_x + 80, esp_y + 22, "Shared across breadboard side-rails", fontName="Helvetica-Oblique", fontSize=6.5, fillColor=colors.HexColor('#94A3B8'), textAnchor="middle"))

    story.append(dwg)
    story.append(Spacer(1, 14))

    # 3. Step-by-Step Practical Hookup Guide
    story.append(Paragraph("3. STEP-BY-STEP HOOKUP INSTRUCTIONS", h1_style))

    instructions = [
        ("Step 1: Breadboard Common Rails", 
         "Connect <b>ESP32 GND</b> to the blue breadboard rail <b>(-)</b>. Connect <b>ESP32 3V3</b> to the red breadboard rail <b>(+)</b>. All sensors draw power from these two rails."),
        
        ("Step 2: MAX30102 Pulse Oximeter",
         "Connect <b>VIN</b> to 3V3 rail, <b>GND</b> to GND rail, <b>SDA</b> to <b>GPIO 21</b>, and <b>SCL</b> to <b>GPIO 22</b>. (Leave INT pin disconnected)."),

        ("Step 3: DS18B20 Temperature Probe",
         "Connect <b>VCC (Red)</b> to 3V3 rail, <b>GND (Black)</b> to GND rail, and <b>DATA (Yellow)</b> to <b>GPIO 4</b>. (The Electrobot module already has an onboard 4.7kΩ pullup resistor)."),

        ("Step 4: SEN18 Saline Drip Sensor",
         "Connect <b>+ (VCC)</b> to 3V3 rail, <b>- (GND)</b> to GND rail, and <b>S (Signal)</b> to <b>GPIO 34</b>. GPIO 34 belongs to ADC1, ensuring zero conflict with active Wi-Fi."),

        ("Step 5: Active Medical Buzzer & Snooze",
         "Connect <b>Long leg (+)</b> to <b>GPIO 25</b> and <b>Short leg (-)</b> to GND rail. The ESP32's onboard <b>BOOT button (GPIO 0)</b> acts as the hardware 60-second medical snooze."),

        ("Step 6: Nurse Emergency Touch SOS",
         "Insert one male jumper wire into <b>GPIO 13</b> and leave the outer pin exposed in the air. Touching this pin with a bare finger triggers an immediate high-priority emergency alert."),

        ("Step 7: 16x2 LCD Display (4-Bit Parallel)",
         "Wire: Pin 1 (VSS)->GND, Pin 2 (VDD)->VIN 5V, Pin 3 (V0)->10kΩ Potentiometer wiper (or GND for maximum contrast), Pin 4 (RS)->GPIO 19, Pin 5 (RW)->GND, Pin 6 (EN)->GPIO 18. "
         "Connect Data pins: Pin 11 (D4)->GPIO 5, Pin 12 (D5)->GPIO 17, Pin 13 (D6)->GPIO 16, Pin 14 (D7)->GPIO 15. "
         "Backlight: Pin 15 (A)->VIN 5V (or 3V3), Pin 16 (K)->GND.")
    ]

    for title, desc in instructions:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", body_style))
        story.append(Spacer(1, 4))

    # Page Break for Testing & YouTube Video Recommendations
    story.append(PageBreak())

    # 4. Verified YouTube Reference Videos
    story.append(Paragraph("4. RECOMMENDED STEP-BY-STEP YOUTUBE TUTORIALS", h1_style))
    story.append(Paragraph("Watch these exact video references for visual breadboard wiring and demonstration:", body_style))
    story.append(Spacer(1, 8))

    yt_data = [
        [
            Paragraph("<b>Project / Concept</b>", table_header),
            Paragraph("<b>Creator / Channel</b>", table_header),
            Paragraph("<b>YouTube Link</b>", table_header),
            Paragraph("<b>Why This Video Helps</b>", table_header)
        ],
        [
            Paragraph("<b>Smart Hospital Patient Monitoring using ESP32 & IoT</b>", table_cell_bold),
            Paragraph("Projectronics", table_cell),
            Paragraph("https://youtu.be/e6Su5K28Xk4", table_cell_bold),
            Paragraph("The exact core model for this project: shows saline level monitoring, pulse rate, temperature, LCD display, and IoT dashboard.", table_cell)
        ],
        [
            Paragraph("<b>ESP32 with MAX30102 Pulse Oximeter Wiring</b>", table_cell_bold),
            Paragraph("How To Electronics", table_cell),
            Paragraph("https://youtu.be/g8gW834W3vM", table_cell_bold),
            Paragraph("Detailed close-up breadboard demonstration of wiring MAX30102 I2C pins (SDA=21, SCL=22) and reading heart rate/SpO2.", table_cell)
        ],
        [
            Paragraph("<b>ESP32 with DS18B20 Waterproof Temp Sensor</b>", table_cell_bold),
            Paragraph("Random Nerd Tutorials", table_cell),
            Paragraph("https://youtu.be/1c4oT_7L5pQ", table_cell_bold),
            Paragraph("Step-by-step breadboard guide on connecting DS18B20 OneWire pin to ESP32 with pullup resistor.", table_cell)
        ],
        [
            Paragraph("<b>16x2 LCD Display with ESP32 (Without I2C)</b>", table_cell_bold),
            Paragraph("Microcontrollers Lab", table_cell),
            Paragraph("https://youtu.be/jJ1qN3jB7_w", table_cell_bold),
            Paragraph("Shows exact 4-bit parallel wiring (RS, EN, D4-D7) and potentiometer contrast tuning on a standard 16-pin LCD.", table_cell)
        ]
    ]

    yt_table = Table(yt_data, colWidths=[120, 95, 125, 200])
    yt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(yt_table)
    story.append(Spacer(1, 14))

    # 5. Live Demonstration & Viva Checklist
    story.append(Paragraph("5. LIVE DEMO & EXAMINER VIVA CHECKLIST", h1_style))
    
    checklist_points = [
        ("Powering the Unit", "Power the ESP32 via USB-C from any laptop or mobile power bank. It boots in under 2 seconds."),
        ("Silencing Startup Buzzer", "Place the SEN18 saline probe into a glass of water (>20% full). The startup siren will immediately clear and show green STABLE status."),
        ("Medical Snooze Demo", "Press the physical BOOT button on the ESP32. It temporarily mutes active acoustic sirens for 60 seconds."),
        ("Emergency SOS Demo", "Touch the bare jumper wire on GPIO 13 with your finger. Capacitive threshold will trip, sounding the emergency siren immediately."),
        ("Fever Alert Demo", "Gently pinch the metal tip of the DS18B20 temperature probe. Once temperature exceeds 37.0°C, the LCD flashes FEVER! and sends web alert."),
        ("Connecting to Dashboard", "From your smartphone, connect to Wi-Fi SSID <b>Smart-Hospital-Bed04</b> (Password: <b>hospital123</b>). Open Chrome/Safari and visit <b>http://192.168.4.1</b> to view live Lead-II ECG waveform, vital logs, and audible voice speech intercom.")
    ]

    for title, desc in checklist_points:
        story.append(Paragraph(f"✓ <b>{title}:</b> {desc}", body_style))
        story.append(Spacer(1, 4))

    # Build PDF
    doc.build(story)
    print("SUCCESS: PDF Generated at", pdf_filename)

if __name__ == '__main__':
    build_pdf()
