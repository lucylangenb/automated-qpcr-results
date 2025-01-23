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
### Imports
##############################################################################################################################

import tkinter as tk # GUI handling
from tkinter import messagebox
from PIL import Image, ImageTk # Image handling
import os # Filepath handling
import sys # Executable packaging
import vhf_library as vhf # Custom dependency for parsing and analysis
import pandas as pd

class PANDAAApp:
    def __init__(self):
        self.root = tk.Tk()
        self.assay = None
        self.machine_type = None

    def setup_main_menu(self):
        self.root.title('Aldatu Biosciences - qPCR Analysis')
        self.root.geometry('500x350')
        self.root.protocol('WM_DELETE_WINDOW', self.close_program)
        self.center_window()

        ico = self.get_image('aldatulogo_icon.gif')
        self.root.wm_iconphoto(True, ico)

        logo = self.get_image('aldatulogo.gif', resize=(100, 100))
        logo_label = tk.Label(self.root, image=logo)
        logo_label.image = logo
        logo_label.pack(side='top', fill=tk.X, pady=15)

        title_label = tk.Label(self.root, text='PANDAA qPCR Results Analysis', font=('Arial', 12, 'bold'))
        title_label.pack(side='top', fill=tk.X, pady=10)

        self.setup_questions_frame()

        ok_button = tk.Button(self.root, text='Select results file...', command=self.ok_click)
        ok_button.pack(side='bottom', pady=30)

        self.root.mainloop()

    def center_window(self):
        self.root.update_idletasks()
        width, height = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def get_image(self, filename, resize=None):
        path = os.path.join(sys._MEIPASS, filename) if hasattr(sys, '_MEIPASS') else filename
        img = Image.open(path)
        if resize:
            img = img.resize(resize)
        return ImageTk.PhotoImage(img)

    def setup_questions_frame(self):
        questions_frame = tk.Frame(self.root)
        questions_frame.pack(side='top')

        assay_type_frame = tk.Frame(questions_frame)
        assay_type_frame.pack(side='left', padx=20)

        tk.Label(assay_type_frame, text='Choose assay results to analyze:', font=('Arial', 10)).pack(side='top', fill=tk.X, pady=2)
        self.assay_var = tk.StringVar(value=None)

        for option in ['PANDAA LASV', 'PANDAA CCHFV', 'PANDAA Ebola + Marburg']:
            tk.Radiobutton(assay_type_frame, text=option, variable=self.assay_var, value=option).pack(anchor=tk.W)

        machine_type_frame = tk.Frame(questions_frame)
        machine_type_frame.pack(side='right', padx=20)

        tk.Label(machine_type_frame, text='qPCR machine used:', font=('Arial', 10)).pack(side='top', fill=tk.X, pady=2)
        self.machine_var = tk.StringVar(value='QuantStudio 5')

        tk.OptionMenu(machine_type_frame, self.machine_var, 'QuantStudio 3', 'QuantStudio 5', 'Rotor-Gene', 'Mic').pack(anchor=tk.W)

    def ok_click(self):
        self.assay = self.assay_var.get()
        self.machine_type = self.machine_var.get()
        self.close_program()

    def close_program(self):
        try:
            self.root.destroy()
        except Exception as e:
            print(f"Error while closing resources: {e}")
        finally:
            raise SystemExit()

    def validate_assay(self):
        valid_assays = ['PANDAA LASV', 'PANDAA CCHFV', 'PANDAA Ebola + Marburg']
        if self.assay not in valid_assays:
            raise ValueError(f"Invalid assay selection: {self.assay}. Please select a valid assay.")

    def get_pandaa_result(self, row, fluor_names, internal_control_fluor, unique_reporters, max_dRn):
        cq_vals = [98]

        for i in range(1, len(unique_reporters)):
            if self.machine_type in ['QuantStudio 3', 'QuantStudio 5']:
                if (row[unique_reporters[i] + ' CT'] < 30 and
                        row[unique_reporters[i] + ' dRn'] / max_dRn[unique_reporters[i]] > 0.05):
                    cq_vals.append(row[unique_reporters[i] + ' CT'])
                else:
                    cq_vals.append(99)
            else:
                if row[unique_reporters[i] + ' CT'] < 30:
                    cq_vals.append(row[unique_reporters[i] + ' CT'])
                else:
                    cq_vals.append(99)

        fluor_min = cq_vals.index(min(cq_vals))
        if fluor_min != 0:
            return f'{fluor_names[unique_reporters[fluor_min]]} Positive'
        elif row[internal_control_fluor + ' CT'] < 30:
            return 'Negative'
        else:
            return 'Invalid Result'

    def run_analysis(self):
        self.validate_assay()
        fluor_names, internal_control_fluor, unique_reporters = vhf.getfluors(self.assay)
        summary_table, results_file, head = None, None, None

        if self.machine_type in ["QuantStudio 3", "QuantStudio 5"]:
            summary_table, max_dRn, results_file, head = vhf.quantstudio(self.machine_type, fluor_names, cq_cutoff=35)
        elif self.machine_type == "Rotor-Gene":
            summary_table, results_file, head = vhf.rotorgene(fluor_names, cq_cutoff=35)
        elif self.machine_type == "Mic":
            summary_table, results_file, head = vhf.mic(fluor_names, cq_cutoff=35)

        summary_table['Result'] = summary_table.apply(lambda row: self.get_pandaa_result(row, fluor_names, internal_control_fluor, unique_reporters, max_dRn), axis=1)

        csv_columns = ["Well Position", "Sample Name", "Result"]

        for i in range(len(unique_reporters)):
            summary_table = summary_table.rename(columns={f'{unique_reporters[i]} CT': f'{fluor_names[unique_reporters[i]]} Cq'})
            csv_columns.insert(i + 2, f'{fluor_names[unique_reporters[i]]} Cq')
            if self.machine_type in ["QuantStudio 3", "QuantStudio 5"]:
                summary_table = summary_table.rename(columns={f'{unique_reporters[i]} Cq Conf': f'{fluor_names[unique_reporters[i]]} Cq Conf',
                                                              f'{unique_reporters[i]} dRn': f'{fluor_names[unique_reporters[i]]} dRn'})

        summary_filepath = os.path.splitext(results_file)[0] + " - Summary.csv"
        file_saved = False

        while not file_saved:
            try:
                summary_table.to_csv(path_or_buf=summary_filepath, columns=csv_columns, index=False)
                vhf.prepend(summary_filepath, head)
                file_saved = True
            except PermissionError:
                proceed = messagebox.askretrycancel(message='Unable to write results file. Make sure results file is closed, then click Retry to try again.', icon=messagebox.ERROR)
                if not proceed:
                    raise SystemExit()

        messagebox.showinfo(title="Success", message=f"Summary results saved in:\n\n{summary_filepath}")

if __name__ == "__main__":
    app = PANDAAApp()
    app.setup_main_menu()
    app.run_analysis()
