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

    try:
        # assign "Undetermined" wells a CT value - "CT" column will only exist in correctly formatted results files, so can be used for error checking
        results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = cq_cutoff)
        # create new "Copies" column by parsing "Comments" column (get text before ' '), convert scientific notation to numbers
        # (note that this needs editing - doesn't seem to be working properly)
        results_table["Copies"] = results_table["Comments"].str.extract(r'(\w+)\s').apply(pd.to_numeric)
    except:
        tk.messagebox.showerror(message='Unexpected machine type. Check instrument input setting.')
        # close program
        raise SystemExit()
    
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

    return summary_table, results_file


def rotorgene(fluor_names, cq_cutoff):
    
    results_filenames = filedialog.askopenfilenames(title = 'Choose results files', filetypes= [("CSV", ".csv")])
    first_loop = True
    used_filenames = []

    # did the user choose enough files? (Rotor-Gene makes one file for each fluorophore)
    if len(results_filenames) != len(fluor_names):
        tk.messagebox.showerror(message=f'Incorrect number of files. Expected {len(fluor_names)} files, but {len(results_filenames)} were selected. Make sure files are not open in other programs.')
        # close program
        raise SystemExit()

    for filename in results_filenames:

        results_table = pd.read_csv(filename, skiprows = 27)

        # see if files chosen are correct - if the file is a valid results file, it will have a column called "Ct"
        try:
            results_table["Ct"] = results_table["Ct"].fillna(cq_cutoff)
        except:
            tk.messagebox.showerror(message='Incorrect files selected. Please try again.')
            # close program
            raise SystemExit()

        # cycle through all fluors needed for selected assay, match them to names of files selected
        for fluor in fluor_names:
            if f"{fluor}.csv" in filename or f"{fluor_names[fluor]}.csv" in filename:
                used_filenames.append(filename)
                results_table = results_table.rename(columns={"No.": "Well Position",
                                                            "Name": "Sample Name",
                                                            "Ct": f"{fluor} CT",
                                                            "Ct Comment": "Comments",
                                                            "Given Conc (copies/reaction)": "Copies"})
                # first time loop is run, initialize summary table
                if first_loop == True:
                    summary_table = results_table.loc[:, ["Well Position", "Sample Name", "Copies", "Comments", f"{fluor} CT"]]
                    first_loop = False
                else:
                    summary_table = pd.merge(summary_table, results_table.loc[:, ["Well Position", f"{fluor} CT"]], on="Well Position")

    # number of files was determined to be correct, but did every file get used? if not, results are incomplete
    if sorted(results_filenames) != sorted(used_filenames):
        tk.messagebox.showerror(message='Incorrect files selected, or file names have been edited. Please try again.')
        # close program
        raise SystemExit()

    return summary_table, results_filenames[0]