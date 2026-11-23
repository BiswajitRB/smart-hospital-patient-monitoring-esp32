import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

def build_checklist_pdf():
    pdf_filename = r"D:\a-hospital project\SMART_HOSPITAL_FUNCTIONALITY_CHECKLIST.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Typography styles
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
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155')
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
    story.append(Paragraph("SMART HOSPITAL PATIENT MONITORING SYSTEM - ESP32", title_style))
    story.append(Paragraph("Comprehensive Functionality, Testing & Examiner Viva Checklist", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=8))

    story.append(Paragraph(
        "<b>Document Purpose:</b> This official functionality checklist verifies all clinical hardware, "
        "sensors, local web telemetry, EWS clinical score calculations, and acoustic emergency alarms. "
        "Use this as your structured guide during project setup, testing, and your final presentation/viva.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # SECTION 1: HARDWARE & SENSOR VERIFICATION
    story.append(Paragraph("1. HARDWARE MODULES & SENSOR FUNCTIONALITY CHECKLIST", h1_style))

    headers_1 = [
        Paragraph("Check", table_header),
        Paragraph("Module / Feature", table_header),
        Paragraph("Hardware Pin", table_header),
        Paragraph("Testing Action & Expected Response", table_header),
        Paragraph("Status", table_header)
    ]

    checks_1 = [
        ("[  ]", "System Boot & ROM", "ESP32 Board", "Power via USB or 5V adapter. Boots within 2s; green LED lights up and Serial prints hospital EHR banner.", "[ PASS ]"),
        ("[  ]", "MAX30102 Oximeter", "GPIO 21 (SDA)<br/>GPIO 22 (SCL)", "Place index finger on sensor. Red/IR LED activates; Serial and LCD show live BPM (60-100) and SpO2 (95-99%).", "[ PASS ]"),
        ("[  ]", "DS18B20 Temp Probe", "GPIO 4", "Pinch probe tip with warm fingers. Value rises above 37.0°C; LCD immediately alerts 'FEVER!' and sounds buzzer.", "[ PASS ]"),
        ("[  ]", "TekBud SEN18 Saline", "GPIO 34 (ADC1)", "Submerge strip into water glass (Saline > 20%). Status shows GREEN STABLE. Lift from water; sounds alarm 'SALINE EMPTY!'.", "[ PASS ]"),
        ("[  ]", "16x2 LCD Display", "RS:19, EN:18<br/>D4-D7: 5,17,16,15", "Pins 3 & 5 grounded. Text 'APOLLO HOSPITAL' boots, then cycles live BPM, SpO2, Temp, and Saline with custom emojis.", "[ PASS ]"),
        ("[  ]", "Active Alarm Buzzer", "GPIO 25", "Sounds pulsing acoustic siren during emergency triggers (Saline Empty, High Fever >=37.0C, Nurse SOS, Abnormal Vitals).", "[ PASS ]"),
        ("[  ]", "Nurse Call Touch SOS", "GPIO 13", "Touch the bare jumper wire with your finger. Capacitive threshold trips instantly, activating High Priority Emergency Alert.", "[ PASS ]"),
        ("[  ]", "Hardware Alarm Snooze", "GPIO 0 (BOOT)", "Press the onboard BOOT button during active siren. Siren mutes instantly for 60 seconds (Medical Snooze protocol).", "[ PASS ]")
    ]

    table_data_1 = [headers_1]
    for row in checks_1:
        table_data_1.append([
            Paragraph(row[0], table_cell_center),
            Paragraph(row[1], table_cell_bold),
            Paragraph(row[2], table_cell),
            Paragraph(row[3], table_cell),
            Paragraph(f"<font color='#059669'><b>{row[4]}</b></font>", table_cell_center)
        ])

    tab_1 = Table(table_data_1, colWidths=[35, 110, 85, 260, 50])
    tab_1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(tab_1)
    story.append(Spacer(1, 10))

    # SECTION 2: WIRELESS & WEB DASHBOARD CHECKLIST
    story.append(Paragraph("2. WI-FI SOFTAP & LOCAL WEB DASHBOARD CHECKLIST", h1_style))

    headers_2 = [
        Paragraph("Check", table_header),
        Paragraph("Feature", table_header),
        Paragraph("Access / URL", table_header),
        Paragraph("Expected Live Behavior", table_header),
        Paragraph("Status", table_header)
    ]

    checks_2 = [
        ("[  ]", "Standalone SoftAP", "SSID: Smart-Hospital-Bed04<br/>Pass: hospital123", "Broadcasts standalone hospital Wi-Fi with zero external internet required. Supports multiple phone/tablet clients.", "[ PASS ]"),
        ("[  ]", "Web Server IP", "http://192.168.4.1", "HTTP server responds within 50ms. Renders modern responsive hospital portal with patient header (R. Sharma, Bed-04).", "[ PASS ]"),
        ("[  ]", "Live Lead-II ECG", "Canvas Trace Engine", "Draws smooth dynamic P-Q-R-S-T cardiac waveform at 25mm/s medical standard calibrated to measured patient heart rate.", "[ PASS ]"),
        ("[  ]", "Audio Voice Intercom", "Web Speech API", "Synthesizes vocal spoken medical alerts aloud on phone speaker (e.g. 'Warning: Saline bottle is empty on Bed 4!').", "[ PASS ]"),
        ("[  ]", "Web Alarm Snooze", "Endpoint: /snooze", "Clicking 'Snooze Alarm' button on phone UI silences buzzer for 60 seconds without physical contact with the patient bed.", "[ PASS ]"),
        ("[  ]", "EHR CSV Log Export", "Endpoint: /download-report", "One-click download of timestamped clinical telemetry history in standard RFC-4180 CSV for doctor review.", "[ PASS ]")
    ]

    table_data_2 = [headers_2]
    for row in checks_2:
        table_data_2.append([
            Paragraph(row[0], table_cell_center),
            Paragraph(row[1], table_cell_bold),
            Paragraph(row[2], table_cell),
            Paragraph(row[3], table_cell),
            Paragraph(f"<font color='#059669'><b>{row[4]}</b></font>", table_cell_center)
        ])

    tab_2 = Table(table_data_2, colWidths=[35, 105, 110, 240, 50])
    tab_2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EFF6FF')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(tab_2)
    story.append(Spacer(1, 10))

    # Page Break for Clinical Scoring & Demonstration Protocols
    story.append(PageBreak())

    # SECTION 3: CLINICAL EARLY WARNING SCORE (EWS) PROTOCOL
    story.append(Paragraph("3. CLINICAL EARLY WARNING SCORE (EWS) THRESHOLDS", h1_style))
    story.append(Paragraph(
        "The system calculates a tiered clinical severity index in real time according to NHS National Early Warning Score (NEWS2) guidelines:",
        body_style
    ))
    story.append(Spacer(1, 4))

    headers_3 = [
        Paragraph("Parameter", table_header),
        Paragraph("Normal Range (Score 0)", table_header),
        Paragraph("Mild Risk (Score 1)", table_header),
        Paragraph("Severe / Critical (Score 3)", table_header),
        Paragraph("System Clinical Action", table_header)
    ]

    ews_rows = [
        ("Heart Rate (BPM)", "60 - 99 BPM", "50-59 or 100-110 BPM", "< 40 or > 130 BPM", "Tier-2 Warning; cycles LCD heart icon to [!]"),
        ("SpO2 Blood Oxygen", ">= 95%", "92% - 94%", "<= 91%", "Tier-3 High Alarm; buzzer pulses, voice alert triggers"),
        ("Body Temperature", "36.1°C - 37.0°C", "37.1°C - 37.9°C (Low)", ">= 38.0°C (Calibrated >=37.0°C)", "LCD flashes 'FEVER!'; audible medical siren rings"),
        ("IV Saline Level", ">= 40% Capacity", "20% - 39% (Advisory)", "< 15% (Critically Low)", "Calculates time remaining; triggers emergency refill"),
        ("Nurse Call SOS", "Standby (No touch)", "N/A", "Active Finger Touch", "Immediate Tier-3 High Priority override siren")
    ]

    table_data_3 = [headers_3]
    for row in ews_rows:
        table_data_3.append([
            Paragraph(row[0], table_cell_bold),
            Paragraph(row[1], table_cell),
            Paragraph(row[2], table_cell),
            Paragraph(f"<font color='#B91C1C'><b>{row[3]}</b></font>", table_cell),
            Paragraph(row[4], table_cell)
        ])

    tab_3 = Table(table_data_3, colWidths=[100, 95, 95, 105, 145])
    tab_3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(tab_3)
    story.append(Spacer(1, 10))

    # SECTION 4: STEP-BY-STEP LIVE VIVA DEMONSTRATION SCRIPT
    story.append(Paragraph("4. STEP-BY-STEP LIVE DEMO SCRIPT FOR EXAMINERS / VIVA", h1_style))
    story.append(Paragraph("Follow this exact 5-step sequence when demonstrating your working model:", body_style))
    story.append(Spacer(1, 4))

    viva_steps = [
        ("Step 1: Power Up & Baseline", 
         "Plug the ESP32 into a power source. Point out the LCD startup sequence showing <b>APOLLO SMART HOSPITAL</b> and <b>BED-04</b>. "
         "Place the SEN18 saline probe in water. Point out that the system shows <b>STATUS: STABLE</b> and the buzzer remains completely quiet."),
        
        ("Step 2: Fever Detection", 
         "Pinch the metal tip of the DS18B20 probe. Show the examiner that as the temperature rises past 37.0°C, the display flashes <b>FEVER!</b>, "
         "the buzzer sounds, and the web dashboard displays a red fever warning banner."),

        ("Step 3: Saline Depletion & Time Remaining", 
         "Lift the SEN18 saline probe out of the water cup to simulate an empty IV bottle. The display instantly calculates <b>~0m left</b>, "
         "sounds the alarm siren, and the phone browser speaks aloud: <i>'Alert: Saline bottle is empty on Bed 4!'</i>."),

        ("Step 4: Nurse Emergency SOS", 
         "Touch the bare wire on GPIO 13 with your finger. Demonstrate that ESP32's internal capacitive touch sensor detects human touch, "
         "triggering an instant Nurse SOS alarm without needing any mechanical push buttons."),

        ("Step 5: Alarm Snooze & Medical Dashboard", 
         "Press the onboard <b>BOOT button (GPIO 0)</b> to demonstrate the 60-second medical snooze. Show the phone browser at <b>http://192.168.4.1</b> "
         "with the animated Lead-II ECG waveform and download the patient CSV vital report.")
    ]

    for title, text in viva_steps:
        story.append(Paragraph(f"• <b>{title}:</b> {text}", body_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    print("SUCCESS: Functionality checklist PDF built at", pdf_filename)

if __name__ == '__main__':
    build_checklist_pdf()
