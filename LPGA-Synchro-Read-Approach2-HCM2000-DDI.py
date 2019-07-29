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

#Debug:
i=3
#IntersectionsName
#IntHCM_No = IntersectionsLineNO[i]
#QueueNo= QueueLineNO[i]
#IntLineNo = IntHCM_No
#QueueLineNo = QueueNo

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
    
    Results = Dat[Dat.Movement.isin(['Traffic Volume (vph)  ','v/c Ratio             ','Delay (s)             ',
                                       'Level of Service      ',
                                       'Approach Delay (s)    ','Approach LOS          '])].transpose()
        #Correct the columns
    Results.columns = Results.iloc[0]
    Results =Results.drop(Results.index[0])
    # Merge with Queue data
    Results = Results.merge(DatQueue,left_index=True,right_index=True)  
    #CAUTION: This is a bad move. Should use rename. This might mess up things
    Results.columns = ['Volume',"V/C_Ratio","LnGrpDelay","LnGrpLOS","ApproachDelay","ApproachLOS",'QLen']
    Results["QLen1"] = Results.QLen.apply(pd.to_numeric, errors='coerce')/25
    Results["QLen1"] = Results.QLen1.round(0)*25
    Results1 =  Results[['Volume',"V/C_Ratio","LnGrpDelay","LnGrpLOS","QLen1","ApproachDelay","ApproachLOS",'QLen']]
    Results1.index =pd.Categorical(Results1.index,[ 
                                        'WBL','WBT', 'WBR',
                                        'NEL','NET','NER',
                                       'NBL', 'NBT','NBR', 
                                        'NWL', 'NWT', 'NWR',
                                       'EBL', 'EBT', 'EBR', 
                                       'SWL','SWT','SWR',
                                       'SEL', 'SET','SER',
                                       'SBL', 'SBT', 'SBR'])
            
    Results1.LnGrpLOS =Results1[['LnGrpDelay','LnGrpLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
    #Get the format of the Qlen and Delay same as the table in word
    Results1.ApproachLOS =Results1[['ApproachDelay','ApproachLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
    #Need Lane Group Delay for getting approach delay for DDI
    #Results1= Results1.drop(["LnGrpDelay","ApproachDelay"],axis=1)
    Results1= Results1.drop(["ApproachDelay"],axis=1)
    Results1.QLen1 = Results1.QLen1.apply(lambda x: int(x) if x == x else "")
    Results1.QLen1 = Results1.QLen1.apply(lambda x: format(int(x),",d") if x != "" else "")
    Results1 = Results1.sort_index()
    return(Results1,IntSum)


year = "2035"

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
            IntersectionsName[num]=line[:2].split(':')[0]
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
            QueueIntName[num]=line[:2].split(':')[0]
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
    
    
DatAMNode3 = IntDetail_AM['3']
DatAMNode8 = IntDetail_AM['8']
DatAMNode14 = IntDetail_AM['14']
DatAMNode24 = IntDetail_AM['24']
DatAMNode45 = IntDetail_AM['45']
DatAMNode49 = IntDetail_AM['49']

DatAMNode3 = DatAMNode3[DatAMNode3.index=='NER'].rename(index={'NER':'NBR'})
DatAMNode8 = DatAMNode8[DatAMNode8.index=='SWR'].rename(index={'SWR':'SBR'})
DatAMNode14 = DatAMNode14[DatAMNode14.index.isin(['EBT','SWT'])].rename(index={'SWT':'WBT'})
DatAMNode24 = DatAMNode24[DatAMNode24.index.isin(['WBT','NET'])].rename(index={'NET':'EBT'})
DatAMNode45 = DatAMNode45[DatAMNode45.index=='NWL'].rename(index={'NWL':'NBL'})
DatAMNode49 = DatAMNode49[DatAMNode49.index=='SEL'].rename(index={'SEL':'SBL'})

    
#Get approach delay for Diverging Diamond Interchange
#********************************************************************************
    
SB_Ramp_Dat_AM = pd.concat([DatAMNode24,DatAMNode49,DatAMNode8])
NB_Ramp_Dat_AM = pd.concat([DatAMNode14,DatAMNode3,DatAMNode45]).sort_index()
NB_Ramp_Dat_AM.index =pd.Categorical(NB_Ramp_Dat_AM.index,[ 
                                        'WBT', 'NBL','NBR','EBT'])
NB_Ramp_Dat_AM =NB_Ramp_Dat_AM.sort_index()

TotalVol = SB_Ramp_Dat_AM.Volume.astype('float').sum()
VolIntoDelay = (SB_Ramp_Dat_AM.Volume.astype('float') * SB_Ramp_Dat_AM.LnGrpDelay.astype('float')).sum()
SB_Ramp_OverallInt_AM_Delay = VolIntoDelay /TotalVol

SB_Ramp_SB_Approach = SB_Ramp_Dat_AM.loc[['SBL','SBR']]
TotalVol_SB_AM = SB_Ramp_SB_Approach.Volume.astype('float').sum()
VolIntoDelay_SB_AM = (SB_Ramp_SB_Approach.Volume.astype('float') * SB_Ramp_SB_Approach.LnGrpDelay.astype('float')).sum()
SB_Ramp_SB_Delay_AM = VolIntoDelay_SB_AM /TotalVol_SB_AM

SB_Ramp_Dat_AM = SB_Ramp_Dat_AM.drop(columns= ['LnGrpDelay'])
SB_Ramp_Dat_AM
SB_Ramp_SB_Delay_AM
SB_Ramp_OverallInt_AM_Delay

#**********************************************************
TotalVol1 = NB_Ramp_Dat_AM.Volume.astype('float').sum()
VolIntoDelay1 = (NB_Ramp_Dat_AM.Volume.astype('float') * NB_Ramp_Dat_AM.LnGrpDelay.astype('float')).sum()
NB_Ramp_OverallInt_AM_Delay = VolIntoDelay1 /TotalVol1

NB_Ramp_NB_Approach1 = NB_Ramp_Dat_AM.loc[['NBL','NBR']]
TotalVol_NB_AM = NB_Ramp_NB_Approach1.Volume.astype('float').sum()
VolIntoDelay_NB_AM = (NB_Ramp_NB_Approach1.Volume.astype('float') * NB_Ramp_NB_Approach1.LnGrpDelay.astype('float')).sum()
NB_Ramp_NB_Delay_AM  = VolIntoDelay_NB_AM /TotalVol_NB_AM


NB_Ramp_Dat_AM = NB_Ramp_Dat_AM.drop(columns= ['LnGrpDelay'])
NB_Ramp_Dat_AM
NB_Ramp_NB_Delay_AM
NB_Ramp_OverallInt_AM_Delay


#********************************************************************************
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
            IntersectionsName_PM[num]=line[:2].split(':')[0]
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
            QueueIntName_PM[num]=line[:2].split(':')[0]
            print(LineQueue,"-",num)


IntDetail_PM = {}
IntSum_PM = {}
for IntHCM_No,QueueNo in zip(IntersectionsLineNO_PM,QueueLineNO_PM):
    IntDetail_PM[IntersectionsName_PM[IntHCM_No]], IntSum_PM[IntersectionsName_PM[IntHCM_No]] = Get_Relvant_Dat(IntHCM_No,QueueNo,fi_PM)

for i in IntersectionsLineNO_PM:
    print(IntersectionsName_PM[i],IntSum_PM[IntersectionsName_PM[i]])
    print('\n----------------------------------------------------\n')


IntDetail_PM.keys()
    
DatPMNode3 = IntDetail_PM['3']
DatPMNode8 = IntDetail_PM['8']
DatPMNode14 = IntDetail_PM['14']
DatPMNode24 = IntDetail_PM['24']
DatPMNode45 = IntDetail_PM['45']
DatPMNode49 = IntDetail_PM['49']

DatPMNode3 = DatPMNode3[DatPMNode3.index=='NER'].rename(index={'NER':'NBR'})
DatPMNode8 = DatPMNode8[DatPMNode8.index=='SWR'].rename(index={'SWR':'SBR'})
DatPMNode14 = DatPMNode14[DatPMNode14.index.isin(['EBT','SWT'])].rename(index={'SWT':'WBT'})
DatPMNode24 = DatPMNode24[DatPMNode24.index.isin(['WBT','NET'])].rename(index={'NET':'EBT'})
DatPMNode45 = DatPMNode45[DatPMNode45.index=='NWL'].rename(index={'NWL':'NBL'})
DatPMNode49 = DatPMNode49[DatPMNode49.index=='SEL'].rename(index={'SEL':'SBL'})

#Get approach delay for Diverging Diamond Interchange
#********************************************************************************
    
SB_Ramp_Dat_PM = pd.concat([DatPMNode24,DatPMNode49,DatPMNode8])

NB_Ramp_Dat_PM = pd.concat([DatPMNode14,DatPMNode3,DatPMNode45]).sort_index()

NB_Ramp_Dat_PM.index =pd.Categorical(NB_Ramp_Dat_PM.index,[ 
                                        'WBT', 'NBL','NBR','EBT'])
NB_Ramp_Dat_PM =NB_Ramp_Dat_PM.sort_index()

TotalVol1 = SB_Ramp_Dat_PM.Volume.astype('float').sum()
VolIntoDelay1 = (SB_Ramp_Dat_PM.Volume.astype('float') * SB_Ramp_Dat_PM.LnGrpDelay.astype('float')).sum()
SB_Ramp_OverallInt_PM_Delay = VolIntoDelay1 /TotalVol1

SB_Ramp_SB_Approach1 = SB_Ramp_Dat_PM.loc[['SBL','SBR']]
TotalVol_SB_PM = SB_Ramp_SB_Approach1.Volume.astype('float').sum()
VolIntoDelay_SB_PM = (SB_Ramp_SB_Approach1.Volume.astype('float') * SB_Ramp_SB_Approach1.LnGrpDelay.astype('float')).sum()
SB_Ramp_SB_Delay_PM = VolIntoDelay_SB_PM /TotalVol_SB_PM

SB_Ramp_Dat_PM = SB_Ramp_Dat_PM.drop(columns= ['LnGrpDelay'])
SB_Ramp_Dat_PM
SB_Ramp_SB_Delay_PM
SB_Ramp_OverallInt_PM_Delay

#**********************************************************
TotalVol1 = NB_Ramp_Dat_PM.Volume.astype('float').sum()
VolIntoDelay1 = (NB_Ramp_Dat_PM.Volume.astype('float') * NB_Ramp_Dat_PM.LnGrpDelay.astype('float')).sum()
NB_Ramp_OverallInt_PM_Delay = VolIntoDelay1 /TotalVol1

NB_Ramp_NB_Approach1 = NB_Ramp_Dat_PM.loc[['NBL','NBR']]
TotalVol_NB_PM = NB_Ramp_NB_Approach1.Volume.astype('float').sum()
VolIntoDelay_NB_PM = (NB_Ramp_NB_Approach1.Volume.astype('float') * NB_Ramp_NB_Approach1.LnGrpDelay.astype('float')).sum()
NB_Ramp_NB_Delay_PM  = VolIntoDelay_NB_PM /TotalVol_NB_PM


NB_Ramp_Dat_PM = NB_Ramp_Dat_PM.drop(columns= ['LnGrpDelay'])
NB_Ramp_Dat_PM
NB_Ramp_NB_Delay_PM
NB_Ramp_OverallInt_PM_Delay




