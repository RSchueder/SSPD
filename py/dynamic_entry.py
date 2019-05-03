# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 16:34:07 2016

@author: Rudy
"""
from isnum import isnum
import numpy as np
import sys


def dynamic_entry(table, properties, x, sourcefile, iD, conn, c):
    # the compounds file will not be run through this loop
    # in 5000 sub list the 5th line always marks the data
    if table is 'substance_properties':
        qu2 = []
        # here are all of the possible names for headers that are not properties
        notprop = ['No',	'Line in table Compounds',	'MLoS number']

        m = 4
        n = 3
        # and the metadata is always organized like this
        # 0 = endpoint
        # 1 model
        # 2 software
        # 3 property name
        # depending on how many of the rows were skipped before a CAS number (m)

        propertiesAugm = []
        propertiesComb = []
        unitind = 0
        modelind = 1
        softwareind = 2
        unit = x.iloc[unitind,:]
        model = x.iloc[modelind,:]
        software = x.iloc[softwareind,:]
        prop = x.iloc[3,:]
        x.replace(np.nan,'', inplace = True)
        # p is the index of the first property, n is the index of the first substance
        for jj in range(m,len(x[x.columns[0]])): #for each substance, skipping n headers
            tmp = x.loc[jj]
            # the unique number is the first index
            no = tmp[0]
            mlos = tmp[2]
            # unique index is 'MLOS'
            c.execute("SELECT CAS FROM substances WHERE MLOS = '{qq}'".format(qq=mlos))
            CAS = c.fetchall()
            for ii in range(n,len(tmp)): #for each property, skipping not props
                # ['ID', 'CAS', 'property', 'value', 'endpoint [unit]', 'model', 'software', 'source']
                
                entry = [iD, CAS[0][0], prop[ii], tmp[ii], unit[ii], model[ii], software[ii]]
                entry.append(sourcefile)
                qu = ['?' for number in range(len(entry))]
                qu2 = ' ,'.join(qu)
                try:
                    c.executemany('''INSERT INTO {tn} (ID, CAS, property, value, endpoint_unit, model, software, source) VALUES ({qq})'''.format(tn = table, qq = qu2), [entry])
                except:
                    print(entry)
                iD = iD + 1
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
            c.executemany('''INSERT INTO {tn} (STREAM_EU_parameter,description,unit) VALUES ({qq})'''.format(tn = table, qq = qu2), [entry])                                                   

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
            c.executemany('''INSERT INTO {tn} (substance_property,STREAM_EU_parameter,conversion, method) VALUES ({qq})'''.format(tn = table, qq = qu2), [entry])

    if table is 'SIMPLE_TREAT_database_dictionary':
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
            c.executemany('''INSERT INTO {tn} (substance_property,SIMPLE_TREAT_parameter,conversion, method) VALUES ({qq})'''.format(tn = table, qq = qu2), [entry])

    if table is 'SIMPLE_TREAT_meta':
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
            c.executemany('''INSERT INTO {tn} (SIMPLE_TREAT_parameter,description,unit) VALUES ({qq})'''.format(tn = table, qq = qu2), [entry])

###############################################################################
    if table is 'substances':
        # only occurs with one of the files
        m = 4
        n = 4

        noind = 0
        mlosind = 3
        CASind = 6
        nameind = 7
        smilesind = 8
        codeind = 9
        mwind = 11

        # now add the CAS substance info if the CAS does not exist
        for jj in range(m, len(x[x.columns[0]])):  # for each substance, all properties, skipping headers
            tmp = x.loc[jj]
            entry = [tmp[noind],tmp[CASind], tmp[smilesind], tmp[nameind], tmp[codeind],tmp[mlosind],tmp[mwind]]
            qu = ['?' for number in range(len(entry))]
            qu2 = ' ,'.join(qu)
            c.executemany('''INSERT OR IGNORE INTO substances ('NO','CAS','SMILES', 'NAME', 'CODE','MLOS','MW') VALUES ({qq})'''.format(qq=qu2),
            [entry])

            #return iD
            
    conn.commit()

