# eob_flow_consumer.py

import os
import time
import getpass
from datetime import datetime

import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import utils, colors
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus import Flowable, Indenter, Table, TableStyle


class Header(Flowable):
    
    def __init__(self, width=2*inch, height=0.2*inch):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.styles = getSampleStyleSheet()

    def coord(self, x, y, unit=1):
        x, y = x*unit, self.height - y*unit
        return x, y
    
    def draw(self):

        img_filepath = r"C:\Users\lucy\OneDrive - Aldatu Biosciences\Desktop\PANDAA qPCR Results\vhf\aldatulogo_icon.gif"
        desired_width = 30

        img = utils.ImageReader(img_filepath) #ImageReader uses Pillow to get information about image, so that we can grab the image size
        img_width, img_height = img.getSize()
        aspect = img_height / float(img_width) #calculate aspect ratio based on obtained height and width information
        img = Image(img_filepath,
                width=desired_width,
                height=(desired_width * aspect)) #scale height based on aspect ratio
        #img.hAlign = 'CENTER'
        img.wrapOn(self.canv, self.width, self.height)
        img.drawOn(self.canv, *self.coord(0,0,inch))

        ptext = '<font size=18><b>Report</b></font>'
        p = Paragraph(ptext, self.styles['Normal'])
        p.wrapOn(self.canv, self.width, self.height)
        p.drawOn(self.canv, *self.coord(0.55,-0.2, inch))



class Report:
    '''
    report class
    '''
    def __init__(self, pdf_file, pagesize=letter):
        ''''''
        self.doc = SimpleDocTemplate(pdf_file, pagesize=pagesize,
                                     rightMargin=0.75*inch, leftMargin=0.75*inch,
                                     topMargin=0.75*inch, bottomMargin=0.75*inch)
        self.elements = []
        self.styles = getSampleStyleSheet()
        self.width, self.height = pagesize

    def coord(self, x, y, unit=1):
        x, y = x*unit, self.height - y*unit
        return x, y
    
    def create_text(self, text, size=10, bold=False):
        """"""
        if bold:
            return Paragraph('''<font size={size}><b>
            {text}</b></font>
            '''.format(size=size, text=text),
               self.styles['Normal'])

        return Paragraph('''<font size={size}>
        {text}</font>
        '''.format(size=size, text=text),
           self.styles['Normal'])

   
    def create_header(self):
        ''''''
        header = Header()
        self.elements.append(header)
    


    def create_run_info(self):
        ''''''
        ptext = '<font size=14><b>Run Information</b></font>'
        p = Paragraph(ptext, self.styles['Normal'])
        self.elements.append(p)
        self.elements.append(Spacer(1,0.2*inch))

        filepath = os.path.dirname(os.path.abspath(__file__))
        user = getpass.getuser()
        data = [[self.create_text('Name', bold=True), self.create_text('experiment name')],
                [self.create_text('File', bold=True), self.create_text(filepath+'\\'+pdf_file)],
                [self.create_text('Signature', bold=True), self.create_text('Valid')],
                [self.create_text('Status', bold=True), self.create_text('Completed')],
                [self.create_text('Operator', bold=True), self.create_text(user)
                 ]]
        
        colWidths = [0.875*inch, 5.95*inch]
        table_style = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                  ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                  ('VALIGN',(0,0),(-1,-1),'MIDDLE')])

        table = Table(data, colWidths=colWidths)
        table.setStyle(table_style)
        table.hAlign = 'LEFT'
        self.elements.append(table)
        self.elements.append(Spacer(1, 0.3*inch))


    def create_results(self):
        ''''''
        ptext = '<font size=14><b>Samples</b></font>'
        p = Paragraph(ptext, self.styles['Normal'])
        self.elements.append(p)
        self.elements.append(Spacer(1, 0.2*inch))

        well_pos = self.create_text('Well', bold=True)
        sample = self.create_text('Sample Name', bold=True)
        result_txt = self.create_text('Result', bold=True)
        data = [[well_pos, sample, result_txt]]

        result_one = [self.create_text('A1'),
                      self.create_text('Sample 1'),
                      self.create_text('LASV Positive')]
        for item in range(50):
            data.append(result_one)

        colWidths = [0.5*inch, 3.625*inch, 2.75*inch]
        table_style = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                                  ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                  ('VALIGN',(0,0),(-1,-1),'MIDDLE')])

        table = Table(data,
                      colWidths=colWidths,
                      repeatRows=1)
        table.setStyle(table_style)
        table.hAlign = 'LEFT'
        self.elements.append(table)


    def create(self):
        ''''''
        self.create_header()
        self.create_run_info()
        self.create_results()
        self.save()


    def save(self):
        ''''''
        self.doc.build(self.elements)



if __name__ == '__main__':
    pdf_file = 'results_example.pdf'
    results = Report(pdf_file)
    results.create()
