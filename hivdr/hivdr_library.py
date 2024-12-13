##############################################################################################################################
### About this code
##############################################################################################################################
#
#   This script contains functions accessed by the main 'PANDAA Results' script.
#
#   Different qPCR machines have very different results outputs;
#   because of this, files from different machines need to be handled differently.
#
#   After the user tells the program which machine they used,
#   the program uses that information to choose which algorithm to use to create a usable results dataframe (pandas).
#
#   This dataframe - identical, regardless of the qPCR machine the results file originally came from -
#   is then used by the main script to generate a results file.
#
#
#


##############################################################################################################################
### Imports
##############################################################################################################################

import pandas as pd #file and data handling
from tkinter import filedialog #prompt user to select results file
import tkinter as tk #error message GUI
import csv #text file parsing
import itertools #for mic csv parsing
import os #for getting file extension
import numpy as np #for least squares regression


##############################################################################################################################
### Initialization - get fluors based on selected assay
##############################################################################################################################

def getfluors(assay):
    # create variables based on assay chosen

    # match case would be preferable here, but I have to use Python 3.9 for Opentrons... so, we're stuck with if/elif

    ###
    ### Viral hemorrhagic fevers
    ###
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

    ###
    ### HIVDR
    ###
    elif assay == "076V 184VI":
        fluor_names = {"CY5": "VQ",  
                    "FAM": "076V",              
                    "NED": "184VI"               
                    }
        internal_control_fluor = "CY5"

    elif assay == '82AFT 84V':
        fluor_names = {"CY5": "VQ",  
                        "FAM": "84V",              
                        "NED": "82AFT"               
                        }
        internal_control_fluor = 'CY5'
    

    try:
        unique_reporters = [key for key in fluor_names]
    except:
        tk.messagebox.showerror(message='Not enough parameters selected. Please try again.')
        raise SystemExit
    
    return fluor_names, internal_control_fluor, unique_reporters


##############################################################################################################################
### Helper functions for data analysis - file to dataframe
##############################################################################################################################

# helper function for tsv / text file parsing
def isblank(row):
    return all(not field.strip() for field in row)


# helper function - cleans up csv, returns relevant data
def csv_to_df(csv_file, csv_delim, results_flag=None):
    
    data_bool = False
    header_found = False
    data_cleaned = []
    results_reader = csv.reader(csv_file, delimiter = csv_delim)

    for line in results_reader:
        if isblank(line): #check for additional (blank) lines at end of file
            data_bool = False
        if data_bool == True:
            data_cleaned.append(line)
        if results_flag:
            if results_flag in line: #skip non-results info at beginning of file
                data_bool = True
        if not results_flag: #if no results_flag is defined, look for blank line
            if isblank(line) and not header_found:
                data_bool = True
                header_found = True
            
    header = data_cleaned.pop(0)
    results_table = pd.DataFrame(data_cleaned, columns = header)

    return results_table


# helper function - combines many data frames into one summary data frame
def summarize(df_dict, machine_type = ''):

    first_loop = True

    for fluor in df_dict:

        columns = ["Well Position", "Sample Name", "Task", f"{fluor} CT", f"{fluor} Quantity"]
        if machine_type == 'QuantStudio 5' or machine_type == 'QuantStudio 3':
            columns.append(f"{fluor} Cq Conf")
        '''
        # this code snippet includes 'Assigned Quantity' for non-QS files
        else:
            if first_loop:
                columns.append('Assigned Quantity')
        '''
        if not first_loop:
            columns = columns[:1] + columns[3:] #remove columns with indices 1 and 2 - 'Sample Name' and 'Task'

        if first_loop:
            try:
                summary_table = df_dict[fluor].loc[:, columns]
            except Exception as e:
                #print(e)
                tk.messagebox.showerror(message='Incorrect file selected. Please try again.')
                # close program
                raise SystemExit()
            first_loop = False
        else:
            summary_table = pd.merge(summary_table, df_dict[fluor].loc[:, columns], on="Well Position")
    
    return summary_table


# add a line/header to the beginning of a file
# parameters: summary file filepath, header
def prepend(filepath, header):
    with open(filepath, 'r+', newline='') as file:
        existing = file.read() #save file contents to 'existing'
        file.seek(0) #move pointer back to start of file
        if isinstance(header, str): #if header is single line
            file.write(header+'\n\n'+existing)
        else:
            # header is a list - need to make writer csv object, then write list to file item by item
            writer = csv.writer(file)
            writer.writerows(header)
            file.write('\n\n'+existing)


