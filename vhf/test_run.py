import sys
import threading
import vhf_library as vhf
import userinterface

print('Starting script...')
print('Modules imported successfully...')

def run_gui():
    window.start()

if __name__ == '__main__':
    print('Running PandaaMenu...')
    window = userinterface.PandaaMenu()

    # Start GUI in a separate thread
    gui_thread = threading.Thread(target=run_gui)
    gui_thread.start()

    # Wait for GUI to finish before continuing
    gui_thread.join()

    # Check if file was imported successfully
    if not hasattr(window, 'importer') or window.importer is None:
        print("Error: No file was selected. Exiting...")
        sys.exit(1)

    print('Running analysis...')
    analyzer = vhf.DataAnalyzer(window.importer)
    analyzer.vhf_analysis()
    print('Analysis complete. Running export...')

    exporter = vhf.DataExporter(window.importer, analyzer)
    exporter.export()
    print('Export complete')
