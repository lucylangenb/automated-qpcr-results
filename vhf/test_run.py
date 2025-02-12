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


import vhf_library as vhf
from userinterface import PandaaMenu
from reportbuilder_2 import Report
import os

def main():
    '''Runs the full process of selecting an assay and machine, uploading a file, analyzing, and exporting results.'''
    
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

    '''
    headers_to_keep = ['Well Position', 'Sample Name']
    rm_headers = list(exporter.results)
    for header in headers_to_keep:
        #if header in rm_headers:
            rm_headers.remove(header)

    for header in rm_headers:
        exporter.results = exporter.results.drop(header, axis=1)
        '''

    '''
    results_header = list(exporter.results)
    print(results_header)
    print(type(results_header))

    results_csv = exporter.results.values.tolist()
    results_csv.insert(0, results_header)
    #to_csv(path_or_buf=None, columns=exporter.columns, index=False)
    print(results_csv)
    print(type(results_csv))
    '''

    
    # Make the results into a PDF
    pdf_filepath = os.path.splitext(exporter.dest_filepath)[0] + '.pdf'
    pdf = Report(pdf_filepath, exporter.header, exporter.results)
    pdf.create()
    

    print("Analysis complete. Results exported successfully.")

if __name__ == '__main__':
    main()
