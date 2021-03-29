#!/usr/bin/python3
from datetime import datetime
import sys

try:
	if sys.argv[1]:
		fileName = sys.argv[1]
except IndexError:
	print("Using default file name.")
	fileName = 'loglistener.txt'

f = open(fileName,"r")
#f.close()


def test():
    summ=0
    txcounter=0.0
    rxcounter=0.0
    for i in range(1,200):
        f.seek(0)
        
        dTime=0
        for line in f.readlines():
            text="control broadcast: " + "%03d"%i
            best="BEST time: " + str(i) +"\n"
            # print(text)
            # print(best)
            if text in line:
                sTime = datetime.strptime(line[0:9], '%M:%S.%f')
                txcounter+=1
                # print (line)
            if best in line:
                # print (line)
                rTime = datetime.strptime(line[0:9], '%M:%S.%f')
                dTime=rTime-sTime
                dTime=dTime.seconds*1000000+dTime.microseconds
                # dTime=dTime.microseconds
                rxcounter+=1
                print("delay:")
                print(dTime)
                break
        summ=summ+int(dTime)
    print("avg="+str(summ/rxcounter)+"\n")
    print("PDR="+str(rxcounter/txcounter)+"\n")


if __name__ == '__main__' :
		test()
