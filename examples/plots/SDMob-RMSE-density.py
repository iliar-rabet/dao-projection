import matplotlib.pyplot as plt

RMSE=[3.5,2.35912891518766,0.882403643575027,0.994499010843885,0.97583936214235,0.939375632974118,1.16130832597422]
x=[5,15,25,35,45,55,85]
plt.ylabel('RMSE [m]', fontweight ='bold') 
plt.xlabel('Nodes in the region [#]', fontweight ='bold') 
plt.plot(x, RMSE,linestyle='dashed',label='SDMob')
# plt.plot(x, proj,label='RPL-RP')
plt.legend()
plt.show()