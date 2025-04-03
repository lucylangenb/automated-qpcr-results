##############################################################################################################################
### About this code
##############################################################################################################################
#
#   This script contains the class PandaaMenu, which is a tkinter-based GUI to handle PANDAA data analysis.
#
#


##############################################################################################################################
### Imports
##############################################################################################################################

import tkinter as tk #GUI handling
from PIL import Image, ImageTk #image handling - allows for rescaling of Aldatu logo in main menu
import os #filepath handling - allows for saving of results file in same directory location as user's original file is uploaded from
import sys #finds absolute image location - important for exe packaging



##############################################################################################################################
### User-defined values
##############################################################################################################################

#cq_cutoff = 35
#pos_cutoff = 30
#dRn_percent_cutoff = 0.05 #if (sample dRn / max dRn) is less than this value, sample is considered No Amplification and marked negative


##############################################################################################################################
### 0. Main menu
##############################################################################################################################

def get_shared_assets_path(filename):
    '''Helper function: gets file path for asset in "shared" folder.'''
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, 'assets', filename)

class PandaaMenu:
    '''GUI object that holds information about user selections.'''
    def __init__(self, app_title='ReFocus Assistant',
                       version='0',
                       use='(RUO)',
                       header_title='PANDAA qPCR Results Analysis',
                       assay_choices=['PANDAA LASV', 'PANDAA CCHFV', 'PANDAA Ebola + Marburg'],
                       machine_choices=['QuantStudio 3', 'QuantStudio 5', 'Rotor-Gene', 'Mic']):
        ''''''
        self.root = None
        self.menu_frame = None

        self.app_title = app_title
        self.version = version
        self.use = use
        self.window_title = self.app_title + ' v' + self.version + ' ' + self.use
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
        path = os.path.join(sys._MEIPASS, filename) if hasattr(sys, '_MEIPASS') else get_shared_assets_path(filename)
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
        '''When 'Select file' button is clicked, assign assay/machine variables.'''
        self.assay = self.assay_var.get()
        self.machine = self.machine_var.get()

        self.root.withdraw()
        self.root.quit()
        # note: do NOT use self.close_program()!
        # using root.quit() instead ensures that root.mainloop() is ended, without actually quitting Python / destroying the run process
        

    def add_filebutton(self):
        '''Add button for user to proceed to file selection.'''
        ok_button = tk.Button(self.root,
                              text = 'Select results file...',
                              command = self.ok_click)
        ok_button.pack(side = 'bottom', pady = 30)

    
    def start(self):
        '''Run PandaaMenu.'''
        self.init_root()
        self.add_header()
        self.add_assay_choice()
        self.add_machine_choice()
        self.add_filebutton()
        self.root.mainloop()


if __name__ == '__main__':
    app = PandaaMenu()
    app.start()
    print(app.assay)