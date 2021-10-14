import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.25
# fig = plt.subplots(figsize =(12, 8)) 

# set height of bar 

PDR=[0.633136094675,0.7,0.846153846154,0.990990990991,0.021822849807445]
Filter=[0.723032069970845,0.71,0.88,0.976909413854352,0.217672413793103]




# Set position of bar on X axis 
br1 = np.arange(2,len(PDR)+2) 
print(br1)
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
plt.xlabel('Number of neighbors [#]', fontweight ='bold',fontsize=17) 
plt.ylabel('Reception Ratio [%]', fontweight ='bold',fontsize=17) 


plt.yticks(fontsize=15)
plt.legend(fontsize=15)

plt.show() 

RMSE=[1.43394533652394,1.44394533652394,1.45860840464733,1.47824637203261,2.45796016765343]
# fig = plt.subplots(figsize =(14, 8)) 
plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)

plt.bar(br1, RMSE, width = barWidth, 
		edgecolor ='black', label ='RMSE [m]', color=[next(colors)]) 
plt.xlabel('Number of neighbors [#]', fontweight ='bold',fontsize=17) 
plt.ylabel('RMSE [m]', fontweight ='bold',fontsize=17) 

plt.show() 

# fig = plt.subplots(figsize =(14, 8)) 
plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)

delay=[191.863,200.1,209.961,218.996,	861.0759]

plt.bar(br1, delay, width = barWidth, 
		edgecolor ='black', label ='E2E delay [ms]', color=[next(colors)]) 
plt.xlabel('Number of neighbors [#]', fontweight ='bold',fontsize=17) 
plt.ylabel('E2E delay [ms]', fontweight ='bold',fontsize=17) 


plt.show()
