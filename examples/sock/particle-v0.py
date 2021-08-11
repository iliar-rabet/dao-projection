import sysv_ipc
import urllib.request
#import matplotlib.pyplot as plt
import numpy as np
import time as timeP
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


# Create shared memory object
memory = sysv_ipc.SharedMemory(123456)
down_memory = sysv_ipc.SharedMemory(123457)

data={}
window={}
filepath="../multipath/random-45.dat"
vel = {}
position = {}
Window=107
lastx= 0
lasty= 0
time=0.0
with open(filepath) as fp:
   for line in fp:
        ip=str(int(line.split()[0])+1)
        time=float(line.split()[1])
        x=float(line.split()[2])
        y=float(line.split()[3])    
        position[(ip,time)]=(x,y)
        if time == 0:
            window[ip]=0
        if(window[ip] < float(time)):
            window[ip]=int(time)
        lastx=x
        lasty=y


print(position)
print(window)

rssfile="5m.dat"
c=0
rss={}
with open(rssfile) as fp:
   for line in fp:
           rss.update({line.split()[0]:line.split()[1]})

N = 20000  # number of points


def actual(t,ip):
    t=(t+1)%window[ip]
    return position[(ip,t)]


def RMSE(x,y,t,ip):
    act=actual(float(t),ip)
    Xerr=x-act[0]
    Yerr=y-act[1]
    error=math.sqrt(Xerr**2 + Yerr**2)
    print(ip)
    data[ip].new_error(error)

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


def update(particles, weights, z, R,anchors):
    for i, anchor in enumerate(anchors):
        distance = np.linalg.norm(particles - anchor,axis=1)
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

def closest(x,y,mn):
    #print(x,y)
    dists=landmarks-[x,y]
    #print(dists)
    dd=dists[:,0]**2 + dists[:,1]**2
    #print(dd)
    #for ind in range(len(dd)): 
    #    if anchors_ind[ind]!=1:
    #        dd[ind]=1000.0
    return "SET fd00:0:0:0:212:7408:8:808 for fe80::212:740b:b:b0b\nSET fd00:0:0:0:212:7405:5:505 for fe80::212:740c:c:c0c\0"

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


def veloc(ip,T):
    T=T%window[ip]
    print(T)
    print(window[ip])
    return (position[(ip,T+1)][0]-position[(ip,T)][0],position[(ip,T+1)][1]-position[(ip,T)][1])


sensor_std_err=.1
initial_x=None


particles={}
weights={}
objects={}
 
class MN:
    def __init__(self):
        print("init")
        self.measurements = 0
        self.distances=[]
        self.anchors=[]
        self.count=0
        self.sum_err=0

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
        print("AVG:::::::::::::::::::::::::::: "+str(self.sum_err/self.count))
        print("RMSE:"+str(rmse))


IPC_FIFO_NAME = "MYFIFO"
IPC_FIFO_DOWN_NAME = "DOWNFIFO"
timeBase = 0
iterWait = 0
runs=0
mnList=[]


def ip_to_id(ip):
    if(ip=='c'):
        return '12'
    if(ip=='b'):
        return '11'
    else:
        return ip
 

try:
    os.mkfifo(IPC_FIFO_NAME)
except OSError:
    print("File Exists")
try:
    oldLine = "never"
    oldWordList = []
    while True:
        timeP.sleep(0.001)
        line= str(memory.read())
        memory.write("x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00")
        line= line[2:]
        if line != oldLine:
            wordList = []
            for i in range(0, len(line), 10):
                word = line[i:i+9]
                if 'x00' not in word and word not in oldWordList:
                    wordList.append(word)
                else:
                    pass
            #print(wordList)
            oldWordList = wordList
            oldLine = line
        else:
            continue

        line=line.split('\'')[1]
        line = line.split(';')[0]
        
        if len(wordList)==0:
            continue
        if wordList[0]=="'":
            continue

        for word in wordList:
            print("Received encoded data: " + word)
            time = int(word[6:9])
            
            ip=ip_to_id(word[5])
            print("------------\nip:")
            print(ip)
            if ip not in mnList:
                mnList.append(ip)
                particles[ip] = create_uniform_particles((0,15), (2,3), N)
                weights[ip] = np.ones(N) / N
                data[ip]=MN()

            if timeBase != time :
                timeBase = time
                data[ip].reset_meas()
            
            dist = calculate_dist(int(word[2:5])) 
            print("dist:")
            print(dist)
            anchor = int(word[0:2], 16)
            anchor=anchor-1
            # print("anchor"+str(anchor))
            print("anchor:")
            print(landmarks[int(anchor)])
            data[ip].new_meas(dist,landmarks[int(anchor)])

    
        # incorporate measurements
        print(data[ip].anchors)
        print(data[ip].distances)
        update(particles[ip], weights[ip], data[ip].distances, R=sensor_std_err, 
        anchors=data[ip].anchors)
        
        mu, var = estimate(particles[ip], weights[ip])
        # print ("prior:" + str(mu))
        vx,vy = veloc(ip,time)
        runs+=1
        # print("runs:"+str(runs))
        # print(vx)

        predict(particles[ip], u=(vx, vy), std=(.2, .5))

        # move diagonally forward to (x+1, x+1)
        mu, var = estimate(particles[ip], weights[ip])
        RMSE(mu[0],mu[1],time,ip)
        print("actual "+str(actual(int(time),ip)))
        print("estimated "+str(mu))
        content=closest(mu[0],mu[1],data[ip])
        print(content)
        down_memory.write(content)

        # resample if too few effective particles
        if neff(weights[ip]) < N/2:
            # print("resapmling!!!!!!!!!!!!!")
            indexes = systematic_resample(weights[ip])
            resample_from_index(particles[ip], weights[ip], indexes)
        
        #urllib.request.urlopen('http://[fd00::212:740b:b:b0b]') 
    
    #assert np.allclose(weights, 1/N)
        # mu, var = estimate(particles, weights)
        # print("posterior:" + str(mu)) 
        # print("RSSI: " , line[2:5], " distance: ", dist," anchor ", anchor)

            
        #else:
        #    content = "WAIT"

        # Writing to Pipe
        # content = "fe80::212:7404:4:404"
        #content=content+" "+str(time)


        #fifow = os.open(IPC_FIFO_DOWN_NAME, os.O_WRONLY | os.O_TRUNC)
        #os.write(fifow, content.encode('utf8'))
        #os.close(fifow)
        

except KeyboardInterrupt:
    print("Exit deep here")