# extract header info from csv reader object
# return header as a list / csv
# parameters: reader, flag (to begin reading lines to header), stop (to stop reading lines to header)
def extract_header(reader, flag = None, stop = None):
    
    if flag:
        headbool = False
    else:
        # if no flag is defined, start reading header from top of file
        headbool = True

    head = []

    for line in reader:
        if not stop:
            # if no stop point is defined, use blank line (isblank) as break point
            if isblank(line):
                headbool = False
        else:
            # if stop is found in current line, stop creating header
            if stop in str(line):
                headbool = False
        if flag:
            # if flag is defined, look for flag in line; start appending to header if it exists
            if flag in str(line):
                headbool = True
        if headbool == True:
            head.append(line)
    return head


# helper function - get standard curve using least squares
def linreg(df, fluor='CY5'):
    data = df.loc[df['Assigned Quantity'].notnull(), #only rows with assigned copy numbers - *not* NaN
                     ['Assigned Quantity', f'{fluor} CT']] #only columns with 'x' and 'y' data
    
    if fluor != 'CY5':
        data['Assigned Quantity'] = data['Assigned Quantity'].div(5) #controls have 20% DRMs

    x = np.array(data['Assigned Quantity'].apply(np.log10))
    y = np.array(data[f'{fluor} CT'])

    A = np.vstack([x, np.ones(len(x))]).T
    m, b = np.linalg.lstsq(A,y, rcond=None)[0] #0 specifies that we only want the least squares solution, not residuals

    return m, b


# helper function - get quantity based on standard curve regression
# in regression, y=mx+b ==
# (Cq) = m*(log10 copies) + b
def quantify(y, m, b):
    x = (y-b)/m
    return 10**x


##############################################################################################################################
### QuantStudio - file to dataframe
##############################################################################################################################

def quantstudio(machine_type, fluor_names, cq_cutoff=35):

    results_filepath = filedialog.askopenfilename(title = 'Choose results file', filetypes = [("All Excel Files","*.xlsx"),("All Excel Files","*.xls"),("Text Files", "*.txt")])

    # check whether a file was selected
    try:
        file_ext = os.path.splitext(results_filepath)[1]
    # if user didn't select a results file, or if the file is otherwise unreadable, close the program
    except:
        tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
        # close program
        raise SystemExit()

    if file_ext == '.txt': #file extension check - special handling for text files
        with open(results_filepath, newline = '') as csvfile:
            # text file versions of results contain inconsistent formatting throughout file, so reading these straight to a pandas df doesn't work
            # need to work line-by-line instead to get rid of header/footer data
            # get results df:
            results_table = csv_to_df(csvfile, '\t', '[Results]')
            # get header as list:
            csvfile.seek(0)
            sheet_reader = csv.reader(csvfile, delimiter=',')
            head = extract_header(sheet_reader, 'Experiment')

        # only need to convert data to numeric if coming from text file
        results_table["Cq Conf"] = results_table["Cq Conf"].apply(pd.to_numeric)
        results_table["Quantity"] = pd.to_numeric(results_table['Quantity'].str.replace(',', ''), errors='coerce')


    else: #file is not a text file (so it's an excel file) - excel files cannot be selected if open in another program, so check for this
        
        # get results df:
        file_selected = False
        while not file_selected:
            try:
                if machine_type == "QuantStudio 5":
                    results_table = pd.read_excel(results_filepath, sheet_name = "Results", skiprows = 47)
                elif machine_type == "QuantStudio 3":
                    results_table = pd.read_excel(results_filepath, sheet_name = "Results", skiprows = 43)
            except:
                proceed = tk.messagebox.askretrycancel(message='Incorrect file, or file is open in another program. Click Retry to analyze selected file again.', icon = tk.messagebox.ERROR)
                if not proceed:
                    raise SystemExit()
            
            if 'results_table' in locals():
                file_selected = True

        # get header as list:
        with open(results_filepath, 'rb') as excel_file:
            sheet_csv = pd.read_excel(excel_file, sheet_name = 'Results', usecols='A:B').to_csv(index=False)
            sheet_reader = csv.reader(sheet_csv.splitlines(), delimiter=',')
            head = extract_header(sheet_reader, 'Experiment')
        

    try:
        # assign "Undetermined" wells a CT value - "CT" column will only exist in correctly formatted results files, so can be used for error checking
        results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = cq_cutoff)
    except:
        tk.messagebox.showerror(message='Unexpected machine type. Check instrument input setting.')
        # close program
        raise SystemExit()
    
    # make sure CT, CqConf, Quantity columns contain number values, not strings
    results_table["CT"] = results_table["CT"].apply(pd.to_numeric)
    results_table["Quantity"] = results_table["Quantity"].fillna(0)

    # make sure file and fluor_names have the same fluorophores listed
    if sorted(list(results_table['Reporter'].unique())) != sorted(fluor_names):
        tk.messagebox.showerror(message='Fluorophores in file do not match expected fluorophores. Check assay assignment.')
        # close program
        raise SystemExit()
    
    results_dict = {}
    for fluor in fluor_names:
        
        results_dict[fluor] = results_table.loc[results_table["Reporter"] == fluor]
        try:
            results_dict[fluor] = results_dict[fluor].rename(columns={"CT": f"{fluor} CT", "Quantity": f"{fluor} Quantity", "Cq Conf": f"{fluor} Cq Conf"})
        except:
            tk.messagebox.showerror(message='Fluorophores in file do not match those entered by user. Check fluorophore assignment.')
            # close program
            raise SystemExit()

    summary_table = summarize(results_dict, machine_type)

    return summary_table, results_filepath, head


