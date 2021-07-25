import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

temp_warm = pd.Series(np.arange(258,274,1)) #temperature series from 273 to 150
temp_cold = pd.Series(np.arange(100,258,1))
temp = pd.Series(np.arange(100,274,1))


for row in temp_warm:
    DCGBS = []
    GBSBS = []

    # Individual Mechanims
    boundary_DC = A_DC259 * np.exp ((-Q_DC259)/ (R * temp_warm)) / (d ** p_DC)
    boundary_GBS = A_GBS256 * np.exp ((-Q_GBS256)/ (R * temp_warm)) / (d ** p_GBS)
    boundary_BS = A_BS * np.exp ((-Q_BS)/ (R * temp_warm)) / (d ** p_BS)

    #Boundaries 
    boundary_DCGBS259 = (boundary_GBS / boundary_DC) ** (1 / (n_DC/n_GBS))
    boundary_GBSBS259 = (boundary_GBS / boundary_BS) ** (1 / (n_BS/n_GBS))
    DCGBS.append(boundary_DCGBS259)
    GBSBS.append(boundary_GBSBS259)

for row in temp_cold:   
    # Individual Mechanims
    boundary_DC = A_DC257 * np.exp ((-Q_DC257)/ (R * temp_cold)) / (d ** p_DC)
    boundary_GBS = A_GBS254 * np.exp ((-Q_GBS254)/ (R * temp_cold)) / (d ** p_GBS)
    boundary_BS = A_BS * np.exp ((-Q_BS)/ (R * temp_cold)) / (d ** p_BS)

    #Boundaries 
    boundary_DCGBS257 = (boundary_GBS / boundary_DC) ** (1 / (n_DC/n_GBS))
    boundary_GBSBS257 = (boundary_GBS / boundary_BS) ** (1 / (n_BS/n_GBS))
    DCGBS.append(boundary_DCGBS257)
    GBSBS.append(boundary_GBSBS257)


#print(boundary_DCGBS259[0])
#print(boundary_GBSBS257[157])

m = (258-257)/(boundary_DCGBS259[0]-boundary_GBSBS257[157])
print(m)
b = (boundary_DCGBS259[0]*258-boundary_GBSBS257[157]*257)/(boundary_DCGBS259[0]-boundary_GBSBS257[157])
print (b)

y = m*temp + b
plt.plot(temp, y, '-r', label='y=2x+1')
plt.title('Graph of y=2x+1')
plt.xlabel('x', color='#1C2833')
plt.ylabel('y', color='#1C2833')
plt.legend(loc='upper left')
plt.grid()
plt.show()