##############################################################################################################################
### About this code
##############################################################################################################################
#
#   This script contains a main() function that can be used to run PANDAA data analysis from a GUI.
#
#
##############################################################################################################################

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'shared'))) #look for custom dependencies in shared folder

import data_analysis as hiv
from userinterface import PandaaMenu
from reportbuilder import Report, get_app_info
from importlib import util
import time, tomli

with open(os.path.join(os.path.dirname(__file__), 'config.toml'), mode='rb') as f: #get TOML configuration
    config = tomli.load(f)
    info, intc, extc = config['info'], config['int'], config['ext']


def main():
    '''Runs the full process of selecting an assay and machine, uploading a file, analyzing, and exporting results.'''
    
    # Handling pyinstaller splash screen, if it exists
    if '_PYI_SPLASH_IPC' in os.environ and util.find_spec("pyi_splash"):
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
        print('Splash screen closed.')
    
    # Initialize GUI to get user selections
    app = PandaaMenu(app_title=info['name'],
                     version=info['version'],
                     use=info['use'],
                     disclaimer=info['disclaimer'],
                     year=info['year'],
                     division=intc['division'],
                     assay_choices=extc['assay_choices'],
                     assay_format=extc['assay_choice_format'],
                     machine_choices=extc['machine_choices'])
    app.start()

    # Retrieve user's selections
    assay_selected = app.assay
    machine_selected = app.machine

    if not assay_selected or not machine_selected:
        print("Error: No assay or machine selected. Exiting.")
        return

    # Initialize the data importer and parse the file
    importer = hiv.DataImporter(assay=assay_selected, machine_type=machine_selected,
                                cq_cutoff=intc['cq_cutoff'], division=intc['division'])
    importer.parse()

    # Analyze the data
    analyzer = hiv.DataAnalyzer(data=importer,
                                min_drm_percent=intc['min_drm_percent'], max_drm_percent=intc['max_drm_percent'])
    analyzer.hiv_analysis()

    # Export the results
    if intc['wait']:
        time.sleep(0.3) #program runs extremely quickly - adding sleep step may improve perceived legitimacy
    exporter = hiv.DataExporter(importer, analyzer,
                                columns=extc['export_columns'])
    exporter.export()
    
    # Make the results into a PDF
    if extc['create_pdf']:
        pdf_filepath = os.path.splitext(exporter.dest_filepath)[0] + '.pdf'
        get_app_info(info['name'], info['version'], info['use'])
        if 'QuantStudio' not in machine_selected:
            pdf = Report(pdf_filepath, exporter.header, exporter.results, path_as_filename=exporter.dest_filepath)
        else:
            pdf = Report(pdf_filepath, exporter.header, exporter.results)
        pdf.create()
    
    print("Analysis complete. Results exported successfully.")


if __name__ == '__main__':
    main()
