###
### Functions for different machines: based on machine type, create summary results dataframe
###

import pandas as pd #file and data handling
from tkinter import filedialog
import tkinter as tk

def quantstudio(machine_type, fluor_names, internal_control_fluor, cq_cutoff):

    results_file = filedialog.askopenfilename(title = 'Choose results file', filetypes= [("Excel file","*.xlsx"),("Excel file 97-2003","*.xls")])

    # see if user successfully selected a results file
    try:
        if machine_type == "QuantStudio 5":
            results_table = pd.read_excel(results_file, sheet_name = "Results", skiprows = 47)
        elif machine_type == "QuantStudio 3":
            results_table = pd.read_excel(results_file, sheet_name = "Results", skiprows = 43)
            
    # if user didn't select a results file, or if the file is otherwise unreadable, close the program
    except:
        tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
        # close program
        raise SystemExit()
    
    ###
    ### 1. Parse data
    ###

    # print table we imported - make sure machine type selection worked
    try:
        results_table.loc[:, ["Sample Name", "Target Name", "CT", "Cq Conf"]]
    except:
        tk.messagebox.showerror(message='Unexpected machine type. Check instrument input setting.')
        # close program
        raise SystemExit()

    # assign "Undetermined" wells a CT value
    results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = cq_cutoff)
    # create new "Copies" column by parsing "Comments" column (get text before ' '), convert scientific notation to numbers
    results_table["Copies"] = results_table["Comments"].str.extract(r'(\w+)\s').apply(pd.to_numeric)
    #summary_table = results_table.loc[:, ["Well Position", "Sample Name", "Copies", "Reporter", "CT"]]


    ###
    ### 2. Analyze data, summarize in new dataframe (to preserve original dataset)
    ###

    # get names of reporters/fluorophores
    unique_reporters = sorted(list(results_table['Reporter'].unique()))

    # make sure internal control fluorophore is the first fluorophore in the list, then alphabetize rest of list
    if unique_reporters[0] != internal_control_fluor:
        unique_reporters[unique_reporters.index(internal_control_fluor)] = unique_reporters[0]
        unique_reporters[0] = internal_control_fluor
        unique_reporters[1:] = sorted(unique_reporters[1:])

    #print(unique_reporters)

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

    #print(summary_table)
    return summary_table, results_file


def rotorgene(fluor_names, cq_cutoff):
    
    results_filenames = filedialog.askopenfilenames(title = 'Choose results files', filetypes= [("CSV", ".csv")])
    first_loop = True
    used_filenames = []

    for filename in results_filenames:

        results_table = pd.read_csv(filename, skiprows = 27)
        
        try:
            results_table["Ct"] = results_table["Ct"].fillna(cq_cutoff)
        except:
            tk.messagebox.showerror(message='Incorrect files selected. Please try again.')
            # close program
            raise SystemExit()

        for fluor in fluor_names:
            if f"{fluor}.csv" in filename or f"{fluor_names[fluor]}.csv" in filename:
                used_filenames.append(filename)
                results_table = results_table.rename(columns={"No.": "Well Position",
                                                            "Name": "Sample Name",
                                                            "Ct": f"{fluor} CT",
                                                            "Ct Comment": "Comments",
                                                            "Given Conc (copies/reaction)": "Copies"})
                if first_loop == True:
                    summary_table = results_table.loc[:, ["Well Position", "Sample Name", "Copies", "Comments", f"{fluor} CT"]]
                    first_loop = False
                else:
                    summary_table = pd.merge(summary_table, results_table.loc[:, ["Well Position", f"{fluor} CT"]], on="Well Position")

    if sorted(results_filenames) != sorted(used_filenames):
        tk.messagebox.showerror(message='Incorrect files selected. Please try again.')
        # close program
        raise SystemExit()

    try:
        return summary_table, results_filenames[0]
    except:
        tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
        # close program
        raise SystemExit()