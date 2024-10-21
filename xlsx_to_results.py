###
### Imports
###

import pandas as pd #file and data handling
from tkinter import filedialog
import tkinter as tk
import os

###
### User-defined values
###

cq_cutoff = 35
file_type = "Excel"
machine_type = "QuantStudio 3/5"
assay = "PANDAA Ebola + Marburg"



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


# create root window / main window
#main_window = tk.Tk()

# prompt user to select results file
if file_type == "Excel":
    results_file = filedialog.askopenfilename(title = 'Choose results file', filetypes= [("Excel file","*.xlsx"),("Excel file 97-2003","*.xls")])

# see if user successfully selected a results file
try:
    if machine_type == "QuantStudio 3/5":
        results_table = pd.read_excel(results_file, sheet_name = "Results", skiprows = 47)
# if user didn't select a results file, or if the file is otherwise unreadable, close the program
except:
    tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
    # close program
    raise SystemExit()


###
### 2. Parse data
###

# print table we imported
print(results_table.loc[:, ["Sample Name", "Target Name", "CT", "Cq Conf"]])
# assign "Undetermined" wells a CT value
results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = cq_cutoff)
# create new "Copies" column by parsing "Comments" column (get text before ' '), convert scientific notation to numbers
results_table["Copies"] = results_table["Comments"].str.extract(r'(\w+)\s').apply(pd.to_numeric)
#summary_table = results_table.loc[:, ["Well Position", "Sample Name", "Copies", "Reporter", "CT"]]


###
### 3. Analyze data, summarize in new dataframe (to preserve original dataset)
###

# get names of reporters/fluorophores
unique_reporters = sorted(list(results_table['Reporter'].unique()))

# make sure internal control fluorophore is the first fluorophore in the list, then alphabetize rest of list
if unique_reporters[0] != internal_control_fluor:
    unique_reporters[unique_reporters.index(internal_control_fluor)] = unique_reporters[0]
    unique_reporters[0] = internal_control_fluor
    unique_reporters[1:] = sorted(unique_reporters[1:])

print(unique_reporters)

# error handling: make sure fluorophores in file match the ones the user is expecting
for key in fluor_names:
    if key not in unique_reporters:
        tk.messagebox.showerror(message='Fluorophores in file do not match those entered by user. Check fluorophore assignment.')
        # close program
        raise SystemExit()


for i in range(len(unique_reporters)):
    # make table that only contains data for one fluorophore, then rename "CT" and "Cq Conf" columns
    results_newfluor = results_table.loc[results_table["Reporter"] == unique_reporters[i]]
    results_newfluor = results_newfluor.rename(columns={"CT": f"{unique_reporters[i]} CT", "Cq Conf": f"{unique_reporters[i]} Cq Conf"})
    # add this table's data to a new summary table
    if i == 0:
        summary_table = results_newfluor.loc[:, ["Well Position", "Sample Name", "Copies", "Comments", f"{unique_reporters[i]} CT", f"{unique_reporters[i]} Cq Conf"]]
    else:
        summary_table = pd.merge(summary_table, results_newfluor.loc[:, ["Well Position", f"{unique_reporters[i]} CT", f"{unique_reporters[i]} Cq Conf"]], on="Well Position")

print(summary_table)


###
### 4. Function to get PANDAA result
###

def getPandaaResult_3fluors(row):

    if row[internal_control_fluor + " CT"] >= 30:
        return "Inconclusive"
    
    elif row[unique_reporters[1] + " CT"] < 30:
        if (row[unique_reporters[2] + " CT"] >= 30) or ((row[unique_reporters[2] + " CT"] < 30) and (row[unique_reporters[2] + " Cq Conf"] <= 0.5)):
            return f"{fluor_names[unique_reporters[1]]} Positive"
        else:
            return "Inconclusive"

    elif row[unique_reporters[2] + " CT"] < 30:
        if (row[unique_reporters[1] + " CT"] >= 30) or ((row[unique_reporters[1] + " CT"] < 30) and (row[unique_reporters[1] + " Cq Conf"] <= 0.5)):
            return f"{fluor_names[unique_reporters[2]]} Positive"
        else:
            return "Inconclusive"
        
    else:
        return "Negative"
    
###
### 5. Use PANDAA function to get new column in dataframe
###

summary_table['Result'] = summary_table.apply(getPandaaResult_3fluors, axis=1)
print(summary_table.loc[:, ["Well Position", "Sample Name", "Result"]])

summary_table.to_csv(path_or_buf=(os.path.splitext(results_file)[0]+"_summary.csv"), columns=["Well Position", "Sample Name", "Result"])
tk.messagebox.showinfo(title="Success", message=f"Summary results saved in: {os.path.splitext(results_file)[0]+'_summary.csv'}")

# call main window
#main_window.mainloop()


