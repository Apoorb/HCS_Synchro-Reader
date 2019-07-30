# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:08:22 2018
Modified: Tue Jul 30 13:42:16 2019
@author: A-Bibeka
"""

import os


print('Current working directory ',os.getcwd())
os.chdir('C:\\Users\\abibeka\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\HCS - V1\\DCDI') 
print('Current working directory ',os.getcwd())
# Replace _ to - in a file name 
#[os.rename(f, f.replace('_', '-')) for f in os.listdir('.') if not f.startswith('.')]
# Replace the year from 2045 to 2025
[os.rename(f, f.replace('Copy', 'AXB')) for f in os.listdir('.') if not f.startswith('.')]

