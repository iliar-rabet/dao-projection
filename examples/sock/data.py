data="7.dat"
s=0.0
c=0
with open(data) as fp:
   for line in fp:
       words=line.split(':')
       if(words[0]=="RMSE"):
           c+=1
        #    print(words[1])
           s+=float(words[1])
        #    print(s)

print("average:")
print(s/c)