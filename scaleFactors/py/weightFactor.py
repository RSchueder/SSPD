# -*- coding: utf-8 -*-
"""
Created on Wed May  9 15:30:32 2018

@author: schueder
"""

def weightFactor(GDP,TI):
    if GDP > 40:
        pass
    else:
        m = (TI - 1)/40
        TI = GDP*m + 1
    return TI