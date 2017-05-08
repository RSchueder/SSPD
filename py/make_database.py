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

# CURRENT ISSUE IS THAT I THINK IF THERE ARE ABSOLUTEY NO STREAMEU VALUES
# FOR A SUBSTANCE THEN IT TAKES THE LAST VALUE IT HAD FOR THE PREVIOUS SUBSTANCE
# check at least sub 126-33-0
#128-39-2
# there is something wrong where the kds kde kdw are being given to the wrong
# param
# this does not happen if I specify only 128-39-2
# must be due to leftovers from other substance?

###############################################################################
# USER CONSTANTS
make_db = 1 # 1 is on, 0 is off
# switch for creating the duplicate copy for manual manipulation
manual = 'true'
###############################################################################
os.chdir('../')
PATH = os.getcwd()
###############################################################################
    
if manual is 'true':
    #if manual is true then a second database will be created that can be edited manually
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

    abrev = [] # stream eu abbreviation
    STabrev = [] # simple treat abbreviation
    description = [] # stream eu description
    STdescription = [] # simple treat description
    units = []
    STunits = []
    source = []
    SUalias = []
    UFZalias = []
    term = []
    multiple = []
    paramN = []
    searchT = []
    conversion = []
    prop = []
    DW = []
    conversion2 = []
    ST = []
    STprop = []
    conversion3 = []

    with open(("%s\\database_properties\\stream_eu_meta.csv")%(PATH)) as csvfile:
        att = csv.reader(csvfile)
        for row in att:
            row = row[0].split(';')
            abrev.append(row[1])
            description.append(row[3])
            units.append(row[4])
            source.append(row[5])
            SUalias.append(row[6])
            UFZalias.append(row[7])
        attributes = [abrev,description,units,source,SUalias,UFZalias]

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
            prop.append(row[0])
            DW.append(row[1])
            conversion2.append(row[2])
        dictD2 = [prop,DW,conversion2]

    with open(("%s\\database_properties\\simple_treat_database_dictionary.csv")%(PATH)) as csvfile:
        att = csv.reader(csvfile)
        for row in att:
            row = row[0].split(';')
            STprop.append(row[0])
            ST.append(row[1])
            conversion3.append(row[2])
        dictD3 = [STprop, ST, conversion3]

###############################################################################
    if make_db == 1:
        create_table('substances',['CAS','SMILES', 'NAME'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('degredation_products',['CAS','degredation_product','quantity'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('substance_properties',['ID','CAS','property','value','unit','source'],['INT','TEXT','TEXT','TEXT','TEXT','TEXT'],conn,c)
        create_table('STREAM_EU_meta',['STREAM_EU_parameter','description','unit','source','SUalias','UFZalias'],['TEXT','TEXT','TEXT','TEXT','TEXT','TEXT'],conn,c)
        create_table('STREAM_EU_database_dictionary',['substance_property','STREAM_EU_parameter','conversion'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('SIMPLE_TREAT_meta',['SIMPLE_TREAT_parameter','description','unit'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('SIMPLE_TREAT_database_dictionary',['substance_property','SIMPLE_TREAT_parameter','conversion'],['TEXT','TEXT','TEXT'],conn,c)
###############################################################################
        os.chdir(('%s\\substance_properties\\source_properties\\physchem')%(PATH))
        iD = 1
        for file in glob.glob("*.txt"):    
            dat = read_csv(file,conn,c) # this is the whole file
            properties = dat[0] # these are the headers
            sourcefile = file
            iD = dynamic_entry('substance_properties', properties, dat, sourcefile, iD, conn, c)
###############################################################################
        # populate the property-model dictionary table
        dynamic_entry('STREAM_EU_meta', attributes[0], attributes, sourcefile, iD, conn, c)
        dynamic_entry('STREAM_EU_database_dictionary', dictD2[0], dictD2, sourcefile, iD, conn, c)
        dynamic_entry('SIMPLE_TREAT_meta', STattributes[0], STattributes, sourcefile, iD, conn, c)
        dynamic_entry('SIMPLE_TREAT_database_dictionary', dictD3[0], dictD3, sourcefile, iD, conn, c)
###############################################################################
    c.close()
    conn.close() 
print('Database is created')
