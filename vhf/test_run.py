print('Starting script...')

import sys
import vhf_library as vhf
import userinterface
import threading

print('Modules imported successfully...')

###

def run_gui():
    window = userinterface.PandaaMenu()
    window.start()
    print('GUI finished running.')


if __name__ == '__main__':
    print('Running PandaaMenu...')
    run_gui()
    
    print('Checking results...')
    #print(window.analyzer)
    #print(window.analyzer.results)
