# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 10:13:23 2018

can we explain something about why the scenarioA is better than reference?
@author: schueder
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pylab
import numpy as np

def CASrem(sr):
    return sr.replace('CAS','').replace(' ','')

# FILES
file = r'P:\1209104-solutions\WP14\SIM\_Scen\_analysis\SCNA_chk_remDupCas.xlsx'
TIFile = r'p:\1209104-solutions\WP14\SIM\scaleFactors\_dataProcessing\TI_substitutions_remDup117-81-7.xlsx'
# current - no pop change, no locator change, only scna change
scn = 'B2'
scnaFile = r'p:\1209104-solutions\WP14\SIM\_Scen\QP_RhineChf\PP-IF\out\chfootprint_Bio_%s.csv' % scn
# old - no pop change, everyhting else present
# scnaFile = r'p:\1209104-solutions\WP14\SIM\_Scen\QP_RhineChf\PP-IF\chfootprintA_noPop2030.csv'
# old - everything present
# scnaFile = r'p:\1209104-solutions\WP14\SIM\_Scen\QP_RhineChf_old\_PP-IF\chfootprintA.csv '
refFile = r'p:\1209104-solutions\WP14\SIM\_Prod\QP_RhineChF\PP-IF\out\chfootprint_Bio_.csv'

CASchk = ['22047-49-0','18835-34-2']
refCAS = 'p:\\1209104-solutions\\WP14\\SIM\\_Scen\\QP_RhineChf_Scn_Ref\\subout\\'
ACAS = 'p:\\1209104-solutions\\WP14\\SIM\\_Scen\\QP_RhineChf_Scn\\suboutA\\'

plt.close('all')

############################### LOAD ##########################################

TIDat = pd.read_excel(TIFile)
TIDat.drop_duplicates(inplace = True)
TIDat.set_index('CAS',inplace = True)

# load catchment and sub - REF
RefSub = pd.read_csv(refFile,skiprows = 2, nrows = 1793)
RefSub = RefSub[['Substance','Subs_Impact(weighed)']]
RefCat = pd.read_csv(refFile,skiprows = 1798, nrows = 813)
RefCat = RefCat[['SUBID','Evalue']]

RefSub['ind'] = RefSub['Substance']
RefSub.set_index('ind',inplace = True)

# load catchment and sub SCNA
ASub = pd.read_csv(scnaFile,skiprows = 2, nrows = 1793)
ASub = ASub[['Substance','Subs_Impact(weighed)']]
ACat = pd.read_csv(scnaFile,skiprows = 1798, nrows = 813)
ACat = ACat[['SUBID','Evalue']]

ASub['ind'] = ASub['Substance']
ASub.set_index('ind',inplace = True)


# load metadata
catInfo = pd.read_excel(file, sheetname = 'subcatchments')
catInfo.set_index('SUBID', inplace = True)

subInfo = pd.read_excel(file, sheetname = 'info')
subInfo['CAS'] = subInfo['CAS'].map(CASrem)
subInfo.set_index('CAS', inplace = True)

############################### CAT ###########################################

# calculate Ediff for catchments
catEdiff = pd.DataFrame(ACat['Evalue'] -  RefCat['Evalue'])

catEdiff.columns = ['diffE']
catEdiffP = catEdiff['diffE'] / np.array(RefCat['Evalue'])
# catEdiffP = catEdiff['diffE'] / ((np.array(ACat['Evalue']) + np.array(RefCat['Evalue']))/2)

catEdiffP = pd.DataFrame(catEdiffP)
catEdiffP.columns = ['diffEP']

# add E diff to SCNA data
ACat = pd.concat([ACat,catEdiff], axis = 1, ignore_index = False)
ACat = pd.concat([ACat,catEdiffP], axis = 1, ignore_index = False)
ACat.set_index('SUBID',inplace = True)
ACat = pd.concat([ACat,catInfo],axis = 1, ignore_index = False)
# remove those subcatchments not in Rhine
ACat = ACat.drop(ACat[np.isnan(ACat['diffE'])].index)

# remove those subcatchments not in Rhine
# ACat.dropna(inplace = True)

# plot difference in Evalues based on up area and country
f1 = sns.lmplot(x = 'ROWNR', y = 'diffEP', hue = 'UPAREA', data = ACat, fit_reg = False)
pylab.savefig(r'P:\1209104-solutions\WP14\SIM\_Scen\_analysis\diffEPHueUparea.png', dpi = 200)
f2 = sns.lmplot(x = 'ROWNR', y = 'diffEP', hue = 'Country', data = ACat, fit_reg = False)
pylab.savefig(r'P:\1209104-solutions\WP14\SIM\_Scen\_analysis\diffEPHueCountry.png', dpi = 200)

################################ SUB ##########################################

