# -*- coding: utf-8 -*-
"""
Created on Wed May  9 09:51:13 2018


This script aims to calculate scale factors for emissions to all receptors for 
5 scenarios. 

#1 for each substance, we must identify its type. This type is defined as one
of three types, with local substitutions being made based on additional 
information that is available for some substances on a CAS number basis.
Along with the scenario name (A,B1,B2,C1,C2), this type will define what value 
we use for the trend indicator

#2 When we know the substance type, we apply the TI as a multiplication factor
to all 5 types of emissions for each scenario

@author: schueder
"""

import pandas as pd
import numpy as np
from replaceTI import replaceTI
from weightFactor import weightFactor

subs      = pd.read_excel(r'..\_dataProcessing\SubstancesList_1835_2.xlsx',sheetname = 'SubstancesList')
specTI    = pd.read_excel(r'..\_dataProcessing\TI_substitutions.xlsx')
genTI       = pd.read_excel(r'..\_dataProcessing\TI.xlsx')
    
land     = pd.read_excel(r'..\_dataProcessing\ListOfCountries_andCalculus_wCode.xlsx',sheetname = 'Countries')
    
# scenario A scale factors must always be determined
subscnA = replaceTI(subs,genTI,specTI,'A')
    
scenarios = ['A','B1','B2','C1','C2']
# scenarios = ['C1']
mat = {}
for scen in scenarios:
    if scen != 'A':
        subscn = replaceTI(subs,genTI,specTI,scen)
    
    # the scaling factor for each scenario is the product of 3 numbers:
    # 1) the TI for the substance, whether determined by overall trend or specific
    #    value chosen by dirk for that substance
    # 2) the country specific factors based on increase in GDP PPP
    # 3) the pollution control factors
    # for scenario A, the last of these 3 == 1 always
    # scaleMat = [A factor,pharma pop growth,scenariotreatment]
    scaleMat = np.ones((len(subscnA['CAS Number']),len(land['Code']),3))
    # mat[(('%s') % scen)] = {} # diagnostic
    # mat[(('%s') % scen)]['CAS'] = [] # diagnostic    
    for ii,sub in enumerate(subscnA['CAS Number']):
        # mat[(('%s') % scen)]['CAS'].append(sub) # diagnostic 
        for jj,ll in enumerate(land['Code']):
            # base rate of increase
            scaleMat[ii,jj,0] = subscnA.loc[subscnA['CAS Number'] == sub, 'TI']
            # increase attributed to population growth
            if subscnA.loc[subs['CAS Number'] == sub,'Type'].iloc[0] == '1_Pharma':  
                scaleMat[ii,jj,1] = land.loc[land['Code'] == ll, 'PopGrowth 2010-2030']
            if scen != 'A':
                GDP = land.loc[land['Code'] == ll, 'GDP-PPP (k$/cap) 2030'].iloc[0]
                TI = subscn['TI'][subscn['CAS Number'].str.contains(sub)].iloc[0]
                # reduction due to implementation of scenario controls
                scaleMat[ii,jj,2] = weightFactor(GDP,TI)
        print('substance ' + str(ii+1) + ' processed')
    # mat[(('%s') % scen)]['DAT'] = scaleMat # diagnostic
    print('beginning file printing...')
    with open(('../scalFiles/scaleValuesScenario_%s.prn') % scen,'w') as scalFile:
        scalFile.write('CAS,')
        #first for scenario A values
        for ii in range(1,len(land['Code'])+1):
            scalFile.write(('%i,')%ii)
        # second for scenario B1/B2/C1/C2 values
        for ii in range(1,len(land['Code'])+1):
            scalFile.write(('%i,')%ii)
        scalFile.write('Close\n')
        for ii,sub in enumerate(subscnA['CAS Number']):
            scalFile.write(('%s,') % sub)
            for jj,ll in enumerate(land['Code']):
                # scenario A
                val = scaleMat[ii,jj,0] * scaleMat[ii,jj,1]
                scalFile.write(('%.3f,') % val)
            for jj,ll in enumerate(land['Code']):
                # scenario B1,B2,C1,C2
                val = scaleMat[ii,jj,2]
                scalFile.write(('%.3f,') % val)
            scalFile.write('lf\n')    
    print('scenario ' + scen + ' file complete')

        
        