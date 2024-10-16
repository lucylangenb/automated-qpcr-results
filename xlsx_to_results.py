###
### Imports
###

import pandas as pd #file and data handling
from tkinter import Tk, filedialog, messagebox


###
### Read file/sheet as pandas dataframe
###

results_file = filedialog.askopenfilename(title = 'Choose results file (.xlsx)', filetypes= [("Excel file","*.xlsx"),("Excel file 97-2003","*.xls")])


try:
    results_table = pd.read_excel(results_file, sheet_name = "Results", skiprows = 47)
except:
    messagebox.showerror(message='File not selected')
    # close program
    raise SystemExit()

print(results_table.loc[:, ["Sample Name", "Target Name", "CT"]])
results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = "35").apply(pd.to_numeric)
print(results_table.loc[:, ["Sample Name", "Target Name", "CT"]])