# eob_flow_consumer.py

import os
import time
import getpass
from datetime import datetime

from lxml import objectify
from reportlab.lib import colors, utils
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.platypus import Flowable, Indenter, Table, TableStyle


from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.units import inch, mm


class Report:
    '''
    report class
    '''
    def __init__(self, pdf_file, pagesize=letter):
        ''''''
        self.canvas = canvas.Canvas(pdf_file, pagesize=pagesize)
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
        img_filepath = r"C:\Users\lucy\OneDrive - Aldatu Biosciences\Desktop\PANDAA qPCR Results\vhf\aldatulogo_icon.gif"
        desired_width = 30

        img = utils.ImageReader(img_filepath) #ImageReader uses Pillow to get information about image, so that we can grab the image size
        img_width, img_height = img.getSize()
        aspect = img_height / float(img_width) #calculate aspect ratio based on obtained height and width information
        img = Image(img_filepath,
                width=desired_width,
                height=(desired_width * aspect)) #scale height based on aspect ratio
        #img.hAlign = 'CENTER'
        img.wrapOn(self.canvas, self.width, self.height)
        img.drawOn(self.canvas, *self.coord(20,25,mm))

        ptext = '<font size=18><b>Report</b></font>'
        p = Paragraph(ptext, self.styles['Normal'])
        p.wrapOn(self.canvas, self.width, self.height)
        p.drawOn(self.canvas, *self.coord(34, 19.5, mm))



    def create_run_info(self):
        ''''''
        ptext = '<font size=14><b>Run Information</b></font>'
        p = Paragraph(ptext, self.styles['Normal'])
        p.wrapOn(self.canvas, self.width, self.height)
        p.drawOn(self.canvas, *self.coord(20, 34, mm))

        colWidths = [72, 500]
        filepath = os.path.dirname(os.path.abspath(__file__))
        user = getpass.getuser()
        data = [[self.create_text('Name', bold=True), self.create_text('experiment name')],
                [self.create_text('File', bold=True), self.create_text(filepath)],
                [self.create_text('Signature', bold=True), self.create_text('Valid')],
                [self.create_text('Status', bold=True), self.create_text('Completed')],
                [self.create_text('Operator', bold=True), self.create_text(user)
                 ]]
        table = Table(data, colWidths=colWidths)
        table.wrapOn(self.canvas, self.width, self.height)
        table.drawOn(self.canvas, *self.coord(18, 72, mm)) #coords are for lower left corner of table


    def create_results(self):
        ''''''
        pass

    def save(self):
        ''''''
        self.canvas.save()


def main(pdf_file):
    ''''''
    results = Report(pdf_file)
    results.create_header()
    results.create_run_info()
    results.save()

if __name__ == '__main__':
    pdf_file = 'results_example.pdf'
    main(pdf_file)
