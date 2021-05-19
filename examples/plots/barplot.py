import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 
RPL = [98,0,0,64,116,46,64,80]

PROJ = [112,100,71,64,116,46,64,64]


# Set position of bar on X axis 
br1 = np.arange(8) 
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 

colors = iter([plt.cm.tab20(i) for i in range(20)])

next(colors)
next(colors)
next(colors)

plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)


# Make the plot 
plt.bar(br1, RPL, width = barWidth, 
		edgecolor ='black', label ='RPL', color=[next(colors)]) 

next(colors)


plt.bar(br2, PROJ,  width = barWidth, 
		edgecolor ='black', label ='RPL-RP',color=[next(colors)],hatch = '/') 


# Adding Xticks 
plt.xlabel('Packet Type', fontweight ='bold',fontsize=17) 
plt.ylabel('Packet Size (bytes)', fontweight ='bold',fontsize=17) 


plt.xticks([r + barWidth for r in range(len(RPL))], 
		['DAO', 'PDAO', 'PDR', 'DAO-ACK', 'DIO', 'DIS','data\n(storing \nmode)', 'data\n(source \nrouted)'],fontsize=17) 
plt.yticks(fontsize=15)
plt.legend(fontsize=15)

plt.show() 
