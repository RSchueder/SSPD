# -*- coding: utf-8 -*-
"""
Created on Tues Feb 28 09:30:36 2017

@author: schueder

this script was written to de-couple any database querying or writing from the
creation of the database itself
"""

import os
import glob
import csv
import sqlite3
from dynamic_entry import dynamic_entry
from create_table import create_table
from read_from_db import read_from_db
from read_csv import read_csv
from write_SIMPLE_TREAT_output import write_SIMPLE_TREAT_output
from save_auto_table import save_auto_table
from make_hl_val import make_hl_val
from get_val import get_val
from SIMPLE_TREAT_search_list import SIMPLE_TREAT_search_list
from datetime import datetime
from read_csv2array import read_csv2array
import pandas as pd
from read_csv2dict import read_csv2dict

os.chdir('../')
PATH = os.getcwd()
if os.path.isfile(("%s\simple_treat_include_files\STdataFromDatabase.txt")%(PATH)):
    os.remove(("%s\simple_treat_include_files\STdataFromDatabase.txt")%(PATH))
if not os.path.exists(("%s\simple_treat_include_files")%(PATH)):
    os.makedirs(("%s\simple_treat_include_files")%(PATH))

try:
    c.close()
    conn.close()
except:
    pass
conn = sqlite3.connect('substance_properties.db')
c = conn.cursor()
model = 'SIMPLE_TREAT'

c.execute("SELECT SIMPLE_TREAT_parameter FROM SIMPLE_TREAT_meta")
paramReq = c.fetchall()
c.execute("SELECT SIMPLE_TREAT_parameter FROM SIMPLE_TREAT_database_dictionary")
paramPos = c.fetchall()

search_t = []
for nn in range(0, len(paramReq)):
    # if there is a corresponding property in the database
    if paramReq[nn][0] in [lp[0] for lp in paramPos]:
        search_t.append(paramReq[nn][0])
        # search_t contains all parameters present in the database
        # these are those we are going to loop through

defaultCAS = 1
if defaultCAS == 1:
    c.execute("SELECT CAS FROM substances where CAS IS NOT NULL AND TRIM(CAS)")
    allCAS = c.fetchall()
    allCAS = list(allCAS)
    allCAS = set(allCAS)
    allCAS = list(allCAS)
###############################################################################
# MUST SPECIFY METHOD IN search_list.py IF YOU DO NOT WISH TO USE THE
# DEFAULT SEARCH TERMS

method, filespec1, filespec2, filespec3, ref_temp = SIMPLE_TREAT_search_list(paramReq, paramReq)
headers = 0

for ii in range(0, len(allCAS)):
    if defaultCAS == 1:
        CASreq = allCAS[ii][0]
    else:
        CASreq = allCAS[ii]

    ###############################################################################
    data = read_from_db(CASreq, conn, c)
    write_SIMPLE_TREAT_output(CASreq, allCAS, paramReq, paramPos, search_t, ii, model, method, filespec1, filespec2,
                           filespec3, ref_temp, data, PATH, headers, conn, c)
    if ii is 0:
        headers = 1
