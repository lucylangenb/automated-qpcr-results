###
### Parse text input as dataframes
###

import pandas as pd #file and data handling
from tkinter import filedialog
import tkinter as tk
import csv
import itertools
import sys

# helper function for tsv / text file parsing
def isblank(row):
    return all(not field.strip() for field in row)

def csv_to_df(csv_file, csv_delim, results_flag):
    
    data_bool = False
    data_cleaned = []
    results_reader = csv.reader(csv_file, delimiter = csv_delim)

    for line in results_reader:
        if isblank(line): #check for additional (blank) lines at end of file
            data_bool = False
        if data_bool == True:
            data_cleaned.append(line)
        if results_flag in line: #skip non-results info at beginning of file
            data_bool = True

    header = data_cleaned.pop(0)
    results_table = pd.DataFrame(data_cleaned, columns = header)

    return results_table

# add a line/header to the beginning of a file
def prepend(filepath, header):
    with open(filepath, 'r+') as file:
        existing = file.read()
        file.seek(0)
        file.write(header+'\n\n'+existing)




filepath = r"C:\Users\lucy\Aldatu Biosciences\Aldatu Lab - Documents\Cooperative Lab Projects\PANDAA Software\example_dataset_freetown_qs5.xlsx"


with open(filepath, 'rb') as excel_file:
    sheet_df = pd.read_excel(excel_file, sheet_name = 'Results', usecols='A:B')

print(sheet_df)


'''
machine_type = 'Mic'
fluor_names = {"VIC": "Internal Control",
                   "FAM": "LASV"
                   }
cq_cutoff = 35

def isblank(row):
    return all(not field.strip() for field in row)


def csv_to_df(csv_file, csv_delim, results_flag):
    
    data_bool = False
    data_cleaned = []
    results_reader = csv.reader(csv_file, delimiter = csv_delim)

    for line in results_reader:
        if isblank(line): #check for additional (blank) lines at end of file
            data_bool = False
        if data_bool == True:
            data_cleaned.append(line)
        if results_flag in line: #skip non-results info at beginning of file
            data_bool = True

    header = data_cleaned.pop(0)
    results_table = pd.DataFrame(data_cleaned, columns = header)

    return results_table


def summarize(df_dict):

    first_loop = True

    for fluor in df_dict:
        if first_loop == True:
            try:
                summary_table = df_dict[fluor].loc[:, ["Well Position", "Sample Name", f"{fluor} CT"]]
            except:
                tk.messagebox.showerror(message='Incorrect file selected. Please try again.')
                # close program
                raise SystemExit()
            first_loop = False
        else:
            summary_table = pd.merge(summary_table, df_dict[fluor].loc[:, ["Well Position", f"{fluor} CT"]], on="Well Position")
    
    return summary_table
    

root = tk.Tk()
root.title('Paste results data')
root.geometry('850x400')

input_label = tk.Label(root,
                       text  = 'Paste Mic results below:',
                       font = ('Arial', 10)
                       ).pack(anchor = tk.NW,
                              pady = 10,
                              padx = 10)

input_text = tk.Text(root,
                     height = 20,
                     width = 100)
input_text.pack(anchor = tk.NW,
                padx = 10)

def get_input():
    input = input_text.get(1.0, 'end-1c')
    print(input)

accept_input = tk.Button(root,
                         text = 'OK',
                         command = get_input)
accept_input.pack()








root.mainloop()
'''





