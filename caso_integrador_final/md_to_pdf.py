from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import enums
import os


def parse_markdown_lines(lines, styles):
    flow = []
    list_items = []
    in_list = False

    def flush_list():
        nonlocal list_items, in_list
        if list_items:
            lf = ListFlowable([ListItem(Paragraph(it, styles['Normal'])) for it in list_items], bulletType='bullet')
            flow.append(lf)
            list_items = []
        in_list = False

    for raw in lines:
        line = raw.rstrip('\n')
        if not line.strip():
            flush_list()
            flow.append(Spacer(1, 4))
            continue

        if line.startswith('# '):
            flush_list()
            flow.append(Paragraph(line[2:].strip(), styles['MyHeading1']))
            continue
        if line.startswith('## '):
            flush_list()
            flow.append(Paragraph(line[3:].strip(), styles['MyHeading2']))
            continue
        if line.startswith('### '):
            flush_list()
            flow.append(Paragraph(line[4:].strip(), styles['MyHeading3']))
            continue

        if line.lstrip().startswith('- '):
            list_items.append(line.lstrip()[2:].strip())
            in_list = True
            continue

        # fallback paragraph
        flush_list()
        flow.append(Paragraph(line.strip(), styles['Normal']))

    flush_list()
    return flow


def md_to_pdf(md_path, pdf_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    styles = getSampleStyleSheet()
    # Use unique style names to avoid redefinition in environments that preload styles
    styles.add(ParagraphStyle(name='MyHeading1', parent=styles['Heading1'], fontSize=18, leading=22, spaceAfter=8))
    styles.add(ParagraphStyle(name='MyHeading2', parent=styles['Heading2'], fontSize=14, leading=18, spaceAfter=6))
    styles.add(ParagraphStyle(name='MyHeading3', parent=styles['Heading3'], fontSize=12, leading=14, spaceAfter=4))

    story = parse_markdown_lines(lines, styles)

    doc = SimpleDocTemplate(pdf_path, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    doc.build(story)


if __name__ == '__main__':
    base = os.path.dirname(__file__)
    md = os.path.join(base, 'INFORME_TECNICO_PROFESIONAL.md')
    out = os.path.join(base, 'INFORME_TECNICO_PROFESIONAL.pdf')
    if not os.path.exists(md):
        print('Markdown source not found:', md)
        raise SystemExit(1)
    try:
        md_to_pdf(md, out)
        size = os.path.getsize(out)
        print('PDF generado:', out)
        print('Tamaño (bytes):', size)
    except Exception as e:
        print('Error al generar PDF:', e)
        raise
