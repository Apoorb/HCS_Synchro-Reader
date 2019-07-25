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
# Common path to the Synchro Files 
fi = os.path.abspath('C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\Synchro-Results\\Text Report')
## Synchro file name
fi_IN = os.path.join(fi,"LPGA-2025-PM.txt")
## Read the tab delimited file
Dat = pd.read_fwf(fi_IN,header=None)
## Find the intersection
Dat["FlagInt"] = Dat[0].apply(lambda x: bool(re.search("^[1-6]:",x)))
## Create the start point of intersection 
Intersections = Dat.index[Dat.FlagInt]
# Get started with 1st intersection (Tomoka)
i = 1
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

Results1 = Results1.sort_index()
IntStat_Tomoka



















i = 1
Dat.iloc[Intersections[i]+1:Intersections[i]+36,:]
i = 2
Dat.iloc[Intersections[i]+1:Intersections[i]+36,:]
i = 3
Dat.iloc[Intersections[i]+1:Intersections[i]+36,:]
i = 4
Dat.iloc[Intersections[i]+1:Intersections[i]+36,:]

i = 5
Dat.iloc[Intersections[i]+1:Intersections[i]+36,:]



















