###
### Imports
###

from tkinter import filedialog
import tkinter as tk
import os

import xlsx_to_df

###
### User-defined values
###

cq_cutoff = 35
file_type = "Excel"
machine_type = "QuantStudio 3"
assay = "PANDAA LASV"



###
### 1. Read file/sheet as pandas dataframe
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

unique_reporters = []
for key in fluor_names:
    unique_reporters.append(key)

###
### 2. Run analysis subprocess based on machine type
###

if file_type == "Excel":
    if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
        summary_table, results_file = xlsx_to_df.quantstudio(machine_type, fluor_names, internal_control_fluor, cq_cutoff)


###
### 3. Functions to get PANDAA result
###

def getPandaaResult_2fluors(row):

    if row[unique_reporters[1] + " CT"] < 30:
        return f"{fluor_names[unique_reporters[1]]} Positive"
    
    elif row[internal_control_fluor + " CT"] < 30:
        return "Negative"
    
    else:
        return "Invalid Result"
    

def getPandaaResult_3fluors(row):

    if row[unique_reporters[1] + " CT"] < 30:
        if (row[unique_reporters[2] + " CT"] >= 30) or ((row[unique_reporters[2] + " CT"] < 30) and (row[unique_reporters[2] + " Cq Conf"] <= 0.5)):
            return f"{fluor_names[unique_reporters[1]]} Positive"
        else:
            return "Invalid Result"

    elif row[unique_reporters[2] + " CT"] < 30:
        if (row[unique_reporters[1] + " CT"] >= 30) or ((row[unique_reporters[1] + " CT"] < 30) and (row[unique_reporters[1] + " Cq Conf"] <= 0.5)):
            return f"{fluor_names[unique_reporters[2]]} Positive"
        else:
            return "Invalid Result"
        
    elif row[internal_control_fluor + " CT"] < 30:
        return "Negative"
      
    else:
        return "Invalid Result"
    
    
###
### 4. Use PANDAA function to get new column in dataframe
###

if assay == "PANDAA Ebola + Marburg": #3 fluors
    summary_table['Result'] = summary_table.apply(getPandaaResult_3fluors, axis=1)

else: #2 fluors
    summary_table['Result'] = summary_table.apply(getPandaaResult_2fluors, axis=1)

print(summary_table.loc[:, ["Well Position", "Sample Name", "Result"]])

summary_table.to_csv(path_or_buf=(os.path.splitext(results_file)[0]+"_summary.csv"), columns=["Well Position", "Sample Name", "Result"])
tk.messagebox.showinfo(title="Success", message=f"Summary results saved in: {os.path.splitext(results_file)[0]+'_summary.csv'}")

# call main window
#main_window.mainloop()


