# -*- coding: utf-8 -*-
"""
Created on Feb 28 2017

@author: schueder
"""

def SIMPLE_TREAT_search_list(abrev,paramReq):
    # REMEMBER THAT IN PYTHON THE FIRST INDEX IS '0' AND THE SECOND IS '1'
    method = {}

    for ii in paramReq:
        method[(("%s")% ii[0])] = 'average'

    method['Melting Point'] = 'Mean Melting Point'
    method['Vapor pressure'] = 'Vapor Pressure (Antoine Method)'
    method['Water solubility'] = 'Water Solubility'
    method['pka1'] = 'pka1'
    method['pka2'] = 'pka2'
    method['pkb1'] = 'pka1'
    method['pkb2'] = 'pka2'
    method['Degradation rate in sediment'] = 'Ultimate Half Life Predicted'
    method['Degradation rate in soil'] = 'Ultimate Half Life Predicted'
    method['Degradation rate in water'] = 'Ultimate Half Life Predicted'
    method['log Kow'] = 'log Kow'
    method['Koc'] = 'Koc (MCI)'

    # (OPTIONAL) SPECIFY THE FILE SPECIFIER AT THIS LOCATION, IF THERE ARE
    # MULTIPLE VALUES OF SAME NAME BUT FROM DIFFERENT FILES
    filespec1 = {}
    filespec2 = {}
    filespec3 = {}
    
    for ii in paramReq:
        filespec1[(("%s")% ii[0])] = 'none'
    # filespec1['kde'] = '301B'


    for ii in paramReq:
        filespec2[(("%s")% ii[0])] = 'none'
    # filespec2['kde'] = '301C'

    
    
    for ii in paramReq:
        filespec3[(("%s")% ii[0])] = 'none'
    # filespec3['kde'] = '301_F'

    ref_temp = [25] * len(abrev)
    
    return method, filespec1, filespec2, filespec3, ref_temp