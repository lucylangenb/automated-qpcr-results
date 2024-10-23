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
file_type = "csv"
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
if file_type == "csv":
    try:
        results_filenames = filedialog.askopenfilenames(title = 'Choose results files', filetypes= [("CSV", ".csv")])
    except:
        tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
        # close program
        raise SystemExit()

    first_loop = True

    for filename in results_filenames:

        results_table = pd.read_csv(filename, skiprows = 27)
        results_table["Ct"] = results_table["Ct"].fillna(cq_cutoff)

        for fluor in fluor_names:
            if f"{fluor}.csv" in filename or f"{fluor_names[fluor]}.csv" in filename:
                results_table = results_table.rename(columns={"No.": "Well Position",
                                                            "Name": "Sample Name",
                                                            "Ct": f"{fluor} CT",
                                                            "Ct Comment": "Comments",
                                                            "Given Conc (copies/reaction)": "Copies"})
                if first_loop == True:
                    summary_table = results_table.loc[:, ["Well Position", "Sample Name", "Copies", "Comments", f"{fluor} CT"]]
                    first_loop = False
                    print("First iteration:")
                    print(summary_table)
                else:
                    summary_table = pd.merge(summary_table, results_table.loc[:, ["Well Position", f"{fluor} CT"]], on="Well Position")
                    print(f"Added data for {fluor}:")
                    print(summary_table)

