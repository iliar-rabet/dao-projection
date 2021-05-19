import matplotlib.pyplot as plt

PDR=[0.093,	0.545977011494,	0.97,	0.83,	0.74,	0.844660194175,	0.391304347826]
x=[5,15,25,35,45,55,85]
plt.ylabel('PDR [%]', fontweight ='bold') 
plt.xlabel('Nodes in the region [#]', fontweight ='bold') 
plt.plot(x, PDR,linestyle='dashed',label='SDMob')
# plt.plot(x, proj,label='RPL-RP')
plt.legend()
plt.show()