# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 11:31:10 2016

@author: schueder
"""
# method is a mx1 list of strings with values of 'average', 'min', 'max', or 
# some other indicator of the method you want to use for the variable you are 
# searching for
def write_STREAM_EU_output(CAS,allCAS,statind,model,method,filespec1,filespec2,filespec3,ref_temp,data,PATH,headers,conn,c):
    tot = len(allCAS)    
    from isnum import isnum
    import numpy as np    
    import os
    import math
    from make_hl_val import make_hl_val
    from get_val import get_val
###############################################################################    

###############################################################################    
    if model is 'STREAM_EU':
        if not os.path.exists(("%s\stream_eu_include_files\%s")%(PATH,CAS)):
            os.makedirs(("%s\stream_eu_include_files\%s")%(PATH,CAS))
        if os.path.isfile(("%s\stream_eu_include_files\%s\parameters.inc")%(PATH,CAS)):
            os.remove(("%s\stream_eu_include_files\%s\parameters.inc")%(PATH,CAS))

        os.chdir(('%s\\stream_eu_include_files\%s')%(PATH,CAS))
        with open(('parameters.inc'),'a') as fileID:
            tofilename = []
            tofileval = []
            ind = 0
            dataentry = []
            tmp = []
            
            # DELWAQA = delwaq all parameters
            # DELWAQC = delwaq parameters confirmed in database
            c.execute("SELECT STREAM_EU_parameter FROM STREAM_EU_meta")
            DELWAQA = c.fetchall()
            c.execute("SELECT STREAM_EU_parameter FROM STREAM_EU_database_dictionary")
            DELWAQC = c.fetchall()
            
            search_t = []

            # get the search terms from the DELWAQ dictionary v2 table
            # compare to all of the known paramters to identify known and unknown
            for nn in range(0,len(DELWAQA)):
                #if there is a corresponding property in the database
                if DELWAQA[nn][0] in [lp[0] for lp in DELWAQC]:
                    search_t.append(DELWAQA[nn][0])
                    # search_t contains all parameters present in the database
            for ii in range(0,len(DELWAQA)): #skip CAS, Name, Smiles
                c.execute("SELECT description FROM STREAM_EU_meta WHERE STREAM_EU_parameter = '{qq}'".format(qq = DELWAQA[ii][0]))
                description = c.fetchall()               
                entry = []
                check  = DELWAQA[ii][0]
                
                if 'Name' in check or 'CAS' in check or 'SMILES' in check:
                    print('break found')
            
###############################################################################
############################EXISTS IN DATABASE#################################
###############################################################################                
                elif DELWAQA[ii][0] in search_t: #check if it is in the dictionary
                # If there are values for this property in the database then
                # it should be specified here in this dictionary for this check
                # to pass. If nothing is written in the dictionary entry for 
                # the DELWAQ parameter then it assumes the parameter does not
                # exist in the library and it will automatically prescribe a 
                # value of '-9999'
                    prop_used = []
                    #obtain the search queries that tie this parameter to
                    #properties in the database
                    c.execute("SELECT substance_property FROM STREAM_EU_database_dictionary WHERE STREAM_EU_parameter = '{qq}'".format(qq = DELWAQA[ii][0]))
                    property_search = c.fetchall()
                    c.execute("SELECT conversion FROM STREAM_EU_database_dictionary WHERE STREAM_EU_parameter = '{qq}'".format(qq = DELWAQA[ii][0]))
                    conv = c.fetchall()
                    entry.append('CONSTANTS')
                    # now we need to find the property types in the properties 
                    # table, and there will be different cases depending on the 
                    # desired methods
                    # methods:
                    #1. average
                    #2. min
                    #3. max
                    #4. specific (with list)
                    val = float(0)
                    med = []
                    dat = []
###############################################################################
##############################GET VAL##########################################
                    
                    val = get_val(val,CAS,method,property_search,dat,prop_used,med,ii,filespec1,filespec2,filespec3,conv,c,conn)
                    
###############################################################################
#############################END GET VAL, VALUE KNOWN##########################      
###############################################################################
                    #this gets the metadata about the property in DELWAQ, and
                    #again this is a parameter for which some database value is
                    #available for some substances according to the dictionary
                                
                    conline = []
                    conline.append('DATA')
                    if type(val) is float:
                        conline.append(str(val))
                    if type(val) is np.float64:
                        conline.append(str(val)) 
                    if type(val) is list:
                        conline.append(str(val[0]))
                    if type(val) is str:
                        conline.append(val)
                    tofileval.append(val)
                    tmp = ','.join(conline) 
                    tmp = tmp.replace(',','    ')
                    dataentry.append(tmp)
                    tmpV = tmp
                    
                    c.execute("SELECT * FROM STREAM_EU_meta WHERE STREAM_EU_parameter = '{qq}'".format(qq = DELWAQA[ii][0]))
                    tmp = c.fetchall() #tmp is the metadata for this parameter
                    line = tmp[0]
                    line = ','.join(line)
                    line = line.split(',')
                    meta = [0,1,2,3] # we only want the first 4 meta components to be put in the file
                    for mm in range(len(line)):
                        if mm in meta:
                            entry.append(line[mm])
                        if mm is 0:
                            entry.append(tmpV)
                            entry.append(';')
                        if mm is 1:
                            entry = ','.join(entry)
                            entry = entry.split(',')
                    entry.append('name of parameters used ---->')
                    if len(prop_used) > 0:                    
                        for pp in prop_used:
                            entry.append(pp)
                    
                    tofilename.append(entry[1])
                    entry = ','.join(entry)
                    entry = entry.replace(',','    ')
                    fileID.write(('%s\n') % entry)
                    
###############################################################################                    

                    
###############################################################################
################################REF TEMP#######################################
###############################################################################
               
               # if the parameter is a ref temp, there is no corresponding 
                # property, but we need to put a value in for delwaq        
                elif 'ref.temp' in description[0][0]:                   
                    conline = []
                    conline.append('DATA')
                    val = float(ref_temp[ii])
                    if type(val) is float:
                        conline.append(str(val))
                    if type(val) is np.float64:
                        conline.append(str(val)) 
                    if type(val) is list:
                        conline.append(str(val[0]))
                    if type(val) is str:
                        conline.append(val)
                    tofileval.append(val)
                    tmp = ','.join(conline) 
                    tmp = tmp.replace(',','    ')
                    dataentry.append(tmp)
                    tmpV = tmp
                    
                    entry = []
                    entry.append('CONSTANTS')
                    c.execute("SELECT * FROM STREAM_EU_meta WHERE description = '{qq}'".format(qq =  description[0][0]))
                    tmp = c.fetchall()
                    line = tmp[0]
                    line = ','.join(line)
                    line = line.split(',')
                    meta = [0,1,2,3]
                    for mm in range(len(line)):
                        if mm in meta:
                            entry.append(line[mm])
                        if mm is 0:
                            entry.append(tmpV)
                            entry.append(';')
                        if mm is 1:
                            entry = ','.join(entry)
                            entry = entry.split(',')
                    entry.append('name of parameters used ---->')
                    tofilename.append(entry[1])
                    entry = ','.join(entry)
                    entry = entry.replace(',','    ')
                    fileID.write(('%s\n') % entry)
###############################################################################                    

###############################################################################
########################NO DICTIONARY VALUE AVAILABLE##########################
###############################################################################
                # there is no data for this parameter in the database, so in
                # DELWAQ it will take on a value of '-9999'
                else:
                    entry = []
                    entry.append('CONSTANTS')
                    val = '-9999'
                    conline = []
                    conline.append('DATA')
                    if type(val) is str:
                        conline.append(val)
                    tofileval.append(val)
                    tmp = ','.join(conline) 
                    tmp = tmp.replace(',','    ')
                    dataentry.append(tmp)
                    tmpV = tmp 


                    c.execute("SELECT * FROM STREAM_EU_meta WHERE description = '{qq}'".format(qq =  description[0][0]))
                    tmp = c.fetchall()
                    line = tmp[0]
                    line = ','.join(line)
                    line = line.split(',')
                    meta = [0,1,2,3]
                    for mm in range(len(line)):
                        if mm in meta:
                            entry.append(line[mm])
                        if mm is 0:
                            entry.append(tmpV)
                            entry.append(';')
                        if mm is 1:
                            entry = ','.join(entry)
                            entry = entry.split(',')
                    entry.append('name of parameters used ---->')
                    tofilename.append(entry[1])
                    entry = ','.join(entry)
                    entry = entry.replace(',','    ')
                    fileID.write(('%s\n') % entry)
###############################################################################                    

            fileID.write('CONSTANTS Delho  DATA    30000') 
###############################################################################
            tofilename.insert(0,'CAS')
            tofileval.insert(0,CAS)
  
            os.chdir(('%s\\properties_table\overall')%(PATH))

            with open(('overall.txt'),'a') as overallFile:
                if headers is 0:
                    tofilename = ','.join(tofilename)
                    overallFile.write(('%s\n')% tofilename)
                for ii in range(0,len(tofileval)):
                    tofileval[ii] = str(tofileval[ii])
                tofileval = ','.join(tofileval)
                overallFile.write(('%s\n')% tofileval)
            print(('substance %i/%i written')%(statind, tot))