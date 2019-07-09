# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 10:38:18 2018

@author: schueder
"""

# post tool

import pandas as pd
import numpy as np
import glob

def isnum(varagin):
    try:                    
        float(varagin)
        return True
    except ValueError:
        return False

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
        
# first do the properties file
props = ['MolMass','bp','mp','pv','ks','kac','kba','kn','kds','kde','kdw','kow0','kaw0','dhaw']
df = pd.DataFrame(np.nan, index = ['void'], columns = props)
df['CAS'] = np.nan
with open(r'p:\1209104-solutions\WP14\SIM\_Prod\PFASTools\properties_used.csv','w') as propFile:
    for pp in props:
        propFile.write(pp + ',') 
    propFile.write( "\n")
    for ind,file in enumerate(glob.glob(r'p:\1209104-solutions\WP14\SIM\_Prod\QP_RhineChF_PFAS\subout\*.prop')):
        with open(file) as fid:
            df = pd.concat([df,pd.DataFrame(np.nan, index = [ind], columns = props)], axis = 0, ignore_index = True)
            CAS = file[(find_last(file,'\\') + 1):-5]
            df.loc[ind]['CAS'] = CAS
            propFile.write(CAS + ',')
            doc = fid.readlines()
            for line in doc:
                if 'parameter' in line[1:10]:
                    tmp = line.split(' ')
                    par = tmp[2]
                    for val in tmp:
                        if isnum(val):
                            # setting with copy warning
                            # I cannot set to indicies that do not yet exist
                            # this is foolish, as I need to concatenated each time
                            df.loc[ind][par] = val.replace('\n','')
            for par in props:
                val = df[par].loc[ind]
                if np.isnan(val):
                    propFile.write('-999,')                   
                else:
                    propFile.write(str(df[par].loc[ind]) + ',')                
                    
            propFile.write('\n')
                    
                    
                    
        
