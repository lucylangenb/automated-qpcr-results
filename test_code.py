###
### testing tk optionmenu
###

import tkinter as tk

root = tk.Tk()
root.title('Test window')
root.geometry('200x200')


options_list = ['PANDAA qDx LASV', 'PANDAA Ebola + Marburg Complete']
value_inside = tk.StringVar()

value_inside.set('Select an option')

question_menu = tk.OptionMenu(root, value_inside, *options_list)
question_menu.pack()

def print_answers(): 
    print("Selected Option: {}".format(value_inside.get())) 
    return None

submit_button = tk.Button(root, text='Submit', command=print_answers) 
submit_button.pack() 
  
root.mainloop() 