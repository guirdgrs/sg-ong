import io
from datetime import date
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def gerar_relatorio_presenca_pdf(polo: str, turma: str, data_aula: date, registros: list) -> bytes:
    """
    Gera um relatório impresso/PDF formatado com o resumo da chamada.
    Retorna os bytes do PDF gerado.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    styles = getSampleStyleSheet()

    # Título do Relatório
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#002B66'),
        spaceAfter=12
    )
    elements.append(Paragraph("<b>SG-ONG — Relatório Mensal de Assiduidade</b>", title_style))
    
    # Detalhes da Turma
    meta_text = f"<b>Polo:</b> {polo} | <b>Turma:</b> {turma} | <b>Data:</b> {data_aula.strftime('%d/%m/%Y')}"
    elements.append(Paragraph(meta_text, styles['Normal']))
    elements.append(Spacer(1, 15))

    # Tabela com Lista de Alunos
    data = [["Matrícula", "Nome do Aluno", "Status"]]
    for reg in registros:
        data.append([
            reg.get("matricula", "N/A"),
            reg.get("nome_aluno", "Aluno"),
            reg.get("status_presenca", "Sem Registro")
        ])

    table = Table(data, colWidths=[100, 300, 120])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#002B66')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes