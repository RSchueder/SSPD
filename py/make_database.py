# -*- coding: utf-8 -*-

#Created on Sun Jul 10 14:10:57 2016

#@author: Rudy

import os
import glob
import csv
import sqlite3
from dynamic_entry import dynamic_entry
from create_table import create_table
from read_from_db import read_from_db
from read_csv import read_csv
from write_STREAM_EU_output import write_STREAM_EU_output
from save_auto_table import save_auto_table
from make_hl_val import make_hl_val
from get_val import get_val
from datetime import datetime
from read_csv2array import read_csv2array
import pandas as pd
from read_csv2dict import read_csv2dict


try:
    c.close()
    conn.close()
except:
    pass

startTime = datetime.now()

###############################################################################
# USER CONSTANTS
make_db = 1  # 1 is on, 0 is off
# switch for creating the duplicate copy for manual manipulation
manual = 'false'
###############################################################################
os.chdir('../')
PATH = os.getcwd()
###############################################################################
    
if manual is 'true':
    # if manual is true then a second database will be created that can be edited manually
    ll = ['','_manual']
else:
    ll = ['']
for dd in ll:
    if os.path.isfile(('%s\\substance_properties%s.db')%(PATH,dd)) and make_db == 1:
        os.remove(('%s\\substance_properties%s.db')%(PATH,dd))
    os.chdir(PATH)
    conn = sqlite3.connect(('substance_properties%s.db')%(dd))
    c = conn.cursor()

    ###############################################################################
    #                    POPULATE THE DATABASE PROPERTIES
    ###############################################################################

    SEabrev = [] # stream eu abbreviation
    STabrev = [] # simple treat abbreviation
    SEdescription = [] # stream eu description
    STdescription = [] # simple treat description
    SEunits = []
    STunits = []
    searchT = []
    SEprop = []
    SEparam = []
    conversionSE = []
    STparam = []
    STprop = []
    conversionST = []
    SEmethod = []
    STmethod = []

    with open(("%s\\database_properties\\stream_eu_meta.csv")%(PATH)) as csvfile:
        att = csv.reader(csvfile)
        for row in att:
            row = row[0].split(';')
            SEabrev.append(row[1])
            SEdescription.append(row[3])
            SEunits.append(row[4])
        SEattributes = [SEabrev,SEdescription,SEunits]

    with open(("%s\\database_properties\\simple_treat_meta.csv") % (PATH)) as csvfile:
        att = csv.reader(csvfile)
        for row in att:
            row = row[0].split(';')
            STabrev.append(row[0])
            STdescription.append(row[1])
            STunits.append(row[2])
        STattributes = [STabrev, STdescription, STunits]

    with open(("%s\\database_properties\\stream_eu_database_dictionary.csv")%(PATH)) as csvfile:
        att = csv.reader(csvfile)
        for row in att:
            row = row[0].split(';')
            SEprop.append(row[0])
            SEparam.append(row[1])
            conversionSE.append(row[2])
            SEmethod.append(row[3])
        dictSE = [SEprop, SEparam, conversionSE, SEmethod]

    with open(("%s\\database_properties\\simple_treat_database_dictionary.csv")%(PATH)) as csvfile:
        att = csv.reader(csvfile)
        for row in att:
            row = row[0].split(';')
            STprop.append(row[0])
            STparam.append(row[1])
            conversionST.append(row[2])
            STmethod.append(row[3])

        dictST = [STprop, STparam, conversionST, STmethod]

###############################################################################
    if make_db == 1:
        create_table('STREAM_EU_meta',['STREAM_EU_parameter','description','unit'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('STREAM_EU_database_dictionary',['substance_property','STREAM_EU_parameter','conversion','method'],['TEXT','TEXT','TEXT','TEXT'],conn,c)
        create_table('SIMPLE_TREAT_meta',['SIMPLE_TREAT_parameter','description','unit'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('SIMPLE_TREAT_database_dictionary',['substance_property','SIMPLE_TREAT_parameter','conversion','method'],['TEXT','TEXT','TEXT','TEXT'],conn,c)
        create_table('substances',['NO','CAS','SMILES', 'NAME', 'CODE','MLOS','MW'],['TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT'],conn,c)
        create_table('substance_properties',['ID','CAS','property','value','endpoint_unit','model','software','source'],['TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT','TEXT'],conn,c)

###############################################################################
        os.chdir(('%s\\substance_properties\\')%(PATH))
        iD = 1
        for file in glob.glob("*.xlsx"):    
            xl = pd.ExcelFile(file)
            sheets = xl.sheet_names
            properties = []

            for ss in sheets:
                dat = pd.read_excel(file, sheetname = ss, header = None)
                sourcefile = file + '_' + ss
                print(sourcefile)
                if 'Compounds' in ss:
                    dynamic_entry('substances', properties, dat, sourcefile, iD, conn, c)
                else:
                    iD = dynamic_entry('substance_properties', properties, dat, sourcefile, iD, conn, c)
###############################################################################
        # populate the property-model dictionary table
        dynamic_entry('STREAM_EU_meta', SEattributes[0], SEattributes, sourcefile, iD, conn, c)
        dynamic_entry('STREAM_EU_database_dictionary', dictSE[0], dictSE, sourcefile, iD, conn, c)
        dynamic_entry('SIMPLE_TREAT_meta', STattributes[0], STattributes, sourcefile, iD, conn, c)
        dynamic_entry('SIMPLE_TREAT_database_dictionary', dictST[0], dictST, sourcefile, iD, conn, c)
###############################################################################
    c.close()
    conn.close() 
print('COMPLETE: Database is created')
