#!/usr/bin/python3
from datetime import datetime
import sys
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt 
from math import log
from operator import add

try:
	if sys.argv[1]:
		fileName = sys.argv[1]
except IndexError:
	print("Using default file name.")
	fileName = 'loglistener.txt'

f = open(fileName,"r")
end=11

def test():
    
    dao=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    dio=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    dis=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    pdao=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    pdao_ack=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    pdr=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    f.seek(0)
    
    dTime=0
    for line in f.readlines():
        if(len(line.split('\t'))<3):
            continue
        if(len(line.split('\t')[2].split(':'))<2):
            continue
        if("DAO" not in line.split('\t')[2] and "PDAO" not in line.split('\t')[2] and "DIS" not in line.split('\t')[2] and "DIO" not in line.split('\t')[2]):
            continue
        if(line.split('\t')[0].count(':')==1):
            Time=datetime.strptime(line.split('\t')[0], '%M:%S.%f')
        else:
            Time=datetime.strptime(line.split('\t')[0], '%H:%M:%S.%f')
        typ=line.split('\t')[2].split(":")[0]
        siz=int(line.split('\t')[2].split(":")[1])
        # print(typ)
        # print(siz)
        print(Time)
        # print(dao[Time.minute])
        if(typ=="DAO"):
            dao[Time.minute]+=siz
        if(typ=="DIO"):
            dio[Time.minute]+=siz
        if(typ=="PDAO"):
            pdao[Time.minute]+=siz
        if(typ=="DIS"):
            dis[Time.minute]+=siz
        if(typ=="PDAO_ACK"):
            pdao_ack[Time.minute]+=siz
        if(typ=="PDR"):
            pdr[Time.minute]+=siz

    f2=open("OH-RPL-RP2","r")
    for line in f2.readlines():
        w0=line.split('\t')[0]
        if "PDAO_ACK" not in w0 and "PDR" not in w0 and "DAO" not in w0:
            continue
        if len(line.split(" "))==1:
            continue
        print("line:"+line)
        sec=int(line.split(" ")[1])
        print(sec)
        minu=(sec-338740)/60
        print(minu)
        siz=int(line.split(" ")[0].split(":")[1])
        print(siz)
        typ=line.split(" ")[0].split(":")[0]
        if(typ=="DAO"):
            dao[minu]+=siz
        if(typ=="PDAO_ACK"):
            pdao_ack[minu]+=siz
        if(typ=="PDR"):
            pdr[minu]+=siz


    dao=[log(y+1,2) for y in dao]
    dio=[log(y+1,2) for y in dio]
    dis=[log(y+1,2) for y in dis]
    pdao=[log(y+1,2) for y in pdao]
    pdr=[log(y+1,2) for y in pdr]
    pdao_ack=[log(y+1,2) for y in pdao_ack]

    print(dio)
    print(dao)
    print(dis)
    print(pdao_ack)
    print(pdr)
    print(pdao)
    plt.ylabel('Bytes (log2 scale)', fontweight ='bold') 
    plt.xlabel('Time (minute)', fontweight ='bold') 
    
    colors = iter([plt.cm.tab20(i) for i in range(20)])
    
    plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.5)

    dao=dao[:end]
    dio=dio[:end]
    pdr=pdr[:end]
    pdao=pdao[:end]
    dis=dis[:end]


    width=0.45
    next(colors)
    plt.bar(range(0,end), dao,label='DAO', hatch = 'x', width=width, color=[next(colors)],edgecolor='black')
    bot=dao
    next(colors)
    plt.bar(range(0,end), dio,label='DIO',bottom=bot, width=width,hatch = '//', color=[next(colors)],edgecolor='black')
    bot=list( map(add, bot, dio) )
    next(colors)
    plt.bar(range(0,end), pdr,label='PDR',bottom=bot,width=width, hatch = '/', color=[next(colors)],edgecolor='black')
    bot=list( map(add, bot, pdr) )
    next(colors)
    plt.bar(range(0,end), pdao,label='PDAO',bottom=bot, width=width,hatch = '-', color=[next(colors)],edgecolor='black')
    bot=list( map(add, bot, pdao) )
    next(colors)
    plt.bar(range(0,end), dis,label='DIS',bottom=bot, width=width,hatch = '+', color=[next(colors)],edgecolor='black')
    bot=list( map(add, bot, dis) )
    # plt.bar(range(0,end), pdao_ack,label='PDAO-ACK',bottom=bot)
    # bot=bot+pdao_ack

    a=sum(pdao)+sum(pdr)+sum(pdao_ack)
    b=sum(dis)+sum(dio)+sum(dao)
    print(a)
    print(b)
    plt.legend()
    plt.show()

if __name__ == '__main__' :
		test()