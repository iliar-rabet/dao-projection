#!/usr/bin/python3
from datetime import datetime
import sys

filename="shm-lolo-100-delay"
try:
	if sys.argv[1]:
		fileName = sys.argv[1]
except IndexError:
	print("Using default file name.")
	fileName = 'loglistener.txt'

f = open(fileName,"r")


summ=0
count=0

for line in f:
    if 'NOW BEING BEST' in line:
        summ+=0
        count+=1
    if 'HANDOFF' in line:                
        print(line)
        sTime = datetime.strptime(line[0:9], '%M:%S.%f')
        for line in f: # now you are at the lines you want
            if "NOW BEING BEST" in line:
                rTime = datetime.strptime(line[0:9], '%M:%S.%f')
                dTime=rTime-sTime
                dTime=dTime.seconds*1000000+dTime.microseconds
                print(line)
                print("delay:"+str(dTime/1000)+"\n")
                summ+=int(str(dTime))
                count+=1
                break
                
print("SUM")
print(summ)
print("count:")
print(count)
print(summ/count)