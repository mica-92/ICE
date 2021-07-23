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

##### Strain Rates
exp_data = pd.read_csv ('D:/ICE/DM/rates.csv', names = col_names)
rates = exp_data['rate']
#print(rates)
temp_warm = pd.Series(np.arange(258,274,1))

data_final={}
for i in rates:
    data=[]
    for j in temp_warm:
        SR = (i/(6e+28 * np.exp(-181/(0.0083145*j))))**(0.25)
        SR = np.array(SR)
        data.append(SR)
    data_final[i]=data.copy()
df = pd.DataFrame(data_final)
#print(df)

# Deformation Map Plot
fig, ax = plt.subplots(constrained_layout=True)
for k in range(len(df.columns)):
    ax.plot(temp_warm, df.iloc[:,k], label="{:.2e}".format(rates[k]))
plt.yscale("log")
ax.set_xlabel('Temperature (K)', labelpad=10)
ax.set_ylabel('Stress (MPa)', labelpad=10)
ax.set_title(f'Deformation Mechanism Map\n Grain sizemeters')
ax.legend() 
plt.show()

