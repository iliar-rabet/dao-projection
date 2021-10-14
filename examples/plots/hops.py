import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.25
# fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 

PDR=[0.971896955503513,0.969798657718121,0.979865771812081,0.964285714285714]
Filter=[0.971896955503513,	0.969798657718121,	0.979865771812081,0.964285714285714]




# Set position of bar on X axis 
br1 = np.arange(3,len(PDR)+3) 
print(br1)
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 

colors = iter([plt.cm.tab20(i) for i in range(20)])

# next(colors)
# next(colors)
# next(colors)

plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
plt.xticks([r for r in range(3,7)], 
		['3','4','5','6'],fontsize=13) 

# Make the plot 
plt.bar(br1, Filter, width = barWidth, 
		edgecolor ='black', label ='Filter Reseliency [#]', color=[next(colors)]) 

next(colors)


plt.bar(br2, PDR,  width = barWidth, 
		edgecolor ='black', label ='Data PDR [#]',color=[next(colors)],hatch = '/') 


# plt.bar(br3, RPL,  width = barWidth, 
# 		edgecolor ='black', label ='RPL PDR [#]',color=[next(colors)],hatch = '/') 

# Adding Xticks 
plt.xlabel('Hop Distance [#]', fontweight ='bold',fontsize=13) 
plt.ylabel('Reception Ratio [%]', fontweight ='bold',fontsize=13) 


plt.yticks(fontsize=15)

plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)
plt.show() 

RMSE=[1.45338681798807,1.58,	1.49097110764395,	1.47911376438698]
plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
plt.xticks([r for r in range(3,7)], 
		['3','4','5','6'],fontsize=13) 

plt.bar(br1, RMSE, width = barWidth, 
		edgecolor ='black', label ='RMSE [m]', color=[next(colors)]) 
plt.xlabel('Hop Distance [#]', fontweight ='bold',fontsize=13) 
plt.ylabel('RMSE [m]', fontweight ='bold',fontsize=13) 




plt.show() 

# fig = plt.subplots(figsize =(14, 8)) 
delay=[179.383,247.218,268.157,291.104]
Hodelay=[61.871,	126.117,	156.024,197.142]	

plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)
plt.xticks([r for r in range(3,7)], 
		['3','4','5','6'],fontsize=13) 

plt.bar(br1, delay, width = barWidth, 
		edgecolor ='black', label ='E2E delay [ms]', color=[next(colors)]) 

plt.bar(br2, Hodelay, width = barWidth, 
		edgecolor ='black', label ='Handover delay [ms]', color=[next(colors)]) 

plt.xlabel('Hop Distance [#]', fontweight ='bold',fontsize=13) 
plt.ylabel('Delay [ms]', fontweight ='bold',fontsize=13) 

plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)

plt.show()
