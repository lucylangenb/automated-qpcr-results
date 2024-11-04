###
### testing tk radio button
###

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# initialize root window
root = tk.Tk()
root.title('Aldatu Biosciences - qPCR Analysis')
root.geometry('600x400')

# resize image
logo = Image.open('aldatulogo.gif')
logo = logo.resize((logo.width//6, logo.height//6))

# turn image into tk object
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(root, image = logo).pack(side = 'top',
                                               fill = tk.X,
                                               pady = 15)

# window title
title_label = tk.Label(root,
                       text = 'PANDAA qPCR Results Analysis',
                       font = ('Arial', 12, 'bold')
                       ).pack(side = 'top',
                              fill = tk.X,
                              pady = 10)


# question title
assay_type_label = tk.Label(root,
                            text = 'Choose assay results to analyze:',
                            font = ('Arial', 10)
                            ).pack(side = 'top',
                                   fill = tk.X,
                                   pady = 2)

# buttons
assay_var = tk.IntVar()
assay_var.set(1) # initialize choice
assays = [('PANDAA qDx LASV', 101),
          ('PANDAA qDx CCHFV', 102),
          ('PANDAA Ebola + Marburg', 103)]

def show_assay_choice():
    print(assay_var.get())

for option, val in assays:
    tk.Radiobutton(root,
                   text = option,
                   padx = 20,
                   variable = assay_var,
                   command = show_assay_choice,
                   value = val).pack(anchor = tk.W)


root.mainloop()

# https://python-course.eu/tkinter/radio-buttons-in-tkinter.php

# https://www.pythonguis.com/tutorials/create-ui-with-tkinter-pack-layout-manager/