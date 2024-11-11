###
### Parse text files as dataframes
###

import pandas as pd #file and data handling
from tkinter import filedialog
import tkinter as tk

machine_type = 'QuantStudio 5'
fluor_names = {"CY5": "Internal Control",  
                "FAM": "EBOV",              
                "VIC": "MARV"               
                }
cq_cutoff = 35

results_filepath = filedialog.askopenfilename(title = 'Choose results file', filetypes= [("All Excel Files","*.xlsx"),("All Excel Files","*.xls"),("Text Files", "*.txt")])

print(results_filepath)
print(f"File extension: {results_filepath.split('.')[1]}")

if results_filepath.split('.')[1] == 'txt':
    print('Results file is a text file')
else:
    print('Results file is not a text file')