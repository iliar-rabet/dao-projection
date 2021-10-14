#!/usr/bin/python3
from datetime import datetime
import sys
import numpy

PKTS=300
slip=2
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
        print(i)
        dTime=0
        for line in f.readlines():
            hello = "hello " + str(i)
            
            if hello in line:
                if "sending "+hello +" from 100:fe80::212:7401:1" in line:
                    sTime = datetime.strptime(line[0:9], '%M:%S.%f')
                    txcounter+=1
                    print("add tx 1")
                    print (line)
                if "ID:"+str(slip) in line and hello + " from 100:fe80::212:7401:1" in line:
                    if(first==0):
                        first=i
                    print("add rx 1")
                    print (line)
                    rTime = datetime.strptime(line[0:9], '%M:%S.%f')
                    dTime=rTime-sTime
                    dTime=dTime.seconds*1000000+dTime.microseconds
                    
                    rxcounter[i]+=1
                    if(min>dTime):
                        min=dTime
                    if(max<dTime):
                        max=dTime
                    list.append(dTime)
                    print("delay:"+str(dTime)+"\n")
                    break
                            
                # if "sending "+hello+" from 100:fe80::212:7402:2" in line:
                #     sTime = datetime.strptime(line[0:9], '%M:%S.%f')
                #     txcounter+=1
                #     print("add tx 2")
                #     print (line)
                # if "ID:"+str(slip) in line and hello + " from 100:fe80::212:7402:2" in line:
                #     if(first==0):
                #         first=i
                #     print("add rx 2")
                #     print (line)
                #     rTime = datetime.strptime(line[0:9], '%M:%S.%f')
                #     dTime=rTime-sTime
                #     dTime=dTime.seconds*1000000+dTime.microseconds
                #     rxcounter[i]+=1
                #     if(min>dTime):
                #         min=dTime
                #     if(max<dTime):
                #         max=dTime
                #     list.append(dTime)
                #     print("delay:"+str(dTime)+"\n")
                    
                # if "sending "+hello +" from 100:fe80::212:7403:3" in line:
                #     sTime = datetime.strptime(line[0:9], '%M:%S.%f')
                #     txcounter+=1
                #     print("add tx 3")
                #     print (line)
                # if "ID:"+str(slip) in line and hello + " from 100:fe80::212:7403:3" in line:
                #     if(first==0):
                #         first=i
                #     print("add rx 3")
                #     print (line)
                #     rTime = datetime.strptime(line[0:9], '%M:%S.%f')
                #     dTime=rTime-sTime
                #     dTime=dTime.seconds*1000000+dTime.microseconds
                #     rxcounter[i]+=1
                #     if(min>dTime):
                #         min=dTime
                #     if(max<dTime):
                #         max=dTime
                #     list.append(dTime)
                #     print("delay:"+str(dTime)+"\n")
                #     break

        summ=summ+int(dTime)
    rx=0
    for el in rxcounter:
        rx+=el
    print("avg="+str(summ/rx)+"\n")
    print("max:"+str(max)+ " Min:"+str(min)," StdDev:"+str(numpy.std(list)))
    print(rx)
    print(txcounter)
    print("PDR="+str((rx)/(txcounter))+"\n")


if __name__ == '__main__' :
		test()
