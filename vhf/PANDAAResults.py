##############################################################################################################################
### About this code
##############################################################################################################################
#
#   This script prompts the user to select a results file from a QuantStudio, Rotor-Gene, or Mic run,
#   then analyzes the data according to the user's chosen assay.
#
#   Results are saved as a csv file with the columns: Well, Sample Name, and Result.
#
#


##############################################################################################################################
### EXE PACKAGING INSTRUCTIONS
##############################################################################################################################

# pyinstaller --onefile -w --add-data="*.gif;." --icon=aldatulogo_icon.ico --version-file=version.txt PANDAAResults.py

# --add-data flag expects directory info in the format SOURCE;DESTINATION - use '.' as destination for "this directory"
# --icon adds an icon
# --version-file adds readable file properties



##############################################################################################################################
### Imports
##############################################################################################################################

import tkinter as tk #GUI handling
from PIL import Image, ImageTk #image handling - allows for rescaling of Aldatu logo in main menu
import os #filepath handling - allows for saving of results file in same directory location as user's original file is uploaded from
import sys #executable packaging

# custom dependency - holds functions that handle parsing of xls to pandas dataframes
import vhf_library as vhf


##############################################################################################################################
### User-defined values
##############################################################################################################################

cq_cutoff = 35
pos_cutoff = 30
dRn_percent_cutoff = 0.05 #if (sample dRn / max dRn) is less than this value, sample is considered No Amplification and marked negative


##############################################################################################################################
### 0. Main menu
##############################################################################################################################

# initialize root window
root = tk.Tk()
root.title('Aldatu Biosciences - qPCR Analysis')
root.geometry('500x350')

# handle events when close button is clicked
def close_program():
    root.destroy() #get rid of root window
    raise SystemExit() #close program

root.protocol('WM_DELETE_WINDOW', close_program) #when delete_window event occurs, run close_program function

# center root on user's screen
def center_window(self):
        self.update_idletasks()             #check for any changes to window size
        width = self.winfo_width()          #get root's width and height
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)  #x = half of screen width / half of window width
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')  #use previously calculated x, y as adjustments to horiz/vert window alignment on screen

center_window(root)

# make sure that, when script is packaged as exe, logo image file can be found
def get_img_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename

# change feather icon in upper corner to Aldatu logo
ico = Image.open(get_img_path('aldatulogo_icon.gif'))
ico = ImageTk.PhotoImage(ico)
root.wm_iconphoto(True, ico) #True bool here ensures that all subsequent windows also use this icon

# resize image
logo = Image.open(get_img_path('aldatulogo.gif'))
logo = logo.resize((logo.width//6, logo.height//6)) #pixels are whole numbers, so int division needed

# turn image into tk object
logo = ImageTk.PhotoImage(logo) #convert logo to tk image object
logo_label = tk.Label(root,     #tk object logo will live inside
                      image = logo
                      ).pack(side = 'top', #where to position, relative to other objects
                            fill = tk.X,   #if empty space exists in x direction, fill it with logo's background (in this case, transparent)
                            pady = 15)     #add 15 pixels above/below logo

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

# question title - assay choice
assay_type_label = tk.Label(assay_type_frame,
                                text = 'Choose assay results to analyze:',
                                font = ('Arial', 10)
                                ).pack(side = 'top',
                                    fill = tk.X,
                                    pady = 2)

# radio buttons - assay choice
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
                    value = option
                    ).pack(anchor = tk.W) #center text vertically around reference point, left-justified - "W" refers to "West"

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
                            machine_var, #initial value in drop-down
                            *machines,   #values to choose from
                            command = lambda x: machine_var.get()
                            ).pack(anchor = tk.W)


# button to continue to file selection after selections have been made
def ok_click():
    global assay, machine_type #to edit global variables within a function, need to specify that we're editing the global verisons of these variables
    assay = assay_var.get()
    machine_type = machine_var.get()
    root.destroy()

ok_button = tk.Button(root,
                    text = 'Select results file...',
                    command = ok_click)
ok_button.pack(side = 'bottom',
               pady = 30)

root.mainloop()


##############################################################################################################################
### 1. Initialization
##############################################################################################################################

fluor_names, internal_control_fluor, unique_reporters = vhf.getfluors(assay)


##############################################################################################################################
### 2. Run analysis subprocess based on machine type
##############################################################################################################################

# tkinter needs root window - but, OK to hide this window immediately
root = tk.Tk()
root.withdraw() #hides root
root.protocol('WM_DELETE_WINDOW', close_program) #when delete_window event occurs, run close_program function

if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
    summary_table, max_dRn, results_file, head = vhf.quantstudio(machine_type, fluor_names, cq_cutoff)
