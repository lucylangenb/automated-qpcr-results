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
        for chunk in chunks:
            title = chunk[0]
            if 'Start Worksheet - Analysis - Cycling' in title and 'Result' in title and (fluor in title or fluor_names[fluor] in title):
                results_csvs[fluor] = chunk
                break

    first_loop = True
    results_dict = {}
    for fluor in results_csvs:

        results_dict[fluor] = csv_to_df(results_csvs[fluor], ',', 'Results')

        results_dict[fluor]["Cq"] = results_dict[fluor]["Cq"].replace("", cq_cutoff)
        results_dict[fluor] = results_dict[fluor].rename(columns={"Well": "Well Position", "Cq": f"{fluor} CT"})

    summary_table = summarize(results_dict)

    print(summary_table)




