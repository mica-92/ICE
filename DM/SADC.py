## Code for Strain Rates only with graph all temperatures

import csv
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import pandas as pd
import math
import numpy as np
from scipy.stats import linregress
import datetime
import time

col_names = ['rate']
# DC
A_DC257 = 1.2e+06 # A <258 (MPa^-4 s^-1) updated form Kuiper 2019 4e+05 original value
A_DC259 = 6e+28 # A >258 (MPa^-4 s^-1)
n_DC = 4 # stress exponent
p_DC = 0 # grain size exponent
Q_DC257 = 60 # activation energy <258 (KJ/mol)
Q_DC259 = 181 # activation energy >258 (KJ/mol)
# GBS Parameters
A_GBS254 = 3.9e-03 # A <258 (MPa^-1.8 m^1.4 s^-1)
A_GBS256 = 3e+26 # A >258 (MPa^-1.8 m^1.4 s^-1)
n_GBS = 1.8 # stress exponent
p_GBS = 1.4 # grain size exponent
Q_GBS254 = 49 # activation energy <255 (KJ/mol)
Q_GBS256 = 192 # activation energy >255 (KJ/mol)

# Variables
exp_data = pd.read_csv ('D:/ICE/DM/rates.csv', names = col_names)
rates = exp_data['rate']
temp_warm = pd.Series(np.arange(258,274,1))
temp_cold = pd.Series(np.arange(250,258,1))
temp = temp_cold.append(temp_warm)
d =  1e-03
R = 0.0083145 # gas constant (KJ/mol K)

SRDCdata_final={} #SRDC = strain rate dislocation creep
for i in rates:
    SRDCdata=[]
    for c in temp_cold:
        SRDC = ((i*(d**p_DC))/(A_DC257 * np.exp(-Q_DC257/(R*c))))**(n_DC ** -1)
        SRDC = np.array(SRDC)
        SRDCdata.append(SRDC)
    for j in temp_warm:
        SRDC = ((i*(d**p_DC))/(A_DC259 * np.exp(-Q_DC259/(R*j))))**(n_DC ** -1)
        SDCR = np.array(SRDC)
        SRDCdata.append(SRDC)
    SRDCdata_final[i]=SRDCdata.copy()
SRDC_final = pd.DataFrame(SRDCdata_final)

SRGBSdata_final={} #SRGBS = strain rate grain boundary sliding
for i in rates:
    SRGBSdata=[]
    for c in temp_cold:
        SRGBS = ((i*(d**p_GBS))/(A_GBS256 * np.exp(-Q_GBS256/(R*c))))**(n_GBS ** -1)
        SRGBS = np.array(SRGBS)
        SRGBSdata.append(SRGBS)
    for j in temp_warm:
        SRGBS = ((i*(d**p_GBS))/(A_GBS254 * np.exp(-Q_GBS254/(R*c))))**(n_GBS ** -1)
        SRGBS = np.array(SRGBS)
        SRGBSdata.append(SRGBS)
    SRGBSdata_final[i]=SRGBSdata.copy()
SRGBS_final = pd.DataFrame(SRGBSdata_final)

# Deformation Map Plot
fig, ax = plt.subplots(constrained_layout=True)
for k in range(len(SRDC_final.columns)):
    ax.plot(temp, SRDC_final.iloc[:,k], label="{:.2e}".format(rates[k]))
for k in range(len(SRGBS_final.columns)):
    ax.plot(temp, SRGBS_final.iloc[:,k], label="{:.2e}".format(rates[k]))
plt.yscale("log")
ax.set_xlabel('Temperature (K)', labelpad=10)
ax.set_ylabel('Stress (MPa)', labelpad=10)
ax.set_title(f'Deformation Mechanism Map\n Grain size {d} meters')
#ax.legend() 
plt.show()

