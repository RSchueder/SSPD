# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 17:22:20 2016

@author: schueder
"""

def get_val_SIMPLE_TREAT(CAS,method,property_search,DELWAQA,dat,prop_used,model_used,med,ii,modelspec1,modelspec2,modelspec3,conv,c,conn):
    from isnum import isnum
    from make_hl_val import make_hl_val
    import numpy as np
    f1 = modelspec1[(("%s")%DELWAQA)]
    f2 = modelspec2[(("%s")%DELWAQA)]
    f3 = modelspec3[(("%s")%DELWAQA)]
    convF = []
    arith = []  
  
    if method[(("%s")%DELWAQA)] is 'median':
        for ss in [yy[0] for yy in property_search]:
            # for each name that the DELWAQ property may have in the database
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{pp}%'".format(qq =  CAS, pp = ss.replace("'","''")))
            dat.append(c.fetchall())
            c.execute("SELECT conversion FROM SIMPLE_TREAT_database_dictionary WHERE SIMPLE_TREAT_parameter = '{qq}' AND substance_property LIKE '%{pp}%'".format(qq = DELWAQA, pp = ss.replace("'","''")))
            convF.append(c.fetchall()) 
            c.execute("SELECT method FROM SIMPLE_TREAT_database_dictionary WHERE substance_property = '{qq}'".format(qq = ss.replace("'","''")))
            arith.append(c.fetchall())
        # list within a list for some reason...

            #Regardless of number of hits, we need there to be a list of lists
            #[unique name hit index][non unique hits][tuple index][position index]
        if not dat:
            val = '-9999'
        # for each word that was used in the search
        # mm counts the number of hits
        for mm in range(0,len(dat)):
            for nn in range(0,len(dat[mm])):
                #if no entry was found with that search term
                if not dat[mm][nn]:
                    pass
                else:   
            # there might be one conversion that is shared by multiple properties
            # that share the same name but are computed by different models
                    try:
                        convS = convF[mm][0][0]
                    except:
                        convS = convF[0][0][0]
                        # an entry was found
                   
                    if isnum(dat[mm][nn][3]):
                        if convS == '-3600':
                            ll = float(dat[mm][nn][3])
                            ll = 0.6931471/(ll*3600)    
                        else:
                            if arith[mm][0][0] == 'MD':
                                ll = float(dat[mm][nn][3])*float(convS)
                            elif arith[mm][0][0] == 'AS':
                                ll = float(dat[mm][nn][0][3])+float(convS)
                            elif arith[mm][0][0] == 'MWC':                             
                                c.execute("SELECT value FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{pp}%'".format(qq =  CAS, pp = 'Molar mass [Da]'))
                                # MWC values are in mg/L (SW, not Ks)                            
                                # convert to mmol/L from mg/L                            
                                MW = c.fetchall()
                                ll = (float(dat[mm][nn][3])/float(MW[0][0])) * float(convS)
                        med.append(str(ll))
                        prop_used.append(dat[mm][nn][2])
                        model_used.append(dat[mm][nn][5])
                    elif float(make_hl_val(dat[mm][nn][3])) != float(-9999):
                        ll = make_hl_val(dat[mm][nn][3])
                        ll = 0.6931471/(ll*3600)    
                        med.append(str(ll))
                        prop_used.append(dat[mm][nn][2])
                        model_used.append(dat[mm][nn][5])
                    else:
                        pass

        # if it got populated, there was a number found
        #print(DELWAQA)
        #print(med)
        if len(med) > 0: 
            #take the median if there are numbers in the list
            val = []
            for rr in med:
                if float(rr) != 0:
                    val.append(float(rr))
            val = np.median(val)
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
            c.execute("SELECT conversion FROM SIMPLE_TREAT_database_dictionary WHERE SIMPLE_TREAT_parameter = '{qq}' AND substance_property = '{ss}'".format(qq = DELWAQA, ss = method[(("%s")%DELWAQA)]))
            convF = c.fetchall()
            c.execute("SELECT method FROM SIMPLE_TREAT_database_dictionary WHERE substance_property = '{qq}'".format(qq = method[(("%s")%DELWAQA)]))
            arith = c.fetchall()
            if not dat:
                val = '-9999'
        # model spec
        else:
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{ww}' AND model LIKE '%{ss}%'".format(qq =  CAS, ww = method[(("%s")%DELWAQA)], ss = f1))
            dat = c.fetchall()
            c.execute("SELECT conversion FROM SIMPLE_TREAT_database_dictionary WHERE SIMPLE_TREAT_parameter = '{qq}' AND substance_property = '{ss}'".format(qq = DELWAQA, ss = method[(("%s")%DELWAQA)]))
            convF = c.fetchall()         
            c.execute("SELECT method FROM SIMPLE_TREAT_database_dictionary WHERE substance_property = '{qq}'".format(qq = method[(("%s")%DELWAQA)]))
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
        # structure here is dat[mm]3[] and not dat[mm][0][3] because
        # we need there to only be one hit to the query
        for mm in range(0,len(dat)):
            if isnum(dat[mm][3]):                                                                      
                # if there are not more hits than there are conversions
                # assume there are either the same number, or there is only 1
                if len(dat) == len(convF):   
                    convS = convF[mm][0]
                else:
                    convS = convF[0][0]
                if convS == '-3600':
                    ll = float(dat[mm][3])
                    ll = 0.6931471/(ll*3600)    
                else:
                    if arith[0][0] == 'MD':
                        ll = float(dat[mm][3])*float(convS)
                    else:
                        ll = float(dat[mm][3])+float(convS)
                med.append((ll))
                prop_used.append(dat[mm][2])
                model_used.append(dat[mm][5])
            elif float(make_hl_val(dat[mm][3])) != float(-9999):
                ll = make_hl_val(dat[mm][3])
                ll = 0.6931471/(ll*3600)
                med.append((ll))
                prop_used.append(dat[mm][2])
                model_used.append(dat[mm][5])

        if len(med) > 0:
            #take the average if there are numbers in the list
            val = float(0)
            for rr in med:
                val = val + float(rr)
            val = val/len(med)
            #if there are no values it is -9999
        else:
            val = '-9999'

    # recall that conv is a tuple within a list
    # this does not work because it assumes all versions of the substance have the
    # same conversion
    #if conv[0][0][0] is '-' and val != '-9999':
    #    if len(conv[0][0]) > 1:
    #        #the value needs to be inverse
    #        val = 0.6931471/(val*float(conv[0][0][1:]))
    #else:
    #    if len(conv[0][0]) > 1:
    #        if val == '-9999':
    #            pass
    #        else:
    #            val = val*float(conv[0][0])     
    return val