# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 11:31:10 2016

@author: schueder
"""
# method is a mx1 list of strings with values of 'average', 'min', 'max', or 
# some other indicator of the method you want to use for the variable you are 
# searching for
def write_output(CAS,allCAS,statind,model,method,filespec1,filespec2,filespec3,ref_temp,data,PATH,headers,conn,c):
    tot = len(allCAS)    
    from isnum import isnum
    import numpy as np    
    import os
    from make_hl_val import make_hl_val
###############################################################################    

###############################################################################    
    if model is 'DELWAQ':
        if not os.path.exists(("%s\delwaq_include_files\%s")%(PATH,CAS)):
            os.makedirs(("%s\delwaq_include_files\%s")%(PATH,CAS))
        if os.path.isfile(("%s\delwaq_include_files\%s\parameters.inc")%(PATH,CAS)):
            os.remove(("%s\delwaq_include_files\%s\parameters.inc")%(PATH,CAS))

        os.chdir(('%s\\delwaq_include_files\%s')%(PATH,CAS))
        with open(('parameters.inc'),'a') as fileID:
            tofilename = []
            tofileval = []
            fileID.write('CONSTANTS    Delho    ;default reaction enthalpy (J/mol)\n')        
            ind = 0
            dataentry = []
            tmp = []
            #search_terms = []
            c.execute("SELECT search_term FROM DELWAQ_dictionary")
            search_terms = c.fetchall()
            c.execute("SELECT conversion FROM DELWAQ_dictionary")
            conv = c.fetchall()  
            c.execute("SELECT description FROM DELWAQ_properties_def")
            description = c.fetchall()            
            c.execute("SELECT DELWAQ FROM DELWAQ_properties_def")
            cont = c.fetchall()
            search_t = []
            #get the search terms from the DELWAQ dictionary table
            for nn in range(0,len(search_terms)):
                #if something was put for the attribute
                if len(search_terms[nn][0]) > 1:
                    search_t.append(search_terms[nn][0])
                    # search_t contains all non '-' properties
            ss = 0
            
            for ii in range(3,len(search_terms)):
###############################################################################
############################EXISTS IN DATABASE#################################
###############################################################################
                if search_terms[ii][0] in search_t: 
                # If there are values for this property in the database then
                # it should be specified here in this dictionary for this check
                # to pass. If nothing is written in the dictionary entry for 
                # the DELWAQ parameter then it assumes the parameter does not
                # exist in the library and it will automatically prescribe a 
                # value of '-9999'
                    prop_used = []
                    property_search = search_t[ss]
                    ss = ss + 1
                    entry =[] 
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
###############################################################################
                    if method[ii] is 'average':
                        c.execute("SELECT * FROM properties WHERE CAS = '{qq}' AND property LIKE '%{pp}%'".format(qq =  CAS, pp = property_search))
                        dat = c.fetchall()
                        if not dat:
                            val = '-9999'
                        get_table_float(dat,med,prop_used,val)
                    elif method[ii] is 'min':
                        c.execute("SELECT * FROM properties WHERE CAS = '{qq}' AND property LIKE '%{pp}%' AND property LIKE '%min%'".format(qq =  CAS, pp = property_search))
                        dat = c.fetchall()
                        get_table_float(dat,med,prop_used,val)
                    elif method[ii] is 'max':
                        c.execute("SELECT * FROM properties WHERE CAS = '{qq}' AND property LIKE '%{pp}%' AND property LIKE '%max%'".format(qq =  CAS, pp = property_search))
                        dat = c.fetchall()
                        get_table_float(dat,med,prop_used,val)
###############################################################################
                    # if something specific was written    
                    else:
                        if filespec1[ii] is '':
                            c.execute("SELECT * FROM properties WHERE CAS = '{qq}' AND property LIKE '%{ww}%'".format(qq =  CAS, ww = method[ii]))
                            dat = c.fetchall()
                            if not dat:
                                val = '-9999'
                        else:
                            c.execute("SELECT * FROM properties WHERE CAS = '{qq}' AND property LIKE '%{ww}%' AND source LIKE '%{ss}%'".format(qq =  CAS, ww = method[ii], ss = filespec1[ii]))
                            dat = c.fetchall()
                            if not dat:
                                c.execute("SELECT * FROM properties WHERE CAS = '{qq}' AND property LIKE '%{ww}%' AND source LIKE '%{ss}%'".format(qq =  CAS, ww = method[ii], ss = filespec2[ii]))
                                dat = c.fetchall()
                                if not dat:
                                    c.execute("SELECT * FROM properties WHERE CAS = '{qq}' AND property LIKE '%{ww}%' AND source LIKE '%{ss}%'".format(qq =  CAS, ww = method[ii], ss = filespec3[ii]))
                                    dat = c.fetchall()
                                    if not dat:
                                        val = '-9999'
 
                                                for mm in range(0,len(dat)):
                            if isnum(dat[mm][-2]):
                                ll = float(dat[mm][-2])
                                med.append(str(ll))
                                prop_used.append(dat[mm][-3])
                            elif float(make_hl_val(dat[mm][-2])) != float(-9999):
                                ll = make_hl_val(dat[mm][-2])
                                med.append(str(ll))
                                prop_used.append(dat[mm][-3])
                            if len(med) > 0:
                                #take the average if there are numbers in the list
                                for rr in med:
                                    val = val + float(rr)
                                val = val/len(med)
                                #if there are no values it is -9999
                            else:
                                val = '-9999'                                       

                    if conv[ii][0][0] is '-' and val != '-9999': 
                        if len(conv[ii][0]) > 1:
                            #the value needs to be inverse
                            val = 1/(val*float(conv[ii][0][1:]))
                    else:
                        if len(conv[ii][0]) > 1:
                            if val == '-9999':
                                pass
                            else:
                                val = val*float(conv[ii][0]) 
###############################################################################
                    #this gets the metadata about the property in DELWAQ
                    c.execute("SELECT DELWAQ FROM DELWAQ_dictionary WHERE search_term = '{qq}'".format(qq = property_search))  
                    DWQA = c.fetchall()
                    print(DWQA[0])
                    # use the key
                    c.execute("SELECT * FROM DELWAQ_properties_def WHERE DELWAQ = '{qq}'".format(qq = DWQA[0][0]))
                    tmp = c.fetchall()
                    line = tmp[0]
                    line = ','.join(line)
                    line = line.split(',')
                    meta = [0,1,2,3]
                    for mm in range(len(line)):
                        if mm in meta:
                            entry.append(line[mm])
                        if mm is 0:     
                            entry.append(';')
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
                    
###############################################################################
################################REF TEMP#######################################
###############################################################################
               
               # if the parameter is a ref temp, there is no corresponding 
                # property, but we need to put a value in for delwaq        
                elif 'ref.temp' in description[ii][0]:
                    entry = []
                    entry.append('CONSTANTS')
                    val = float(ref_temp[ii])
                    c.execute("SELECT * FROM DELWAQ_properties_def WHERE description = '{qq}'".format(qq =  description[ii][0]))
                    tmp = c.fetchall()
                    line = tmp[0]
                    line = ','.join(line)
                    line = line.split(',')
                    meta = [0,1,2,3]
                    for mm in range(len(line)):
                        if mm in meta:
                            entry.append(line[mm])
                        if mm is 0:     
                            entry.append(';')
                            entry = ','.join(entry)
                            entry = entry.split(',')
                    entry.append('name of parameters used ---->')
                    for pp in prop_used:
                        entry.append(pp)
                    tofilename.append(entry[1])
                    entry = ','.join(entry)
                    entry = entry.replace(',','    ')
                    fileID.write(('%s\n') % entry)
###############################################################################                    
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
###############################################################################
########################NO DICTIONARY VALUE AVAILABLE##########################
###############################################################################
                # there is no data for this parameter in the database, so in
                # DELWAQ it will take on a value of '-9999'
                else:
                    entry = []
                    entry.append('CONSTANTS')
                    val = '-9999'
                    c.execute("SELECT * FROM DELWAQ_properties_def WHERE description = '{qq}'".format(qq =  description[ii][0]))
                    tmp = c.fetchall()
                    line = tmp[0]
                    line = ','.join(line)
                    line = line.split(',')
                    meta = [0,1,2,3]
                    for mm in range(len(line)):
                        if mm in meta:
                            entry.append(line[mm])
                        if mm is 0:     
                            entry.append(';')
                            entry = ','.join(entry)
                            entry = entry.split(',')
                    entry.append('name of parameters used ---->')
                    tofilename.append(entry[1])
                    entry = ','.join(entry)
                    entry = entry.replace(',','    ')
                    fileID.write(('%s\n') % entry)
###############################################################################                    
                    conline = []
                    conline.append('DATA')
                    if type(val) is str:
                        conline.append(val)
                    tofileval.append(val)
                    tmp = ','.join(conline) 
                    tmp = tmp.replace(',','    ')
                    dataentry.append(tmp)            
            ind = 0  
            fileID.write('DATA    30000\n') 
            for ii in range(len(dataentry)):     
                fileID.write(('%s\n') % dataentry[ind])
                ind = ind + 1
###############################################################################
            tofilename.insert(0,'CAS')
            tofileval.insert(0,CAS)
  
            os.chdir(('%s\\delwaq_include_files\overall')%(PATH))
            with open(('overall.txt'),'a') as overallFile:
                if headers is 0:
                    tofilename = ','.join(tofilename)
                    overallFile.write(('%s\n')% tofilename)
                for ii in range(0,len(tofileval)):
                    tofileval[ii] = str(tofileval[ii])
                tofileval = ','.join(tofileval)
                overallFile.write(('%s\n')% tofileval)
            print(('substance %i/%i written')%(statind, tot))
            


            

        
    