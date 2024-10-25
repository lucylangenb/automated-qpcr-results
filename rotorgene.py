###
### Imports
###

import pandas as pd
from tkinter import filedialog
import tkinter as tk

###
### User-defined values
###

cq_cutoff = 35
file_type = "Excel"
machine_type = "Mic"
assay = "PANDAA LASV"



###
### 1. Initialization
###

# create variables based on assay chosen
if assay == "PANDAA Ebola + Marburg":
    fluor_names = {"CY5": "Internal Control",  
                "FAM": "EBOV",              
                "VIC": "MARV"               
                }
    internal_control_fluor = "CY5"

elif assay == "PANDAA CCHFV":
    fluor_names = {"CY5": "Internal Control",
                   "FAM": "CCHFV"
                   }
    internal_control_fluor = "CY5"

elif assay == "PANDAA LASV":
    fluor_names = {"VIC": "Internal Control",
                   "FAM": "LASV"
                   }
    internal_control_fluor = "VIC"


    

###
### 2. Run analysis subprocess based on machine type
###
if file_type == "Excel":
    
    results_filename = filedialog.askopenfilename(title = 'Choose results file', filetypes= [("Excel file","*.xlsx"),("Excel file 97-2003","*.xls")])
    
    try:
        sheetnames = pd.ExcelFile(results_filename).sheet_names
    except:
        tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
        # close program
        raise SystemExit()

    tabs_to_use = {}
    for fluor in fluor_names:
        for tab in sheetnames:
            if fluor_names[fluor] in tab and "Result" in tab and "Absolute" not in tab:
                tabs_to_use[fluor] = tab
                break

    if sorted(tabs_to_use) != sorted(fluor_names):
        tk.messagebox.showerror(message='Fluorophores in file do not match expected fluorophores. Check fluorophore and assay assignment.')
        # close program
        raise SystemExit()
    
    first_loop = True
    for fluor in fluor_names:
        
        results_table = pd.read_excel(results_filename, sheet_name = tabs_to_use[fluor], skiprows = 32)
        results_table["Cq"] = results_table["Cq"].fillna(cq_cutoff)
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
    #return summary_table, results_filename
    


