# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 17:22:20 2016

@author: schueder
"""

def get_val(val,CAS,method,property_search,dat,prop_used,med,ii,filespec1,filespec2,filespec3,conv,c,conn):
    from isnum import isnum
    from make_hl_val import make_hl_val
    if method[ii] is 'average':
        for ss in [yy[0] for yy in property_search]:
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{pp}%'".format(qq =  CAS, pp = ss.replace("'","''")))
            dat.append(c.fetchall())
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
                    ll = float(dat[mm][0][-3])
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
                elif float(make_hl_val(dat[mm][0][-3])) != float(-9999):
                    ll = make_hl_val(dat[mm][0][-3])
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
        # if it got populated, there was a number found
        if len(med) > 0:
            #take the average if there are numbers in the list
            for rr in med:
                val = val + float(rr)
            val = val/len(med)
            #if there are no values it is -9999
        else:
            val = '-9999'

    elif method[ii] is 'min':
        for ss in [yy[0] for yy in property_search]:
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{pp}% AND property LIKE '%min%'".format(qq =  CAS, pp = ss))
            dat.append(c.fetchall())
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
                    ll = float(dat[mm][0][-3])
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
                elif float(make_hl_val(dat[mm][0][-3])) != float(-9999):
                    ll = make_hl_val(dat[mm][0][-3])
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
        # if it got populated, there was a number found
        if len(med) > 0:
            #take the average if there are numbers in the list
            for rr in med:
                val = val + float(rr)
            val = val/len(med)
            #if there are no values it is -9999
        else:
            val = '-9999'                    
    elif method[ii] is 'max':
        for ss in [yy[0] for yy in property_search]:
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{pp}% AND property LIKE '%max%'".format(qq =  CAS, pp = ss))
            dat.append(c.fetchall())
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
                    ll = float(dat[mm][0][-3])
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
                elif float(make_hl_val(dat[mm][0][-3])) != float(-9999):
                    ll = make_hl_val(dat[mm][0][-3])
                    med.append(str(ll))
                    prop_used.append(dat[mm][0][-4])
        # if it got populated, there was a number found
        if len(med) > 0:
            #take the average if there are numbers in the list
            for rr in med:
                val = val + float(rr)
            val = val/len(med)
            #if there are no values it is -9999
        else:
            val = '-9999'                    
    ###############################################################################
    # if something specific was written, do not use the property
    # search terms
    else:
        if filespec1[ii] is '':
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{ww}%'".format(qq =  CAS, ww = method[ii]))
            dat = c.fetchall()
            if not dat:
                val = '-9999'
        else:
            c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{ww}%' AND source LIKE '%{ss}%'".format(qq =  CAS, ww = method[ii], ss = filespec1[ii]))
            dat = c.fetchall()
            if not dat:
                c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{ww}%' AND source LIKE '%{ss}%'".format(qq =  CAS, ww = method[ii], ss = filespec2[ii]))
                dat = c.fetchall()
                if not dat:
                    c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}' AND property LIKE '%{ww}%' AND source LIKE '%{ss}%'".format(qq =  CAS, ww = method[ii], ss = filespec3[ii]))
                    dat = c.fetchall()
                    if not dat:
                        val = '-9999'
        for mm in range(0,len(dat)):
            if isnum(dat[mm][-3]):
                ll = float(dat[mm][-3])
                med.append(str(ll))
                prop_used.append(dat[mm][-4])
            elif float(make_hl_val(dat[mm][-3])) != float(-9999):
                ll = make_hl_val(dat[mm][-3])
                med.append(str(ll))
                prop_used.append(dat[mm][-4])
        if len(med) > 0:
            #take the average if there are numbers in the list
            for rr in med:
                val = val + float(rr)
            val = val/len(med)
            #if there are no values it is -9999
        else:
            val = '-9999'
    #recall that conv is a tuple within a list
    if conv[0][0][0] is '-' and val != '-9999': 
        if len(conv[0][0]) > 1:
            #the value needs to be inverse
            val = 0.6931471/(val*float(conv[0][0][1:]))
    else:
        if len(conv[0][0]) > 1:
            if val == '-9999':
                pass
            else:
                val = val*float(conv[0][0])     
    return val