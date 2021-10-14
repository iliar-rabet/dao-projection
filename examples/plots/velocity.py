import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 

br1=[0.6,1.2,1.8,2.5]
PDR=[0.953068592058,0.685920577617329	,	0.50, 0.381294964028777]
filt=[0.843333333333333,	0.434782608695652,	0.40,0.33	]


RMSE= [0.549565647199233,	1.46701442321579,	1.5,	1.61898528915896]


# OH=[1149, 1215	1721]

# Set position of bar on X axis 
br1 = np.arange(4) 
br2 = [x + barWidth for x in br1] 
# br3 = [x + barWidth for x in br2] 

colors = iter([plt.cm.tab20(i) for i in range(20)])

# next(colors)
# next(colors)
# next(colors)

plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)


# Make the plot 
plt.bar(br1, RMSE, width = barWidth, 
		edgecolor ='black', label ='SDMob', color=[next(colors)]) 


# Adding Xticks 
plt.xlabel('Velocity (m/s)', fontweight ='bold',fontsize=17) 
plt.ylabel('RMSE (m)', fontweight ='bold',fontsize=17) 


plt.xticks(br1, 
		['0.6', '1.2', '1.8', '2.4'],fontsize=17) 
plt.yticks(fontsize=15)
plt.legend(fontsize=15)

plt.show() 


fig = plt.subplots(figsize =(12, 8)) 
plt.bar(br1, filt, width = barWidth, 
		edgecolor ='black', label ='SDMob', color=[next(colors)]) 
plt.bar(br2, PDR, width = barWidth, 
		edgecolor ='black', label ='SDMob', color=[next(colors)]) 
plt.legend(fontsize=15)
plt.xticks(br1, 
		['1', '2', '3'],fontsize=17) 
plt.xlabel('Velocity (m/s)', fontweight ='bold',fontsize=17) 
plt.ylabel('Reception Ratio (%)', fontweight ='bold',fontsize=17) 

plt.show() 
