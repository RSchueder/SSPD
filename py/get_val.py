# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 17:22:20 2016

@author: schueder
"""

def get_val(CAS,method,property_search,DELWAQA,dat,prop_used,med,ii,filespec1,filespec2,filespec3,conv,c,conn):
    from isnum import isnum
    from make_hl_val import make_hl_val
    import numpy as np
    f1 = filespec1[(("%s")%DELWAQA)]
    f2 = filespec1[(("%s")%DELWAQA)]
    f3 = filespec1[(("%s")%DELWAQA)]
    if method[(("%s")%DELWAQA)] is 'average':

        for ss in [yy[0] for yy in property_search]:
            # for each name that the DELWAQ property may have in the database
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{pp}%'".format(qq =  CAS, pp = ss.replace("'","''")))
            dat.append(c.fetchall())
        c.execute("SELECT conversion FROM STREAM_EU_database_dictionary WHERE STREAM_EU_parameter = '{qq}'".format(qq = DELWAQA))
        convF = c.fetchall()  
        if not dat:
            val = '-9999'
        # for each word that was used in the search
        for mm in range(0,len(dat)):
            #if no entry was found with that search term
            if not dat[mm]:
                pass
            else:
                # an entry was found
                if isnum(dat[mm][0][-3]):
                    # do the associated conversion
                    ll = float(dat[mm][0][-3])*float(convF[mm][0])
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
                    # if it can be converted to a half-life
                elif float(make_hl_val(dat[mm][0][-3])) != float(-9999):
                    ll = make_hl_val(dat[mm][0][-3])
                    val = 0.6931471/(ll*3600)    
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
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

    elif method[(("%s")%DELWAQA)] is 'min':
        for ss in [yy[0] for yy in property_search]:
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{pp}% AND property LIKE '%min%'".format(qq =  CAS, pp = ss))
            dat.append(c.fetchall())
        c.execute("SELECT conversion FROM STREAM_EU_database_dictionary WHERE STREAM_EU_parameter = '{qq}'".format(qq = DELWAQA))
        convF = c.fetchall()              
        if not dat:
            val = '-9999'
        # for each word that was used in the search
        for mm in range(0,len(dat)):
            #if no entry was found with that search term
            if not dat[mm]:
                pass
            else:
                # an entry was found
                if isnum(dat[mm][0][-3]):
                    ll = float(dat[mm][0][-3])* float(convF[mm][0])
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
                elif float(make_hl_val(dat[mm][0][-3])) != float(-9999):
                    ll = make_hl_val(dat[mm][0][-3])
                    val = 0.6931471/(ll*3600)    
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
        # if it got populated, there was a number found
        if len(med) > 0:
            #take the average if there are numbers in the list
            tmp = []
            for rr in med:
                tmp.append(float(rr))
            val = min(np.array(tmp))
            #if there are no values it is -9999
        else:
            val = '-9999'                    
    elif method[(("%s")%DELWAQA)] is 'max':
        for ss in [yy[0] for yy in property_search]:
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{pp}% AND property LIKE '%max%'".format(qq =  CAS, pp = ss))
            dat.append(c.fetchall())
        c.execute("SELECT conversion FROM STREAM_EU_database_dictionary WHERE STREAM_EU_parameter = '{qq}'".format(qq = DELWAQA))
        convF = c.fetchall()             
        if not dat:
            val = '-9999'
        # for each word that was used in the search
        for mm in range(0,len(dat)):
            #if no entry was found with that search term
            if not dat[mm]:
                pass
            else:
                #an entry was found
                if isnum(dat[mm][0][-3]):
                    ll = float(dat[mm][0][-3]) * float(convF[mm][0])
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
                elif float(make_hl_val(dat[mm][0][-3])) != float(-9999):
                    ll = make_hl_val(dat[mm][0][-3])
                    val = 0.6931471/(ll*3600)
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
        # if it got populated, there was a number found
        if len(med) > 0:
            #take the average if there are numbers in the list
            tmp = []
            for rr in med:
                tmp.append(float(rr))
            val = max(np.array(tmp))
            #if there are no values it is -9999
        else:
            val = '-9999'    
    ###########################################################################
    elif method[(("%s")%DELWAQA)] is 'calculate':
        # this is specifically the air water phase change enthalpy
        # perhaps new methods needed later?
        vpType = method['pv']
        c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '{pp}'".format(qq =  CAS, pp = vpType))
        vp = c.fetchall()
        if not vp:
            val = '-9999'
        else:
            vp = float(vp[0][-3])
            # following equation taken from Estimating Enthalpy of Vaporization
            # from Vapor Pressure Using
            # Trouton’s Rule
            # units are kJ/mol, must convert to J/mol
            val = 1000*(-3.82* np.log(vp) + 70)
    ###############################################################################
    # if something specific was written, do not use the property
    # search terms
    else:
        if f1 is 'none':
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{ww}'".format(qq =  CAS, ww = method[(("%s")%DELWAQA)]))
            dat = c.fetchall()
            c.execute("SELECT conversion FROM STREAM_EU_database_dictionary WHERE STREAM_EU_parameter = '{qq}' AND substance_property = '{ss}'".format(qq = DELWAQA, ss = method[(("%s")%DELWAQA)]))
            convF = c.fetchall() 
            print(method[(("%s")%DELWAQA)])
            print(DELWAQA)
            if not dat:
                val = '-9999'
        else:
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{ww}' AND source LIKE '%{ss}%'".format(qq =  CAS, ww = method[(("%s")%DELWAQA)], ss = f1))
            dat = c.fetchall()
            c.execute("SELECT conversion FROM STREAM_EU_database_dictionary WHERE STREAM_EU_parameter = '{qq}' AND substance_property = '{ss}'".format(qq = DELWAQA, ss = method[(("%s")%DELWAQA)]))
            convF = c.fetchall()             
            if not dat:
                c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{ww}' AND source LIKE '%{ss}%'".format(qq =  CAS, ww = method[(("%s")%DELWAQA)], ss = f2))
                dat = c.fetchall()
                if not dat:
                    c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property = '{ww}' AND source LIKE '%{ss}%'".format(qq =  CAS, ww = method[(("%s")%DELWAQA)], ss = f3))
                    dat = c.fetchall()
                    if not dat:
                        val = '-9999'

        for mm in range(0,len(dat)):
            if isnum(dat[mm][-3]):
                if len(dat) == len(convF):    
                    ll = float(dat[mm][-3]) * float(convF[mm][0])
                else:
                    # this is a critical assumption that in the duplicates Stela
                    # provides the numbers do not change
                    print(dat)
                    ll = float(dat[mm][-3]) * float(convF[0][0])           
                med.append((ll))
                prop_used.append(dat[mm][-4])
            elif float(make_hl_val(dat[mm][-3])) != float(-9999):
                ll = make_hl_val(dat[mm][-3])
                ll = 0.6931471/(ll*3600)
                med.append((ll))
                prop_used.append(dat[mm][-4])
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