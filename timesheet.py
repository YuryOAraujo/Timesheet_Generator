import streamlit as st
import json
import calendar
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
import io
import zipfile

# Function to create the PDF in memory (using BytesIO)
def create_pdf(employee, selected_month, selected_year, timesheet_data):
    buffer = io.BytesIO()
    
    doc_metadata = {
        'title': f"Folha de Ponto - {employee['name']}",
        'author': timesheet_data["organization"]["supervisor"],
        'subject': 'Relatório de Ponto de Funcionário',
        'keywords': 'folha de ponto, funcionário, relatório, trabalho'
    }
    
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                            topMargin=0.3 * inch, bottomMargin=0.3 * inch,
                            title=doc_metadata['title'],
                            author=doc_metadata['author'], 
                            subject=doc_metadata['subject'],
                            keywords=doc_metadata['keywords'])
    
    elements = []
    styles = getSampleStyleSheet()

    details_data = [
        [
            f"UF: {timesheet_data['organization']['state']}\n"
            f"Município: {timesheet_data['organization']['city']}\n"
            f"Entidade: {timesheet_data['organization']['name']}",
            
            f"\nFolha de Ponto\n"
            f"Período de referência: 01/{selected_month:02d}/{selected_year} - "
            f"{calendar.monthrange(selected_year, selected_month)[1]:02d}/{selected_month:02d}/{selected_year}"
        ],
        [f'Função: {employee["role"]}', "Cargo: Cargo Público"],
        [f'Nome do Servidor: {employee["name"]}'],
        [f'Lotação: {timesheet_data["organization"]["department"]}'],
    ]

    details_table = Table(details_data, colWidths=[245, 245])  
    details_table.setStyle(TableStyle([ 
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
        ('FONTNAME', (0,2), (0,2), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('SPAN', (0,2), (-1,2)),
    ]))
    elements.append(details_table)
    elements.append(Spacer(1, 6))

    timesheet_data_table = [["Dia", "Entrada", "Saída", "Entrada", "Saída", "Assinatura"]]
    
    for day in range(1, calendar.monthrange(selected_year, selected_month)[1] + 1):
        signature = ""
        weekday = calendar.weekday(selected_year, selected_month, day)
        
        if weekday == calendar.SATURDAY:
            signature = "Fim de Semana (Sábado)"
        elif weekday == calendar.SUNDAY:
            signature = "Fim de Semana (Domingo)"
        elif day in timesheet_data["holidays"].get(calendar.month_name[selected_month].lower(), []):
            signature = f"Feriado: {calendar.month_name[selected_month]} {day}"
        
        timesheet_data_table.append([f"{day:02d}/{selected_month:02d}/{selected_year}", "", "", "", "", signature])
    
    timesheet_table = Table(timesheet_data_table, colWidths=[60, 70, 70, 70, 70, 150])  
    timesheet_table.setStyle(TableStyle([ 
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTNAME', (5,0), (5,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('SPAN', (0, -1), (-1, -1)),
        ('ALIGN', (0, -1), (-1, -1), 'LEFT'),
    ]))
    elements.append(timesheet_table)
    elements.append(Spacer(1, 12))

    centered_style = ParagraphStyle(
        name="Centered",
        fontName="Helvetica",
        fontSize=10,
        alignment=1,
        spaceBefore=12,
        spaceAfter=12,
    )

    supervisor_name = timesheet_data["organization"]["supervisor"]
    signature_line = Paragraph("____________________________________________________", centered_style)
    elements.append(signature_line)

    signature_text = f"Assinatura do Responsável: {supervisor_name}"
    signature_paragraph = Paragraph(signature_text, centered_style)
    elements.append(signature_paragraph)

    doc.build(elements)
    buffer.seek(0)
    return buffer

def main():
    months = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    st.set_page_config(
        page_title="Gerador de Folha de Ponto"
    )
    st.title('Gerador de Folha de Ponto')

    uploaded_file = st.file_uploader("Carregar arquivo JSON", type=["json"])

    if uploaded_file is not None:
        timesheet_data = json.load(uploaded_file)
        
        selected_month_name = st.selectbox("Selecione o mês", months)
        selected_month = months.index(selected_month_name) + 1
        selected_year = st.number_input("Selecione o ano", min_value=2020, max_value=2100, value=2025)

        if st.button("Gerar Folhas de Ponto"):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for employee in timesheet_data["employees"]:
                    pdf_buffer = create_pdf(employee, selected_month, selected_year, timesheet_data)
                    pdf_filename = f"{selected_year}_{selected_month:02d}_{'_'.join(employee['name'].split()).lower()}.pdf"
                    zip_file.writestr(pdf_filename, pdf_buffer.read())
            
            zip_buffer.seek(0)

            st.download_button(
                label="Baixar todos os PDFs",
                data=zip_buffer,
                file_name=f"{selected_year}_{selected_month:02d}_folhas_de_ponto.zip",
                mime="application/zip"
            )

if __name__ == "__main__":
    main()
