import matplotlib.pyplot as plt
import numpy as np

plt.plot(
    [0.1,0.5,1,2,10],
    [2255398,1300239,2292732,2363181,3740368],label='SDMob-conf',
    linestyle='--',
    marker='o')
    

plt.plot([0.5,1,2,3,10],[2751770,645824,3678727,3841209,4754058],label='SDMob-journal',
    linestyle='--',
    marker='^')
    


plt.ylabel('Delay (mS)')
plt.xlabel('inter packet interval (S)')
plt.legend()
plt.title('Speed =1m/s, Var=0')
plt.axis([0, 10, 0, 4754058])
plt.show()  
