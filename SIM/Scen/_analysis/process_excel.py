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
    return sr.replace('CAS','')
file = r'P:\1209104-solutions\WP14\SIM\_Scen\_analysis\SCNA_chk.xlsx'
TIFile = r'p:\1209104-solutions\WP14\SIM\scaleFactors\_dataProcessing\TI_substitutions_remDup117-81-7.xlsx'
TIDat = pd.read_excel(TIFile)

TIDat.set_index('CAS',inplace = True)
SCNAfile = r'p:\1209104-solutions\WP14\SIM\_Scen\QP_RhineChf\PP-IF\chfootprintA.csv'
refFile = r'p:\1209104-solutions\WP14\SIM\_Prod\QP_RhineChF\PP-IF\chfootprintRef.csv'

plt.close('all')

ss = 'chk_sub'
dat = pd.read_excel(file, sheetname = ss)
dat['Substance'] = dat['Substance'].map(CASrem)
dat.set_index('Substance',inplace = True)
dat.drop_duplicates(inplace=True)
TIDat.drop_duplicates(inplace = True)
datN = pd.concat([dat,TIDat],  axis = 1, ignore_index = False)
datN.loc[datN['TI Future A'] < 1,'TI Future A'] = -1
datN.loc[datN['TI Future A'] == 1,'TI Future A'] = 0
datN.loc[datN['TI Future A'] > 1,'TI Future A'] = 1
datN.loc[np.isnan(datN['TI Future A']),'TI Future A'] = 0

datN[datN['TI Future A'] == np.nan] = 0
datN.drop('84852-53-9', inplace = True) # no simulation for this substance, but it is in TI
sns.lmplot(x = 'rank',y = 'diffP', hue = 'TI Future A',data = datN, fit_reg = False, palette = 'hsv')
for ii,scal in enumerate(datN['TI Future A']):    
    if datN.index[ii] == '22047-49-0':
        plt.text(np.float(datN['rank'].tolist()[ii]), np.float(datN['diffP'].tolist()[ii]), datN['class'].tolist()[ii] + '/' + str(datN['Type'].tolist()[ii]) + '_' + datN.index[ii] )

sns.lmplot(x = 'rank',y = 'diff', hue = 'TI Future A',data = datN, fit_reg = False, palette = 'hsv')
for ii,scal in enumerate(datN['TI Future A']):    
    if datN.index[ii] == '22047-49-0':
        plt.text(np.float(datN['rank'].tolist()[ii]), np.float(datN['diff'].tolist()[ii]), datN['class'].tolist()[ii] + '/' + str(datN['Type'].tolist()[ii]) + '_' + datN.index[ii] )
pylab.savefig(r'P:\1209104-solutions\WP14\SIM\_Scen\_analysis\scaleChk.png', dpi = 200)


# sns.pairplot(dat[['rank','diff','diffP','ref','A','class']],hue = 'class',palette = 'coolwarm')



