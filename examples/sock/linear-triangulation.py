
# imporing required modules 
import socket      
import datetime 
import time
import localization as lx
import math

P=lx.Project(mode='2D',solver='LSE')


def actual(t):
    t=t%20
    if(t<=10):
        return t
    else:
        return 20-t

def RMSE(x,y,t):
    Xerr=x-actual(t)
    Yerr=y-11
    error=math.sqrt(Xerr**2 + Yerr**2)
    print("RMSE:"+str(error) + "time: "+ str(t))


# P.add_anchor("0", (0, 10))
# P.add_anchor("1", (10, 10))
P.add_anchor("3",  (10, 0))
P.add_anchor("4", (0, 0))
P.add_anchor("5",  (9 ,12))

t,label=P.add_target()

# initializing socket 
s = socket.socket(socket.AF_INET,
    socket.SOCK_STREAM)      
host = "127.0.0.1"
port = 1234
  
# binding port and host 
s.bind((host, port))    
  
# waiting for a client to connect 
s.listen(5)   


   
def calculate_dist(RSS):
   dist= 10**((-40.0 - RSS)/(10.0 * 2.4) )
   dist='{:.10f}'.format(dist)
   return dist

   # accept connection 
c, addr = s.accept()         
print ('got connecton from addr', addr) 
while True: 
   date = datetime.datetime.now()   
   d = str(date) 
   time.sleep(1)
   data=c.recv(1024).decode("ascii")
   # print("data: "+data + "\n")
   lines=data.split(';')
   for line in lines:
      words=line.split(',')
      # print(words[0])
      # print(words[1])
      if(len(words)>1):
          if(len(words[0].split(':'))>3):
            dist=calculate_dist(int(words[1].split(':')[1]))
            anchor=words[0].split(':')[4]
            
            # print("RSSI:" +words[1].split(':')[1] + " distance: " + dist + " anchor " + anchor + "time: " +words[3].split(':')[1])            
            # print(words[2])
            # sending data type should be string and encode before sending 
            
            t.add_measure(anchor,dist)
   if(len(lines)>2):
      P.solve()
      print(t.loc)
      ti=int(lines[0].split(',')[3].split(':')[1])
      RMSE(t.loc.x,t.loc.y,ti)


# Then the target location is:

c.send(d.encode())       
c.close() 
