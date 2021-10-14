import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 

PDR= [0.8625,0.736196319018,0.955172413793,0.892733564014]
Filter=[0.846153846153846,0.931818181818182,0.959731543624161,0.912751677852349]
RPL=[0.846153846153846,0.931818181818182,0.959731543624161,0.912751677852349]



# Set position of bar on X axis 
br1 = np.arange(4) 
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


plt.xlabel('Mobility Pattern', fontweight ='bold',fontsize=17) 
plt.ylabel('Reception Ratio', fontweight ='bold',fontsize=17) 


plt.xticks([r + barWidth for r in range(len(RPL))], 
		['GM','RDM','TLW','RWP'],fontsize=17) 
plt.yticks(fontsize=15)
plt.legend(fontsize=15)

plt.show()


#-------------------------------------

fig = plt.subplots(figsize =(12, 8)) 
RMSE=[1.3397689571856,2.24696197677873,0.903944417559751,2.50639613074245]

plt.bar(br1, RMSE, width = barWidth, 
		edgecolor ='black', label ='RMSE [m]', color=[next(colors)]) 
plt.xticks([r for r in range(len(RPL))], 
		['GM','RDM','TLW','RWP'],fontsize=17) 


plt.xlabel('Mobility Pattern', fontweight ='bold',fontsize=17) 
plt.ylabel('$Error_{Root Mean Squared} (m)$', fontweight ='bold',fontsize=17) 

plt.show() 

#----------------
fig = plt.subplots(figsize =(12, 8)) 
delay=[155.476,166.925,123.690,134.327]
plt.xticks([r for r in range(len(RPL))], 
		['GM','RDM','TLW','RWP'],fontsize=17) 

plt.bar(br1, RMSE, width = barWidth, 
		edgecolor ='black', label ='E2E delay [ms]', color=[next(colors)]) 
plt.xlabel('Mobility Pattern', fontweight ='bold',fontsize=17) 
plt.ylabel('$Delay (ms)$', fontweight ='bold',fontsize=17) 


plt.show()
