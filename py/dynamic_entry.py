# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 16:34:07 2016

@author: Rudy
"""
from isnum import isnum
def dynamic_entry(table,properties,x,sourcefile,iD,conn,c): 
    if table is 'substance_properties':    
        qu2 = []
        # here are all of the possible names for headers that are not properties
        notprop = ['#','Substance No','CAS','Chem name', 'Smiles','SMILES',
                   'NAME','Name','Cas#','Chem. Name','CAS RN','Parent #','Parent Cas#', 
                   'Parent Chem. Name', 'Parent Smiles', 'Substance type']
        # sometimes there are 1-3 headers, make something that can determine
        # this number for this particular file
        
        # for the first few rows, scan the first three columns for a CAS number
        # the row at which a CAS number is found determines how many headers 
        # there are
        n = 0
        p = 0
        for mm in range(0,len(x)):
            # we check for CAS number by seeing if it is a real number, we only 
            # check the first three columns for CAS numbers in a given row
            if isnum(x[mm][0].replace('-','')) or isnum(x[mm][1].replace('-','')) or isnum(x[mm][2].replace('-','')):
                p = 1
            else:
                n = n + 1
            if p is 1:
                break
        # find the index of keys
        # depending on how many of the rows were skipped before a CAS number (n)
        # was found, the name of the property will be the conjugation of all 
        # values in that index
        propertiesAugm = []
        propertiesComb = []
        unitind = []
        unit = []
        # add all of the names together, that is skwish n rows together
        for jj in range(0,n):
            propertiesAugm.append(x[jj])
        # for the number of properties    
        for jj in range(0,len(propertiesAugm[0])):
            tmp = []
            #for each row (name) in each property column, combine them
            for ii in range(0,n):
                tmp.append(propertiesAugm[ii][jj])
            tmp = ','.join(tmp)
            tmp = tmp.replace(',','-')
            tmp = tmp.replace('-','')
            tmp = tmp.rstrip()
            propertiesComb.append(tmp)
            
        p = 0
        #this is contingent on the assumption that all notprops come before
        #real properties
        for jj in range(0,len(propertiesComb)):
            if 'Unit' in propertiesComb[jj]:
                unit.append(propertiesComb[jj])
                unitind.append(jj)
            if propertiesComb[jj].replace('-','') in notprop:
                if 'CAS' in propertiesComb[jj] or 'Cas' in propertiesComb[jj]:
                    CASind = jj
                if 'smiles' in propertiesComb[jj] or 'SMILES' in propertiesComb[jj] or 'Smiles' in propertiesComb[jj]:
                    smilesind = jj
                if 'NAME' in propertiesComb[jj] or 'Chem name' in propertiesComb[jj] or 'Chem. name' in propertiesComb[jj] or 'Name' in propertiesComb[jj]:
                    nameind = jj
                p = p + 1
        # p is the index of the first property, n is the index of the first substance
        for jj in range(n,len(x)): #for each substance, skipping n headers
            tmp = x[jj]
            for ii in range(p,len(tmp)): #for each property, skipping notprops
                if propertiesComb[ii] in unit:
                    pass
                else:
                    # need to look through available units to see if there is a
                    # matching one for the current property
                    if any(propertiesComb[ii] in uu for uu in unit):
                        unitProp = [s for s in unit if propertiesComb[ii] in s]
                        thisInd = unit.index(unitProp[0])
                        unitvalInd = unitind[thisInd]
                        vUnit = tmp[unitvalInd]
                    else:
                        vUnit = 'N/A'
                    entry = [iD,tmp[CASind],propertiesComb[ii],tmp[ii],vUnit]
                    entry.append(sourcefile)
                    qu = ['?' for number in range(len(entry))]
                    qu2 = ' ,'.join(qu)                    
                    c.executemany('''INSERT INTO {tn} (ID, CAS, property, value, unit, source) VALUES ({qq})'''.format(tn = table, qq = qu2), [entry])
                    iD = iD + 1
#        for ii in unit:
#            unitProp = ii.replace('( Unit)','')
#            print((('unitprop = %s ')% unitProp))
#            c.execute('''SELECT unit FROM substance_properties WHERE property = "%{pp}%"''')
#            c.executemany('''INSERT INTO substance_properties (unit) VALUES ('?')''', [unitProp])

###############################################################################
#now add the CAS substance info if the CAS does not exist
        qu2 = []
        for jj in range(1,len(x)): #for each substance, all properties, skipping headers
            tmp = x[jj]
            if '*' in tmp[CASind]:
                pass
            else:
                entry = [tmp[CASind],tmp[smilesind],tmp[nameind]]
                qu = ['?' for number in range(len(entry))]
                qu2 = ' ,'.join(qu)
                c.executemany('''INSERT OR IGNORE INTO substances (CAS, SMILES, NAME) VALUES ({qq})'''.format(qq = qu2), [entry])  
        return iD                     
###############################################################################
                    
    if table is 'STREAM_EU_meta':
        qu2 = []
        for jj in range(len(x[0])): #for each property
            tmp = []
            entry = []
            for nn in range(len(x)): #for each column or property attribute           
                tmp.append(x[nn][jj])
            for ii in range(len(tmp)):
                entry.append(tmp[ii])
            qu = ['?' for number in range(len(tmp))]
            qu2 = ' ,'.join(qu)
            c.executemany('''INSERT INTO {tn} (STREAM_EU_parameter,description,unit,source,SUalias,UFZalias) VALUES ({qq})'''.format(tn = table, qq = qu2), [entry])                                                   

    if table is 'STREAM_EU_database_dictionary':
        qu2 = []
        for jj in range(len(x[0])):
            tmp = []
            entry = []
            for nn in range(len(x)):
                tmp.append(x[nn][jj])
            for ii in range(len(tmp)):
                entry.append(tmp[ii])
            qu = ['?' for number in range(len(tmp))]
            qu2 = ' ,'.join(qu)    
            c.executemany('''INSERT INTO {tn} (substance_property,STREAM_EU_parameter,conversion) VALUES ({qq})'''.format(tn = table, qq = qu2), [entry])            
            
            conn.commit()
    
