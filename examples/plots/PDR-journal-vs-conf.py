import matplotlib.pyplot as plt
import numpy as np

plt.plot([0.1,0.2,1,5], [0.75,0.819,0.77,0.716],label='SDMob-conf',
    linestyle='--',
    marker='o')
plt.plot([0.5,1,2,3,10], [0.96,0.97,0.92,0.93,0.96],label='SDMob-journal',
    linestyle='--',
    marker='^')

plt.ylabel('PDR')
plt.xlabel('inter packet interval (S)')
plt.legend()
plt.title('Speed =1m/s, Var=0')
plt.axis([0, 10, 0, 1])
plt.show()  
