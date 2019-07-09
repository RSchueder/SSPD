# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 14:49:49 2018
make use

for PFAS that are already in the espace data, we simply add it to the list

@author: schueder
"""
import pandas as pd
import numpy as np

def isnum(varagin):
    try:                    
        float(varagin)
        return True
    except ValueError:
        return False
    
def NumRemove(varagin):
    newStr = ''
    for ii,jj in enumerate(varagin):
        if jj == "(" or jj == ")" or isnum(jj) or jj == '-':
            pass
        else:
            newStr = newStr + jj
    return newStr.strip()

def MakeNum(varagin):
    varagin = str(varagin).replace(' million','000000')
    newNum = ''
    for ii,jj in enumerate(varagin):
        if isnum(jj):
            newNum = newNum + jj
        else:
            pass
    try:
        return np.log10(float(newNum))
    except:
        return 0
prop = pd.read_csv(r'p:\1209104-solutions\WP14\SIM\_Prod\substanceproperties\PFAS_Properties_46_2BP.csv', skiprows = 1)
emis = pd.read_csv(r'p:\1209104-solutions\WP14\SIM\_Prod\emissiondata\espacedata_fix_ASCII.csv')
prod = pd.read_excel(r'p:\1209104-solutions\WP14\SIM\_Prod\substanceproperties\PFAS Properties_Collection_Updated_julia.xlsx', sheetname = 'Together. Collection properties')
oprop = pd.read_csv(r'p:\1209104-solutions\WP14\SIM\_Prod\substanceproperties\wp17data_readable2.csv',skiprows = 1)
oprop.rename(index = str, columns = {'bp': 'bp.3', 'bp.1': 'bp.4','bp.2': 'bp.5'}, inplace = True)
names = ['','.1','.2']
for ii,jj in enumerate(range(6,9)):
    oprop.insert(jj,'bp%s' % names[ii], -999)
    oprop['bp%s' % names[ii]].iloc[0] = 'none'

# prop = pd.read_csv(r'c:\projects\SOLUTIONS\substanceproperties\PFAS_Properties_46_2BP.csv', skiprows = 1)
# emis = pd.read_csv(r'c:\projects\SOLUTIONS\emissiondata\espacedata_fix_ASCII.csv')
# prod = pd.read_excel(r'c:\projects\SOLUTIONS\substanceproperties\PFAS Properties_Collection_Updated_julia.xlsx', sheetname = 'Together. Collection properties')


same = []
air = []
soil = []
ww = []
with open(r'p:\1209104-solutions\WP14\SIM\_Prod\emissiondata\PFAS_espacedataAP.csv','w') as emFile:
    with open(r'p:\1209104-solutions\WP14\SIM\_Prod\substanceproperties\PFAS_Properties.csv','w') as prFile:
        prFile.write('49')
        for ii in range(0,49):
            prFile.write(', ')
        prFile.write('\n')
        # HEADERS #
        for hh in list(emis.columns):
            if len(hh) == 2 and 't' in hh:
                 emFile.write(hh + ',')
            else:                        
                 emFile.write(NumRemove(hh).replace('.','') + ',')
        emFile.write('\n')
        
        for hh in list(oprop.columns):
            if len(hh) == 2 and 't' in hh:
                 prFile.write(hh + ',')
            else:
                if 'Unnamed' not in hh:
                 prFile.write(NumRemove(hh).replace('.','') + ',')
        prFile.write('\n')        
        for ss in oprop.iloc[0]:
            if not str(ss) == 'nan':
                prFile.write(str(ss) + ',' )
        prFile.write('\n')
        
        # END HEADERS #
        
        for cas in prop['void']:
            if len(emis[emis['CAS'].isin([cas])]) == 1:    
                # if if this PFAS was in the list of emission values 
                df = emis[emis['CAS'].isin([cas])]
                same.append(cas)           
                air.append(df['air.42'].iloc[0])
                ww.append(df['ww.42'].iloc[0])
                soil.append(df['soil.42'].iloc[0])
                for ss in df.iloc[0]:
                    emFile.write(str(ss) + ',' )
                emFile.write('\n')
                # as it was in the previous emission data, it should also be in the previous 
                # properties data
                if len(oprop[oprop['void'].isin([cas])]) == 1:
                    # check again because of new file
                    df = oprop[oprop['void'].isin([cas])]
                    for ss in df.iloc[0]:
                        prFile.write(str(ss) + ',' )
                    prFile.write('\n')
                else:
                    print('ERROR between emis file and oprop file!\n')

        print(str(len(set(same))) + ' PFAS substances found in original data')
        # now all the pre-existing PFAS substances are written to the file, not all of them
        # may be in the 1800 list, but they were in the 5210 list
    
        # make medians for missing data
        mair = np.median(np.array(air))
        mww = np.median(np.array(ww))
        msoil = np.median(np.array(soil))
        repvol = mair + mww + msoil
        for cas in prop['void']:
            if len(emis[emis['CAS'].isin([cas])]) == 0 and cas != 'CAS':
                # substance not previously modelled
                vol = []
                met1 = prod.loc[prod['CAS number'] == cas,['Production volume','Unnamed: 5']]
                met2 = prod.loc[prod['CAS number'] == cas,['Production volume.1','Unnamed: 6']]
                val = np.empty([2,1]) # for both methods
                #if len(met1) != 1:
                #    print('duplicate cas = %s, length = %i' % (cas,len(met1)))
                tmp1 = []
                tmp2 = []
                for ll in range(0,len(met1)):
                    val1 = []
                    val2 = []
                    for ii in met1.iloc[ll]:
                        val1.append(MakeNum(ii))
                    tmp1.append(np.mean(val1))
                    for ii in met2.iloc[ll]:
                        val2.append(MakeNum(ii))
                    tmp2.append(np.mean(val2))
                val[0] = np.mean(np.array(tmp1))
                val[1] = np.mean(np.array(tmp2))
    
                # priority for 2nd column
                if val[1] != 0 and not np.isnan(val[1]):
                    # already in tonnes per year to kg/s
                    vol = 1000.0 * (10**np.mean(np.array(val[1]))) /(86400.0 * 365.0)
                elif val[0] != 0 and not np.isnan(val[0]):
                    # pounds per year to kg/s per second
                    vol = 0.454 * (10**np.mean(np.array(val[0])))/(86400.0 * 365.0)
                else:
                    vol = repvol             
                emFile.write(cas + ',2,0,0.45,0.25,0.1,0.25,')
                for co in range(1,43):
                    emFile.write('-1,-1,-1,-1,-1,')
                emFile.write(str(vol * 0.36) + ',0,' + str(vol * 0.51) + ',' + str(vol * 0.13) + ',0,If\n')      
                # print the properties now
                df = prop[prop['void'].isin([cas])]
                for ss in df.iloc[0]:
                    prFile.write(str(ss) + ',' )
                prFile.write('\n')      
    
