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
plt.xlabel('E2E delay (ms)', fontweight ='bold') 
plt.ylabel('Packet number', fontweight ='bold') 
plt.plot(x, pure,linestyle='dashed',label='RPL')
plt.plot(x, proj,label='projected')
plt.legend()
plt.show()