#!/usr/bin/env python
# coding: utf-8

# In[17]:


import csv
from typing import final
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy.stats import linregress
import datetime
import time

col_names = ['Date',
             'Time',
             'Pressure',
             'Temperature',
             'Internal Load',
             'External Load',
             'Displacement',
             'Intensifier',
             '6v',
             'Temperature Bath',
             'Piston13',
             'Piston20',
             'Stress',
             'Strain',
             'TimeSec']

n = 'PIL20'
exp_data = pd.read_csv (f'D:\ICE\DATA\{n}.csv',names=col_names, skiprows=2)

# Data
temp = exp_data['Temperature']
IL = exp_data['Internal Load']
disp = exp_data['Displacement']

# Time to seconds
raw_time = exp_data['Time']
sec_list = []
time = []

for row in raw_time:
    time = row[:-3]
    ftr = [3600,60,1]
    if row[-2:] == 'PM' and row[0:2] != '12':
        sec = 43200 + sum([a*b for a,b in zip(ftr, map(int,time.split(':')))])
    else:
        sec = sum([a*b for a,b in zip(ftr, map(int,time.split(':')))])
    sec_list.append(sec)


# Machine Parameters
vtoinch = 0.17153
vtoIL_coarse = 1280 #high stresses or very cold conditions
vtoIL_fine = 202

# Experiment Parameters
L0 = 2.2 #inches
strain_rate = 5e-05 #constant
Lf = L0 - disp * vtoinch
sample_r = 0.55 #inches includes sample plus iridium jacket
Q_DC = 181 #KJ/mol
R = 0.0083145 #KJ/mol
T_norm = 263.55 #how was this calculated



Lf = L0 - disp * vtoinch
stress = IL * vtoIL_fine * Lf / (sample_r**2 * math.pi * L0)
strain = np.log(L0 / Lf)
strain_norm = strain * np.exp((- Q_DC / R) * ((T_norm ** -1)-(temp**-1)))
    
plot_TS = plt.plot(raw_time, strain_norm, color = 'darkblue')
plt.title(f'{n}\nStrain- Time Plot')
plt.xlabel('Time (seconds)')
plt.ylabel('Strain')
plt.show()
    


# In[33]:



def experiment(s):
    a = s
    values = []
    
    for i in range(0,(len(a)-1)):
        j = i+5
        if j <= (len(a)-1):
            slope, intercept, r_value, p_value, std_err = linregress (sec_list[i:j],strain_norm[i:j])
        else:
            j = (len(a)-1)
            slope, intercept, r_value, p_value, std_err = linregress (sec_list[i:j],strain_norm[i:j])
        values.append(slope)
    
    #First Cut
    condition = False
    h = 0
    while condition == False:
        if 4e-05 < values[h] < 6e-05:
            condition = True
        else:
            h=h+1
    
    #Second Cut
    condition_2 = False
    q = h
    while condition_2 == False:
        if values[q] < 0:
            condition_2 = True
        else:
            q=q+1
    return h, q


# In[34]:


cut = experiment(sec_list)
print(cut)


# In[36]:


y_final = strain_norm[cut[0]:cut[1]+4]
time_final = raw_time[cut[0]:cut[1]+4]

plot_TS = plt.plot(time_final, y_final, color = 'darkblue')
plt.title(f'{n}\nStrain- Time Plot')
plt.xlabel('Time (seconds)')
plt.ylabel('Strain')
plt.show()


# In[ ]:





# In[ ]:




