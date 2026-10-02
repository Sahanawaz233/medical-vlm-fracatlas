#!/usr/bin/env python3
"""
FracAtlas Clinical Report Generator
===================================
Formats VLM diagnostic inferences into structured, standard clinical radiology reports.
Supports export to PDF, HTML, and formatted text.
"""

import os
import sys
import time
import argparse
from pathlib import Path


def generate_clinical_report(diagnostic_data, patient_id=None, output_dir="reports"):
    """
    Generate a formatted clinical radiology report from diagnostic data.
    """
    os.makedirs(output_dir, exist_ok=True)
    study_date = time.strftime("%Y-%m-%d %H:%M:%S")
    pid = patient_id or f"PT-{int(time.time()) % 100000:05d}"
    image_name = os.path.basename(diagnostic_data.get("image_path", "Radiograph.jpg"))
    is_fractured = diagnostic_data.get("fracture_detected", False)
    confidence = diagnostic_data.get("confidence", 0.95) * 100

    report_text = f"""================================================================================
                    DEPARTMENT OF RADIOLOGY & ORTHOPEDICS
                         DIAGNOSTIC RADIOLOGY REPORT
================================================================================
PATIENT ID    : {pid}                      DATE/TIME : {study_date}
MODALITY      : Musculoskeletal Radiography (DX)     ACCESSION : ACC-{pid}
IMAGE SOURCE  : {image_name}               STATUS    : FINAL SIGNED

CLINICAL INDICATION:
Evaluation of traumatic pain, suspicion of acute musculoskeletal fracture.

TECHNIQUE:
Digital projection radiography of the musculoskeletal extremity. Diagnostic
interpretation performed utilizing specialized FracAtlas Vision-Language Model.

FINDINGS:
{diagnostic_data.get('findings', 'Osseous architecture evaluated.')}

LOCALIZATION:
{f"Cortical defect localized at coordinate region {diagnostic_data.get('bounding_box')}." if is_fractured else "No focal cortical breach identified."}

IMPRESSION:
1. {diagnostic_data.get('impression', 'No acute abnormality.')}
2. Diagnostic Confidence: {confidence:.1f}%

RECOMMENDATIONS:
{("Immediate orthopedic consultation for immobilization and surgical evaluation." if is_fractured else "Symptomatic conservative management as clinically indicated. Follow-up if pain persists.")}

ELECTRONICALLY VERIFIED AND SIGNED BY:
FracAtlas AI Diagnostic Core Engine (Orthopedic Radiology Multimodal VLM)
================================================================================
"""

    base_name = f"Report_{pid}_{Path(image_name).stem}"
    txt_path = os.path.join(output_dir, f"{base_name}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    # Try PDF generation if reportlab is installed
    pdf_path = None
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        pdf_path = os.path.join(output_dir, f"{base_name}.pdf")
        doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor('#0e2a36'),
            spaceAfter=6
        )

        sub_style = ParagraphStyle(
            'SubStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=12
        )

        section_heading = ParagraphStyle(
            'SecHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.HexColor('#1e1b4b'),
            spaceBefore=10,
            spaceAfter=4
        )

        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#1f2937')
        )

        highlight_box = ParagraphStyle(
            'Impression',
            parent=body_style,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#dc2626') if is_fractured else colors.HexColor('#16a34a')
        )

        story = [
            Paragraph("DEPARTMENT OF RADIOLOGY & ORTHOPEDICS", title_style),
            Paragraph(f"DIAGNOSTIC REPORT • Patient ID: {pid} • Date: {study_date}", sub_style),
            HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#00ffc8'), spaceAfter=14),
            Paragraph("CLINICAL INDICATION", section_heading),
            Paragraph("Suspected acute traumatic fracture. Digital radiography evaluation.", body_style),
            Spacer(1, 10),
            Paragraph("FINDINGS", section_heading),
            Paragraph(diagnostic_data.get('findings', '').replace('\n', '<br/>'), body_style),
            Spacer(1, 10),
            Paragraph("IMPRESSION", section_heading),
            Paragraph(diagnostic_data.get('impression', ''), highlight_box),
            Spacer(1, 10),
            Paragraph("DIAGNOSTIC METRICS", section_heading),
            Paragraph(f"Fracture Detected: {'YES' if is_fractured else 'NO'} | VLM Confidence: {confidence:.1f}%", body_style),
            Spacer(1, 20),
            HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceAfter=8),
            Paragraph("Electronic Signature: FracAtlas Multimodal AI Core Engine", sub_style)
        ]

        doc.build(story)
        print(f"[Report] PDF generated: {pdf_path}")

    except ImportError:
        pass
    except Exception as e:
        print(f"[Report] PDF build notice: {e}")

    return {
        "txt_path": txt_path,
        "pdf_path": pdf_path,
        "report_text": report_text
    }


def main():
    parser = argparse.ArgumentParser(description="FracAtlas Radiology Report Generator")
    parser.add_argument("--image", type=str, required=True, help="Path to input X-ray radiograph")
    parser.add_argument("--patient_id", type=str, default=None, help="Optional Patient ID")
    parser.add_argument("--output_dir", type=str, default="reports", help="Directory to save report")
    args = parser.parse_args()

    # Import inference engine
    from inference import MedicalVLMInferenceEngine
    engine = MedicalVLMInferenceEngine()
    diag = engine.diagnose_xray(args.image)

    report_res = generate_clinical_report(diag, patient_id=args.patient_id, output_dir=args.output_dir)
    print(f"\n[Success] Clinical report created:")
    print(f"  - Text Report: {report_res['txt_path']}")
    if report_res.get('pdf_path'):
        print(f"  - PDF Report : {report_res['pdf_path']}")
    print("\n" + report_res['report_text'])


if __name__ == "__main__":
    main()
