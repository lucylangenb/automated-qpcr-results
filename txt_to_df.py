###
### Parse text files as dataframes
###

import pandas as pd #file and data handling
from tkinter import filedialog
import tkinter as tk
import csv

machine_type = 'QuantStudio 5'
fluor_names = {"CY5": "Internal Control",  
                "FAM": "EBOV",              
                "VIC": "MARV"               
                }
cq_cutoff = 35

excel_files = ["*.xlsx", "*.xls"]

def isblank(row):
    return all(not field.strip() for field in row)

results_filepath = filedialog.askopenfilename(title = 'Choose results file', filetypes = [("All Excel Files", excel_files),("Text Files", "*.txt")])

print(results_filepath)
print(f"File extension: {results_filepath.split('.')[1]}")

if results_filepath.split('.')[1] == 'txt':
    print('Results file is a text file')
else:
    print('Results file is not a text file')

with open(results_filepath, newline = '') as csvfile:
    results_reader = csv.reader(csvfile, delimiter = '\t')
    data_bool = False
    data_cleaned = []
    for line in results_reader:
        if isblank(line): #check for additional lines at end of file
            data_bool = False
        if data_bool == True:
            #print(', '.join(line))
            data_cleaned.append(line)
        if '[Results]' in line: #skip non-results info at beginning of file
            data_bool = True

header = data_cleaned.pop(0)
df = pd.DataFrame(data_cleaned, columns = header)
print(df)