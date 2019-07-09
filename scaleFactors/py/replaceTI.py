# -*- coding: utf-8 -*-
"""
Created on Wed May  9 14:36:38 2018

@author: schueder
"""
def replaceTI(subs,genTI,specTI,scen):
    for CAS in subs['CAS Number']:
        # replace specific types if applicable
        if len(specTI['CAS'][specTI['CAS'].isin([CAS])]) != 0:
            subs.loc[subs['CAS Number'] == CAS,'Type'] = specTI['Type'][specTI['CAS'] == CAS].iloc[0]
    
        # replace all TI with generic type specific TI values
        stype = subs['Type'][subs['CAS Number'].str.contains(CAS)]
        subs.loc[subs['CAS Number'] == CAS,'TI'] = genTI['Scenario ' + scen][genTI['Substances group'] == stype.iloc[0]].iloc[0]
    
        # replace type specific TI with CAs specific TI
        if len(specTI['CAS'][specTI['CAS'].isin([CAS])]) != 0:
            subs.loc[subs['CAS Number'] == CAS,'TI'] = specTI['TI Future ' + scen][specTI['CAS'] == CAS].iloc[0]
    newSubs = subs.copy()
    return newSubs