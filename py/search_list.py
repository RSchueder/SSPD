# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:51:23 2016

@author: schueder
"""
#0	CAS	     #27	toba
#1	Name	     #28	Delhba
#2	SMILES     #29	kn
#3	MolMass    #30	ton
#4	Delho	     #31	Delhn
#5	bp	     #32	kp
#6	mp	     #33	top
#7	pv	     #34	Delhp
#8	ks	     #35	kds
#9	tos	     #36	tods
#10	Delhs	     #37	kde
#11	pka1	     #38	tode
#12	toa1	     #39	kdw
#13	Delha1     #40	todw
#14	pka2	     #41	kow0
#15	toa2	     #42	kaw0
#16	Delha2     #43	koa0
#17	pkb1	     #44	dhow
#18	tob1	     #45	dhaw
#19	Delhb1     #46	dhoa
#20	pkb2	     #47	X1water
#21	tob2	     #48	X1soil
#22	Delhb2     #49	X1sedim
#23	kac	     #50	X2water
#24	toac	     #51	X2soil
#25	Delhac     #52	X2sedim
#26	kba

def search_list(abrev):
    #REMEMBER THAT IN PYTHON THE FIRST INDEX IS '0' AND THER SECOND IS '1'
    method = ['average'] * len(abrev)
    method[6] = 'Mean melting point'
    method[7] = 'Vapor Pressure (Antoine Method)'
    method[8] = 'Water solubility'
    method[35] = 'Ultimate Half Life Predicted'
    method[37] = 'Ultimate Half Life Predicted'
    method[39] = 'Ultimate Half Life Predicted'
    method[41] = 'log Kow'
    
    #(OPTIONAL) SPECIFY THE FILE SPECIFIER AT THIS LOCATION, IF THERE ARE 
    #MULTIPLE VALUES OF SAME NAME BUT FROM DIFFERENT FILES    
    filespec1 = [''] * len(abrev)
    filespec1[35] = '301B'
    filespec1[37] = '301B'
    filespec1[39] = '301B'
    filespec1[41] = 'KOWWIN'
  # if not found use these instead
    filespec2 = [''] * len(abrev)
    filespec2[35] = '301C'
    filespec2[37] = '301c'
    filespec2[39] = '301C'
  # if still not found use these instead
    filespec3 = [''] * len(abrev)
    filespec3[35] = '301_F'
    filespec3[37] = '301_F'
    filespec3[39] = '301_F'
    
    ref_temp = [25] * len(abrev)
    
    return method, filespec1, filespec2, filespec3, ref_temp