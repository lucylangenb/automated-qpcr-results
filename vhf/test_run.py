print('Starting script...')

import sys
import vhf_library as vhf
import userinterface
import threading

print('Modules imported successfully...')

###


if __name__ == '__main__':
    print('Running PandaaMenu...')
    window = userinterface.PandaaMenu()
    window.start()
    
    print('Running analysis...')
    analyzer = vhf.DataAnalyzer(window.importer)
    analyzer.vhf_analysis()
    print('Analysis complete. Running export...')

    exporter = vhf.DataExporter(window.importer, analyzer)
    exporter.export()
    print('Export complete')
