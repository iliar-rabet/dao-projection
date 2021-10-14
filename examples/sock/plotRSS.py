from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import math
fig, ax = plt.subplots(1, 1)
x_axis=12
tx=6
x1 = np.linspace(0.5,tx+0.5, 100)
x2 = np.linspace(5,x_axis-0.5, 100)
eta=10
d=1
y1= -20 - 10*eta* np.log10(x1/d)
y2= -20 - 10*eta* np.log10((x_axis-x2)/d)

plt.xlabel('time [s]',fontsize=14)
plt.ylabel('RSSI [dB]',fontsize=14) 

ax.axhline(y=-90, color='k', linestyle='-')

ax.plot(x1, y1,'b.', lw=2, alpha=0.6, label='$R_a$')
ax.plot(x2, y2,'r.', lw=2, alpha=0.6, label='$R_b$')
plt.legend(fontsize=14)
plt.show()