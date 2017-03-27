# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:51:23 2016

@author: schueder
"""


def STREAM_EU_search_list(abrev,DELWAQA):
    # REMEMBER THAT IN PYTHON THE FIRST INDEX IS '0' AND THER SECOND IS '1'
    # TEST
    method = {}

    for ii in DELWAQA:
        method[(("%s")% ii[0])] = 'average'

    method['mp'] = 'Mean melting point'
    method['pv'] = 'Vapor Pressure (Antoine Method)'
    method['ks'] = 'Water solubility'
    method['pka1'] = 'pka1'
    method['pka2'] = 'pka2'
    method['kde'] = 'Ultimate Half Life Predicted'
    method['kds'] = 'Ultimate Half Life Predicted'
    method['kdw'] = 'Ultimate Half Life Predicted'
    method['kow0'] = 'log Kow'

    # (OPTIONAL) SPECIFY THE FILE SPECIFIER AT THIS LOCATION, IF THERE ARE
    # MULTIPLE VALUES OF SAME NAME BUT FROM DIFFERENT FILES
    filespec1 = {}
    filespec2 = {}
    filespec3 = {}
    
    for ii in DELWAQA:
        filespec1[(("%s")% ii[0])] = 'none'
    filespec1['kde'] = '301B'
    filespec1['kds'] = '301B'
    filespec1['kdw'] = '301B'
    filespec1['kow0'] = 'KOWWIN'

    for ii in DELWAQA:
        filespec2[(("%s")% ii[0])] = 'none'
    filespec2['kde'] = '301C'
    filespec2['kds'] = '301C'
    filespec2['kdw'] = '301C'
    filespec2['kow0'] = 'KOWWIN'
    
    
    for ii in DELWAQA:
        filespec3[(("%s")% ii[0])] = 'none'
    filespec3['kde'] = '301_F'
    filespec3['kds'] = '301_F'
    filespec3['kdw'] = '301_F'
    filespec3['kow0'] = 'KOWWIN'

    ref_temp = [25] * len(abrev)
    
    return method, filespec1, filespec2, filespec3, ref_temp