# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:09:48 2016

@author: schueder
"""

def make_hl_val(hl):
    
    #need to make a function to turn statements like 5d 4h 53m into # hours
    #option 1
    if hl.find('days') is not -1:
        numint = hl.find('days')-1
        days = float(hl[0:numint])
        hours = days*24
    #option 2
    elif hl.find('y') is not -1 and hl.find('m') is not -1 and hl.find('d') is not -1:
        numinty = hl.find('y')
        years = float(hl[0:numinty])
        numintm = hl.find('m')
        months = float(hl[numinty+1:numintm])
        numintd = hl.find('d')
        days = float(hl[numintm+1:numintd])
        days = years * 365 + months*31 + days
        hours = days*24
    #option 3
    elif hl.find('y') is -1 and hl.find('m') is not -1 and hl.find('d') is not -1:
        numintm = hl.find('m')
        months = float(hl[0:numintm])
        numintd = hl.find('d')
        days = float(hl[numintm+1:numintd])
        days = months*31 + days  
        hours = days*24
    else:
        hours = '-9999'
        
    return hours

#h = make_hl_val(hl)
    
