import salt, subprocess, json, importlib, sys, os

from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, SimpleDocTemplate

from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors

from reportlab.rl_config import defaultPageSize  

def pdf_styles():
    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=10,
            leading=12,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= colors.black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,         
            splitLongWords=1,
        ),
    }
    styles.update({
        'title' : ParagraphStyle(
            'title',
            parent=styles['default'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=42,
            alignment=TA_CENTER,
        ),
    })

    return styles

def get_pdf(panel, pdf_file = '/tmp/table.pdf', range_from = 0):
    if range_from: return
    pdf_contents = {
        'title' : panel['title'],
        'tables' : [],
    }

    for table in panel['tbl_source']:
        panel_table = [x for x in panel['content'] if x.get('name') == table]
        columns = []
        if panel_table:
            panel_table = panel_table[0]
            columns = panel_table['columns']
        pdf_contents['tables'].append({'table' : panel['tbl_source'][table], 'name' : table, 'columns' : columns})

    elements = contents_to_elements(pdf_contents, pdf_file)
 
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    doc.build(elements)
  

def contents_to_elements(pdf_contents, pdf_file):
    PAGE_HEIGHT=defaultPageSize[1]  
    PAGE_WIDTH=defaultPageSize[0]  

    styles = pdf_styles()

    #    elements = [pdf_contents['title']]
    table_width = PAGE_WIDTH 
    title = pdf_contents['title']
    title = Paragraph(title, styles['title'])
    elements = [title, 
            Spacer(1, 20)]
    for table in pdf_contents['tables']:
        default_columns = [{'label' : x, 'key' : x} for x in table['table'][0].keys()]
        columns = table.get('columns', default_columns)

        data = [[x['label'] for x in columns]]
        for row in table['table']:
            for x in row: 
                row[x] = str(row[x]) #TODO properly convert lists to string

            row = [Paragraph(row[i['key']], styles['default']) for i in columns]
            data.append(row)

        cols_width = table_width / len(columns)

        pdf_table = Table(data, colWidths = cols_width)
        pdf_table.setStyle(TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black), ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))

#        elements.append(Paragraph(table['name'], styles['Normal']))
        elements.append(pdf_table)
        elements.append(Spacer(1, 10))

    return elements


