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
                       year='2025',
                       division='vhf',
                       header_title='PANDAA qPCR Results Analysis',
                       assay_choices=['PANDAA LASV', 'PANDAA CCHFV', 'PANDAA Ebola + Marburg'],
                       machine_choices=['QuantStudio 3', 'QuantStudio 5', 'Rotor-Gene', 'Mic']):
        ''''''
        self.root = None
        self.menu_frame = None

        self.app_title = app_title
        self.version = version
        self.use = use
        self.year = year
        self.division = division
        self.window_title = self.app_title + ' v' + self.version + ' ' + self.use
        self.header_title = header_title
        self.assay_choices = assay_choices
        self.machine_choices = machine_choices

        self.assay = None
        self.machine = None


    def get_file_path(self, filename):
        '''Helper function: gets file path for asset in vhf or hivdr folder.'''
        base_dir = os.path.dirname(__file__)
        return os.path.join(base_dir, '..', self.division, filename)


    def center_window(self, win, xadj=0, yadj=0):
        '''Center window on user's screen.
        
        Optionally, adjust window location further using xadj and yadj parameters.
        '''
        win.update_idletasks()             #check for any changes to window size
        width = win.winfo_width()          #get root's width and height
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)  #x = half of screen width / half of window width
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x+xadj}+{y+yadj}')  #use previously calculated x, y as adjustments to horiz/vert window alignment on screen


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
        self.root.geometry('500x360')
        self.root.resizable(False, False)

        # when delete_window event occurs, run close_program function
        self.root.protocol('WM_DELETE_WINDOW', self.close_program)

        # change feather icon in upper corner to Aldatu logo
        ico = self.get_image('aldatulogo_icon.gif')
        self.root.wm_iconphoto(True, ico) #True bool here ensures that all subsequent windows also use this icon

    
    def add_menu(self):
        '''Add menu bar to tkinter window.'''
        menubar = tk.Menu()

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label='{} Help...'.format(self.app_title),
                              accelerator='Ctrl+H',
                              command=self.help_click)
        file_menu.add_command(label='About {}...'.format(self.window_title),
                              command=self.about_click)
        
        menubar.add_cascade(menu=file_menu, label='Help')
        self.root.config(menu=menubar)


    def about_click(self):
        '''When "About" is clicked in menu bar, show info.'''
        self.about_window = tk.Toplevel()
        self.about_window.title('About {}'.format(self.window_title))
        self.about_window.config(width=400, height=275,
                            background='white',
                            relief='groove')
        self.about_window.overrideredirect(True) #make window borderless - splash-screen style
        self.about_window.resizable(False, False)
        self.about_window.focus() #make this the active/top window
        self.about_window.grab_set() #modal window - can't do anything with main program until About window is closed
        self.center_window(self.about_window, yadj=28)

        border_color = '#525252'
        frame = tk.Frame(self.about_window, background='white',highlightbackground=border_color, highlightthickness=2, bd=0)
        frame.pack()

        canvas = tk.Canvas(frame, background='white', width=400, height=100,
                           highlightthickness=0) #removes border around canvas element
        canvas.pack()
        canvas.create_image(self.about_window.winfo_width()//2, 50, image=self.logo)

        
        text = tk.Label(frame,
                          text='''\n{name}\nVersion {ver}\nCopyright © {year} Aldatu Biosciences, Inc.\n\nFor Research Use Only.\nNot for use in diagnostic procedures.
                          '''.format(name=self.app_title, ver=self.version, year=self.year),
                          font=('Arial', 10),
                          background='white',
                          anchor='w',
                          justify='left'
                          ).pack(side='top',
                                 fill=tk.X,
                                 padx=35)

        close_button = tk.Button(frame,
                                text='Close',
                                command=self.closeabout_click)
        close_button.pack(side='right',
                         anchor=tk.SE,
                         padx=5,
                         pady=5)
        
        eula_button = tk.Button(frame,
                                text='View license agreement',
                                command=self.eula_click)
        eula_button.pack(side='right',
                         anchor=tk.SE,
                         pady=5)


    def help_click(self):
        '''When "Help" is clicked in menu bar, show readme file.'''
        print('Help was clicked')

    def eula_click(self):
        '''Pull up EULA text file when button is clicked.'''
        path = os.path.join(sys._MEIPASS, 'eula.txt') if hasattr(sys, '_MEIPASS') else self.get_file_path('eula.txt')
        os.startfile(path)

    def closeabout_click(self):
        '''Close the About window.'''
        self.about_window.destroy()


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


    def getfile_click(self):
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
                              command = self.getfile_click)
        ok_button.pack(side = 'bottom', pady = 30)

    
    def start(self):
        '''Run PandaaMenu.'''
        self.init_root()
        self.add_menu()
        self.add_header()
        self.add_assay_choice()
        self.add_machine_choice()
        self.add_filebutton()
        self.center_window(self.root)
        self.root.mainloop()


if __name__ == '__main__':
    app = PandaaMenu()
    app.start()
    print(app.assay)