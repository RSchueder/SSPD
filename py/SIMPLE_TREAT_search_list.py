# -*- coding: utf-8 -*-
"""
Created on Feb 28 2017

@author: schueder
"""

def SIMPLE_TREAT_search_list(abrev,paramReq):
    # REMEMBER THAT IN PYTHON THE FIRST INDEX IS '0' AND THE SECOND IS '1'
    method = {}

    for ii in paramReq:
        method[(("%s")% ii[0])] = 'median'

#    method['Melting Point'] = 'Tm'
#    method['Vapor pressure'] = 'Vp'
#    method['Water solubility'] = 'Sw'
#    method['pka1'] = 'pKa1'
#    method['pka2'] = 'pKa2'
#    method['pkb1'] = 'pKb1'
#    method['pkb2'] = 'pKb2'
#    method['Degredation rate in sediment'] = 'HL in sediment'
#    method['Degredation rate in soil'] = 'HL in soil'
#    method['Degredation rate in water'] = 'HL in water'
#    method['log Kow'] = 'log Kow'

   
    # (OPTIONAL) SPECIFY THE MODEL SPECIFIER AT THIS LOCATION, IF THERE ARE
    # MULTIPLE VALUES OF SAME NAME BUT FROM DIFFERENT MODELS
    modelspec1 = {}
    modelspec2 = {}
    modelspec3 = {}
    
    for ii in paramReq:
        modelspec1[(("%s")% ii[0])] = 'none'
#    modelspec1['log Kow'] = 'KOWWIN 1.68'
#    modelspec1['Melting Point'] = 'MPBPWIN v1.43: Mean Joback,Gold and Ogle method'
#    modelspec1['Water solubility'] = 'Kühne R, Ebert R-U, Schüürmann G 2006. Model selection based on structural similarity – method description and application to water solubility prediction. J. Chem. Inf. Model. 46: 636-641.'
#    modelspec1['Vapor pressure'] = 'MPBPWIN v1.43: Grain modified Antoine model and Mackay model'

    for ii in paramReq:
        modelspec2[(("%s")% ii[0])] = 'none'

    
    
    for ii in paramReq:
        modelspec3[(("%s")% ii[0])] = 'none'

    ref_temp = [25] * len(abrev)
    
    return method, modelspec1, modelspec2, modelspec3, ref_temp