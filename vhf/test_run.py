print('Starting script...')

import sys
import vhf_library as vhf
import userinterface
import threading

print('Modules imported successfully...')

###

def run_gui():
    
    print('GUI finished running.')


if __name__ == '__main__':
    print('Running PandaaMenu...')
    window = userinterface.PandaaMenu()
    window.start()
    print(window.importer.results)
    print('Checking results...')
    #print(window.analyzer)
    #print(window.analyzer.results)
