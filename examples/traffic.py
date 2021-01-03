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

    for line in f.readlines():
        if "received" in line and "bytes" in line:
            b = line.split("received")[1].split("bytes")[0]
            b = int(b)
            print(b)
            summ=summ+int(b)
    print("sum="+str(summ))    
    # print("max:"+str(max)+ " Min:"+str(min)," StdDev:"+str(numpy.std(list)))
    # print("PDR="+str(rx/txcounter)+"\n")


if __name__ == '__main__' :
		test()