##############################################################################################################################
### Rotor-Gene - file to dataframe
##############################################################################################################################

def rotorgene(fluor_names, cq_cutoff=35):
    
    results_filepaths = filedialog.askopenfilenames(title = 'Choose results files', filetypes= [("Text Files", "*.csv")])
    first_loop = True
    used_filepaths = []

    # did the user choose enough files? (Rotor-Gene makes one file for each fluorophore)
    if len(results_filepaths) != len(fluor_names):
        tk.messagebox.showerror(message=f'Incorrect number of files. Expected {len(fluor_names)} files, but {len(results_filepaths)} were selected. Make sure files are not open in other programs.')
        # close program
        raise SystemExit()

    for filepath in results_filepaths:

        results_table = pd.read_csv(filepath, skiprows = 27)

        # see if files chosen are correct - if the file is a valid results file, it will have a column called "Ct"
        try:
            results_table["Ct"] = results_table["Ct"].fillna(cq_cutoff)
        except:
            tk.messagebox.showerror(message='Incorrect files selected. Please try again.')
            # close program
            raise SystemExit()

        # cycle through all fluors needed for selected assay, match them to names of files selected
        for fluor in fluor_names:
            if f"{fluor}.csv" in filepath or f"{fluor_names[fluor]}.csv" in filepath:
                used_filepaths.append(filepath)
                results_table = results_table.rename(columns={"No.": "Well Position",
                                                            "Name": "Sample Name",
                                                            "Ct": f"{fluor} CT",
                                                            "Ct Comment": "Comments",
                                                            "Given Conc (copies/reaction)": "Copies"})
                # first time loop is run:
                if first_loop == True:
                    # initialize summary table
                    summary_table = results_table.loc[:, ["Well Position", "Sample Name", "Copies", "Comments", f"{fluor} CT"]]
                    # and get header info
                    with open(filepath, 'r') as csv_file:        
                        sheet_reader = csv.reader(csv_file, delimiter=',')
                        head = extract_header(sheet_reader, stop='Quantitative')
                    first_loop = False
                else:
                    summary_table = pd.merge(summary_table, results_table.loc[:, ["Well Position", f"{fluor} CT"]], on="Well Position")

    # number of files was determined to be correct, but did every file get used? if not, results are incomplete
    if sorted(results_filepaths) != sorted(used_filepaths):
        tk.messagebox.showerror(message='Incorrect files selected, or file names have been edited. Please try again.')
        # close program
        raise SystemExit()

    return summary_table, os.path.commonprefix(results_filepaths), head


##############################################################################################################################
### Mic - file to dataframe
##############################################################################################################################

