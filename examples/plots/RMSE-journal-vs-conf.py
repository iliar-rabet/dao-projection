import matplotlib.pyplot as plt
import numpy as np

plt.plot([0.1,0.2,1,5], [0.6,0.6,0.6,0.6],label='SDMob-conf',
    linestyle='--',
    marker='o')
plt.plot([0.5,1,2,3,10], [0.49,0.41,0.52,0.49,0.43],label='SDMob-journal',
    linestyle='--',
    marker='^')

plt.ylabel('RMSE (m)')
plt.xlabel('inter packet interval (S)')
plt.legend()
plt.title('Speed =1m/s, Var=0')
plt.axis([0, 10, 0, 1])
plt.show()  
