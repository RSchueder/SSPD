# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 16:34:33 2016

@author: Rudy
"""

def create_table(table,headers,types,conn,c):
    nn = 0
    c.execute('CREATE TABLE IF NOT EXISTS {tn} ({cn} {ct}, UNIQUE({cn}))' 
    .format(tn = table, cn = headers[nn], ct = types[nn]))
    nn = 1
    for ii in range(nn,len(headers)):
        c.execute('''SELECT * FROM {tn}'''.format(tn = table))
        columns = list(map(lambda x: x[0], c.description))
        if headers[ii] in columns:
            continue
        else:          
            c.execute('''ALTER TABLE {tn} ADD COLUMN '{cn}' {ct}'''
            .format(tn = table, cn = headers[ii], ct = types[ii]))
    
    conn.commit()
    


