import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.025
#fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 
particle_line = [0.566147244933,0.566147244933]
particle_cir = [0.63188589771,0.972161651262]

ukf_line = [0.724651076994, 0.89]
ukf_cir = [0.824651076994, 1.97326041542]


# Set position of bar on X axis 
br1 = [0.85, 1.0] 
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 
br4 = [x + barWidth for x in br3] 

colors = iter([plt.cm.tab20(i) for i in range(20)])

next(colors)
next(colors)
next(colors)

plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)


# Make the plot 
plt.bar(br1, particle_line, width = barWidth, 
		edgecolor ='black', label ='Particle Linear', color=[next(colors)]) 

next(colors)


plt.bar(br2, particle_cir,  width = barWidth, 
		edgecolor ='black', label ='Particle Circle',color=[next(colors)],hatch = 'x') 

plt.bar(br3, ukf_line,  width = barWidth, 
		edgecolor ='black', label ='UKF Linear',color=[next(colors)],hatch = '/') 
plt.bar(br4, ukf_cir,  width = barWidth, 
		edgecolor ='black', label ='UKF Circle',color=[next(colors)],hatch = '-') 


# Adding Xticks 
plt.xlabel('Mobile Node Speed (m/s)', fontweight ='bold',fontsize=14) 
plt.ylabel('RMSE (m)', fontweight ='bold',fontsize=14) 

legend_properties = {'weight':'bold', 'size':'13'}


plt.xticks([0.895,1.045], 
		['0.5','1.0'],fontsize=14) 
plt.yticks(fontsize=15)
plt.legend(prop=legend_properties)
plt.title("SDMob's Accuracy; Data Interval: 1 s,\n Path Loss Variance=0",fontsize=15)

plt.show() 
