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

##### Strain Rates
exp_data = pd.read_csv ('D:/ICE/DM/rates.csv', names = col_names)
rates = exp_data['rate']
print(rates)
temp_warm = pd.Series(np.arange(258,274,1))

for row in temp_warm:
    t=[]
    SR = (1/(6e+28 * np.exp(-181/(0.0083145*temp_warm))))**(0.25)
    t.append(SR)
    print(t)

# Deformation Map Plot
fig, ax = plt.subplots(constrained_layout=True)
ax.plot(temp_warm, t, label='Boundary')
ax.set_xlabel('Temperature (K)', labelpad=10)
ax.set_ylabel('Stress (MPa)', labelpad=10)
ax.set_title(f'Deformation Mechanism Map\n Grain sizemeters')
#ax.legend() 
plt.show()

