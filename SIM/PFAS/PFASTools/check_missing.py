

# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:58:53 2018

@author: schueder
"""
import pandas as pd
import numpy as np
from shutil import copyfile
import os
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
os.chdir(os.path.realpath(__file__)[0:find_last(os.path.realpath(__file__),'\\')])

sc = 'B1'

scenComp = {'A0' : ['035','036','037','096','097','098','099','172','158','174'],
            'A' : ['035','036','037','096','097','098','099','172','158','174'],
        'B1': range(135,145),
        'B2': range(135,145),
        'C1': ['035','036','037','096','097','098','099','172','158','174'],
        'C2': range(135,145)}


comps = scenComp[sc]
comps = [str(ii) for ii in comps]
outDir = 'p:\\1209104-solutions\\WP14\\SIM\\_Prod\\QP_RhineChF_PFAS\\subout\\'
allot = {}
subs  = pd.read_csv(r'p:\1209104-solutions\WP14\SIM\_Prod\PFASTools\processing_status.csv')

totSubs = len(subs['CAS'])
fractInd = int(np.ceil(totSubs/10)) 

# finished CAS numbers
finCas = []
for outFile in glob.glob(outDir + "\\*.csv"):
    if 'Cdis' not in outFile[find_last(outFile,'\\')+1:-4] and  'Ctot' not in outFile[find_last(outFile,'\\')+1:-4] and os.path.getsize(outFile) > 5e6:
        finCas.append(outFile[find_last(outFile,'\\')+1:-4])

# missing cas numbers
miss = {}
for ii in subs['CAS']:
    if ii not in finCas:
        miss[ii] = []
# rather than parse files we redo the process assuming it was the same as the
# batch file creation
        
for ii,cc in enumerate(comps):
    allot[cc] = []
    ind1 = ii*(fractInd)
    ind2 = ii*(fractInd) + fractInd
    if ind2 > totSubs:
        ind2 = totSubs
    for ss in range(ind1,ind2):
        allot[cc].append(subs['CAS'].iloc[ss])
                
for ii in miss.keys():
    for jj in allot.keys():
        if ii in allot[jj]:
            miss[ii].append(jj)
            miss[ii].append(allot[jj].index(ii)+1)

with open(r'p:\1209104-solutions\WP14\SIM\_Prod\PFASTools\failed_runs.txt','w') as misFile:
    misFile.write('# this contains the substances missing from this simulation \n#SUBSTANCE,NODE,RUN ORDER\n')
    for ii in miss.keys():
        misFile.write('%s,%s,%i\n' % (ii,miss[ii][0],miss[ii][1]))
    