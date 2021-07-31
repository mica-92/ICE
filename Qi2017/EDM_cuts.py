## This is working but not the way of cutting data


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
sample_r = 0.55
R = 0.0083145 #KJ/mol
T_norm = 263 #Leaving this constant but this can be another column in EMS
Q_DC = 181 #KJ/mol

# Reading Experiment Information from Experiment Master Sheet (EMS)
col_EMS = ['Experiment Number', 'Grain size', 'Original Lenght', 'Strain Rate']
exp_EMS = pd.read_csv (f'D:\ICE\DATA\EMS.csv', names = col_EMS, skiprows=1)
experiment_number = pd.Series(exp_EMS['Experiment Number'])

col_EXP = ['Date', 'Time', 'Pressure', 'Temperature', 'Internal Load', 'External Load', 'Displacement', 'Intensifier', '6v', 'Bath Temperature', 'Piston13', 'Piston20', 'Seconds Travis']

#Loading experiment Data
final_data = {}
for i in experiment_number:
    exp_data = pd.read_csv (f'D:\ICE\DATA\PIL{i}.csv', names = col_EXP, skiprows = 2)
    temp = exp_data['Temperature']
    IL = exp_data['Internal Load']
    disp = exp_data['Displacement']
    loc = experiment_number[experiment_number == i].index[0]
    L0 = exp_EMS['Original Lenght'][loc]
    SR_exp = exp_EMS['Strain Rate'][loc]
    GS_exp = exp_EMS['Grain size'][loc]

    
    # Determination of d (grain size)
    if GS_exp == 'Coarse':
        d = 360e-06 #meters
    elif GS_exp == 'Standard':
        d = 230e-06
    else:
        d = 10e-06
    
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
        
    #print(sec_list)
    
    # Calculation of experiment Raw Stress and Strain 
    Lf = L0 - disp * vtoinch
    raw_stress = IL * vtoIL_fine * Lf / (sample_r**2 * math.pi * L0)
    raw_strain = np.log(L0 / Lf)
    raw_strain_norm = raw_strain * np.exp((- Q_DC / R) * ((T_norm ** -1)-(temp**-1)))
    
    
    # Strain Rate Range - need to fix for 1 and 9
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
    SRR = strain_rate_range(SR_exp)

    
    # Cutting the data according to the slope
    def data_range(s):
        a = s
        values = []

        for w in range(0,(len(a)-1)):
            j = w+5
            if j <= (len(a)-1):
                slope, intercept, r_value, p_value, std_err = linregress (sec_list[w:j],raw_strain_norm[w:j])
            else:
                j = (len(a)-1)
                slope, intercept, r_value, p_value, std_err = linregress (sec_list[w:j],raw_strain_norm[w:j])
            values.append(slope)
        

        #First Cut
        condition = False
        h = 0
        while condition == False:
            if SRR[0] < values[h] < SRR[1]:
                condition = True
            else:
                h=h+1

        #Second Cut
        condition_2 = False
        q = h
        while condition_2 == False:
            if values[q] < SRR[0]:
                condition_2 = True
            else:
                q=q+1
        return h, q
    
    cut = data_range(sec_list)
    print(cut)

    Lf_cut = L0 - (disp - disp[cut[0]]) * vtoinch
    stress = IL * vtoIL_fine * Lf_cut / (sample_r**2 * math.pi * L0)
    strain = np.log(L0 / Lf)
    strain_norm = strain * np.exp((- Q_DC / R) * ((T_norm ** -1)-(temp**-1)))

    sec_int = sec_list[cut[0]:(cut[1])]
    sec_final = []
    for p in range(len(sec_int)):
        secii = sec_int[p] - sec_list[cut[0]]
        sec_final.append(secii)

    
    strain_final = strain_norm[cut[0]:cut[1]]
    stress_final = stress[cut[0]:cut[1]]



    plot_TS = plt.plot(sec_int, strain_final, color = 'darkblue')
    plt.title(f'{i}\nStrain- Time Plot')
    plt.xlabel('Time (seconds)')
    #plt.xticks(np.arange(min(sec_final),max(sec_final),500))
    plt.ylabel('Strain')
            
    plt.show()

    plot_TS = plt.plot(strain_final, stress_final, color = 'darkblue')
    plt.title(f'{i}\nStrain- Time Plot')
    plt.xlabel('Time (seconds)')
    #plt.xticks(np.arange(min(sec_final),max(sec_final),500))
    plt.ylabel('Strain')

    plt.show()

    #final_data[i] = {'Temperature':temp, 'Internal Load':IL, 'Displacement':disp, 'Seconds': sec_list, 'L0': L0, 'Strain Rate Exp': SR_exp, 'Grain Size': d, 'Stress': stress, 'Strain Norm': strain_norm} #Diccionario    


    
