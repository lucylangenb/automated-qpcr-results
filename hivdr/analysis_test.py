# existing imports in hivdr_library

import pandas as pd #file and data handling
from tkinter import filedialog #prompt user to select results file
import tkinter as tk #error message GUI
import csv #text file parsing
import itertools #for mic csv parsing
import os #for getting file extension

# new imports for hivdr_library
import re
import numpy as np


# helper function - combines many data frames into one summary data frame
def summarize(df_dict, machine_type = ''):

    first_loop = True

    for fluor in df_dict:

        columns = ["Well Position", "Sample Name", "Task", f"{fluor} CT", f"{fluor} Quantity"]
        if machine_type == 'QuantStudio 5' or machine_type == 'QuantStudio 3':
            columns.append(f"{fluor} Cq Conf")
        else:
            if first_loop:
                columns.append('Assigned Quantity')
        if not first_loop:
            columns = columns[:1] + columns[3:] #remove columns with indices 1 and 2

        if first_loop:
            try:
                summary_table = df_dict[fluor].loc[:, columns]
            except Exception as e:
                print(e)
                tk.messagebox.showerror(message='Incorrect file selected. Please try again.')
                # close program
                raise SystemExit()
            first_loop = False
        else:
            summary_table = pd.merge(summary_table, df_dict[fluor].loc[:, columns], on="Well Position")
    
    return summary_table


# helper function - determine task
def task(row):
    if re.fullmatch(r"C\d[A-B]", row['Sample Name']):
        return 'Standard'
    else:
        return 'Unknown'
    


# helper function - get standard curve using least squares
def linreg(df, fluor='CY5'):
    data = df.loc[df['Assigned Quantity'].notnull(), #only rows with assigned copy numbers - *not* NaN
                     ['Assigned Quantity', f'{fluor} CT']] #only columns with 'x' and 'y' data
    
    if fluor != 'CY5':
        data['Assigned Quantity'] = data['Assigned Quantity'].div(5)

    x = np.array(data['Assigned Quantity'].apply(np.log10))
    y = np.array(data[f'{fluor} CT'])

    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A,y, rcond=None)[0] #0 specifies that we only want the least squares solution, not residuals

    return m, c


# helper function - get quantity based on standard curve regression
def quantify(y, m, b):
    x = (y-b)/m
    return 10**x


##################################

machine_type = 'Mic'
cq_cutoff = 35

##################################
if machine_type == 'QuantStudio 5':

    fluor_names = {"CY5": "VQ",  
                    "FAM": "076V",              
                    "NED": "184VI"               
                    }

    results_filepath = r"C:\Users\lucy\Aldatu Biosciences\Aldatu Lab - Documents\Cooperative Lab Projects\PANDAA Software\HIVDR\2024-11-12 - 076 184VI - QS-PHIVDR001 PANDAA 2 - Raw.xlsx"

    file_ext = os.path.splitext(results_filepath)[1]
    #print(file_ext)

    results_table = pd.read_excel(results_filepath, sheet_name = "Results", skiprows = 47)
    #print(results_table.loc[:, :'Quantity'])

    results_table["CT"] = results_table["CT"].replace(to_replace = "Undetermined", value = cq_cutoff)
    results_table["Quantity"] = results_table["Quantity"].fillna(0)
    results_table["CT"] = results_table["CT"].apply(pd.to_numeric)
    results_table["Cq Conf"] = results_table["Cq Conf"].apply(pd.to_numeric)
    results_table["Quantity"] = results_table["Quantity"].apply(pd.to_numeric)
    #results_table["Test Task"] = results_table.apply(task, axis=1)
    #print(results_table.loc[:, ['Sample Name', 'Test Task']])

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
    print(summary_table)



elif machine_type == 'Mic':

    fluor_names = {"CY5": "VQ",  
                        "FAM": "84V",              
                        "NED": "82AFT"               
                        }
    results_filepath = r"C:\Users\lucy\Aldatu Biosciences\Aldatu Lab - Documents\Cooperative Lab Projects\PANDAA Software\HIVDR\2024-11-13 - 82AFT 84V - Run 1 - Raw.xlsx"
    tabs_to_use = {}
    file_ext = os.path.splitext(results_filepath)[1]


    sheetnames = pd.ExcelFile(results_filepath).sheet_names #get tabs in file
    for fluor in fluor_names:
        for tab in sheetnames: #cycle through fluorophores and tabs, assign tabs to fluorophores
            if fluor_names[fluor] in tab and "Result" in tab and "Absolute" not in tab:
                tabs_to_use[fluor] = tab
                break

    #print(tabs_to_use)
    
    info_df = pd.read_excel(results_filepath, sheet_name = "Samples"
                            ).loc[:, ['Well', 'Type', 'Standards Concentration (Copies/µL)']
                            ].rename(columns={"Well": "Well Position", 'Type': 'Task', 'Standards Concentration (Copies/µL)': 'Assigned Quantity'})

    results_dict = {}
    first_loop = True
    for fluor in fluor_names:

        row_indices_to_drop = []
        col_names = None

        results_dict[fluor] = pd.read_excel(results_filepath, sheet_name = tabs_to_use[fluor], skiprows = 32)
        
        #print(results_dict[fluor])
        for row_index in list(results_dict[fluor].index.values):
            try:
                int(results_dict[fluor].iloc[row_index, 0])
            except ValueError:
                #print(results_dict[fluor].iloc[row_index, 0])
                col_names = list(results_dict[fluor].iloc[row_index, :])
                row_indices_to_drop.append(row_index)
        if col_names is not None:
            for i in row_indices_to_drop:
                results_dict[fluor] = results_dict[fluor].drop(i)
                results_dict[fluor].columns = col_names
            results_dict[fluor].reset_index(inplace=True, drop=True)
        
        results_dict[fluor]["Cq"] = results_dict[fluor]["Cq"].fillna(cq_cutoff).apply(pd.to_numeric)
        #results_dict[fluor]["Assigned Quantity"] = results_dict[fluor]["Assigned Quantity"].fillna(0).apply(pd.to_numeric)
        results_dict[fluor]["Well"] = results_dict[fluor]["Well"].apply(pd.to_numeric)
        results_dict[fluor] = results_dict[fluor].rename(columns={"Well": "Well Position", "Cq": f"{fluor} CT"})
        
        #results_dict[fluor]["Task"] = results_dict[fluor].apply(task, axis=1)
        results_dict[fluor][f"{fluor} Quantity"] = f"{fluor} Quantity"

        results_dict[fluor] = pd.merge(results_dict[fluor], info_df, on='Well Position')

        if fluor == 'CY5':
            m, b = linreg(results_dict[fluor])
            results_dict[fluor][f"{fluor} Quantity"] = results_dict[fluor][f"{fluor} CT"].apply(quantify, args=(m, b))


    summary_table = summarize(results_dict)
    print(summary_table)
    #print(summary_table.loc[summary_table['Assigned Quantity'].notnull()])
    #print(linreg(summary_table))

    
