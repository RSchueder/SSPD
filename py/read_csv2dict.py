# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 11:13:15 2016

@author: schueder
"""
import numpy as np
def read_csv2dict(varagin,hline = 0,dline = 1,srow = 1, drow = 2):
    # hline is the headerline
    # dline is the line the data starts on
    # srow is the row of the substances we want to evaluate
    with open(varagin,'r+') as data:
        dat  = {}
        page = data.readlines()
        for ii in page:
            #for each row
            subfound = 0
            if page.index(ii) == hline:
                headers = ii.split(";")                 
            if page.index(ii) >= dline:
                tmp = ii.split(";")
                for nn in tmp:
                    if tmp.index(nn) == srow:
                        sub = nn
                        dat[(("%s")%sub)] = {}   
                        subfound = 1
                    if subfound == 1 and tmp.index(nn) >= drow:
                        nn = nn.replace('ÿþ','')
                        nn = nn.replace('\x00','')
                        dat[(("%s")%sub)][(("%s")%headers[tmp.index(nn)])] = np.array(nn)               
    return dat