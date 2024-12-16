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

# pyinstaller --onefile -w --add-data="*.gif;." --icon=aldatulogo_icon.ico --version-file=version.txt ReFocusAssistant.py

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
import hivdr_library as hivdr


##############################################################################################################################
### User-defined values
##############################################################################################################################

cq_cutoff = 35
pos_cutoff = 25


##############################################################################################################################
### 0. Main menu
##############################################################################################################################

# initialize root window
root = tk.Tk()
root.title('Aldatu Biosciences - ReFocus Assistant')
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
                        text = 'ReFocus Assistant',
                        font = ('Arial', 12, 'bold')
                        ).pack(side = 'top',
                                fill = tk.X,
                                pady = 10)


# frame to hold questions
questions_frame = tk.Frame(root)
questions_frame.pack(side = 'top')

# frame to hold information about assay type choice
assay_type_frame = tk.Frame(questions_frame)
assay_type_frame.pack(side = 'left', padx = 20, pady = 20)

# question title - assay choice
assay_type_label = tk.Label(assay_type_frame,
                                text = 'Analyze results for:',
                                font = ('Arial', 10)
                                ).pack(side = 'top',
                                    fill = tk.X,
                                    pady = 2)

# radio buttons - assay choice
assays = ['076V 184VI',
        '82AFT 84V']
assay_var = tk.StringVar(value = '076V 184VI')
#assay_var.set(None) #initialize - forces radio buttons to be empty upon loading screen

machine_menu = tk.OptionMenu(assay_type_frame,
                            assay_var, #initial value in drop-down
                            *assays,   #values to choose from
                            command = lambda x: assay_var.get()
                            ).pack(anchor = tk.W)

# instrument choice
machine_type_frame = tk.Frame(questions_frame)
machine_type_frame.pack(side = 'right', padx = 20, pady = 20)

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

fluor_names, internal_control_fluor, unique_reporters = hivdr.getfluors(assay)


##############################################################################################################################
### 2. Run analysis subprocess based on machine type
##############################################################################################################################

# tkinter needs root window - but, OK to hide this window immediately
root = tk.Tk()
root.withdraw() #hides root
root.protocol('WM_DELETE_WINDOW', close_program) #when delete_window event occurs, run close_program function

if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
    summary_table, results_file, head = hivdr.quantstudio(machine_type, fluor_names, cq_cutoff)
elif machine_type == "Rotor-Gene":
    summary_table, results_file, head = hivdr.rotorgene(fluor_names, cq_cutoff)
elif machine_type == "Mic":
    summary_table, results_file, head = hivdr.mic(fluor_names, cq_cutoff)


##############################################################################################################################
### 3. Functions to get PANDAA result
##############################################################################################################################

def hivdr_results(row, col_name):
    if row[col_name] < 0.05 or row[unique_reporters[0] + ' Quantity'] < 50:
        call = 'Negative'
    elif row[col_name] >= 0.1:
        call = 'Positive'
    else:
        call = 'Indeterminate'
    return call

    
##############################################################################################################################
### 4. Use PANDAA function to get new column in dataframe
##############################################################################################################################

# create additional columns with DRM percentages
summary_table = summary_table.assign(
                                    drm1_percent = lambda x: x[unique_reporters[1] + ' Quantity'] / x[unique_reporters[0] + ' Quantity'],
                                    drm2_percent = lambda x: x[unique_reporters[2] + ' Quantity'] / x[unique_reporters[0] + ' Quantity']
                                    ).fillna(0)

# using DRM percentage data, make a qualitative call
summary_table[fluor_names[unique_reporters[1]] + ' Call'] = summary_table.apply(hivdr_results, col_name='drm1_percent', axis=1)
summary_table[fluor_names[unique_reporters[2]] + ' Call'] = summary_table.apply(hivdr_results, col_name='drm2_percent', axis=1)

# get destination filepath
summary_filepath = os.path.splitext(results_file)[0]+" - Summary.csv"

# results file can't be created/written if the user already has it open - catch possible PermissionErrors
file_saved = False
while not file_saved:
    try:
        # save file to destination filepath
        summary_table.to_csv(
            path_or_buf=summary_filepath,
            columns=["Well Position", 
                    "Sample Name", 
                    #'drm1_percent', 
                    #'drm2_percent', 
                    fluor_names[unique_reporters[1]] + ' Call', 
                    fluor_names[unique_reporters[2]] + ' Call'],
            index=False
            )
        # add header info
        hivdr.prepend(summary_filepath, head)
        file_saved = True

    # if file couldn't be saved, let the user know
    except PermissionError:
        proceed = tk.messagebox.askretrycancel(message='Unable to write results file. Make sure results file is closed, then click Retry to try again.', icon = tk.messagebox.ERROR)
        if not proceed:
            raise SystemExit()
        

tk.messagebox.showinfo(title="Success", message=f"Summary results saved in:\n\n{summary_filepath}")
root.destroy()