# calculate Ediff for subs
# have to be able to deal with case where different subs were successful
# subEdiff = pd.DataFrame(ASub['Subs_Impact'] -  RefSub['Subs_Impact'])
subEdiff = pd.concat([ASub['Subs_Impact(weighed)'],RefSub['Subs_Impact(weighed)']], axis = 1, ignore_index = False)
subEdiff.dropna(axis = 0, inplace = True)
subEdiff.columns = ['ASub','RefSub']
subEdiff['diffE'] = subEdiff['ASub'] - subEdiff['RefSub']
subEdiffP = subEdiff['diffE'] / np.array(RefSub['Subs_Impact(weighed)'])
# subEdiffP = subEdiff['diffE'] / ((np.array(ASub['Subs_Impact']) + np.array(RefSub['Subs_Impact']))/2)

subEdiffP = pd.DataFrame(subEdiffP)
subEdiffP.columns = ['diffEP']

# add E diff to SCNA data
ASub = pd.concat([ASub,subEdiff], axis = 1, ignore_index = False)
ASub = pd.concat([ASub,subEdiffP], axis = 1, ignore_index = False)
ASub['Substance'] = ASub['Substance'].map(CASrem)
ASub.set_index('Substance',inplace = True)
ASub = pd.concat([ASub,subInfo],axis = 1, ignore_index = False)

ASub = ASub.drop(ASub[np.isnan(ASub['diffE'])].index)

# plot difference in Evalues based on substance class and SCN A factor

f4 = sns.lmplot(x = 'No', y = 'diffEP', hue = 'Emissions', data = ASub, fit_reg = False)
pylab.savefig(r'P:\1209104-solutions\WP14\SIM\_Scen\_analysis\SubdiffEPHueClass.png', dpi = 200)

ASub = pd.concat([ASub,TIDat],  axis = 1, ignore_index = False)
ASub.loc[ASub['TI Future %s' % scn] < 1,'TI Future A'] = -1
ASub.loc[ASub['TI Future %s' % scn] == 1,'TI Future A'] = 0
ASub.loc[ASub['TI Future A'] > 1,'TI Future A'] = 1
ASub.loc[np.isnan(ASub['TI Future A']),'TI Future A'] = 0
ASub[ASub['TI Future A'] == np.nan] = 0
ASub.drop('84852-53-9', inplace = True) # no simulation for this substance, but it is in TI

f6 = sns.lmplot(x = 'No',y = 'diffEP', hue = 'TI Future A',data = ASub, fit_reg = False, palette = 'colorblind')
for ii,scal in enumerate(ASub['TI Future A']):    
    # plt.text(np.float(ASub['No'].tolist()[ii]), np.float(ASub['diffEP'].tolist()[ii]), ASub['Emissions'].tolist()[ii] + '/' + str(ASub['Type'].tolist()[ii]) + '_' + ASub.index[ii] )
    plt.text(np.float(ASub['No'].tolist()[ii]), np.float(ASub['diffEP'].tolist()[ii]), ASub['Emissions'].tolist()[ii] + '/' + str(ASub['Type'].tolist()[ii]))

pylab.savefig(r'P:\1209104-solutions\WP14\SIM\_Scen\_analysis\SubdiffEPHueEmiss_%s.png' % scn, dpi = 200)

############################ SPECIFIC SUBSTANCES ##############################

for ss in CASchk:
    refDat = pd.read_csv(refCAS + ss + '.csv')
    ADat = pd.read_csv(ACAS + ss + '.csv')
    refDat.set_index('SUBID',inplace = True)
    ADat.set_index('SUBID',inplace = True)
    
    catEdiff = pd.DataFrame(ADat['Cdis'] -  refDat['Cdis'])
    catEdiff.columns = ['diffCdis']
    catEdiffP = catEdiff['diffCdis'] / np.array(refDat['Cdis'])
    # catEdiffP = catEdiff['diffCdis'] / (np.array(ADat['Cdis']) + np.array(refDat['Cdis']))/2
    catEdiffP = pd.DataFrame(catEdiffP)
    catEdiffP.columns = ['diffCdisP']

    # add E diff to SCNA data
    ADat = pd.concat([ADat,catEdiff], axis = 1, ignore_index = False)
    ADat = pd.concat([ADat,catEdiffP], axis = 1, ignore_index = False)
    ADat = pd.concat([ADat,catInfo],axis = 1, ignore_index = False)
    # remove those subcatchments not in Rhine
    ADat = ADat.drop(ADat[np.isnan(ADat['Cdis'])].index)

    # remove those subcatchments not in Rhine
    # ADat.dropna(inplace = True)

    # plot difference in Evalues based on up area and country
    f7 = sns.lmplot(x = 'ROWNR', y = 'diffCdisP', hue = 'UPAREA', data = ADat, fit_reg = False)
    ax = plt.gca()
    ax.set_title(ss) 
    f8 = sns.lmplot(x = 'ROWNR', y = 'diffCdisP', hue = 'Country', data = ADat, fit_reg = False)    
    ax = plt.gca()
    ax.set_title(ss) 
    f7.set_axis_labels('subcatchment no.','difference in Cdis')
    f8.set_axis_labels('subcatchment no.','%difference in Cdis')

