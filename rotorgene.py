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
machine_type = "QuantStudio 3"
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

unique_reporters = []
for key in fluor_names:
    unique_reporters.append(key)

results_files = filedialog.askopenfilenames(title = 'Choose results files', filetypes= [("CSV", ".csv")])
print(results_files)

'''
for i in range(len(unique_reporters)):
    # make table that only contains data for one fluorophore, then rename "CT" and "Cq Conf" columns
    results_file = filedialog.askopenfilename(title = f'Choose results file {i+1}', filetypes= [("Excel file","*.xlsx"),("Excel file 97-2003","*.xls")])
    results_table = pd.read_excel(results_file, skiprows = 27).rename(columns={"Ct": f"{unique_reporters[i]} CT"})
    # add this table's data to a new summary table
    if i == 0:
        summary_table = results_table.loc[:, ["Well Position", "Sample Name", "Copies", "Comments", f"{unique_reporters[i]} CT", f"{unique_reporters[i]} Cq Conf"]]
    else:
        summary_table = pd.merge(summary_table, results_table.loc[:, ["Well Position", f"{unique_reporters[i]} CT", f"{unique_reporters[i]} Cq Conf"]], on="Well Position")
'''
