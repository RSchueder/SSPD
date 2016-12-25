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
from search_list import search_list
from datetime import datetime

startTime = datetime.now()
###############################################################################
#USER CONSTANTS
model = 'STREAM_EU'
make_db = 1 # 1 is on, 0 is off
#switch for creating the duplicate copy for manual manipulation
manual = 'true'
###############################################################################
os.chdir('../')
PATH = os.getcwd()

if os.path.isfile(("%s\properties_table\overall\overall.txt")%(PATH)):
    os.remove(("%s\properties_table\overall\overall.txt")%(PATH))
if not os.path.exists(("%s\properties_table\overall")%(PATH)):
    os.makedirs(("%s\properties_table\overall")%(PATH))
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
    abrev = []
    description = []
    units = []
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
    
###############################################################################
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
    with open(("%s\\database_properties\\stream_eu_database_dictionary.csv")%(PATH)) as csvfile:
        att = csv.reader(csvfile)
        for row in att:
            row = row[0].split(';')
            prop.append(row[0])
            DW.append(row[1])
            conversion2.append(row[2])
        dictD2 = [prop,DW,conversion2]
###############################################################################
    if make_db == 1:
        create_table('substances',['CAS','SMILES', 'NAME'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('degredation_products',['CAS','degredation_product','quantity'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('substance_properties',['ID','CAS','property','value','unit','source'],['INT','TEXT','TEXT','TEXT','TEXT','TEXT'],conn,c)
        create_table('STREAM_EU_meta',['STREAM_EU_parameter','description','unit','source','SUalias','UFZalias'],['TEXT','TEXT','TEXT','TEXT','TEXT','TEXT'],conn,c)
        create_table('STREAM_EU_database_dictionary',['substance_property','STREAM_EU_parameter','conversion'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('emissions_meta',['emissions_parameter','description','unit'],['TEXT','TEXT','TEXT'],conn,c)
        create_table('emissions_database_dictionary',['substance_property','emissions_parameter','conversion'],['TEXT','TEXT','TEXT'],conn,c)
###############################################################################
        os.chdir(('%s\\substance_properties\\source_properties')%(PATH))
        iD = 1
        for file in glob.glob("*.txt"):    
            dat = read_csv(file,conn,c) # this is the whole file
            properties = dat[0] # these are the headers
            sourcefile = file
            iD = dynamic_entry('substance_properties',properties,dat,sourcefile,iD,conn,c)
###############################################################################
        # populate the property-DELWAQ dictionary table
        dynamic_entry('STREAM_EU_meta',attributes[0],attributes,sourcefile,iD,conn,c)
        dynamic_entry('STREAM_EU_database_dictionary',dictD2[0],dictD2,sourcefile,iD,conn,c)
###############################################################################
    
    # read all of the unique CAS numbers from the database to determine list to put into program file
    
    c.execute("SELECT CAS FROM substances where CAS IS NOT NULL AND TRIM(CAS)") 
    allCAS = c.fetchall()
    allCAS = list(allCAS)
    allCAS = set(allCAS)
    allCAS = list(allCAS)
###############################################################################
    #MUST SPECIFY METHOD IN search_list.py IF YOU DO NOT WISH TO USE THE 
    #DEFAULT SEARCH TERMS IN THE delwaq_parameter_att.csv
    
    method, filespec1, filespec2, filespec3, ref_temp = search_list(abrev)
    
    headers  = 0    
    #for ii in range(0,1):
    for ii in range(0,len(allCAS)):
        
        #CASreq = '117-81-7'
        CASreq = allCAS[ii][0]

###############################################################################    
    #for user prompted input
    #CASreq = '215-58-7'
    #CASreq = input('enter CAS number or SMILES    ')
    #model = input('enter output type "(DELWAQ)"   ')
###############################################################################
        
        if dd is '':
            # the database is already created
            data = read_from_db(CASreq,conn,c)
            write_STREAM_EU_output(CASreq,allCAS,ii,model,method,filespec1,filespec2,filespec3,ref_temp,data,PATH,headers,conn,c)
        if ii is 0:
            headers = 1
        #else:
           #data = read_from_db(CASreq,conn,c)
        
    c.close()
    conn.close() 
    print(datetime.now()-startTime)