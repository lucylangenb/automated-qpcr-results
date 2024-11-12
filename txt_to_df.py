###
### Parse text files as dataframes
###

import pandas as pd #file and data handling
from tkinter import filedialog
import tkinter as tk
import csv
import itertools

machine_type = 'Mic'
fluor_names = {"VIC": "Internal Control",
                   "FAM": "LASV"
                   }
cq_cutoff = 35

excel_files = ["*.xlsx", "*.xls"]

def isblank(row):
    return all(not field.strip() for field in row)

results_filepath = filedialog.askopenfilename(title = 'Choose results file', filetypes = [("All Excel Files", excel_files),("Text Files", "*.csv")])

# check whether a file was selected
try:
    file_ext = results_filepath.split('.')[1]
# if user didn't select a results file, or if the file is otherwise unreadable, close the program
except:
    tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
    # close program
    raise SystemExit()

if file_ext == 'csv': #file extension check - special handling for text files
       
    # text file versions of results contain inconsistent formatting throughout file, so reading these straight to a pandas df doesn't work
    # need to work line-by-line instead to get rid of header/footer data
    with open(results_filepath, newline = '') as csvfile:
        csv_lines = csvfile.readlines()

    chunks = [list(group) for is_blank, group in itertools.groupby(csv_lines, lambda line: line.strip() == "") if not is_blank]
    results_csvs = {}

    for fluor in fluor_names:
        for i in range(len(chunks)):
            #print(chunks[i][0:2])
            title = chunks[i][0]
            if 'Start Worksheet - Analysis - Cycling' in title and 'Result' in title and (fluor in title or fluor_names[fluor] in title):
                results_csvs[fluor] = chunks[i]
                break

    first_loop = True
    for fluor in results_csvs:

        data_bool = False
        data_cleaned = []
        results_reader = csv.reader(results_csvs[fluor])

        for line in results_reader:
            if isblank(line): #check for additional (blank) lines at end of file
                data_bool = False
            if data_bool == True:
                data_cleaned.append(line)
            if 'Results' in line: #skip non-results info at beginning of file
                data_bool = True

        header = data_cleaned.pop(0)
        results_table = pd.DataFrame(data_cleaned, columns = header)
        results_table["Cq"] = results_table["Cq"].replace("", cq_cutoff)
        results_table = results_table.rename(columns={"Well": "Well Position", "Cq": f"{fluor} CT"})

        if first_loop == True:
            try:
                summary_table = results_table.loc[:, ["Well Position", "Sample Name", f"{fluor} CT"]]
            except:
                tk.messagebox.showerror(message='Incorrect file selected. Please try again.')
                # close program
                raise SystemExit()
            first_loop = False
        else:
            summary_table = pd.merge(summary_table, results_table.loc[:, ["Well Position", f"{fluor} CT"]], on="Well Position")


    print(summary_table)




