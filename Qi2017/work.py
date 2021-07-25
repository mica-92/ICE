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
exp_data = pd.read_csv (f'D:\ICE\DATA\{n}h.csv',names=col_names)
#exp_data = exp_data[130:526] #see

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
    #print(timeii)
    ftr = [3600,60,1]
    sec = sum([a*b for a,b in zip(ftr, map(int,time.split(':')))])#see how I can substract the first out of each
    sec_list.append(sec)
    sec0 = sec_list[0] 
    sec = sec - sec0 #not startin
    #print(sec_list)
    #print(sec0)

# Machine Parameters
vtoinch = 0.17153
vtoIL_coarse = 1280 #high stresses or very cold conditions
vtoIL_fine = 202

# Experiment Parameters
L0 = 2.2 #inches
strain_rate = 5e+05 #constant
disp0 = disp[0]
Lf = L0 - (disp - disp0) * vtoinch
sample_r = 0.55 #inches includes sample plus iridium jacket
Q_DC = 181 #KJ/mol
R = 0.0083145 #KJ/mol
T_norm = 263.55 #how was this calculated

stress = IL * vtoIL_fine * Lf / (sample_r**2 * math.pi * L0)
strain = np.log(L0 / Lf)
strain_norm = strain * np.exp((- Q_DC / R) * ((T_norm ** -1)-(temp**-1)))

# Plots
plot_TS = plt.plot(raw_time, strain_norm, color = 'darkblue')
plt.title(f'{n}\nStrain- Time Plot')
plt.xlabel('Time (seconds)')
plt.ylabel('Strain')
plt.show()

plot_SS = plt.plot(strain_norm, stress, color = 'darkblue', alpha = 0.3)
plt.title(f'{n}\nStrain- Stress Plot')
plt.xlabel('Time (seconds)')
plt.ylabel('Stress (MPa)')
plt.show()

plot_ST = plt.plot(strain_norm, temp)
plt.title(f'{n}\nStrain- Temperature Plot')
plt.xlabel('Temperature')
plt.ylabel('Stress (MPa)')
#plt.show()

plot_param = linregress (sec_list, strain)
print(plot_param)

# Peak
index_min = np.argmax(stress)
#print(index_min)
max_stress = np.amax(stress)
#print(max_stress)
maxstress = stress[26]
#print(maxstress)
max_temp = temp[26] #temp peak

# Flow
flow_stress = np.mean(stress[-5:-1])
flow_temp = np.mean(temp[-5:-1])
flow_strain = np.mean(strain[-5:-1])