import csv
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

import pandas as pd
import math
import numpy as np
from scipy.stats import linregress
import datetime
import time

# Parameters Goldsby, Kohlstedt, Pappalardo (2001) - A COMPOSITE FLOW LAW FOR WATER ICE (...)

# Dislocation Creep Parameters
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

# Basal Slip Parameters
A_BS = 5.5e+07 # A
n_BS = 2.4 # stress exponent
p_BS = 0 # grain size exponent
Q_BS = 60 # activation energy <258 (KJ/mol)

# Other Parameters
R = 0.0083145 # gas constant (KJ/mol K)
EE = 9100 # Ice Young's Modulus (MPa)

d = 1e-03 # grain size (m)

# temperature
temp_warm = pd.Series(np.arange(258,274,1)) #temperature series from 273 to 150
temp_cold = pd.Series(np.arange(150,258,1))
# temp_data = pd.Series(np.arange(150,274,1)) 
# there has to be a way to create an if ... then use this and this equation if not...
#print(temp_data)

for row in temp_warm:
    DCGBS = []
    GBSBS = []

    # Individual Mechanims
    boundary_DC = A_DC259 * np.exp ((-Q_DC259)/ (R * temp_warm)) / (d ** p_DC)
    boundary_GBS = A_GBS256 * np.exp ((-Q_GBS256)/ (R * temp_warm)) / (d ** p_GBS)
    boundary_BS = A_BS * np.exp ((-Q_BS)/ (R * temp_warm)) / (d ** p_GBS)

    #Boundaries 
    boundary_DCGBS259 = (boundary_GBS / boundary_DC) ** (1 / (n_DC/n_GBS))
    boundary_GBSBS259 = (boundary_GBS / boundary_BS) ** (1 / (n_BS/n_GBS))
    DCGBS.append(boundary_DCGBS259)
    GBSBS.append(boundary_GBSBS259)

for row in temp_cold:   
    # Individual Mechanims
    boundary_DC = A_DC257 * np.exp ((-Q_DC257)/ (R * temp_cold)) / (d ** p_DC)
    boundary_GBS = A_GBS254 * np.exp ((-Q_GBS254)/ (R * temp_cold)) / (d ** p_GBS)
    boundary_BS = A_BS * np.exp ((-Q_BS)/ (R * temp_cold)) / (d ** p_GBS)

    #Boundaries 
    boundary_DCGBS257 = (boundary_GBS / boundary_DC) ** (1 / (n_DC/n_GBS))
    boundary_GBSBS257 = (boundary_GBS / boundary_BS) ** (1 / (n_BS/n_GBS))
    DCGBS.append(boundary_DCGBS257)
    GBSBS.append(boundary_GBSBS257)


##### Strain Rates
col_namesi = ['rate']
exp_data = pd.read_csv ('D:/ICE/DM/rates.csv', names = col_namesi)
rates = exp_data['rate']

for row in temp_warm:
    t=[]
    SR = ((1)/(6e+28 * np.exp(-181/(0.0083145*temp_warm))))**(0.25)
    t.append(SR)
    #print(t)




# Series Append - unsure what is not working of DCGBS
temp = temp_cold.append(temp_warm)
bound = boundary_DCGBS257.append(boundary_DCGBS259)

# Deformation Map Plot
fig, ax = plt.subplots(constrained_layout=True)

#Boundary DC-GBS 
ax.plot(temp, bound, color='#F4AC32', linestyle='dashed', linewidth=3)
ax.plot(temp_warm, t)
#Boundary GBS-BS
#ax.plot(temp_cold, boundary_GBSBS257, label='Boudnary II')

plt.yscale("log")
ax.set_xlabel('Temperature (K)', labelpad=10)
ax.set_ylabel('Stress (MPa)', labelpad=10)
ax.set_title(f'Deformation Mechanism Map\n Grain size {d} meters')
ax.fill_between(temp, 10e-6, bound, facecolor='#FACC6B', alpha=0.3, label='Grain Boundary Sliding')
ax.fill_between(temp, bound, 1000, facecolor='#FFD131', alpha=0.3, label='Dislocation Creep' )
ax.text(220, 30, 'Dislocation\nCreep', fontweight='bold', color = '#271902', path_effects=[pe.withStroke(linewidth=5, foreground='w')])
ax.text(180, 0.001, 'Grain Boundary\nSliding', fontweight='bold', color = '#271902', path_effects=[pe.withStroke(linewidth=5, foreground='w')])


# Secondary XAxis
def THT(x):
    return x / 273
def tht(x):
    return 273 * x
secax = ax.secondary_xaxis('top', functions=(THT, tht))
secax.set_xlabel('T/Tm', labelpad=10)

# Secondary XAxis
def SEE(y):
    return y / EE
def EES(y):
    return EE * y
secay = ax.secondary_yaxis('right', functions=(SEE, EES))
secay.set_ylabel('Stress / E', labelpad=10)

ax.legend
plt.show()