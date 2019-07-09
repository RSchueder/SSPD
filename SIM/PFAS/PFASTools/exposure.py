# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 12:18:36 2018

@author: schueder
"""

# compute pXX concentrations of each subcatchment accross the year, then the 
# pXX concentration for the Rhine simulation per substance

import numpy as np
import pandas as pd
import glob

def find_last(var,ss):
    ind = 0
    lstInd = ind
    it = 0
    while ind >= 0:
        ind = var.find(ss,ind + it,len(var))
        it = 1
        if ind < 0:
            return lstInd
        lstInd = ind
perc = [50,95,99]

with open(r'p:\1209104-solutions\WP14\SIM\_Prod\PFASTools\Cdis_percentiles.csv','w') as percFile:
    percFile.write('CAS,')
    for pp in perc:
        percFile.write(str(pp) + 'centile,')
    percFile.write("\n")
    alf = len(glob.glob(r'p:\1209104-solutions\WP14\SIM\_Prod\QP_RhineChF_PFAS\subout\*Cdis*'))
    for ind,file in enumerate(glob.glob(r'p:\1209104-solutions\WP14\SIM\_Prod\QP_RhineChF_PFAS\subout\*Cdis*')):
        data = pd.read_csv(file)
        data.set_index('Unnamed: 0', inplace = True)
        data.drop('Unnamed: 367', axis = 1, inplace  = True)
        data.drop(1,axis = 0, inplace = True)
        CAS = file[(find_last(file,'\\') + 1):-9]
        percFile.write(CAS + ',')
        for pp in perc:
            # why is this not a set with copy error but the other line is
            data[str(pp) + 'centile'] = data.quantile(q = pp/100, axis = 1)
            # data.loc[scat][str(pp) + 'centile'] = np.percentile(his, pp)
            percFile.write(str(data[str(pp) + 'centile'].quantile(q = pp/100)) + ',')
        percFile.write("\n")
        print((CAS + ' finished (%.2f %%)') % (100* ind/alf))
        