elif machine_type == "Rotor-Gene":
    summary_table, results_file, head = vhf.rotorgene(fluor_names, cq_cutoff)
elif machine_type == "Mic":
    summary_table, results_file, head = vhf.mic(fluor_names, cq_cutoff)


##############################################################################################################################
### 3. Functions to get PANDAA result
##############################################################################################################################


def getPandaaResult_2fluors(row):

    if row[unique_reporters[1] + " CT"] < pos_cutoff and row[unique_reporters[1] + " dRn"]/max_dRn[unique_reporters[1]] > dRn_percent_cutoff:
        return f"{fluor_names[unique_reporters[1]]} Positive"
    
    elif row[internal_control_fluor + " CT"] < pos_cutoff:
        return "Negative"
    
    else:
        return "Invalid Result"
    

def getPandaaResult_3fluors(row):

    if row[unique_reporters[1] + " CT"] < pos_cutoff:
        if (row[unique_reporters[2] + " CT"] >= pos_cutoff):
            return f"{fluor_names[unique_reporters[1]]} Positive"
        else:
            return "Invalid Result"

    elif row[unique_reporters[2] + " CT"] < pos_cutoff:
        if (row[unique_reporters[1] + " CT"] >= pos_cutoff):
            return f"{fluor_names[unique_reporters[2]]} Positive"
        else:
            return "Invalid Result"
        
    elif row[internal_control_fluor + " CT"] < pos_cutoff:
        return "Negative"
      
    else:
        return "Invalid Result"
    

def getPandaaResult_3fluors_cqconf(row):

    if row[unique_reporters[1] + " CT"] < pos_cutoff:
        if (row[unique_reporters[2] + " CT"] >= pos_cutoff) or ((row[unique_reporters[2] + " CT"] < pos_cutoff) and (row[unique_reporters[2] + " Cq Conf"] <= 0.5)):
            return f"{fluor_names[unique_reporters[1]]} Positive"
        else:
            return "Invalid Result"

    elif row[unique_reporters[2] + " CT"] < pos_cutoff:
        if (row[unique_reporters[1] + " CT"] >= pos_cutoff) or ((row[unique_reporters[1] + " CT"] < pos_cutoff) and (row[unique_reporters[1] + " Cq Conf"] <= 0.5)):
            return f"{fluor_names[unique_reporters[2]]} Positive"
        else:
            return "Invalid Result"
        
    elif row[internal_control_fluor + " CT"] < pos_cutoff:
        return "Negative"
      
    else:
        return "Invalid Result"
    
    
##############################################################################################################################
### 4. Use PANDAA function to get new column in dataframe
##############################################################################################################################

if assay == "PANDAA Ebola + Marburg": #3 fluors
    if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
        summary_table['Result'] = summary_table.apply(getPandaaResult_3fluors_cqconf, axis=1) #axis=1 specifies to work row by row
    else:
        summary_table['Result'] = summary_table.apply(getPandaaResult_3fluors, axis=1)

else: #2 fluors
    summary_table['Result'] = summary_table.apply(getPandaaResult_2fluors, axis=1)

print(summary_table)
print(max_dRn)

csv_columns = ["Well Position",
                 "Sample Name",
                 "Result"]

# rename summary table columns since data analysis is complete
for i in range(len(unique_reporters)):
    summary_table = summary_table.rename(columns={f'{unique_reporters[i]} CT': f'{fluor_names[unique_reporters[i]]} Cq',
                                                  f'{unique_reporters[i]} dRn': f'{fluor_names[unique_reporters[i]]} dRn' 
                                                  })
    #if i != 0: #don't add internal control column to csv
    csv_columns.insert(i+2, f'{fluor_names[unique_reporters[i]]} Cq') #insert columns starting at col index 2
    csv_columns.append(f'{fluor_names[unique_reporters[i]]} dRn')
    if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
        summary_table = summary_table.rename(columns={f'{unique_reporters[i]} Cq Conf': f'{fluor_names[unique_reporters[i]]} Cq Conf'})

      
summary_filepath = os.path.splitext(results_file)[0]+" - Summary.csv"

# results file can't be created/written if the user already has it open - catch possible PermissionErrors
file_saved = False
while not file_saved:
    try:
        summary_table.to_csv(
            path_or_buf=summary_filepath,
            columns=csv_columns,
            index=False
            )
        vhf.prepend(summary_filepath, head)
        file_saved = True

    # if file couldn't be saved, let the user know
    except PermissionError:
        proceed = tk.messagebox.askretrycancel(message='Unable to write results file. Make sure results file is closed, then click Retry to try again.', icon = tk.messagebox.ERROR)
        if not proceed:
            raise SystemExit()

tk.messagebox.showinfo(title="Success", message=f"Summary results saved in:\n\n{summary_filepath}")
root.destroy()