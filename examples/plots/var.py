import numpy as np 
import matplotlib.pyplot as plt 

# set width of bar 
barWidth = 0.25

# set height of bar 
RMSE = [0.342729723846969,0.457385533873519, 0.622233461736293, 0.803722671477317]
resil=[0.989966555183946,	0.983277591973244,	0.959866220735786,	0.946488294314381] 
PDR=[0.95673992674,	0.956204379562,	0.916,	0.855]



# Set position of bar on X axis 
br1 = np.arange(4) 
br2 = [x + barWidth for x in br1] 
# br3 = [x + barWidth for x in br2] 

colors = iter([plt.cm.tab20(i) for i in range(20)])

# next(colors)
# next(colors)
# next(colors)

# plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)



#----------------------------------


# Make the plot 
plt.bar(br1, resil, width = barWidth, 
		edgecolor ='black', label ='Control', color=[next(colors)]) 

color=[next(colors)]

plt.bar(br2, PDR, width = barWidth, 
		edgecolor ='black', label ='Data', color=[next(colors)],hatch='/') 

# Adding Xticks 
plt.xlabel('Path Loss Variance [$dB^2$]', fontweight ='bold',fontsize=15) 
plt.ylabel('Reception Ratio [%]', fontweight ='bold',fontsize=15) 


plt.xticks(br1, 
		['0', '5', '10', '15'],fontsize=15) 
plt.yticks(fontsize=15)
plt.ylim([0.7, 1])
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=3, fancybox=True, shadow=True,fontsize=15)

plt.subplots_adjust(bottom=0.15,left=0.15)

plt.show() 


# Make the plot 
plt.bar(br1, RMSE, width = barWidth, 
		edgecolor ='black', color=[next(colors)]) 


# Adding Xticks 
plt.xlabel('Path Loss Variance [$dB^2$]', fontweight ='bold',fontsize=15) 
plt.ylabel('Localization error [m]', fontweight ='bold',fontsize=15) 


plt.xticks(br1, 
		['0', '5', '10', '15'],fontsize=15) 
plt.yticks(fontsize=15)
plt.legend(fontsize=10)
plt.subplots_adjust(bottom=0.15)

plt.show() 


