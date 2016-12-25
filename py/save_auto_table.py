# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:40:08 2016

@author: schueder
"""

def save_auto_table(table,PATH,conn,c):
    import os
    import csv
    if not os.path.exists(("%s\properties_table")%(PATH)):
        os.makedirs(("%s\properties_table")%(PATH))
    if os.path.isfile(("%s\properties_table\\auto_table.csv")%(PATH)):
        os.remove(("%s\properties_table\\auto_table.csv")%(PATH))
    os.chdir(("%s\properties_table")%(PATH))   
    with open(("%s\properties_table\\auto_table.csv")%(PATH),'a') as fileID:
        c.execute('''SELECT * FROM {qq}'''.format(qq = table))
        sel = c.fetchall()
        wr = csv.writer(fileID, dialect = 'excel')
        for ww in sel:
            wr.writerow(ww)
        
    
    
    
    
    