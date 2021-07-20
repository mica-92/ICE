import csv
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy.stats import linregress



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

exp_data = pd.read_csv ('D:\ICE\Qi-2017\MICA\PIL19t.csv',names=col_names, skiprows=50, skipfooter=0)

# Machine Parameters
vtoinch = 0.17153
vtoIL_coarse = 1280 #high stresses or very cold conditions
vtoIL_fine = 202

# Experiment Parameters
L0 = 2.2 #inches
strain_rate = 5e+05 #constant
temp = exp_data['Temperature']
IL = exp_data['Internal Load']
disp = exp_data['Displacement']
disp0 = disp[0]
Lf = L0 - (disp - disp0) * vtoinch
sample_r = 0.55 #inches includes sample plus iridium jacket
time = exp_data['TimeSec']
Q_DC = 181 #KJ/mol
R = 0.0083145 #KJ/mol
T_norm = 263.55 #how was this calculated

stress = IL * vtoIL_fine * Lf / (sample_r**2 * math.pi * L0)
strain = np.log(L0 / Lf)
strain_norm = strain * np.exp((- Q_DC / R) * ((T_norm ** -1)-(temp**-1)))


print(type(disp0))

print(type(disp))
#print(strain)
#print(time)


# Plots
#plot_TS = plt.plot(strain_norm, stress)
#plt.title('Strain- Stress Plot')
#plt.show()
