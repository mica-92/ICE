import csv
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from scipy.stats import linregress
import datetime
import time

# Parameters Goldsby, Kohlstedt, Pappalardo (2001) - A COMPOSITE FLOW LAW FOR WATER ICE (...)

# Dislocation Creep Parameters
A_DC257 = 4e+05 # A <258 (MPa^-4 s^-1)
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
E = 9100 # Ice Young's Modulus (MPa)

d = 3e-04 # grain size (m)

# temperature
temp_data = pd.Series(np.arange(258,274,1)) #temperature series from 273 to 150
#print(temp_data)

for row in temp_data:
    DCGBS = []
    GBSBS = []

    # Individual Mechanims
    boundary_DC = A_DC259 * np.exp ((-Q_DC259)/ (R * temp_data)) / (d ** p_DC)
    boundary_GBS = A_GBS256 * np.exp ((-Q_GBS256)/ (R * temp_data)) / (d ** p_GBS)
    boundary_BS = A_BS * np.exp ((-Q_BS)/ (R * temp_data)) / (d ** p_GBS)

    #Boundaries 
    boundary_DCGBS = (boundary_GBS / boundary_DC) ** (1 / (n_DC/n_GBS))
    boundary_GBSBS = (boundary_GBS / boundary_BS) ** (1 / (n_BS/n_GBS))
    # unsure what's the problem with the following equation
    # boundary_DCGBS = ((A_GBS256 * np.exp ((-Q_GBS256)/ (R * temp_data)) / (d ** p_GBS)) / A_DC259 * np.exp ((-Q_DC259)/ (R * temp_data))) ** (1 / (n_DC/n_GBS))
    DCGBS.append(boundary_DCGBS)
    GBSBS.append(boundary_GBSBS)
    print(boundary_GBSBS)

plt.plot(temp_data, boundary_DCGBS, color = 'darkblue')
plt.plot(temp_data, boundary_GBSBS, color = 'red')
plt.title(f'Deformation Mechanism Map\n Grain size {d} meters')
#plt.xlabel('Time (seconds)')
#plt.ylabel('Strain')
plt.show()