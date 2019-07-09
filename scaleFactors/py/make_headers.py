# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:19:20 2018

@author: schueder
"""

countries = ['AL',
'AN',
'AT',
'BY',
'BE',
'BA',
'BG',
'HR',
'CY',
'CZ',
'DK',
'EE',
'FI',
'FR',
'DE',
'EL',
'HU',
'IS',
'IE',
'IT',
'XK',
'LV',
'LT',
'LU',
'MA',
'MT',
'MD',
'ME',
'NL',
'NO',
'PL',
'PT',
'RO',
'RU',
'RS',
'SK',
'SI',
'ES',
'SE',
'CH',
'UA',
'UK',
'EU']

headers = []
for cc in countries:
    headers.append('air' + cc)
    headers.append('water' + cc)
    headers.append('ww' + cc)
    headers.append('soil' + cc)
    headers.append('undef' + cc)