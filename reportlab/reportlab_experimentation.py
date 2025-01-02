# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# ReportLab - How-to guide / experimentation
#
# Resources:
# - https://docs.reportlab.com/reportlab/userguide/
# - https://www.reportlab.com/docs/reportlab-userguide.pdf
# - https://www.blog.pythonlibrary.org/page/9/?s=reportlab
# - https://leanpub.com/reportlab/read_sample
#
# Currently reading:
# https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


###
### 1. A Simple Step-by-Step Reportlab Tutorial
### https://www.blog.pythonlibrary.org/2010/03/08/a-simple-step-by-step-reportlab-tutorial/
###

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter #A4 is default - to change, need this import

# to use inches as units instead of pixels, can import:
from reportlab.lib.units import inch

page_width, page_height = letter

c = canvas.Canvas("hello.pdf", pagesize=letter) #in order to save pdf, need to provide filename (absolute or relative path is ok)
c.drawString(inch,              #x coord
             page_height-inch,  #y coord
             "Welcome to Reportlab!") #"draws" text, using lower left corner as origin
c.save() #save drawing to pdf