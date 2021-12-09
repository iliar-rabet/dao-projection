import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.1


# set height of bar 


filt= [0.989966555183946, 0.855704697986577, 0.788888888888889]
PDR= [0.95673992674, 0.817073170731707,0.65]
RPL=[0.21694915254237288,0.418079096045, 0.500619578686]
ARMOR=[0.47,0.49,0.41]



RMSE = [0.342729723846969, 1.26502796191238, 2.00818310163831]

delay=[123,	153, 237]
RPL_delay=[263,239,122]
ARMOR_delay=[129.31,151.56,230.17]

# Set position of bar on X axis 
br1 = np.arange(2,len(PDR)+2) /2.0
print(br1)
br2 = [x + barWidth for x in br1] 
br3 = [x + barWidth for x in br2] 

colors = iter([plt.cm.tab20(i) for i in range(20)])


# Make the plot 
# plt.bar(br1, filt, width = barWidth, 
# 		edgecolor ='black', label ='SDMob\'s Control', color=[next(colors)]) 



plt.bar(br1, PDR,  width = barWidth, 
		edgecolor ='black', label ='SDMob',color=[next(colors)],hatch = '/') 
next(colors)

plt.bar(br2, RPL,  width = barWidth, 
		edgecolor ='black', label ='RPL',color=[next(colors)],hatch = '+') 

plt.bar(br3, ARMOR,  width = barWidth, 
		edgecolor ='black', label ='ARMOR',color=[next(colors)]) 

plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True, fontsize=15)

plt.xticks(br1, 
		['1', '2', '3'],fontsize=15) 
plt.yticks(fontsize=15)
plt.xlabel('Number of MNs', fontweight ='bold',fontsize=15) 
plt.ylabel('Reception Ratio [%]', fontweight ='bold',fontsize=15) 

plt.show() 


plt.subplots_adjust(left=0.15)

# Make the plot 
plt.bar(br1, RMSE, width = barWidth, 
		edgecolor ='black', label ='SDMob', color=[next(colors)]) 


# Adding Xticks 
plt.xlabel('Number of MNs', fontweight ='bold',fontsize=15) 
plt.ylabel('Localization Error [m]', fontweight ='bold',fontsize=15) 


plt.xticks(br1, 
		['1', '2', '3'],fontsize=15) 
plt.yticks(fontsize=15)
# plt.legend(fontsize=15)

plt.show() 



plt.bar(br1, delay, width = barWidth, 
		edgecolor ='black', label ='SDMob', color=[next(colors)]) 
plt.bar(br2,RPL_delay, width = barWidth, 
		edgecolor ='black', label ='RPL', color=[next(colors)]) 
plt.bar(br3,ARMOR_delay, width = barWidth, 
		edgecolor ='black', label ='ARMOR', color=[next(colors)]) 

# plt.legend(fontsize=15)
plt.xticks(br1, 
		['1', '2', '3'],fontsize=15) 
plt.xlabel('Number of MNs', fontweight ='bold',fontsize=15) 
plt.ylabel('E2E Delay [ms]', fontweight ='bold',fontsize=15) 
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True, fontsize=15)

plt.show() 


RPL_OH=[1219, 1357, 2663]
OH=[2554,3602,4658]

plt.xlabel('Number of MNs', fontweight ='bold',fontsize=15) 
plt.ylabel('Communication Overhead [bytes]', fontweight ='bold',fontsize=15) 

plt.bar(br1, OH, width = barWidth, 
		edgecolor ='black', label ='SDMob', color=[next(colors)]) 
plt.bar(br2,RPL_OH, width = barWidth, 
		edgecolor ='black', label ='RPL', color=[next(colors)]) 
plt.xticks(br1, 
		['1', '2', '3'],fontsize=15) 
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True, fontsize=15)

plt.show() 
