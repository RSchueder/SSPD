# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 10:40:56 2018

@author: schueder
"""


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab
import statsmodels.api as sm
from sklearn import linear_model
clf = linear_model.LinearRegression()
plt.close()

plot_kws = {'s' : 20}
classified = pd.read_excel('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\ResultsCaseStudies_corr.xlsx',sheetname = 'classified')
sns.pairplot(classified,hue = 'class',palette = 'hls')
pylab.savefig('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\\impact_manualclassified_pairplot.png',dpi = 200)

regression = pd.read_excel('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\ResultsCaseStudies_corr.xlsx',sheetname = 'BalRhineRegression')
fullset = pd.read_excel('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\ResultsCaseStudies_corr.xlsx',sheetname = 'BalRhine')

regression.drop(0.1, axis = 1,inplace = True)
# remove bad runs
regression.loc[regression['OK?'] == False] = np.nan
# remove subs with no impact
regression.loc[regression['PAF'] < 1e-20] = np.nan
regression['PAF'] = np.log10(regression['PAF'])
regression.dropna(axis = 0, inplace = True)

###############################################################################
# CREATE LABELS FOR DATA IN CORNERS
###############################################################################

medPAF = np.median(regression['PAF'])
medE   = np.median(regression['E/PNEC'])
cl = []
for ind,ii in enumerate(regression['PAF']):
    if ii > medPAF+1 and regression['E/PNEC'].iloc[ind] > medE+1:
        cl.append('HH')
    elif ii > medPAF+1 and regression['E/PNEC'].iloc[ind] < medE-1:
        cl.append('HL')
    elif ii < medPAF-1 and regression['E/PNEC'].iloc[ind] > medE+1:
        cl.append('LH')
    elif ii < medPAF-1 and regression['E/PNEC'].iloc[ind] < medE-1:
        cl.append('LL')
    else:
        cl.append('NN')
tmp = pd.DataFrame()
tmp['impact_class'] = pd.Series(cl)
regression.reset_index(inplace = True)
regression = pd.concat([regression, tmp],axis = 1, ignore_index = mely False)
regression.drop(['index'], axis = 1, inplace = True)

###############################################################################
# CREATE REGRESSION SET FOR ALL SUBSTANCES
###############################################################################

rset = regression.copy()
# REMOVE CERTAIN VARIABLES
rset.drop(['case','OK?','Check','C%','Etot (kmol/y)','E(kg/y)','PNEC(ug/L)'], inplace = True, axis = 1)
rset = sm.add_constant(rset)

# CREATE SUBSTANCES SUIBSETS
pharma = rset.loc[rset['type'] == '1_Pharma'].copy()
pharmaPAF = pharma['PAF']
reach = rset.loc[rset['type'] == '3_REACH'].copy()
reachPAF = reach['PAF']
pest = rset.loc[rset['type'] == '2_Pest'].copy()
pestPAF = pest['PAF']

# FOR TYPE
rsetpair1 = rset.copy()
rsetpair1.drop(['impact_class'], axis = 1, inplace = True)

# FOR IMPACT CLASS
rsetpair2 = rset.copy()
rsetpair2 = rsetpair2[rsetpair2['impact_class'] != 'NN']
rsetpair2.drop(['type'], axis = 1)


# DROP LABELS and ENDOGENOUS VARIABLE AS THEY CANNOT BE INCLUDED IN REGRESSION 
rset.drop(['type','PAF','impact_class'], inplace = True, axis = 1)
pharma.drop(['type','PAF','impact_class'], inplace = True, axis = 1)
pest.drop(['type','PAF','impact_class'], inplace = True, axis = 1)
reach.drop(['type','PAF','impact_class'], inplace = True, axis = 1)

###############################################################################
# CREATE REGRESSION MODELS
###############################################################################

X = rset
y = regression['PAF']
regmodel = sm.OLS(y, X.astype(float)).fit()

X = pharma
y = pharmaPAF
pharmamodel = sm.OLS(y, X.astype(float)).fit()

X = pest
y = pestPAF
pestmodel = sm.OLS(y, X.astype(float)).fit()

X = reach
y = reachPAF
reachmodel = sm.OLS(y, X.astype(float)).fit()

###############################################################################

fig, axes = plt.subplots(nrows = 2,ncols = 2, figsize = (8.5,11))
axes[0][0].plot(regression['PAF'],regmodel.predict(rset),'o')
axes[0][0].set_xlabel('observed logPAF')
axes[0][0].set_ylabel('predicted logPAF')
axes[0][0].plot([-6,1],[-6,1],'--')

axes[0][1].plot(pharmaPAF,pharmamodel.predict(pharma),'o')
axes[0][1].set_xlabel('observed logPAF PHARMA')
axes[0][1].set_ylabel('predicted logPAF PHARMA')
axes[0][1].plot([-6,1],[-6,1],'--')

axes[1][0].plot(pestPAF,pestmodel.predict(pest),'o')
axes[1][0].set_xlabel('observed logPAF PEST')
axes[1][0].set_ylabel('predicted logPAF PEST')
axes[1][0].plot([-6,1],[-6,1],'--')

axes[1][1].plot(reachPAF,reachmodel.predict(reach),'o')
axes[1][1].set_xlabel('observed logPAF REACH')
axes[1][1].set_ylabel('predicted logPAF REACH')
axes[1][1].plot([-6,1],[-6,1],'--')
pylab.savefig('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\\multivariate_regression.png',dpi = 200)

###############################################################################
# SINGLE VARIABLE REGRESSION FOR BEST RESPONSE
fig = plt.figure(2)
ax = fig.add_axes([.1,0.1,0.9,0.9])
X = regression['E/PNEC']
X = sm.add_constant(X)
Y = regression['PAF']

ax.plot(regression['E/PNEC'],regression['PAF'],'o')

linmodel = sm.OLS(endog = Y, exog = X, missing = 'drop').fit()
linpred = linmodel.predict(X)
ax.plot(X['E/PNEC'],linpred,'o')
ax.set_xlabel('log E/PNEC')
ax.set_ylabel('logPAF')
ax.plot([medE+1,medE+1],[-8,0],'--k')
ax.plot([medE-1,medE-1],[-8,0],'--k')

ax.plot([0,10],[medPAF+1,medPAF+1],'--k')
ax.plot([0,10],[medPAF-1,medPAF-1],'--k')

pylab.savefig('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\\E-PNEC_regression.png',dpi = 200)

###############################################################################
# EXPLORATORY PAIR PLOTS 

rsetpair1.drop(['const'], axis = 1, inplace = True)
sns.pairplot(rsetpair1,hue = 'type',palette = 'hls')
pylab.savefig('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\\type_autoclassified_fullregpar_pairplot.png',dpi = 200)

rsetpair2.drop(['const'], axis = 1, inplace = True)
sns.pairplot(rsetpair2,hue = 'impact_class',palette = 'hls')
pylab.savefig('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\\impact_autoclassified_fullregpar_pairplot.png',dpi = 200)

###############################################################################
# ATTEMPT TO REMOVE POTTENTIALLY COLINEAR DESCRIPTORS
###############################################################################
# SELECT TO AVOID COLINEARITY
colinreg = regression[['type','impact_class','PAF',	'E/PNEC',	'E2RIV (kmol/y)'	,'E2S1 (kmol/y)', '%Export','%Decay'	,'%Fug', '%Ion','logKOW0','kdw']].copy()

pharma = colinreg.loc[colinreg['type'] == '1_Pharma'].copy()
pharmaPAF = pharma['PAF']
reach = colinreg.loc[colinreg['type'] == '3_REACH'].copy()
reachPAF = reach['PAF']
pest = colinreg.loc[colinreg['type'] == '2_Pest'].copy()
pestPAF = pest['PAF']

colinrsetpair1 = colinreg.copy()
colinrsetpair2 = colinreg.copy()

colinrsetpair1.drop(['impact_class'], axis = 1)
colinrsetpair2 = colinrsetpair2[colinrsetpair2['impact_class'] != 'NN']
colinrsetpair2.drop(['type'], axis = 1)

sns.pairplot(colinrsetpair1,hue = 'type',palette = 'hls')
pylab.savefig('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\\type_autoclassified_colinpar_pairplot.png',dpi = 200)
sns.pairplot(colinrsetpair2,hue = 'impact_class',palette = 'hls')
pylab.savefig('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\\impact_autoclassified_colinpar_pairplot.png',dpi = 200)

pharma.drop(['type','PAF','impact_class'], inplace = True, axis = 1)
pest.drop(['type','PAF','impact_class'], inplace = True, axis = 1)
reach.drop(['type','PAF','impact_class'], inplace = True, axis = 1)

###############################################################################
# CREATE REGRESSION MODELS WITH REDUCED COLINEARITY
###############################################################################

rset = colinreg.drop(['type','impact_class','PAF'], axis = 1)
X = rset
y = regression['PAF']
regmodel = sm.OLS(y, X.astype(float)).fit()

X = pharma
y = pharmaPAF
pharmaColinmodel = sm.OLS(y, X.astype(float)).fit()

X = pest
y = pestPAF
pestColinmodel = sm.OLS(y, X.astype(float)).fit()

X = reach
y = reachPAF
reachColinmodel = sm.OLS(y, X.astype(float)).fit()
fig2, axes2 = plt.subplots(nrows = 2,ncols = 2, figsize = (8.5,11))

axes2[0][0].plot(regression['PAF'],regmodel.predict(rset),'o')
axes2[0][0].set_xlabel('observed logPAF')
axes2[0][0].set_ylabel('predicted logPAF')
axes2[0][0].plot([-6,1],[-6,1],'--')

axes2[0][1].plot(pharmaPAF,pharmaColinmodel.predict(pharma),'o')
axes2[0][1].set_xlabel('observed logPAF PHARMA')
axes2[0][1].set_ylabel('predicted logPAF PHARMA')
axes2[0][1].plot([-6,1],[-6,1],'--')

axes2[1][0].plot(pestPAF,pestColinmodel.predict(pest),'o')
axes2[1][0].set_xlabel('observed logPAF PEST')
axes2[1][0].set_ylabel('predicted logPAF PEST')
axes2[1][0].plot([-6,1],[-6,1],'--')

axes2[1][1].plot(reachPAF,reachColinmodel.predict(reach),'o')
axes2[1][1].set_xlabel('observed logPAF REACH')
axes2[1][1].set_ylabel('predicted logPAF REACH')
axes2[1][1].plot([-6,1],[-6,1],'--')
pylab.savefig('d:\schueder\Documents\projects\SOLUTIONS\QP_ReferenceAnalysis\\colin_multivariate_regression.png',dpi = 200)