#!/usr/bin/python3
from datetime import datetime
import sys
import numpy

PKTS=100

try:
	if sys.argv[1]:
		fileName = sys.argv[1]
except IndexError:
	print("Using default file name.")
	fileName = 'loglistener.txt'

f = open(fileName,"r")
#f.close()


def test():
    list=[]
    summ=0
    first=0
    txcounter=0.0
    rxcounter=[0]*PKTS
    min=1000000
    max=0
    for i in range(1,PKTS):
        f.seek(0)
        
        dTime=0
        for line in f.readlines():
            hello = "hello " + str(i) 
            if hello in line:
                if "sending "+hello in line:
                    sTime = datetime.strptime(line[0:9], '%M:%S.%f')
                    txcounter+=1
                    print (line+"\n")
                if "ID:11" in line and hello in line:
                    if(first==0):
                        first=i

                    print (line)
                    rTime = datetime.strptime(line[0:9], '%M:%S.%f')
                    dTime=rTime-sTime
                    dTime=dTime.seconds*1000000+dTime.microseconds
                    rxcounter[i]=1
                    if(min>dTime):
                        min=dTime
                    if(max<dTime):
                        max=dTime
                    list.append(dTime)
                    print("delay:"+str(dTime)+"\n")
                    break
        summ=summ+int(dTime)
    rx=0
    for el in rxcounter:
        rx+=el
    print("avg="+str(summ/rx)+"\n")
    print("max:"+str(max)+ " Min:"+str(min)," StdDev:"+str(numpy.std(list)))
    print(first)
    print("PDR="+str((rx-first)/(txcounter-first))+"\n")


if __name__ == '__main__' :
		test()
