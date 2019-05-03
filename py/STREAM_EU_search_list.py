# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:51:23 2016

@author: schueder
"""


def STREAM_EU_search_list(abrev,DELWAQA):
    # REMEMBER THAT IN PYTHON THE FIRST INDEX IS '0' AND THER SECOND IS '1'
    method = {}
    # unit conversions using Stream EU database dictionary do not work if method
    # is not a specific string
    for ii in DELWAQA:
        method[(("%s")% ii[0])] = 'average'
    method['MolMass'] = 'Molar mass [Da]'
    method['mp'] = 'Tm'
    method['pv'] = 'Pv'
    method['ks'] = 'Sw'
    method['bp'] = 'Tb'
    method['kde'] = 'HL in soil'
    method['kds'] = 'HL in sediment'
    method['kdw'] = 'HL in water'
    method['kow0'] = 'log Kow'
    method['kaw0'] = 'log Kaw'
    method['kac'] = 'Acidic hydr. HL at pH 7'
    method['kba'] = 'Basic hydr. HL at pH 7'
    method['kn'] = 'Neutral hydr. HL'

    # (OPTIONAL) SPECIFY THE FILE SPECIFIER AT THIS LOCATION, IF THERE ARE
    # MULTIPLE VALUES OF SAME NAME BUT FROM DIFFERENT FILES
    modelspec1 = {}
    modelspec2 = {}
    modelspec3 = {}
    
    for ii in DELWAQA:
        modelspec1[(("%s")% ii[0])] = 'none'
    
    for ii in DELWAQA:
        modelspec2[(("%s")% ii[0])] = 'none'

    for ii in DELWAQA:
        modelspec3[(("%s")% ii[0])] = 'none'

    ref_temp = [25] * len(abrev)
    
    return method, modelspec1, modelspec2, modelspec3, ref_temp