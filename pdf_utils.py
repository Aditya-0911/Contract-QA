from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from io import BytesIO
import pdfkit
from config import WKHTMLTOPDF_PATH
import tempfile

def generate_pdf_from_html(html_content):
    try:
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

        # Use a system-managed temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf_file:
            pdf_path = tmp_pdf_file.name

        pdfkit.from_string(html_content, pdf_path, configuration=config)

        # Read and return PDF as bytes
        with open(pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()

        return pdf_bytes
    except Exception as e:
        print(f"[ERROR] PDF generation failed: {e}")
        return None
    
def format_section(text: str, styles) -> list:
    """Format a section of text into reportlab paragraphs with improved styling"""
    elements = []
    
    # Custom styles
    header1_style = ParagraphStyle(
        'Header1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=16,
        spaceBefore=20,
        textColor=colors.HexColor('#1B4F72'),
        bold=True
    )
    
    header2_style = ParagraphStyle(
        'Header2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=16,
        textColor=colors.HexColor('#2874A6'),
        bold=True
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8,
        textColor=colors.HexColor('#2C3E50')
    )
    
    sections = text.split('\n')
    
    for section in sections:
        if not section.strip():
            continue
            
        if section.strip().startswith('**') and section.strip().endswith('**'):
            clean_text = section.strip('* \n')
            if 'EXECUTIVE SUMMARY' in clean_text or 'TIMELINE OF CONTRACT OBLIGATIONS' in clean_text:
                elements.append(Paragraph(clean_text, header1_style))
            else:
                elements.append(Paragraph(clean_text, header2_style))
        elif '|' in section:
            rows = [row.split('|') for row in section.split('\n')]
            rows = [[cell.strip() for cell in row if cell.strip()] for row in rows if row]
            
            if rows:
                table = Table(rows, colWidths=[100] * len(rows[0]))
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F4F6F7')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2C3E50')),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E8E8')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9F9')]),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 12))
        else:
            elements.append(Paragraph(section.strip(), normal_style))
            
    return elements


def create_pdf(content: str) -> BytesIO:
    """Create PDF document from compliance report content"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    elements = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1B4F72'),
        alignment=1
    )
    elements.append(Paragraph("Contract Compliance Analysis Report", title_style))
    elements.append(Spacer(1, 20))
    
    elements.extend(format_section(content, styles))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer