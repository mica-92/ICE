import csv
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

n = 'PIL19'
exp_data = pd.read_csv (f'D:\ICE\DATA\{n}.csv',names=col_names, skiprows=2)
#exp_data = exp_data[130:526] #see

# Data
temp = exp_data['Temperature']
IL = exp_data['Internal Load']
disp = exp_data['Displacement']
timeTravis = exp_data['TimeSec']

# Time to seconds
raw_time = exp_data['Time']
#print(raw_time)
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
disp0 = disp[122]
Lf = L0 - (disp - disp0) * vtoinch
sample_r = 0.55 #inches includes sample plus iridium jacket
Q_DC = 181 #KJ/mol
R = 0.0083145 #KJ/mol
T_norm = 263.55 #how was this calculated

stress = IL * vtoIL_fine * Lf / (sample_r**2 * math.pi * L0)
strain = np.log(L0 / Lf)
strain_norm = strain * np.exp((- Q_DC / R) * ((T_norm ** -1)-(temp**-1)))      

# Plots
plot_TS = plt.plot(sec_list[142:520], strain_norm[142:520], color = 'darkblue')
#plt.title(f'{n}\nStrain- Time Plot')
#plt.xlabel('Time (seconds)')
#plt.ylabel('Strain')
plt.show()
