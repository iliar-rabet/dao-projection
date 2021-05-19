import numpy as np
file1 = open('output.dat', 'r') 
Lines = file1.readlines() 
X=np.zeros(500)  
last = 0
count=0
# Strips the newline character 
for line in Lines: 
    if "hello" in line:
	str=line.split("hello ")[1].split("'")[0]
	i=int(str)
	X[i]=1

count=sum(X)
print(count)
	


