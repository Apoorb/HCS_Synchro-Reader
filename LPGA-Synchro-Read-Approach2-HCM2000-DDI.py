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


def Get_Relvant_Dat(IntLineNo,QueueLineNo,fi_AM):
    # Get the HCM 2000 Summary
    #****************************************************** 
    Dat = pd.read_csv(fi_AM,skiprows=IntLineNo+3,nrows=35,sep='\t')
    # Get the HCM 2000 Intersection Summary    
    IntSummary = linecache.getline(fi_AM, IntLineNo+42)
    IntSummary =  ' '.join(IntSummary.split('\t')).strip()
    temp = IntSummary.find('HCM 2000 Level of Service')
    IntSum = [IntSummary[0:temp-1],IntSummary[temp:]]
    
    Dat.columns =[col.strip() for col in Dat.columns]
    #******************************************************
    # Get Queues Summary
    DatQueue = pd.read_csv(fi_AM,skiprows=QueueLineNo+3,nrows=7,sep='\t')
    DatQueue = DatQueue.drop([0,1,2,3,4,5])
    DatQueue = DatQueue.transpose()
    DatQueue.columns = DatQueue.iloc[0]
    DatQueue =DatQueue.drop(DatQueue.index[0])
    DatQueue.columns= ['QLen']
    DatQueue.index.name = 'Movements'
        
    # Merge 
    #******************************************************
    
    Results = Dat[Dat.Movement.isin(['v/c Ratio             ','Delay (s)             ',
                                       'Level of Service      ',
                                       'Approach Delay (s)    ','Approach LOS          '])].transpose()
        #Correct the columns
    Results.columns = Results.iloc[0]
    Results =Results.drop(Results.index[0])
    # Merge with Queue data
    Results = Results.merge(DatQueue,left_index=True,right_index=True)  
    #CAUTION: This is a bad move. Should use rename. This might mess up things
    Results.columns = ["V/C_Ratio","LnGrpDelay","LnGrpLOS","ApproachDelay","ApproachLOS",'QLen']
    Results["QLen"] = Results.QLen.apply(pd.to_numeric, errors='coerce')/25
    Results["QLen"] = Results.QLen.round(0)*25
    Results1 =  Results[["V/C_Ratio","LnGrpDelay","LnGrpLOS","QLen","ApproachDelay","ApproachLOS"]]
    Results1.index =pd.Categorical(Results1.index,[ 
                                        'WBL','WBT', 'WBR',
                                        'NEL','NET','NER',
                                       'NBL', 'NBT','NBR', 
                                       'EBL', 'EBT', 'EBR', 
                                       'SWL','SWT','SWR',
                                       'SBL', 'SBT', 'SBR'])
            
    Results1.LnGrpLOS =Results1[['LnGrpDelay','LnGrpLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
    #Get the format of the Qlen and Delay same as the table in word
    Results1.ApproachLOS =Results1[['ApproachDelay','ApproachLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
    Results1= Results1.drop(["LnGrpDelay","ApproachDelay"],axis=1)
    Results1.QLen = Results1.QLen.apply(lambda x: int(x) if x == x else "")
    Results1.QLen = Results1.QLen.apply(lambda x: format(int(x),",d") if x != "" else "")
    Results1 = Results1.sort_index()
    return(Results1,IntSum)


year = "2045"

# Common path to the Synchro Files 
fi = os.path.abspath('C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\Synchro-Results\\Text Report')
## Synchro file name
fi_AM = os.path.join(fi,"LPGA-"+year+"-AM-Build-HCM2000.txt")

## Read the tab delimited file
file_object  = open(fi_AM, 'r')
IntersectionsLineNO = []
IntersectionsName = {}
RawLines = []
#https://www.geeksforgeeks.org/enumerate-in-python/
LineHCM = 0
for num, line in enumerate(file_object,0):
    # Get HCM data
    if(bool(re.search("HCM Signalized Intersection Capacity Analysis",line))):
        LineHCM=num
    #Get intersection not in HCM 2010 Analysis
    if(bool(re.search("^[38]:",line))|bool(re.search("^[1-9][0-9]",line))):
        if(num==LineHCM+1):
            IntersectionsLineNO.append(num)
            IntersectionsName[num]=line
            print(LineHCM,"-",num)



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
    # Get Queue data
    if(bool(re.search("Queues",line))):
        LineQueue=num
    #Get intersection not in HCM 2010 Analysis
    if(bool(re.search("^[38]:",line))|bool(re.search("^[1-9][0-9]",line))):
        if(num==LineQueue+1):
            QueueLineNO.append(num)
            QueueIntName[num]=line
            print(LineQueue,"-",num)


IntersectionsName[IntersectionsLineNO[0]]
i=0
IntHCM_No = IntersectionsLineNO[i]
QueueNo= QueueLineNO[i]
Get_Relvant_Dat(IntHCM_No,QueueNo,fi_AM)




IntDetail_AM = {}
IntSum_AM = {}
for IntHCM_No,QueueNo in zip(IntersectionsLineNO,QueueLineNO):
    IntDetail_AM[IntersectionsName[IntHCM_No]], IntSum_AM[IntersectionsName[IntHCM_No]] = Get_Relvant_Dat(IntHCM_No,QueueNo,fi_AM)

for i in IntersectionsLineNO:
    print(IntersectionsName[i],IntSum_AM[IntersectionsName[i]])
    print('\n----------------------------------------------------\n')
    
    
    
#********************************************************************************
    
year = "2045"

# Common path to the Synchro Files 
fi = os.path.abspath('C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\Synchro-Results\\Text Report')
## Synchro file name
fi_PM = os.path.join(fi,"LPGA-"+year+"-PM-Build-HCM2000.txt")

## Read the tab delimited file
file_object  = open(fi_PM, 'r')
IntersectionsLineNO_PM = []
IntersectionsName_PM = {}
RawLines = []
#https://www.geeksforgeeks.org/enumerate-in-python/
LineHCM = 0
for num, line in enumerate(file_object,0):
    # Get HCM data
    if(bool(re.search("HCM Signalized Intersection Capacity Analysis",line))):
        LineHCM=num
    #Get intersection not in HCM 2010 Analysis
    if(bool(re.search("^[38]:",line))|bool(re.search("^[1-9][0-9]",line))):
        if(num==LineHCM+1):
            IntersectionsLineNO_PM.append(num)
            IntersectionsName_PM[num]=line
            print(LineHCM,"-",num)



file_object.close()

#Queue
#******************************************************
file_object  = open(fi_PM, 'r')
QueueLineNO_PM = []
QueueIntName_PM = {}
RawLines = []
#https://www.geeksforgeeks.org/enumerate-in-python/
LineQueue = 0
for num, line in enumerate(file_object,0):
    # Get Queue data
    if(bool(re.search("Queues",line))):
        LineQueue=num
    #Get intersection not in HCM 2010 Analysis
    if(bool(re.search("^[38]:",line))|bool(re.search("^[1-9][0-9]",line))):
        if(num==LineQueue+1):
            QueueLineNO_PM.append(num)
            QueueIntName_PM[num]=line
            print(LineQueue,"-",num)


IntDetail_PM = {}
IntSum_PM = {}
for IntHCM_No,QueueNo in zip(IntersectionsLineNO_PM,QueueLineNO_PM):
    IntDetail_PM[IntersectionsName_PM[IntHCM_No]], IntSum_PM[IntersectionsName_PM[IntHCM_No]] = Get_Relvant_Dat(IntHCM_No,QueueNo,fi_PM)

for i in IntersectionsLineNO_PM:
    print(IntersectionsName_PM[i],IntSum_PM[IntersectionsName_PM[i]])
    print('\n----------------------------------------------------\n')
