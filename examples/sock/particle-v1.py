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
# filepath="../position/rwp-20"
filepath="../../../pymobility/random-25.dat"
# filepath="low.dat"
mobile_nodes=1
vel = {}
position = {}
lastx= 0
lasty= 0
time=0.0
landmarks = np.array([[0,0]])

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
            print(line)
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


# print("position:")
# print(position)
print("window:")
print(window)
print(landmarks)
rssfile="5m.dat"
c=0
rss={}
with open(rssfile) as fp:
   for line in fp:
           rss.update({line.split()[0]:line.split()[1]})

N = 20000  # number of points


def actual(t,ip):
    # print("ip:"+ip)
    t=(t+1)%window[ip]
    return position[(ip,t)]


def RMSE(x,y,t,ip):
    act=actual(float(t),ip)
    Xerr=x-act[0]
    Yerr=y-act[1]
    error=math.sqrt(Xerr**2 + Yerr**2)
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
    #return "SET fd00:0:0:0:212:7408:8:808 for fd00:0:0:0:212:7401:1:101 \n UNSET fd00:0:0:0:212:740a:a:a0a for fd00:0:0:0:212:740c:c:c0c\n"

    arg=np.argmin(dd)
    arg=arg+1
    if(arg>=16):
        arg=hex(arg)[2:]
        arg=str(arg)
        # ip_str="fe80::c30c:0:0:"+arg
        ip_str="fd00::212:74"+arg+":"+arg+":"+arg+arg
    else:
        arg=hex(arg)[2:]
        arg=str(arg)
        # ip_str="fe80::c30c:0:0:"+arg
        ip_str="fd00::212:740"+arg+":"+arg+":"+arg+"0"+arg
    return ip_str


def veloc(ip,T):
    T=T%window[ip]
    print(T)
    print(window[ip])
    return (position[(ip,T+1)][0]-position[(ip,T)][0],position[(ip,T+1)][1]-position[(ip,T)][1])


sensor_std_err=.05
initial_x=None

x_min=0
x_max=20
y_min=0
y_max=20
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


def ip_to_id(ip):
    if(ip=='c'):
        return '12'
    if(ip=='b'):
        return '11'
    else:
        return ip

def id_to_ip(id):
    if id=='1':
        # return "fd00::c30c:0:0:1"
        return "fe80::212:7401:1:101"


try:
    oldLine = "never"
    oldWordList = []
    while True:
        timeP.sleep(0.001)
        line= memory.read().decode('UTF-8')
        memory.write("\\")
        # if line != oldLine:
        #     print("the whole line:::"+line)
        #     wordList = []
        #     for i in range(0, len(line), 10):
        #         word = line[i:i+9]
        #         if 'x00' not in word and word not in oldWordList:
        #             wordList.append(word)
        #         else:
        #             pass
        #     #print(wordList)
        #     oldWordList = wordList
        #     oldLine = line
        # else:
        #     continue



        line=line.rstrip('\x00').rstrip('\0').rstrip('-')
        wordList=line.split('|')
        if len(wordList)==0:
            continue
        if wordList[0].startswith('\\'):
            continue

        for word in wordList:
            if(word==''):
                continue
            # print("Received encoded data: " + word)

            lw=word.split(' ')
            # print(lw)
            time = int(lw[5])
            
            hex_id='0x'+lw[3][-1:]
            ip=str(int(hex_id,16))
            
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
            # print(lw[7])
            # print(lw[7].split(':'))
            # anchor = int(lw[7].split(':')[5], 16)
            anchor = int(lw[7].split(':')[4], 16)
            anchor=anchor-1
            # print("anchor index"+str(anchor))
            # print("anchor:")
            # print(landmarks[int(anchor)])
            data[ip].new_meas(dist,landmarks[int(anchor)])

        response=""
        # incorporate measurements
        for mn in mnList:
            # print("for:"+mn)
            print(data[mn].anchors)
            print(data[mn].distances)
            update(particles[mn], weights[mn], data[mn].distances, R=sensor_std_err, 
            anchors=data[mn].anchors)
        
            mu, var = estimate(particles[mn], weights[mn])
            # print ("prior:" + str(mu))
            vx,vy = veloc(mn,time)
            # print("VELOC:")
            # print(vx)
            # print(vy)
            runs+=1
            # print("runs:"+str(runs))
            # print(vx)

            predict(particles[mn], u=(vx, vy), std=(.2, .5))

            mu, var = estimate(particles[mn], weights[mn])
            RMSE(mu[0],mu[1],time,mn)
            # print("actual "+str(actual(int(time),mn)))
            # print("estimated "+str(mu))
            data[mn].old_parent=data[mn].new_parent
            data[mn].new_parent=closest(mu[0],mu[1],data[mn])

            # print("new parent:"+data[mn].new_parent)  
            # print("old parent:"+data[mn].old_parent)  

            if(data[mn].new_parent != data[mn].old_parent):
                response = response + "NOT " + data[mn].old_parent + " for "+ id_to_ip(mn)+"\n"
                response = response + "SET " + data[mn].new_parent + " for "+ id_to_ip(mn) +"\0"
            response=""
            print("resp"+response)

            #content=closest(mu[0],mu[1],data[mn])
            #content= "SET fd00:0:0:0:212:7408:8:808 for fd00::212:740b:b:b0b\nSET fd00:0:0:0:212:7405:5:505 for fd00::212:740c:c:c0c\0"
            down_memory.write(response)

            # resample if too few effective particles
            if neff(weights[mn]) < N/2:
                # print("resapmling!!!!!!!!!!!!!")
                indexes = systematic_resample(weights[mn])
                resample_from_index(particles[mn], weights[mn], indexes)
       

except KeyboardInterrupt:
    print("Exit deep here")
