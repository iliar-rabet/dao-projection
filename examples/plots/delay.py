#!/usr/bin/python3
from datetime import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.ticker as tick
import scipy.stats


def confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return h

def mean(data):
    if(len(data)==0):
        print("0000")
        return 0
    return sum(data)/len(data)

def y_fmt(tick_val, pos):
    if tick_val > 1000:
        val = int(tick_val) / 1000
        return '{:d}'.format(val)
    else:
        return tick_val

RPL = np.load('RPL.npz')
RP = np.load('RP.npz')

RPx=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
RPLx=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

for ind in range(len(RP['x'])):
    x=RP['x'][ind]
    y=RP['y'][ind]
    # print(int(x))
    # print(RPx[int(x)])
    # print(y)
    RPx[int(x)].append(y)


for ind in range(len(RPL['x'])):
    x=RPL['x'][ind]
    y=RPL['y'][ind]
    RPLx[int(x)].append(y)

RPy=[mean(RPx[x]) for x in range(1,10)]
RPLy=[mean(RPLx[x]) for x in range(1,10)]

# print(RPy)
# print(RPx)
colors = iter([plt.cm.tab20(i) for i in range(20)])
next(colors)
next(colors)
next(colors)

barWidth=0.25
r2 = [x + barWidth for x in range(1,10)]
RPerr=[confidence_interval(RPx[x]) for x in range(1,10)]
RPLerr=[confidence_interval(RPLx[x]) for x in range(1,10)]

plt.bar(r2,RPLy,width=0.25,label="RPL",yerr=RPLerr,color=[next(colors)],edgecolor='black')

next(colors)
plt.bar(range(1,10),RPy,width=0.25,label="RPL-RP",yerr=RPerr,color=[next(colors)],edgecolor='black',hatch = '/')

plt.ylabel('E2E delay (millisecond)', fontweight ='bold') 
plt.xlabel('Active Flows (#)', fontweight ='bold') 
plt.gca().yaxis.set_major_formatter(tick.FuncFormatter(y_fmt))
plt.legend()
plt.show()
