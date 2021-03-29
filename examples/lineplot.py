import matplotlib.pyplot as plt

file1 = open('pure', 'r') 
Lines1 = file1.readlines() 
pure=[]
for line in Lines1:
    pure.append(int(line))


file2 = open('proj', 'r') 
Lines2 = file2.readlines() 
proj=[]
for line in Lines2:
    proj.append(int(line))
del pure[-11:-1]
x=range(1,65)
plt.ylabel('E2E delay (millisecond)', fontweight ='bold') 
plt.xlabel('Time (second)', fontweight ='bold') 
plt.plot(x, pure,linestyle='dashed',label='RPL')
plt.plot(x, proj,label='RPL-RP')
plt.legend()
plt.show()