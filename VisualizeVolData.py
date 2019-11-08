# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 11:28:14 2019

@author: abibeka
Visualize the volume data for I-75 near SR 200
"""

#data
'''
http://flto.dot.state.fl.us/website/FloridaTrafficOnline/qryReport2.aspx?sID=360317&rID=SHourly%20Continuous%20Counts
'''

import pandas as pd
import numpy as np
import matplotlib as mlt
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.chdir(r'C:\Users\abibeka\OneDrive - Kittelson & Associates, Inc\Documents\RampMetering')


x1 = pd.ExcelFile('DatSouthSR40--I75.xlsx')
x1.sheet_names
dat = x1.parse('Subset Data South of SR 40')
dat.columns
Sum_dat  = dat.describe()
dat.dtypes
dat.loc[:,'day'] = dat.BEGDATE.dt.weekday_name
dat.set_index('BEGDATE',inplace=True)
dat.drop(columns = ['COUNTY','SITE','TOTVOL'],inplace=True)

'''
01/01: NEW YEARS DAY
01/08: NCAA NTL CHAMP GAME @ 8PM
01/15: MARTIN LUTHER KING JR DAY
02/04: SUPERBOWL - PHILADELPHIA EAGLES VS NE PATRIOTS - MINNEAPOLIS, MN -6:30 PM
02/14: VALENTINE'S DAY; 02/19: PRESIDENT'S DAY
03/11: DAYLIGHT SAVING TIME BEGINS
03/12-16: PUBLIC SCHOOLS - SPRING BREAK
03/17: ST. PATRICK'S DAY
04/01: EASTER SUNDAY; 04/17: FEDERAL TAX DAY
05/02-12: COLLEGES & UNIVERSITIES - END OF 2018 SPRING SEMESTER
05/13: MOTHER'S DAY; 05/28: MEMORIAL DAY
05/24: PUBLIC SCHOOLS 2017-18 YEAR CLOSES
05/26-28: TS ALBERTO IMPACTS TRAFFIC  # Tropical storm

6/17: FATHER'S DAY
7/4: INDEPENDENCE DAY
08/13: PUBLIC SCHOOLS OPEN FOR 2018-19 ACADEMIC YEAR
09/01: CHARLESTON SO 7:30PM; 09/08: KENTUCKY 7:30PM; 09/15: COL ST 4PM @ UF

09/03: LABOR DAY
10/06: LSU @ FL GATORS 3:30PM
10/08-14: HURRICANE MICHAEL IMPACTS TRAFFIC
10/31: HALLOWEEN
11/03: MISSOURI (4PM); 11/10: SO CAROLINA (12PM); 11/17: IDAHO @ UF (12PM)
11/04: DAYLIGHT SAVING TIME ENDS; 11/06: 2018 MID-TERM ELECTION DAY
11/11 (OBSERVED 11/12): VETERAN'S DAY
11/22: THANKSGIVING
12/06-16: COLLEGES & UNIVERSITIES - 2018 FALL SEMESTER ENDS
12/20-01/02: PUBLIC SCHOOLS CLOSED FOR WINTER BREAK
12/25: CHRISTMAS DAY
NOTE: ATYPICAL DAYS HAVE COUNTS THAT ARE HIGHER OR LOWER THAN NORMAL, BUT STILL REASONABLE, AND NO LOCAL SPECIAL EVENTS ARE KNOWN.
'''
Type_Map = {
        'A':  'Atypical Day',
        'B' : 'Bad Day',
        'S' :  'Special Event', 
        'H' :  'Holiday' , 
        'N' : 'Normal' 
        }

def plot_Vol(dat, x='N',dir1 = 'Northbound'):
    dat1 = dat[dat.DIR == x].copy()
    dat1.drop(columns='DIR',inplace=True)  
    dat1 = dat1.reset_index()
    dat1 = pd.wide_to_long(dat1,['HR'],i='BEGDATE',j='Hour').reset_index()
    dat1.rename(columns={'HR' : 'Vol'},inplace=True)
    dat1.Hour = dat1.Hour-1
    
    g = sns.catplot(x='Hour',y='Vol',data=dat1[dat1.TYPE=='N'], col='day',col_wrap=3,kind ='box',
                col_order=['Monday','Tuesday','Wednesday','Thursday','Friday'
                           ,'Saturday','Sunday'])
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle("{}—Normal".format(dir1),fontsize =15)
    plt.savefig('{}_NormalDayVol.jpg'.format(dir1))
    g = sns.catplot(x='Hour',y='Vol',data=dat1[dat1.TYPE=='A'], col='day',col_wrap=3,kind ='box',
                col_order=['Monday','Tuesday','Wednesday','Thursday','Friday'
                           ,'Saturday','Sunday'])
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle("{}—Atypical".format(dir1),fontsize =15)
    plt.savefig('{}_AtypicalDayVol.jpg'.format(dir1))
    
    dat1.BEGDATE = dat1.BEGDATE.dt.date
    
    sns.catplot(x='Hour',y='Vol',data=dat1[dat1.TYPE=='S'], col='BEGDATE',col_wrap=3,
                kind='bar',palette='Set2')
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle("{}—Special Events".format(dir1),fontsize =15)
    g.savefig('{}_SplVol.jpg'.format(dir1))
    
    
    g = sns.catplot(x='Hour',y='Vol',data=dat1[dat1.TYPE=='H'], col='BEGDATE',col_wrap=3,
                kind='bar',palette='Set2')
    
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle("{}—Holiday Events".format(dir1),fontsize =15)
    g.savefig('{}_HolidayVol.jpg'.format(dir1))
    

plot_Vol(dat,x='N',dir1 = 'Northbound') 
plot_Vol(dat,x='S',dir1 = 'Southbound') 
    
    
    
for x in ['N','S']:
    for i,j in zip(['N','A'],['Normal','Atypical']):
        plt.figure()
        dat_Norm_N = dat[((dat.DIR == x) & (dat.TYPE == i))]
        dat_Norm_N.drop(columns='DIR',inplace=True)  
        dat_Norm_N_1 = dat_Norm_N.groupby('day')[['HR{}'.format(x) for x in range(1,25)]].mean()
        dat_Norm_N_1.columns = ['HR{}'.format(int(x[2:])-1) for x in dat_Norm_N_1.columns]
        dat_Norm_N_1.index = pd.CategoricalIndex(dat_Norm_N_1.index, 
          categories= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                       "Saturday",'Sunday'])
        dat_Norm_N_1.sort_index(level=0, inplace=True)
        colorBar_ = 'viridis_r'
        vmax_ = 4500; vmin_ = 0
        g = sns.heatmap(dat_Norm_N_1,cmap = colorBar_, vmin=vmin_, vmax=vmax_,linewidths=.5)
        g.set_title('{}—{}'.format(x,j))    
        fig = g.get_figure()
        fig.savefig('Heatmap_{}_{}'.format(x,j))

    
    
    
    
