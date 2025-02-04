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

class PandaaMenu:
    ''''''
    def __init__(self, window_title='Aldatu Biosciences - qPCR Analysis',
                       header_title='PANDAA qPCR Results Analysis',
                       assay_choices=['PANDAA LASV', 'PANDAA CCHFV', 'PANDAA Ebola + Marburg'],
                       machine_choices=['QuantStudio 3', 'QuantStudio 5', 'Rotor-Gene', 'Mic']):
        ''''''
        self.root = None
        self.menu_frame = None

        self.window_title = window_title
        self.header_title = header_title
        self.assay_choices = assay_choices
        self.machine_choices = machine_choices

        self.assay = None
        self.machine = None


    def center_window(self):
        '''Center window on user's screen.'''
        self.root.update_idletasks()             #check for any changes to window size
        width = self.root.winfo_width()          #get root's width and height
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)  #x = half of screen width / half of window width
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')  #use previously calculated x, y as adjustments to horiz/vert window alignment on screen


    def close_program(self):
        '''Handle events when close button is clicked on tkinter window.'''
        try:
            self.root.destroy() #get rid of root window
        except Exception as e:
            print(f"Error while closing resources: {e}")
        finally:
            raise SystemExit() #close program


    def get_image(self, filename:str, resize=None, aspect=None):
        '''Image processor: make sure that, when script is packaged as exe, logo image file can be found.'''
        path = os.path.join(sys._MEIPASS, filename) if hasattr(sys, '_MEIPASS') else filename
        img = Image.open(path)
        if resize:
            if aspect:
                img = img.resize((round(img.width*aspect),
                                  round(img.height*aspect)))
            else:
                img = img.resize(resize)
        return ImageTk.PhotoImage(img)


    def init_root(self):
        '''Initialize root tkinter window.'''

        self.root = tk.Tk()
        self.root.title(self.window_title)
        self.root.geometry('500x350')

        # when delete_window event occurs, run close_program function
        self.root.protocol('WM_DELETE_WINDOW', self.close_program)
        # center root on user's screen
        self.center_window()

        # change feather icon in upper corner to Aldatu logo
        ico = self.get_image('aldatulogo_icon.gif')
        self.root.wm_iconphoto(True, ico) #True bool here ensures that all subsequent windows also use this icon


    def add_header(self):
        '''Add header image and text to tkinter window.'''
        self.logo = self.get_image('aldatulogo.gif', resize=True, aspect=1/6)
        # tk object logo will live inside logo_label
        logo_label = tk.Label(self.root, image = self.logo
                             ).pack(side = 'top', #where to position, relative to other objects
                                    fill = tk.X,   #if empty space exists in x direction, fill it with logo's background (in this case, transparent)
                                    pady = 15)     #add 15 pixels above/below logo
        # window title
        title_label = tk.Label(self.root, text = self.header_title,
                               font = ('Arial', 12, 'bold')
                              ).pack(side = 'top',
                                     fill = tk.X,
                                     pady = 10)
        # frame to hold questions
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(side='top')
    

    def add_assay_choice(self):
        '''Add menu for the user to select an assay.'''
        # frame to hold information about assay type choice
        assay_frame = tk.Frame(self.menu_frame)
        assay_frame.pack(side='left', padx=20)

        # question title - assay choice
        assay_label = tk.Label(assay_frame,
                                text = 'Choose assay results to analyze:',
                                font = ('Arial', 10)
                                ).pack(side = 'top',
                                    fill = tk.X,
                                    pady = 2)
        
        # radio buttons - assay choice
        self.assay_var = tk.StringVar()
        self.assay_var.set(None) #initialize - forces radio buttons to be empty upon loading screen

        for option in self.assay_choices:
            tk.Radiobutton(assay_frame,
                            text = option,
                            padx = 20,
                            variable = self.assay_var,
                            command = self.assay_var.get(),
                            value = option
                            ).pack(anchor = tk.W) #center text vertically around reference point, left-justified - "W" refers to "West"
            
    
    def add_machine_choice(self):
        '''Add menu for the user to select a qPCR machine.'''
        machine_frame = tk.Frame(self.menu_frame)
        machine_frame.pack(side = 'right', padx = 20)

        # question title for instrument choice
        machine_label = tk.Label(machine_frame,
                                    text = 'qPCR machine used:',
                                    font = ('Arial', 10)
                                    ).pack(side = 'top',
                                            fill = tk.X,
                                            pady = 2)

        # drop-down for instrument choice
        self.machine_var = tk.StringVar(value = 'QuantStudio 5') # includes initialization
        machine_menu = tk.OptionMenu(machine_frame,
                                    self.machine_var, #initial value in drop-down
                                    *self.machine_choices,   #values to choose from
                                    command = lambda x: self.machine_var.get()
                                    ).pack(anchor = tk.W)


    def ok_click(self):
        self.assay = self.assay_var.get()
        self.machine = self.machine_var.get()
        self.close_program()


    def add_filebutton(self):
        '''Add button for user to proceed to file selection.'''
        ok_button = tk.Button(self.root,
                              text = 'Select results file...',
                              command = self.ok_click)
        ok_button.pack(side = 'bottom', pady = 30)


    def perform_analysis(self):
        '''After OK button is clicked, create instance of qpcrAnalyzer class to obtain and clean qPCR data.'''
        self.analyzer = vhf.qpcrAnalyzer(assay=self.assay, machine_type=self.machine)
        self.analyzer.analyze()
            
    
    def start(self):
        '''Run PandaaMenu.'''
        self.init_root()
        self.add_header()
        self.add_assay_choice()
        self.add_machine_choice()
        self.add_filebutton()
        self.root.mainloop()

        self.perform_analysis()
        
        self.root.destroy()


