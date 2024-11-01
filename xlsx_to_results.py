###
### Imports
###

import tkinter as tk
import os

import xlsx_to_df

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

unique_reporters = [key for key in fluor_names]
    

###
### 2. Run analysis subprocess based on machine type
###

root = tk.Tk()
root.withdraw()

if file_type == "Excel":
    if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
        summary_table, results_file = xlsx_to_df.quantstudio(machine_type, fluor_names, cq_cutoff)
    elif machine_type == "Rotor-Gene":
        summary_table, results_file = xlsx_to_df.rotorgene(fluor_names, cq_cutoff)
    elif machine_type == "Mic":
        summary_table, results_file = xlsx_to_df.mic(fluor_names, cq_cutoff)

print(summary_table)

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
        if (row[unique_reporters[2] + " CT"] >= 30):
            return f"{fluor_names[unique_reporters[1]]} Positive"
        else:
            return "Invalid Result"

    elif row[unique_reporters[2] + " CT"] < 30:
        if (row[unique_reporters[1] + " CT"] >= 30):
            return f"{fluor_names[unique_reporters[2]]} Positive"
        else:
            return "Invalid Result"
        
    elif row[internal_control_fluor + " CT"] < 30:
        return "Negative"
      
    else:
        return "Invalid Result"
    

def getPandaaResult_3fluors_cqconf(row):

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
    if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
        summary_table['Result'] = summary_table.apply(getPandaaResult_3fluors_cqconf, axis=1)
    else:
        summary_table['Result'] = summary_table.apply(getPandaaResult_3fluors, axis=1)

else: #2 fluors
    summary_table['Result'] = summary_table.apply(getPandaaResult_2fluors, axis=1)

print(summary_table.loc[:, ["Well Position", "Sample Name", "Result"]])


# results file can't be created/written if the user already has it open - catch possible PermissionErrors
try:
    summary_table.to_csv(path_or_buf=(os.path.splitext(results_file)[0]+" - Summary.csv"), columns=["Well Position", "Sample Name", "Result"])
except PermissionError:
    tk.messagebox.showerror(message='Unable to write results file. Make sure results file is closed, then click OK to try again.')

tk.messagebox.showinfo(title="Success", message=f"Summary results saved in: {os.path.splitext(results_file)[0]+' - Summary.csv'}")

# call main window
#main_window.mainloop()


