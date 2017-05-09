# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 17:43:36 2017

@author: schueder

this script was written to de-couple any database querying or writing from the
creation of the database itself
"""
import os
import glob
import csv
import shutil
import sqlite3
from dynamic_entry import dynamic_entry
from create_table import create_table
from read_from_db import read_from_db
from read_csv import read_csv
from write_STREAM_EU_output import write_STREAM_EU_output
from save_auto_table import save_auto_table
from make_hl_val import make_hl_val
from get_val import get_val
from STREAM_EU_search_list import STREAM_EU_search_list
from datetime import datetime
from read_csv2array import read_csv2array
import pandas as pd
from read_csv2dict import read_csv2dict

os.chdir('../')
PATH = os.getcwd()
if os.path.isfile(("%s\properties_table\STREAM_EU\property_matrix.txt")%(PATH)):
    os.remove(("%s\properties_table\STREAM_EU\property_matrix.txt")%(PATH))
if not os.path.exists(("%s\properties_matrix\STREAM_EU")%(PATH)):
    os.makedirs(("%s\properties_matrix\STREAM_EU")%(PATH))
try:
    shutil.rmtree(("%s\stream_eu_include_files")% PATH)
except:
    pass
if not os.path.exists(("%s\stream_eu_include_files")% PATH):
    os.makedirs(("%s\stream_eu_include_files")% PATH)

try:
    c.close()
    conn.close()
except:
    pass
conn = sqlite3.connect('substance_properties.db')
c = conn.cursor()
model = 'STREAM_EU'

# paramReq = delwaq all parameters
# paramPos = delwaq parameters confirmed in database
# FOR EACH PARAMETER IN THE DATABASE AN EQUIVALENT NAME MUST BE GIVEN
# IN THIE DISCTIONARY (MANUALLY ADDED) THAT TELLS THE PROGRAM HOW TO
# TRANSLATE BETWEEN GENERIC PROPERTY NAMES AND STREAM EU PROPERTY NAMES
        
c.execute("SELECT STREAM_EU_parameter FROM STREAM_EU_meta")
paramReq = c.fetchall()
c.execute("SELECT STREAM_EU_parameter FROM STREAM_EU_database_dictionary")
paramPos = c.fetchall()

search_t = []

os.chdir(PATH)

###############################################################################

defaultCAS = 1

# get the search terms from the DELWAQ dictionary v2 table
# compare to all of the known paramters to identify known and unknown
for nn in range(0, len(paramReq)):
    # if there is a corresponding property in the database
    if paramReq[nn][0] in [lp[0] for lp in paramPos]:
        search_t.append(paramReq[nn][0])
        # search_t contains all parameters present in the database
        # these are those we are going to loop through
                
# read all of the unique CAS numbers from the database to determine list to put into program file
if defaultCAS == 1:
    c.execute("SELECT CAS FROM substances where CAS IS NOT NULL AND TRIM(CAS)") 
    allCAS = c.fetchall()
    allCAS = list(allCAS)
    allCAS = set(allCAS)
    allCAS = list(allCAS)
###############################################################################
    # MUST SPECIFY METHOD IN search_list.py IF YOU DO NOT WISH TO USE THE
    # DEFAULT SEARCH TERMS IN THE delwaq_parameter_att.csv
    
method, filespec1, filespec2, filespec3, ref_temp = STREAM_EU_search_list(paramReq,paramReq)
headers = 0

for ii in range(0, len(allCAS)):
    if defaultCAS == 1:
        # this is taken from the data base and is thus a tuple
        CASreq = allCAS[ii][0]
    else:
        CASreq = allCAS[ii]
###############################################################################
    data = read_from_db(CASreq, conn, c)
    write_STREAM_EU_output(CASreq, allCAS, paramReq, paramPos, search_t, ii, model, method, filespec1, filespec2,
                           filespec3, ref_temp, data, PATH, headers, conn, c)
    if ii is 0:
        headers = 1
