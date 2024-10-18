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


###
### Read file/sheet as pandas dataframe
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

# print table we imported
print(results_table.loc[:, ["Sample Name", "Target Name", "CT"]])
# assign "Undetermined" wells a CT value
results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = cq_cutoff)
# create new "Copies" column by parsing "Comments" column, convert scientific notation to numbers
results_table["Copies"] = results_table["Comments"].str.extract(r'(\w+)\s').apply(pd.to_numeric)
# print new columns
print(results_table.loc[:, ["Well Position", "Sample Name", "Copies", "Reporter", "CT"]])

# call main window
main_window.mainloop()