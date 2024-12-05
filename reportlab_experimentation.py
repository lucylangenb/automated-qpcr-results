from reportlab.pdfgen import canvas
import sys

def hello(c):
    c.drawString(100,100,"Hello World")
c = canvas.Canvas("hello.pdf",
                  # args below are set to defaults
                  pagesize=(595.27,841.89), #A4
                  bottomup=1,
                  pageCompression=0,
                  verbosity=0,
                  encrypt=None
                  )
hello(c)
c.showPage()
c.save()