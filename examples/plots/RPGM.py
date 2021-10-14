import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 

PDR= [0.969798657718121,0.454545454545,0.195586760281]
Filter=[0.976,0.478827361563518,0.318132464712269]




# Set position of bar on X axis 
br1 = np.arange(len(PDR)) 
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 

colors = iter([plt.cm.tab20(i) for i in range(20)])

# next(colors)
# next(colors)
# next(colors)

plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)


# Make the plot 
plt.bar(br1, Filter, width = barWidth, 
		edgecolor ='black', label ='Filter Reseliency [#]', color=[next(colors)]) 

next(colors)


plt.bar(br2, PDR,  width = barWidth, 
		edgecolor ='black', label ='Data PDR [#]',color=[next(colors)],hatch = '/') 


# plt.bar(br3, RPL,  width = barWidth, 
# 		edgecolor ='black', label ='RPL PDR [#]',color=[next(colors)],hatch = '/') 

# Adding Xticks 
plt.xlabel('Number of nodes [#]', fontweight ='bold',fontsize=17) 
plt.ylabel('Reception Ratio [%]', fontweight ='bold',fontsize=17) 


plt.yticks(fontsize=15)
plt.legend(fontsize=15)

plt.show() 

RMSE=[1.58,1.36774218419935,1.87345106451568]

plt.bar(br1, RMSE, width = barWidth, 
		edgecolor ='black', label ='RMSE [m]', color=[next(colors)]) 
plt.xlabel('Number of nodes [#]', fontweight ='bold',fontsize=17) 
plt.ylabel('RMSE [m]', fontweight ='bold',fontsize=17) 

plt.show() 

fig = plt.subplots(figsize =(14, 8)) 
delay=[247.218,153.270,237.122]

plt.bar(br1, delay, width = barWidth, 
		edgecolor ='black', label ='E2E delay [ms]', color=[next(colors)]) 
plt.xlabel('Number of nodes [#]', fontweight ='bold',fontsize=17) 
plt.ylabel('E2E delay [ms]', fontweight ='bold',fontsize=17) 


plt.show()
