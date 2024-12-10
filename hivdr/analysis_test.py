import pandas as pd #file and data handling
from tkinter import filedialog #prompt user to select results file
import tkinter as tk #error message GUI
import csv #text file parsing
import itertools #for mic csv parsing
import os #for getting file extension


# helper function - combines many data frames into one summary data frame
def summarize(df_dict, machine_type = ''):

    first_loop = True

    for fluor in df_dict:

        columns = ["Well Position", "Sample Name", f"{fluor} CT", f"{fluor} Quantity"]
        if machine_type == 'QuantStudio 5' or machine_type == 'QuantStudio 3':
            columns.append(f"{fluor} Cq Conf")
        if first_loop == False:
            columns.pop(1)

        if first_loop == True:
            try:
                summary_table = df_dict[fluor].loc[:, columns]
            except:
                tk.messagebox.showerror(message='Incorrect file selected. Please try again.')
                # close program
                raise SystemExit()
            first_loop = False
        else:
            summary_table = pd.merge(summary_table, df_dict[fluor].loc[:, columns], on="Well Position")
    
    return summary_table


machine_type = 'QuantStudio 5'
fluor_names = {"CY5": "VQ",  
                    "FAM": "076V",              
                    "NED": "184VI"               
                    }
cq_cutoff = 35

results_filepath = r"C:\Users\lucy\Aldatu Biosciences\Aldatu Lab - Documents\Cooperative Lab Projects\PANDAA Software\HIVDR\2024-11-12 - 076 184VI - QS-PHIVDR001 PANDAA 2 - Raw.xlsx"

file_ext = os.path.splitext(results_filepath)[1]
#print(file_ext)

results_table = pd.read_excel(results_filepath, sheet_name = "Results", skiprows = 47)
#print(results_table.loc[:, :'Quantity'])

results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = cq_cutoff)
results_table["Quantity"] = results_table["Quantity"].fillna(0)
results_table["CT"] = results_table["CT"].apply(pd.to_numeric)
results_table["Cq Conf"] = results_table["Cq Conf"].apply(pd.to_numeric)
results_table["Quantity"] = results_table["Quantity"].apply(pd.to_numeric)

results_dict = {}
for fluor in fluor_names:
    
    results_dict[fluor] = results_table.loc[results_table["Reporter"] == fluor]
    try:
        results_dict[fluor] = results_dict[fluor].rename(columns={"CT": f"{fluor} CT", "Quantity": f"{fluor} Quantity", "Cq Conf": f"{fluor} Cq Conf"})
    except:
        tk.messagebox.showerror(message='Fluorophores in file do not match those entered by user. Check fluorophore assignment.')
        # close program
        raise SystemExit()





summary_table = summarize(results_dict, machine_type)
print(summary_table)