import matplotlib.pyplot as plt
import numpy as np

plt.plot([0,2,3,5], [0.8192, 0.6776, 0.6693, 0.61643],label='SDMob (Speed=1m/s)',
    linestyle='--',
    marker='o')

plt.plot([0,2,3,5], [0.59106,0.61074,0.60457,0.60204],label='mRPL (Speed=1m/s)',
    linestyle='--',
    marker='^')

plt.ylabel('PDR')
plt.xlabel('Path Loss Variance (dB)')
plt.legend()
plt.title('Speed =1m/s, data rate=1pkt/s')
plt.axis([0, 5, 0, 1])
plt.show()  



plt.plot([10,5,1,0.2], [0.75,0.819,0.77,0.716],label='SDMob',
    linestyle='--',
    marker='o')
plt.plot([10,5,1,0.2], [1.00, 0.67750,0.59106,0.23636],label='mRPL',
    linestyle='--',
    marker='^')

plt.ylabel('PDR')
plt.xlabel('Sampling rate (Packet/S)')
plt.legend()
plt.title('Speed =1m/s, Var=0')
plt.axis([0, 10, 0, 1])
plt.show()  



plt.plot([0,0.5,1,2], [0.975609756097561,0.92156862745098,0.650,0.664],label='SDMob',
    linestyle='--',
    marker='o')

plt.plot([0,0.5,1,2], [0.60204,0.60204,0.60204,0.53040],label='mRPL',
    linestyle='--',
    marker='^')

plt.ylabel('PDR')
plt.xlabel('Speed (m/s)')
plt.legend()
plt.title('Sampling rate= 1pkt/s, Var= 5dB')
plt.axis([0, 2, 0, 1])
plt.show()  