if __name__ == '__main__':
    app = PandaaMenu()
    app.start()
    print('{0} {1}'.format(app.assay, app.machine))


'''

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
### 3. Function to get PANDAA result
##############################################################################################################################

def get_pandaa_result(row):

    # first value - index 0 - in list corresponds to internal control
    # therefore, fill this list index with high number
    cq_vals = [98]

    # iterate through all other (non-IC) fluorophores for the row
    for i in range(1, len(unique_reporters)):
        # if a positive signal is observed (Cq below cutoff plus dRn is >5% of max on plate), add it to the list
        if machine_type == 'QuantStudio 3' or machine_type == 'QuantStudio 5':
            if (row[unique_reporters[i] + " CT"] < pos_cutoff and
                row[unique_reporters[i] + " dRn"]/max_dRn[unique_reporters[i]] > dRn_percent_cutoff
                ):
                cq_vals.append(row[unique_reporters[i] + " CT"])
            # otherwise, add another high number
            else:
                cq_vals.append(99)
        else:
            if row[unique_reporters[i] + " CT"] < pos_cutoff: #RotorGene and Mic have internal dRn cutoff handling
                cq_vals.append(row[unique_reporters[i] + " CT"])
            else:
                cq_vals.append(99)

    # find the minimum of the list of Cq values
    fluor_min = cq_vals.index(min(cq_vals))
    # if the minimum is not the artificial internal control / index-0 value, well was positive for something
    # well tested positive for whatever the lowest observed Cq value was (if more than one fluorophore present)
    if fluor_min != 0:
        return f'{fluor_names[unique_reporters[fluor_min]]} Positive'
    # otherwise, check IC amplification - was it successful? if so, this is a negative reaction
    elif row[internal_control_fluor + " CT"] < pos_cutoff:
        return "Negative"
    # nothing amplified, including IC? result invalid
    else:
        return "Invalid Result"
    

    
    
##############################################################################################################################
### 4. Use PANDAA function to get new column in dataframe
##############################################################################################################################


summary_table['Result'] = summary_table.apply(get_pandaa_result, axis=1)

csv_columns = ["Well Position",
                 "Sample Name",
                 "Result"]

# rename summary table columns since data analysis is complete
for i in range(len(unique_reporters)):
    summary_table = summary_table.rename(columns={f'{unique_reporters[i]} CT': f'{fluor_names[unique_reporters[i]]} Cq'
                                                  #f'{unique_reporters[i]} dRn': f'{fluor_names[unique_reporters[i]]} dRn' 
                                                  })
    #if i != 0: #don't add internal control column to csv
    csv_columns.insert(i+2, f'{fluor_names[unique_reporters[i]]} Cq') #insert columns starting at col index 2
    if machine_type == "QuantStudio 3" or machine_type == "QuantStudio 5":
        summary_table = summary_table.rename(columns={f'{unique_reporters[i]} Cq Conf': f'{fluor_names[unique_reporters[i]]} Cq Conf',
                                                      f'{unique_reporters[i]} dRn': f'{fluor_names[unique_reporters[i]]} dRn'
                                                      })
        #csv_columns.append(f'{fluor_names[unique_reporters[i]]} dRn')

      
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
'''