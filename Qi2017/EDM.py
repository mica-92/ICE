## This is working but not the way of cutting data
## Revisar

import csv
from typing import final
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from pandas.core.frame import DataFrame
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
Q_DC = 181 # Dislocation Creep Activation Energy (KJ/mol)

# Reading Experiment Information from Experiment Master Sheet (EMS)
col_EMS = ['Experiment Number', 'Grain size', 'Original Lenght', 'Strain Rate', 'Sample Touch']
exp_EMS = pd.read_csv (f'D:\ICE\DATA\EMS.csv', names = col_EMS, skiprows=1)
experiment_number = pd.Series(exp_EMS['Experiment Number'])

col_EXP = ['Date', 'Time', 'Pressure', 'Temperature', 'Internal Load', 'External Load', 'Displacement', 'Intensifier', '6v', 'Bath Temperature', 'Piston13', 'Piston20', 'Seconds Travis']

#Loading experiment Data
final_data = {}
for i in experiment_number:
# Loading the CSV file for each experiment
    exp_data = pd.read_csv (f'D:\ICE\DATA\PIL{i}.csv', names = col_EXP, skiprows = 2)
    # Loading the data of the Experiment Master Sheet (EMS) fore each experiment
    loc = experiment_number[experiment_number == i].index[0] #determination of the row for each experiment
    L0 = exp_EMS['Original Lenght'][loc] # Original Sample Lenght
    SR_exp = exp_EMS['Strain Rate'][loc] # Target Strain Rate
    GS_exp = exp_EMS['Grain size'][loc] # Grain Size (Coarse, Standard or Fine )
    time_sample =  exp_EMS['Sample Touch'][loc] # Log of the touch sample moment

# Experiment Time Treatment
    ## Time to seconds  convention
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
    
    ## Location of the touch sample time
    time_loc = [n for n,i in enumerate(sec_list) if i> time_sample][0]

# Loading Temperature, Internal Load and Displacement from the Experiment Data
    temp = exp_data['Temperature'][time_loc:]
    IL = exp_data['Internal Load'][time_loc:]
    disp = exp_data['Displacement'][time_loc:]

    # Determination of d (grain size)
    if GS_exp == 'Coarse':
        d = 360e-06 # meters
    elif GS_exp == 'Standard':
        d = 230e-06
    else:
        d = 10e-06

# Raw Data Stress and Strain Calculation
    Lf_raw = L0 - disp * vtoinch
    stress_raw = IL * vtoIL_fine * Lf_raw / (sample_r**2 * math.pi * L0)
    strain_raw = np.log(L0 / Lf_raw)
    strain_norm_raw = strain_raw * np.exp((- Q_DC / R) * ((T_norm ** -1)-(temp**-1)))
    sec_list = sec_list[time_loc:]


# Slope Range determined by 
    def strain_rate_range(u,n=1):
        counter = 1
        u = str(f'{u:8f}')
        s = u.replace(".","") 
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
    SRR = strain_rate_range(SR_exp)
    #print (f'This is SRR for {i}', SRR)
    
# Cutting location according to slope
    def slope_calc(s):
        a = s
        values = []
        
        for i in range(0,(len(a)-1)):
            j = i+5
            if j <= (len(a)-1):
                slope, intercept, r_value, p_value, std_err = linregress (sec_list[i:j],strain_norm_raw[i:j])
            else:
                j = (len(a)-1)
                slope, intercept, r_value, p_value, std_err = linregress (sec_list[i:j],strain_norm_raw[i:j])
            values.append(slope)
        
        #First Cut
        condition = False
        h = 0
        while condition == False:
            if SRR[0] < values[h] < SRR[1]:
                condition = True
            else:
                h=h+1
        
        #Second Cut - Not sure if necessary
            #        condition_2 = False
            #        q = h
            #        while condition_2 == False:
            #            if values[q] < -4.5e-04:
            #                condition_2 = True
            #            else:
            #                q=q+1
        return h
    initial_cut = slope_calc(sec_list)
    #print(f'This is the loc cut for {i}', initial_cut)    
    
# Recalculation Strain and Stess with new displacent[0] for trimmed data
    # Por algun extraño motivo cuando tengo que hacer ranges necesito el numero de range pero si llamo un elemento necesito la posicion en relacion a la row original (?)
    disp_loc = time_loc + initial_cut
    Lf_final = L0 - (disp[initial_cut:]-disp[disp_loc]) * vtoinch
    stress = IL[initial_cut:] * vtoIL_fine * Lf_final / (sample_r**2 * math.pi * L0)
    strain_norm = np.log(L0 / Lf_final) * np.exp((- Q_DC / R) * ((T_norm ** -1)-(temp[initial_cut:]**-1)))

    #  Datos funcionando para todos menos para 33


    # Raw Data Plots
    fig, axs = plt.subplots(4)
    fig.suptitle(f'Raw Data Plots: PIL{i}')
    axs[0].plot(strain_norm, stress, color = 'darkblue')
    axs[0].set_title('Stress- Strain')
    axs[1].plot(sec_list[initial_cut:], strain_norm, color = 'red')
    axs[1].set_title('Strain- Time')

    axs[2].plot(strain_norm_raw, stress_raw, color = 'darkblue')
    axs[2].set_title('Raw Stress- Strain')
    axs[3].plot(sec_list, strain_norm_raw, color = 'red')
    axs[3].set_title('Raw Strain- Time')

    plt.show()




    #strain_loc = [n for n,i in enumerate(strain_norm) if i > 0.2][0]
    final_data[i] = {'Stress': stress, 'Strain': Lf_raw, 'IL': IL, 'LF': Lf_raw, 'DISLOC': initial_cut} #Diccionario    





