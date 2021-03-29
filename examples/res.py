#!/usr/bin/python3
from datetime import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt 

try:
	if sys.argv[1]:
		fileName = sys.argv[1]
except IndexError:
	print("Using default file name.")
	fileName = 'loglistener.txt'

f = open(fileName,"r")
f2 = open(fileName,"r")
#f.close()

def get_ip(id):
    if id=="2":
        return "fd00::212:7402:2:202"
    if id=="14":
        return "fd00::212:740e:e:e0e"
    if id=="6":
        return "fd00::212:7406:6:606"
    if id=="15":
        return "fd00::212:740f:f:f0f"
    if id=="10":
        return "fd00::212:740a:a:a0a"
    if id=="16":
        return "fd00::212:7410:10:1010"
    if id=="17":
        return "fd00::212:7411:11:1111"
    if id=="21":
        return "fd00::212:7415:15:1515"
    if id=="22":
        return "fd00::212:7416:16:1616"
    if id=="26":
        return "fd00::212:741a:1a:1a1a"
    


def test():
    ls=[]
    s=[]
    r=[]
    flows=0
    summ=0
    txcounter=0.0
    rxcounter=[0]*100
    min=1000000
    max=0

    f.seek(0)
    
    dTime=0
    for line in f.readlines():
        if "Starting Flow" in line:
            flows=flows+1
            ls.append([])
            s.append(0)
            r.append(0)
            # print("************************************************")
        if "Sending" in line:
            s[flows-1]=s[flows-1]+1
            src_id=line.split('\t')[1].split(':')[1]
            src_ip=str(get_ip(src_id))
            dst_ip=line.split('\t')[2].split(' ')[12].split('\n')[0]
            seq=line.split('\t')[2].split(' ')[10]
            # print("seq:"+seq)
            # print("src_id:"+src_id)
            # print("src_ip:"+src_ip)
            # print("dst_ip:"+dst_ip)
            
            f2.seek(0)
            
            if(line.split('\t')[0].count(':')==1):
                sTime=datetime.strptime(line.split('\t')[0], '%M:%S.%f')
            else:
                sTime=datetime.strptime(line.split('\t')[0], '%H:%M:%S.%f')
            # print(line)
            for line2 in f2.readlines():
                # if "Received 'hello "+str(seq+"'") in line2:
                #     print("1")
                #     if dst_ip in line2:
                #         print("2")
                #         if src_ip in line2:
                #             print("BING")
                if "Received 'hello "+str(seq+"'") in line2 and dst_ip in line2 and src_ip in line2:
                    if(line.split('\t')[0].count(':')==1):
                        rTime=datetime.strptime(line2.split('\t')[0], '%M:%S.%f')
                    else:
                        rTime=datetime.strptime(line2.split('\t')[0], '%H:%M:%S.%f')
                    r[flows-1]=r[flows-1]+1
                    # print(line2)
                    dTime=rTime-sTime
                    dTime=dTime.seconds*1000000+dTime.microseconds
                    ls[flows-1].append(dTime) 
    
    x=[]
    y=[]
    ind=0
    for i in ls:
        ind+=1
        x.extend(np.ones(len(i))*ind)
        y.extend(i)
    #     if(len(i)!=0):
    #         print(sum(i)/len(i))
    #     else:
    #         print("0")
    # for i in ls:
    #     if(len(i)!=0):
    #         print(len(i))
    #     else:
    #         print("0")
    print(s)
    print(r)

    
    np.savez(fileName+".npz",x=x,y=y)
    
    # ax = sns.lineplot(x,y)
    # plt.show(ax)

if __name__ == '__main__' :
		test()