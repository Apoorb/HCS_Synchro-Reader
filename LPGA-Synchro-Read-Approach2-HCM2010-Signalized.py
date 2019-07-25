# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 15:40:38 2019
#muy bien
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



def GetRelevantDat(file,SkRow=0):
    Dat = pd.read_csv(file,skiprows=SkRow+1,nrows=36,sep='\t')
    Dat2 = pd.read_csv(file,skiprows=SkRow+47,nrows=2,sep='\t')
    Dat2.index = Dat2.index.droplevel([1,2,3])
    Dat.columns =[col.strip() for col in Dat.columns]
     # Get only rows I need and transpose
    Results = Dat[Dat.Movement.isin(['V/C Ratio(X)          ','LnGrp Delay(d),s/veh  ',
                                       'LnGrp LOS             ','' ,'%ile BackOfQ(95%),veh/ln',
                                       'Approach Delay, s/veh ','Approach LOS          '])].transpose()
    #Correct the columns
    Results.columns = Results.iloc[0]
    Results =Results.drop(Results.index[0])
    Results.columns = ["V/C_Ratio","Q_95Per","LnGrpDelay","LnGrpLOS","ApproachDelay","ApproachLOS"]
    Results["QLen"] = Results.Q_95Per.apply(pd.to_numeric, errors='coerce').round(0)*25
    #Subset data
    Results1 =  Results[["V/C_Ratio","LnGrpDelay","LnGrpLOS","QLen","ApproachDelay","ApproachLOS"]]
    
    #Get the order of the rows same as the table in word
    Results1.index =pd.Categorical(Results1.index,[ 'WBL','WBT', 'WBR',
                                   'NBL', 'NBT','NBR', 
                                   'EBL', 'EBT', 'EBR', 
                                   'SBL', 'SBT', 'SBR'])
        
    Results1.LnGrpLOS =Results1[['LnGrpDelay','LnGrpLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
    #Get the format of the Qlen and Delay same as the table in word
    Results1.ApproachLOS =Results1[['ApproachDelay','ApproachLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
    Results1.QLen = Results1.QLen.apply(lambda x: int(x) if x == x else "")
    Results1.QLen = Results1.QLen.apply(lambda x: format(int(x),",d") if x != "" else "")
    Results1= Results1.drop(["LnGrpDelay","ApproachDelay"],axis=1)
    Results1 = Results1.sort_index()
    return(Results1,Dat2)



# Common path to the Synchro Files 
fi = os.path.abspath('C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\Synchro-Results\\Text Report')
## Synchro file name
fi_AM = os.path.join(fi,"LPGA-2025-AM-Build-HCM2010.txt")

## Read the tab delimited file
file_object  = open(fi_AM, 'r')
IntersectionsLineNO = []
IntersectionsName = {}
RawLines = []
#https://www.geeksforgeeks.org/enumerate-in-python/
for num, line in enumerate(file_object,0):
    if(bool(re.search("^[1-6]:",line))):
        IntersectionsLineNO.append(num)
        IntersectionsName[num]=line
#Pop the Diamond interchange for future scenarios
        # use regex expression later
if fi_AM ==  os.path.join(fi,"LPGA-2025-AM-Build-HCM2010.txt"):
    IntersectionsLineNO.pop(1)

IntDetail_AM = {}
IntSum_AM = {}
for Indx in IntersectionsLineNO:
    IntDetail_AM[IntersectionsName[Indx]], IntSum_AM[IntersectionsName[Indx]] = GetRelevantDat(fi_AM,Indx)

for i in IntersectionsLineNO:
    print(IntersectionsName[i],IntSum_AM[IntersectionsName[i]])
    print('\n----------------------------------------------------\n')
    
    
    


# Common path to the Synchro Files 
fi = os.path.abspath('C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\Synchro-Results\\Text Report')
## Synchro file name
fi_PM = os.path.join(fi,"LPGA-2035-PM.txt")

## Read the tab delimited file
file_object  = open(fi_PM, 'r')
IntersectionsLineNO_PM = []
IntersectionsName_PM = {}
RawLines = []
#https://www.geeksforgeeks.org/enumerate-in-python/
for num, line in enumerate(file_object,0):
    if(bool(re.search("^[1-6]:",line))):
        IntersectionsLineNO_PM.append(num)
        IntersectionsName_PM[num]=line
        
IntDetail_PM = {}
IntSum_PM = {}
for Indx in IntersectionsLineNO_PM:
    IntDetail_PM[IntersectionsName_PM[Indx]], IntSum_PM[IntersectionsName_PM[Indx]] = GetRelevantDat(fi_PM,Indx)

for i in IntersectionsLineNO_PM:
    print(IntersectionsName_PM[i],IntSum_PM[IntersectionsName_PM[i]])
    print('\n----------------------------------------------------\n')
    
    
