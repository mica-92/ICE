import matplotlib.pyplot as plt
import numpy as np
import datetime
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator

fig, ax = plt.subplots(constrained_layout=True)
x = np.arange(150, 274, 1)
y = np.sin(2 * x * np.pi / 180)
ax.plot(x, y)
ax.set_xlabel('Temperature')
ax.set_ylabel('Stress')
ax.set_title('This is a trial :)')


def HT(x):
    return x / 273


def rad2deg(x):
    return 273 * x


secax = ax.secondary_xaxis('top', functions=(HT, rad2deg))
secax.set_xlabel('angle [rad]')
plt.show()