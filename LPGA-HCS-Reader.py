# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 13:31:11 2019

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
from bs4 import BeautifulSoup as BS
import xml.etree.ElementTree as ET
from itertools import islice
import glob
import datetime


NBTable = {
"Merge at US 92 WB-to-NB on-ramp":"US 92\\NB Merge",
"From US 92 onramp to LPGA off-ramp":"I95 from US92 to LPGA\\NB",
"Diverge at LPGA off-ramp": "NB Offramp", 
"Merge at LPGA EB-to-NB on-ramp": "EB to NB",
"Merge at LPGA WB-to-NB on-ramp": "WB to NB",
"From LPGA WB-to-NB onramp to SR 40 off-ramp": "I95 from LPGA to SR40\\NB",
"Diverge at SR 40 off-ramp": "SR 40\\NB Offramp"
}

NB_dat = pd.DataFrame.from_dict(NBTable,orient='index')
NB_dat.reset_index(inplace=True)
NB_dat.columns = ["TabName","Path"]
NB_dat["AMPM"] ="AM"
NB_dat["Time"] ="2017"

T1 = NB_dat.copy()
T1["AMPM"] ="PM"
T1["Time"] ="2017"
NB_dat=pd.concat([NB_dat,T1])

T1 = NB_dat.copy()
T1["Time"] ="2045"
NB_dat=pd.concat([NB_dat,T1])


def LOS_Den_Fun(Pa):
    with open(Pa) as myfile:
        head = list(islice(myfile,2))
    doc = ET.fromstring(head[1])
    LOS = doc.find('.//LOS').text
    Density = doc.find('.//Density').text
    return '{} [{}]'.format(Density,LOS)

fi = 'C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\HCS - Copy\\'
NB_dat["FullPathPattern"] = fi+ '\\'+NB_dat.Path+"*"+NB_dat.Time+"*"+NB_dat.AMPM+"*AXB*"
NB_dat.reset_index(inplace=True)
NB_dat["PathToFile"] = NB_dat["FullPathPattern"].apply(lambda x: glob.glob(x))
NB_dat["PathToFile"]=NB_dat["PathToFile"].apply(lambda x: x[0])
NB_dat["Results"] = NB_dat["PathToFile"].apply(LOS_Den_Fun)
NB_Final = NB_dat[["Time","TabName","AMPM","Results"]]
NB_Final["TabName"] = pd.Categorical(NB_Final["TabName"],["Merge at US 92 WB-to-NB on-ramp",
"From US 92 onramp to LPGA off-ramp",
"Diverge at LPGA off-ramp", 
"Merge at LPGA EB-to-NB on-ramp",
"Merge at LPGA WB-to-NB on-ramp",
"From LPGA WB-to-NB onramp to SR 40 off-ramp",
"Diverge at SR 40 off-ramp"])
    






SBTable = {
"Merge at SR 40 on-ramp": "SR 40\\SB Merge",
"From SR 40 onramp to LPGA off-ramp": "I95 from LPGA to SR40\\SB",
"Diverge at LPGA off-ramp": "SB Offramp",
"Merge at LPGA WB-to-SB on-ramp":"WB to SB",
"Merge at LPGA EB-to-SB on-ramp":"EB to SB", 
"From LPGA EB-to-SB onramp to US 92 off-ramp": "I95 from US92 to LPGA\\SB",
"Diverge at US 92 SB-to-WB off-ramp": "US 92\\SB Offramp"
}
SB_dat = pd.DataFrame.from_dict(SBTable,orient='index')
SB_dat.reset_index(inplace=True)
SB_dat.columns = ["TabName","Path"]
SB_dat["AMPM"] ="AM"
SB_dat["Time"] ="2017"

T1 = SB_dat.copy()
T1["AMPM"] ="PM"
T1["Time"] ="2017"
SB_dat=pd.concat([SB_dat,T1])

T1 = SB_dat.copy()
T1["Time"] ="2045"
SB_dat=pd.concat([SB_dat,T1])


fi = 'C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\HCS - Copy\\'
SB_dat["FullPathPattern"] = fi+ '\\'+SB_dat.Path+"*"+SB_dat.Time+"*"+SB_dat.AMPM+"*AXB*"
SB_dat.reset_index(inplace=True)
SB_dat["PathToFile"] = SB_dat["FullPathPattern"].apply(lambda x: glob.glob(x))
SB_dat["PathToFile"]=SB_dat["PathToFile"].apply(lambda x: x[0])
SB_dat["Results"] = SB_dat["PathToFile"].apply(LOS_Den_Fun)
SB_Final = SB_dat[["Time","TabName","AMPM","Results"]]
SB_Final["TabName"] = pd.Categorical(SB_Final["TabName"],["Merge at SR 40 on-ramp",
"From SR 40 onramp to LPGA off-ramp",
"Diverge at LPGA off-ramp",
"Merge at LPGA WB-to-SB on-ramp",
"Merge at LPGA EB-to-SB on-ramp", 
"From LPGA EB-to-SB onramp to US 92 off-ramp",
"Diverge at US 92 SB-to-WB off-ramp"])
    


fOut = 'C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\'
dt_buf=datetime.datetime.now()
dt_buf1=dt_buf.strftime("%m-%d-%Y")
writer=pd.ExcelWriter(fOut+"Res"+dt_buf1+".xlsx")
NB_Final.groupby(["Time","TabName","AMPM"])['Results'].agg({'Results':'first'}).sort_index().to_excel(writer,"NB")
SB_Final.groupby(["Time","TabName","AMPM"])['Results'].agg({'Results':'first'}).sort_index().to_excel(writer,"SB")
writer.save()