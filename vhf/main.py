##############################################################################################################################
### About this code
##############################################################################################################################
#
#   This script contains a main() function that can be used to run PANDAA data analysis from a GUI.
#
#

name = 'ReFocus Assistant'
use = '(RUO)'
year = '2025'
division = 'vhf'

##############################################################################################################################

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared'))) #look for custom dependencies in shared folder

import data_analysis as vhf
from userinterface import PandaaMenu
from reportbuilder import Report, get_app_info
from importlib import util
import time

with open(os.path.join(os.path.dirname(__file__), 'version_number.txt')) as f:
    __version__ = f.read().strip()


def main():
    '''Runs the full process of selecting an assay and machine, uploading a file, analyzing, and exporting results.'''
    
    # Handling pyinstaller splash screen, if it exists
    if '_PYI_SPLASH_IPC' in os.environ and util.find_spec("pyi_splash"):
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
        print('Splash screen closed.')
    
    # Initialize GUI to get user selections
    app = PandaaMenu(app_title=name,
                     version=__version__,
                     use=use,
                     year=year,
                     division=division,
                     assay_choices=['PANDAA LASV', 'PANDAA CCHFV', 'PANDAA Ebola + Marburg'],
                     machine_choices=['QuantStudio 3', 'QuantStudio 5', 'Rotor-Gene', 'Mic'])
    app.start()

    # Retrieve user's selections
    assay_selected = app.assay
    machine_selected = app.machine

    if not assay_selected or not machine_selected:
        print("Error: No assay or machine selected. Exiting.")
        return

    # Initialize the data importer and parse the file
    importer = vhf.DataImporter(assay=assay_selected, machine_type=machine_selected)
    importer.parse()

    # Analyze the data
    analyzer = vhf.DataAnalyzer(data=importer)
    analyzer.vhf_analysis()

    # Export the results
    time.sleep(0.3) #program runs extremely quickly - adding sleep step may improve perceived legitimacy
    exporter = vhf.DataExporter(importer, analyzer)
    exporter.export()

    
    # Make the results into a PDF
    pdf_filepath = os.path.splitext(exporter.dest_filepath)[0] + '.pdf'
    get_app_info(name, __version__, use)
    if 'QuantStudio' not in machine_selected:
        pdf = Report(pdf_filepath, exporter.header, exporter.results, path_as_filename=exporter.dest_filepath)
    else:
        pdf = Report(pdf_filepath, exporter.header, exporter.results)
    pdf.create()
    
    print("Analysis complete. Results exported successfully.")


if __name__ == '__main__':
    main()
