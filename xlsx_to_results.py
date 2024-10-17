###
### Imports
###

import pandas as pd #file and data handling
from tkinter import filedialog
import tkinter as tk


###
### Read file/sheet as pandas dataframe
###

# create root window / main window
main_window = tk.Tk()

results_file = filedialog.askopenfilename(title = 'Choose results file (.xlsx)', filetypes= [("Excel file","*.xlsx"),("Excel file 97-2003","*.xls")])


try:
    results_table = pd.read_excel(results_file, sheet_name = "Results", skiprows = 47)
except:
    tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
    # close program
    raise SystemExit()

print(results_table.loc[:, ["Sample Name", "Target Name", "CT"]])
results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = "35").apply(pd.to_numeric)
print(results_table.loc[:, ["Sample Name", "Comments", "Reporter", "CT"]])

# call main window
main_window.mainloop()