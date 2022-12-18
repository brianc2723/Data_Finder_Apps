# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 14:08:16 2022

@author: brianc2723
"""


import PySimpleGUI as sg
import pandas as pd
import datetime


# Add some color to the window


def data_entry_form():
    
 sg.theme('LightGreen3')
 
 #GUI layout (1)
 DATABASE_FILE = sg.popup_get_file("Choose your databse file (.csv):                                                                                  ","Find all record in your ID list  (Column MUST NAME as ID) ", file_types=(("ALL CSV Files", "*.csv"), ("ALL Files", "*.*"), ))
 database_dataframe = pd.read_csv(DATABASE_FILE)
 
 #GUI layout (2)
 ID_need_enquiry_FILE = sg.popup_get_file("Choose Your ID list (.csv) prepared (Leave blank if entering ID manually):                                 ", "Find all record in your ID list  (Column MUST NAME as ID) ", file_types=(("ALL CSV Files", "*.csv"), ("ALL Files", "*.*"), ))
 #enquiry_file_dataframe is read in loop beneath, to provide options to choose upload file or enter manully
 
 #GUI layout (3)
 layout = [
    [sg.Text('Manually enter ID:')],
    [sg.Text('(Leave blank if you have already imported a ID list)', text_color='red')],
    [sg.Text('ID', size=(15,1)), sg.InputText(key='ID')],
    [sg.Submit(), sg.Button('Clear'), sg.Exit()]
              ]

 window = sg.Window('Manually enter ID', layout)


 #  Provide a empty dataframe for adding more than one entry of ID into output file
 Appended_ID_row_extracted = pd.DataFrame(columns = ['ID'])
 
 #  Naming output file
 folder_time = datetime.datetime.now().strftime(" (%Y-%m-%d_%H-%M)")
 folder_name = "ID_ENQUIRY_RESULT"
 ID_ENQUIRY_RESULT = folder_name + folder_time + ".csv"





 def clear_input():
    for key in values:
        window[key]('')
    return None




 while True:
    
    event, values = window.read()

        
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
        
            
    if event == 'Submit':
       
      try:
        # Case_01 load file for enquiry, not entering ID manually
          enquiry_file_dataframe = pd.read_csv(ID_need_enquiry_FILE)
          same_ID_row_extracted = enquiry_file_dataframe.merge(database_dataframe, how='left', left_on='ID', right_on='ID')
          Appended_ID_row_extracted = pd.concat([Appended_ID_row_extracted, same_ID_row_extracted], ignore_index=True)

        
          Appended_ID_row_extracted.to_csv(ID_ENQUIRY_RESULT, index=False)  
   
          sg.popup('ID_enquiry_result(Date_Time).csv is export!')
          clear_input()
          
          window.close()
          
          
          
      except:
        # Case_02 not load any file for enquiry, entering ID manually one by one 
   
       
         read_ID_entry = pd.DataFrame(values, index = [0])
         same_ID_row_extracted = read_ID_entry.merge(database_dataframe, how='left', left_on='ID', right_on='ID')
         Appended_ID_row_extracted = pd.concat([Appended_ID_row_extracted, same_ID_row_extracted], ignore_index=True)

          
         Appended_ID_row_extracted.to_csv(ID_ENQUIRY_RESULT, index=False)   
            

         sg.popup('ID_enquiry_result(Date_Time).csv is export!')
         clear_input()
         
         #Not adding auto close for this case, it will break the loop. Beside we have Exit button already.
 
        
       
 window.close()
 
data_entry_form()
