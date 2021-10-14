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


total_count=0
ctr_count=0
RPL_count=0
data_count=0


for line in f:
    if 'forwarding control' in line:
        total_count+=1
        ctr_count+=1

    if 'DIO' in line or "DIS" in line or "DAO" in line:
        total_count+=1
        RPL_count+=1
    
    if 'now sending hello' in line:
        total_count+=1
        data_count+=1
        
                
print("data")
print(data_count)
print("ctr:")
print(ctr_count)
print("RPL:")
print(RPL_count)
print("SUM:")
print(total_count)
