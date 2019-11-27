# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 10:02:36 2019

@author: abibeka
Purpose: Batch update synchro volumes
"""

# 0.0 Housekeeping. Clear variable space
#******************************************************************************************
from IPython import get_ipython  #run magic commands
ipython = get_ipython()
ipython.magic("reset -f")
ipython = get_ipython()

import os
import pandas as pd
import numpy as np
import csv

os.chdir(r'C:\Users\abibeka\OneDrive - Kittelson & Associates, Inc\Documents\RampMetering\operations\Synchro')
# Read the volume data 
dat = pd.read_csv('VOLUME.CSV',skiprows=2)
dat.fillna('',inplace=True)
dat2 = dat 
dat2 = dat2.drop(columns = 'DATE')
dat2.rename(columns = {'TIME': 'RECORDNAME'},inplace=True)
dat2.RECORDNAME = 'Volume'

# Scale the volume data 
#Number of Years  = 2040 - 2016
NumYears = 2040 - 2016
GrowthRates = [0,1,2] # percent per year
NetGrowthCalc = lambda x: (1+x/100)**NumYears
NetGrowthRate = list(map(NetGrowthCalc,GrowthRates))
NetGrowthRate

def Output2040Vols(datCp = dat2, NetGrowthRt = 1):
    datCp.iloc[:,2:] = datCp.iloc[:,2:].applymap(lambda x: x if not x else round(x*NetGrowthRt))
    #Change volume data and columns to list --- so it can be written
    dat2Write = datCp.values.tolist()
    #Read the two 2 lines of the csv file separately 
    with open('VOLUME.csv', 'r') as readFile:
        reader = csv.reader(readFile)
        lines = list(reader)
    Header = lines[0:3]
    
    Header[0] = ['[Lanes]']
    Header[1] =['Lane Group Data']
    Header[2][0] = 'RECORDNAME'
    Header[2].remove('TIME')
    #Write the top 2 lines of the csv file, column name and data 
    with open('Volume2040_GrwRt_{}.csv'.format(round(NetGrowthRt,2)), 'w', newline = '') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(Header)
        writer.writerows(dat2Write)
    writeFile.close()
    
Output2040Vols(datCp = dat2, NetGrowthRt = NetGrowthRate[0])
Output2040Vols(datCp = dat2, NetGrowthRt = NetGrowthRate[1])
Output2040Vols(datCp = dat2, NetGrowthRt = NetGrowthRate[2])





