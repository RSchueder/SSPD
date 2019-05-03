# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 17:22:20 2016

@author: schueder
"""

def get_val_STREAM_EU(CAS,method,property_search,DELWAQA,dat,prop_used,med,ii,modelspec1,modelspec2,modelspec3,conv,c,conn):
    from isnum import isnum
    from make_hl_val import make_hl_val
    import numpy as np
    f1 = modelspec1[(("%s")%DELWAQA)]
    f2 = modelspec2[(("%s")%DELWAQA)]
    f3 = modelspec3[(("%s")%DELWAQA)]
    convF = []
    arith = []  
    model = []
    if method[(("%s")%DELWAQA)] is 'average':
        for ss in [yy[0] for yy in property_search]:
            # for each name that the DELWAQ property may have in the database
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{pp}'".format(qq =  CAS, pp = ss.replace("'","''")))
            dat.append(c.fetchall())
            c.execute("SELECT conversion FROM STREAM_EU_database_dictionary WHERE substance_property = '{qq}'".format(qq = ss.replace("'","''")))
            convF.append(c.fetchall())
            c.execute("SELECT method FROM STREAM_EU_database_dictionary WHERE substance_property = '{qq}'".format(qq = ss.replace("'","''")))
            arith.append(c.fetchall())
        if not dat:
            val = '-9999'
        # for each word that was used in the search
        # mm counts the number of hits
        # extra layer [0] because it contains multiple hits, and is a list in a list
        for mm in range(0,len(dat)):
            #if no entry was found with that search term
            if not dat[mm]:
                pass
            else:
                convS = convF[mm][0][0]
                # an entry was found
                if isnum(dat[mm][0][3]):
                    if convS == '-3600':
                        ll = float(dat[mm][0][3])
                        ll = 0.6931471/(ll*3600)    
                    else:
                        if arith[0][0][0] == 'MD':
                            ll = float(dat[mm][0][3])*float(convS)
                        else:
                            ll = float(dat[mm][0][3])+float(convS)            
                elif float(make_hl_val(dat[mm][0][3])) != float(-9999):
                    ll = make_hl_val(dat[mm][0][3])
                    ll = 0.6931471/(ll*3600)    
                med.append(str(ll))
                print(dat[mm][0][2])
                prop_used.append(dat[mm][0][2])
                model.append(dat[mm][0][5])
        # if it got populated, there was a number found
        if len(med) > 0:
            #take the average if there are numbers in the list
            val = float(0)
            for rr in med:
                val = val + float(rr)
            val = val/len(med)
            #if there are no values it is -9999
        else:
            val = '-9999'

    ###############################################################################
    # deleted min, max, and calculate methods
    ###############################################################################
    # if something specific was written, do not use the property
    # search terms
    else:
        # no file/model spec
        if f1 is 'none':
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{ww}'".format(qq =  CAS, ww = method[(("%s")%DELWAQA)]))
            dat = c.fetchall()            
            c.execute("SELECT conversion FROM STREAM_EU_database_dictionary WHERE STREAM_EU_parameter = '{qq}' AND substance_property = '{ss}'".format(qq = DELWAQA, ss = method[(("%s")%DELWAQA)]))
            convF = c.fetchall() 
            c.execute("SELECT method FROM STREAM_EU_database_dictionary WHERE substance_property = '{qq}'".format(qq = method[(("%s")%DELWAQA)]))
            arith = c.fetchall()
            if not dat:
                val = '-9999'
        # model spec
        else:
            
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{ww}' AND model LIKE '%{ss}%'".format(qq =  CAS, ww = method[(("%s")%DELWAQA)], ss = f1))
            dat = c.fetchall()
            c.execute("SELECT conversion FROM STREAM_EU_database_dictionary WHERE STREAM_EU_parameter = '{qq}' AND substance_property = '{ss}'".format(qq = DELWAQA, ss = method[(("%s")%DELWAQA)]))
            convF = c.fetchall()             
            c.execute("SELECT method FROM STREAM_EU_database_dictionary WHERE substance_property = '{qq}'".format(qq = method[(("%s")%DELWAQA)]))
            arith = c.fetchall()
            if not dat:
                c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{ww}' AND model LIKE '%{ss}%'".format(qq =  CAS, ww = method[(("%s")%DELWAQA)], ss = f2))
                dat = c.fetchall()
                if not dat:
                    c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{ww}' AND model LIKE '%{ss}%'".format(qq =  CAS, ww = method[(("%s")%DELWAQA)], ss = f3))
                    dat = c.fetchall()
                    if not dat:
                        val = '-9999'
        # for each word that was used in the search
        # mm counts the number of hits
        for mm in range(0,len(dat)):
            if isnum(dat[mm][3]):
                # if there are not more hits than there are conversions
                # assume there are either the same number, or there is only 1
                if len(dat) == len(convF):   
                    convS = convF[mm][0]
                else:
                    convS = convF[0][0]
                    
                if convS == '-3600':
                    try:
                        ll = float(dat[mm][3])
                    except(TypeError):
                        ll = float(dat[mm][3])    
                    ll = 0.6931471/(ll*3600)    
                else:
                    if arith[0][0] == 'MD':
                        ll = float(dat[mm][3])*float(convS)
                    elif arith[0][0] == 'AS':
                        ll = float(dat[mm][3])+float(convS)
                    elif arith[0][0] == 'MWC':
                       c.execute("SELECT value FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{pp}%'".format(qq =  CAS, pp = 'Molar mass [Da]'))
                       # MWC values are in mg/L (SW, not Ks)                            
                       # convert to mmol/L from mg/L                            
                       MW = c.fetchall()
                       print(convS)
                       ll = (float(dat[mm][3])/MW[0]) * float(convS)
                       # now convert from mmol/L is equivalent to mol/m3  
                       # for MD type solubilities, the mol/L value is * 1000 to
                       # get to mol/m3                         
                   
#                else:
#                    # this is a critical assumption that in the duplicates Stela
#                    # provides the units do not change
#                    ll = float(dat[mm][3]) * float(convF[0][0][0])     
#                    print(('more than one match found for property %s using preferred method %s') % (DELWAQA,method[(("%s")%DELWAQA)]))
#                    print('\n try to specify an exact string match or specify the exact file via modelspec1-3')
                med.append((ll))
                prop_used.append(dat[mm][5])
            elif float(make_hl_val(dat[mm][3])) != float(-9999):
                ll = make_hl_val(dat[mm][3])
                ll = 0.6931471/(ll*3600)
                med.append((ll))
                prop_used.append(dat[mm][5])
        if len(med) > 0:
            #take the average if there are numbers in the list
            val = float(0)
            for rr in med:
                val = val + float(rr)
            val = val/len(med)
            #if there are no values it is -9999
        else:
            val = '-9999'
 
    return val