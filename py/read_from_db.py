# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:58:01 2016

@author: schueder
"""


def read_from_db(varagin,conn,c):
    from isnum import isnum
    tmp = varagin.replace('-','')
    if isnum(tmp):
        c.execute("SELECT * FROM substance_properties WHERE CAS = '{qq}'".format(qq =  varagin)) 
        data = c.fetchall()
        if len(data) is 0:
            print(('%s\n')%(varagin))
            print('the requested substance is not in the database')
    else:
        c.execute("SELECT * FROM substance_properties WHERE SMILES = '{qq}'".format(qq =  varagin)) 
        data = c.fetchall()
        if len(data) is 0:
            print('the requested substance is not in the database')
    return data
    