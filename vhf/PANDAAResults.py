##############################################################################################################################
### About this code
##############################################################################################################################
#
#   This script contains a main() function that can be used to run PANDAA data analysis from a GUI.
#
#


##############################################################################################################################
### EXE PACKAGING INSTRUCTIONS
##############################################################################################################################

# pyinstaller --onefile -w --add-data="*.gif;." --icon=aldatulogo_icon.ico --version-file=version.txt PANDAAResults.py

# --add-data flag expects directory info in the format SOURCE;DESTINATION - use '.' as destination for "this directory"
# --icon adds an icon
# --version-file adds readable file properties


import data_analysis as vhf
from userinterface import PandaaMenu
from reportbuilder import Report
import os
from importlib import util

def main():
    '''Runs the full process of selecting an assay and machine, uploading a file, analyzing, and exporting results.'''\
    
    # Handling pyinstaller splash screen, if it exists
    if '_PYI_SPLASH_IPC' in os.environ and util.find_spec("pyi_splash"):
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
        print('Splash screen closed.')
    
    # Initialize GUI to get user selections
    app = PandaaMenu()
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
    exporter = vhf.DataExporter(importer, analyzer)
    exporter.export()

    
    # Make the results into a PDF
    pdf_filepath = os.path.splitext(exporter.dest_filepath)[0] + '.pdf'
    if 'QuantStudio' not in machine_selected:
        pdf = Report(pdf_filepath, exporter.header, exporter.results, path_as_filename=exporter.dest_filepath)
    else:
        pdf = Report(pdf_filepath, exporter.header, exporter.results)
    pdf.create()
    
    print("Analysis complete. Results exported successfully.")


if __name__ == '__main__':
    main()
