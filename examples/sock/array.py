
import sys
import numpy as np

mobile_nodes=1
try:
	if sys.argv[1]:
		filepath= sys.argv[1]
except IndexError:
	print("Using default file name.")
	filepath="../../../pymobility/rw.dat"


position = {}

with open(filepath) as fp:
   for line in fp:
        ip=str(int(line.split()[0])+1)
        time=float(line.split()[1])
        x=float(line.split()[2])
        y=float(line.split()[3])    
        if(int(line.split()[0])+1>mobile_nodes):
            
            temp=np.array([[x,y]])
            # print(temp)
            # print(line)
            # # landmarks=np.concatenate((landmarks,temp))
            landmarks=np.concatenate((landmarks,temp))
            # print(landmarks)
        position[(ip,time)]=(x,y)
        lastx=x
        lasty=y

def veloc(ip,T):
    # print(T)
    # print(window[ip])
    step=1
    return (position[(ip,T+step)][0]-position[(ip,T)][0],position[(ip,T+step)][1]-position[(ip,T)][1])

for t in range(1,600):
    print(position[(1,t)])