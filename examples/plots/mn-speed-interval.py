import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 


filt= [0.989966555183946, 0.855704697986577, 0.788888888888889]
PDR= [0.95673992674, 0.817073170731707,0.65]

RMSE = [0.342729723846969, 1.26502796191238, 2.00818310163831]

# OH=[1149, 1215	1721]

# Set position of bar on X axis 
br1 = np.arange(3) 
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
plt.xlabel('Number of mobile nodes (#)', fontweight ='bold',fontsize=17) 
plt.ylabel('RMSE (m)', fontweight ='bold',fontsize=17) 


plt.xticks(br1, 
		['1', '2', '3'],fontsize=17) 
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
plt.xlabel('Number of mobile nodes (#)', fontweight ='bold',fontsize=17) 
plt.ylabel('Reception Ratio (%)', fontweight ='bold',fontsize=17) 

plt.show() 
