###
### Imports
###

import pandas as pd #file and data handling
from tkinter import filedialog
import tkinter as tk

###
### User-defined values
###

cq_cutoff = 35
file_type = "Excel"
machine_type = "QuantStudio 3/5"

fluor_names = {"CY5": "Internal Control",  
               "FAM": "EBOV",              
               "VIC": "MARV"               
            }

internal_control_fluor = "CY5"

###
### 1. Read file/sheet as pandas dataframe
###

# create root window / main window
main_window = tk.Tk()

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

# make table that only contains data for one fluorophore, then rename "CT" and "Cq Conf" columns
results_rep1 = results_table.loc[results_table["Reporter"] == unique_reporters[0]]
results_rep1 = results_rep1.rename(columns={"CT": f"{unique_reporters[0]} CT", "Cq Conf": f"{unique_reporters[0]} Cq Conf"})

results_rep2 = results_table.loc[results_table["Reporter"] == unique_reporters[1]]
results_rep2 = results_rep2.rename(columns={"CT": f"{unique_reporters[1]} CT", "Cq Conf": f"{unique_reporters[1]} Cq Conf"})

results_rep3 = results_table.loc[results_table["Reporter"] == unique_reporters[2]]
results_rep3 = results_rep3.rename(columns={"CT": f"{unique_reporters[2]} CT", "Cq Conf": f"{unique_reporters[2]} Cq Conf"})


# combine results into one dataframe
summary_table = results_rep1.loc[:, ["Well Position", "Sample Name", "Copies", "Comments", f"{unique_reporters[0]} CT", f"{unique_reporters[0]} Cq Conf"]]
summary_table = pd.merge(summary_table, results_rep2.loc[:, ["Well Position", f"{unique_reporters[1]} CT", f"{unique_reporters[1]} Cq Conf"]], on="Well Position")
summary_table = pd.merge(summary_table, results_rep3.loc[:, ["Well Position", f"{unique_reporters[2]} CT", f"{unique_reporters[2]} Cq Conf"]], on="Well Position")
print(summary_table)

# call main window
main_window.mainloop()