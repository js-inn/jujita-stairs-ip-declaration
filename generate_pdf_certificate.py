import json
import hashlib
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

MANIFEST_FILE = "MANIFEST.json"
LEDGER_FILE = "wire_ledger.json"
WIPO_FILE = "wipo_token.wpo"
OUTPUT_PDF = "audit_certificate.pdf"

def calculate_sha256(filepath):
    if not os.path.exists(filepath):
        return "FILE_NOT_FOUND"
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_pdf():
    if not os.path.exists(MANIFEST_FILE) or not os.path.exists(LEDGER_FILE):
        print("Error: MANIFEST.json or wire_ledger.json missing.")
        return

    with open(MANIFEST_FILE, "r") as f:
        manifest = json.load(f)

    with open(LEDGER_FILE, "r") as f:
        ledger = json.load(f)

    # Compute WIPO Token status and digest
    wipo_exists = os.path.exists(WIPO_FILE)
    wipo_hash = calculate_sha256(WIPO_FILE) if wipo_exists else "N/A (Missing)"
    wipo_status = "VERIFIED_PRESENT" if wipo_exists else "MISSING"

    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0d1117'),
        alignment=1,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor('#57606a'),
        alignment=1,
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHead',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0969da'),
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#24292f')
    )

    mono_style = ParagraphStyle(
        'MonoText',
        parent=body_style,
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1f2328')
    )

    story = []

    # Title Banner
    story.append(Paragraph("10839477 CANADA INC.", title_style))
    story.append(Paragraph("PUBLIC PROVENANCE & ISO 20022 AUDIT CERTIFICATE", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0969da'), spaceAfter=10))

    # Entity Metadata Table
    story.append(Paragraph("Corporate Identity & Cryptographic State", section_heading))

    entity_info = [
        [Paragraph("<b>Legal Entity:</b>", body_style), Paragraph(manifest.get("entity", "N/A"), body_style),
         Paragraph("<b>Jurisdiction:</b>", body_style), Paragraph(manifest.get("jurisdiction", "N/A"), body_style)],
        [Paragraph("<b>Creator UUID:</b>", body_style), Paragraph(manifest.get("creator_uuid", "N/A"), mono_style),
         Paragraph("<b>Anchor UUID:</b>", body_style), Paragraph(manifest.get("cryptographic_anchor_uuid", "N/A"), mono_style)],
        [Paragraph("<b>Contracts:</b>", body_style), Paragraph(", ".join(manifest.get("related_contracts", [])), body_style),
         Paragraph("<b>Last Updated:</b>", body_style), Paragraph(manifest.get("last_updated", "N/A"), body_style)]
    ]

    t_entity = Table(entity_info, colWidths=[80, 190, 80, 190])
    t_entity.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f6f8fa')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d0d7de')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_entity)
    story.append(Spacer(1, 10))

    # Cryptographic Proof & WIPO Token Table
    story.append(Paragraph("Cryptographic Proofs & WIPO Anchor Verification", section_heading))

    proof_info = manifest.get("ledger_proof", {})
    proof_data = [
        [Paragraph("<b>Target File:</b>", body_style), Paragraph(proof_info.get("file", "wire_ledger.json"), body_style)],
        [Paragraph("<b>Ledger SHA-256:</b>", body_style), Paragraph(proof_info.get("sha256", "N/A"), mono_style)],
        [Paragraph("<b>WIPO Token Status:</b>", body_style), Paragraph(f"<b>{wipo_status}</b> ({WIPO_FILE})", body_style)],
        [Paragraph("<b>WIPO SHA-256:</b>", body_style), Paragraph(wipo_hash, mono_style)]
    ]

    t_proof = Table(proof_data, colWidths=[110, 430])
    t_proof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ddf4ff')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#54a3ff')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_proof)
    story.append(Spacer(1, 10))

    # Ledger Summary Table
    story.append(Paragraph("ISO 20022 Wire Ledger Entries (`wire_ledger.json`)", section_heading))

    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=body_style,
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )

    ledger_table_data = [
        [Paragraph("Reference ID", header_style),
         Paragraph("Timestamp (UTC)", header_style),
         Paragraph("Schema / Details", header_style)]
    ]

    entries = ledger if isinstance(ledger, list) else ledger.get("entries", [])

    for entry in entries[-10:]:
        ref_id = entry.get("reference_id", entry.get("id", "N/A"))
        ts = entry.get("timestamp", entry.get("created_at", "N/A"))
        details = f"{entry.get('schema', 'camt.053')} | Contract: {entry.get('contract_ref', 'N/A')}"

        ledger_table_data.append([
            Paragraph(ref_id, mono_style),
            Paragraph(str(ts), body_style),
            Paragraph(details, body_style)
        ])

    t_ledger = Table(ledger_table_data, colWidths=[130, 180, 230])
    t_ledger.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#24292f')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#d0d7de')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f6f8fa')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))

    story.append(t_ledger)
    story.append(Spacer(1, 15))

    # Footer Notice
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#d0d7de'), spaceAfter=6))
    footer_text = "Generated automatically via Termux pipeline | 10839477 Canada Inc. Sovereign Ledger Anchor | Verifiable via GitHub Pages"
    story.append(Paragraph(footer_text, subtitle_style))

    doc.build(story)
    print(f"Successfully generated audit certificate with WIPO anchor: {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_pdf()
