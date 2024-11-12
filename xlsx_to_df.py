###
### Functions for different machines: based on machine type, create summary results dataframe
###

import pandas as pd #file and data handling
from tkinter import filedialog
import tkinter as tk
import csv


# helper function for tsv / text file parsing
def isblank(row):
    return all(not field.strip() for field in row)



def quantstudio(machine_type, fluor_names, cq_cutoff):

    results_file = filedialog.askopenfilename(title = 'Choose results file', filetypes = [("All Excel Files","*.xlsx"),("All Excel Files","*.xls"),("Text Files", "*.txt")])

    # check whether a file was selected
    try:
        file_ext = results_file.split('.')[1]
    # if user didn't select a results file, or if the file is otherwise unreadable, close the program
    except:
        tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
        # close program
        raise SystemExit()

    if file_ext == 'txt': #file extension check - special handling for text files
       
        # text file versions of results contain inconsistent formatting, so reading these straight to a pandas df doesn't work
        # need to work line-by-line instead to get rid of header/footer data
        with open(results_file, newline = '') as csvfile:
            results_reader = csv.reader(csvfile, delimiter = '\t') #create csvreader object to iterate through each line of text file
            data_bool = False
            data_cleaned = [] #list of lists - will be equivalent to python's handling of a csv file
            for line in results_reader:
                if isblank(line): #check for additional (blank) lines at end of file
                    data_bool = False
                if data_bool == True:
                    data_cleaned.append(line)
                if '[Results]' in line: #skip non-results info at beginning of file
                    data_bool = True

        header = data_cleaned.pop(0)
        results_table = pd.DataFrame(data_cleaned, columns = header)

        
    else: #file is not a text file (so it's an excel file) - excel files cannot be selected if open in another program, so check for this
        file_selected = False
        while file_selected == False:
            try:
                if machine_type == "QuantStudio 5":
                    results_table = pd.read_excel(results_file, sheet_name = "Results", skiprows = 47)
                elif machine_type == "QuantStudio 3":
                    results_table = pd.read_excel(results_file, sheet_name = "Results", skiprows = 43)
            except:
                tk.messagebox.showerror(message='File is open in another program. Close the file, then click OK to continue analysis.')
            
            if 'results_table' in locals():
                file_selected = True

                

    try:
        # assign "Undetermined" wells a CT value - "CT" column will only exist in correctly formatted results files, so can be used for error checking
        results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = cq_cutoff)
    except:
        tk.messagebox.showerror(message='Unexpected machine type. Check instrument input setting.')
        # close program
        raise SystemExit()
    
    # create new "Copies" column by parsing "Comments" column (get text before ' '), convert scientific notation to numbers
    # (note that this needs editing - doesn't seem to be working properly)
    results_table["Copies"] = results_table["Comments"].str.extract(r'(\w+)\s').apply(pd.to_numeric)
    # make sure CT and CqConf columns contain number values, not strings
    results_table["CT"] = results_table["CT"].apply(pd.to_numeric)
    results_table["Cq Conf"] = results_table["Cq Conf"].apply(pd.to_numeric)

    # make sure file and fluor_names have the same fluorophores listed
    if sorted(list(results_table['Reporter'].unique())) != sorted(fluor_names):
        tk.messagebox.showerror(message='Fluorophores in file do not match expected fluorophores. Check assay assignment.')
        # close program
        raise SystemExit()
    
    first_loop = True
    for fluor in fluor_names:
        
        results_newfluor = results_table.loc[results_table["Reporter"] == fluor]
        try:
            results_newfluor = results_newfluor.rename(columns={"CT": f"{fluor} CT", "Cq Conf": f"{fluor} Cq Conf"})
        except:
            tk.messagebox.showerror(message='Fluorophores in file do not match those entered by user. Check fluorophore assignment.')
            # close program
            raise SystemExit()

        if first_loop == True: #on first iteration of loop, initialize summary_table
            summary_table = results_newfluor.loc[:, ["Well Position", "Sample Name", "Copies", "Comments", f"{fluor} CT", f"{fluor} Cq Conf"]]
            first_loop = False
        else: #on subsequent iterations, just add new data to loop
            summary_table = pd.merge(summary_table, results_newfluor.loc[:, ["Well Position", f"{fluor} CT", f"{fluor} Cq Conf"]], on="Well Position")

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

def mic(fluor_names, cq_cutoff):
        
    results_filename = filedialog.askopenfilename(title = 'Choose results file', filetypes= [("Excel file","*.xlsx"),("Excel file 97-2003","*.xls")])
    
    try:
        sheetnames = pd.ExcelFile(results_filename).sheet_names
    except:
        tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
        # close program
        raise SystemExit()

    tabs_to_use = {}
    for fluor in fluor_names:
        for tab in sheetnames:
            if fluor_names[fluor] in tab and "Result" in tab and "Absolute" not in tab:
                tabs_to_use[fluor] = tab
                break

    if sorted(tabs_to_use) != sorted(fluor_names):
        tk.messagebox.showerror(message='Fluorophores in file do not match expected fluorophores. Check fluorophore and assay assignment.')
        # close program
        raise SystemExit()
    
    first_loop = True
    for fluor in fluor_names:
        
        results_table = pd.read_excel(results_filename, sheet_name = tabs_to_use[fluor], skiprows = 32)
        results_table["Cq"] = results_table["Cq"].fillna(cq_cutoff)
        results_table = results_table.rename(columns={"Well": "Well Position", "Cq": f"{fluor} CT"})

        if first_loop == True:
            try:
                summary_table = results_table.loc[:, ["Well Position", "Sample Name", f"{fluor} CT"]]
            except:
                tk.messagebox.showerror(message='Incorrect file selected. Please try again.')
                # close program
                raise SystemExit()
            first_loop = False
        else:
            summary_table = pd.merge(summary_table, results_table.loc[:, ["Well Position", f"{fluor} CT"]], on="Well Position")


    return summary_table, results_filename