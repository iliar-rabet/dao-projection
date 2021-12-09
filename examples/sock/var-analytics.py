import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 1
#fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 
particle_line = [0.786068/10.0, 0.878285/10.0,1.089896/10.0,1.333744/10.0]




# Set position of bar on X axis 
br1 = [0,5,10,15] 
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 
br4 = [x + barWidth for x in br3] 

colors = iter([plt.cm.tab20(i) for i in range(20)])

next(colors)
next(colors)
next(colors)

# plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)


# Make the plot 
plt.bar(br1, particle_line, width = barWidth, 
		edgecolor ='black'
        , color=[next(colors)]) 


# Adding Xticks 
plt.xlabel('($\sigma$) Standard Deviation in RSSI[dB]',fontsize=14) 
plt.ylabel('Packet Loss Probability', fontsize=14) 

legend_properties = {'weight':'bold', 'size':'13'}


plt.xticks([0,5,10,15], 
		['0','5','10','15'],fontsize=14) 
plt.yticks(fontsize=15)
plt.subplots_adjust(bottom=0.15,left=0.15)

# plt.legend(prop=legend_properties)
# plt.title("SDMob's Accuracy; Data Interval: 1 s,\n Path Loss Variance=0",fontsize=15)

plt.show() 
