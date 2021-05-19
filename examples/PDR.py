#!/usr/bin/python3
from datetime import datetime
import sys
import numpy as np

try:
	if sys.argv[1]:
		fileName = sys.argv[1]
except IndexError:
	print("Using default file name.")
	fileName = 'loglistener.txt'

f = open(fileName,"r")
#f.close()


def test():
    ls=[]
    summ=0
    first=0
    txcounter=0.0
    rxcounter=[0]*3000
    # min=1000000
    # max=0
    for i in range(1,3000):
        f.seek(0)
        
        
        for line in f.readlines():
            numb = str(i) 
            if numb in line:
                if "sending hello "+numb +" "in line:
                    # sTime = datetime.strptime(line[0:9], '%M:%S.%f')
                    # sTime=int(line.split('\t')[0])
                    txcounter+=1
                    print (line+"\n")
                if "ID:2" in line and "hello "+numb+" " in line:
                    if(first==0):
                        first=int(numb)
                    # print (line)
                    # rTime = datetime.strptime(line[0:9], '%M:%S.%f')
                    # rTime=int(line.split('\t')[0])
                    # dTime=rTime-sTime
                    # dTime=dTime.seconds*1000000+dTime.microseconds
                    rxcounter[i]=1
                    # if(min>dTime):
                    #     min=dTime
                    # if(max<dTime):
                    #     max=dTime
                    # print(str(dTime))
                    # ls.append(dTime)
                    break
        # if(dTime is not None):
        #     summ=summ+dTime.microseconds
    rx=0
    for el in rxcounter:
        rx+=el
    # print("avg="+str(np.average(ls)))
    # print("var="+str(np.var(ls)))
    # print("max:"+str(max)+ " Min:"+str(min)," StdDev:"+str(numpy.std(list)))
    # print(txcounter)
    # print(rx)
    print(rx)
    print(txcounter)
    print(first)
    print((rx)/(txcounter-first+1))


if __name__ == '__main__' :
		test()
