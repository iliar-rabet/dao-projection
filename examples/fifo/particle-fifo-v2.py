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

filepath="../multipath/random-45.dat"
vel = {}
position = {}
mobile_nodes=1
data={}
window={}
lastx= 0
lasty= 0
landmarks = np.array([[0,0]])
x_min=0
x_max=20
y_min=0
y_max=20
particles={}
weights={}
objects={}


with open(filepath) as fp:
   for line in fp:
        ip=str(int(line.split()[0])+1)
        time=float(line.split()[1])
        x=float(line.split()[2])
        y=float(line.split()[3])    
        if(int(line.split()[0])+1>mobile_nodes):
            print("adding landmark\n")
            temp=np.array([[x,y]])
            print(temp)
            # landmarks=np.concatenate((landmarks,temp))
            landmarks=np.concatenate((landmarks,temp))
            print(landmarks)
        position[(ip,time)]=(x,y)
        if time == 0:
            window[ip]=0
        if(window[ip] < float(time)):
            window[ip]=int(time)
        lastx=x
        lasty=y
 
rssfile="5m.dat"
c=0
rss={}
with open(rssfile) as fp:
   for line in fp:
        #    print(line.split())
           rss.update({line.split()[0]:line.split()[1]})

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
    return rss.get(str(RSSI))*5
 

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
    #print(x,y)
    dists=landmarks-[x,y]
    #print(dists)
    dd=dists[:,0]**2 + dists[:,1]**2
    #print(dd)
    #for ind in range(len(dd)): 
    #    if anchors_ind[ind]!=1:
    #        dd[ind]=1000.0
    #return "SET fd00:0:0:0:212:7408:8:808 for fd00:0:0:0:212:7401:1:101 \n UNSET fd00:0:0:0:212:740a:a:a0a for fd00:0:0:0:212:740c:c:c0c\n"

    arg=np.argmin(dd)
    arg=arg+2
    if(arg>16):
        arg=hex(arg)[2:]
        arg=str(arg)
        ip_str="fd00:0:0:0:212:74"+arg+":"+arg+":"+arg+arg
    else:
        arg=hex(arg)[2:]
        arg=str(arg)
        ip_str="fd00:0:0:0:212:740"+arg+":"+arg+":"+arg+"0"+arg
    return ip_str

    

def veloc(ip,T):
    T=T%window[ip]
    print(T)
    print(window[ip])
    return (position[(ip,T+1)][0]-position[(ip,T)][0],position[(ip,T+1)][1]-position[(ip,T)][1])


sensor_std_err=.1
initial_x=None


# NL = len(landmarks)

# create particles and weights
# if initial_x is not None:
#     particles = create_gaussian_particles(
#         mean=initial_x, std=(5, 5, np.pi/4), N=N)
# else:
#particles = create_uniform_particles((0,16), (2.5,3.5), N)
# particles[ip] = create_uniform_particles((x_min,x_max), (y_min,y_max), N)
# weights = np.ones(N) / N


class MN:
    def __init__(self):
        print("init")
        self.measurements = 0
        self.distances=[]
        self.anchors=[]
        self.count=0
        self.sum_err=0
        self.new_parent=""
        self.old_parent="fd00:0:0:0:212:7405:5:505"

    def new_meas(self,dist,anch):
        self.measurements = self.measurements +1
        self.anchors.append(anch)
        self.distances.append(dist)
    
    def reset_meas(self):
        self.measurements = 0
        self.anchors=[]
        self.distances=[]

    def new_error(self,rmse):
        self.sum_err=rmse + self.sum_err
        self.count=self.count+1
        print("AVG RMSE for "+str(self.sum_err/self.count))
        print("instatn RMSE:"+str(rmse))
    


timeBase = 0
iterWait = 0
runs=0
mnList=[]



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
        os.close(fifor)

        print(line)

        line=line.rstrip('\x00').rstrip('\0').rstrip('-').rstrip('|')

        # print("\n******************************\nAt "+ str(time) + "\nReceived encoded data: " + line)

        lw=line.split(' ')
        print(lw)
        time = int(lw[5])
        
        hex_id='0x'+lw[3][-1:]
        ip=str(int(hex_id,16))
        print("------------\nmn:")
        print(ip)
        if ip not in mnList:
            mnList.append(ip)
            particles[ip] = create_uniform_particles((x_min,x_max), (y_min,y_max), N)
            weights[ip] = np.ones(N) / N
            data[ip]=MN()

        if timeBase != time :
            timeBase = time
            response=""
            for mn in mnList:
                data[mn].reset_meas()
        
        dist = calculate_dist(int(lw[1])) 
        # print("dist:")
        # print(dist)
        print(lw[7])
        print(lw[7].split(':')[-2])
        anchor = int(lw[7].split(':')[-2], 16)
        anchor=anchor-2
        print("anchor"+str(anchor))
        print("anchor:")
        print(landmarks[int(anchor)])
        data[ip].new_meas(dist,landmarks[int(anchor)])
        print("measurements:")
        print(data[ip].measurements)

        response=""
        # User update
        if data[ip].measurements >= 3 :
            # incorporate measurements
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
            
        else:
            content = "WAIT"

        # Writing to Pipe
        # content = "fe80::212:7404:4:404"
        content=content+" "+str(time)


        fifow = os.open(IPC_FIFO_NAME, os.O_WRONLY | os.O_TRUNC)
        os.write(fifow, content.encode('utf8'))
        os.close(fifow)

 

except KeyboardInterrupt:
    print("Exit deep here")
