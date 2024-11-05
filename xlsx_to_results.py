###
### Imports
###

import tkinter as tk
from PIL import Image, ImageTk
import os

import xlsx_to_df

###
### User-defined values
###

cq_cutoff = 35
file_type = "Excel"
global assay, machine_type
machine_type = "Mic"
assay = "PANDAA LASV"

###
### 0. Main menu
###

# initialize root window
root = tk.Tk()
root.title('Aldatu Biosciences - qPCR Analysis')
root.geometry('500x350')

# destroy root if close button is clicked
root.protocol('WM_DELETE_WINDOW', root.destroy)

# center root on user's screen
def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

center_window(root)

# resize image
logo = Image.open('aldatulogo.gif')
logo = logo.resize((logo.width//6, logo.height//6))

# turn image into tk object
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(root, image = logo).pack(side = 'top',
                                                fill = tk.X,
                                                pady = 15)

# window title
title_label = tk.Label(root,
                        text = 'PANDAA qPCR Results Analysis',
                        font = ('Arial', 12, 'bold')
                        ).pack(side = 'top',
                                fill = tk.X,
                                pady = 10)


# frame to hold questions
questions_frame = tk.Frame(root)
questions_frame.pack(side = 'top')

# frame to hold information about assay type choice
assay_type_frame = tk.Frame(questions_frame)
assay_type_frame.pack(side = 'left', padx = 20)

# question title
assay_type_label = tk.Label(assay_type_frame,
                                text = 'Choose assay results to analyze:',
                                font = ('Arial', 10)
                                ).pack(side = 'top',
                                    fill = tk.X,
                                    pady = 2)

# buttons
assays = ['PANDAA LASV',
        'PANDAA CCHFV',
        'PANDAA Ebola + Marburg']
assay_var = tk.StringVar()
assay_var.set(None) #initialize - forces radio buttons to be empty upon loading screen

for option in assays:
    tk.Radiobutton(assay_type_frame,
                    text = option,
                    padx = 20,
                    variable = assay_var,
                    command = assay_var.get(),
                    value = option).pack(anchor = tk.W)

# instrument choice
machine_type_frame = tk.Frame(questions_frame)
machine_type_frame.pack(side = 'right', padx = 20)

# question title for instrument choice
machine_label = tk.Label(machine_type_frame,
                            text = 'qPCR machine used:',
                            font = ('Arial', 10)
                            ).pack(side = 'top',
                                    fill = tk.X,
                                    pady = 2)

# drop-down for instrument choice
machines = ['QuantStudio 3',
                'QuantStudio 5',
                'Rotor-Gene',
                'Mic']
machine_var = tk.StringVar(value = 'QuantStudio 5') # includes initialization

machine_menu = tk.OptionMenu(machine_type_frame,
                            machine_var,
                            *machines,
                            command = lambda x: machine_var.get()
                            ).pack(anchor = tk.W)


# button to continue to file selection after selections have been made
def ok_click():
    global assay, machine_type
    assay = assay_var.get()
    machine_type = machine_var.get()
    root.destroy()

ok_button = tk.Button(root,
                    text = 'Select results file...',
                    command = ok_click)
ok_button.pack(side = 'bottom',
               pady = 30)

root.mainloop()


###
### 1. Initialization
###

# create variables based on assay chosen
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

unique_reporters = [key for key in fluor_names]
    

###
### 2. Run analysis subprocess based on machine type
###

# tkinter needs root window - but, OK to hide this window immediately
root = tk.Tk()
root.withdraw() #hides root

if file_type == "Excel":
    if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
        summary_table, results_file = xlsx_to_df.quantstudio(machine_type, fluor_names, cq_cutoff)
    elif machine_type == "Rotor-Gene":
        summary_table, results_file = xlsx_to_df.rotorgene(fluor_names, cq_cutoff)
    elif machine_type == "Mic":
        summary_table, results_file = xlsx_to_df.mic(fluor_names, cq_cutoff)

print(summary_table)

###
### 3. Functions to get PANDAA result
###

def getPandaaResult_2fluors(row):

    if row[unique_reporters[1] + " CT"] < 30:
        return f"{fluor_names[unique_reporters[1]]} Positive"
    
    elif row[internal_control_fluor + " CT"] < 30:
        return "Negative"
    
    else:
        return "Invalid Result"
    

def getPandaaResult_3fluors(row):

    if row[unique_reporters[1] + " CT"] < 30:
        if (row[unique_reporters[2] + " CT"] >= 30):
            return f"{fluor_names[unique_reporters[1]]} Positive"
        else:
            return "Invalid Result"

    elif row[unique_reporters[2] + " CT"] < 30:
        if (row[unique_reporters[1] + " CT"] >= 30):
            return f"{fluor_names[unique_reporters[2]]} Positive"
        else:
            return "Invalid Result"
        
    elif row[internal_control_fluor + " CT"] < 30:
        return "Negative"
      
    else:
        return "Invalid Result"
    

def getPandaaResult_3fluors_cqconf(row):

    if row[unique_reporters[1] + " CT"] < 30:
        if (row[unique_reporters[2] + " CT"] >= 30) or ((row[unique_reporters[2] + " CT"] < 30) and (row[unique_reporters[2] + " Cq Conf"] <= 0.5)):
            return f"{fluor_names[unique_reporters[1]]} Positive"
        else:
            return "Invalid Result"

    elif row[unique_reporters[2] + " CT"] < 30:
        if (row[unique_reporters[1] + " CT"] >= 30) or ((row[unique_reporters[1] + " CT"] < 30) and (row[unique_reporters[1] + " Cq Conf"] <= 0.5)):
            return f"{fluor_names[unique_reporters[2]]} Positive"
        else:
            return "Invalid Result"
        
    elif row[internal_control_fluor + " CT"] < 30:
        return "Negative"
      
    else:
        return "Invalid Result"
    
    
###
### 4. Use PANDAA function to get new column in dataframe
###

if assay == "PANDAA Ebola + Marburg": #3 fluors
    if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
        summary_table['Result'] = summary_table.apply(getPandaaResult_3fluors_cqconf, axis=1)
    else:
        summary_table['Result'] = summary_table.apply(getPandaaResult_3fluors, axis=1)

else: #2 fluors
    summary_table['Result'] = summary_table.apply(getPandaaResult_2fluors, axis=1)

print(summary_table.loc[:, ["Well Position", "Sample Name", "Result"]])


# results file can't be created/written if the user already has it open - catch possible PermissionErrors
try:
    summary_table.to_csv(path_or_buf=(os.path.splitext(results_file)[0]+" - Summary.csv"), columns=["Well Position", "Sample Name", "Result"])
except PermissionError:
    tk.messagebox.showerror(message='Unable to write results file. Make sure results file is closed, then click OK to try again.')

tk.messagebox.showinfo(title="Success", message=f"Summary results saved in: {os.path.splitext(results_file)[0]+' - Summary.csv'}")

# call main window
'''
root.mainloop()
root.quit()
root.destroy()
'''


