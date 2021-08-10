#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
from typing import final
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy.stats import linregress
import scipy
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

#time_new = [x for x in sec_list if x >= 39881]
#print(time_new)
    
    
    
    
# Machine Parameters
vtoinch = 0.17153
vtoIL_coarse = 1280 #high stresses or very cold conditions
vtoIL_fine = 202

# Experiment Parameters
L0 = 1.94 #inches
strain_rate = 2.30E-05 #constant
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
#plt.show()


plot_TS = plt.plot(strain_norm, stress, color = 'darkblue')
plt.title(f'{n}\nStrain- Time Plot')
plt.xlabel('Time (seconds)')
plt.ylabel('Strain')
#plt.show()
    


# In[ ]:


def strain_rate_range(u,n=1):
    counter = 1
    u = str(f'{u:8f}')
    s = u.replace(".","") #in case the SR is given as a function 
    for ndx,i in enumerate(s):
        if i == "0":
            counter = 1
            continue
        if counter >= n:
            first_nonzero = int(s[ndx - n + 1: ndx + 1])
            if first_nonzero == 9:
                h = str(first_nonzero + 1)
                zero_count  =  ndx - 2
                digits =  '0' * zero_count
                max_range = float(str(f"0.{digits}{h}"))
                
                q = str(first_nonzero - 1)
                min_range = float(u.replace(str(first_nonzero), q))
                
            elif first_nonzero == 1:    
                h = str(first_nonzero + 1)
                max_range = float(u.replace(str(first_nonzero), h))
                
                q = 9
                digits = '0' * ndx
                min_range = float(str(f"0.{digits}{q}"))
                
            else: #original argument
                h = str(first_nonzero + 1)
                max_range = float(u.replace(str(first_nonzero), h))
                q = str(first_nonzero - 1)
                min_range = float(u.replace(str(first_nonzero), q))    
                
                
        return min_range, max_range
        counter += 1
SRR = strain_rate_range(strain_rate)
print (SRR)            
               


# In[ ]:


SRR = strain_rate_range(strain_rate)


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
        if SRR[0] < values[h] < SRR[1]:
            condition = True
        else:
            h=h+5
    
    #Second Cut
    condition_2 = False
    q = h
    while condition_2 == False:
        if values[q] < -0.25e-04:
            condition_2 = True
        else:
            q=q+1
    return h, q


# In[ ]:


cut = experiment(sec_list)
print(cut)


# In[ ]:


Lf_cut = L0 - (disp - disp[cut[0]]) * vtoinch
stress = IL * vtoIL_fine * Lf_cut / (sample_r**2 * math.pi * L0)
strain = np.log(L0 / Lf)
strain_norm = strain * np.exp((- Q_DC / R) * ((T_norm ** -1)-(temp**-1)))


# In[ ]:


sec_int = sec_list[cut[0]:(cut[1])]
sec_final  = []
for p in range(len(sec_int)):
    x = sec_int[p] - sec_list[cut[0]]
    sec_final.append(x)
    
strain_final = strain_norm[cut[0]:cut[1]]
stress_final = stress[cut[0]:cut[1]]



plot_TS = plt.plot(sec_final, strain_final, color = 'darkblue')
plt.title(f'{n}\nStrain- Time Plot')
plt.xlabel('Time (seconds)')
plt.xticks(np.arange(min(sec_final),max(sec_final),500))
plt.ylabel('Strain')
           
plt.show()


# In[ ]:



plot_TS = plt.plot(strain_final, stress_final, color = 'darkblue')
plt.title(f'{n}\nStrain- Stress Plot')
plt.xlabel('Strain')
plt.ylabel('Stress (MPa)')
           
plt.show()


# In[ ]:





# In[ ]:


def strain_rate_range(u,n=1):
    counter = 1
    u = str(f'{u:8f}')
    s = u.replace(".","") #in case the SR is given as a function 
    for ndx,i in enumerate(s):
        if i == "0":
            counter = 1
            continue
        if counter >= n:
            first_nonzero = s[ndx - n + 1: ndx + 1]
            h = str(int(first_nonzero) + 1)
            max_range = float(u.replace(first_nonzero, h))
            q = str(int(first_nonzero) - 1)
            min_range = float(u.replace(first_nonzero, q))
            return min_range, max_range
        counter += 1
SRR = strain_rate_range(strain_rate)
print (SRR)

