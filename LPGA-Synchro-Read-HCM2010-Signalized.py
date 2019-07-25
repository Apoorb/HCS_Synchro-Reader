# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 09:14:46 2019

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

 
def ReadIntData(i,Intersections,Dat):
    '''
    i is intersection #. i =0 is Tomoka
    '''
    Dat_Tomoka = Dat.iloc[Intersections[i]+1:Intersections[i]+36,:]
    #Get total intersection delay and LOS
    IntStat_Tomoka = Dat.iloc[Intersections[i]+43:Intersections[i]+46,:]
    IntStat_Tomoka = IntStat_Tomoka.iloc[:,0].apply(lambda x: x.replace('\t',''))
    
    
    # Replace comma's with "-" to write file into csv
    Dat_Tomoka.iloc[:,0] = Dat_Tomoka.iloc[:,0].apply(lambda x: x.replace(',','-'))
    # Split by tab and replace with comma's 
    Da_str = Dat_Tomoka.iloc[:,0].apply(lambda x: ','.join(x.split('\t'))+'\n')
    # Output to a buffer line by line 
    output = StringIO()
    for i in range(Da_str.shape[0]):
        output.write(Da_str.iloc[i])
    contents = output.getvalue()
    # Read the clean buffer
    Dat_Clean = pd.read_csv(StringIO(contents))
    output.close()
    # Remove space from columns
    Dat_Clean.columns =[col.strip() for col in Dat_Clean.columns]
    # Get only rows I need and transpose
    Results = Dat_Clean[Dat_Clean.Movement.isin(['V/C Ratio(X)          ','LnGrp Delay(d)-s/veh  ',
                                       'LnGrp LOS             ','' ,'%ile BackOfQ(95%)-veh/ln',
                                       'Approach Delay- s/veh ','Approach LOS          '])].transpose()
    #Correct the columns
    Results.columns = Results.iloc[0]
    Results =Results.drop(Results.index[0])
    Results.columns = ["V/C_Ratio","Q_95Per","LnGrpDelay","LnGrpLOS","ApproachDelay","ApproachLOS"]
    Results["QLen"] = Results.Q_95Per.apply(pd.to_numeric, errors='coerce').round(0)*25
    
    Results1 =  Results[["V/C_Ratio","LnGrpDelay","LnGrpLOS","QLen","ApproachDelay","ApproachLOS"]]
    
    
    Results1.index =pd.Categorical(Results1.index,[ 'WBL','WBT', 'WBR',
                                   'NBL', 'NBT','NBR', 
                                   'EBL', 'EBT', 'EBR', 
                                   'SBL', 'SBT', 'SBR'])
        
    Results1.LnGrpLOS =Results1[['LnGrpDelay','LnGrpLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
    
    Results1.ApproachLOS =Results1[['ApproachDelay','ApproachLOS']].apply(lambda x: '{} [{}]'.format(x[0],x[1]),axis=1)
    Results1.QLen = Results1.QLen.apply(lambda x: int(x) if x == x else "")
    Results1.QLen = Results1.QLen.apply(lambda x: format(int(x),",d") if x != "" else "")
    Results1= Results1.drop(["LnGrpDelay","ApproachDelay"],axis=1)
    Results1 = Results1.sort_index()
    IntStat_Tomoka
    return(Results1,IntStat_Tomoka)



# Common path to the Synchro Files 
fi = os.path.abspath('C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\Synchro-Results\\Text Report')
## Synchro file name
fi_AM = os.path.join(fi,"LPGA-2025-AM.txt")
## Read the tab delimited file
DatMessyAM = pd.read_fwf(fi_AM,header=None)
## Find the intersection
DatMessyAM["FlagInt"] = DatMessyAM[0].apply(lambda x: bool(re.search("^[1-6]:",x)))
## Create the start point of intersection 
Intersections = DatMessyAM.index[DatMessyAM.FlagInt]
IntersectionName = DatMessyAM[DatMessyAM.FlagInt]
# Get started with 1st intersection (Tomoka)

## Create the start point of intersection 
Intersections = DatMessyAM.index[DatMessyAM.FlagInt]
IntersectionName = DatMessyAM[DatMessyAM.FlagInt]

IntDetail_AM = {}
IntSum_AM = {}
NamesDict = {1:'Tomoka',2:'I95_SB',3:'I95_NB',4:'Technology',5:'Williamson',6:'N_Clyde'}
# Tomoka i = 0 
lab =1
for key,val in NamesDict.items():
    IntDetail_AM[key], IntSum_AM[key] = ReadIntData(key-1,Intersections,Dat= DatMessyAM)
    lab =lab+1


# Tomoka i = 0
i = 1
IntDetail_AM[i]
IntSum_AM[i]

# SB Ramp 
i = 2
IntDetail_AM[i]
IntSum_AM[i]

# NB Ramp 
i = 3
IntDetail_AM[i]
IntSum_AM[i]

# Technology 
i = 4
IntDetail_AM[i]
IntSum_AM[i]

# Williamson
i = 5
IntDetail_AM[i]
IntSum_AM[i]

# N_Clyde 
i = 6
IntDetail_AM[i]
IntSum_AM[i]

# Common path to the Synchro Files 
fi = os.path.abspath('C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\Synchro-Results\\Text Report')
## Synchro file name
fi_PM = os.path.join(fi,"LPGA-2025-PM.txt")
## Read the tab delimited file
DatMessyPM = pd.read_fwf(fi_PM,header=None)
## Find the intersection
DatMessyPM["FlagInt"] = DatMessyPM[0].apply(lambda x: bool(re.search("^[1-6]:",x)))
## Create the start point of intersection 
Intersections = DatMessyPM.index[DatMessyPM.FlagInt]
IntersectionName = DatMessyPM[DatMessyPM.FlagInt]
# Get started with 1st intersection (Tomoka)

## Create the start point of intersection 
Intersections = DatMessyPM.index[DatMessyPM.FlagInt]
IntersectionName = DatMessyPM[DatMessyPM.FlagInt]
IntDetail_PM = {}
IntSum_PM = {}
NamesDict = {1:'Tomoka',2:'I95_SB',3:'I95_NB',4:'Technology',5:'Williamson',6:'N_Clyde'}
# Tomoka i = 0 
lab =1
for key,val in NamesDict.items():
    IntDetail_PM[key], IntSum_PM[key] = ReadIntData(key-1,Intersections,Dat= DatMessyPM)
    lab =lab+1


# Tomoka i = 1
i = 1
IntDetail_PM[i]
IntSum_PM[i]

# SB Ramp 
i =2
IntDetail_PM[i]
IntSum_PM[i]

# NB Ramp 
i = 3
IntDetail_PM[i]
IntSum_PM[i]

# Technology 
i = 4
IntDetail_PM[i]
IntSum_PM[i]

# Williamson
i = 5
IntDetail_PM[i]
IntSum_PM[i]

# N_Clyde 
i = 6
IntDetail_PM[i]
IntSum_PM[i]


















