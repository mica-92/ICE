import csv
from typing import final
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy.stats import linregress
import datetime
import time

# Machine Parameters
vtoinch = 0.17153
vtoIL_coarse = 1280 #high stresses or very cold conditions
vtoIL_fine = 202

# Reading Experiment Information from Experiment Master Sheet (EMS)
col_EMS = ['Experiment Number', 'Grain size', 'Original Lenght', 'Strain Strain', 'Sample Touch']
exp_EMS = pd.read_csv (f'D:\ICE\DATA\EMS.csv', names = col_EMS, skiprows=1)
experiment_number = exp_EMS['Experiment Number']

col_EXP = ['Date', 'Time', 'Pressure', 'Temperature', 'Internal Load', 'External Load', 'Displacement', 'Intensifier', '6v', 'Bath Temperature', 'Piston13', 'Piston20', 'Seconds Travis']

final_data = {}
for i in experiment_number:
    exp_data = pd.read_csv (f'D:\ICE\DATA\PIL{i}.csv', names = col_EXP, skiprows = 2)
    temp = exp_data['Temperature']
    IL = exp_data['Internal Load']
    disp = exp_data['Displacement']

    # Time to seconds - PM AM solved
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
        pd.Series(sec_list)        
        #print(sec_list)
    
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
plot_TS = plt.plot(sec_list, strain_norm, color = 'darkblue')
plt.title('Strain- Time Plot')
plt.xlabel('Time (seconds)')
plt.ylabel('Strain')
plt.show()
    
final_data[i] = {'Temperature':temp, 'Internal Load':IL, 'Displacement':disp, 'Seconds': sec_list} #Diccionario


#print(final_data[19]['Temperature'])
