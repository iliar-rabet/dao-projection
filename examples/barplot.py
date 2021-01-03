import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.15
fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 
RPL = [98,0,64,116,46,64,80]

PROJ = [112,100,64,116,46,64,64]


# Set position of bar on X axis 
br1 = np.arange(7) 
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 

# Make the plot 
plt.bar(br1, RPL, color ='r', width = barWidth, 
		edgecolor ='grey', label ='RPL') 
plt.bar(br2, PROJ, color ='b', width = barWidth, 
		edgecolor ='grey', label ='Route Projection') 


# Adding Xticks 
plt.xlabel('Packet Type', fontweight ='bold') 
plt.ylabel('Packet Size (bytes)', fontweight ='bold') 
plt.xticks([r + barWidth for r in range(len(RPL))], 
		['DAO', 'PDAO','DAO-ACK', 'DIO', 'DIS','data(HBH)', 'data(SRH)']) 
plt.legend()
plt.show() 
