import numpy as np
filepath="vel.dat"
data = "position.dat"
# vel=np.ones(100)
vel = {0:(1,0)}
position = [0 for i in range(100)]


# with open(filepath) as fp:
#    for line in fp:
#     #    print(line.split())
#        time=int(float(line.split()[1]))
#        velx=line.split()[2].split('(')[1].split(',')[0]
#        vely=line.split()[3].split(')')[0]
#     #    print(time)
#     #    print(velx)
#     #    print(vely)
#        vel[time]=velx,vely
last=(60.0,60.0)
with open(data) as fp:
   for line in fp:
       print(line.split())
       time=int(float(line.split()[1]))
       x=float(line.split()[2])
       y=float(line.split()[3])
       position[time]=x,y
       if(time not in vel):
            vel.update({time:(x-last[0],y-last[1])})
            print(x)
            print(y)
            print(last)
            print(time)
            last=(x,y)

print(vel)