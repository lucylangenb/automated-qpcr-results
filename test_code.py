###
### testing tk radio button
###

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# initialize root window
root = tk.Tk()
root.title('Aldatu Biosciences - qPCR Analysis')
root.geometry('500x350')

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


# frame to hold questions
questions_frame = tk.Frame(root)
questions_frame.pack(side = 'top')

# frame to hold information about assay type choice
assay_type_frame = tk.Frame(questions_frame)
assay_type_frame.pack(side = 'left', padx = 20)

# question title
assay_type_label = tk.Label(assay_type_frame,
                            text = 'Choose assay results to analyze:',
                            font = ('Arial', 10)
                            ).pack(side = 'top',
                                   fill = tk.X,
                                   pady = 2)

# buttons
assays = ['PANDAA LASV',
          'PANDAA CCHFV',
          'PANDAA Ebola + Marburg']
assay_var = tk.StringVar()
assay_var.set(None) #initialize - forces radio buttons to be empty upon loading screen

def show_assay_choice():
    print(assay_var.get())

for option in assays:
    tk.Radiobutton(assay_type_frame,
                   text = option,
                   padx = 20,
                   variable = assay_var,
                   command = show_assay_choice,
                   value = option).pack(anchor = tk.W)

# instrument choice
machine_type_frame = tk.Frame(questions_frame)
machine_type_frame.pack(side = 'right', padx = 20)

# question title for instrument choice
machine_label = tk.Label(machine_type_frame,
                         text = 'qPCR machine used:',
                         font = ('Arial', 10)
                         ).pack(side = 'top',
                                   fill = tk.X,
                                   pady = 2)

# drop-down for instrument choice
machines = ['QuantStudio 3',
            'QuantStudio 5',
            'Rotor-Gene',
            'Mic']
machine_var = tk.StringVar(value = 'QuantStudio 5')

def show_machine_choice(option):
    print(option.get())

machine_menu = tk.OptionMenu(machine_type_frame,
                             machine_var,
                             *machines,
                             command = lambda x: show_machine_choice(machine_var)
                             ).pack(anchor = tk.W)


# button to continue to file selection after selections have been made
def ok_click():
    show_assay_choice()
    show_machine_choice(machine_var)

ok_button = tk.Button(root,
                      text = 'Select results file...',
                      command = ok_click
                      ).pack(side = 'bottom',
                             pady = 30)

root.mainloop()

# https://python-course.eu/tkinter/radio-buttons-in-tkinter.php

# https://www.pythonguis.com/tutorials/create-ui-with-tkinter-pack-layout-manager/