import matplotlib.pyplot as plt
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

 

N = 2000  # number of points
import numpy as np
filepath="position.dat"
vel = {}
position = {}
Window=776
lastx= 183.5615498105
lasty= 148.147316381
with open(filepath) as fp:
   for line in fp:
    #    print(line.split())
        time=float(line.split()[1])
        x=float(line.split()[2])
        y=float(line.split()[3])    
        position.update({time:(x,y)})
        lastx=x
        lasty=y

def veloc(T):
    T=T % Window
    return (position[T+1][0]-position[T][0],position[T+1][1]-position[T][1])
    # return (vel[str(T)][0]*5,vel[str(T)][1]*5)


def actual(t):
    t=(t+1)%Window
    return position[t]


def RMSE(x,y,t):
    act=actual(float(t))
    print("rmse:")
    print(act)
    Xerr=x-act[0]
    Yerr=y-act[1]
    error=math.sqrt(Xerr**2 + Yerr**2)
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
            # diff=particles - landmark
            # distance=(diff[:,0])**2 + (diff[:,1])**2
            # distance=math.sqrt(distance)  
            distance = np.linalg.norm(particles - landmark,axis=1)
            # print("%%%%%%")
            # print("landmark")
            # print(landmark)
            # print("particles - landmark")
            # print(particles-landmark)
            # print("distance:")
            # print(distance)
            # print(z[i])
            # print(type(z[i]))
            weights *= scipy.stats.norm(distance, R).pdf(float(z[i]))

 

    weights += 1.e-300      # avoid round-off to zero
    weights /= sum(weights) # normalize


def calculate_RSS(dist):
    return -10 - 0.4 * 10 * math.log10(dist)
 

def calculate_dist(RSS):
    dist= 10**((-25.0 - RSS)/(10.0 * 7) )
    dist='{:.10f}'.format(dist)
    return dist

 

def predict(particles, u, std, dt=1.):
    """ move according to control input u (velocity in x, velocity in y)
    with noise Q (std heading change, std velocity)`"""
    print(u)
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
    print("max:")
    print(particles[index])
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
    print("resampling!!!!!")

    # resample according to indexes
    particles[:] = particles[indexes]
    weights.fill(1.0 / N)

 


def calculate_dist(RSS):
   dist= 10**((-38.44 - RSS)/(10.0 * 2.4) )
   dist='{:.10f}'.format(dist)
   return dist

 

sensor_std_err=.1
initial_x=None
# landmarks = np.array([[10, 0], [0, 1], [18, 12], [2, 18], [20, 18], [0, 10], [20,10]])
# landmarks = np.array([[10, 0], [0, 1], [18, 12]])
landmarks= np.array([[250.0,150.0],[187.0,130.0],[180.0,150.0]])
# landmarks= np.array([[70.0,70.0],[50,65],[80,80]])

# NL = len(landmarks)

# create particles and weights
# if initial_x is not None:
#     particles = create_gaussian_particles(
#         mean=initial_x, std=(5, 5, np.pi/4), N=N)
# else:
particles = create_uniform_particles((180,185), (140,150), N)
weights = np.ones(N) / N

 


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
        anchor=anchor-3
        anchors_ind[anchor] = 1
        zs[anchor] = dist 


        # User update
        if iterWait == 3 :
            
            velocity = veloc(time)
            # print(vx)
        # incorporate measurements
            update(particles, weights, z=zs, R=sensor_std_err, 
            landmarks=landmarks,anchors=anchors_ind)

            mu, var = estimate(particles, weights)
            print ("prior:" + str(mu))
        # move diagonally forward to (x+1, x+1)
            predict(particles, u=velocity, std=(.2, .05))
            mu, var = estimate(particles, weights)
            RMSE(mu[0],mu[1],time)
            print("actual "+str(actual(int(time))))


    # resample if too few effective particles
            if neff(weights) < N/2:
                print("resapmling!!!!!!!!!!!!!")
                indexes = systematic_resample(weights)
                resample_from_index(particles, weights, indexes)

                
        #assert np.allclose(weights, 1/N)
            mu, var = estimate(particles, weights)
            print("posterior:" + str(mu)) 
            print("RSSI: " , line[2:5], " distance: ", dist," anchor ", anchor)
            print("anchors: ", anchors_ind, "Zs : ", zs)
            
 

        # Writing to Pipe
        content = "fd00::212:7404:4:404"

 

        fifow = os.open(IPC_FIFO_NAME, os.O_WRONLY | os.O_TRUNC)
        os.write(fifow, content.encode('utf8'))
        os.close(fifow)

 

except KeyboardInterrupt:
    print("Exit deep here")
