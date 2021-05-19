#import matplotlib.pyplot as plt
import numpy as np
from numpy.random import uniform 
from filterpy.monte_carlo import systematic_resample
from numpy.linalg import norm
from numpy.random import randn
import scipy.stats
from numpy.random import uniform
from numpy.random import seed
import math
import socket      
import datetime 
import time
import os
import select

summation=0
count=0

filepath="lowlow.dat"
vel = {}
position = {}
Window=63
lastx= 0
lasty= 0
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
        #    print(line.split())
           rss.update({line.split()[0]:line.split()[1]})
print(rss)
N = 20000  # number of points


def actual(t):
    t=(t+1)%Window
    return position[t]


def RMSE(x,y,t):
    act=actual(float(t))
    Xerr=x-act[0]
    Yerr=y-act[1]
    error=math.sqrt(Xerr**2 + Yerr**2)
    global summation
    global count
    summation=error + summation
    count=count+1
    print("AVG            ::::::::::::::::::::::::::::   "+str(summation/count))
    print("RMSE:"+str(error))

def create_uniform_particles(x_range, y_range, N):
    particles = np.empty((N, 2))
    particles[:, 0] = uniform(x_range[0], x_range[1], size=N)
    particles[:, 1] = uniform(y_range[0], y_range[1], size=N)
    return particles

 

def create_gaussian_particles(mean, std, N):
    particles = np.empty((N, 3))
    particles[:, 0] = mean[0] + (randn(N) * std[0])
    particles[:, 1] = mean[1] + (randn(N) * std[1])
    particles[:, 2] = mean[2] + (randn(N) * std[2])
    particles[:, 2] %= 2 * np.pi
    return particles

 


def update(particles, weights, z, R, landmarks,anchors):
    for i, landmark in enumerate(landmarks):
        if(anchors[i]==1):
            distance = np.linalg.norm(particles - landmark,axis=1)            
            weights *= scipy.stats.norm(distance, R).pdf(float(z[i]))

 

    weights += 1.e-300      # avoid round-off to zero
    weights /= sum(weights) # normalize



 

def calculate_dist(RSSI):
    if(int(RSSI)<-94):
        return 5
    if(int(RSSI)>-17):
        return 0.2
    return rss.get(str(RSSI))
 

def predict(particles, u, std, dt=1.):
    """ move according to control input u (velocity in x, velocity in y)
    with noise Q (std heading change, std velocity)`"""
    N = len(particles)
    # update heading
    #particles[:, 2] += u[0] + (randn(N) * std[0])
    #particles[:, 2] %= 2 * np.pi

    # move in the (noisy) commanded direction
    dist = (u[0] * dt) + (randn(N) * std[1])
    particles[:, 0] += dist
    dist = (u[1] * dt) + (randn(N) * std[1])
    particles[:, 1] += dist
 

def estimate(particles, weights):
    """returns mean and variance of the weighted particles"""

    pos = particles[:, 0:2]
    mean = np.average(pos, weights=weights, axis=0)
    var  = np.average((pos - mean)**2, weights=weights, axis=0)
    maximum=max(weights)
    index=np.argmax(weights)
    return mean, var

 
def neff(weights):
    return 1. / np.sum(np.square(weights))

 

def resample_from_index(particles, weights, indexes):
    particles[:] = particles[indexes]
    weights[:] = weights[indexes]
    weights.fill(1.0 / len(weights))


def simple_resample(particles, weights):
    N = len(particles)
    cumulative_sum = np.cumsum(weights)
    cumulative_sum[-1] = 1. # avoid round-off error
    indexes = np.searchsorted(cumulative_sum, random(N))
    # print("resampling!!!!!")

    # resample according to indexes
    particles[:] = particles[indexes]
    weights.fill(1.0 / N)

 

 
def closest(x,y,anchors_ind):
    dists=landmarks-[x,y]
    # print(dists)
    dd=dists[:,0]**2 + dists[:,1]**2
    # print(dd)
    # for ind in range(len(anchors_ind)): 
    #     if anchors_ind[ind]!=1:
    #         dd[ind]=1000.0

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

# def vel(T):
#     T=T % 20
#     if(T<10):
#         return 10,0
#     else:
#         return -10,0

def veloc(T):
    T=T%Window
    print(T)
    return (position[T+1][0]-position[T][0],position[T+1][1]-position[T][1])
    # return (vel[str(T)][0]*5,vel[str(T)][1]*5)


sensor_std_err=.1
initial_x=None

# landmarks = np.array([[70, 70],[41, 65],[60, 80],[60, 40],[60, 50],[70, 40],[70, 80]])

landmarks = np.array([[0,0],[0,0],[2,0],[4,0],[6,0],[8,0],[10,0],[12,0],[14,0],[16,0]]) #first one is dummy


# NL = len(landmarks)

# create particles and weights
# if initial_x is not None:
#     particles = create_gaussian_particles(
#         mean=initial_x, std=(5, 5, np.pi/4), N=N)
# else:
#particles = create_uniform_particles((0,16), (2.5,3.5), N)
# particles = create_uniform_particles((55,65), (60,70), N)
particles = create_uniform_particles((0,15), (2,3), N)
weights = np.ones(N) / N

 


IPC_FIFO_NAME = "MYFIFO"
timeBase = 0
iterWait = 0
runs=0

anchors_ind = [0, 0, 0, 0, 0, 0, 0, 0, 0]
zs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
 
 

try:
    os.mkfifo(IPC_FIFO_NAME)
except OSError:
    print("File Exists")
try:
    while True:
        # Reading from Pipe
        # print("reading from pipe")
        fifor = os.open(IPC_FIFO_NAME, os.O_RDONLY)
        line = os.read(fifor, 500).decode('utf8')
        # print(line)
        line = line.split(';')
        line= line[0]
        time = int(line[6:9])
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
        # print("anchor"+str(anchor))
        anchors_ind[anchor] = 1
        zs[anchor] = dist 

        # if iterWait == 1:
          
            
            
        content=""
        # User update
        if iterWait == 2 :
            # incorporate measurements
            print(zs)
            update(particles, weights, z=zs, R=sensor_std_err, 
            landmarks=landmarks,anchors=anchors_ind)

            mu, var = estimate(particles, weights)
            # print ("prior:" + str(mu))
            vx,vy = veloc(time)
            runs+=1
            print("runs:"+str(runs))
            # print(vx)

            predict(particles, u=(vx, vy), std=(.2, .5))

        # move diagonally forward to (x+1, x+1)
            mu, var = estimate(particles, weights)
            RMSE(mu[0],mu[1],time)
            print("actual "+str(actual(int(time))))
            content=closest(mu[0],mu[1],anchors_ind)
            print(content)


    # resample if too few effective particles
            if neff(weights) < N/2:
                # print("resapmling!!!!!!!!!!!!!")
                indexes = systematic_resample(weights)
                resample_from_index(particles, weights, indexes)

        
        #assert np.allclose(weights, 1/N)
            # mu, var = estimate(particles, weights)
            # print("posterior:" + str(mu)) 
            # print("RSSI: " , line[2:5], " distance: ", dist," anchor ", anchor)
            # print("anchors: ", anchors_ind, "Zs : ", zs)
            


        # Writing to Pipe
        # content = "fe80::212:7404:4:404"
        # content=content+" "+str(time)


        fifow = os.open(IPC_FIFO_NAME, os.O_WRONLY | os.O_TRUNC)
        os.write(fifow, content.encode('utf8'))
        os.close(fifow)

 

except KeyboardInterrupt:
    print("Exit deep here")
