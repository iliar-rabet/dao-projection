# imporing required modules 
import socket      
import datetime 
import time
import localization as lx
import math
import socket      
import datetime 
import time
import os
import select
import numpy as np
from filterpy.kalman import UnscentedKalmanFilter
from filterpy.kalman import (unscented_transform, MerweScaledSigmaPoints,
                             JulierSigmaPoints, SimplexSigmaPoints,
                             KalmanFilter)
from filterpy.common import Q_discrete_white_noise, kinematic_kf, Saver
from numpy.random import randn


def fx(x, dt):
    # state transition function - predict next state based
    # on constant velocity model x = vt + x_0
    F = np.array([[1, dt, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, dt],
                [0, 0, 0, 1]], dtype=float)
    return np.dot(F, x)

def hx(x):
# measurement function - convert state into a measurement
# where measurements are [x_pos, y_pos]
    return np.array([x[0], x[2]])

dt = 1
# create sigma points to use in the filter. This is standard for Gaussian processes
points = MerweScaledSigmaPoints(4, alpha=.1, beta=2., kappa=-1)

kf = UnscentedKalmanFilter(dim_x=4, dim_z=2, dt=dt, fx=fx, hx=hx, points=points)
kf.x = np.array([0., 0., 0., 0]) # initial state
kf.P *= 0.1 # initial uncertainty
z_std = 0.1
kf.R = np.diag([z_std**2, z_std**2]) # 1 standard
kf.Q = Q_discrete_white_noise(dim=2, dt=dt, var=0.01**2, block_size=2)


errs=0
count=0

P=lx.Project(mode='2D',solver='LSE')

filepath="lowlow"
vel = {}
position = {}
Window=63
lastx= 60
lasty= 60
with open(filepath) as fp:
   for line in fp:
    #    print(line.split())
        time=float(line.split()[1])
        x=float(line.split()[2])
        y=float(line.split()[3])    
        position.update({time:(x,y)})
        lastx=x
        lasty=y

rssfile="5m.dat"
c=0
rss={}
with open(rssfile) as fp:
   for line in fp:
           rss.update({line.split()[0]:line.split()[1]})

def veloc(T):
    T=T%Window
    print(T)
    return (position[T+1][0]-position[T][0],position[T+1][1]-position[T][1])


def actual(t):
    t=(t+1)%Window
    return position[t]


def RMSE(x,y,t):
    print("time: "+str(t))
    act=actual(float(t))
    print("actual: "+str(act))
    print("x,y:" + str(x)+" "+str(y))
    Xerr=x-act[0]
    Yerr=y-act[1]
    global errs
    global count
    error=math.sqrt(Xerr**2 + Yerr**2)
    errs+=error 
    count+=1
    print("AVG            : :: : :::::::"+str(errs/count))

    print("RMSE:"+str(error))

landmarks = np.array([[0,0],[0,0],[2,0],[4,0],[6,0],[8,0],[10,0],[12,0],[14,0],[16,0]]) #first one is dummy

P.add_anchor("0", (0, 0))
P.add_anchor("1", (0, 0))
P.add_anchor("2", (2, 0))
P.add_anchor("3", (4,0))
P.add_anchor("4", (6,0))
P.add_anchor("5", (8,0))
P.add_anchor("6", (10,0))
P.add_anchor("7", (12,0))
P.add_anchor("8", (14,0))
P.add_anchor("9", (16,0))
t,label=P.add_target()

# initializing socket 
s = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)      
host = "127.0.0.1"
port = 1234
  
# binding port and host 
s.bind((host, port))    
  
# waiting for a client to connect 
s.listen(5)   


def calculate_dist(RSSI):
    if(int(RSSI)<-94):
        return 5
    if(int(RSSI)>-17):
        return 0.2
    return rss.get(str(RSSI))
 
def closest(x,y,anchors_ind):
    dists=landmarks-[x,y]
    print(dists)
    dd=dists[:,0]**2 + dists[:,1]**2
    print(dd)
    for ind in range(len(anchors_ind)): 
        if anchors_ind[ind]!=1:
            dd[ind]=1000.0

    arg=np.argmin(dd)
    if(arg==0): 
        return "fd00:0:0:0:212:7404:4:404+fd00:0:0:0:212:7402:2:202"
        # return "fd00:0:0:0:212:7404:4:404"
    if(arg==1):
        return "fd00:0:0:0:212:7404:4:404+fd00:0:0:0:212:7403:3:303"
        # return "fd00:0:0:0:212:7404:4:404"
    if(arg==2):
        return "fd00:0:0:0:212:7404:4:404"
    if(arg==3):
        return "fd00:0:0:0:212:7405:5:505"
    if(arg==4):
        return "fd00:0:0:0:212:7406:6:606"
    if(arg==5):
        return "fd00:0:0:0:212:7407:7:707"
    if(arg==6): 
        return "fd00:0:0:0:212:7408:8:808"
    if(arg==7): 
        # return "fd00:0:0:0:212:7408:8:808"
        return "fd00:0:0:0:212:7408:8:808+fd00:0:0:0:212:7409:9:909"        
    if(arg==8): 
        return "fd00:0:0:0:212:7408:8:808+fd00:0:0:0:212:740a:a:a0a"
    if(arg==9): 
        return "fd00:0:0:0:212:7408:8:808+fd00:0:0:0:212:740a:a:a0a"
    return "None"


IPC_FIFO_NAME = "MYFIFO"
timeBase = 0
iterWait = 0

anchors_ind = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
zs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
 

try:
    os.mkfifo(IPC_FIFO_NAME)
except OSError:
    print("File Exists")
try:
    while True:
        # Reading from Pipe
        fifor = os.open(IPC_FIFO_NAME, os.O_RDONLY)
        line = os.read(fifor, 500).decode('utf8')
        line = line.split(';')
        line= line[0]
        time = int(line[6:10])
        print("\n******************************\nAt "+ str(time) + "\nReceived encoded data: " + line)
        os.close(fifor)

        if timeBase != time :
            timeBase = time
            anchors_ind = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            zs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            iterWait = 1
        else :
            iterWait += 1        

        dist = calculate_dist(int(line[2:5]))
        anchor = int(line[0:2], 16)
        anchor=anchor-1
        anchors_ind[anchor] = 1
        zs[anchor] = dist 
        print("meas:",str(anchor),str(dist))
        t.add_measure(str(anchor),dist)

        # User update
        if iterWait == 2:
            P.solve()
            print(t.loc)
            tmp=[t.loc.x,t.loc.y]
            kf.update(tmp)
            print("measured",kf.x)
            kf.x[1]=veloc(time)[0]
            kf.x[3]=veloc(time)[1]
            print("before prediction",kf.x)
            kf.predict()
            
            print("predicted",kf.x)
            
            RMSE(kf.x[0],kf.x[2],time)
            t.reset()
            content=closest(kf.x[0],kf.x[2],anchors_ind)
            print(content)
        else:
            content = "WAIT"


        # Writing to Pipe
        fifow = os.open(IPC_FIFO_NAME, os.O_WRONLY | os.O_TRUNC)
        os.write(fifow, content.encode('utf8'))
        os.close(fifow)

except KeyboardInterrupt:
    print("Exit deep here")