def mic(fluor_names, cq_cutoff=35):
        
    results_filepath = filedialog.askopenfilename(title = 'Choose results file', filetypes = [("All Excel Files","*.xlsx"),("All Excel Files","*.xls"),("Text Files", "*.csv")])
    
    tabs_to_use = {}

    # check whether a file was selected
    try:
        file_ext = os.path.splitext(results_filepath)[1]
    # if user didn't select a results file, or if the file is otherwise unreadable, close the program
    except:
        tk.messagebox.showerror(message='File not selected. Make sure file is not open in another program.')
        # close program
        raise SystemExit()
    

    if file_ext == '.csv': #file extension check - special handling for text files
        
        # text file versions of results contain inconsistent formatting throughout file, so reading these straight to a pandas df doesn't work
        # need to work line-by-line instead to get rid of header/footer data
        with open(results_filepath, newline = '') as csvfile:
            
            # make list of lines
            csv_lines = csvfile.readlines()

            # get header info while we're here
            csvfile.seek(0)
            sheet_reader = csv.reader(csvfile, delimiter=',')
            head = extract_header(sheet_reader, stop='Log')

        # create 'chunks' list: break csv into groups, separated by blank lines
        chunks = [list(group) for is_blank, group in itertools.groupby(csv_lines, lambda line: line.strip() == "") if not is_blank]
        results_csvs = {}

        for fluor in fluor_names:
            for chunk in chunks:
                title = chunk[0] #first line of chunk
                if 'Start Worksheet - Analysis - Cycling' in title and 'Result' in title and (fluor in title or fluor_names[fluor] in title):
                    results_csvs[fluor] = chunk
                    tabs_to_use[fluor] = title
                    break
                elif 'Start Worksheet - Samples' in title: #get sample info (control vs unknown, concentration if available) while we're here
                    info_csv = chunk


    else: #file is not a text file - must be Excel
        sheetnames = pd.ExcelFile(results_filepath).sheet_names #get tabs in file
        for fluor in fluor_names:
            for tab in sheetnames: #cycle through fluorophores and tabs, assign tabs to fluorophores
                if fluor_names[fluor] in tab and "Result" in tab and "Absolute" not in tab:
                    tabs_to_use[fluor] = tab
                    break
        # get header info
        with open(results_filepath, 'rb') as excel_file:
            sheet_csv = pd.read_excel(excel_file, sheet_name = 'General Information', usecols='A:B').to_csv(index=False)
            sheet_reader = csv.reader(sheet_csv.splitlines(), delimiter=',')
            head = extract_header(sheet_reader, stop='Log')

        # get sample task assignment (controls vs unknowns) and assigned copy numbers, if any
        info_df = pd.read_excel(results_filepath, sheet_name = "Samples"
                            ).loc[:, ['Well', 'Type', 'Standards Concentration (Copies/µL)']
                            ].rename(columns={"Well": "Well Position", 'Type': 'Task', 'Standards Concentration (Copies/µL)': 'Assigned Quantity'})


    # check to make sure fluorophores with assigned tabs match the list of fluors known to be in assay
    if sorted(tabs_to_use) != sorted(fluor_names):
        tk.messagebox.showerror(message='Fluorophores in file do not match expected fluorophores. Check fluorophore and assay assignment.')
        # close program
        raise SystemExit()


    # get results dataframes for each fluorophore, compile into dict    
    results_dict = {}
    first_loop = True
    for fluor in fluor_names:
        
        if file_ext == '.csv':
            results_dict[fluor] = csv_to_df(results_csvs[fluor], ',', 'Results')
            if first_loop:
                info_df = csv_to_df(info_csv, ','
                                    ).loc[:, ['Well', 'Type', 'Standards Concentration (Copies/ÂµL)']
                                    ].rename(columns={"Well": "Well Position", 'Type': 'Task', 'Standards Concentration (Copies/ÂµL)': 'Assigned Quantity'})
                info_df['Well Position'] = info_df['Well Position'].apply(pd.to_numeric)
                info_df['Assigned Quantity'] = info_df['Assigned Quantity'].apply(pd.to_numeric)
                first_loop = False
        else:
            results_dict[fluor] = pd.read_excel(results_filepath, sheet_name = tabs_to_use[fluor], skiprows = 32)

            # Mic results might not start at expected skiprow - remove any non-numerical data before results table
            row_indices_to_drop = []
            col_names = None
            for row_index in list(results_dict[fluor].index.values):
                try:
                    int(results_dict[fluor].iloc[row_index, 0]) #can we convert the value in the first column ("Well") into an integer? if not, must be text
                except ValueError:
                    col_names = list(results_dict[fluor].iloc[row_index, :]) #this must then be the header row - copy info to variable
                    row_indices_to_drop.append(row_index)
            if col_names is not None:
                for i in row_indices_to_drop:
                    results_dict[fluor] = results_dict[fluor].drop(i)    #drop any saved rows
                    results_dict[fluor].columns = col_names              #replace header
                results_dict[fluor].reset_index(inplace=True, drop=True) #fix any index numbering problems that may have occurred as result of row dropping


        results_dict[fluor]["Cq"] = results_dict[fluor]["Cq"].apply(pd.to_numeric)
        results_dict[fluor]["Cq"] = results_dict[fluor]["Cq"].fillna(cq_cutoff)
        results_dict[fluor]["Well"] = results_dict[fluor]["Well"].apply(pd.to_numeric)
        results_dict[fluor] = results_dict[fluor].rename(columns={"Well": "Well Position", "Cq": f"{fluor} CT"})

        results_dict[fluor] = pd.merge(results_dict[fluor], info_df, on='Well Position')

        # get linear regression for given fluorophore/assay, then quantify that DRM
        m, b = linreg(results_dict[fluor], fluor)
        results_dict[fluor][f"{fluor} Quantity"] = results_dict[fluor][f"{fluor} CT"].apply(quantify, args=(m, b))


    summary_table = summarize(results_dict)

    return summary_table, results_filepath, head