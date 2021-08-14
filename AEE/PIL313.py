from collections import Counter
from nptdms import TdmsFile
import csv
from os import read
from typing import final
import matplotlib.pyplot as plt
from numpy.lib.function_base import average
import pandas as pd
import math
import numpy as np
from pandas.core.frame import DataFrame
from scipy.stats import linregress
import scipy
import datetime
import time
import seaborn as sns
import random

# Reading Experiment Information from Experiment Master Sheet (EMS)
col_EMS = ['Experiment Number', 'Date', 'Target Temperature', 'Grain Size', 
            'Target Strain Rate', 'Initial Length', 'Final Length', 'Target Pressure', 'Internal Axial Load Read', 'Storage', 'Sample Touch']
exp_EMS = pd.read_csv (f'D:\ICE\AEE\AEEM.csv', names = col_EMS, skiprows=1)
experiment_number = pd.Series(exp_EMS['Experiment Number'])

# Machine Parameters
vtoinch = 0.17153
vtoIL_coarse = 1280 #high stresses or very cold conditions
vtoIL_fine = 202
sample_r = 0.55
R = 0.0083145 #KJ/mol
T_norm = 263 #Leaving this constant but this can be another column in EMS
Q_DC = 181 # Dislocation Creep Activation Energy (KJ/mol)

#Loading experiment Data
count_experiment = 0
final_data = {}
for i in experiment_number:
# Loading the CSV file for each experiment
    tdms_file = TdmsFile.read(f'D:\ICE\DATA\PIL314.tdms')
    print(tdms_file)