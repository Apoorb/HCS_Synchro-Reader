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

import xml.etree.ElementTree as ET


fi = os.path.abspath('C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\HCS - Copy')

fi_IN = os.path.join(fi,"EB to NB 2017 AM-AXB.xhr")

tree = ET.parse(fi_IN)
root = tree.getroot()
LOS = root.find(".//LOS")
LOS_Val = LOS.text

Density = root.find(".//Density")
Density_Val = Density.text
TabVal = Density_Val +" [{}]".format(LOS_Val)


NBTable = {
"Merge at US 92 WB-to-NB on-ramp":"US 92\\NB Merge ",
"From US 92 onramp to LPGA off-ramp":"I95 from US92 to LPGA\\NB ",
"Diverge at LPGA off-ramp": "NB Offramp ", 
"Merge at LPGA EB-to-NB on-ramp": "EB to NB ",
"Merge at LPGA WB-to-NB on-ramp": "WB to NB ",
"From LPGA WB-to-NB onramp to SR 40 off-ramp": "I95 from LPGA to SR40\\NB",
"Diverge at SR 40 off-ramp": "SR 40\\NB Offramp "
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


def LOS_Den_Fun(Pa):
    tree = ET.parse(Pa)
    root = tree.getroot()
    LOS = root.find(".//LOS")
    LOS_Val = LOS.text
    Density = root.find(".//Density")
    Density_Val = Density.text
    TabVal = Density_Val +" [{}]".format(LOS_Val)
    return TabVal

fi = 'C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\HCS - Copy\\'
NB_dat["FullPath"] = fi+ NB_dat.Path + NB_dat.Time + " " + NB_dat.AMPM +"-AXB.xhr"

fi1= 'C:\\Users\\abibeka\\OneDrive - Kittelson & Associates, Inc\\Documents\\LPGA\\ToFDOT\\HCS - Copy\\I95 from US92 to LPGA\\NB 2017 AM-AXB.xhf'
ET.parse(fi1)


doc = ET  .fromstring(code)
doc.find('.//LOS').text


NB_dat["FullPath"].apply(LOS_Den_Fun)
{
"Merge at SR 40 on-ramp"
"From SR 40 onramp to LPGA off-ramp"
"Diverge at LPGA off-ramp"
"Merge at LPGA WB-to-SB on-ramp"
"Merge at LPGA EB-to-SB on-ramp"
"From LPGA EB-to-SB onramp to US 92 off-ramp"
"Diverge at US 92 SB-to-WB off-ramp'
}
