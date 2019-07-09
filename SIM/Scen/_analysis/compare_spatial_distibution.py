# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 17:24:41 2018

@author: schueder
"""

import glob
import pandas as pd
import matplotlib.pyplot as plt
import pylab
import seaborn as sns

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
        

ADir = r'p:\1209104-solutions\WP14\SIM\_Scen\QP_RhineChf\suboutA\ ' 
refDir = r'p:\1209104-solutions\WP14\SIM\_Prod\QP_RhineChF\subout\*.csv' 
exFile = r'p:\1209104-solutions\WP14\SIM\scaleFactors\_dataProcessing\TI_substitutions.xlsx'
plt.close('all')
TIDat = pd.read_excel(exFile)
# fig, axes = plt.subplots(nrows = 3,ncols = 1)
file = r'P:\1209104-solutions\WP14\SIM\_Scen\_analysis\SCNA_chk.xlsx'

sheets = ['100986-85-4_chk','103-90-2_chk','118-82-1_chk','52918-63-5_chk']

for ss in sheets:
    dat = pd.read_excel(file, sheetname = ss)
    f1 = sns.lmplot(x = 'rank',y = 'diffCdisP', hue = 'uparea',data = dat, fit_reg = False, palette = 'colorblind')
    ax = plt.gca()
    ax.set_title(ss)    
    f2 = sns.lmplot(x = 'rank',y = 'diffCdisP', hue = 'country',data = dat, fit_reg = False, palette = 'colorblind')
    ax = plt.gca()
    ax.set_title(ss) 
    # pylab.savefig(r'P:\1209104-solutions\WP14\SIM\_Scen\_analysis\diffCdisHueUparea_%s' % ss, dpi = 200)
    # plt.close('all')    

ss = '22047-49-0_CdisAvgChk'
dat = pd.read_excel(file, sheetname = ss)
f1 = sns.lmplot(x = 'rank',y = 'CdiffP', hue = 'uparea',data = dat, fit_reg = False, palette = 'colorblind')
ax = plt.gca()
ax.set_title(ss) 
f2 = sns.lmplot(x = 'rank',y = 'CdiffP', hue = 'country',data = dat, fit_reg = False, palette = 'colorblind')
ax = plt.gca()
ax.set_title(ss) 
f2.set_axis_labels('subcatchment no.','%difference in Cdis')


    

