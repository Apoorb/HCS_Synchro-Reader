# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 17:01:52 2019

@author: abibeka
"""


#0.0 Housekeeping. Clear variable space
from IPython import get_ipython  #run magic commands
ipython = get_ipython()
ipython.magic("reset -f")
ipython = get_ipython()



import os
import sys
import numpy as np
import pandas as pd
import re
from io import StringIO

import linecache

# Common path to the Synchro Files 
fi = os.path.abspath('C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\Synchro-Results\\Text Report')
## Synchro file name
fi_AM = os.path.join(fi,"LPGA-2025-AM-Build-HCM2000.txt")

## Read the tab delimited file
file_object  = open(fi_AM, 'r')
IntersectionsLineNO = []
IntersectionsName = {}
RawLines = []
#https://www.geeksforgeeks.org/enumerate-in-python/
LineHCM = 0
for num, line in enumerate(file_object,0):
    if(bool(re.search("HCM Signalized Intersection Capacity Analysis",line))):
        LineHCM=num
    if(bool(re.search("^[38]:",line))|bool(re.search("^[1-9][0-9]",line))):
        if(num==LineHCM+1):
            IntersectionsLineNO.append(num)
            IntersectionsName[num]=line
            print(LineHCM,"-",num)


SkRow = IntersectionsLineNO[0]
# Get the HCM 2000 Summary
Dat = pd.read_csv(fi_AM,skiprows=SkRow+3,nrows=35,sep='\t')
# Get the HCM 2000 Intersection Summary
Dat2 = pd.read_fwf(fi_AM,skiprows=SkRow+40,nrows=1,sep='\t')

IntSummary = linecache.getline(fi_AM, SkRow+42)
IntSummary =  ' '.join(IntSummary.split('\t')).strip()
temp = IntSummary.find('HCM 2000 Level of Service')
IntSum = [IntSummary[0:temp-1],IntSummary[temp:]]


file_object.close()

#Queue
#******************************************************



file_object  = open(fi_AM, 'r')
QueueLineNO = []
QueueIntName = {}
RawLines = []
#https://www.geeksforgeeks.org/enumerate-in-python/
LineQueue = 0
for num, line in enumerate(file_object,0):
    if(bool(re.search("Queues",line))):
        LineQueue=num
    if(bool(re.search("^[38]:",line))|bool(re.search("^[1-9][0-9]",line))):
        if(num==LineQueue+1):
            QueueLineNO.append(num)
            QueueIntName[num]=line
            print(LineQueue,"-",num)

SkRow = QueueLineNO[0]
# Get Queues Summary
DatQueue = pd.read_csv(fi_AM,skiprows=SkRow+3,nrows=7,sep='\t')
DatQueue = DatQueue.drop([0,1,2,3,4,5])
DatQueue = DatQueue.transpose()
DatQueue.columns = DatQueue.iloc[0]
DatQueue =DatQueue.drop(DatQueue.index[0])
DatQueue.columns= ['Q_95Per']
DatQueue.index.name = 'Movements'
# Merge 
#******************************************************


Dat.columns =[col.strip() for col in Dat.columns]

    
Results = Dat[Dat.Movement.isin(['v/c Ratio             ','Delay (s)             ',
                                   'Level of Service      ',
                                   'Approach Delay (s)    ','Approach LOS          '])].transpose()
    #Correct the columns
Results.columns = Results.iloc[0]
Results =Results.drop(Results.index[0])
Results = Results.merge(DatQueue,left_index=True,right_index=True)  
Results.columns = ["V/C_Ratio","LnGrpDelay","LnGrpLOS","ApproachDelay","ApproachLOS",'Q_95Per']
Results["QLen"] = Results.Q_95Per.apply(pd.to_numeric, errors='coerce').round(0)*25
Results1 =  Results[["V/C_Ratio","LnGrpDelay","LnGrpLOS","QLen","ApproachDelay","ApproachLOS"]]
Results1.index =pd.Categorical(Results1.index,[ 
                                    'WBL','WBT', 'WBR',
                                    'NEL','NET','NER',
                                   'NBL', 'NBT','NBR', 
                                   'EBL', 'EBT', 'EBR', 
                                   'SEL','SET','SWR',
                                   'SBL', 'SBT', 'SBR'])
        
Results1.LnGrpLOS =Results1[['LnGrpDelay','LnGrpLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
#Get the format of the Qlen and Delay same as the table in word
Results1.ApproachLOS =Results1[['ApproachDelay','ApproachLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
Results1= Results1.drop(["LnGrpDelay","ApproachDelay"],axis=1)
Results1.QLen = Results1.QLen.apply(lambda x: int(x) if x == x else "")
Results1.QLen = Results1.QLen.apply(lambda x: format(int(x),",d") if x != "" else "")
Results1 = Results1.sort_index()
